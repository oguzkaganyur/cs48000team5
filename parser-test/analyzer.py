from collections import OrderedDict
import collections
from ntpath import join
import xmltodict as xd
def fileToDict(filename):
    with open(filename, 'r') as f:
        return xd.parse(f.read().encode('utf-8'))

def parseSpecifier(funtype):
    text = ''
    if 'specifier' in funtype.keys():
        if type(funtype['specifier']) == str:
            text += funtype['specifier']
        else:
            text += ' '.join(funtype['specifier'])
    return text + ' '

def parseTypeName(funtype):
    text = ''
    if 'name' in funtype.keys():
        if type(funtype['name']) == str:
            text += funtype['name']
        else:
            text += ' '.join(funtype['name'])
    return text + ' '

def parseFuncName(fun):
    text = ''
    if type(fun) == list:
        text += '.'.join(fun)
    elif type(fun) == str:
        text += fun
    else:
        if 'name' in fun.keys():
            if type(fun['name']) == str:
                text += fun['name']
            else:
                text += parseFuncName(fun['name'])
                #text += '.'.join(fun['name'])
    return text

def parseArguments(fun):
    text = ''
    return text

def hasGeneric(funName):
    if type(funName) == collections.OrderedDict:
        return'argument_list' in funName.keys()
    return False

def parseGeneric(funName):
    text = []
    if type(funName['argument_list']) == list:
        for arg in funName['argument_list']:
            text.append(arg['argument']['name'])
    else:
        text.append(funName['argument_list']['argument']['name'])
    return ', '.join(text)

def parseFunction(fun):
    if type(fun) == str:
        return
    else:
        text = ''
        text += parseSpecifier(fun['type']) + parseTypeName(fun['type']) + parseFuncName(fun)
        if hasGeneric(fun['name']):
            text += "<" + parseGeneric(fun['name']) + ">"
        #print(fun, end='\n\n\n')
        print(text)



def writeFunctionNames(fileObject):
    fileObject = fileObject['unit']
    if 'namespace' in fileObject.keys():
        fileObject = fileObject['namespace']['block']
    if 'class' in fileObject.keys():
        for c in fileObject['class']:
            for fun in c['block']['function']:
                parseFunction(fun)

obj = fileToDict('script.cs.parsed')
"""
Top level keys:
- unit
- namespace? > block
- class[] > block
- function[] > block 
"""
#print(obj['unit']['namespace']['block']['class'][0]['block']['function'][0]['name'])
writeFunctionNames(obj)