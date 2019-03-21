import pymongo as pm
import multiprocessing

client = pm.MongoClient()

db = client.adj_mat

def process_cursor(skip_n, limit_n):

    for i, document in enumerate(db.first_adj.find().skip(skip_n).limit(limit_n)):

        subject = document["subject"]
        neighbours = document["neighbours"]

        n_neighbours = len(document["neighbours"])

        document = {subject: dict()}

        for key, item in neighbours.items():

            try:
                similarity = item/n_neighbours
            except Exception as e:
                print(e)
                similarity = 0
                
            #db.common_adj.find_one_and_update({"subject": subject}, {"$set" : {"subject.j" : similarity}})
            document[subject][key] = similarity

        db.first_dis.insert_one(document)

cores = 7
collection_size = db.first_adj.count()
batch_size = collection_size//7
skips = range(0, collection_size, batch_size)
threads = [multiprocessing.Process(target=process_cursor, args=(skip_n, batch_size))for skip_n in skips]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()