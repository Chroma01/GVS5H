import sys
from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        sys.setrecursionlimit(2 * 10**5 + 10)
        n = len(nums)

        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        # path[d] = node id at depth d on current root-to-node path
        # pref[d] = weighted distance from root to depth d
        path = [0] * n
        pref = [0] * n

        last_depth = {}  # value -> deepest depth index on current path

        best_len = 0
        best_nodes = 1

        # Process root (depth 0)
        v0 = nums[0]
        prev0 = last_depth.get(v0, -1)
        last_depth[v0] = 0
        path[0] = 0
        pref[0] = 0
        # Root candidate: length 0, nodes 1 (already initial best)

        start = 0  # current window top depth

        # Stack tuple: (node, depth, child_iter_index, prev_last_depth, start_after_entry)
        stack = [(0, 0, 0, prev0, start)]

        while stack:
            node, depth, ci, prev_ld, start_entry = stack[-1]

            if ci < len(adj[node]):
                stack[-1] = (node, depth, ci + 1, prev_ld, start_entry)
                nxt, w = adj[node][ci]
                if depth > 0 and nxt == path[depth - 1]:
                    continue  # skip parent

                nd = depth + 1
                path[nd] = nxt
                pref[nd] = pref[depth] + w

                val = nums[nxt]
                prev = last_depth.get(val, -1)
                new_start = start if start > prev + 1 else prev + 1
                last_depth[val] = nd
                start = new_start

                # Candidate special path: depth 'start' -> 'nd'
                cand_len = pref[nd] - pref[start]
                cand_nodes = nd - start + 1
                if cand_len > best_len or (cand_len == best_len and cand_nodes < best_nodes):
                    best_len = cand_len
                    best_nodes = cand_nodes

                stack.append((nxt, nd, 0, prev, new_start))
            else:
                # Pop: restore last_depth for this node's value
                val = nums[node]
                if prev_ld == -1:
                    del last_depth[val]
                else:
                    last_depth[val] = prev_ld
                stack.pop()
                if stack:
                    start = stack[-1][4]
                else:
                    start = 0

        return [best_len, best_nodes]