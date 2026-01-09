### python sol
### passes all tcs except 12-16
import sys
import math
from collections import defaultdict

# greedy to count groups on a single label positions list p for given x
def groups_for_x_positions(p, x):
    m = len(p)
    cnt = 0
    i = 0
    while i < m:
        j = i
        # extend group while next element still within p[i] + x
        while j + 1 < m and p[j+1] - p[i] <= x:
            j += 1
        cnt += 1
        i = j + 1
    return cnt

def solve(a):
    N = len(a)
    pos = defaultdict(list)
    for i, v in enumerate(a, start=1):
        pos[v].append(i)

    # sqrt threshold
    z = int(math.sqrt(N)) if N > 0 else 1

    heavy = [] # lists with length > z
    light = [] # lists with length <= z

    for label, p in pos.items():
        if len(p) > z:
            heavy.append(p)
        else:
            light.append(p)

    # heavy contribution per x (1..N)
    heavy_ans = [0] * (N + 1) # index 1..N

    # build the next array and for each x count jumps
    for p in heavy:
        # build nxt: nxt[i] = first index >= i that belongs to this label, or N+1
        nxt = [N+1] * (N + 2) # 0..N+1, use 1..N
        for idx in p:
            nxt[idx] = idx
        for i in range(N, 0, -1):
            if nxt[i] == N+1:
                nxt[i] = nxt[i + 1]
        start = p[0]
        # count groups for each x
        for x in range(1, N + 1):
            cnt = 0
            i = start
            while i <= N:
                cnt += 1
                jump_to = i + x + 1
                if jump_to > N:
                    break
                i = nxt[jump_to]
                if i == N + 1:
                    break
            heavy_ans[x] += cnt

    # light labels: for each label with small m, compute min_x[t] by binary search on x
    # convert min_x[t] to ranges [L..R] where this label contributes exactly t groups,
    # accumulate in diff array.
    diff = [0] * (N + 3)  # 1..N used, safe up to N+2

    for p in light:
        m = len(p)
        if m == 0:
            continue
        if m == 1:
            diff[1] += 1
            diff[N + 1] -= 1
            continue
        max_span = p[-1] - p[0]
        min_x = [0] * (m + 1)  # index 1..m
        # for each t (number of groups) find minimal x s.t. groups_for_x_positions(p, x) <= t
        for t in range(1, m + 1):
            lo, hi = 0, max_span
            while lo < hi:
                mid = (lo + hi) // 2
                if groups_for_x_positions(p, mid) <= t:
                    hi = mid
                else:
                    lo = mid + 1
            min_x[t] = lo
        # enforce monotonicity (nonincreasing)
        for t in range(2, m + 1):
            if min_x[t] > min_x[t - 1]:
                min_x[t] = min_x[t - 1]
        prev = N + 1
        for t in range(1, m + 1):
            L = min_x[t]
            if L < 1:
                L = 1
            R = prev - 1
            if R > N:
                R = N
            if L <= R:
                diff[L] += t
                diff[R + 1] -= t
            prev = min_x[t]

    # combine light (diff prefix) + heavy into final answers
    ans = [0] * N
    cur = 0
    for x in range(1, N + 1):
        cur += diff[x]
        ans[x - 1] = cur + heavy_ans[x]
    return ans

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    a = [int(next(it)) for i in range(N)]
    res = solve(a)
    sys.stdout.write("\n".join(map(str, res)) + "\n")

if __name__ == "__main__":
    main()
