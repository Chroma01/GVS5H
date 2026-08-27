import sys
from collections import defaultdict
from typing import List

# Increase recursion depth to handle deep trees (up to 50,000 nodes)
sys.setrecursionlimit(60000)

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        
        # Build adjacency list: node -> list of (neighbor, weight)
        adj = defaultdict(list)
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        # Global variables to track the best path found
        max_len = 0
        min_nodes = 1
        
        # last_pos stores: value -> (depth_of_child_of_duplicate, dist_from_root_of_child_of_duplicate)
        # This helps us quickly find where a path with unique values must restart if a duplicate is found.
        last_pos = {}
        
        # dp[u] will store (length, nodes) for the longest special path ending at u
        dp = [None] * n
        
        def dfs_w(u: int, p: int, depth: int, dist: int, last_pos: dict, w: int = 0):
            nonlocal max_len, min_nodes
            val = nums[u]
            
            # Calculate the length and number of nodes for the longest special path ending at u
            if val in last_pos:
                # If val was seen before, the path must start at the child of the previous occurrence.
                # The previous occurrence's child is defined by the stored depth and dist.
                prev_depth, prev_dist = last_pos[val]
                curr_len = dist - prev_dist
                curr_nodes = depth - prev_depth + 1
            else:
                # If val has not been seen in the current valid path segment:
                if p == -1:
                    # Root node
                    curr_len = 0
                    curr_nodes = 1
                else:
                    # Extend from parent
                    # We assume dp[p] is valid because we are traversing down and updating last_pos correctly.
                    # If the path from root to p was valid (or restarted correctly), dp[p] holds the max path ending at p.
                    curr_len = dp[p][0] + w
                    curr_nodes = dp[p][1] + 1
            
            # Update global maximums
            if curr_len > max_len:
                max_len = curr_len
                min_nodes = curr_nodes
            elif curr_len == max_len:
                if curr_nodes < min_nodes:
                    min_nodes = curr_nodes
            
            # Store result for current node
            dp[u] = (curr_len, curr_nodes)
            
            # Update last_pos for the current value to the current node's position.
            # This position represents the start of the path for any future child that has the same value.
            # We save the old value to backtrack later.
            old_val = last_pos.get(val)
            last_pos[val] = (depth, dist)
            
            # Recurse for children
            for v, w_child in adj[u]:
                if v != p:
                    dfs_w(v, u, depth + 1, dist + w_child, last_pos, w_child)
            
            # Backtrack: restore last_pos to its state before visiting u
            if old_val is None:
                del last_pos[val]
            else:
                last_pos[val] = old_val
        
        # Start DFS from root (node 0)
        dfs_w(0, -1, 0, 0, last_pos)
        
        return [max_len, min_nodes]