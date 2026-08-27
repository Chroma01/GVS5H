import sys
from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        sys.setrecursionlimit(10**6)
        
        # Stacks for cumulative distance and node count from root to current node
        # dist_stack[d] = total edge length from root to node at depth d
        # cnt_stack[d] = number of nodes from root to depth d (i.e., d+1)
        dist_stack = [0]
        cnt_stack = [1]
        
        # Map from node value to the depth of its most recent occurrence on the current path
        last_occ = {}
        
        # start_stack[depth] = the leftmost depth index such that the subpath 
        # from that index to the current node has all unique values.
        # We save it per depth so we can restore on backtrack.
        start_stack = [0]
        
        best_len = 0
        best_cnt = 1
        
        def dfs(u: int, parent: int, depth: int):
            nonlocal best_len, best_cnt
            
            val = nums[u]
            prev_idx = last_occ.get(val, -1)
            
            # Inherit the current window start from the parent depth
            cur_start = start_stack[depth]
            
            # If this value already appears in the current window, move start past it
            if prev_idx >= cur_start:
                cur_start = prev_idx + 1
            
            # Save the window start for this depth
            start_stack.append(cur_start)
            
            # Compute total length and node count for the path from cur_start to u
            path_dist = dist_stack[depth] - (dist_stack[cur_start - 1] if cur_start > 0 else 0)
            path_cnt = cnt_stack[depth] - (cnt_stack[cur_start - 1] if cur_start > 0 else 0)
            
            # Update global best
            if path_dist > best_len:
                best_len = path_dist
                best_cnt = path_cnt
            elif path_dist == best_len and path_cnt < best_cnt:
                best_cnt = path_cnt
            
            # Mark this value as seen at this depth
            last_occ[val] = depth
            
            # Explore children
            for v, w in adj[u]:
                if v == parent:
                    continue
                dist_stack.append(dist_stack[-1] + w)
                cnt_stack.append(cnt_stack[-1] + 1)
                dfs(v, u, depth + 1)
                dist_stack.pop()
                cnt_stack.pop()
            
            # Restore last_occ to its state before entering this node
            if prev_idx == -1:
                del last_occ[val]
            else:
                last_occ[val] = prev_idx
            
            # Pop the saved window start for this depth
            start_stack.pop()
        
        dfs(0, -1, 0)
        return [best_len, best_cnt]