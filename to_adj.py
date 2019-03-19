"""
Original Source and credit: https://gist.github.com/markharwood/21c723039425b4b3e4277b2bffa5c54c
"""
import bz2, os, re
from urllib.request import unquote
from importlib import reload
import sys
import json
import pymongo as pm

reload(sys)

# Download of data http://downloads.dbpedia.org/2016-04/core-i18n/en/page_links_en.ttl.bz2
filename = sys.argv[1]
indexName = "dbpedialinks"
docTypeName = "article"

linePattern = re.compile(r'<http://dbpedia.org/resource/([^>]*)> <[^>]*> <http://dbpedia.org/resource/([^>]*)>.*',
                         re.MULTILINE | re.DOTALL)
actions = []
rowNum = 0
lastSubject = ""
article = {}
numLinks = 0
numOrigLinks = 0
nameHash = []
numberArticles = 0
adj_mat = {}
client = pm.MongoClient()

db = client.adj_mat
collection = db.first_adj


def addLink(article, subject):

    if subject.startswith("Category:"):
        article["linked_categories"].append(subject[len("Category:"):])
    else:
        article["linked_subjects"].append(subject)

def newArticle(subject):

    article = {}
    article["subject"] = subject
    article["linked_subjects"] = []
    article["linked_categories"] = []
    addLink(article, subject)
    return article


last_line = ""

#with bz2.open(filename, "rt", encoding="utf-8") as file:
with open(filename, "r", encoding="utf-8") as file:
    for line in file:

        m = linePattern.match(str(line))

        if m:
            subject = unquote(m.group(1)).replace('_', ' ')
            linkedSubject = unquote(m.group(2)).replace('_', ' ')
            subject = subject.replace(".","")
            if numberArticles == 0:

                #adj_mat[subject] = []
                document = {
                    subject: []
                }
                try:
                    collection.insert_one(document)
                except Exception as e:
                    print(e)
                lastSubject = subject
                numberArticles += 1
                print("Current Subject", subject)
                print("Articles processed", numberArticles)
                print("Current Link", line)

            elif subject != lastSubject:


                #adj_mat[subject] = []
                document = {
                    "subject": subject,
                    "neighbours": []
                }
                try:
                    collection.insert_one(document)
                except Exception as e:
                    print(e)
                lastSubject = subject
                numberArticles += 1

                if numberArticles % 10000 == 0:
                    print("Line", line)
                    print("Last line", last_line)

                    print("Current Subject", subject)
                    print("Articles processed", numberArticles)
                    print("Current Link", line)

            else:
                try:
                    collection.find_one_and_update({"subject": subject}, {"$push": {"neighbours": '%s' % linkedSubject}})
                
                    numLinks += 1

                except Exception as e:

                   print(e)

            last_line = line


