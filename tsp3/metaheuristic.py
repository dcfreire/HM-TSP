import re
import math
import numpy as np
import os
import random

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

def compute_distance(route, adj):
    dist = 0
    for i in range(len(route) - 1):
        dist += adj[route[i]][route[i+1]]
    dist += adj[route[-1]][0]
    return dist

def two_opt_move(route, i, k):
    ret = route[0:i] + route[k:i-1:-1] + route[k+1:]
    return ret

def is_tabu(tabu, new_route):
    pass

def two_opt(route, adj, tabu, best_result, it):
    best_distance = np.inf
    best_route = []
    best_distance_tabu = np.inf
    best_route_tabu = []

    for i in range(1, len(route)):
        for j in range(i+1, len(route)):
            new_route = two_opt_move(route, i, j)
            new_distance = compute_distance(new_route, adj)

            if (new_distance < best_result):
                best_route = new_route
                best_distance = new_distance

            if (new_distance < best_distance):
                if tabu[new_route[i-1]][new_route[j]] > it or tabu[new_route[i+1]][new_route[(j+1) % len(route)]] > it:
                    if (new_distance < best_distance_tabu):
                        best_route_tabu = new_route
                        best_distance_tabu = new_distance
                else:
                    best_route = new_route
                    best_distance = new_distance

    return (best_route, best_distance) if best_route else (best_route_tabu, best_distance_tabu)

def tabu(adj, imp_time, init_tabu_size):
    tabu_size = init_tabu_size
    tabu_matrix = np.zeros(adj.shape)
    best_sol, best_cost = tsp_greedy(adj)
    prev_sol = best_sol
    improvement = 0
    iteration = 0
    while iteration - improvement < imp_time:
        iteration += 1
        sol, cost = two_opt(prev_sol, adj, tabu_matrix, best_cost, iteration)
        if cost < best_cost:
            best_cost = cost
            best_sol = sol
            improvement = iteration
            tabu_size = init_tabu_size

        if cost == best_cost:
            tabu_size = int(tabu_size*1.2)

        for i, (a, b) in enumerate(zip(sol, prev_sol)):
            if a - b:
                tabu_matrix[prev_sol[i-1]][prev_sol[i]] = random.randint(tabu_size, tabu_size + 7) + iteration
                break


        prev_sol = sol


    return best_sol, best_cost



if __name__ == "__main__":
    test_path = "tests"
    for filename in os.listdir(test_path):
        filepath = os.path.join(test_path, filename)
        adj = read_file(filepath)
        route, distance = tabu(adj, 500, 7)
        print(f"\"{filename}\": {distance}")