#interact with watson nlc api

import json

from watson_developer_cloud import NaturalLanguageClassifierV1

natural_language_classifier = NaturalLanguageClassifierV1(
  username="66d51137-b6ef-4e73-9563-b71f3e742e45",
  password="x760OVu4CbGR")

classifier_id = '1e0d8ex232-nlc-24751'

text = 'I like trump'

#request classification
classification = natural_language_classifier.classify(classifier_id, text)
class_name = classification['classes'][0]['class_name']
confidence = classification['classes'][0]['confidence']
print(confidence)
