import re
import numpy as np
import math
import os

def read_file(file_path):
    with open(file_path) as fp:
        line = fp.readline()
        while not line.startswith("DIMENSION"):
            line = fp.readline()
        dim = int(re.findall(r"\d+$", line)[0])

        line = fp.readline()

        while not line.startswith("EDGE_WEIGHT_TYPE"):
            line = fp.readline()

        weight = re.findall(r"\S+$", line)[0]

        while not fp.readline().startswith("NODE_COORD_SECTION"):
            continue

        line = fp.readline()
        coords = []
        while not line.startswith("EOF"):
            _, x, y = map(float, re.findall(r"\d+\.?\d*", line))
            coords.append((x, y))
            line = fp.readline()


        adj = np.zeros((dim, dim))
        for i, v in enumerate(coords):
            adj[i, i] = np.inf
            for j in range(i+1, dim):
                adj[i, j] = d(v, coords[j], weight)

        adj = adj + adj.T
        return adj



def d(p1, p2, weight):
    xd = p1[0] - p2[0]
    yd = p1[1] - p2[1]
    if weight == "EUC_2D":
        return int(round(math.sqrt(xd**2 + yd**2)))

    if weight == "ATT":
        r= math.sqrt((xd**2 + yd**2)/10.0)
        t= int(round(r ))
        return t + 1 if t < r else t

    return None

def tsp_optimized(adj):
    cost = 0
    not_visited = list(range(0, adj.shape[0]))
    c = 0
    cur = 0
    while c < adj.shape[0] - 1:
        visit = -1

        # Faster than deleting rows on numpy, does not improve assymptotic complexity complexity over deleting rows (And it's uglier)
        for i in not_visited[1:]:
            if i >= 0:
                if visit < 0:
                    visit = i
                elif adj[cur][i] < adj[cur][visit]:
                    visit = i

        not_visited[cur] = -1
        cost += adj[cur][visit]
        cur = visit
        c += 1
    return int(cost + adj[0][cur])


#def tsp(adj):
#    full_adj = adj.copy()
#    cost = 0
#    cur = 0
#    while adj.shape[0] > 1:
#        visit = np.argmin(adj[cur])
#        cost += adj[cur][visit]
#        adj = np.delete(adj, cur, axis=0)
#        adj = np.delete(adj, cur, axis=1)
#        cur = visit if cur > visit else visit - 1


#    return cost


if __name__ == "__main__":
    test_path = "tests"
    for filename in os.listdir(test_path):
        filepath = os.path.join(test_path, filename)
        adj = read_file(filepath)
        res = tsp_optimized(adj)
        print(f"{filename}: {res}")