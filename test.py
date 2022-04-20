from github import Github
import re
import base64
import pandas as pd

g = Github("",per_page=5)

count = 0

topic = ['unity', 'unity3d']

repo = g.search_repositories("topic:{}".format(topic[0]), sort='stars')
a = repo.get_page(0)
print(repo.totalCount)
print(len(a))


df = pd.DataFrame(columns=['name', 'repo'])

counter = 0
flag = False
aregex = '\b(public|private|internal|protected|void)\s*s*\b(async)?\s*\b(static|virtual|abstract|void)?\s*\b(async)?\b(Task)?\s*[a-zA-Z]*(\s[A-Za-z_][A-Za-z_0-9]*\s*)\((([a-zA-Z\[\]\<\>]*\s*[A-Za-z_][A-Za-z_0-9]*\s*)[,]?\s*)+\)'
regex = '([^{]*)((?:\{[^}]*\}|//.*\r?\n|"[^"]*"|[\S\s])*?\{(?:\{[^}]*\}|//.*\r?\n|"[^"]*"|[\S\s])*?)\}'
reg = '\b(public|private|internal|protected|void)\s*s*\b(async)?\s*\b(static|virtual|abstract|void)?\s*\b(async)?\b(Task)?\s*[a-zA-Z]*(\s[A-Za-z_][A-Za-z_0-9]*\s*)\((([a-zA-Z\[\]\<\>]*\s*[A-Za-z_][A-Za-z_0-9]*\s*)[,]?\s*)+\)'

#a loop that lets us get all the pages in Paginated list

page = repo.get_page(0)
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
                        if counter == 1000:
                            flag = True
                            break
                        print(file_content.name," - ",count)
                        count += 1
                        plain = base64.b64decode(file_content.content)
                        plain = plain.decode('utf-8')
                        for x in re.findall(reg, plain):
                            lines = x[0].split('\n')
                            for line in lines:
                                if '{' not in line and '}' not in line:
                                    y=1
                                    #print(line.strip())
                        #print('\n\n\n\n\n')
    
    page = repo._fetchNextPage()
    print("next page - ",page)

#convert df to csv
df.to_csv('data.csv', index=True)

                
