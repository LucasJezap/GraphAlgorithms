from dimacs import *
import os
import time

def union(x,y,p):
    a = find(x, p)
    b = find(y, p)

    if(a!=b):
        p[a] = b

def find(x,p):
    if(p[x] != x):
        v = p[x]
        p[x] = find(v,p)
        return p[x]
    else:
        return x

def solution(test):
    (V,E) = loadWeightedGraph(test)
    E.sort(key=lambda c: c[2], reverse=True)
    s=1
    t=2
    parents = {i:i for i in range(1,V+1)}
    m=-1
    for (x,y,c) in E:
        union(x,y,parents)
        if(find(s,parents)==find(t,parents)):
            m=c
            break
    return m


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