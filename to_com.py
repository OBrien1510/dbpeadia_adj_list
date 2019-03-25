import pymongo as pm
import multiprocessing

client = pm.MongoClient()

db = client.adj_mat

print("Clearing collection")
db.common_adj.delete_many({})

client.close()

def get_common(x, y):

    x_set = set(x)
    y = y.replace(".", "")
    y = y.replace("$", "")
    filter = {"subject": str(y)}
    try:
        
        y_query = db.first_adj.find_one(filter)
        y_set = set(y_query["neighbours"])

        common = x_set.intersection(y_set)

        return len(common)

    except Exception as e:
        #print("couldn't find", filter)
        #print(e)
        return 0

def process_cursor(skip_n, limit_n):
    
    print("cursor spinning up")

    process_client = pm.MongoClient()
    db = process_client.adj_mat
    try:
        for i, document in enumerate(db.first_adj.find().skip(skip_n).limit(limit_n).batch_size(100)):
            try:
                subject = document["subject"]
                neighbours = document["neighbours"]
            except Exception as e:
                #print(e)
                #print(document)
                continue
            
            document = {"subject": subject, "neighbours": dict()}

            for j in neighbours:

                common = get_common(neighbours, j)
                document["neighbours"][subject.replace(".", "")][j.replace(".","")] = common

            try:
                db.common_adj.insert_one(document)
            except Exception as e:
                print(e)
                print("Failure on doc insert")


            if i % 10000 == 0:

                print("Documents processed:", i)

    except Exception as e:
        print(e)
        print("failed on find")        


cores = 7
collection_size = db.first_adj.count()
batch_size = collection_size//7
skips = range(0, collection_size, batch_size)
threads = [multiprocessing.Process(target=process_cursor, args=(skip_n, batch_size))for skip_n in skips]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
