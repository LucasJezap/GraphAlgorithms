from dimacs import loadDirectedWeightedGraph, loadWeightedGraph, readSolution
import time
import os


class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()  # zbiór sąsiadów

    def connect_to(self, v):
        self.out.add(v)

    def __str__(self):
        return str(self.out)


def DFS_VISIT(G, V, visited, parent, low, disc, i, count_time, result):
    visited[i] = True
    disc[i] = count_time
    low[i] = count_time
    children_count = 0
    for u in G[i].out:
        if not visited[u]:
            children_count += 1
            parent[u] = i
            DFS_VISIT(G, V, visited, parent, low, disc, u, count_time + 1, result)
            low[i] = min(low[i], low[u])
            if parent[i] == -1 and children_count > 1:
                result.add(i)
            if parent[i] != -1 and low[u] >= disc[i]:
                result.add(i)
        elif u != parent[i]:
            low[i] = min(low[i], disc[u])


def DFS(G, V):
    result = set()
    visited = [False] * (V + 1)
    parent = [-1] * (V + 1)
    low = [float("inf")] * (V + 1)
    disc = [float("inf")] * (V + 1)
    count_time = 1
    for i in range(1, V + 1):
        if not visited[i]:
            DFS_VISIT(G, V, visited, parent, low, disc, i, count_time, result)
    return result

def solution(test):
    (V, L) = loadWeightedGraph(test)
    G = [None] + [Node(i) for i in range(1, V + 1)]
    for (u, v, _) in L:
        G[u].connect_to(v)
        G[v].connect_to(u)
    result = DFS(G, V)
    return result


tests = os.listdir("graphs/articulation/")
print(tests)
successes = 0
fullTime = 0

for i in tests:
    with open('graphs/articulation/' + i) as f:
        res = eval(f.readline().split()[-1])
    time1 = time.time()
    res2 = solution('graphs/articulation/' + i)
    time2 = time.time()
    if res == res2:
        successes += 1
        print("Test of ", i , " was successful. ", end = '')
    else:
        print("Test of ", i , " was wrong. Correct answer: ", res, " while found: ", res2, ". ", end = '')
    print("It took ", time2-time1, "s time")
    fullTime += (time2-time1)

print(str(successes), "/", str(len(tests)))
print("It took ", fullTime, "s overall")
