from typing import List
import sys

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        sys.setrecursionlimit(10**6)
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        # Iterative DFS from root 0
        # Frame: [node, parent, depth, dist, child_index, prev_occurrence]
        # prev_occurrence is filled in on first visit (when child_index == 0 and not yet entered)
        stack = [[0, -1, 0, 0, 0, None]]  # None = not entered yet
        path = [0] * n          # node at each depth
        dist = [0] * n          # distance from root at each depth
        last = {}               # value -> last depth seen on current path
        start_depth = 0         # current window start (inclusive)
        best_len = 0
        best_nodes = 1

        while stack:
            frame = stack[-1]
            node, parent, depth, d, idx, prev = frame

            if prev is None:
                # Entering node for the first time: adjust window
                v = nums[node]
                if v in last and last[v] >= start_depth:
                    start_depth = last[v] + 1
                # Save previous occurrence for backtrack
                frame[5] = last.get(v, -1)
                prev = frame[5]
                last[v] = depth
                path[depth] = node
                dist[depth] = d
                # Update best with path from start_depth to depth
                cur_len = dist[depth] - dist[start_depth]
                cur_nodes = depth - start_depth + 1
                if cur_len > best_len or (cur_len == best_len and cur_nodes < best_nodes):
                    best_len = cur_len
                    best_nodes = cur_nodes

            # Find next child
            if idx < len(adj[node]):
                child, w = adj[node][idx]
                frame[4] = idx + 1
                if child != parent:
                    stack.append([child, node, depth + 1, d + w, 0, None])
            else:
                # Backtrack: restore last occurrence
                v = nums[node]
                if prev == -1:
                    if v in last:
                        del last[v]
                else:
                    last[v] = prev
                stack.pop()

        return [best_len, best_nodes]