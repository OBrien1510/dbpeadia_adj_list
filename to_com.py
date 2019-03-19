import pymongo as pm
import threading

client = pm.MongoClient()

db = client.adj_mat

def get_common(x, y):

    x_set = set(x)
    y_query = db.first_adj.find({"subject:'%s'", y})
    y_set = set(y_query.neighbours)

    common = x_set.intersection(y_set)

    return len(common)

def process_cursor(cursor):

    print("cursor spinning up")

    for i, document in enumerate(db.first_adj.find()):

        subject = document.subject
        neighbours = document.neighbours

        document = {subject: dict()}

        for j in neighbours:

            common = get_common(neighbours, j)
            document[subject][j] = common

        db.first_adj.insert_one(document)

        if i % 10000 == 0:

            print("Documents processed:", i)


cursors = db.first_adj.parallel_scan(7)

threads = [threading.Thread(target=process_cursor, args=(cursor,))for cursor in cursors]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()