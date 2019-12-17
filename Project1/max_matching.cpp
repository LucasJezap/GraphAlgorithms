#include <iostream>
#include <unordered_set>
#include <list>
#include <array>
#include <queue>
#include <climits>
#define NIL 0
#define INF INT_MAX

using namespace std;

struct node{
    int index=-1;
    bool is_left=false;
    bool matched=false;
    int pair=NIL;
    int dist;
    unordered_set<int> adj = {};
};


bool BFS(node *G, int size) {
    queue<int> Q;
    for (int i=0; i<size; i++)
        if(G[i].is_left) {
            if (G[i].pair==NIL) {
                G[i].dist=0;
                Q.push(i);
            }
            else G[i].dist=INF;
        }
    G[NIL].dist=INF;
    while (!Q.empty()) {
        int u=Q.front();
        Q.pop();
        if (G[u].dist < G[NIL].dist) {
            for (int v: G[u].adj)
                if (G[G[v].pair].dist==INF) {
                    G[G[v].pair].dist=G[u].dist+1;
                    Q.push(G[v].pair);
                }
        }
    }
    return G[NIL].dist != INF;
}

bool DFS(node *G, int u) {
    if (u != NIL) {
        for (int v: G[u].adj) {
            if ( G[G[v].pair].dist==G[u].dist+1 and DFS(G,G[v].pair) ) {
                G[u].matched=true;
                G[v].pair=u;
                G[u].pair=v;
                return true;
            }
        }
        G[u].dist=INF;
        return false;
    }
    return true;
}

void Hopcroft_Karp(node *G, int size) {
    int matching=0;
    while (BFS(G,size)) {
        for (int i=0; i<size; i++)
            if (G[i].is_left and G[i].pair==NIL and DFS(G,i))
                matching++;
    }
    cout << matching << endl;
    for (int i=0; i<size; i++)
        if(G[i].is_left and G[i].matched)
            cout << i-1 << " " << G[i].pair-1 << endl;
}


int main() {
    string name;
    cin >> name;
    int size;
    cin >> size;
    node *G = new node[size+1];
    for (int i=0; i<=size; i++) {
        G[i].index=i;
    }
    int l_size;
    cin >> l_size;
    int r_size=size-l_size;
    for (int i=0; i<l_size; i++) {
        int x;
        cin >> x;
        G[x+1].is_left=true;
    }
    int edges;
    cin >> edges;
    for (int i=0; i<edges; i++) {
        int x,y;
        cin >> x >> y;
        G[x+1].adj.insert(y+1);
    }

    Hopcroft_Karp(G,size+1);
}
