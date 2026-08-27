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
        
        # We'll use DFS. We need to track:
        # - cumulative distance from root (depth_dist)
        # - depth index (depth_idx) which is 0 for root, 1 for children, etc.
        # - last_occurrence: dict mapping value -> depth_idx of last occurrence in current path
        # - We also need to know the cumulative distance at the depth_idx where a value last occurred.
        #   So we can store last_occurrence as value -> (depth_idx, cumulative_dist_at_that_idx)
        
        last_occurrence = {}  # val -> (depth_idx, cum_dist)
        
        # Global state for result
        max_len = 0
        min_nodes = 1
        
        # We'll use an iterative DFS to avoid recursion depth issues, 
        # but recursive is cleaner for backtracking. Given N=5e4, recursion limit might be hit.
        # Set recursion limit.
        import sys
        sys.setrecursionlimit(100000)
        
        # For iterative DFS with backtracking, we can use a stack that stores (node, parent, cum_dist, depth_idx)
        # But backtracking last_occurrence is tricky iteratively. 
        # Let's use recursive DFS.
        
        def dfs(node, parent, cum_dist, depth_idx):
            nonlocal max_len, min_nodes
            
            val = nums[node]
            
            # Check if val has been seen in the current path
            if val in last_occurrence:
                prev_idx, prev_cum_dist = last_occurrence[val]
                # The valid path must start after prev_idx
                start_idx = prev_idx + 1
                start_cum_dist = 0
                # We don't have direct access to cum_dist at start_idx, but we can compute:
                # The path length from start_idx to depth_idx is cum_dist - (cum_dist at start_idx)
                # But we stored cum_dist at prev_idx. The node at prev_idx is the one with the duplicate value.
                # The path cannot include that node. So the start node is the child of the node at prev_idx that is on the current path.
                # Actually, the cumulative distance at start_idx is not directly stored. 
                # However, note: the path from root to current node has cumulative distance cum_dist.
                # The path from root to the node at prev_idx has cumulative distance prev_cum_dist.
                # The edge from the node at prev_idx to its child (which is the start of the new path) has some weight.
                # But we don't know which child it is without more info.
                
                # Alternative: Store the entire path's cumulative distances in a list? That would be O(N) space per path, too much.
                # Instead, we can store last_occurrence as value -> depth_idx only, and maintain a separate array for cum_dist at each depth_idx in the current path.
                # But with recursion, we can use a list that we append/pop.
                pass
            else:
                start_idx = 0
                start_cum_dist = 0
            
            # Actually, let's change approach: maintain a list 'path_cum_dist' where path_cum_dist[i] is the cumulative distance from root to the node at depth_idx i in the current path.
            # Then if val is in last_occurrence, let prev_idx = last_occurrence[val], then the start of the valid path is at depth_idx prev_idx + 1.
            # The cumulative distance at start is path_cum_dist[prev_idx + 1]? No, path_cum_dist[prev_idx+1] is the cum dist to the node at depth_idx prev_idx+1.
            # The path from that node to current node has length: cum_dist - path_cum_dist[prev_idx+1]
            # But wait, the node at depth_idx prev_idx has value val. The next node (child) on the path to current node is at depth_idx prev_idx+1.
            # The path starting at that child and ending at current node is valid.
            # So:
            #   length = cum_dist - path_cum_dist[prev_idx + 1]
            #   num_nodes = depth_idx - (prev_idx + 1) + 1 = depth_idx - prev_idx
            
            # If not in last_occurrence, start from root (depth_idx 0):
            #   length = cum_dist - path_cum_dist[0]  (which is 0)
            #   num_nodes = depth_idx - 0 + 1 = depth_idx + 1
            
            # We need to maintain path_cum_dist as a list that we append and pop.
            
            # Update last_occurrence for current val
            if val in last_occurrence:
                prev_idx, _ = last_occurrence[val]
                start_idx = prev_idx + 1
                # The cumulative distance at start_idx is path_cum_dist[start_idx]
                current_path_length = cum_dist - path_cum_dist[start_idx]
                current_num_nodes = depth_idx - start_idx + 1
            else:
                start_idx = 0
                current_path_length = cum_dist - path_cum_dist[0]  # path_cum_dist[0] is 0
                current_num_nodes = depth_idx + 1
            
            # Update global result
            if current_path_length > max_len:
                max_len = current_path_length
                min_nodes = current_num_nodes
            elif current_path_length == max_len:
                if current_num_nodes < min_nodes:
                    min_nodes = current_num_nodes
            
            # Record current node's info in last_occurrence and path_cum_dist
            last_occurrence[val] = (depth_idx, cum_dist)
            path_cum_dist.append(cum_dist)
            
            # Recurse to children
            for neighbor, weight in adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node, cum_dist + weight, depth_idx + 1)
            
            # Backtrack
            path_cum_dist.pop()
            del last_occurrence[val]
        
        # Initialize
        path_cum_dist = [0]  # cum_dist at depth_idx 0 is 0
        # last_occurrence is empty initially
        # Start DFS from root (node 0)
        dfs(0, -1, 0, 0)
        
        return [max_len, min_nodes]