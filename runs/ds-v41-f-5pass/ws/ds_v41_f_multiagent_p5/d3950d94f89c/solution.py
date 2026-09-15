from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        best_len = 0
        best_cnt = 1

        last = {}                      # value -> depth of most recent occurrence on current root-to-node path
        d_at_depth = [0] * (n + 1)     # depth -> prefix distance from root

        # frame: (node, parent, Lp, dist, depth, phase, old)
        # phase 0 = enter, phase 1 = exit;  old = previous last value for this node's value
        stack = [(0, -1, 0, 0, 0, 0, -1)]
        while stack:
            node, parent, Lp, d, depth, phase, old = stack.pop()
            if phase == 0:
                val = nums[node]
                old = last.get(val, -1)
                L = Lp if Lp > old + 1 else old + 1
                d_at_depth[depth] = d
                length = d - d_at_depth[L]
                cnt = depth - L + 1
                if length > best_len or (length == best_len and cnt < best_cnt):
                    best_len = length
                    best_cnt = cnt
                last[val] = depth
                stack.append((node, parent, L, d, depth, 1, old))
                for nb, w in adj[node]:
                    if nb != parent:
                        stack.append((nb, node, L, d + w, depth + 1, 0, -1))
            else:
                val = nums[node]
                if old == -1:
                    del last[val]
                else:
                    last[val] = old

        return [best_len, best_cnt]