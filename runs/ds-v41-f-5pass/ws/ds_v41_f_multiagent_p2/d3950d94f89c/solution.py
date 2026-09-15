from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        max_val = max(nums)
        last = [-1] * (max_val + 1)
        path_dist = [0] * n
        
        best_len = 0
        best_cnt = 1
        
        stack = [(0, -1, 0, 0, 0, False, -1)]
        while stack:
            v, p, dep, d, parent_ns, entered, prev = stack.pop()
            x = nums[v]
            if not entered:
                ns = parent_ns
                if last[x] != -1:
                    cand = last[x] + 1
                    if cand > ns:
                        ns = cand
                    prev = last[x]
                else:
                    prev = -1
                last[x] = dep
                path_dist[dep] = d
                
                length = d - path_dist[ns]
                cnt = dep - ns + 1
                if length > best_len or (length == best_len and cnt < best_cnt):
                    best_len = length
                    best_cnt = cnt
                
                stack.append((v, p, dep, d, ns, True, prev))
                for to, w in adj[v]:
                    if to != p:
                        stack.append((to, v, dep + 1, d + w, ns, False, -1))
            else:
                last[x] = prev
        
        return [best_len, best_cnt]