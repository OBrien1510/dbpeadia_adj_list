from .MultiLayerPerceptron import MultiLayerPerceptron as mlp
import pymongo as pm
import numpy as np
from matplotlib import pyplot as plt

client = pm.MongoClient()

db = client.adj_mat

count = db.first_adj.count()

cluster_size = 100

skips = range(0, count, 50)

subject_hot = db.first_adj.find().distinct("subject")

size = len(subject_hot)

subject_dict = dict(zip(subject_hot, list(range(0, size))))

autoencoder = mlp((count, count/cluster_size, count), hidden_activation="tanh", output_activation="softmax", linear_factor=1,
                  max_iters=10000, learning_rate=0.1, loss="crossentropy", verbose=True, weight_update=5)

total_errors = list()

for skip in skips:

    train = list()

    for i, document in enumerate(db.first_adj.find().skip(skip).limit(50)):

        example = np.zeros(count)

        for n in document["neighbour"]:

            index = subject_dict[n]
            example[index] = 1

        train.append(example)

    errors = autoencoder.fit(train, train)
    total_errors = total_errors + errors



plt.figure()
plt.plot(total_errors, color="blue")
plt.xlabel("$Epochs$")
plt.ylabel("$Error$")
plt.title("Error v Epochs")

