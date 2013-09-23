import os, json, re

from lxml.html import fromstring
import nose.tools as n

import federation

def check_parse_targets(filename):
    html = fromstring(open(filename).read())
    expected = json.load(open(filename.replace('.html', '.json')))
    observed = federation.parse_targets(html)
    n.assert_list_equal(observed, expected)
    for item in observed:
        n.assert_equal(type(item), unicode)

def check_parse_source(filename):
    html = fromstring(open(filename).read())
    observed = federation.parse_source(html)

    expected = unicode(re.match(r'.*/([^/]+)\.html', filename).group(1))

    n.assert_equal(type(observed), type(expected))
    n.assert_equal(observed, expected)
    n.assert_equal(type(observed), unicode)

def test_parse_targets_snippet():
    html = fromstring('''
    <div class="browseFacets ">
      <div class="facetSection clearfix federation_filter">
          <h4 class="title">Federated Domains</h4>
            <ul>
                <li><a href="/browse/embed?federation_filter=162&utf8=%E2%9C%93" class=""><img class="customIcon" src="/api/domains/data.hawaii.gov/icons/smallIcon" alt="icon" />This site only</a></li>
                <li><a href="/browse/embed?federation_filter=19&utf8=%E2%9C%93" class=""><img class="customIcon" src="/api/domains/explore.data.gov/icons/smallIcon" alt="icon" />explore.data.gov</a></li>
            </ul>
        </div>
      </div>
''')
    observed = federation.parse_targets(html)
    expected = ['explore.data.gov']
    n.assert_list_equal(observed, expected)

def test_parse_targets():
    for basename in os.listdir('fixtures'):
        if basename.endswith('.html'):
            yield check_parse_targets, os.path.join('fixtures', basename)

def test_parse_source():
    for basename in os.listdir('fixtures'):
        if basename.endswith('.html'):
            yield check_parse_source, os.path.join('fixtures', basename)

def test_parse_page():
    html = fromstring(open(os.path.join('fixtures', 'explore.data.gov.html')).read())
    expected = [
        ('explore.data.gov', 'data.cityofboston.gov'),
        ('explore.data.gov', 'data.medicare.gov'),
        ('explore.data.gov', 'info.samhsa.gov'),
    ]
    observed = federation.parse_page(html)
    n.assert_list_equal(observed, expected)

def test_build_network():
    observed = federation.build_network()
    expected_keys = {'edges', 'nodes'}
    n.assert_equal(set(observed.keys()), expected_keys)
    for k in expected_keys:
        n.assert_equal(type(observed[k]), list)

    for edge in observed['edges']:
        n.assert_equal(type(edge), tuple)
        for node in edge:
            n.assert_equal(type(node), unicode)

    for node in observed['nodes']:
        n.assert_equal(type(node), unicode)

def test_build_d3_json():
    observed = json.loads(federation.build_d3_json())
    expected_keys = {'links', 'nodes'}
    n.assert_equal(set(observed.keys()), expected_keys)
    for k in expected_keys:
        n.assert_equal(type(observed[k]), list)

    for link in observed['links']:
        n.assert_equal(type(link), dict)
        n.assert_equal(set(link.keys()), {'source', 'target'})
        for node in link.values():
            n.assert_equal(type(node), int)

    for node in observed['nodes']:
        n.assert_equal(node.keys(), ['name'])
