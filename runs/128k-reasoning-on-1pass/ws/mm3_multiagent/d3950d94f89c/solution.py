import sys
from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        """
        Returns [maximum length, minimum number of nodes] among all special
        downward paths in the tree rooted at 0.
        """
        n = len(nums)
        # ---------- build adjacency list ----------
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        sys.setrecursionlimit(200000)          # safe for n = 5·10^4

        # ---------- data structures ----------
        depth_dist = [0] * n          # distance from root to the node at a given depth
        last_pos = {}                 # value -> most recent depth on current path
        start_depth = 0               # left border of the current distinct‑value window

        best_len = -1
        best_cnt = n + 1

        # ---------- depth‑first search ----------
        def dfs(v: int, parent: int, cur_dist: int, cur_depth: int) -> None:
            nonlocal best_len, best_cnt, start_depth

            val = nums[v]

            # ----- handle duplicate (if any) -----
            prev_depth = last_pos.get(val, -1)          # -1 → not seen before
            old_start = start_depth
            if prev_depth != -1:
                # window must start after the previous occurrence
                if prev_depth + 1 > start_depth:
                    start_depth = prev_depth + 1

            # ----- insert current node -----
            last_pos[val] = cur_depth
            depth_dist[cur_depth] = cur_dist

            # ----- candidate best path ending here -----
            cand_len = cur_dist - depth_dist[start_depth]
            cand_cnt = cur_depth - start_depth + 1
            if cand_len > best_len or (cand_len == best_len and cand_cnt < best_cnt):
                best_len = cand_len
                best_cnt = cand_cnt

            # ----- recurse to children -----
            for to, w in adj[v]:
                if to == parent:
                    continue
                dfs(to, v, cur_dist + w, cur_depth + 1)

            # ----- backtrack : restore previous state -----
            start_depth = old_start
            if prev_depth == -1:
                del last_pos[val]
            else:
                last_pos[val] = prev_depth

        # start from the root
        dfs(0, -1, 0, 0)

        return [best_len, best_cnt]