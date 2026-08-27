from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        # Build adjacency list: node -> list of (neighbor, weight)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        # Global variables to store the result
        max_len = 0
        min_nodes = 1
        
        # Dictionary to store the cumulative length and node count of the last occurrence of each value
        # Key: value, Value: (cumulative_len_from_root, cumulative_nodes_from_root)
        last_pos = {}
        
        def dfs(u: int, parent: int, current_len: int, current_nodes: int, cut_len: int, cut_nodes: int):
            nonlocal max_len, min_nodes
            val = nums[u]
            
            # Determine the new cut point for the valid special path ending at u
            # If val has been seen before on the current path, the valid path must start 
            # immediately after the previous occurrence of val.
            if val in last_pos:
                prev_len, prev_nodes = last_pos[val]
                new_cut_len = prev_len
                new_cut_nodes = prev_nodes
            else:
                # If val is unique in the current path, the valid path can extend from the previous cut point
                new_cut_len = cut_len
                new_cut_nodes = cut_nodes
            
            # Update last_pos for the current node
            # We store the cumulative stats up to the current node
            last_pos[val] = (current_len, current_nodes)
            
            # Calculate the length and number of nodes of the valid special path ending at u
            # This path starts after the 'cut' point and ends at u
            path_len = current_len - new_cut_len
            path_nodes = current_nodes - new_cut_nodes
            
            # Update global maximums
            if path_len > max_len:
                max_len = path_len
                min_nodes = path_nodes
            elif path_len == max_len:
                if path_nodes < min_nodes:
                    min_nodes = path_nodes
            
            # Recurse for children
            for v, w in adj[u]:
                if v != parent:
                    next_current_len = current_len + w
                    next_current_nodes = current_nodes + 1
                    dfs(v, u, next_current_len, next_current_nodes, new_cut_len, new_cut_nodes)
            
            # Backtrack: Remove the current node's value from last_pos
            # This ensures that when we return to the parent and go to another branch,
            # the 'last_pos' reflects only the path from root to the parent.
            del last_pos[val]
            
        # Initial call from root (node 0)
        # current_len=0, current_nodes=1
        # cut_len=0, cut_nodes=0 (representing the virtual node before the start of the path)
        dfs(0, -1, 0, 1, 0, 0)
        
        return [max_len, min_nodes]