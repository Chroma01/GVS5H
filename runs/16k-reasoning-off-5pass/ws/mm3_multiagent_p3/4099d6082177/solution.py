import sys
from sys import setrecursionlimit

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    V = N * K
    if V == 0:
        print("No")
        return
    adj = [[] for _ in range(V + 1)]
    for _ in range(V - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    # K = 1: each path is a single vertex, trivially always Yes
    if K == 1:
        print("Yes")
        return

    # Iterative DFS to get parent and post-order
    parent = [0] * (V + 1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)
    # order is preorder; process in reverse for post-order
    up = [0] * (V + 1)
    closed = 0

    for u in reversed(order):
        # collect child remainders
        rems = []
        for v in adj[u]:
            if v == parent[u]:
                continue
            r = up[v]
            if r != 0:
                rems.append(r)
            # if r == 0, that subtree is fully closed; we don't track how many closed inside
        rems.sort()
        # greedy pair smallest with largest
        new_rems = []
        i, j = 0, len(rems) - 1
        while i < j:
            a = rems[i]
            b = rems[j]
            s = a + b + 1
            if s == K:
                closed += 1
            else:
                new_rems.append(s % K)
            i += 1
            j -= 1
        # handle leftover
        if i == j:
            a = rems[i]
            s = a + 1
            if s == K:
                closed += 1
                up[u] = 0
            else:
                up[u] = s % K
        else:
            # no leftover from pairing; need to account for node u itself
            if not new_rems:
                up[u] = 1
            else:
                # This case: when we paired everything but had nothing else?
                # Actually if all paired and no leftover, up[u] should be 0 unless node starts a path
                # But node u must be in some path. If no partial reaches u and u has no children partials,
                # u starts a new partial of size 1.
                # If new_rems is non-empty, it means after pairing we have remainders to propagate;
                # but these remainders already include the +1 for u, so we should just take the smallest?
                # Standard approach: after greedy pairing, we have at most one unpaired remainder.
                # Since we paired i<j fully, if i==j we handled it. Otherwise all paired.
                # But new_rems may have multiple entries! This happens when multiple pairs didn't close.
                # We need to re-pair new_rems? Or the algorithm should keep pairing until <=1 remainder.
                # Actually the standard algorithm continues pairing. Let's re-pair new_rems.
                # However, due to structure, after one round there can be multiple remainders.
                # We need to iteratively pair or use a different structure.
                # The correct approach: use a multiset and repeatedly pair; but with sorting it's O(n log n) per node.
                # Alternative: pair smallest+largest iteratively until <=1 remains.
                new_rems.sort()
                cur = new_rems
                while len(cur) > 1:
                    a = cur[0]
                    b = cur[-1]
                    s = a + b + 1
                    if s == K:
                        closed += 1
                    else:
                        mid = cur[1:-1]
                        cur = mid + [s % K]
                        cur.sort()
                    if len(cur) <= 1:
                        break
                if len(cur) == 1:
                    up[u] = cur[0]
                else:
                    up[u] = 0
                up[u] = up[u]  # placeholder
                # Actually this is getting complicated. Let's use a simpler approach:
                # just store all partials and re-pair until at most one.
                # But we already updated up[u] above. Let's restructure.

    # This code path above is broken. Let me rewrite cleanly below.
    print("No")  # placeholder

# Rewrite cleanly:
def solve_clean():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    V = N * K
    if V == 0:
        print("No")
        return
    adj = [[] for _ in range(V + 1)]
    for _ in range(V - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    if K == 1:
        print("Yes")
        return

    parent = [0] * (V + 1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)

    up = [0] * (V + 1)
    closed = 0

    for u in reversed(order):
        rems = []
        for v in adj[u]:
            if v == parent[u]:
                continue
            r = up[v]
            if r != 0:
                rems.append(r)
        rems.sort()
        # repeatedly pair smallest with largest until <= 1 remains
        while len(rems) > 1:
            a = rems[0]
            b = rems[-1]
            s = a + b + 1
            if s == K:
                closed += 1
            else:
                rems = rems[1:-1] + [s % K]
                rems.sort()
                continue
            rems = rems[1:-1]
        if len(rems) == 1:
            a = rems[0]
            s = a + 1
            if s == K:
                closed += 1
                up[u] = 0
            else:
                up[u] = s % K
        else:
            # no partials from children; node u starts a new partial
            up[u] = 1

    if closed == N and up[1] == 0:
        print("Yes")
    else:
        print("No")

solve_clean()