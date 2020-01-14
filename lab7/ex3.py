import networkx as nx
from networkx.algorithms.components import strongly_connected_components
from networkx.algorithms.dag import topological_sort
from dimacs import loadCNFFormula
import os
import time

def check(result,E):
    for (a,b) in E:
        if a>0 and b>0:
            if not result[a] and not result[b]:
                return False
        elif a>0 and b<0:
            if not result[a] and result[-b]:
                return False
        elif a<0 and b>0:
            if result[-a] and not result[b]:
                return False
        else:
            if result[-a] and result[-b]:
                return False
    return True

def solution(test):
    (V,E)=loadCNFFormula(test)
    G = nx.DiGraph()
    for i in range(-V,V+1):
        G.add_node(i)
    G.remove_node(0)
    for (a,b) in E:
        G.add_edge(-a,b)
        G.add_edge(-b,a)
    SCC = strongly_connected_components(G)
    for S in SCC:
        for v in S:
            if -v in S:
                return False
    components_map={}
    components_list=[]
    t=0
    SCC = strongly_connected_components(G)
    for S in SCC:
        for v in S:
            components_map[v] = t
        t += 1
        components_list.append(S)
    H = nx.DiGraph()
    for v in range(len(components_list)):
        H.add_node(v)
    for edge in G.edges:
        c1 = components_map[edge[0]]
        c2 = components_map[edge[1]]
        if c1 != c2:
            H.add_edge(c1,c2)
    O=topological_sort(H)
    result = {}
    for v in O:
        for x in components_list[v]:
            if x>0 and not x in result:
                result[x] = False
            elif x<0 and not -x in result:
                    result[-x] = True
    for i in range(1,V+1):
        print('X'+str(i)+' = '+str(result[i]))
    if check(result,E):
        print("The result is correct")
    else:
        print("The result is incorrect")
    return True


tests = os.listdir("sat/sat")
successes = 0
fullTime = 0

for i in tests:
    with open('sat/sat/' + i) as f:
        res = int(f.readline().split("=")[-1])
    time1 = time.time()
    res2 = solution('sat/sat/' + i)
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
