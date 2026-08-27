from typing import List
from collections import defaultdict
import sys

# Increase recursion depth to handle deep trees (up to 50,000 nodes)
sys.setrecursionlimit(100000)

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        if n == 0:
            return [0, 0]
        
        # Build adjacency list for the undirected tree
        adj = defaultdict(list)
        for u, v, length in edges:
            adj[u].append((v, length))
            adj[v].append((u, length))
        
        # Build directed tree structure (parent -> children) rooted at 0
        # We use BFS to establish parent-child relationships and avoid recursion depth issues during construction
        children = defaultdict(list)
        visited = [False] * n
        queue = [0]
        visited[0] = True
        
        # Standard BFS to build the directed tree
        idx = 0
        while idx < len(queue):
            u = queue[idx]
            idx += 1
            for v, length in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    children[u].append((v, length))
                    queue.append(v)
        
        # Global variables to store results
        max_len = 0
        min_nodes = 1
        
        # State for the current path from root
        # stack_vals: values of nodes on the path from root
        # stack_lens: cumulative lengths from root to each node in stack_vals
        # stack_lens[i] corresponds to the cumulative length to reach stack_vals[i]
        stack_vals = []
        stack_lens = []
        seen_map = {}  # Maps value -> index in stack_vals
        
        def dfs(u, curr_len):
            nonlocal max_len, min_nodes
            
            val = nums[u]
            # depth is the index where the current node would be placed in stack_vals
            depth = len(stack_vals)
            
            # Check if current value exists in the path
            if val in seen_map:
                prev_idx = seen_map[val]
                # The valid special path must start immediately after the previous occurrence.
                # The path starts at node (prev_idx + 1) and ends at current node u.
                # Length = (cumulative length to u) - (cumulative length to node at prev_idx)
                special_len = curr_len - stack_lens[prev_idx]
                nodes_count = depth - prev_idx  # Number of nodes from prev_idx+1 to depth
                
                if special_len > max_len:
                    max_len = special_len
                    min_nodes = nodes_count
                elif special_len == max_len:
                    if nodes_count < min_nodes:
                        min_nodes = nodes_count
            else:
                # No duplicate found in the current path from root.
                # The path from root to current node is valid.
                special_len = curr_len
                nodes_count = depth + 1
                
                if special_len > max_len:
                    max_len = special_len
                    min_nodes = nodes_count
                elif special_len == max_len:
                    if nodes_count < min_nodes:
                        min_nodes = nodes_count
            
            # Add current node to the path stack
            stack_vals.append(val)
            stack_lens.append(curr_len)
            seen_map[val] = depth
            
            # Recurse for children
            for v, length in children[u]:
                dfs(v, curr_len + length)
            
            # Backtrack: remove current node from path
            stack_vals.pop()
            stack_lens.pop()
            # Only delete if present to avoid KeyError in case of logic errors, though logic guarantees presence
            if val in seen_map:
                del seen_map[val]
        
        # Start DFS from root (node 0) with cumulative length 0
        dfs(0, 0)
        
        return [max_len, min_nodes]