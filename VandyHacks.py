# Attempt to make reddit bot that determines political leanings
# could be applied to threads, subreddits, or users
# will read in all comments from hot 10 in selected subreddits(eg t_d, conservative)
# will find most common words, but will ignore most common words from askreddit
# will compare these lists

# start by connecting to reddit:

import praw
import re
import csv
import os
import os.path
import collections

reddit = praw.Reddit(client_id='ZRfPmQnieqTWUw',
                     client_secret='iUpQc7K0iRw8CZM6tGmPjRBBU4I',
                     password='timberline3',
                     user_agent='political leanings by /u/thisaccounttestsbots',
                     username='thisaccounttestsbots')
conservative_reddits = ('The_Donald', 'conservative', 'Republican')
liberal_reddits = ('liberal','democrats', 'progressive')
common_words = ('AskReddit', 'funny')
numPosts = 15

longwords = []
def writeComments( redditsList, fileName ):
    myFile = fileName
    if os.path.isfile(myFile):
        os.remove(myFile)
    for subreddits in redditsList:
        subreddit = reddit.subreddit(subreddits)
        hot = subreddit.top(limit=numPosts)
        for submission in hot:
            words=[]
            submission.comments.replace_more(limit=0)
            all_comments = submission.comments.list()
            for comments in all_comments:
                body = comments.body
                found_words = re.findall(r'\w+', body)
                cap_words = [word.upper() for word in found_words]
                words.extend(cap_words)
                longwords.extend(cap_words)
                print("appended comment body")
            commentsFile = open(myFile, 'a', encoding='utf-8')
            wr = csv.writer(commentsFile)
            wr.writerow(words)
            commentsFile.close()
            print("wrote to file")
    print("done")
    word_counts = collections.Counter(longwords)
    common = word_counts.most_common()
    #commonSet = set(common)
    return common

conCounts = writeComments(conservative_reddits, 'conservative_comments.csv')
libCounts = writeComments(liberal_reddits, 'liberal_comments.csv')
comCounts = writeComments(common_words, 'ask_comments.csv')

comWords = set([word for word, word_counter in comCounts[0:500]])
conWords = set([word for word, word_counter in conCounts[0:700]]) - comWords
libWords = set([word for word, word_counter in libCounts[0:700]]) - comWords
conOnly = conWords - libWords
libOnly = libWords - conWords

don = {'HillaryforPrison'}
donaldCounts = writeComments(don, 'donald.csv')
donaldWords = set([word for word, word_counter in donaldCounts[0:700]]) - comWords
print(len(donaldWords & conOnly))
print(len(donaldWords & libOnly))
print(len(conOnly))
print(len(libOnly))
