from dimacs import *
import os
import time
from queue import PriorityQueue

class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()              # zbiór sąsiadów

    def connect_to(self, v):
        self.out.add(v)

    def __str__(self):
        return str(self.out)

def LexBFS(G,V):
    vs=[]
    p=[None]*(V+1)
    sets=[]
    first=set()
    for i in range(1,V+1):
        first.add(i)
    sets.append(first)
    while(len(sets)>0):
        u=sets[-1].pop()
        if(len(sets[-1])==0):
            sets.pop()
        vs.append(u)
        neighbours=set()
        for neighbour in G[u].out:
            neighbours.add(neighbour)
        n_sets=[]
        for s in sets:
            Y=s&neighbours
            K=s-Y
            if len(K)>0:
                n_sets.append(K)
            if len(Y)>0:
                n_sets.append(Y)
        sets=n_sets
    return vs

def max_clique(G,V,vs):             # TODO: BETTER COMPLEXITY ?
    RN=[set() for _ in range(V+1)]
    for i in range(len(vs)):
        for j in range(i):
            if vs[j] in G[vs[i]].out:
                RN[i].add(j)
    max=0
    for r in RN:
        if(len(r)>max):
            max=len(r)
    return max+1

def solution(test):
    (V, L) = loadWeightedGraph(test)
    G = [None] + [Node(i) for i in range(1, V+1)]
    for (u, v, _) in L:
        G[u].connect_to(v)
        G[v].connect_to(u)
    vs=LexBFS(G,V)
    return max_clique(G,V,vs)



tests = os.listdir("graphs/maxclique/")
print(tests)
successes=0
fullTime=0

for i in tests:
    with open('graphs/maxclique/' + i) as f:
        res = int(f.readline().split()[-1])
    time1 = time.time()
    res2 = solution('graphs/maxclique/' + i)
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