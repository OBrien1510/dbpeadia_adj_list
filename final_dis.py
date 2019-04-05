import pymongo as pm
import multiprocessing
from LinkedList import *

client = pm.MongoClient()

db = client.adj_mat

db.final_dis.remove({})

def process_subject(current, dis_dict, depth, seen):

    if depth == 3:
        return dis_dict

    document = db.first_dis.find_one({"subject": current["subject"]})
    neighbours = document["neighbours"]

    for key, item in neighbours.items():

        distance = current["distance"] + item
        current = Node(distance, None, key)
        if key not in seen:
            dis_dict.check_sim(current)
            seen.add(key)
        else:
            dis_dict.update_node(current)
        dis_dict = process_subject({"subject": key, "distance": distance}, dis_dict, depth+1, seen)

    return dis_dict

def process_cursor(skip_n, limit_n):

    for i, document in enumerate(db.first_dis.find().skip(skip_n).limit(limit_n)):


        subject = document["subject"]
        
        doc_insert = {"subject": subject, "neighbours": dict()}

        distance_dict = process_subject({"subject": subject, "distance": 0}, LinkedList(), 0, set())

        doc_insert["neighbours"] = distance_dict.linkedlist

        try:

            db.first_dis.insert_one(doc_insert)
            distance_dict = 0

        except Exception as e:

            print(e)
            print("Failed to insert subject:", subject)


cores = 7
collection_size = db.first_adj.count()
batch_size = collection_size//cores
skips = range(0, collection_size, batch_size)
threads = [multiprocessing.Process(target=process_cursor, args=(skip_n, batch_size))for skip_n in skips]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
