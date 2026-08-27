import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    V = N * K
    adj = [[] for _ in range(V + 1)]
    for _ in range(V - 1):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        adj[u].append(v)
        adj[v].append(u)

    if K == 1:
        print("Yes")
        return

    # Iterative DFS from root 1 to get parent pointers and a post-order
    parent = [0] * (V + 1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:
        v = stack.pop()
        order.append(v)
        for u in adj[v]:
            if u != parent[v]:
                parent[u] = v
                stack.append(u)

    # up[v] = length (in vertices) of the single unfinished path ending at v
    # that must be extended through its parent; 0 means the subtree of v is
    # fully decomposed.
    up = [0] * (V + 1)
    ok = True
    for v in reversed(order):
        lens = [up[u] for u in adj[v] if u != parent[v] and up[u] > 0]
        lens.sort()
        survivor = 0  # length of the unique path to be extended through v
        i, j = 0, len(lens) - 1
        while i <= j:
            if i == j:
                if survivor != 0:
                    ok = False
                    break
                survivor = lens[i]
                break
            s, l = lens[i], lens[j]
            t = s + l + 1
            if t == K:
                # join the two paths through v -> one complete path
                i += 1
                j -= 1
            elif t > K:
                # l cannot pair with anything (s is minimal) -> must survive
                if survivor != 0:
                    ok = False
                    break
                survivor = l
                j -= 1
            else:
                # s cannot pair with anything (l is maximal) -> must survive
                if survivor != 0:
                    ok = False
                    break
                survivor = s
                i += 1
        if not ok:
            break
        if survivor:
            # extend the surviving path by v
            up[v] = 0 if survivor + 1 == K else survivor + 1
        else:
            # start a new path at v (K >= 2 here)
            up[v] = 1

    print("Yes" if ok and up[1] == 0 else "No")

main()