class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        if n == 1:
            return [0, 1]
        
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v, length in edges:
            adj[u].append((v, length))
            adj[v].append((u, length))
        
        # Precompute distances from root and build parent pointers / children structure via BFS
        # Actually, we can do DFS directly, but we need to avoid going back to parent.
        # We'll use iterative DFS or recursive DFS with parent tracking.
        
        # dist[i] = distance from root to node i
        dist = [0] * n
        # depth[i] = depth of node i (root at depth 0)
        depth = [0] * n
        
        # We'll use a stack for DFS: (node, parent, current_dist, current_depth)
        # But we also need to maintain the path values for uniqueness check.
        # Instead, we'll use recursive DFS with backtracking on a dictionary.
        
        last_occurrence = {}  # value -> depth index in the current path
        path_nodes = []       # list of nodes on the current path from root to current
        
        # We'll store the best result globally
        max_len = 0
        min_nodes = 1  # at least one node (the node itself)
        
        # To avoid recursion depth issues, we can use iterative DFS with explicit stack.
        # Stack elements: (node, parent, dist_from_root, depth_in_tree, entering)
        # But managing the last_occurrence and path_nodes with iterative DFS is tricky.
        # Given n <= 5e4, recursion should be fine in Python if we increase recursion limit.
        
        import sys
        sys.setrecursionlimit(100000)
        
        def dfs(node, parent, d, depth_idx):
            nonlocal max_len, min_nodes
            
            val = nums[node]
            prev_occ = last_occurrence.get(val, -1)
            
            # The earliest valid start depth for a special path ending at this node
            start_depth = prev_occ + 1
            if start_depth < 0:
                start_depth = 0
            
            # The node at start_depth is the start of the longest special path ending at node
            # We have path_nodes list, so the node at start_depth is path_nodes[start_depth]
            start_node = path_nodes[start_depth]
            
            path_len = d - dist[start_node]
            num_nodes = depth_idx - start_depth + 1
            
            if path_len > max_len:
                max_len = path_len
                min_nodes = num_nodes
            elif path_len == max_len:
                if num_nodes < min_nodes:
                    min_nodes = num_nodes
            
            # Update last_occurrence for current value
            last_occurrence[val] = depth_idx
            path_nodes.append(node)
            
            for neighbor, length in adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node, d + length, depth_idx + 1)
            
            # Backtrack: remove current node from path and restore last_occurrence
            path_nodes.pop()
            if prev_occ == -1:
                if val in last_occurrence:
                    del last_occurrence[val]
            else:
                last_occurrence[val] = prev_occ
        
        dfs(0, -1, 0, 0)
        
        return [max_len, min_nodes]