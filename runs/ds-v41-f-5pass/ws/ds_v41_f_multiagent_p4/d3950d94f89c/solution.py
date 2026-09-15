from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        # last[value] = deepest depth on the current root-to-node path where value occurs
        last = {}
        # dist_at_depth[d] = distance from root to the node currently at depth d
        dist_at_depth = [0] * (n + 1)

        best_len = 0
        best_nodes = 1  # single-node path is always valid

        # stack frames: (node, parent, depth, dist, bound, type, saved_old)
        # type 0 = enter, type 1 = exit (restore)
        stack = [(0, -1, 0, 0, 0, 0, -1)]
        while stack:
            v, parent, depth, dist, bound, typ, old = stack.pop()

            if typ == 1:
                # restore previous occurrence depth of nums[v]
                last[nums[v]] = old
                continue

            x = nums[v]
            prev = last.get(x, -1)
            new_bound = bound
            if prev != -1 and prev + 1 > new_bound:
                new_bound = prev + 1

            # schedule restoration AFTER all descendants are processed
            stack.append((v, 0, 0, 0, 0, 1, prev))
            last[x] = depth
            dist_at_depth[depth] = dist

            cand_len = dist - dist_at_depth[new_bound]
            cand_nodes = depth - new_bound + 1
            if cand_len > best_len or (cand_len == best_len and cand_nodes < best_nodes):
                best_len = cand_len
                best_nodes = cand_nodes

            nd = depth + 1
            for to, w in adj[v]:
                if to != parent:
                    stack.append((to, v, nd, dist + w, new_bound, 0, -1))

        return [best_len, best_nodes]