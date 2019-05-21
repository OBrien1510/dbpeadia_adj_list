import pymongo as pm
import multiprocessing
from LinkedList import *

client = pm.MongoClient()

db = client.adj_mat

db.final_dis.remove({})

dis_dict = 0

def process_subject(current, depth):

    global dis_dict

    #print(dis_dict.length)

    if depth == 2 or (dis_dict.tail is not None and current["distance"] > dis_dict.tail.get_sim()):
        return

    document = db.first_dis.find_one({"subject": current["subject"]})
    if document is None:
        #print("broken branch")
        # branch is broken so just return as much as possible
        return

    neighbours = document["neighbours"]

    for key, item in neighbours.items():

        if isinstance(item, dict):
            # due to a previous mistake there are a very small number of document in the first_dis
            # that were inserted with the incorrect format but the number of invalid document
            # should be so small that ignoring them should not make a difference
            break
        
        distance = current["distance"] + item
        current_node = Node(distance, None, key)
        #print("before", dis_dict.length)
        dis_dict.check_sim(current_node)
        #print("after", dis_dict.length)
        process_subject({"subject": key, "distance": distance}, depth+1)

def process_cursor(skip_n, limit_n):

    for i, document in enumerate(db.first_dis.find().skip(skip_n).limit(limit_n).batch_size(100)):


        subject = document["subject"]
        neighbours = document["neighbours"]
        doc_insert = {"subject": subject, "neighbours": dict()}
        # initialize new global linked list so all recusion instances can access it.
        global dis_dict
        dis_dict = LinkedList()
        #print("Processing Subject:", subject)
        process_subject({"subject": subject , "distance": 0},  0)

        doc_insert["neighbours"] = dis_dict.linkedlist

        try:
            #print("Inserting:", subject)
            db.final_dis.insert_one(doc_insert)

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
