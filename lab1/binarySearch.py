from dimacs import *
import os
import time
import sys
sys.setrecursionlimit(100000)

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

def dfs(graph, weight, s, t):
    visited = [False] * (graph.V+1)
    stack = [s]
    while (len(stack)!=0):
        u = stack.pop(-1)
        if(not visited[u]):
            visited[u]=True
        if visited[t]:
            return True
        for (v,c) in graph.G[u]:
            if (not visited[v] and c >= weight):
                stack.append(v)
    return False

def solution(test):
    (V,E) = loadWeightedGraph(test)
    E.sort(key=lambda c: c[2], reverse=True)
    graph = Graph(E,V)
    l, r = 0, len(E)-1
    while l < r:
        m = (l+r) // 2
        if dfs(graph, E[m][2], 1, 2):
            r = m
        else:
            l = m+1

    return E[l][2]

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