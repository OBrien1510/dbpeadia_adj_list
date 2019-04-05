import pymongo as pm
import multiprocessing
import re
import numpy as np
import math

client = pm.MongoClient()

db = client.adj_mat

db.first_dis.remove({})

def get_similarity(n):

    doc = db.common_adj.find_one({"subject":n})

    return doc

def process_cursor(skip_n, limit_n):

    for i, document in enumerate(db.common_adj.find().skip(skip_n).limit(limit_n).batch_size(100)):

        subject = document["subject"]
        neighbours = document["neighbours"]

        n_neighbours = len(neighbours)
        #initialize empty dictionary to  hold document
        document = {"subject": subject, "neighbours": dict()}

        if n_neighbours == 1:

            document["neighbours"][list(neighbours.keys())[0]] = 0
            
        else:

            neighbours_list = list()
            similarities = np.ones(n_neighbours)

            for i, (key, item) in enumerate(neighbours.items()):

                pattern = re.compile("Category:(.+)")

                m = pattern.match(key)

                if m:
                    
                    cleaned_neighbour = m.group(1)

                else:

                    cleaned_neighbour = key

                try:
                    #similarity metric: The number of common links with another article divided by the total number
                    #of links in the entire article
                    #n = get_similarity(key)

                    similarity =  (1/((item+1)/1+math.log(n_neighbours)))

                except Exception as e:
                    print(e)
                    similarity = 0

                #db.common_adj.find_one_and_update({"subject": subject}, {"$set" : {"subject.j" : similarity}})

                #document[subject][key] = similarity
                similarities[i-1] = similarity

                neighbours_list.append(cleaned_neighbour)

            #we wish to normalize all distances for each article into the range 1-0
            #and then get the inverse to convert into our distance proxy
            #we use numpy elementwise operations for this
            y = lambda x: (1 / x)

            inverse = y(similarities)

            min_sim = np.min(inverse)
            max_sim = np.max(inverse)

            difference = max_sim - min_sim

            f = lambda x: (x - min_sim) / difference

            f2 = lambda x: abs(x -1)

            normalized = f(inverse)

            normalized = f2(normalized)

            #convert numpy array back to regualar list
            similarities = list(normalized)

            #combine list with keys with the lsit of normalized values to get final dict
            similarity_dict = dict(zip(neighbours_list, similarities))

            document["neighbours"] = similarity_dict


        #finally insert document
        if len(list(document["neighbours"].keys())) == 1:
            document["neighbours"][list(document["neighbours"].keys())[0]] = 0

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
