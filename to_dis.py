import pickle

adj_mat = pickle.load("")

dis_mat = {}

def get_distance(x, y, current_depth):

    if current_depth >= 10:

        dis_mat[x][y] = current_depth
        return

    else:

        dis_mat[x][y] = current_depth
        row = adj_mat[x]

        for i in row:

            return get_distance(x, i, current_depth + 1)


num_items = 0

for key, item in adj_mat.items():

    if num_items % 100000 == 0:

        print("Current item", key)
        print("#%d" % num_items)

    get_distance(key, key, 0)

    
pickle.dump(dis_mat, "")
