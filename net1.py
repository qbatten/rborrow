import networkx as nx
import json

import main



# Make our nice lists

def make_netdict(dicts):
    tmp_nice = [post for post in dicts if 'ptype' in post]
    reqs = [post for post in tmp_nice if post['ptype'] == 'REQ']
    paids = [post for post in tmp_nice if post['ptype'] == 'PAID']

    netdict = []

    for post in paids:
        currDict = {
            'bor' : post['user'],
            'lend' : post['author'],
            'amt' : post['p_amt']
        }
        netdict.append(currDict)

    # Export our output file
    with open('netdict1.txt', 'w') as f:
        json.dump(netdict, f, indent=4)

    return netdict

def load_netdict(netdict):
    G = nx.Graph()
    for loan in netdict:
            G.add_edge(loan['bor'], loan['lend'], amt = loan['amt'])
    return G
