import praw
import json
import os
import lark
from parsing import parsetitle

def getdata(limit=None):
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
            tmp = parsetitle(post.title)
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
