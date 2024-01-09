#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Author: Manuel Bucher <dev@manuelbucher.com>
# Date: 2024-01-08

# Convert github issue meeting notes to markdown document
# Downloaded with curl, see [rate_limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28)
# 
#     for i in {1..85}; do curl https://api.github.com/repos/mozilla-necko/meeting-notes/issues/$i/timeline > $i.json; done

import json

author = {
        'valenting': 'Valentin',
        'mayhemer': 'mayhemer',
        'JuniorHsu': 'Junior',
        'vonasek': 'Michal',
        'selenamarie': 'Selena',
        'KershawChang': 'Kershaw',
        'ddragana': 'Dragana',
        'agrover': 'Andy',
        'nhi-nguyen': 'Nhi',
        'undef1nd': 'Tania',
}

def to_md(issue, j):
    time = j[0]['created_at']
    date = time.split('T', 2)[0]
    md = ''
    for comment in j:
        if 'body' not in comment:
            continue
        a = comment['user']['login']
        body = comment['body']
        md += '\n## ' + author[a] + '\n\n' + body + '\n'

    creator = issue['user']['login']
    out = issue['body']

    num_empty = 0
    comment = False
    for line in md.splitlines():
        line = line + '\n'
        start = line.strip()
        if start.startswith('```'):
            comment = not comment
        if start == "":
            if num_empty == 0:
                out += "\n"
            num_empty += 1
            continue
        else:
            num_empty = 0
        start = start[0]
        out += line
        if start != '-' and start != '*' and not line[0].isspace() and not comment:
            out += '\n'
            num_empty = 1
    out = f'# Meeting {date}\n' + out

    return date, out

def main():
    for i in range(1, 86):
        if i == 8:
            continue
        issue = json.load(open("issue-" + str(i) + ".json"))
        inp = json.load(open(str(i) + ".json"))
        date, out = to_md(issue, inp)
        file_name = "../archive/meeting-" + date + ".md"
        with open(file_name, 'w') as f:
            f.write(out)

if __name__ == '__main__':
    main()

