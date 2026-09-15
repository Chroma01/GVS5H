import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    n = N * K

    # K == 1: every vertex is its own path of length 1 -> always possible
    if K == 1:
        print("Yes")
        return

    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)

    # Root the tree at 1, iterative DFS to get a processing order
    parent = [0] * (n + 1)
    visited = [False] * (n + 1)
    order = []
    stack = [1]
    visited[1] = True
    parent[1] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if not visited[w]:
                visited[w] = True
                parent[w] = u
                stack.append(w)

    # Subtree sizes (bottom-up via reversed preorder)
    size = [1] * (n + 1)
    for u in reversed(order):
        if u != 1:
            size[parent[u]] += size[u]

    # Forced cut rule: edge (parent[v], v) is SELECTED iff size[v] % K != 0
    sel = [[] for _ in range(n + 1)]
    for v in range(2, n + 1):
        if size[v] % K != 0:
            p = parent[v]
            sel[v].append(p)
            sel[p].append(v)

    # Check max selected degree <= 2
    for v in range(1, n + 1):
        if len(sel[v]) > 2:
            print("No")
            return

    # Check every selected component is a path of exactly K vertices
    vis = [False] * (n + 1)
    for s in range(1, n + 1):
        if not vis[s]:
            cnt = 0
            st = [s]
            vis[s] = True
            while st:
                u = st.pop()
                cnt += 1
                for w in sel[u]:
                    if not vis[w]:
                        vis[w] = True
                        st.append(w)
            if cnt != K:
                print("No")
                return

    print("Yes")

main()