class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        if n == 1:
            return [0, 1]
        
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        # We need to root the tree at 0 and establish parent-child relationships
        # to avoid going back to parent during DFS.
        # We can do a BFS/DFS to create a directed tree or just use a visited set.
        # Using a stack for DFS to build parent pointers or just use visited in main DFS.
        
        # Let's use iterative DFS for the main traversal to avoid recursion depth issues.
        # But recursion is cleaner for backtracking state. Given n=5e4, recursion limit might be hit.
        # We'll increase recursion limit.
        import sys
        sys.setrecursionlimit(100000)
        
        # last_occurrence: value -> (dist_from_root, depth) of the last node with that value on current path
        last_occurrence = {}
        
        max_len = 0
        min_nodes = 1  # At least one node (the node itself) with path length 0
        
        # We'll do a recursive DFS
        # To avoid passing too many arguments, we can use a helper
        def dfs(node, parent, dist_from_root, depth):
            nonlocal max_len, min_nodes
            
            val = nums[node]
            prev = last_occurrence.get(val)
            
            if prev is None:
                # Path starts at root
                path_len = dist_from_root
                num_nodes = depth + 1
            else:
                prev_dist, prev_depth = prev
                path_len = dist_from_root - prev_dist
                num_nodes = depth - prev_depth
            
            # Update global result
            if path_len > max_len:
                max_len = path_len
                min_nodes = num_nodes
            elif path_len == max_len:
                if num_nodes < min_nodes:
                    min_nodes = num_nodes
            
            # Save previous occurrence for backtracking
            old_prev = prev
            last_occurrence[val] = (dist_from_root, depth)
            
            # Visit children
            for neighbor, weight in adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node, dist_from_root + weight, depth + 1)
            
            # Backtrack: restore last_occurrence
            if old_prev is None:
                if val in last_occurrence:
                    del last_occurrence[val]
            else:
                last_occurrence[val] = old_prev
        
        dfs(0, -1, 0, 0)
        
        return [max_len, min_nodes]