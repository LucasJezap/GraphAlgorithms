import networkx as nx
from networkx.algorithms.flow import maximum_flow
from dimacs import loadDirectedWeightedGraph
import os
import time

def solution(test):
    (V,E)=loadDirectedWeightedGraph(test)
    G = nx.DiGraph()
    for i in range(1,V+1):
        G.add_node(i)
    for (a,b,c) in E:
        G.add_edge(a,b)
        G[a][b]['capacity']=c
    return maximum_flow(G,1,V)[0]

tests = os.listdir("graphs-lab2/flow/")
successes = 0
fullTime = 0

for i in tests:
    with open('graphs-lab2/flow/' + i) as f:
        res = int(f.readline().split()[-1])
    time1 = time.time()
    res2 = solution('graphs-lab2/flow/' + i)
    time2 = time.time()
    if res == res2:
        successes += 1
        print("Test of ", i, " was successful. ", end='')
    else:
        print("Test of ", i, " was wrong. Correct answer: ", res, " while found: ", res2, ". ", end='')
    print("It took ", time2 - time1, "s time")
    fullTime += (time2 - time1)

print(str(successes), "/", str(len(tests)))
print("It took ", fullTime, "s overall")
