#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Author: Manuel Bucher <dev@manuelbucher.com>
# Date: 2023-01-09

# This file fixes new line management from github flavored markdown to commonmark

import sys

def rewrite_newlines(inp):
    out = ""

    num_empty = 0 # max 2 newlines
    code = False
    for line in inp:
        start = line.strip()
        if start == "":
            if num_empty == 0:
                out += "\n"
            num_empty += 1
            continue
        else:
            num_empty = 0
        if start.startswith('```'):
            code = not code
        start = start[0]
        out += line
        if start != '-' and start != '*' and not line[0].isspace() and not code:
            out += '\n'
            num_empty = 1
    return out

def main():
    for file in sys.argv[1:]:
        inp = open(file).readlines()
        out = rewrite_newlines(inp)
        with open(file, 'w') as f:
            f.write(out)

if __name__ == '__main__':
    main()

