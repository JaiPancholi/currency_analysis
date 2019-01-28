with open('python.txt', 'r') as fp:
    p = fp.readlines()

# define a set up tuples to detect types of syntax, and what highlight.js syntax to use.
syntax = {
    'meta': ('(@\w+)', 'meta'),
    'keyword': ('(for | in | range\(|set\(\)|def | date\()', 'keyword'),
    'comment': ('(#.*)', 'comment'),
    'title': ('span>(\w+)\(', 'title')
}
new_string = ''

# print(p)

def start_tag(word):
    return '<span class="hljs-'+word+'">'

def end_tag():
    return '</span>'

lines = []
import re
for line in p:
    for value in syntax.values():
        # value_regex = '|'.join(cell for cell in value[0])
        # print(value_regex)
        value_regex = value[0]
        # print(line)
        line = re.sub(value_regex, start_tag(value[1])+r'\1'+end_tag(), line).rstrip()
    
    lines.append(line)
    print(line.rstrip())

# print(lines)

with open('python.html', 'w') as fp:
    fp.write('\n'.join(cell for cell in lines))