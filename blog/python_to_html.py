with open('python.txt', 'r') as fp:
    p = fp.readlines()

# define a set up tuples to detect types of syntax, and what highlight.js syntax to use.
# syntax = {
#     'function': ('(.*def .*)', 'function'),
#     'meta': ('(@\w+)', 'meta'),
#     'keyword': ('(for | in | range\(| set|def|date)', 'keyword'),
#     'comment': ('(#.*)', 'comment'),
#     'title': ('def.* (\w+s)', 'title'),
# }

syntax = {
    'function': (['(.*def .*)'], 'function'),
    'meta': (['(@\w+)'], 'meta'),
    'keyword': (['(for) ',' (in) ',' (range)\(', ' (set)\(', '(def) ', '(date)\(2000,'], 'keyword'),
    # 'keyword': (['(for) ',' (in) ',' (range)\(', ' (set)\(', '(def) '], 'keyword'),
    # 'keyword': (['(for) ',' (in) ',' (range)\(', ' (set)\(', '(def) ', '[^_](date)\(20'], 'keyword'),
    'comment': (['(#.*)'], 'comment'),
    'title': (['def.* (\w+s)'], 'title'),
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

        # replace whole line with the match wrapped in quotes
        # line = re.sub(value_regex, start_tag(value[1])+r'\1'+end_tag(), line).rstrip()
        # line = re.sub(value_regex, '__START__'+r'\1'+'__END__', line).rstrip()
        for value_regex in value_regex:
            print(value_regex, 'regex')
            # replace match with match wrapped in quotes
            matches = re.search(value_regex, line)
            if matches:
                match = matches.group(1)
                match_escape = re.escape(match)
                print(match)
                # line = re.sub(match_escape, '__START__'+match+'__END__', line).rstrip()
                line = re.sub(match_escape, start_tag(value[1])+match+end_tag(), line).rstrip()

        # replace the match with the match wrapped in quotes
        # line = re.sub(value_regex, start_tag(value[1])+r'\1'+end_tag(), line).rstrip()

    
    lines.append(line)
    print(line.rstrip())

# print(lines)

with open('python.html', 'w') as fp:
    fp.write('\n'.join(cell for cell in lines))