# Python /r/borrow scrape and analysis.

[Network Graph of /r/borrow](gephi/main.png)

There's a subreddit called "/r/borrow" where redditors can post asking to borrow money, and other redditors lend to them. I thnk that's pretty interesting, so I gathered as many posts as I could and made it all into a nice dataset containing information on ~15,000 loans. Then I made a network graph and performed some analysis of the data. This repository holds the code I wrote in order to do that, all of my results, and the dataset itself! 

If you're interested in reading more, check out the Jupyter notebook in this repo ([here's a link to the HTML export of the notebook.](analysis/main_analysis.html) You'll have to download it as it's too big for Github to display). 

Here are a few quick facts about /r/borrow:
- One lender has lent more than $300,000 in total over their whole /r/borrow lifetime (from here on, I'll call this the 'total lifetime lend/lending'. or 'total lifetime borrow/borrowing'.
- There are 11 lenders who each have a total lifetime lend of over $50,000.
- The majority of lenders have lent less than <$1,000 over their lifetime, but 20 lenders have given more than $100,000 in loans.


# What's in this repository?
There are a few different things in here:
- The data: The full data set is in the folder titled 'data'. The files 'final_out.csv' and 'final_out.json' are the complete, parsed and cleaned data set in csv and json forms, respectively. If you just want to exlore this data on your own, check out those files. The 'raw... .json' files are the initial data downloaded form pushshift. The 'parsed[...].json' files are the raw files with data points obtained from parsing added on to every row. And, finally, the 'netdict_both.json' file contains the full data set in its final form, except for a few individual raws that have not been fixed. Those fixes are implemented in the Jupyter notebook described in the next list item.
- The analysis: in the 'analysis' folder is a Jupyter Notebook that walks through the analysis work I've done and outputs some very pretty graphs (if I do say so myself).
- The python files used to collect and process the data. in the 'data_processing' folder are two python files that contain the functions I used to collect, clean, and parse this data. These work perfectly well, but they're not production-ready. They're not really meant to be used by anyone else, and in particular... **please** do not run the `getdata_ps` function. It will fetch a lot of data from pushshift once again— that data is already available in this repo, and pushshift is basically someone's hobby project and is completely donation-supported. Best not to waste pushshift's resources.
- The graph files: Finally, in the 'gephi' folder is a GEXF file, a Gephi workspace, and an exported SVG. These contain a network visualization of the final and complete data set. in the SVG and the Gephi workspace, I've applied a few visual distinctions: red edges are unpaid loans, green nodes are lenders (a user who has given at least 1 loan), and red nodes are borrowers. The green nodes (lenders) are scaled by the number of unique borrowers they have lent to.

# I like this / hate this / want to talk about this!
Sweet! If you want to get in touch with me, please drop me a line at my website's contact page ([link here](https://www.quinnbatten.com/contact/)). I'd love to talk about this with you, and would be excited to hear, well, anything at all, including but not limited to: thoughts, criticism, suggested edits, areas of future research/work, and rants. 

If you want to post this somewhere, please ask me first— this is really meant to be a personal & portfolio project, and ideally, I'd love to have a conversation with you before it gets publicized in any way. Of course, it is out on the internet and I understand that might mean someone will go ahead and do something with this regardless of my desires.