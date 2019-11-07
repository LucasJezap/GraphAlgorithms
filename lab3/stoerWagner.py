from dimacs import *
import os
import time
from queue import PriorityQueue


class Node:
    def __init__(self):
        self.edges = {}    # słownik par mapujący wierzchołki do których są krawędzie na ich wagi

    def addEdge( self, to, weight):
        self.edges[to] = self.edges.get(to,0) + weight  # dodaj krawędź do zadanego wierzchołka
    # o zadanej wadze; a jeśli taka krawędź
    # istnieje, to dodaj do niej wagę

    def delEdge( self, to ):
        del self.edges[to]


def mergeVertices(graph,x,y):
    tmp = list(graph[y].edges.items())
    for (v,c) in tmp:
        graph[y].delEdge(v)
        graph[v].delEdge(y)
        if (v!=x):
            graph[v].addEdge(x,c)
            graph[x].addEdge(v,c)


def minimumCutPhase(graph):
    weights = [0]*(len(graph))
    a = 1
    S = []
    visited = [False]*(len(graph))
    Q = PriorityQueue()
    Q.put((weights[a],a))

    while(not Q.empty()):
        (w, u) = Q.get()
        w = -w
        if (not visited[u]):
            visited[u]=True
            S.append(u)
            for (v, c) in graph[u].edges.items():
                if (not visited[v]):
                    weights[v] += c
                    Q.put((-weights[v], v))

    s = S[-1]
    t = S[-2]

    c_p = 0
    for (v, c) in graph[s].edges.items():
        c_p += c

    mergeVertices(graph,s,t)
    return c_p




def solution(test):
    (V,E) = loadWeightedGraph(test)
    graph = [ Node() for i in range(V+1) ]

    for (x,y,c) in E:
        graph[x].addEdge(y,c)
        graph[y].addEdge(x,c)
    V_n = V
    e_c = float('inf')
    while(V_n > 1):
        e_c = min(e_c, minimumCutPhase(graph))
        V_n -= 1

    return e_c



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