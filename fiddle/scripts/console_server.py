#!/usr/bin/python
#-- Content-Encoding: UTF-8 --
"""
A simple Python remote console script.
From: http://www.coderxpress.net/blog-dl/python-remote-console.py

Based on multiple scripts found on the Internet, mainly :
* http://evadeflow.com/2010/03/python-console-for-ig/
* http://snipperize.todayclose.com/snippet/py/Network-TCP-backend-for-console-access--25356/

:author: Thomas Calmant (thomas [dot] calmant [at] gmail [dot] com)
:license: MIT
"""

from contextlib import contextmanager
from select import select

# Common imports
import code
import os
import socket
import sys
import threading
import time

PYTHON3 = sys.version_info[0] == 3
if PYTHON3:
    # Python 3 imports
    from io import StringIO
    import socketserver
else:
    from cStringIO import StringIO
    import SocketServer as socketserver

# ------------------------------------------------------------------------------

class FakeOut(object):
    """
    Fakes the write method, if a thread register himself with a different writer
    the new writer is used when writing on this.
    Otherwise default writer is used
    """

    def __init__(self, default):
        """
        Sets up members
        
        :param default: Default stream
        """
        self.default = default
        self.others = {}
        self._lock = threading.Lock()


    def set_thread_output(self, thread, outstream):
        """
        Sets the output stream for the given thread
        """
        with self._lock:
            self.others[thread] = outstream


    def unset_thread(self, thread):
        """
        Unset the output stream for the given thread
        """
        with self._lock:
            if thread in self.others:
                del self.others[thread]


    def write(self, data):
        """
        Writes some data to the current thread stream
        
        :param data: Data to be written
        """
        thread = threading.current_thread()
        with self._lock:
            if thread in self.others:
                self.others[thread].write(data)
            else:
                self.default.write(data)


    def __getattr__(self, name):
        """
        Proxify attribute accesses to the stream members
        """
        thread = threading.current_thread()
        with self._lock:
            if thread in self.others:
                return getattr(self.others[thread], name)
            else:
                return getattr(self.default, name)

# ------------------------------------------------------------------------------

class Interpreter(code.InteractiveConsole):
    """
    Interactive console with redirected output, using StringIO
    """
    def __init__(self, itp_locals=None):
        """
        Sets up the console
        
        :param itp_locals: Interpreter itp_locals
        """
        code.InteractiveConsole.__init__(self, locals=itp_locals)
        self.ps1 = getattr(sys, "ps1", ">>> ")
        self.ps2 = getattr(sys, "ps2", "... ")
        self.banner = ("Python %s\n%s\n" % (sys.version, sys.platform) +
                       'Type "help", "copyright", "credits" or "license" '
                       'for more information.\n')

        self._more = False
        self._buffer = StringIO()


    def push(self, command):
        """
        Push a command to the interpreter
        
        :param command: A command line to push to the interpreter
                        (can be incomplete)
        :return: (more, output) tuple. If more is True, the line needs to be
                 completed. 
        """
        if self._more:
            if len(command.strip()) != 0:
                # Continue reading a multi-line command
                self._buffer.write(command)
                return self._more

            else:
                # End of a multi-line command
                command = self._buffer.getvalue()
                self._buffer.truncate(0)

        try:
            self._more = code.InteractiveConsole.push(self, command)

        except (SyntaxError, OverflowError):
            # Ignore errors
            self._more = False

        return self._more

# ------------------------------------------------------------------------------

class SharedBoolean(object):
    """
    Shared boolean between objects / threads
    """
    def __init__(self, value=False):
        """
        Set up members
        """
        self._lock = threading.Lock()
        self._value = value


    def get_value(self):
        """
        Retrieves the boolean value
        """
        with self._lock:
            return self._value


    def set_value(self, value):
        """
        Sets the boolean value
        """
        with self._lock:
            self._value = value

# ------------------------------------------------------------------------------

class RemoteConsole(socketserver.StreamRequestHandler):
    """
    Handles incoming connections and redirect network incomings to a Python
    interpreter
    """
    def __init__(self, active_flag, *args):
        """
        Sets up members
        
        :param active_flag: Common flag for stopping the client communication
        """
        self._active = active_flag
        socketserver.StreamRequestHandler.__init__(self, *args)


    def send(self, data):
        """
        Send data to the client
        
        :param data: Data to be sent
        """
        if data is not None:
            data = data.encode("UTF-8")

        self.wfile.write(data)
        self.wfile.flush()


    def _local_print(self, string):
        """
        Prints on local output
        """
        sys.stdout.default.write("{0}\n".format(string))
        sys.stdout.default.flush()


    def handle(self):
        """
        Creates a new thread, with modified streams, to answer the client
        """
        # We do it in a thread to joke the stdout 
        thread = threading.Thread(target=self._inner_loop)
        thread.start()

        # Wait for the thread to end because exiting from here shuts down
        #Â the connection
        thread.join()


    def _inner_loop(self):
        """
        Handles a TCP client
        """
        self._local_print("Client connected: [%s]:%d" % self.client_address)

        thread = threading.current_thread()
        sys.stdout.set_thread_output(thread, self.wfile)
        sys.stderr.set_thread_output(thread, self.wfile)

        # The interpreter uses a copy the globals
        #Â (to avoid sharing data between clients)
        py = Interpreter(dict(globals()))

        # Print the banner and the first prompt
        self.send(py.banner)
        self.send(py.ps1)

        try:
            while self._active.get_value():
                # Wait for data
                r = select([self.rfile], [], [], .5)[0]
                if len(r) == 0:
                    # Nothing to do (poll timed out)
                    continue

                data = self.rfile.readline().decode("UTF-8")
                if len(data) == 0:
                    # End of stream (client gone)
                    break

                # Strip the line but ensure we have a new line character
                line = data.rstrip() + "\n"

                # Add the line to the console
                more = py.push(line)

                # Write the prompt
                if more:
                    self.send(py.ps2)

                else:
                    self.send(py.ps1)

        finally:
            sys.stderr.unset_thread(thread)
            sys.stdout.unset_thread(thread)

            self._local_print("Client gone: [%s]:%d" % self.client_address)
            try:
                # Be polite, if possible
                self.send("\nServer closed. Good bye.\n")
            except:
                # Can't send data anymore
                pass

# ------------------------------------------------------------------------------

def createServer(ip, port):
    """
    Creates the TCP console on the given ip and port
    
    :param ip: Server IP
    :param port: Server port
    :return: server thread, TCP server object
    """
    # Set up the request handler creator
    active_flag = SharedBoolean(True)
    request_handler = lambda *args: RemoteConsole(active_flag, *args)

    # Set up the server
    server = socketserver.ThreadingTCPServer((ip, port), request_handler, False)

    # Set flags
    server.daemon_threads = True
    server.allow_reuse_address = True

    # Activate the server
    server.server_bind()
    server.server_activate()

    # Serve clients
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    return (server_thread, server, active_flag)

# ------------------------------------------------------------------------------

running = True

def _stop():
    """
    Stops the main loop
    """
    global running
    running = False
    print("Server STOP flag setter called")


def main(host=None, port=None):
    """
    Entry point
    """
    # Fake outputs
    sys.stderr = FakeOut(sys.stderr)
    sys.stdout = FakeOut(sys.stdout)

    # Analyse the host parameter
    if host is None:
        try:
            host = sys.argv[1]
        except:
            # Default host
            host = '127.0.0.1'

    # Analyse the port parameter
    if port is None:
        try:
            port = int(sys.argv[2])
        except:
            # Default port
            port = 3000

    # Print server IP and port
    print("Starting server on [%s]:%d... (PID: %d)" % (host, port, os.getpid()))
    thread, srv, active_flag = createServer(host, port)

    global running
    try:
        print("Waiting for server to stop or interruption")
        while running:
            thread.join(1)
    except:
        # Jump off the loop on exception
        running = False

    try:
        # Stop the server
        srv.shutdown()
        thread.join(5)
    except:
        # Ignore exception
        pass

    # Tell clients to get out
    active_flag.set_value(False)

    print("Waiting for remaining clients to be kicked")
    while threading.active_count() > 1:
        # Two threads by client (request thread, console thread)
        print("Waiting for %d client(s)" % ((threading.active_count() - 1) / 2))
        time.sleep(.5)

    # srv.socket.shutdown(socket.SHUT_RDWR)
    srv.server_close()
    print("Server closed")

    print("Bye !")

if __name__ == "__main__":
    main()