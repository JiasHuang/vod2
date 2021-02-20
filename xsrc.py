import extractors

def getSource(url, fmt, ref):

    src = None
    cookies = None

    if url == '':
        src = None

    elif url[0] == '/':
        src = url

    elif url[0:4] != 'http':
        src = None

    else:
        src, cookies, ref = extractors.getSource(url, fmt, ref)

    if src:
        return src, cookies, ref

    raise Exception('GetSourceError')
    return None, None, None

def getSub(url, opt):
    return extractors.getSub(url, opt)

