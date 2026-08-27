from typing import List
import sys

# Increase recursion depth to handle deep trees (up to 50,000 nodes)
sys.setrecursionlimit(100000)

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        # Build undirected adjacency list
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        # Build directed adjacency list (children only) using BFS starting from root 0
        children = [[] for _ in range(n)]
        queue = [0]
        visited = [False] * n
        visited[0] = True
        
        # Use a list as a queue for BFS to avoid import overhead, though pop(0) is O(k)
        # Given constraints N=5*10^4, O(N^2) worst case for queue operations is unlikely 
        # because the tree structure limits the number of times we pop from the front 
        # relative to the total edges, but for strict O(N) we can use collections.deque.
        # However, standard list pop(0) is acceptable here as the total number of queue operations is O(N).
        # To be safe and efficient, let's use a pointer or collections.deque.
        # Using collections.deque is cleaner.
        from collections import deque
        queue = deque([0])
        
        while queue:
            u = queue.popleft()
            for v, w in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    children[u].append((v, w))
                    queue.append(v)
        
        # Global variables for the result
        max_len = 0
        min_nodes = 1  # Minimum nodes for a path of length 0 is 1
        
        # last_seen_map: value -> (depth_in_edges, sum_weights_from_root)
        last_seen_map = {}
        
        def dfs(u: int, current_depth: int, current_sum: int):
            nonlocal max_len, min_nodes
            
            val = nums[u]
            
            # Check if this value has been seen before in the current path
            if val in last_seen_map:
                prev_depth, prev_sum = last_seen_map[val]
                # The unique path starts immediately after the previous occurrence
                path_len = current_sum - prev_sum
                path_nodes = current_depth - prev_depth + 1
                
                if path_len > max_len:
                    max_len = path_len
                    min_nodes = path_nodes
                elif path_len == max_len:
                    if path_nodes < min_nodes:
                        min_nodes = path_nodes
            else:
                # If not seen, the unique path can start from the root
                path_len = current_sum
                path_nodes = current_depth + 1
                
                if path_len > max_len:
                    max_len = path_len
                    min_nodes = path_nodes
                elif path_len == max_len:
                    if path_nodes < min_nodes:
                        min_nodes = path_nodes
            
            # Update last_seen for the current node
            last_seen_map[val] = (current_depth, current_sum)
            
            # Recurse to children
            for v, w in children[u]:
                dfs(v, current_depth + 1, current_sum + w)
            
            # Backtrack: remove current node from last_seen to maintain path integrity
            del last_seen_map[val]
        
        # Start DFS from root (node 0)
        # Depth 0, Sum 0
        dfs(0, 0, 0)
        
        return [max_len, min_nodes]