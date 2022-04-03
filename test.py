from github import Github
import re
import base64

g = Github("")

count = 0

topic = ['unity', 'unity3d']

repo = g.search_repositories("topic:{}".format(topic[0]))
a = repo.get_page(0)

for r in repo:
    contents = r.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir" and 'Assets/Scripts' in file_content.name:
            contents.extend(r.get_contents(file_content.path))
        else:
            if re.match(r'.*\.cs$', file_content.name):
                count += 1
                plain = base64.b64decode(file_content.content)
                rm = re.findall('\b(public|private|internal|protected|void)\s*s*\b(async)?\s*\b(static|virtual|abstract|void)?\s*\b(async)?\b(Task)?\s*[a-zA-Z]*(?<method>\s[A-Za-z_][A-Za-z_0-9]*\s*)\((([a-zA-Z\[\]\<\>]*\s*[A-Za-z_][A-Za-z_0-9]*\s*)[,]?\s*)+\)', plain.decode('utf-8'))

                print(rm)
                