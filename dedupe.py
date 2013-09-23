#!/usr/bin/env python
from federation import build_network

def reducer(a, b, edges = None):
    '''
    Args:
        Two tuples of (portal, dcat list)
    Returns:
        One list of dcat

    This deduplicates and combines of dcat based on the edges of the federation graph.
    '''
    if edges == None:
        edges = build_network()['edges']


    return l

def load():
    '''
    Returns an iterable of dcat lists
    '''
    for data_json in os.listdir(os.path.join('socrata-catalog', 'catalogs')):
        yield json.load(open(os.path.join('catalogs', data_json)))[1:]

def main():
    reduce(lambda a,b:a+b,load())
