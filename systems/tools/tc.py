#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re


prev_sent = None
for line in sys.stdin:
    sent = line.rstrip()

    if prev_sent and re.search(r'[?!."\']$', prev_sent):
        sent = sent[0].upper() + sent[1:]
    sys.stdout.write(sent + "\n")

    prev_sent = sent
