from dimacs import *
import os
import time
import queue

class Graph:                                     # adjacency lists
    def __init__(self, E, V):
        self.V = V
        self.G = [[] for i in range(V+1)]

        for (x, y, c) in E:
            self.G[x].append((y,0,c))            # (destination,flow,capacity)
            self.G[y].append((x,0,c))

    def update(self,u, v, new_f, new_c):
        index = 0
        for i, (x,_,_) in enumerate(self.G[u]):
            if x==v:
                index=i
                break
        self.G[u][index] = (v,new_f,new_c)

    def print_graph(self):
        for u in range (1,self.V+1):
            print(u, " -> ", end = '')
            for (v,f,c) in self.G[u]:
                print((v,f,c),  end = '')
            print('\n')

def BFS(graph, s, t):
    p = [-1]*(graph.V+1)
    visited = [False]*(graph.V+1)
    visited[s] = True
    flow = [100000000]*(graph.V+1)
    found=False
    q = queue.Queue()
    q.put(s)
    while(not q.empty()):
        u = q.get()
        for (v,f,c) in graph.G[u]:
            if(c>0 and not visited[v]):
                visited[v]=True
                p[v]=u
                flow[v]=min(flow[u],c)
                if(v==t):
                    found=True
                    break;
                q.put(v)
        if(found):
            break
    return (p,flow)

def fordFulkerson(graph,s,t):
    fmax=0
    while(True):
        (p,flow)=BFS(graph,s,t)
        if p[t]==-1:
            break
        fmax += flow[t]
        v = t
        while v!=s:
            u=p[v]
            for (x,f,c) in graph.G[u]:
                if(x==v):
                    new_f = f + flow[t]
                    new_c = c - flow[t]
                    graph.update(u,v,new_f,new_c)
                    break
            for (x,f,c) in graph.G[v]:
                if(x==u):
                    new_f = f - flow[t]
                    new_c = c + flow[t]
                    graph.update(v,u,new_f,new_c)
                    break
            v=u
    return fmax

def solution(test):
    (V,E)= loadWeightedGraph(test)
    res=float('inf')
    s=1
    for t in range(2,V):
        graph = Graph(E,V)
        f=fordFulkerson(graph,s,t)
        if(f<res):
            res=f
    return res



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