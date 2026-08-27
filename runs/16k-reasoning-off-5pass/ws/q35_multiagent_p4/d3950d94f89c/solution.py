class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        # Global variables to track result
        max_len = 0
        min_nodes = 1
        
        # Path from root to current node
        path = []
        # Cumulative distance from root to each node in path
        cum_dist = []
        # Dictionary to store the last seen index (in path) for each value
        last_pos = {}
        
        def dfs(u: int, parent: int, depth: int, current_dist: int):
            nonlocal max_len, min_nodes
            
            val = nums[u]
            
            # Get the previous last position of this value, or -1 if not seen
            prev_last_pos = last_pos.get(val, -1)
            
            # The valid start index for a special path ending at u is prev_last_pos + 1
            start_index = prev_last_pos + 1
            
            # Add current node to path
            path.append(u)
            cum_dist.append(current_dist)
            
            # The number of nodes in the special path from start_index to current depth
            num_nodes = depth - start_index + 1
            # The length of the special path
            # If start_index is 0, the length is current_dist (since cum_dist[0]=0)
            # Otherwise, it's current_dist - cum_dist[start_index]
            if start_index == 0:
                path_len = current_dist
            else:
                path_len = current_dist - cum_dist[start_index]
            
            # Update global results
            if path_len > max_len:
                max_len = path_len
                min_nodes = num_nodes
            elif path_len == max_len:
                if num_nodes < min_nodes:
                    min_nodes = num_nodes
            
            # Update last_pos for this value
            last_pos[val] = depth
            
            # Recurse to children
            for v, w in adj[u]:
                if v != parent:
                    dfs(v, u, depth + 1, current_dist + w)
            
            # Backtrack
            path.pop()
            cum_dist.pop()
            if prev_last_pos == -1:
                del last_pos[val]
            else:
                last_pos[val] = prev_last_pos
        
        # Start DFS from root (node 0)
        dfs(0, -1, 0, 0)
        
        return [max_len, min_nodes]