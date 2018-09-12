import networkx as nx
import json
from helpers import *


def read_raw():
    '''Helper that reads raw output file (from pushshift)'''
    inraw = readfile("/Users/quinnbatten/Documents/Programming/PyProjects/" +
                     "rborrow/textfiles/ps_out_raw.json")

    return inraw


def read_parsed(input='ps_output_parsed'):
    '''Helper that reads parsed output (either paid or unpaid, adding
    reqslater maybe if we parse it)'''
    if not (input == 'paid' or input == 'unpaid'):
        print("please specify paid or unpaid")
        indict = 0
    else:
        indict = readfile("/Users/quinnbatten/Documents/Programming/" +
                          "PyProjects/rborrow/textfiles/" + input + ".json")
    return indict


def read_netdict(input="netdict1"):
    '''Helper that reads our netdict file (parsed output that got translated
       into a useful list of dictionaryies by parse_indict.)'''
    netdict = readfile("/Users/quinnbatten/Documents/Programming/" +
                       "PyProjects/rborrow/textfiles/" + input + ".json")
    return netdict


def parse_indict(indict):
    '''Accepts raw output from pushshift, parses it into an indict.'''
    output = []
    i = 0
    for post in indict:
        i += 1
        currPost = {}

        # Parse titles
        success = 0
        try:
            tmp = parseTitle(post['title'])
            success = 1
        except Exception as inst:
            try: tmp = parse_title_fallback(post['title'])
        else:
            currPost.update({'parseErr': False})
        finally:
            currPost.update(tmp)

        # Collect additional information
        currPost['author'] = post['author']
        currPost['date'] = post['created_utc']
        currPost['url'] = post['full_link']
        currPost['title'] = post['title']
        if 'selftext' in post:
            currPost['body'] = post['selftext']
        else:
            currPost['body'] = ''
        currPost['score'] = post['score']
        currPost['postid'] = post['id']

        if i % 100 == 0:
            print(i)
        output.append(currPost)
    # Export our output file
    with open('parsed_out_.json', 'w') as f:
        json.dump(output, f, indent=4)
    return output


def make_netdict(dicts, post_type='paid'):
    '''Makes a netdict given a parsed output dictionary (from parse_indict).
    A netdict is a simpler dictionary with only the info we're interested
    in.'''

    # set up given post_type
    if post_type == 'paid':
        bor_key = 'p_user'
        lend_key = 'author'
        amt_key = 'p_amt'
    elif post_type == 'unpaid':
        bor_key = 'u_user'
        lend_key = 'author'
        amt_key = 'u_amt'
    else:
        print("You must choose 'paid' or 'unpaid'! Try " +
              "make_netdict again with one of those options.")

    # filter those that don't have a ptype and those that failed parsing
    tmp_nice = [post for post in dicts if post_type in post and
                not post['parseErr']]
    posts = [post for post in tmp_nice if post['ptype'] == post_type]

    # make a dictionary for each post, add it to the list
    for post in posts:
        currDict = {
            'bor': post[bor_key],
            'lend': post[lend_jey],
            'amt': post[amt_key],
            'date': post['date'],
            'url': post['url']
        }
        netdict.append(currDict)

    # Export our output file
    with open('netdict_out_.json', 'w') as f:
        json.dump(netdict, f, indent=4)

    return netdict


def load_graph(netdict):
    '''Takes a netdict that's in memory and puts it into a
    Gephi filein memory and on disk'''

    G = nx.DiGraph()
    for loan in netdict:
            if loan['amt'].isdigit():
                tmp_amt = int(loan['amt'])
            else:
                tmp_amt = 0
            G.add_edge(loan['lend'], loan['bor'], amt=tmp_amt,
                       date=loan['date'])
    nx.write_gexf(G, 'output_.gexf')
    return G
