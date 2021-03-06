import re
import os

import xurl
import xproc

def unpackURL(url):
    txt = xurl.load(url)
    return unpack(txt)

def unpackFILE(local):
    txt = xurl.readLocal(local)
    return unpack(txt)

def parseCode(code):
    cnt_brace_start = 0
    cnt_brace_end = 0
    idx = 0
    func_start = 0
    func_end = 0
    for c in code:
        if c == '{':
            cnt_brace_start = cnt_brace_start + 1
            if func_start == 0:
                func_start = idx
        if c == '}':
            cnt_brace_end = cnt_brace_end + 1
            if cnt_brace_end == cnt_brace_start:
                func_end = idx
                break
        idx = idx + 1
    return code[func_start:func_end+1], code[func_end+1:-1]

def showAll(code, output):
    print('\n----------------------------------------------------- [packed] -------------------------------------------------------------\n\n')
    print(code or '')
    print('\n----------------------------------------------------- [unpack] -------------------------------------------------------------\n\n')
    print(output or '')
    print('\n----------------------------------------------------------------------------------------------------------------------------\n\n')

def unpack(txt):
    m = re.search('(eval\s*\(function\(p,a,c,k,e,d\)\{.+\))', txt)
    if m:
        code = m.group()
        func, args = parseCode(code)
        txt = 'function unpack(p,a,c,k,e,d)%s\nconsole.log(unpack%s);\n' %(func, args)
        output = executeJSCode(txt)
        showAll(code, output)
        return output
    return None

def executeJSCode(code):
    local = xurl.genLocal(str(os.getuid), prefix='vod_code_')
    xurl.saveLocal(local, code)
    try:
        output = xproc.checkOutput('nodejs '+local)
    except:
        return None
    output = output.replace("\/", "/")
    showAll(code, output)
    return output

