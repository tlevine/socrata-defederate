import nose.tools as n

import dedupe

def test_dedupe():
    dcat1 = [
        {'identifier': 'a', 'portal': 'portal1'},
        {'identifier': 'b', 'portal': 'portal1'},
        {'identifier': 'c', 'portal': 'portal1'}]
    dcat2 = [
        {'identifier': 'g', 'portal': 'portal2'},
        {'identifier': 'h', 'portal': 'portal2'},
        {'identifier': 'c', 'portal': 'portal2'}]
    edges = [('portal1', 'portal2')]
    observed = dedupe.dedupe([dcat1, dcat2], edges)

    # Sort by identifier
    expected = [
        {'identifier': 'a', 'portal': 'portal1'},
        {'identifier': 'b', 'portal': 'portal1'},
        {'identifier': 'c', 'portal': 'portal2'},
        {'identifier': 'g', 'portal': 'portal2'},
        {'identifier': 'h', 'portal': 'portal2'},
    ]
    observed_list = list(sorted(observed, key = lambda x: x['identifier']))
    n.assert_list_equal(observed_list, expected)
