#!/usr/bin/env python
import json, os
from collections import Counter

from federation import build_network

def identifiers(dcat):
    identifiers = Counter([dataset['identifier'] for dataset in dcat])
    return identifiers

def dedupe(dcat, edges):
    '''
    Args:
        An iterable of Socrata dcat, each list augmented with a "portal" key
    Returns:
        An iterable of dcat, still augmented with the "portal" key

    This deduplicates and combines of dcat based on the edges of the federation graph.
    '''

    losing_portals = set([edge[0] for edge in edges])
    print dcat
    duplicates = set((k for k,v in identifiers(dcat).iteritems() if v > 1))

    for dataset in dcat:
        if not(dataset['portal'] in losing_portals and dataset['identifier'] in duplicates):
            yield dataset

def load(catalogs = os.path.join('socrata-catalog', 'catalogs')):
    '''
    Returns an iterable of dcat lists
    '''
    for data_json in os.listdir(catalogs):
        portal = data_json.replace('.json', '')
        dcat = json.load(open(os.path.join(catalogs, data_json)))[1:]
        for dataset in dcat:
            dataset['portal'] = portal
            yield dataset

def main():
    edges = build_network()['edges']
    dcat_in = list(load())
    dcat_out = dedupe(dcat_in, edges)
    print json.dumps(dcat)

if __name__ == '__main__':
    main()
