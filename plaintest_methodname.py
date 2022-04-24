import re

regex = "(public|private|internal|protected|void)\s*" + \
        "(async)?\s*" + \
        "(static|virtual|abstract|void)?\s*" + \
        "(async)?\s*" + \
        "(Task)?\s*" + \
        "(?P<method>[A-Za-z_][A-Za-z_0-9]*\s*)\((([a-zA-Z\[\]\<\>]*\s*[A-Za-z_]*[A-Za-z_0-9]*\s*)[=]?[,]?\s*)+\)"

# when not read binary, gives "charmap codec error"
file = open('sample_code.txt', 'rb')
lines = file.readlines()
for index, line in enumerate(lines):
    # re.compile takes a normal string
    line = line.decode()
    # skip empty line or just {, } lines
    if line.strip() and line.strip() != '{' and line.strip() != '}':
        #print("Line {}: {}".format(index, line.strip()))
        for match in re.finditer(regex,line.strip()):
            #print('matched string =', match)
            print('matched method =', match['method'])

