from github import Github
import re
import base64
import pandas as pd

#g = Github("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",per_page=3)
#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
g = Github("",per_page=5)


count = 0

topic = ['unity', 'unity3d']

repo = g.search_repositories("topic:{}".format(topic[0]), sort='stars')
a = repo.get_page(0)
print(repo.totalCount)
print(len(a))

def fun(content, path):
    list = []
    rex = "/ ([A - Z])([A - Z])([a - z]) | ([a - z])([A - Z]) / g"

    "CSVFilesAreCoolButTXT".replace(rex, '$1$4 $2$3$5');
    regex = "(public|private|internal|protected|void)\s*" + \
            "(async)?\s*" + \
            "(static|virtual|abstract|void)?\s*" + \
            "(async)?\s*" + \
            "(Task)?\s*" + \
            "(?P<method>[A-Za-z_][A-Za-z_0-9]*\s*)\((([a-zA-Z\[\]\<\>]*\s*[A-Za-z_]*[A-Za-z_0-9]*\s*)[=]?[,]?\s*)+\)"

    # when not read binary, gives "charmap codec error"
    preContent = content.splitlines()
    #print("contentz", preContent)
    #lines = preContent.readlines()
    for index, line in enumerate(preContent):
        # re.compile takes a normal string
        # skip empty line or just {, } lines
        if line.strip() and line.strip() != '{' and line.strip() != '}':
            # print("Line {}: {}".format(index, line.strip()))
            for match in re.finditer(regex, line.strip()):
                # print('matched string =', match)
                spacedName = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', match['method'])
                namesWithPaths = {'name': match['method'], 'spacedName': spacedName, 'path': path+"#L"+str(index+1)}
                list.append(namesWithPaths)


                #print('matched method =', match['method'])
    return list


df = pd.DataFrame(columns=['name', 'repo'])

counter = 0
flag = False
aregex = '\b(public|private|internal|protected|void)\s*s*\b(async)?\s*' \
         '\b(static|virtual|abstract|void)?\s*\b(async)?\b(Task)?\s*[a-zA-Z]*(\s[A-Za-z_][A-Za-z_0-9]*\s*)\
         ((([a-zA-Z\[\]\<\>]*\s*[A-Za-z_][A-Za-z_0-9]*\s*)[,]?\s*)+\)'
regex = '([^{]*)((?:\{[^}]*\}|//.*\r?\n|"[^"]*"|[\S\s])*?\{(?:\{[^}]*\}|//.*\r?\n|"[^"]*"|[\S\s])*?)\}'
reg = '\b(public|private|internal|protected|void)\s*s*\b(async)?\s*\b(static|virtual|abstract|void)?\s*\b' \
      '(async)?\b(Task)?\s*[a-zA-Z]*(\s[A-Za-z_][A-Za-z_0-9]*\s*)\((([a-zA-Z\[\]\<\>]*\s*[A-Za-z_]' \
      '[A-Za-z_0-9]*\s*)[,]?\s*)+\)'

#a loop that lets us get all the pages in Paginated list

page = repo.get_page(0)
functionsMappedPaths = {}
listsOfLists = []
while(True):
    if flag:
        break
    for i in range(5):
        r = page[i]
        if not r:
            break
        else:
            if flag:
                break
            contents = r.get_contents("")
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir" and 'Assets/Scripts' in file_content.name:
                    contents.extend(r.get_contents(file_content.path))
                else:
                    if re.match(r'.*\.cs$', file_content.name):
                        #append df new row

                        df.loc[counter] = [file_content.name, r.url]
                        counter += 1
                        if counter == 5:
                            flag = True
                            break
                        print(file_content.name," - ",count)
                        count += 1
                        plain = base64.b64decode(file_content.content)
                        plain = plain.decode('utf-8')
                        functionNamesAndPaths = fun(plain, file_content.html_url)
                        listsOfLists.append(functionNamesAndPaths)
                        print(functionNamesAndPaths)

    page = repo._fetchNextPage()
    print("next page - ",page)

#convert df to csv
df.to_csv('data.csv', index=True)
