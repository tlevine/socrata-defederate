import nose.tools as n

import dedupe

@n.nottest
def test_dedupe():
    dcat1 = [{'identifier': 'a', 'portal': 1}, {'identifier': 'b', 'portal': 1}, {'identifier': 'c', 'portal': 1}]
    dcat2 = [{'identifier': 'g', 'portal': 2}, {'identifier': 'h', 'portal': 2}, {'identifier': 'c', 'portal': 2}]
    edges = [('portal1', 'portal2')]
    observed = dedupe(('portal1', dcat1), ('portal2', dcat2), edges)

    # Sort by identifier
    expected = [
        {'identifier': 'a', 'portal': 1}, {'identifier': 'b', 'portal': 1},
        {'identifier': 'c', 'portal': 2},
        {'identifier': 'g', 'portal': 2}, {'identifier': 'h', 'portal': 2},
    ]
    n.assert_list_equal(observed, expected)

def test_winning_portal():
    edges = [('one', 'three')]
    observed = dedupe.winning_portal('one', 'three', edges)
    n.assert_equal(observed, 'three')
