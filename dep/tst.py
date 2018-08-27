import praw
import json
from titleparse import *
import os

# Authenticate then get a subreddit instance.
reddit = praw.Reddit(client_id='f_12DlDQXQrIeg',
                     client_secret=os.environ['rAPISecret'],
                     user_agent='python bot collecting data on rborrow')
brw = reddit.subreddit('borrow')

# Initialize vars
results = []
i = 0

# Download and iterate through submissions
for post in brw.new(limit=2):

    currPost = {}

    # Parse titles
    try:
        tmp = outtest(title_parser.parse(post.title))
        tmp.update({'parseErr' : False}) 
    except Exception as inst:
        print("Exc! type: " + inst.type + "; args: " + inst.args)
        tmp = {'parseErr' : inst}

    currPost.update(tmp)

    # Add the rest of the values.
    currPost['title'] = post.title
    currPost['score'] = post.score
    currPost['postid'] = post.id
    currPost['url'] = post.url
    currPost['tcomm'] = []

    # Sort through comments, removing LoansBot and AutoModerator.
    try:
        for top_comment in post.comments.list():
            if not top_comment.author.name == "LoansBot" and not top_comment.author.name == "AutoModerator" : 

                currPost['tcomm'].append({ 'author': top_comment.author.name, 'body': top_comment.body})
    except:
        currPost['tcomm'].append("NoComment")

    results.append(currPost)
    i += 1
    print(i)


