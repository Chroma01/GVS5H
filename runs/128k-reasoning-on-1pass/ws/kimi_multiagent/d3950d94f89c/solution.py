import sys
from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        sys.setrecursionlimit(200000)
        n = len(nums)

        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        INF = (float('inf'), float('inf'))

        # Iterative segment tree over depths, storing (pref, -depth) for active depths.
        size = 1
        while size < n:
            size <<= 1
        seg = [INF] * (2 * size)

        def seg_update(pos: int, val) -> None:
            i = pos + size
            seg[i] = val
            i >>= 1
            while i:
                a = seg[2 * i]
                b = seg[2 * i + 1]
                seg[i] = a if a <= b else b
                i >>= 1

        def seg_query(l: int, r: int):
            l += size
            r += size
            res = INF
            while l <= r:
                if l & 1:
                    if seg[l] < res:
                        res = seg[l]
                    l += 1
                if not (r & 1):
                    if seg[r] < res:
                        res = seg[r]
                    r -= 1
                l >>= 1
                r >>= 1
            return res

        pref = [0] * n          # weighted prefix sum per depth on current stack
        lastSeen = {}           # value -> depth on current root-to-node path
        best_len = 0
        best_nodes = 1
        L = 0                   # leftmost valid start depth for current path

        # Explicit enter/exit DFS events.
        # (node, parent, edge_weight, depth, is_exit, saved_L, saved_prev)
        stack = [(0, -1, 0, 0, False, 0, -1)]
        while stack:
            node, parent, w, depth, is_exit, saved_L, saved_prev = stack.pop()

            if is_exit:
                seg_update(depth, INF)
                x = nums[node]
                if saved_prev == -1:
                    del lastSeen[x]
                else:
                    lastSeen[x] = saved_prev
                L = saved_L
                continue

            # Enter node.
            pref[depth] = (pref[depth - 1] if depth > 0 else 0) + w
            x = nums[node]
            prev = lastSeen.get(x, -1)
            old_L = L
            if prev + 1 > L:
                L = prev + 1
            lastSeen[x] = depth
            seg_update(depth, (pref[depth], -depth))

            # Best special path ending at this node: min pref over [L, depth],
            # tie broken by largest depth (fewest nodes).
            min_pref, neg_d = seg_query(L, depth)
            length = pref[depth] - min_pref
            nodes = depth + neg_d + 1
            if length > best_len or (length == best_len and nodes < best_nodes):
                best_len = length
                best_nodes = nodes

            # Schedule exit (with rollback data), then children.
            stack.append((node, parent, w, depth, True, old_L, prev))
            for child, cw in adj[node]:
                if child != parent:
                    stack.append((child, node, cw, depth + 1, False, 0, -1))

        return [best_len, best_nodes]