import sys

sys.setrecursionlimit(300000)

class DSU:
    __slots__ = ['parent', 'size', 'cnt']
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.cnt = [0] * n

    def find(self, i):
        root = i
        while root != self.parent[root]:
            root = self.parent[root]
        
        curr = i
        while curr != root:
            nxt = self.parent[curr]
            self.parent[curr] = root
            curr = nxt
        return root

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        
        added_pairs = 0
        
        if root_i != root_j:
            added_pairs = self.cnt[root_i] * self.cnt[root_j]
            if self.size[root_i] < self.size[root_j]:
                self.parent[root_i] = root_j
                self.size[root_j] += self.size[root_i]
                self.cnt[root_j] += self.cnt[root_i]
            else:
                self.parent[root_j] = root_i
                self.size[root_i] += self.size[root_j]
                self.cnt[root_i] += self.cnt[root_j]
                
        return added_pairs

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        s_str = next(iterator)
    except StopIteration:
        return

    s = [int(c) for c in s_str]
    
    adj = [[] for i in range(N)]
    for i in range(M):
        u = int(next(iterator)) - 1
        v = int(next(iterator)) - 1
        adj[u].append(v)
        adj[v].append(u)

    dsu = DSU(N)
    
    is_active = [False] * N
    for i in range(N):
        if s[i] == 1:
            is_active[i] = True
            
    for u in range(N):
        if s[u] == 1:
            for v in adj[u]:
                if v > u and s[v] == 1:
                    dsu.union(u, v)
    
    results = []
    total_pairs = 0
    
    for t in range(N - 1, -1, -1):
        root_t = dsu.find(t)
        total_pairs += dsu.cnt[root_t]
        dsu.cnt[root_t] += 1
        
        if s[t] == 0:
            is_active[t] = True
            for v in adj[t]:
                if is_active[v]:
                    total_pairs += dsu.union(t, v)
        
        results.append(total_pairs)
        
    sys.stdout.write('\n'.join(map(str, reversed(results))) + '\n')

if __name__ == '__main__':
    solve()