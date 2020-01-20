#include <iostream>
#include <unordered_set>
#include <list>
#include <array>
#include <queue>
#include <climits>
#define NIL 0
#define INF INT_MAX

using namespace std;

struct BNode{
    int index=-1;
    bool is_left=false;
    bool matched=false;
    int pair=NIL;
    int dist;
    unordered_set<int> adj = {};
};

struct Edge {
    int from;
    int to;
    int l;
    int u;
    bool used;
};

struct Node {
    int number;
    Edge *out[2]= {nullptr,nullptr};
};

bool BFS(BNode *G, int size) {
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

bool DFS(BNode *G, int u) {
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

int Hopcroft_Karp(BNode *G, int size) {
    int matching=0;
    while (BFS(G,size)) {
        for (int i=0; i<size; i++)
            if (G[i].is_left and G[i].pair==NIL and DFS(G,i))
                matching++;
    }
    return matching;
}

void solution(Node *G, int n) {
    BNode *H = new BNode[2*n+1];
    for (int i=0; i<2*n+1; i++) {
        H[i].index = i;
    }
    for (int i=1; i<n+1; i++) {
        H[i].is_left=true;
    }
    for (int i=1; i<n+1; i++) {
        for (int j=0; j<2; j++) {
            if(G[i].out[j] != nullptr) {
                H[i].adj.insert(G[i].out[j]->to+n);
            }
        }
    }
    int x = Hopcroft_Karp(H,2*n+1);
    int l=INT_MIN;
    int r=INT_MAX;
    for (int i=1; i<n+1; i++) {
        for (int j=0; j<2; j++) {
            if(G[i].out[j] != nullptr and G[i].out[j]->to == H[i].pair-n) {
                l=max(l,G[i].out[j]->l);
                r=min(r,G[i].out[j]->u);
            }
        }
    }
    if (x != n || l>r) {                                          // no perfect matching, no answer
        cout << -1 << endl;
        return;
    }
    cout << l << endl;
    for (int i=1; i<n+1; i++)
        cout << i << " " << H[i].pair-n << endl;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        int m;
        cin >> m;
        Node *G = new Node[n+1];
        for (int i=1; i<n+1; i++)
            G[i].number = i;
        for (int i=0; i<m; i++) {
            int from,to,l,u;
            cin  >> from >> to >> l >> u;
            Edge *x = new Edge;
            x->from = from;
            x->to = to;
            x->l = l;
            x->u = u;
            if (G[from].out[0] == nullptr)
                G[from].out[0] = x;
            else
                G[from].out[1] = x;
        }
        solution(G,n);
    }
}

