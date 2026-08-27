class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v, length in edges:
            adj[u].append((v, length))
            adj[v].append((u, length))
        
        # Build tree structure (parent-child) and compute depth (distance from root)
        # We'll use BFS to establish parent-child relationships and compute distances
        parent = [-1] * n
        dist_from_root = [0] * n
        children = [[] for _ in range(n)]  # children[i] contains list of (child, edge_length)
        
        visited = [False] * n
        visited[0] = True
        queue = [0]
        
        # BFS to build tree structure
        while queue:
            node = queue.pop(0)
            for neighbor, length in adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    parent[neighbor] = node
                    dist_from_root[neighbor] = dist_from_root[node] + length
                    children[node].append((neighbor, length))
                    queue.append(neighbor)
        
        # Now do DFS to find longest special path
        # We maintain a dictionary: value -> index in the current path (where index is the depth in terms of node count from root)
        # Actually, we can use a dictionary: value -> the depth (distance from root) of the node with that value in the current path
        # But we need to know the start node's distance to compute path length.
        # Better: maintain a list of nodes in the current path, and a dict: value -> index in the list (0-indexed)
        
        path_nodes = []  # list of node indices in current root-to-node path
        val_to_index = {}  # maps value to index in path_nodes
        
        max_len = 0
        min_nodes = 1  # at least one node (the path of length 0)
        
        def dfs(node):
            nonlocal max_len, min_nodes
            
            val = nums[node]
            # Determine the start index for the special path ending at this node
            if val in val_to_index:
                start_index = val_to_index[val] + 1
            else:
                start_index = 0
            
            # Add current node to path
            idx = len(path_nodes)
            path_nodes.append(node)
            val_to_index[val] = idx
            
            # Calculate the length of the special path ending at this node
            # The special path starts at path_nodes[start_index] and ends at node
            start_node = path_nodes[start_index]
            path_length = dist_from_root[node] - dist_from_root[start_node]
            num_nodes = idx - start_index + 1
            
            # Update global result
            if path_length > max_len:
                max_len = path_length
                min_nodes = num_nodes
            elif path_length == max_len:
                if num_nodes < min_nodes:
                    min_nodes = num_nodes
            
            # Recurse on children
            for child, _ in children[node]:
                dfs(child)
            
            # Backtrack
            path_nodes.pop()
            del val_to_index[val]
        
        dfs(0)
        
        return [max_len, min_nodes]