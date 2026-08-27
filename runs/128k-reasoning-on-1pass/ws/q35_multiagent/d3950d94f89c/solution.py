import sys
from typing import List

sys.setrecursionlimit(100000)

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
            
        dist = [0] * n
        depth = [0] * n
        path_nodes = [0] * n
        last_pos = [-1] * 50001  
        
        max_len = 0
        min_nodes = 1
        
        def dfs(u, p, current_forbidden, current_dist):
            nonlocal max_len, min_nodes
            val = nums[u]
            old_last = last_pos[val]
            
            # Update state for current path BEFORE computing ancestor
            # This fixes the stale ancestor access when start_depth == depth[u]
            last_pos[val] = depth[u]
            path_nodes[depth[u]] = u
            
            # The deepest valid ancestor must be deeper than any conflicting value's last position
            new_forbidden = current_forbidden if current_forbidden > old_last else old_last
            start_depth = new_forbidden + 1
            
            # path_nodes[start_depth] gives the ancestor node at the valid starting depth
            ancestor = path_nodes[start_depth]
            path_len = current_dist - dist[ancestor]
            node_count = depth[u] - start_depth + 1
            
            if path_len > max_len:
                max_len = path_len
                min_nodes = node_count
            elif path_len == max_len:
                if node_count < min_nodes:
                    min_nodes = node_count
                    
            for v, w in adj[u]:
                if v != p:
                    dist[v] = current_dist + w
                    depth[v] = depth[u] + 1
                    dfs(v, u, new_forbidden, dist[v])
                    
            # Backtrack: restore last_pos to previous state
            last_pos[val] = old_last

        dfs(0, -1, -1, 0)
        return [max_len, min_nodes]