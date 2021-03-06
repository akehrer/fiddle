from distutils.core import setup, Command
import fileinput
import os
import subprocess
import logging
import sys
# For cx-freeze to work on Windows install from here
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#cx_freeze
from cx_Freeze import setup, Executable

from fiddle.config import LOG_LEVEL
from fiddle import __version__

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    'packages': [],
    'excludes': ['tkinter', 'lib2to3'],
    'zip_includes': [],
    'bin_excludes': [],
    'includes': [
        'PyQt4.QtNetwork',
        'PyQt4.QtWebKit',
        'PyQt4.Qsci'],
    'include_files': [
        'locale/',
        'LICENSE',
        'searchers.json'],
    'include_msvcr': False}


# ##### Missing includes #####
# lib2to3 needs to load its Grammar files at run time, but cannot open them when they are included in the cx_Freeze
# `library.zip` file.  The module is excluded in the options and then copied over here in the include_files.
import lib2to3
lib23_path = os.path.dirname(lib2to3.__file__)
build_exe_options['include_files'].append(lib23_path)

# ##### Platform Specific Parameters #####
base = None
icon = None
if sys.platform == 'win32':
    # GUI applications require a different base on Windows (the default is for a console application).
    # Hide the console window in Windows
    base = 'Win32GUI'
    build_exe_options['include_msvcr'] = True
    target_name = 'fiddle.exe'
    icon = os.path.join('.', 'media', 'icons', 'fiddle_icon_light.ico')
elif sys.platform == 'darwin':
    # exclude: libQsci.dylib
    # the compiled file is copied from libQsci.dylib to Qsci.so during build process
    # this leaves the original library name intact and cx_Freeze cannot detect this
    # so to get this to build cleanly, need to exclude libQsci.dylib file
    # Thanks to the RAFT project for this hint…
    # build_exe_options['bin_excludes'].append('libQsci.dylib')
    excludes = ['Qsci',
                'QtCore',
                'QtDeclarative',
                'QtDesigner',
                'QtGui',
                'QtHelp',
                'QtMultimedia',
                'QtNetwork',
                'QtOpenGL',
                'QtScript',
                'QtScriptTools',
                'QtSql',
                'QtSvg',
                'QtTest',
                'QtWebKit',
                'QtXml',
                'QtXmlPatterns']
    for e in excludes:
        build_exe_options['bin_excludes'].append('lib%s.dylib' % (e))
    target_name = 'fiddle'
    icon = os.path.join('.', 'media', 'icons', 'fiddle_icon_light.hqx')
else:
    target_name = 'fiddle.py'


# ##### Version #####
# Update the module version based on:
# https://github.com/warner/python-ecdsa/blob/9e21c3388cc98ba90877a1e4dbc2aaf66c67d365/setup.py#L33
VERSION = __version__


def update_version_py():
    if not os.path.isdir(".git"):
        print("This does not appear to be a Git repository.")
        return
    try:
        p = subprocess.Popen(["git", "describe",
                              "--tags", "--dirty", "--always"],
                             stdout=subprocess.PIPE)
    except EnvironmentError:
        print("Unable to run git, leaving fiddle/__init__.py version alone")
        return
    gitout = p.communicate()[0]
    if p.returncode != 0:
        print("Unable to run git, leaving fiddle/__init__.py version alone")
        return
    ver = gitout.decode().strip()
    for line in fileinput.input('fiddle/__init__.py', inplace=True):
        if line.startswith('__version__'):
            print(
                "__version__ = '{0}'  # autogenerated from Git (see setup.py)".format(ver))
        else:
            print(line, end='')
    print("Set fiddle/__init__.py version to '%s'" % ver)
    return ver


class Version(Command):
    description = "Update __init__.py version from Git repo"
    user_options = []
    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        ver = update_version_py()
        VERSION = ver
        print("Version is now", VERSION)


# ##### Setup #####
setup(
    name='fiddle',
    version=VERSION,
    author='Aaron Kehrer',
    author_email='akehrer@gmail.com',
    url='https://github.com/akehrer/fiddle',
    license='The MIT License (MIT)',
    windows=[{'script': 'fiddle.py'}],
    options={'build_exe': build_exe_options},
    executables=[Executable('fiddle.py', base=base, targetName=target_name, icon=icon)],
    cmdclass={'version': Version}
)
