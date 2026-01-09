import sys
input = sys.stdin.readline

def solve():
    MOD = 10**9 + 7
    
    n = int(input())
    s = list(input().strip().upper())
    
    left_b = [0] * (n + 2)
    left_r = [0] * (n + 2)
    right_b = [n + 1] * (n + 2)
    
    for i in range(1, n + 1):
        left_b[i] = i if s[i-1] == 'B' else left_b[i-1]
        left_r[i] = i if s[i-1] == 'R' else left_r[i-1]
    
    for i in range(n, 0, -1):
        right_b[i] = i if s[i-1] == 'B' else right_b[i+1]
    
    dp = [0] * (n + 1)
    psm = [[0] * (n + 1) for i in range(2)]
    dp[0] = 1
    psm[0][0] = 1
    
    def sumRange(l, r, i):
        l += (l % 2 != i % 2)
        r -= (r % 2 != i % 2)
        if l > r:
            return 0
        result = psm[i % 2][r]
        if l - 1 >= 0:
            result -= psm[i % 2][l - 1]
        return result % MOD
    
    for i in range(1, n + 1):
        # leave white if allowed
        if s[i-1] != 'R' and s[i-1] != 'B':
            dp[i] = dp[i - 1]
        
        # maximal x where right half [i-x+1, i] doesn't contain r
        cutoff_x = i - left_r[i]
        x = 1
        
        while i - 2 * x + 1 >= 1 and x <= cutoff_x:
            l_red = i - 2 * x + 1  # left bound of red part
            r_red = i - x          # right boundary of red part
            
            # checks if red part contains a b
            if right_b[l_red] and right_b[l_red] <= r_red:
                # B found in [l_red, r_red]
                # jump x to move this B to blue part
                x = i - right_b[l_red] + 1
            else:
                # no B in red part
                dp[i] = (dp[i] + sumRange(max(left_b[l_red - 1], i - 2 * cutoff_x), i - 2 * x, i)) % MOD
                # jump to next x
                x = (i - left_b[l_red - 1]) // 2 + 1
        
        # update psums
        for p in range(2):
            psm[p][i] = psm[p][i - 1]
            if p == i % 2:
                psm[p][i] = (psm[p][i] + dp[i]) % MOD
    
    print(dp[n])

solve()