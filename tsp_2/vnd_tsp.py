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

def tsp_greedy(adj):
    route = []
    cost = 0
    not_visited = list(range(0, adj.shape[0]))
    c = 0
    cur = 0
    while c < adj.shape[0] - 1:
        route.append(cur)
        visit = -1

        # Faster than deleting rows on numpy, does not improve assymptotic complexity over deleting rows (And it's uglier)
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
    route.append(cur)

    return route, int(cost + adj[cur][0])

def two_opt_move(route, i, k):
    ret = route[0:i] + route[k:i-1:-1] + route[k+1:]
    return ret

def compute_distance(route, adj):
    dist = 0
    for i in range(len(route) - 1):
        dist += adj[route[i]][route[i+1]]
    dist += adj[route[-1]][0]
    return dist

def two_opt(route, adj):
    best_distance = compute_distance(route, adj)
    improvement = True
    while improvement:
        improvement = False
        for i in range(1, len(route)):
            for j in range(i+1, len(route)):
                new_route = two_opt_move(route, i, j)
                new_distance = compute_distance(new_route, adj)
                if (new_distance < best_distance):
                    route = new_route
                    best_distance = new_distance
                    improvement = True
    return route, best_distance


def three_opt_move(route, i, k, j, adj):
    move1 = route[:i] + route[k:i-1:-1] + route[j:k-1:-1] + route[k+1:]
    move2 = route[:i] + route[k:j] + route[i:k] + route[k+1:]
    move3 = route[:i] + route[k:j] + route[k:i-1:-1] + route[k+1:]
    move4 = route[:i] + route[j:k-1:-1] + route[i:k] + route[k+1:]
    moves = [move1, move2, move3, move4]
    best = compute_distance(move1, adj)
    idx = 0
    for m, move in enumerate(moves[1:]):
        cur = compute_distance(move, adj)
        if cur < best:
            best = cur
            idx = m
    return moves[idx], best

def three_opt(route, adj):
    improvement = True
    best_distance = compute_distance(route, adj)
    while improvement:
        improvement = False
        for i in range(1, len(route)):
            for k in range(i+1, len(route)):
                for j in range(k+1, len(route)):
                    new_route, new_distance = three_opt_move(route, i, k, j, adj)
                    if (new_distance < best_distance):
                        route = new_route
                        best_distance = new_distance
                        improvement = True
    return route, best_distance


def tsp_vnd(adj):
    best_route, best_distance = tsp_greedy(adj)

    improvement = True
    while improvement:
        improvement = False
        two_opt_route, _ = two_opt(best_route, adj)
        three_opt_route, three_opt_distance = three_opt(two_opt_route, adj)
        if three_opt_distance < best_distance:
            improvement = True
            best_route = three_opt_route
            best_distance = three_opt_distance
    return best_route, best_distance



if __name__ == "__main__":
    test_path = "tests"
    for filename in os.listdir(test_path):
        filepath = os.path.join(test_path, filename)
        adj = read_file(filepath)
        route, distance = tsp_vnd(adj)
        print(f"\"{filename}\": {distance}")