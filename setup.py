from distutils.core import setup
import sys
# For cx-freeze to work on Windows install from here
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#cx_freeze
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": [], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="fIDDLE",
    version="0.1",
    author="Aaron Kehrer",
    author_email="akehrer@in2being.com",
    url="https://github.com/akehrer/fiddle",
    license="The MIT License (MIT)",
    windows=[{"script": "fIDDLE.py"}],
    options={"build_exe": build_exe_options},
    executables=[Executable("fIDDLE.py", base=base)]
)
