import pymongo as pm
import multiprocessing
import math
import numpy as np

client = pm.MongoClient()

db = client.adj_mat

def process_cursor(skip_n, limit_n):

    for i, document in enumerate(db.first_adj.find().skip(skip_n).limit(limit_n)):

        subject = document["subject"]
        neighbours = document["neighbours"]

        n_neighbours = len(document["neighbours"])

        #initialize empty dictionary to  hold document
        document = {subject: dict()}

        #initialize empty numpy array to hold similarity metrics
        similarities = np.empty_like(n_neighbours)

        #initialize empty list to hold the keys for our eventual similarity dict
        neighbours_list = list()

        for i, (key, item) in enumerate(neighbours.items()):

            try:
                #similarity metric: The number of common links with another article divided by the total number
                #of links in the entire article
                similarity = item+1/n_neighbours
            except Exception as e:
                print(e)
                similarity = 0

            #db.common_adj.find_one_and_update({"subject": subject}, {"$set" : {"subject.j" : similarity}})

            #document[subject][key] = similarity
            similarities[i] = similarity

            neighbours_list.append(key)

        #we wish to normalize all distances for each article into the range 1-0
        #and then get the inverse to convert into our distance proxy
        #we use numpy elementwise operations for this
        y = lambda x: (1 / x)

        inverse = y(similarities)

        min_sim = np.min(inverse)
        max_sim = np.max(inverse)

        difference = max_sim - min_sim

        f = lambda x: (x - min_sim) / difference

        normalized = f(inverse)

        #convert numpy array back to regualar list
        similarities = list(normalized)

        #combine list with keys with the lsit of normalized values to get final dict
        similarity_dict = dict(zip(neighbours_list, similarities))

        document[subject] = similarity_dict

        #finally insert document
        db.first_dis.insert_one(document)


cores = 7
collection_size = db.first_adj.count()
batch_size = collection_size//cores
skips = range(0, collection_size, batch_size)
threads = [multiprocessing.Process(target=process_cursor, args=(skip_n, batch_size))for skip_n in skips]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()