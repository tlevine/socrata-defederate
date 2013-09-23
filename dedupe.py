#!/usr/bin/env python
from collections import OrderedDict

from federation import build_network

def dedupe(a, b, edges):
    '''
    Args:
        Two tuples of (portal, dcat list)
    Returns:
        One list of dcat, sorted by identifier

    This deduplicates and combines of dcat based on the edges of the federation graph.
    '''
    a_portal, a_list = a
    b_portal, b_list = b

    a_dict = OrderedDict(zip([item['identifier'] for item in a_list], a_list))
    b_dict = OrderedDict(zip([item['identifier'] for item in b_list], b_list))

    winner = winning_portal(a_portal, b_portal, edges)

    if winner == a_portal:
        b_dict.update(a_dict)
        return b_dict.values()
    else:
        a_dict.update(b_dict)
        return a_dict.values()

def winning_portal(a, b, edges):
    return a

def load():
    '''
    Returns an iterable of dcat lists
    '''
    for data_json in os.listdir(os.path.join('socrata-catalog', 'catalogs')):
        portal = data_json.replace('.json', '')
        yield data_json, json.load(open(os.path.join('socrata-catalogs', 'catalogs', data_json)))[1:]

def main():
    edges = build_network()['edges']
    print load().next()
