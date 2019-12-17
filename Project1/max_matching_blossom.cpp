#include <iostream>
#include <cstring>
using namespace std;
#define V_max 10000

struct sEdge
{
    int v;
    sEdge *n;
};

typedef sEdge *Edge;

class BlossomGraph
{
    sEdge *edg;
    Edge top, adj[V_max];           // top - pointer to element of edg
    int V, E, q_head, q_tail;
    int match[V_max], q[V_max], father[V_max], base[V_max];
    bool inq[V_max], inb[V_max], inp[V_max]; // in queue, in base, in P

public:

    BlossomGraph(int V, int E) {
        this->V=V;
        this->E=E;
        edg = new sEdge[2*E+1];
        top = edg;
    }

    void add_new_edge(int u, int v) {
        top->v = v, top->n = adj[u], adj[u] = top++;
        top->v = u, top->n = adj[v], adj[v] = top++;
    }

    int LCA(int root, int u, int v) {
        memset(inp, 0, sizeof(inp));
        while (true) {
            inp[u = base[u]] = true;
            if (u == root)
                break;
            u = father[match[u]];
        }
        while (true) {
            if (inp[v = base[v]])
                return v;
            else
                v = father[match[v]];
        }
    }

    void mark_blossom(int lca, int u) {
        while (base[u] != lca){
            int v = match[u];
            inb[base[u]] = inb[base[v]] = true;
            u = father[v];
            if (base[u] != lca)
                father[u] = v;
        }
    }

    void blossom_contraction(int s, int u, int v) {
        int lca = LCA(s, u, v);
        memset(inb, 0, sizeof(inb));
        mark_blossom(lca, u);
        mark_blossom(lca, v);
        if (base[u] != lca)
            father[u] = v;
        if (base[v] != lca)
            father[v] = u;
        for (int u = 0; u < V; u++)
            if (inb[base[u]]) {
                base[u] = lca;
                if (!inq[u]) {
                    q[++q_tail]=u;
                    inq[u] = true;
                }
            }
    }

    int find_augmenting_path(int s) {
        memset(inq, 0, sizeof(inq));
        memset(father, -1, sizeof(father));
        for (int i = 0; i < V; i++)
            base[i] = i;
        q_head = q_tail = 0;
        q[q_head] = q[q_tail] = s;
        inq[s] = true;
        while (q_head <= q_tail) {
            int u = q[q_head++];
            for (Edge e = adj[u]; e; e = e->n) {
                int v = e->v;
                if (base[u] != base[v] && match[u] != v)
                    if ((v == s) || (match[v] != -1 && father[match[v]] != -1))
                        blossom_contraction(s, u, v);
                    else if (father[v] == -1) {
                        father[v] = u;
                        if (match[v] == -1)
                            return v;
                        else if (!inq[match[v]]) {
                            q[++q_tail] = match[v];
                            inq[match[v]] = true;
                        }
                    }
            }
        }
        return -1;
    }

    int augment_the_path(int s, int t) {
        int u = t, v, w;
        while (u != -1) {
            v = father[u];
            w = match[v];
            match[v] = u;
            match[u] = v;
            u = w;
        }
        return t != -1;
    }

    int edmonds() {
        int matching = 0;
        memset(match, -1, sizeof(match));
        for (int i = 0; i < V; i++)
            if (match[i] == -1)
                matching += augment_the_path(i, find_augmenting_path(i));
        return matching;
    }

    void print() {
        for (int i = 0; i < V; i++)
            if (i < match[i])
                cout << i << " " << match[i] << endl;
    }

};

int main()
{
    string name;
    cin >> name;
    int size;
    cin >> size;
    int l_size;
    cin >> l_size;
    int r_size=size-l_size;
    for (int i=0; i<l_size; i++) {
        int x;
        cin >> x;
    }
    int edges;
    cin >> edges;
    BlossomGraph bm(size, edges);
    int u, v;
    while (edges--)
    {
        cin >> u >> v;
        bm.add_new_edge (u, v);
    }
    int res = bm.edmonds();
    cout << res << endl;
    bm.print();
}
