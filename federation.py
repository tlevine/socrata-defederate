import re

def parse_page():
    return []

def parse_targets(html):
    srcs = html.xpath('//div[@class="browseFacets"]/div/h4/ul/li/a/img/@src')
    print srcs
    return [re.match(r'/api/domains/([^/]+)//icons/smallIcon', src).group(1) for src in srcs]

def parse_source(html):
    url = html.xpath('//meta[@property="og:url"]/@content')[0]
    return re.match(r'https://([^/]+)/browse/embed', url).group(1)
