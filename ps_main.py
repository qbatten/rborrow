import time
import urllib
import json
import sqlite3


def getdata_ps():

    out = []

    url = "https://api.pushshift.io/reddit/search/submission/?subreddit=borrow&title=paid&size=500"

    response = urllib.request.urlopen(url)
    dataCurr = json.load(response)
    for item in dataCurr['data']:
        out.append(item)

    currDate = str(out[-1]['created_utc'])
    outfile_title = 0
    url = "https://api.pushshift.io/reddit/search/submission/?subreddit=borrow&title=paid&size=500&before="

    response_still = 1

    while response_still:
        urltmp = url + currDate
        print(urltmp)
        response = urllib.request.urlopen(urltmp)
        dataCurr = json.load(response)
        if len(dataCurr['data']) <= 1:
               response_still = 0
               break
        for item in dataCurr['data']:
            out.append(item)

        currDate = str(out[-1]['created_utc'])

        # Export our output file
        if len(out) > 4000:
            outfile_title += 1
            with open(str(outfile_title) + ".json", 'w') as f:
                json.dump(out, f, indent=4)

    return out
