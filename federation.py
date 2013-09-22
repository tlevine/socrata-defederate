#!/usr/bin/env python
import os, re
from lxml.html import parse

def parse_page(html):
    source = parse_source(html)
    targets = parse_targets(html)
    return [(source,target) for target in targets]

def parse_targets(html):
    srcs = html.xpath('//h4[text()="Federated Domains"]/following-sibling::ul[position()=1]/li/a/img/@src')
    return [re.match(r'/api/domains/([^/]+)/icons/smallIcon', src).group(1) for src in srcs[1:]]

def parse_source(html):
    url = html.xpath('//meta[@property="og:url"]/@content')[0]
    return re.match(r'https://([^/]+)/browse/embed', url).group(1)

def iterhtml():
    'Returns an iterator of lxml html elements'
    for homepage in os.listdir('homepages'):
        yield parse(os.path.join('homepages',homepage)).getroot()

if __name__ == '__main__':
    import json
    # Print out an adjacency list.
    print json.dumps(reduce(lambda a,b: a + parse_page(b), iterhtml(), []))
