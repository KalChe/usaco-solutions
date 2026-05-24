import sys
sys.setrecursionlimit(1000000)
def main():
    s = sys.stdin.read().split()
    if not s:
        return
        
    cur = 0
    t = int(s[cur])
    cur += 1
    
    out = []
    
    for i in range(t):
        n = int(s[cur])
        cur += 1
        m = int(s[cur])
        cur += 1
        
        adj = [[] for i in range(n + 1)]
        
        for i in range(m):
            u = int(s[cur])
            v = int(s[cur+1])
            c = s[cur+2]
            cur += 3
            
            adj[u].append((v, c))
            adj[v].append((u, c))
            
        min_char = ['{'] * (n + 1)
        
        for i in range(n + 1):
            if adj[i]:
                best = '{'
                for dummy, ch in adj[i]:
                    if ch < best:
                         best = ch
                min_char[i] = best
        
        dist = [-1] * (n + 1)
        dist[1] = 0
        
        q = [1]
        step = 1
        
        while q:
            best = '{'
            for u in q:
                 val = min_char[u]
                 if val < best:
                     best = val
                     
            if best == '{':
                break
                
            nxt = []
            for u in q:
                if min_char[u] == best:
                    for v, ch in adj[u]:
                        if ch == best:
                            if dist[v] == -1:
                                dist[v] = step
                                nxt.append(v)
                                
            q = nxt
            step += 1
            
        case_out = []
        for i in range(1, n + 1):
            case_out.append(str(dist[i]))
            
        out.append(" ".join(case_out))
        
    print('\n'.join(out))

if __name__ == '__main__':
    main()
