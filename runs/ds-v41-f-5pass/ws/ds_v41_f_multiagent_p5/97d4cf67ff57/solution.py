import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]
    ptr = 1
    for _ in range(n - 1):
        a = int(data[ptr]); b = int(data[ptr + 1]); ptr += 2
        adj[a].append(b)
        adj[b].append(a)

    if n < 2:
        print(-1)
        return

    parent = [0] * (n + 1)
    order = []
    visited = [False] * (n + 1)
    dq = deque([1])
    visited[1] = True
    while dq:
        v = dq.popleft()
        order.append(v)
        for c in adj[v]:
            if not visited[c]:
                visited[c] = True
                parent[c] = v
                dq.append(c)

    B = [0] * (n + 1)
    B1 = [-1] * (n + 1)
    best = -1

    for v in reversed(order):
        base = parent[v]
        childB = []
        childB1max = -1
        for c in adj[v]:
            if c != base:
                childB.append(B[c])
                if B1[c] > childB1max:
                    childB1max = B1[c]
        k = len(childB)
        if k >= 3:
            childB.sort(reverse=True)
            B[v] = 1 + childB[0] + childB[1] + childB[2]
            B1[v] = B[v]
            if k >= 4:
                cand = B[v] + childB[3]
                if cand > best:
                    best = cand
        else:
            B[v] = 1
            B1[v] = -1
        if childB1max >= 1:
            cand = 1 + childB1max
            if cand > best:
                best = cand

    print(best if best >= 1 else -1)

main()