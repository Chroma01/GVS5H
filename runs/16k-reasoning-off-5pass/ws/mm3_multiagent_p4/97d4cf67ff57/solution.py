import sys
import sys
import threading

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        a = int(next(it)); b = int(next(it))
        adj[a].append(b)
        adj[b].append(a)

    if N < 5:
        # need at least 5 vertices for an alkane
        print(-1)
        return

    # iterative DFS to get parent and order
    parent = [0] * (N + 1)
    parent[1] = -1
    order = []
    stack = [1]
    while stack:
        v = stack.pop()
        order.append(v)
        for u in adj[v]:
            if u != parent[v]:
                parent[u] = v
                stack.append(u)

    import heapq

    # DP arrays
    # deep_up[v] = size of best upward-connected subtree where v is degree 4, -1 if impossible
    # best_up[v] = max(1, deep_up[v])  (size of best upward-connected subtree)
    deep_up = [-1] * (N + 1)
    best_up = [1] * (N + 1)

    ans = -1

    # Process nodes in reverse order (post-order)
    for v in reversed(order):
        # Collect best_up values of children
        child_vals = []
        max_deep_child = -1
        for u in adj[v]:
            if u == parent[v]:
                continue
            child_vals.append(best_up[u])
            if deep_up[u] != -1 and deep_up[u] > max_deep_child:
                max_deep_child = deep_up[u]

        # deep_up[v]: need at least 3 children
        if len(child_vals) >= 3:
            # sum of three largest best_up values
            top3 = sum(heapq.nlargest(3, child_vals))
            deep_up[v] = 1 + top3
            best_up[v] = deep_up[v]   # deep_up >= 4 > 1
        else:
            deep_up[v] = -1
            best_up[v] = 1

        # candidate when v is the root of the alkane and has degree 1
        if max_deep_child != -1:
            cand = 1 + max_deep_child
            if cand > ans:
                ans = cand

        # candidate when v is the root of the alkane and has degree 4
        if len(child_vals) >= 4:
            top4 = sum(heapq.nlargest(4, child_vals))
            cand = 1 + top4
            if cand > ans:
                ans = cand

    if ans < 0:
        print(-1)
    else:
        print(ans)

# Run the function in a separate thread to increase recursion limit if needed
threading.Thread(target=main).start()