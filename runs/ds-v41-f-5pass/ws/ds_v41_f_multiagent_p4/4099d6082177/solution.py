import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    M = N * K
    adj = [[] for _ in range(M + 1)]
    for _ in range(M - 1):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        adj[u].append(v)
        adj[v].append(u)

    # root the tree at vertex 1, build iterative order
    parent = [0] * (M + 1)
    order = []
    visited = [False] * (M + 1)
    stack = [1]
    visited[1] = True
    parent[1] = -1
    while stack:
        x = stack.pop()
        order.append(x)
        for y in adj[x]:
            if not visited[y]:
                visited[y] = True
                parent[y] = x
                stack.append(y)

    # ret[x]: 0 = subtree fully closed, >0 = open path length (vertices) with x as an endpoint,
    #         -1 = impossible
    ret = [0] * (M + 1)

    for x in reversed(order):
        opens = []
        bad = False
        for y in adj[x]:
            if parent[y] == x:  # y is a child
                r = ret[y]
                if r == -1:
                    bad = True
                    break
                if r > 0:
                    opens.append(r)
        if bad:
            ret[x] = -1
            continue

        if len(opens) > 2:
            ret[x] = -1
        elif len(opens) == 2:
            # both must merge through x; merged path length must be exactly K
            if opens[0] + opens[1] + 1 == K:
                ret[x] = 0
            else:
                ret[x] = -1
        elif len(opens) == 1:
            t = opens[0] + 1
            if t > K:
                ret[x] = -1
            elif t == K:
                ret[x] = 0
            else:
                ret[x] = t
        else:
            # start a new path at x
            ret[x] = 0 if K == 1 else 1

    sys.stdout.write("Yes\n" if ret[1] == 0 else "No\n")

main()