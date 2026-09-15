import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    V = N * K
    if V == 1:
        # N == 1, K == 1: single vertex is a path of length 1
        sys.stdout.write("Yes\n")
        return

    adj = [[] for _ in range(V + 1)]
    for _ in range(V - 1):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        adj[u].append(v)
        adj[v].append(u)

    # Root the tree at 1 and get a DFS pre-order (iterative, avoids recursion limits)
    parent = [0] * (V + 1)
    order = []
    visited = bytearray(V + 1)
    stack = [1]
    visited[1] = 1
    while stack:
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if not visited[w]:
                visited[w] = 1
                parent[w] = u
                stack.append(w)

    size = [0] * (V + 1)
    feasible = [True] * (V + 1)

    # Process bottom-up: reversed pre-order guarantees children before parents
    for u in reversed(order):
        s = 1
        ac = 0            # number of "active" children (size mod K != 0, i.e. open fragments)
        ok = True
        pu = parent[u]
        for w in adj[u]:
            if w != pu:
                if not feasible[w]:
                    ok = False
                s += size[w]
                if size[w] % K:
                    ac += 1
        size[u] = s
        if not ok:
            feasible[u] = False
        elif s % K == 0:
            # subtree must be closed: v's path uses v plus at most two child fragments
            feasible[u] = (ac <= 2)
        else:
            # subtree must be open (fragment forced to length s % K): only one child can attach
            feasible[u] = (ac <= 1)

    sys.stdout.write("Yes\n" if feasible[1] else "No\n")

main()