import sys

MOD = 1000000007

def precompute(limit):
    inverse = [1] * limit

    for value in range(2, limit):
        inverse[value] = MOD - (MOD // value) * inverse[MOD % value] % MOD

    factorial = [1] * limit
    for value in range(1, limit):
        factorial[value] = factorial[value - 1] * value % MOD

    inv_factorial = [1] * limit
    inv_factorial[limit- 1] = pow(factorial[limit - 1], MOD - 2, MOD)

    for value in range(limit -2, -1,-1):
        inv_factorial[value] = inv_factorial[value + 1] * (value + 1) % MOD
    return inverse, inv_factorial


def testcase(n, graph, inverse, inv_factorial):
    subtree = [0] * (n + 1)

    stack = [(1, 0, 0)]
    while stack:
        node, par, state = stack.pop()

        if state == 0:
            stack.append((node,par, 1))
            for v in graph[node]:
                if v == par:
                    continue
                stack.append((v, node, 0))
        else:
            total = 1
            for v in graph[node]:
                if v == par:
                    continue
                total += subtree[v]
            subtree[node] = total

    root = 1
    for node in range(1, n + 1):
        root = root * inverse[subtree[node]] % MOD

    dp = [0] * (n + 1)
    dp[1] = root
    sum = root

    stack = [(1, 0)]
    while stack:
        node, par = stack.pop()
        for v in graph[node]:
            if v == par:
                continue

            ch = subtree[v]
            dp[v] = dp[node] * ch % MOD* inverse[n - ch] % MOD
            sum += dp[v]
            if sum >= MOD:
                sum -= MOD

            stack.append((v, node))

            # 
            # for node in traversal:
            #     for v in graph[node]:
            #         if v == parent[node]:
            #             continue
            #         parent[v] = node
            #         traversal.append(v)
            # for node in traversal[1:]:
            #     par = parent[node]
            #     ch = subtree[node]
            #     dp[node] = dp[par] * ch % MOD * inverse[n - ch] % MOD

    return sum * inv_factorial[n - 1] %MOD


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    inverse, inv_factorial = precompute(200005)

    tests = data[0]
    idx = 1
    output = []

    for i in range(tests):
        n = data[idx]
        idx += 1

        graph = [[] for i in range(n + 1)]
        for i in range(n - 1):
            u = data[idx]
            v = data[idx + 1]
            idx += 2
            graph[u].append(v)
            graph[v].append(u)

        output.append(str(testcase(n, graph, inverse, inv_factorial)))

    sys.stdout.write('\n'.join(output) + '\n')

    # tests = int(input())
    # for i in range(tests):
    #     n = int(input())
    #     graph = [[] for i in range(n + 1)]
    #     for i in range(n - 1):
    #         u, v = map(int, input().split())
    #         graph[u].append(v)
    #         graph[v].append(u)
    #     print(testcase(n, graph, inverse, inv_factorial))


solve()