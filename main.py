import getting
import json


def readfile(fin="/Users/quinnbatten/Documents/Programming/PyProjects/rborrow/main1.json"):

    with open(fin) as f:
        vals = json.load(f)
    return vals



def niceify(filein="/Users/quinnbatten/Documents/Programming/PyProjects/rborrow/main1.json"):
    print(filein)
    vals = readfile(filein)

    out = []
    borrowers = {}
    lenders = {}
    for post in vals:
        if post['parseErr']==False:
            if post['ptype'] == "REQ":
                if post['author'] in borrowers:
                    borrowers[post['author']] = [borrowers[post['author']]].append(post['r_amt'])
                else:
                    borrowers.update({post['author']: post['r_amt']})
            elif post['ptype']=="PAID":
                if post['author'] in lenders:
                    lenders[post['author']] = [lenders[post['author']]].append(post['p_amt'])
                else:
                    lenders.update({post['author']: post['p_amt']})

    out.append(borrowers)
    out.append(lenders)
    return out
