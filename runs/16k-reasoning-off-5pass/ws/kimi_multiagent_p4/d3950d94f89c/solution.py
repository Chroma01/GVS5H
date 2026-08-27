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

        # last occurrence depth of each value on current root-to-node path
        last = {}
        # stack of nodes on current path; path[d] is node at depth d
        path = []
        # prefix distance from root to node at each depth; pref[0] = 0 for root
        pref = [0]

        best_len = 0
        best_nodes = 1

        def dfs(u: int, parent: int, left: int) -> None:
            nonlocal best_len, best_nodes
            val = nums[u]
            prev = last.get(val, -1)
            # move left boundary past previous occurrence of this value
            new_left = left if prev < left else prev + 1
            # candidate path: from node at depth new_left to u
            length = pref[-1] - pref[new_left]
            nodes = len(path) - new_left  # depth(u)+1 - new_left
            if length > best_len or (length == best_len and nodes < best_nodes):
                best_len = length
                best_nodes = nodes

            old = last.get(val, None)
            last[val] = len(path)  # depth of u
            path.append(u)
            for v, w in adj[u]:
                if v == parent:
                    continue
                pref.append(pref[-1] + w)
                dfs(v, u, new_left)
                pref.pop()
            path.pop()
            # rollback last occurrence
            if old is None:
                del last[val]
            else:
                last[val] = old

        dfs(0, -1, 0)
        return [best_len, best_nodes]