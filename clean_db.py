"""
This file is designed to 'clean' the original adjacency list, essentially removing all articles that don't
exceed a certain arbitrary threshold for number of links
"""

import pymongo as pm
import multiprocessing

client = pm.MongoClient()

db = client.adj_mat

def process_cursor(skip_n, limit_n):

    process_client = pm.MongoClient()
    db = process_client.adj_mat

    for i, document in enumerate(db.first_adj.find().skip(skip_n).limit(limit_n).batch_size(100)):

        # only add a new document if the old one has more than 10 links
        if len(document["neighbours"]) > 10:

            doc_insert = {
                "subject": document["subject"],
                "neighbours": document["neighbours"]
            }

            db.clean_adj.insert_one(doc_insert)


cores = 7
collection_size = db.first_adj.count()
batch_size = collection_size//7
skips = range(0, collection_size, batch_size)
threads = [multiprocessing.Process(target=process_cursor, args=(skip_n, batch_size))for skip_n in skips]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
