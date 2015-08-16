# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

import os
import sys
import hashlib


def sha_hash_file(filepath):
    h = hashlib.sha1()
    with open(filepath, 'rb') as fp:
        h.update(fp.read())

    return h.hexdigest()
