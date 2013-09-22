import re

def parse_page():
    return []

def parse_targets(html):
    srcs = html.xpath('//h4[text()="Federated Domains"]/following-sibling::ul[position()=1]/li/a/img/@src')
    return [re.match(r'/api/domains/([^/]+)/icons/smallIcon', src).group(1) for src in srcs[1:]]

def parse_source(html):
    url = html.xpath('//meta[@property="og:url"]/@content')[0]
    return re.match(r'https://([^/]+)/browse/embed', url).group(1)
