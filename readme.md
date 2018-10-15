# Python /r/borrow scrape and analysis.

[Network Graph of /r/borrow](gephi/main.png)

### What is "/r/borrow"?
It's a subreddit (a type of online forum, hosted on reddit.com). Here's a link to it: [www.reddit.com/r/borrow](https://www.reddit.com/r/borrow). It's a community where people can borrow and lend money to each other, completely informally. Depending on the lender's location, it is almost certainly in a bit of a legal gray area. Another line that is a bit blurred is whether it's meant to be a support community (akin to https://www.reddit.com/r/Assistance/) or a way for lenders to make profit.

### So what is this project?
I think /r/borrow is a pretty interesting phenomenon, so I gathered as many posts as I could and made it all into a nice dataset containing information on ~18,000 loans. I made a couple of pretty visualizations, including a network graph with every loan given on the subreddit. I used the PushShift.io API to gather almost all of this data (although recent posts are from Reddit's API). This repository is home to all the code I wrote in the process of fetching, parsing, and cleaning this data. 

### Show me your results!
If you're interested in reading more, check out the Jupyter notebook in this repo. You can download it and run it on your computer, or just check out a hosted version of [the HTML output here](https://quinnbatten.com/assets/docs/rborrow/rborrow.html).

### Here are a few quick facts about /r/borrow:
- One lender has lent more than $300,000 in total over their whole /r/borrow lifetime (I call this 'total lifetime lend').
- There are 11 lenders who each have a total lifetime lend of over $50,000.
- The majority of lenders have lent less than <$1,000 over their lifetime, but 20 lenders have given more than $100,000 in loans.
- The largest loan given was $7,000 (it was successfully repaid).

### Walk me through the contents of the repository?
There are a few different things in here:
- The data: The full data set is in the folder titled 'data'. The files 'final_out.csv' and 'final_out.json' are the complete, parsed and cleaned data set in csv and json forms, respectively. If you just want to exlore this data on your own, check out those files. The 'raw... .json' files are the initial data downloaded form pushshift. The 'parsed[...].json' files are the raw files with data points obtained from parsing added on to every row. And, finally, the 'netdict_both.json' file contains the full data set in its final form, except for a few individual raws that have not been fixed. Those fixes are implemented in the Jupyter notebook described in the next list item.
- The analysis: in the 'analysis' folder is a Jupyter Notebook that walks through the analysis work I've done and outputs some visualizations.
- The python files used to collect and process the data. in the 'data_processing' folder are two python files that contain the functions I used to collect, clean, and parse this data. These work perfectly well, but they're not production-ready. They're not really meant to be used by anyone else, and in particular... **please** do not run the `getdata_ps` function. It will fetch a lot of data from pushshift once again— that data is already available in this repo, and Pushshift is basically someone's hobby project and is completely donation-supported. Best not to waste Pushshift's resources.
- The graph files: Finally, in the 'gephi' folder is a GEXF file, a Gephi workspace, and an exported SVG. These contain a network visualization of the final and complete data set. in the SVG and the Gephi workspace, I've applied a few visual distinctions: red edges are unpaid loans, green nodes are lenders (a user who has given at least 1 loan), and red nodes are borrowers. The green nodes (lenders) are scaled by the number of unique borrowers they have lent to.

### I want to get in touch with you!
Sweet! If you want to talk, please drop me a line at my website's contact page ([link here](https://www.quinnbatten.com/contact/)). I'd love to talk about this with you, and would be excited to hear, well, anything at all, including but not limited to: thoughts, criticism, suggested edits, areas of future research/work, and rants. 