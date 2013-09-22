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

def build_d3_json():
    htmls = [parse(os.path.join('homepages',homepage)).getroot() for homepage in os.listdir('homepages')]

    nodes_set = set(map(parse_source, htmls))
    links_list = reduce(lambda a,b: a + parse_page(b), htmls, [])
    for link in links_list:
        nodes_set = nodes_set.union(link)

    nodes = sorted(nodes_set)
    links = [{'source': nodes.index(link[0]), 'target': nodes.index(link[1])} for link in links_list]

    return json.dumps({
        'links': links,
        'nodes': [{'name': node} for node in nodes],
    })

if __name__ == '__main__':
    print build_d3_json()
