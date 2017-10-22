#get reddit comments to check against watson and check
import praw
import re
import csv
import os
import os.path
import collections
import string

import json

from watson_developer_cloud import NaturalLanguageClassifierV1

natural_language_classifier = NaturalLanguageClassifierV1(
  username="66d51137-b6ef-4e73-9563-b71f3e742e45",
  password="x760OVu4CbGR")

classifier_id = 'ebd15ex229-nlc-67819'

target_reddit = 'adviceanimals'
scary_words = ['trump', 'bernie', 'cruz', 'tillerson', 'obama', 'devos', 'donald', 'hillary', 'obamacare', 'tax', 'podesta']

reddit = praw.Reddit(client_id='ZRfPmQnieqTWUw',
                         client_secret='iUpQc7K0iRw8CZM6tGmPjRBBU4I',
                         password='timberline3',
                         user_agent='political leanings by /u/thisaccounttestsbots',
                         username='thisaccounttestsbots')
    
    
def main():

    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
           posts_replied_to = f.read()
           posts_replied_to = posts_replied_to.split("\n")
           posts_replied_to = list(filter(None, posts_replied_to))
    subreddit = reddit.subreddit(target_reddit)
    for submission in subreddit.stream.submissions():
        if submission.id not in posts_replied_to:
            process_submission(submission)
            posts_replied_to.append(submission.id)
            with open("posts_replied_to.txt", "w") as f:
                for post_id in posts_replied_to:
                    f.write(post_id + '\n')
    

def findBias (user):
    comments = user.comments.new(limit=50)
    libPoints = 0
    conPoints = 0
    for comment in comments:
        text = comment.body
        text = text[0:1000]
        classification = natural_language_classifier.classify(classifier_id, text)
        class_name = classification['classes'][0]['class_name']
        confidence = classification['classes'][0]['confidence']
        if (class_name == 'liberal'):
            libPoints += confidence
        if (class_name == 'conservative'):
            conPoints += confidence
    if libPoints > conPoints:
        bias = 'liberal'
        strength = libPoints / (libPoints + conPoints)
    else:
        bias = 'conservative'
        strength = conPoints / (libPoints + conPoints)
    return [bias, strength]

def process_submission (submission):
    normalized_title = submission.title.lower()
    for words in scary_words:
        if words in normalized_title:
            user = submission.author
            [bias, strength] = findBias(user)
            strength = strength*100
            strength_percent = str(strength)[0:4]
            reply_text = "Heads Up: OP has shown "+ str(strength_percent) +"% " + str(bias) + " inclinations across his/her last 50 comments"
            reply_text += "\n\n\n Bear with me, I'm a bot. I check users' comment historys against IBM Watson's language classifier to predict political bias!"
            reply_text += "\n Am I wrong/is there a better way to use this bot? Please comment/pm and let me know!"
            submission.reply(reply_text)
            print("replied to submission")
            break

if __name__ == '__main__':
    main()
