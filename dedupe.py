#!/usr/bin/env python
import json, os

from federation import build_network

def portal(dcat):


def dedupe(dcats, edges):
    '''
    Args:
        A list of Socrata dcat lists, each list augmented with a "portal" key
    Returns:
        One list of dcat, still augmented with the "portal" key, sorted by identifier

    This deduplicates and combines of dcat based on the edges of the federation graph.
    '''

    losing_portals = set([edge[0] for edge in edges])

    seen = set()
    for dcat in dcats:
        for dataset in dcat:
            if not (dataset['identifier'] in seen and dataset['portal'] in losing_portals):
                yield dataset
            seen.add(dataset['identifier'])

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
    dedupe_ab = lambda a,b: dedupe(a, b, edges)
    json.dumps(reduce(dedupe_ab, load()))

if __name__ == '__main__':
    main()
