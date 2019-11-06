from dimacs import *
import os
import time
import heapq

class Graph:                                     # adjacency lists
    def __init__(self, E, V):
        self.V = V
        self.G = [[] for i in range(V+1)]

        for (x, y, c) in E:
            self.G[x].append((y, c))
            self.G[y].append((x, c))

    def print_graph(self):
        for u in range (1,V+1):
            print(u, " -> ", end = '')
            for (v,c) in self.G[u]:
                print((v,c),  end = '')
            print('\n')

def dfs(graph, s, t, weight):
    visited = [False] * (graph.V+1)
    dfsVisit(graph, visited, weight, s)
    return visited[t]

def dfsVisit(graph, visited, weight, x):
    visited[x]=True
    for (y,c) in graph.G[x]:
        if (not visited[y]) and (c >= weight):
            dfsVisit(graph,visited,weight,y)

def solution(test):
    (V,E) = loadWeightedGraph(test)
    E.sort(key=lambda c: c[2], reverse=True)
    graph = Graph(E,V)
    q = []
    heapq.heapify(q)
    s=1
    t=2

    d = [-10000000 for i in range(V+1)]
    d[s] = 1000000000
    heapq.heappush(q,(-d[s],s))

    while(len(q) != 0):
        p = heapq.heappop(q)
        x = p[1]
        p = -p[0]

        for (y, c) in graph.G[x]:
            if d[y] < min(c, p):
                d[y] = min(c, p)
                heapq.heappush(q, (-d[y], y))

    return d[t]




tests = os.listdir("graphs/")
print(tests)
successes=0
fullTime=0

for i in tests:
    with open('graphs/' + i) as f:
        res = int(f.readline().split()[3])
    time1 = time.time()
    res2 = solution('graphs/' + i)
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