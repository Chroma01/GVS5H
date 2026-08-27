import sys
from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        # Iterative DFS from root 0.
        # dist_stack[i] = distance from root to the node at depth i (depth = edge count).
        dist_stack = [0]
        last = {}   # value -> depth index of its last occurrence on the current path
        left = 0    # shallowest depth index allowed as the start of a valid window

        best_len = 0
        best_nodes = 1

        # Stack frame: [node, parent, child_index, saved_left, saved_prev_occurrence]
        stack = [[0, -1, 0, None, None]]

        while stack:
            frame = stack[-1]
            node, parent, idx, saved_left, saved_last = frame

            if idx == 0 and saved_left is None:
                # First visit to this node: process it.
                v = nums[node]
                d = len(dist_stack) - 1
                prev = last.get(v, -1)
                frame[3] = left
                frame[4] = prev
                if prev >= left:
                    left = prev + 1
                last[v] = d
                # Longest special path ending here starts at depth `left`.
                cur_len = dist_stack[d] - dist_stack[left]
                cur_nodes = d - left + 1
                if cur_len > best_len or (cur_len == best_len and cur_nodes < best_nodes):
                    best_len = cur_len
                    best_nodes = cur_nodes

            if idx < len(adj[node]):
                frame[2] += 1
                nxt, w = adj[node][idx]
                if nxt == parent:
                    continue
                dist_stack.append(dist_stack[-1] + w)
                stack.append([nxt, node, 0, None, None])
            else:
                # Backtrack: restore state so siblings see the parent's window.
                v = nums[node]
                prev = frame[4]
                if prev == -1:
                    del last[v]
                else:
                    last[v] = prev
                left = frame[3]
                dist_stack.pop()
                stack.pop()

        return [best_len, best_nodes]