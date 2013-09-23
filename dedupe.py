#!/usr/bin/env python
import json, os
from collections import Counter

from federation import build_network

def identifiers(dcats):
    identifiers = Counter()
    for dcat in dcats:
        identifiers.update((dataset['identifier'] for dataset in dcat))
    return identifiers

def dedupe(dcats, edges):
    '''
    Args:
        An iterable of Socrata dcat lists, each list augmented with a "portal" key
    Returns:
        An iterable of dcat, still augmented with the "portal" key

    This deduplicates and combines of dcat based on the edges of the federation graph.
    '''

    losing_portals = set([edge[0] for edge in edges])
    duplicates = set((k for k,v in identifiers(dcats).iteritems() if v > 1))

    for dcat in dcats:
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
        yield dcat

def main():
    edges = build_network()['edges']
    dcat = dedupe(load(), edges)
    print json.dumps(list(dcat))

if __name__ == '__main__':
    main()
