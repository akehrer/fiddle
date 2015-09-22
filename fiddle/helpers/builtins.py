# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

py3_keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
                'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
                'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'] + ['self', 'cls']


py2_keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec',
                'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print',
                'raise', 'return', 'try', 'while', 'with', 'yield'] + ['self', 'cls']

# All Python keywords between 2 and 3
python_all_keywords = ['global', 'not', 'print', 'def', 'return', 'for', 'as', 'del', 'or', 'class', 'and', 'else',
                       'exec', 'raise', 'elif', 'self', 'pass', 'if', 'try', 'from', 'import', 'with', 'while', 'yield',
                       'break', 'lambda', 'assert', 'in', 'is', 'except', 'cls', 'continue', 'finally']


py3_builtins = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError',
                'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError',
                'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError',
                'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FileExistsError', 'FileNotFoundError',
                'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning',
                'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError',
                'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'None', 'NotADirectoryError',
                'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning',
                'PermissionError', 'ProcessLookupError', 'ReferenceError', 'ResourceWarning', 'RuntimeError',
                'RuntimeWarning', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit',
                'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError',
                'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning',
                'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '_', '__build_class__', '__debug__',
                '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'all', 'any',
                'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex',
                'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'execfile',
                'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help',
                'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals',
                'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property',
                'quit', 'range', 'repr', 'reversed', 'round', 'runfile', 'set', 'setattr', 'slice', 'sorted',
                'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']

py3_exceptions = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError',
                  'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError',
                  'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError',
                  'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FileExistsError', 'FileNotFoundError',
                  'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning',
                  'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError',
                  'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'None', 'NotADirectoryError',
                  'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning',
                  'PermissionError', 'ProcessLookupError', 'ReferenceError', 'ResourceWarning', 'RuntimeError',
                  'RuntimeWarning', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit',
                  'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError',
                  'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning',
                  'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError']

py2_builtins = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError', 'BytesWarning',
                'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False',
                'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning',
                'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError',
                'NameError', 'None', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
                'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StandardError',
                'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'True',
                'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError',
                'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError',
                'ZeroDivisionError', '__debug__', '__doc__', '__import__', '__name__', '__package__', 'abs', 'all',
                'any', 'apply', 'basestring', 'bin', 'bool', 'buffer', 'bytearray', 'bytes', 'callable', 'chr',
                'classmethod', 'cmp', 'coerce', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir',
                'divmod', 'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 'float', 'format', 'frozenset',
                'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'intern', 'isinstance',
                'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'long', 'map', 'max', 'memoryview', 'min',
                'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'raw_input',
                'reduce', 'reload', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod',
                'str', 'sum', 'super', 'tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange', 'zip']

py2_exceptions = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError', 'BytesWarning',
                  'DeprecationWarning', 'EOFError', 'EnvironmentError', 'Exception', 'FloatingPointError',
                  'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError',
                  'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError',
                  'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'ReferenceError',
                  'RuntimeError', 'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError', 'SyntaxWarning',
                  'SystemError', 'SystemExit', 'TabError', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError',
                  'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning',
                  'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError']


# All Python __builtins__ between 2 and 3
python_all_builtins = ['BrokenPipeError', 'round', 'bytes', 'staticmethod', 'IndentationError', 'dir', 'open', 'hex',
                       'ConnectionResetError', '__debug__', 'set', 'None', 'UnicodeTranslateError', 'compile',
                       'BytesWarning', 'RuntimeError', 'float', 'id', 'ZeroDivisionError', 'oct', 'EnvironmentError',
                       '__import__', 'IOError', 'sorted', 'dict', 'iter', 'locals', 'complex', 'format', 'divmod',
                       'zip', 'RuntimeWarning', 'copyright', 'delattr', 'tuple', 'FloatingPointError', 'frozenset',
                       'globals', 'SyntaxWarning', 'IndexError', 'runfile', 'ValueError', 'FutureWarning', 'bin',
                       'classmethod', 'EOFError', 'memoryview', 'issubclass', 'WindowsError', 'ImportWarning', 'abs',
                       'next', 'UnicodeDecodeError', 'hash', 'ascii', 'ReferenceError', 'pow', 'FileExistsError', 'any',
                       'getattr', 'sum', 'ProcessLookupError', 'MemoryError', 'help', 'slice', 'ConnectionAbortedError',
                       'map', 'exit', '_', '__build_class__', '__loader__', 'filter', 'NameError', 'GeneratorExit',
                       'max', 'NotImplemented', 'PermissionError', 'UnicodeWarning', 'property', '__spec__', 'all',
                       'super', 'UnicodeError', 'ord', 'BaseException', 'Ellipsis', 'str', 'AttributeError',
                       'ImportError', 'KeyboardInterrupt', 'UnicodeEncodeError', 'int', 'True', 'reversed', 'quit',
                       'FileNotFoundError', 'SystemError', 'UnboundLocalError', 'StopIteration', 'False', 'KeyError',
                       'OSError', 'len', 'vars', 'hasattr', 'input', 'object', '__doc__', 'LookupError', 'callable',
                       'ArithmeticError', 'NotADirectoryError', 'ChildProcessError', 'bytearray', 'list', 'type',
                       'TabError', 'execfile', 'isinstance', 'print', 'ResourceWarning', 'ConnectionRefusedError',
                       'credits', 'setattr', 'repr', 'AssertionError', 'SyntaxError', 'Exception', 'ConnectionError',
                       '__package__', 'UserWarning', 'exec', 'IsADirectoryError', 'NotImplementedError', 'SystemExit',
                       'enumerate', 'eval', 'InterruptedError', 'DeprecationWarning', 'range', '__name__', 'TypeError',
                       'PendingDeprecationWarning', 'min', 'BlockingIOError', 'BufferError', 'TimeoutError', 'Warning',
                       'license', 'OverflowError', 'bool', 'chr']
