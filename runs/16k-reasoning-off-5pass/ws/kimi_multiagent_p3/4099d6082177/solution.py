import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    M = N * K
    adj = [[] for _ in range(M + 1)]
    for _ in range(M - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    # Iterative post-order DFS rooted at vertex 1.
    parent = [0] * (M + 1)
    order = []          # visitation order (pre-order); reversed gives post-order
    stack = [1]
    parent[1] = -1
    while stack:
        x = stack.pop()
        order.append(x)
        for y in adj[x]:
            if y != parent[x]:
                parent[y] = x
                stack.append(y)

    d = [0] * (M + 1)   # dangling chain length returned by each subtree
    fail = False
    for x in reversed(order):
        a = b = 0       # the (at most two) nonzero child dangling lengths
        cnt = 0
        for y in adj[x]:
            if y == parent[x]:
                continue
            dy = d[y]
            if dy:
                cnt += 1
                if cnt == 1:
                    a = dy
                elif cnt == 2:
                    b = dy
                else:
                    fail = True
                    break
        if fail:
            break
        if cnt == 2:
            s = a + b + 1
            if s > K:
                fail = True
                break
            d[x] = s % K
        elif cnt == 1:
            d[x] = (a + 1) % K
        else:
            d[x] = 1 % K

    sys.stdout.write("Yes\n" if (not fail and d[1] == 0) else "No\n")

main()