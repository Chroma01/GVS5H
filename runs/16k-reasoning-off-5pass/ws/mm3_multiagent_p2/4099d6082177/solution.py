import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    total = N * K
    adj = [[] for _ in range(total + 1)]
    for _ in range(total - 1):
        u = int(next(it)); v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    # Quick reject: number of leaves must be exactly 2N.
    deg = [0] * (total + 1)
    for i in range(1, total + 1):
        deg[i] = len(adj[i])
    leaf_cnt = sum(1 for i in range(1, total + 1) if deg[i] == 1)
    if leaf_cnt != 2 * N:
        print("No")
        return

    # Special case K == 1: any tree works.
    if K == 1:
        print("Yes")
        return

    # Root the tree at vertex 1, compute parent and depth.
    parent = [0] * (total + 1)
    depth = [0] * (total + 1)
    visited = [False] * (total + 1)
    q = deque([1])
    visited[1] = True
    while q:
        u = q.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                depth[v] = depth[u] + 1
                q.append(v)

    # Leaf-stripping with distance counter.
    # cnt[v] = distance from v to the nearest leaf in its subtree that is still alive.
    # When a leaf is processed, it propagates cnt+1 to its parent.
    # When a vertex receives cnt == K-1, it can be paired with the leaf.
    removed = [False] * (total + 1)
    leaf_queue = deque()
    for i in range(1, total + 1):
        if deg[i] == 1:
            leaf_queue.append(i)

    cnt = [0] * (total + 1)

    processed = 0
    success = True

    while processed < N and success:
        # Find a still-present leaf.
        leaf = None
        while leaf_queue:
            cand = leaf_queue.popleft()
            if not removed[cand]:
                leaf = cand
                break
        if leaf is None:
            success = False
            break

        # Walk up K-1 steps from the leaf, collecting the path.
        path = []
        cur = leaf
        ok = True
        for step in range(K):
            if removed[cur]:
                ok = False
                break
            path.append(cur)
            # Update counter for the current vertex.
            if cnt[cur] == 0:
                cnt[cur] = 0  # leaf has distance 0 to itself
            # Propagate to parent (unless we are at the last step).
            if step == K - 1:
                # This is the K-th vertex; we stop climbing.
                # Its distance to the leaf is K-1, so cnt should be K-1.
                # We don't need to propagate further.
                break
            p = parent[cur]
            if p == 0:
                # No more ancestors before reaching length K-1.
                ok = False
                break
            if removed[p]:
                ok = False
                break
            # Propagate distance to parent.
            if cnt[p] == 0:
                cnt[p] = cnt[cur] + 1
            cur = p

        if not ok:
            success = False
            break

        if len(path) != K:
            success = False
            break

        # Verify that the collected vertices indeed form a path of length K-1.
        # The parent chain is correct because we only moved up the tree.
        # So they are consecutive in the tree.
        # Remove the path and update degrees.
        for v in path:
            removed[v] = True
            for w in adj[v]:
                if not removed[w]:
                    deg[w] -= 1
                    if deg[w] == 1:
                        leaf_queue.append(w)

        processed += 1

    if not success:
        print("No")
    else:
        # Ensure all vertices are removed.
        if all(removed[1:]):
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    solve()