import sys
from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        # Iterative DFS rooted at 0.
        # path[d] = node at depth d on current root-to-node path.
        path = []
        dist = [0] * n          # distance from root
        last = {}               # value -> deepest depth where seen on current path
        start_depth = 0         # depth of top of current unique-value window
        saved_stack = []        # parallel stack: (saved_start, prev_depth, value) per entered node

        best_len = 0
        best_nodes = 1

        # Stack frames: (node, parent, edge_weight_from_parent, entered)
        stack = [(0, -1, 0, False)]
        while stack:
            node, parent, w, entered = stack.pop()
            if not entered:
                # ---- Enter node ----
                depth = len(path)
                if depth > 0:
                    dist[node] = dist[parent] + w
                else:
                    dist[node] = 0

                v = nums[node]
                prev_depth = last.get(v, -1)
                saved_start = start_depth
                if prev_depth >= start_depth:
                    start_depth = prev_depth + 1

                path.append(node)
                last[v] = depth

                # Candidate: best special path ending at `node`
                cur_len = dist[node] - dist[path[start_depth]]
                cur_nodes = depth - start_depth + 1
                if cur_len > best_len or (cur_len == best_len and cur_nodes < best_nodes):
                    best_len = cur_len
                    best_nodes = cur_nodes

                # Push exit frame, then children enter frames
                stack.append((node, parent, w, True))
                saved_stack.append((saved_start, prev_depth, v))
                for child, cw in adj[node]:
                    if child != parent:
                        stack.append((child, node, cw, False))
            else:
                # ---- Exit node ----
                saved_start, prev_depth, v = saved_stack.pop()
                path.pop()
                if prev_depth == -1:
                    del last[v]
                else:
                    last[v] = prev_depth
                start_depth = saved_start

        return [best_len, best_nodes]