from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        # Iterative DFS to avoid recursion depth issues
        # Stack contains (node, parent, dist_from_root)
        # dist == -1 indicates leaving the node
        path_vals = []          # values along current root-to-node path
        path_dist = [0]         # cumulative distance from root for each node in path
        last_occurrence = {}    # value -> index in path_vals of most recent occurrence
        start = 0               # start index of current valid window
        
        max_len = 0
        min_nodes = 1
        
        # Use explicit stack for DFS
        stack = [(0, -1, 0)]    # (node, parent, dist_from_root)
        
        while stack:
            u, parent, dist = stack.pop()
            
            if dist == -1:  # leaving node
                # Pop from path
                if path_vals:
                    path_vals.pop()
                    path_dist.pop()
                continue
            
            # Entering node
            v = nums[u]
            
            # Check for duplicate in current window
            if v in last_occurrence and last_occurrence[v] >= start:
                start = last_occurrence[v] + 1
            
            # Add to path
            path_vals.append(v)
            path_dist.append(dist)
            last_occurrence[v] = len(path_vals) - 1
            
            # Compute current path length and node count
            # Window is [start, len(path_vals)-1]
            curr_len = path_dist[-1] - path_dist[start]
            curr_nodes = len(path_vals) - start
            
            if curr_len > max_len:
                max_len = curr_len
                min_nodes = curr_nodes
            elif curr_len == max_len:
                if curr_nodes < min_nodes:
                    min_nodes = curr_nodes
            
            # Push leaving marker
            stack.append((u, parent, -1))
            
            # Push children
            for neighbor, w in adj[u]:
                if neighbor != parent:
                    stack.append((neighbor, u, dist + w))
        
        return [max_len, min_nodes]