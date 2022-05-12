from github import Github
import re
import base64
import pymongo
import pandas as pd

g = Github("", per_page=90)

topic = ['unity3d']
user = ['Brackeys/Scriptable-Objects']
client = pymongo.MongoClient(
    "mongodb+srv://cs48000team5:mGTDtJJfQhSVQn4@cluster0.bzb9t.mongodb.net/app?retryWrites=true&w=majority", 27017,
    tls=True, tlsAllowInvalidCertificates=True)
db = client.app
collection = db['functions']

#repo = g.search_repositories("repo:{}".format(user[0]), sort='stars')
repo = g.get_user("SebLague").get_repos()
a = repo.get_page(0)
print(repo.totalCount)
print(len(a))

import itertools
from collections import deque


def count_iter_items(iterable):
    """
    Consume an iterable not reading it into memory; return the number of items.
    """
    counter = itertools.count()
    deque(itertools.izip(iterable, counter), maxlen=0)  # (consume at C speed)
    return next(counter)


async def getIter(regex, line):
    return re.finditer(regex, line.strip())


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
    # print("contentz", preContent)
    # lines = preContent.readlines()
    for index, line in enumerate(preContent):
        # print("1. LOOP")
        # print("index ", index)
        # print("path: ", path)
        # re.compile takes a normal string
        # skip empty line or just {, } lines

        if line.count("(") != line.count(")"):
            continue

        if line.strip() and line.strip() != '{' and line.strip() != '}' and "=" not in line.strip() and "@" not in line.strip() and len(
                line.strip()) < 100 and "?" not in line.strip() and "!" not in line.strip() and "&" not in line.strip()\
                and "*" not in line.strip() and "." not in line.strip():
            # print("Line {}: {}".format(index, line.strip()))

            #async with async_timeout.timeout(5):
            myIter = re.finditer(regex, line.strip())
            for match in myIter:
                # print("2. LOOP")
                # print('matched string =', match)
                spacedName = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', match['method'])
                namesWithPaths = {'name': match['method'], 'spacedName': spacedName,
                                  'path': path + "#L" + str(index + 1)}
                list.append(namesWithPaths)

                # print('matched method =', match['method'])
    return list


def mainFunc():
    df = pd.DataFrame(columns=['name', 'repo'])
    count = 0
    counter = 0
    flag = False

    # a loop that lets us get all the pages in Paginated list
    repoCount = 0
    page = repo.get_page(0)
    functionsMappedPaths = {}
    listsOfLists = []

    while (True):
        if flag:
            break
        for i in range(90):
            repoCount += 1
            r = page[i]
            if not r:
                break
            else:
                if flag:
                    break
                contents = r.get_contents("")
                print("repocount: ", repoCount, " repo url: ", r.url)
                while contents:
                    file_content = contents.pop(0)
                    if file_content.type == "dir":
                        # print("filecontent.path: ", file_content.path)
                        contents.extend(r.get_contents(file_content.path))
                    else:
                        print("else file content path: ", file_content.path)
                        if 'Assets' in file_content.path:
                            if re.match(r'.*\.cs$', file_content.name):
                                # append df new row

                                df.loc[counter] = [file_content.name, r.url]
                                counter += 1
                                if counter == 100000:
                                    flag = True
                                    break

                                print(file_content.name, " - ", count)
                                count += 1
                                plain = base64.b64decode(file_content.content)
                                plain = plain.decode('utf-8')
                                functionNamesAndPaths = fun(plain, file_content.html_url)
                                listsOfLists.append(functionNamesAndPaths)
                                if len(functionNamesAndPaths) != 0:
                                    collection.insert_many(functionNamesAndPaths)
                                print(functionNamesAndPaths)

        print("next page - ", page)
        page = repo._fetchNextPage()


mainFunc()
