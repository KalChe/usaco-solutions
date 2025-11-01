#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int xPositions(const vector<int> &p, int x) {
    int m = (int)p.size();
    int cnt = 0;
    int i = 0;
    while (i < m) {
        int j = i;
        int base = p[i];
        // extend j while next pos within base + x
        while (j + 1 < m && p[j+1] - base <= x) ++j;
        ++cnt;
        i = j + 1;
    }
    return cnt;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int N;
    if (!(cin >> N)) return 0;
    vector<int> a(N);
    for (int i = 0; i < N; ++i) cin >> a[i];

    // positions per label
    vector<vector<int>> pos(N + 1);
    for (int i = 0; i < N; ++i) pos[a[i]].push_back(i + 1);

    int z = max(1, (int)floor(sqrt((double)N))); // threshold

    // Split heavy and light labels
    vector<vector<int>*> heavy;
    vector<vector<int>*> light;
    heavy.reserve(N / max(1, z));
    for (int val = 1; val <= N; ++val) {
        if (pos[val].empty()) continue;
        if ((int)pos[val].size() > z) heavy.push_back(&pos[val]);
        else light.push_back(&pos[val]);
    }

    // heavy contributions: heavy_ans[x] for x=1..N
    vector<int> heavy_ans(N + 2, 0);

    // Process heavy labels
    for (auto pptr : heavy) {
        const vector<int> &p = *pptr;
        // nxt[i] = first index >= i that is in p, or N+1
        vector<int> nxt(N + 2, N + 1); // indices 0..N+1 (we use 1..N)
        for (int idx : p) nxt[idx] = idx;
        for (int i = N; i >= 1; --i) if (nxt[i] == N + 1) nxt[i] = nxt[i + 1];

        int start = p.front();
        // For each x count groups by jumping
        for (int x = 1; x <= N; ++x) {
            int cnt = 0;
            int i = start;
            while (i <= N) {
                ++cnt;
                int jump_to = i + x + 1;
                if (jump_to > N) break;
                i = nxt[jump_to];
                if (i == N + 1) break;
            }
            heavy_ans[x] += cnt;
        }
    }

    // build diff array from min_x[t] ranges for light labels
    vector<ll> diff(N + 3, 0); // 1..N used

    for (auto pptr : light) {
        const vector<int> &p = *pptr;
        int m = (int)p.size();
        if (m == 0) continue;
        if (m == 1) {
            diff[1] += 1;
            diff[N + 1] -= 1;
            continue;
        }
        int max_span = p.back() - p.front();
        vector<int> min_x(m + 1, 0); // min_x[t] for t=1..m

        // binary search minimal x such that xPositions(p, x) <= t
        for (int t = 1; t <= m; ++t) {
            int lo = 0, hi = max_span;
            while (lo < hi) {
                int mid = (lo + hi) >> 1;
                if (xPositions(p, mid) <= t) hi = mid;
                else lo = mid + 1;
            }
            min_x[t] = lo;
        }
        // enforce monotonicity nonincreasing
        for (int t = 2; t <= m; ++t) {
            if (min_x[t] > min_x[t-1]) min_x[t] = min_x[t-1];
        }

        int prev = N + 1; // min_x[0] = +inf
        for (int t = 1; t <= m; ++t) {
            int L = min_x[t];
            if (L < 1) L = 1;
            int R = prev - 1;
            if (R > N) R = N;
            if (L <= R) {
                diff[L] += t;
                diff[R + 1] -= t;
            }
            prev = min_x[t];
        }
    }

    // combine diff prefix + heavy_ans to produce answers
    vector<ll> ans(N + 1, 0);
    ll cur = 0;
    for (int x = 1; x <= N; ++x) {
        cur += diff[x];
        ans[x] = cur + heavy_ans[x];
    }

    // output
    for (int x = 1; x <= N; ++x) cout << ans[x] << '\n';
    return 0;
}