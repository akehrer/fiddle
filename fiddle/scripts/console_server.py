#!/usr/bin/env python
"""
A remote interactive Python server
from: http://www.shysecurity.com/posts/Remote%20Interactive%20Python
2014-12-04: Did some clean-up (AK)
"""
import socket
import sys
import contextlib


HOST = '127.0.0.1'
PORT = 3000
BANNER = 'Python %s on %s' % (sys.version, sys.platform)

@contextlib.contextmanager
def std_redirector(stdin, stdout, stderr):
    orig_fds = sys.stdin, sys.stdout, sys.stderr
    sys.stdin, sys.stdout, sys.stderr = stdin, stdout, stderr
    yield
    sys.stdin, sys.stdout, sys.stderr = orig_fds


class SocketWrapper(object):
    def __init__(self, s):
        self.s = s

    def read(self, len):
        return self.s.recv(len)

    def write(self, str):
        return self.s.send(str)

    def readline(self):
        data = ''
        while True:
            iota = self.read(1)
            if not iota:
                break
            else:
                data += iota
            if iota in '\n': break
        return data


def ishell(local=None, banner=BANNER):
    import code
    local = dict(globals(), **local) if local else globals()
    code.interact(banner, local=local)


def linkup(local, link, banner=BANNER):
    # import traceback
    link = SocketWrapper(link)
    # banner += '\nStack Trace\n'
    # banner += '----------------------------------------\n'
    # banner += ''.join(traceback.format_stack()[:-2])
    # banner += '----------------------------------------\n'
    with std_redirector(link, link, link):
        ishell(local, banner)


def listen(local=None, host=HOST, port=PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host,port))
    server.listen(1)
    client,addr = server.accept()
    linkup(local, client)  # , 'connected to %s:%d'%(host,port))
    client.shutdown(socket.SHUT_RDWR)
    server.shutdown(socket.SHUT_RDWR)


def connect(local=None, host=HOST, port=PORT):
    link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    link.connect((host,port))
    linkup(local, link)  # , 'connected to %s:%d'%(host,port))
    link.shutdown(socket.SHUT_RDWR)

if __name__ == '__main__':
    print('Python InteractiveConsole server started at {0}:{1}'.format(HOST, PORT))
    listen()
    connect()