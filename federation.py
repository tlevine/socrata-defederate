#!/usr/bin/env python
import os, re
import json
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

def build_json():
    htmls = [parse(os.path.join('homepages',homepage)).getroot() for homepage in os.listdir('homepages')]
    return json.dumps({
        'edges': reduce(lambda a,b: a + parse_page(b), htmls, []),
        'nodes': map(parse_source, htmls),
    })

if __name__ == '__main__':
    print build_json()
