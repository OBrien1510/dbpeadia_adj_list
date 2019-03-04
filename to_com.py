import pickle
import math

adj = pickle.load("")

dis_mat = dict()


def get_common(x, y):

    x_set = set(x)
    y_set = set(adj[y])

    common = x_set.intersection(y_set)

    return len(common)


for key, item in adj.items():

    for j in item:

        common = get_common(item, j)

        if common == 0:

            dis_mat[key][j] = math.inf

        else:

            dis_mat[key][j] = 1/common


pickle.dump(dis_mat, "")