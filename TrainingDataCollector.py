# Get top comments from top posts on given subreddits
import praw
import re
import csv
import os
import os.path
import collections
import string

reddit = praw.Reddit(client_id='ZRfPmQnieqTWUw',
                     client_secret='iUpQc7K0iRw8CZM6tGmPjRBBU4I',
                     password='timberline3',
                     user_agent='political leanings by /u/thisaccounttestsbots',
                     username='thisaccounttestsbots')
conservative_reddits = ('The_Donald', 'conservative', 'hillaryforprison', 'republican')
liberal_reddits = ('liberal','SandersForPresident', 'democrats', 'esist')
numPosts = 50

longwords = []
def writeComments( redditsList, fileName, category ):
    myFile = fileName
    if os.path.isfile(myFile):
        os.remove(myFile)
    commentsFile = open(myFile, "w", encoding='utf8')
    for subreddits in redditsList:
        subreddit = reddit.subreddit(subreddits)
        hot = subreddit.top(limit=numPosts)
        for submission in hot:
            submission.comment_sort = 'new'
            all_comments = submission.comments.list()
            for comments in all_comments[0:10]:
                body = comments.body
                found_words = re.findall(r'\w+', body)
                commentString = ''
                for words in found_words:
                    commentString += words
                    commentString += ' '
                commentString = commentString[0:1000]
                commentString += ','
                commentString += category
                commentString += '\n'
                commentsFile.write(commentString)
                print("wrote to file")
    print("done")
    commentsFile.close()
    return 0

conLanguage = writeComments(conservative_reddits, 'conservative_comments.csv', 'conservative')
libLanguage = writeComments(liberal_reddits, 'liberal_comments.csv', 'liberal')
