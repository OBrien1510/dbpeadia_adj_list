import pymongo as pm
import multiprocessing
from LinkedList import *
import math

client = pm.MongoClient()

db = client.adj_mat

db.final_dis.remove({})

def process_subject(current, dis_dict, depth, seen):

    #dis_dict.to_str()
    if depth == 3:
       return dis_dict

    document = db.first_dis.find_one({"subject": current["subject"]})
    # if query returns nothing, branch is dead so return
    if document == None:
        print("no document found... returning")
        return dis_dict

    neighbours = document["neighbours"]
    
    for key, item in neighbours.items():
        # occasionally some of the distances will be nan, skip these branches
        distance = current["distance"] + float(item)
        current_node = Node(distance, None, key)
        dis_dict.check_sim(current_node)         
        # recursively update the current linked list with the next neighbour
        process_subject({"subject": key, "distance": distance}, dis_dict, depth+1, seen)

    return dis_dict

def process_cursor(skip_n, limit_n):

    for i, document in enumerate(db.first_dis.find().skip(skip_n).limit(limit_n).batch_size(100)):


        subject = document["subject"]
        if i % 1000:
            print("Article #", i)
            print("Subject", subject)

        doc_insert = {"subject": subject, "neighbours": dict()}

        try:
            distance_dict = process_subject({"subject": subject, "distance": 0}, LinkedList(), 0, set())
            doc_insert["neighbours"] = distance_dict.linkedlist
            db.final_dis.insert_one(doc_insert)
        except Exception as e:
            print("Failed process subject")
            print(e)


cores = 7
collection_size = db.first_adj.count()
batch_size = collection_size//cores
skips = range(0, collection_size, batch_size)
threads = [multiprocessing.Process(target=process_cursor, args=(skip_n, batch_size))for skip_n in skips]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
