from __future__ import division
import math, random, re
from collections import defaultdict, Counter, deque
from linear_algebra import dot, get_row, get_column, make_matrix, magnitude, scalar_multiply, shape, distance
from functools import partial

users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Klein" }
]

friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
               (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

# give each user a friends list
for user in users:
    user["friends"] = []
    
# and populate it
for i, j in friendships:
    # this works because users[i] is the user whose id is i
    users[i]["friends"].append(users[j]) # add i as a friend of j
    users[j]["friends"].append(users[i]) # add j as a friend of i   

from collections import deque

def shortest_paths_from(from_user):
    shortest_paths_to = { from_user["id"] : [[]] }
    frontier = deque((from_user, friend)
            for friend in from_user["friends"])
    while frontier:
        prev_user, user = frontier.popleft()
        user_id = user["id"]
        paths_to_prev_user = shortest_paths_to[prev_user["id"]]
        new_paths_to_user = [path + [user_id] for path in paths_to_prev_user]

        old_paths_to_user = shortest_paths_to.get(user_id, [])

        if old_paths_to_user:
            min_path_length = len(old_paths_to_user[0])
        else:
            min_path_length = float('inf')

        new_paths_to_user = [path
                for path in new_paths_to_user
                if len(path) <= min_path_length
                and path not in old_paths_to_user]

        shortest_paths_to[user_id] = old_paths_to_user + new_paths_to_user

        frontier.extend((user, friend)
                for friend in user["friends"]
                if friend["id"] not in shortest_paths_to)
    return shortest_paths_to

for user in users:
    user["shortest_paths"] = shortest_paths_from(user)

for user in users:
    user["betweenness_centrality"] = 0.0

for source in users:
    source_id = source["id"]
    for target_id, paths in source["shortest_paths"].iteritems():
        if source_id < target_id:
            num_paths = len(paths)
            contrib = 1 / num_paths
            for path in paths:
                for id in path:
                    if id not in [source_id, target_id]:
                        users[id]["betweenness_centrality"] += contrib

# Closeness centrality

def farness(user):
    return sum(len(paths[0])
            for paths in user["shortest_paths"].values())

for user in users:
    user["closeness_centrality"] = 1 / farness(user)
# for user in users:
    # print user["closeness_centrality"]

def matrix_product_entry(A, B, i, j):
    return dot(get_row(A, i), get_column(B, j))

def matrix_multiply(A, B):
    n1, k1 = shape(A)
    n2, k2 = shape(B)
    if k1 != n2:
        raise ArithmeticError("incompatible shapes!")
                
    return make_matrix(n1, k2, partial(matrix_product_entry, A, B))

def vector_as_matrix(v):
    """returns the vector v (represented as a list) as a n x 1 matrix"""
    return [[v_i] for v_i in v]
    
def vector_from_matrix(v_as_matrix):
    """returns the n x 1 matrix as a list of values"""
    return [row[0] for row in v_as_matrix]

def matrix_operate(A, v):
    v_as_matrix = vector_as_matrix(v)
    product = matrix_multiply(A, v_as_matrix)
    return vector_from_matrix(product)

def find_eigenvector(A, tolerance=0.00001):
    guess = [1 for __ in A]

    while True:
        result = matrix_operate(A, guess)
        length = magnitude(result)
        next_guess = scalar_multiply(1/length, result)
        
        if distance(guess, next_guess) < tolerance:
            return next_guess, length # eigenvector, eigenvalue
        
        guess = next_guess

def entry_fn(i, j):
    return 1 if (i, j) in friendships or (j, i) in friendships else 0

n = len(users)
adjacency_matrix = make_matrix(n, n, entry_fn)

#
# directed graphs
#

endorsements = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1), (1, 3),
                (2, 3), (3, 4), (5, 4), (5, 6), (7, 5), (6, 8), (8, 7), (8, 9)]

for user in users:
    user["endorses"] = []
    user["endorsed_by"] = []

for source_id, target_id in endorsements:
    users[source_id]["endorses"].append(users[target_id])
    users[target_id]["endorsed_by"].append(users[source_id])

endorsements_by_id = [(user["id"], len(user["endorsed_by"])) for user in users]

sorted(endorsements_by_id, key=lambda (user_id, num_endorsements): num_endorsements, reverse = True)

def page_rank(users, damping=0.85, num_iters = 100):
    num_users = len(users)
    pr = { user["id"]: 1 / num_users for user in users }

    base_pr = (1 - damping) / num_users

    for _ in range(num_iters):
        next_pr = { user["id"]: base_pr for user in users }
        for user in users:
            links_pr = pr[user["id"]] * damping
            for endorsee in user["endorses"]:
                next_pr[endorsee["id"]] += links_pr / len(user["endorses"])
        pr = next_pr
    return pr

print page_rank(users)