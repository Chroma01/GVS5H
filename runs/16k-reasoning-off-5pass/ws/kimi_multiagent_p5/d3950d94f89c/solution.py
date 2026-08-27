from typing import List
import sys
sys.setrecursionlimit(10**6)

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        path_dists = []  # prefix distances from root along current path
        last_occ = {}    # value -> last index in current path
        best_len = 0
        best_nodes = 1

        def dfs(node, parent, dist, left):
            nonlocal best_len, best_nodes
            
            depth = len(path_dists)
            
            # Save state for backtracking
            old_occ = last_occ.get(nums[node], -1)
            
            # Update window: if this value was seen at or after current left boundary,
            # move left boundary past that occurrence
            if old_occ >= left:
                left = old_occ + 1
            
            # Add current node to path
            path_dists.append(dist)
            last_occ[nums[node]] = depth
            
            # Calculate current valid special path ending at this node
            curr_len = dist - path_dists[left]
            curr_nodes = depth - left + 1
            
            # Update best answer
            if curr_len > best_len or (curr_len == best_len and curr_nodes < best_nodes):
                best_len = curr_len
                best_nodes = curr_nodes
            
            # Recurse to children
            for child, weight in adj[node]:
                if child != parent:
                    dfs(child, node, dist + weight, left)
            
            # Restore state
            path_dists.pop()
            if old_occ == -1:
                del last_occ[nums[node]]
            else:
                last_occ[nums[node]] = old_occ

        dfs(0, -1, 0, 0)
        return [best_len, best_nodes]