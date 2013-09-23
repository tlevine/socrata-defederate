#!/usr/bin/env python
from federation import build_network

def filterer(l, edges = None):
    '''
    Takes a list of dcat and filters it
    '''
    if edges == None:
        edges = build_network()['edges']


    return l

def load():
    '''
    Returns an iterable of dcat lists
    '''
    for data_json in os.listdir('catalogs'):
        yield json.load(open(os.path.join('catalogs', data_json)))[1:]

def main():
    reduce(lambda a,b:a+b,load())
