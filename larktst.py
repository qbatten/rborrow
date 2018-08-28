import pfix

def parse_indict(indict):
    output = []
    for post in indict:

        currPost = {}

        # Parse titles
        try:
            tmp = pfix.parseTitle(post['title'])
            currPost.update({'parseErr' : False})

        except Exception as inst:
            print("Exc! type: " + str(inst))
            tmp = {'parseErr' : str(inst)}
        finally:
            currPost.update(tmp)

        currPost['author'] = post['author']
        currPost['date'] = post['created_utc']
        currPost['url'] = post['full_link']
        currPost['title'] = post['title']
        currPost['body'] = post['selftext']
        currPost['score'] = post['score']
        currPost['postid'] = post['id']

        output.append(currPost)

    return output


