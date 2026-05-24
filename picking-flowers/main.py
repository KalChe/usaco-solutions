import sys
from collections import deque


def bfs(n, graph):
    dist = [-1] * (n + 1)
    dist[1] = 0
    deck = deque([1])
    max = 0

    while deck:
        u = deck.popleft()
        node = dist[u] + 1
        for v in graph[u]:
            if dist[v] != -1:
                continue
            dist[v] = node
            if node > max:
                max = node
            deck.append(v)

    return dist, max


def construct(n, dist, max):
    freq = [0] * (max + 1)
    for u in range(1, n + 1):
        freq[dist[u]] += 1

    begin = [0] * (max + 2)
    for d in range(max + 1):
        begin[d + 1] = begin[d] + freq[d]

    nodes = [0] * n
    at = begin[:]
    for u in range(1, n + 1):
        d = dist[u]
        nodes[at[d]] = u
        at[d] += 1

    return nodes, begin


def testcase(n, flowers, destinations, graph):
    dist, max = bfs(n, graph)
    nodes, begin = construct(n, dist, max)

    must = [0] * (max + 1)
    flwer = [0] * (n + 1)
    deepest = -1

    for flower in flowers:
        flwer[flower] = 1
        d = dist[flower]
        if must[d] != 0 and must[d] != flower:
            return "0" * (n - 1)
        must[d] = flower
        if d > deepest:
            deepest = d

    valid = [True] * (n + 1)
    valid[0] = False

    for d in range(max + 1):
        required = must[d]
        if required == 0:
            continue
        left = begin[d]
        right = begin[d + 1]
        for i in range(left, right):
            u = nodes[i]
            if u != required:
                valid[u] = False

    destination = [0] * (n + 1)
    for x in destinations:
        destination[x] = 1

    begin = [False] * (n + 1)
    for u in nodes:
        if not valid[u]:
            continue
        if u == 1:
            begin[u] = True
            continue

        d = dist[u] - 1
        ok = False
        for v in graph[u]:
            if dist[v] == d and begin[v]:
                ok = True
                break
        begin[u] = ok

    travelling = [False] * (n + 1)
    for i in range(n - 1, -1, -1):
        u = nodes[i]
        if not valid[u]:
            continue

        d = dist[u]
        ok = (d >= deepest and destination[u] == 1)
        if not ok:
            node = d + 1
            for v in graph[u]:
                if dist[v] == node and travelling[v]:
                    ok = True
                    break
        travelling[u] = ok

    base = travelling[1]
    ANSWER = []
    for i in range(2, n + 1):
        if flwer[i]:
            if base:
                ANSWER.append('1')
            else:
                ANSWER.append('0')
            continue

        d = dist[i]
        if must[d] != 0 and must[d] != i:
            ANSWER.append('0')
            continue

        if begin[i]:
            if travelling[i]:
                ANSWER.append('1')
            else:
                ANSWER.append('0')
        else:
            ANSWER.append('0')

    return ''.join(ANSWER)


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    out = []

    for i in range(t):
        n = data[idx]
        m = data[idx + 1]
        k = data[idx + 2]
        l = data[idx + 3]
        idx += 4

        flowers = data[idx:idx + k]
        idx += k
        destinations = data[idx:idx + l]
        idx += l

        graph = [[] for i in range(n + 1)]
        for i in range(m):
            u = data[idx]
            v = data[idx + 1]
            idx += 2
            graph[u].append(v)
            graph[v].append(u)

        out.append(testcase(n, flowers, destinations, graph))

    sys.stdout.write('\n'.join(out) + '\n')


solve()