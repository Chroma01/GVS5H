class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        # We'll do a DFS from root 0
        # We need to track:
        # - path: list of nodes from root to current
        # - last_seen: dict mapping value -> index in path (depth)
        # - dist_from_root: cumulative distance from root to current node
        # - global_max_len and global_min_nodes
        
        self.global_max_len = 0
        self.global_min_nodes = 1  # At least one node (the node itself)
        
        # For DFS, we need to avoid going back to parent
        # We can use a visited array or pass parent in recursion
        
        # last_seen will store the depth (index in path) of the last occurrence of each value
        last_seen = {}
        path = []  # list of nodes on current path from root
        
        # We'll compute dist_from_root as we go
        # dist_from_root[u] is not needed globally, just pass in recursion
        
        def dfs(u: int, parent: int, depth: int, cum_dist: int):
            val = nums[u]
            # Save previous occurrence of val
            prev_idx = last_seen.get(val, -1)
            # Update last_seen for val to current depth
            last_seen[val] = depth
            path.append(u)
            
            # Determine the start of the special path ending at u
            if prev_idx == -1:
                # No duplicate on the path, path starts at root
                path_len = cum_dist
                node_count = depth + 1
            else:
                # Path starts at the child of the duplicate ancestor
                # The duplicate ancestor is at path[prev_idx]
                # The start node is at path[prev_idx + 1]
                start_node = path[prev_idx + 1]
                # We need cum_dist to start_node
                # But we don't have it stored. Instead, we can compute:
                # The length of the path from root to start_node is cum_dist - (edge weight from start_node to u and beyond)? 
                # Actually, we can store cum_dist for each node in the path? 
                # Alternatively, we can store an array dist_path where dist_path[i] is the cumulative distance to path[i]
                # Let's maintain a separate list for cumulative distances along the path.
                pass
            
            # Actually, let's maintain a list cum_dists where cum_dists[i] is the cumulative distance to path[i]
            # But we are appending to path, so we can append to cum_dists too.
            # We'll pass cum_dists as well? Or just maintain it globally and pop on backtrack.
            
            # Let's restructure: maintain cum_dists list
            # But since we are in recursion, we can append and pop.
            
            # Instead, let's compute the length differently:
            # The length of the special path ending at u is:
            #   if prev_idx == -1: cum_dist
            #   else: cum_dist - cum_dist_to_start_node
            # We need cum_dist_to_start_node. 
            # We can store a list path_cum_dist where path_cum_dist[i] = cum_dist to path[i]
            
            # We'll pass path_cum_dist as a list that we append and pop.
            
            # But to avoid passing large lists, we can just append to a global list and pop.
            
            # Let's define path_cum_dist outside and append/pop in dfs.
            
            # For now, let's assume we have path_cum_dist maintained.
            
            # Update global results
            # We'll handle this after computing path_len and node_count
            
            # Recurse to children
            for v, w in adj[u]:
                if v != parent:
                    dfs(v, u, depth + 1, cum_dist + w)
            
            # Backtrack
            path.pop()
            last_seen[val] = prev_idx  # Restore previous state

        # We need to maintain path_cum_dist as well
        path_cum_dist = []
        
        # Redefine dfs to use path_cum_dist
        def dfs2(u: int, parent: int, depth: int, cum_dist: int):
            val = nums[u]
            prev_idx = last_seen.get(val, -1)
            last_seen[val] = depth
            path.append(u)
            path_cum_dist.append(cum_dist)
            
            if prev_idx == -1:
                path_len = cum_dist
                node_count = depth + 1
            else:
                # Start node is at path[prev_idx + 1]
                # Its cumulative distance is path_cum_dist[prev_idx + 1]
                start_cum_dist = path_cum_dist[prev_idx + 1]
                path_len = cum_dist - start_cum_dist
                node_count = depth - prev_idx  # because from prev_idx+1 to depth, inclusive, is (depth - (prev_idx+1) + 1) = depth - prev_idx
            
            # Update global results
            if path_len > self.global_max_len:
                self.global_max_len = path_len
                self.global_min_nodes = node_count
            elif path_len == self.global_max_len:
                if node_count < self.global_min_nodes:
                    self.global_min_nodes = node_count
            
            for v, w in adj[u]:
                if v != parent:
                    dfs2(v, u, depth + 1, cum_dist + w)
            
            path.pop()
            path_cum_dist.pop()
            last_seen[val] = prev_idx

        dfs2(0, -1, 0, 0)
        
        return [self.global_max_len, self.global_min_nodes]