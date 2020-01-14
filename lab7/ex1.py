import networkx as nx
from networkx.algorithms.planarity import check_planarity
from dimacs import loadWeightedGraph
import os
import time

def solution(test):
    (V,E)=loadWeightedGraph(test)
    G = nx.Graph()
    for i in range(1,V+1):
        G.add_node(i)
    for (a,b,c) in E:
        G.add_edge(a,b)
    return check_planarity(G)[0]

tests = os.listdir("graphs-lab6/plnar/")
successes = 0
fullTime = 0

for i in tests:
    with open('graphs-lab6/plnar/' + i) as f:
        res = int(f.readline().split()[-1])
    time1 = time.time()
    res2 = solution('graphs-lab6/plnar/' + i)
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
