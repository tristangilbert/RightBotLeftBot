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

classifier_id = '1e0d8ex232-nlc-24751'

    
    

reddit = praw.Reddit(client_id='ZRfPmQnieqTWUw',
                     client_secret='iUpQc7K0iRw8CZM6tGmPjRBBU4I',
                     password='timberline3',
                     user_agent='political leanings by /u/thisaccounttestsbots',
                     username='thisaccounttestsbots')


#target_reddit = 'pics'
#subreddit = reddit.subreddit(target_reddit)

libPoints = 0
conPoints = 0

target_user = 'newcomputernewme'
user = reddit.redditor(target_user)
comments = user.comments.new(limit=25)
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
        
    
    
    




