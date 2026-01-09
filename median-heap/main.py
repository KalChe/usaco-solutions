import sys

sys.setrecursionlimit(300000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    A = [0] * N
    C = [0] * N
    
    for i in range(N):
        A[i] = int(next(iterator))
        C[i] = int(next(iterator))
        
    try:
        Q_val = int(next(iterator))
    except StopIteration:
        Q_val = 0
        
    queries = []
    for i in range(Q_val):
        val = int(next(iterator))
        queries.append((val, i))
        
    queries.sort(key=lambda x: x[0])
    
    nodes_by_val = sorted([(A[i], i) for i in range(N)])
    
    ans = [0] * Q_val
    half_N = N // 2
    
    dp = [0] * N
    state = [0] * N
    
    def update(u):
        curr = u
        while True:
            if curr >= half_N:
                dp[curr] = 0 if state[curr] else C[curr]
            else:
                left = (curr << 1) + 1
                right = left + 1
                
                vL = dp[left]
                vR = dp[right]
                
                cost_flip = 0 if state[curr] else C[curr]
                                
                sum_v = vL + vR
                min_v = vL if vL < vR else vR
                
                res = cost_flip + min_v
                if sum_v < res:
                    res = sum_v
                dp[curr] = res
            
            if curr == 0:
                break
            curr = (curr - 1) >> 1
    
    state = [1] * N
    dp = [0] * N 
    
    node_ptr = 0

    for m, qI in queries:
        while node_ptr < N:
            val, u = nodes_by_val[node_ptr]
            if val < m:
                state[u] = 0
                update(u)
                node_ptr += 1
            else:
                break
        ans[qI] += dp[0]

    state = [0] * N
    
    for i in range(N - 1, -1, -1):
        if i >= half_N:
            dp[i] = C[i]
        else:
            left = (i << 1) + 1
            right = left + 1
            vL = dp[left]
            vR = dp[right]
            
            cost_flip = C[i] 

            sum_v = vL + vR
            min_v = vL if vL < vR else vR
            
            res = cost_flip + min_v
            if sum_v < res:
                res = sum_v
            dp[i] = res
            
    node_ptr = 0

    for m, qI in queries:
        while node_ptr < N:
            val, u = nodes_by_val[node_ptr]
            if val <= m:
                state[u] = 1
                update(u)
                node_ptr += 1
            else:
                break
        ans[qI] += dp[0]

    print('\n'.join(map(str, ans)))

if __name__ == '__main__':
    solve()