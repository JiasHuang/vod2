import re

from .utils import *

VALID_URL = r'nbareplay|nbafullhd'

def extract_nbafullhd(url):
    objs = []
    for m in re.finditer(r'<iframe .*?>(.*?)</iframe>', load(url)):
        m_src = re.search(r'src="([^"]*)"', m.group(0))
        if m_src:
            link = urljoin(url, m_src.group(1))
            objs.append(videoObj(link, link))
    return objs

def extract_parts(url):
    objs = []
    for m in re.finditer(r'<a href="([^"]*)".*?>([\w\s]*)</span></a>', load(url)):
        link = urljoin(url, m.group(1))
        title = m.group(2)
        objs.append(pageObj(link, title))
    return objs

def extract_index():
    objs = []
    for page_no in range(3):
        page_url = 'https://nbareplay.net/page/%d/' %(page_no)
        objs.extend([obj.to_page() for obj in findImageLink(page_url)])
    return objs

def extract(url):
    if re.search('nbafullhd', url):
        return extract_nbafullhd(url)
    if url.endswith('com/'):
        return extract_index()
    return extract_parts(url)
