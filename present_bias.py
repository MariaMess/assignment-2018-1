import sys

def read_file(filename):
  nodes = []
  edges = []
  with open(filename)  as input_file:
      for line in input_file:
          parts = line.split(' ')
          if len(parts) == 3:
            if (parts[0] not in nodes):
              nodes.append(parts[0])
            if (parts[1] not in nodes):
              nodes.append(parts[1])
            edges.append([parts[0],parts[1],int(float(parts[2]))])
  return (nodes, edges)

def adjacency_list(edges, s):
  neighbors = []
  for e in edges:
    if e[0] == s:
      neighbors.append(e[1])
  return neighbors

def all_simple_paths(edges, s, t, current_path, all_paths):
  current_path.append(s)
  if s == t:
    all_paths.append(current_path)
  else:
    for v in adjacency_list(edges, s):
      if v not in current_path:
        all_paths = all_simple_paths(edges, v, t, current_path.copy(), all_paths.copy())
  return all_paths

def calculate_real_cost(edges, path):
  cost = 0
  for j in range(0, len(path)-1):
    for e in edges:
      if e[0] == path[j] and e[1] == path[j + 1]:
        cost += e[2]
  return cost

def calculate_biased_cost(edges, path, b):
  cost = 0
  for j in range(0, len(path)-1):
    for e in edges:
      if e[0] == path[j] and e[1] == path[j + 1]:
        if j == 0:
          cost += e[2]
        else:
          cost += e[2] * b
  return cost

def present_bias_next_node(edges, s, t, b):
  paths = all_simple_paths(edges, s, t, [], [])
  costs = [0] * len(paths)
  for i in range(0, len(paths)):
    costs[i] = calculate_biased_cost(edges, paths[i], b)
  best_cost = costs[0]
  best_path = paths[0]
  for i in range(0, len(costs)):
    if costs[i] < best_cost:
      best_cost = costs[i]
      best_path = paths[i]
  return best_path[1]

def present_bias_path(edges, s, t, b, current_path):
  current_path.append(s)
  if s == t:
    return current_path
  else:
    next = present_bias_next_node(edges, s, t, b)
    return present_bias_path(edges, next, t, b, current_path)

(nodes, edges) = read_file(sys.argv[1])
b = float(sys.argv[2])
s = sys.argv[3]
t = sys.argv[4]

paths = all_simple_paths(edges, s, t, [], [])

costs = [0] * len(paths)
for i in range(0, len(paths)):
  costs[i] = calculate_real_cost(edges,paths[i])
best_cost = min(costs)
for i in range(0, len(costs)):
  if costs[i] == best_cost:
    best_path = paths[i]
print(best_path, end=' ')
print(best_cost)

biased_path = present_bias_path(edges, s, t, b, [])
print(biased_path, end=' ')
biased_path_real_cost = calculate_real_cost(edges,biased_path)
print(biased_path_real_cost)
