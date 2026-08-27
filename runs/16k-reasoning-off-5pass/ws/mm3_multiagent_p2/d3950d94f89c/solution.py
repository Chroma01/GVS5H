import sys
from collections import defaultdict
from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        # Build adjacency list: adj[u] = list of (v, w)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        # dist[u] = total edge length from root (0) to u
        dist = [0] * n
        
        # value_to_idx[val] = index in stack of the last node with this value
        # stack will hold node indices on the current root->current path
        value_to_idx = {}
        stack = []  # list of node indices
        
        best_len = -1
        best_nodes = 0
        
        sys.setrecursionlimit(200000)
        
        def dfs(u, parent):
            nonlocal best_len, best_nodes
            val = nums[u]
            
            # Handle duplicate value: pop until previous occurrence is removed
            if val in value_to_idx:
                prev_idx = value_to_idx[val]
                # Pop everything after prev_idx (the previous occurrence stays)
                while len(stack) - 1 > prev_idx:
                    popped_node = stack.pop()
                    popped_val = nums[popped_node]
                    # Unconditionally delete the popped node's value from the map
                    if popped_val in value_to_idx:
                        del value_to_idx[popped_val]
            
            # Push current node onto stack
            stack.append(u)
            value_to_idx[val] = len(stack) - 1
            
            # Compute current path length and node count
            # The start of the current unique-value segment is stack[0]
            start_node = stack[0]
            curr_len = dist[u] - dist[start_node]
            curr_nodes = len(stack)
            
            # Update global answer
            if curr_len > best_len:
                best_len = curr_len
                best_nodes = curr_nodes
            elif curr_len == best_len and curr_nodes < best_nodes:
                best_nodes = curr_nodes
            
            # Recurse to children
            for v, w in adj[u]:
                if v == parent:
                    continue
                dist[v] = dist[u] + w
                dfs(v, u)
            
            # Backtrack: pop current node and remove its value from map
            stack.pop()
            if val in value_to_idx:
                del value_to_idx[val]
        
        dfs(0, -1)
        
        return [best_len, best_nodes]