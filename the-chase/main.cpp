#include <bits/stdc++.h>
using namespace std;

const int INF = 1e9 + 7;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N, F;
    if (!(cin >> N >> F)) return 0;

    vector<int> A(N + 1);
    vector<int> in_degree(N + 1, 0);
    vector<vector<int>> revA(N + 1);
    for (int i = 1; i <= N; i++) {
        cin >> A[i];
        in_degree[A[i]]++;
        revA[A[i]].push_back(i);
    }

    vector<int> S(F);
    for (int i = 0; i < F; i++) {
        cin >> S[i];
    }

    vector<int> D_min(N + 1, INF);
    queue<int> q;
    for (int i = 0; i < F; i++) {
        D_min[S[i]] = 0;
        q.push(S[i]);
    }

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        int v = A[u];
        if (D_min[v] == INF) {
            D_min[v] = D_min[u] + 1;
            q.push(v);
        }
    }

    vector<int> state(N + 1, 0);
    vector<int> pos(N + 1, -1);
    vector<int> depth(N + 1, -1);
    vector<int> root(N + 1, -1);
    vector<int> cycle_id(N + 1, -1);
    vector<int> comp_id(N + 1, -1);
    
    int cycles_count = 0;
    vector<int> L_of_cycle;

    for (int i = 1; i <= N; i++) {
        if (state[i] == 0) {
            int curr = i;
            vector<int> path;
            while (state[curr] == 0) {
                state[curr] = 1;
                path.push_back(curr);
                curr = A[curr];
            }
            if (state[curr] == 1) { // Cycle found
                int len = 0;
                int start_idx = -1;
                for (int j = 0; j < path.size(); j++) {
                    if (path[j] == curr) {
                        start_idx = j;
                        break;
                    }
                }
                for (int j = start_idx; j < path.size(); j++) {
                    int node = path[j];
                    state[node] = 2;
                    pos[node] = len++;
                    depth[node] = 0;
                    root[node] = node;
                    cycle_id[node] = cycles_count;
                }
                L_of_cycle.push_back(len);
                cycles_count++;
            }
            for (int node : path) {
                state[node] = 2;
            }
        }
    }

    for (int i = 0; i < cycles_count; i++) {
        queue<int> tree_q;
        for (int j = 1; j <= N; j++) {
            if (cycle_id[j] == i) {
                comp_id[j] = i;
                tree_q.push(j);
            }
        }
        while (!tree_q.empty()) {
            int u = tree_q.front();
            tree_q.pop();
            for (int v : revA[u]) {
                if (cycle_id[v] == -1 && depth[v] == -1) {
                    depth[v] = depth[u] + 1;
                    root[v] = root[u];
                    comp_id[v] = i;
                    tree_q.push(v);
                }
            }
        }
    }

    vector<int> P(N + 1, 0);
    for (int i = 1; i <= N; i++) {
        int L = L_of_cycle[comp_id[i]];
        P[i] = (depth[i] - pos[root[i]]) % L;
        if (P[i] < 0) P[i] += L;
    }

    vector<vector<int>> comp_forbidden(cycles_count);
    for (int i = 0; i < F; i++) {
        comp_forbidden[comp_id[S[i]]].push_back(P[S[i]]);
    }

    vector<vector<int>> comp_nxt(cycles_count);
    vector<bool> comp_has_valid(cycles_count, false);

    for (int i = 0; i < cycles_count; i++) {
        int L = L_of_cycle[i];
        vector<int> valid(L, 1);
        for (int f_p : comp_forbidden[i]) {
            valid[f_p] = 0;
        }
        comp_nxt[i].assign(L, -1);
        bool has_val = false;
        for (int j = 0; j < L; j++) if (valid[j]) has_val = true;
        comp_has_valid[i] = has_val;

        if (has_val) {
            int last_valid = -1;
            for (int j = 2 * L - 1; j >= 0; j--) {
                if (valid[j % L]) last_valid = j % L;
                if (j < L) comp_nxt[i][j] = last_valid;
            }
        }
    }

    for (int b = 1; b <= N; b++) {
        if (D_min[b] == INF) {
            cout << "-2\n";
        } else {
            int R_max = D_min[b] - 1;
            if (R_max < 0) {
                cout << "-1\n";
                continue;
            }
            int cid = comp_id[b];
            if (!comp_has_valid[cid]) {
                cout << "-1\n";
                continue;
            }
            int L = L_of_cycle[cid];
            int tgt = (R_max + P[b]) % L;
            int nxt_val = comp_nxt[cid][tgt];
            int sub = (tgt - nxt_val + L) % L;
            int R = R_max - sub;
            if (R >= 0) cout << R << "\n";
            else cout << "-1\n";
        }
    }

    return 0;
}