# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

"""
The internal linter uses :mod:`pyflakes` as its base with the need for a :class:`pyflakes.reporter.Reporter` class
removed and the warnings passed as a list to the caller.
"""

import sys
import _ast

from pyflakes import checker


class LinterError(Exception):
    def __init__(self, filename):
        self.filename = filename
        self.message = 'linter error'

    def __str__(self):
        return self.message


class LinterUnexpectedError(LinterError):
    def __init__(self, filename):
        self.filename = filename
        self.message = '%s problem decoding source' % self.filename

    def __str__(self):
        return self.message


class LinterSyntaxError(LinterError):
    def __init__(self, filename, msg, lineno, offset, text):
        self.filename = filename
        self.message = msg
        self.lineno = lineno
        self.offset = offset
        self.text = text

    def __str__(self):
        return '%s:%d:%d: %s' % (self.filename, self.lineno, self.offset + 1, self.message)


def check(codeString, filename):
    """
    This is a reimplementation of :func:`pyflask.api.check` to output a list of warnings.

    :param codeString: the code to parse for issues
    :param filename: the source filename
    :return: list of :class:`pyflakes.messages.Message`

    See the pyflakes license in the LICENSE file.
    """
    # First, compile into an AST and handle syntax errors.
    try:
        tree = compile(codeString, filename, "exec", _ast.PyCF_ONLY_AST)
    except SyntaxError:
        value = sys.exc_info()[1]
        msg = value.args[0]

        (lineno, offset, text) = value.lineno, value.offset, value.text

        # If there's an encoding problem with the file, the text is None.
        if text is None:
            # Avoid using msg, since for the only known case, it contains a
            # bogus message that claims the encoding the file declared was
            # unknown.
            raise LinterUnexpectedError(filename)
        else:
            raise LinterSyntaxError(filename, msg, lineno, offset, text)
    except Exception:
        raise LinterUnexpectedError(filename)

    # Okay, it's syntactically valid.  Now check it.
    w = checker.Checker(tree, filename)
    w.messages.sort(key=lambda m: m.lineno)

    return w.messages
