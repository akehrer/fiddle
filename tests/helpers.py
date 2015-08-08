# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

import os
import sys

# A selection of phrases in different languages to test unicode
# http://www.columbia.edu/~kermit/utf8.html
ICANEATGLASS = {'ascii': 'I can eat glass',
                'sanscrit': '﻿काचं शक्नोम्यत्तुम् । नोपहिनस्ति माम् ॥',
                'greek': 'Μπορώ να φάω σπασμένα γυαλιά χωρίς να πάθω τίποτα.',
                'french': 'Je peux manger du verre, ça ne me fait pas mal.',
                'spanish': 'Puedo comer vidrio, no me hace daño.',
                'romanian': 'Pot să mănânc sticlă și ea nu mă rănește.',
                'icelandic': 'Ég get etið gler án þess að meiða mig.',
                'russian': 'Я могу есть стекло, оно мне не вредит.',
                'hawaiian': 'Hiki iaʻu ke ʻai i ke aniani; ʻaʻole nō lā au e ʻeha.'}

