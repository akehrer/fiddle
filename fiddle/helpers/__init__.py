# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)
import sys
import subprocess


def find_python_exe():
    """
    Find the path to the system's Python executable
    :return: str
    """
    try:
        if sys.platform == 'win32':
            p = subprocess.check_output(['where', 'python'])
        else:
            p = subprocess.check_output(['which', 'python'])
        return p.strip().decode('utf8')
    except subprocess.CalledProcessError:
        return ''


def get_python_version(exe_path):
    """
    Get the version list [major, minor, patch] of a Python executable
    :param str exe_path:
    :return: list
    """
    try:
        p = subprocess.Popen([exe_path, '-c', 'import platform; print(platform.python_version())'],
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        out, err = p.communicate(timeout=0.5)
        return out.decode().strip().split('.')
    except subprocess.TimeoutExpired:
        return ['', '', '']


# This is the Python script to check if the interpreter is running in a virtual environment
venv_check_script = """import sys
if sys.version[0] == '2':
    print(hasattr(sys, 'real_prefix'))
else:
    print(sys.prefix != sys.base_prefix)
"""


def check_virtualenv(exe_path):
    """
    Check to see if the Python executable is part of a virtual environment

                 | prefix | base_prefix  | real_prefix  |
    Python 2.7   | True   | False        | False        |
    Python 2.7 VE| True   | False        | True         |
    Python 3.4   | True   | True(=prefix)| False        |
    Python 3.4 VE| True   | True         | False        |

    :param str exe_path:
    :return: boolean
    """
    try:
        p = subprocess.Popen([exe_path, '-c', venv_check_script],
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        out, err = p.communicate(timeout=0.5)
        return True if out.decode().strip().lower() == 'true' else False
    except subprocess.TimeoutExpired:
        return False
