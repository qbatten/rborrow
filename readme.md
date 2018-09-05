# Python /r/borrow scrape and analysis.
There's a subreddit called "/r/borrow," where redditors can post asking to borrow money, and other redditors lend to them. I thnk that's kind of interesting, so I gathered as many posts as I could and made it all into a nice dataset containing 14,995 loans. Then I made some network graphs and getherd some basic stats on this data. This repository holds all the code I wrote in order to do that, all of my results, and the dataset itself! 

(Note: This project isn't particularly wrapped up or finished, I'm still figuring out what exactly I want to do with this data. If you have any ideas or you want to talk, please get in touch!)

This project uses the pushshift.io API to download all available historical data for the subreddit "/r/borrow," then it parses out the post titles for paid and unpaid posts to determine important features of each loan. The parsed titles are collected and cleaned, producing a dataset containing 13,823 successful loans and 1,172 defaulted loans. Each loan has a date, the names of the borrower and the lender, and an amount (the principal). The subreddit deliberately keeps the interest amount private to the borrower and lender, so, sadly, I wasn't able to access that information. Still, the data is pretty interesting. A few quick facts:
- One lender has lent more than $300,000 in total over their whole /r/borrow lifetime (from here on, I'll call this the 'total lifetime lend/lending'. or 'total lifetime borrow/borrowing'.
- There are 11 lenders who each have a total lifetime lend of over $50,000.
- The majority of lenders have a total lifetime lend of <$1,000, and of those, the majority have a total lifetime lend of <$200.
- Roughly $3 million has moved through /r/borrow over its lifetime (~$1 million each year)


# What's in this repository?
The most interesting thing in here is the data! Specifically, the file [netdict1.json](textfiles/netdict1.json). It contains data on 13,823 repaid loans on /r/borrow, in the form of a list of dictionaries ([netdict_unpaid_1.json](textfiles/netdict_unpaid_1.json) is the same type of file, but with all 1,172 defaulted loans). For each loan, I was able to parse out the borrower, the lender, the amount (principal), and the date. I also included the URL for each one, which makes it easy to iterate through and try to grab further information from the post using the Reddit API.

There are some python files in the main directory, but they're a bit messy. getdata.py contains the main code I used to download the data and parse the titles. It includes a program that pulls all available posts from the reddit API and one that pulls all available posts from pushshift.io  [^1]. If you're interested in how I parsed out important imformation from the title text, I used the lark-parser library, and the grammar I used is in helpers.py.

The 'textfiles' folder contains all the data I obtained, in its various forms (although they're all json files and each file is a list of dicts). Here's some naming conventions I used: 'ps' means it's from pushshift.io (aka these are the interesting ones), 'rapi' means it's from the Reddit API, 'out_raw' is, well, the raw, unprocessed data, as pushshift provided it. 'out_parsed' is the data after it's been run through my parser and simplified a bit, and 'netdict' is the final dataset as I exported it to Gephi using the networkx library. 

The 'Gephi' folder contains a few Gephi workspaces and some exported images. I think [this network graph](Gephi/overall_borlend4_nolabel.svg), and [the same one, with labels,](Gephi/overall_borlend4_label.svg) are pretty cool. They show lenders as black nodes, scaled by total number of loans given, and borrowers as small green nodes.

The 'notebooks' folder contains a Jupyter notebook where I gathered some preliminary stats about the dataset.





***
[^1]: I tried to get as many posts as possible using the reddit API and PRAW first, but Reddit recently made it very difficult to access any posts on a subreddit past the most recent 1000. You used to be able to sidestep their 1000-post-limit using a search by date, but they shut that down too! So, I turned to pushshift. The PRAW program works perfectly well, so I kept it in here just in case, but getdata.getdata_ps() is probably the more useful program, because of those reddit API limitations.