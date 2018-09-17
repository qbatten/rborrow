import re
import json
import networkx as nx


def parse_raw(raw):
    '''Accepts raw output from pushshift, parses it into an indict.'''
    output = []
    i = 0
    for post in raw:
        i += 1
        currPost = {}

        # Parse titles
        if re.search(r'\[META\]', post['title']):
            continue
        try:
            tmp = parse_title(post['title'])
        except Exception as inst:
            tmp = {'parseErr': str(inst),
                   'amt': False,
                   'user': False,
                   'ptype': False}
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
    with open('parsed_out_unpaid.json', 'w') as f:
        json.dump(output, f, indent=4)
    return output


def make_netdict(dicts):
    '''Makes a netdict given an indict (parsed raw file).
    A netdict is a simpler dictionary with only the info we're interested
    in.'''
    netdict = []
    # filter those that don't have a ptype and those that failed parsing
    tmp_nice = [post for post in dicts if 'ptype' in post and
                not post['parseErr']]
    posts = [post for post in tmp_nice if ((post['ptype'] == 'PAID') or
             (post['ptype'] == 'UNPAID'))]

    # make a dictionary for each post, add it to the list
    for post in posts:
        if post['ptype'] == 'PAID':
            outcome = 1
        elif post['ptype'] == 'UNPAID':
            outcome = 0
        else:
            outcome = False

        currDict = {
            'bor': post['user'],
            'lend': post['author'],
            'amt': post['amt'],
            'date': post['date'],
            'url': post['url'],
            'outcome': outcome,
        }
        netdict.append(currDict)

    # Export our output file
    with open('netdict_out_.json', 'w') as f:
        json.dump(netdict, f, indent=4)

    return netdict


def parse_title(to_parse):
    '''Fallback parser if first one fails'''

    # Grab ptype
    ptype = False
    if re.search(r'[\[\(]UNPAID\s*\$*[\]\)]', to_parse):
        ptype = 'UNPAID'
    elif re.search(r'[\[\(]Unpaid\s*\$*[\]\)]', to_parse):
        ptype = 'UNPAID'
    elif re.search(r'[\[\() ]unpaid\s*\$*[\]\)]', to_parse):
        ptype = 'UNPAID'
    elif re.search(r'[\(\[]PAID[\]\)]', to_parse):
        ptype = 'PAID'
    elif re.search(r'\[Paid\]', to_parse):
        ptype = 'PAID'

    # Grab user, replace username with nothing, to deal with usernames w nums
    user = re.search(r'\/u\/[\w\d_-]+', to_parse)
    if user:
        to_parse = re.sub(r'\/u\/[\w\d_-]+', '', to_parse)
    if not user:
        user = re.search(r'u\/ ?[\w\d_-]+', to_parse)
        if user:
            to_parse = re.sub(r'u\/ ?[\w\d_-]+', '', to_parse)
    if not user:
        user = re.search(r'u\/ ?[\w\d_-]+', to_parse)
        if user:
            to_parse = re.sub(r'u\/ ?[\w\d_-]+', '', to_parse)
    if not user:
        user = re.search(r'[dD]\][ -,]+ ?[a-zA-Z_-]+', to_parse)
        if user:
            user = re.sub(r'[dD]\][ -,]+ ?', '', user)
            to_parse = re.sub(r'[dD]\][ -,]+ ?[a-zA-Z_-]+', '', to_parse)
    if not user:
        user = False
    else:
        user = user[0].split('/')[-1]

    # Grab amount
    amt_fail = False
    amt = re.search(r'[£\$][0-9,.]+', to_parse)
    if not amt:
        amt = re.search(r'[0-9,.]+', to_parse)

    if not amt:
        amt = False
    else:
        tmp_amt = []
        for i in amt[0]:
            if i.isdigit() or i == '.':
                tmp_amt.append(i)
        amt = float(''.join(tmp_amt))

    # See if it's an actual number. If not, save value and mark false
    try:
        amt = float(amt)
    except ValueError:
        amt_fail = amt
        amt = False

    # Fill output
    tmp = {'amt': amt,
           'user': user,
           'ptype': ptype,
           'parseErr': False}
    if amt_fail:
        tmp.update({'amt_fail': amt_fail})

    return tmp


def failed_items(tmpout, p=1):
    '''Convenience fn to list failed titles and what caused failure'''
    faillist = []
    i = 0
    f = 0
    for item in tmpout:
        if item['amt'] and item['user'] and item['ptype']:
            i += 1
        else:
            faillist.append(item)
            f += 1
    output = {'s': i,
              'f': f,
              'faillist': faillist}
    print('S: ' + str(i))
    print('F: ' + str(f))
    print(str(i / (i + f)))

    if p > 0:
        p_count = 0
        for fail in faillist:
            if not fail['amt']:
                print("amt || ", end='')
            if not fail['user']:
                print('user || ', end='')
            if not fail['ptype']:
                print('ptype || ', end='')
            print('\n' + fail['title'] + '\n')
            p_count += 1
            if p_count > p:
                break

    return output


def load_graph(netdict):
    '''Takes a netdict that's in memory and puts it into a
    Gephi file on disk, and returns a populated networkx DiGraph object.
    The file is written into the current directory as 'out.gexf'.'''
    G = nx.DiGraph()
    for row in netdict:
        try:
            tmp = G[row['lend']][row['bor']]
        except KeyError:
            G.add_edge(row['lend'], row['bor'], count=1, amt=row['amt'],
                       outcome=1, date=row['date'])
        else:
            G[row['lend']][row['bor']]['amt'] =
                    G[row['lend']][row['bor']]['amt'] + row['amt']
            G[row['lend']][row['bor']]['count'] =
                    G[row['lend']][row['bor']]['count'] + 1
            if row['outcome'] == 0:
                G[row['lend']][row['bor']]['outcome'] = 0
    nx.write_gexf(G, 'out.gexf')
    return G
