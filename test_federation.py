from lxml.html import fromstring

import federation

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

def test_parse_targets_snippet():
    observed = federation.parse_one(html)
    expected = ['explore.data.gov']
    n.assert_list_equal(observed, expected)

def check_parse_targets(filename):
    html = fromstring(open(filename).read())
    expected = json.load(open(filename.replace('.html', '.json')))
    n.assert_list_equal(federation.parse_targets(html), expected)

def test_parse_targets():
    for basename in os.listdir('fixtures'):
        yield check_parse_targets, os.path.join('fixtures', basename)

def check_parse_source(filename):
    html = fromstring(open(filename).read())
    observed = federation.parse_source(html)

    expected = re.match(r'/([^/]+)\.html', filename).group(1)

    n.assert_equal(type(observed), type(expected))
    n.assert_equal(observed, expected)

def test_parse_targets():
    for basename in os.listdir('fixtures'):
        yield check_parse_targets, os.path.join('fixtures', basename)
