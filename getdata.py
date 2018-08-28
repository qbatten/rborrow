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


def reddit_api_getdata(limit=None):
    '''Downloads data from Reddit API using PRAW, parsing titles on the way,
	and dumps into a JSON as well as returning the dict.
    '''
# Authenticate then get a subreddit instance.
    reddit = praw.Reddit(client_id='f_12DlDQXQrIeg',
                        client_secret='Qx5Dqhp7NxCYeqqIFC6pGXnsYD0',
                        user_agent='python bot collecting data on rborrow')
    brw = reddit.subreddit('borrow')

    # Setup
    results = []
    i = 0 # Num of comments we've iterated through


    # Download and iterate through submissions
    for post in brw.new(limit=None):

        currPost = {}

        # Parse titles
        try:
            tmp = parseTitle(post.title)
            tmp.update({'parseErr' : False})
        except Exception as inst:
            print("Exc! type: " + str(inst))
            tmp = {'parseErr' : str(inst)}
        except NameError as inst:
            print("Exception: " + str(inst))
            tmp = {'parseErr' : str(inst)}
        finally:
            currPost.update(tmp)

        # Add the rest of the values.

        currPost['title'] = post.title
        currPost['body'] = post.selftext
        currPost['date'] = post.created_utc
        if post.author:
            currPost['author'] = post.author.name
        else:
            currPost['author'] = 'deleted'
        currPost['score'] = post.score
        currPost['postid'] = post.id
        currPost['url'] = post.url

        currPost['tcomm'] = []

        # Sort through comments, removing LoansBot and AutoModerator.
        for top_comment in post.comments.list():
            try:
                if not top_comment.author.name == "LoansBot" and not top_comment.author.name == "AutoModerator":
                    currPost['tcomm'].append({ 'author': top_comment.author.name, 'body': top_comment.body})
            except:
                    currPost['tcomm'].append("None")

        results.append(currPost)
        i += 1
        print(i)

    # Export our output file.
    with open('progOut1.txt', 'w') as f:
        json.dump(results, f, indent=4)

    return results



