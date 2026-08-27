from typing import List
import sys

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        cum_len = [0] * n
        depth = [0] * n
        
        path_nodes = []
        path_start = 0
        value_to_index = {}
        
        best_len = 0
        best_nodes = 1
        
        sys.setrecursionlimit(10**6)
        
        def dfs(u, parent):
            nonlocal best_len, best_nodes, path_start
            for v, w in adj[u]:
                if v == parent:
                    continue
                cum_len[v] = cum_len[u] + w
                depth[v] = depth[u] + 1
                
                old_path_start = path_start
                old_index = -1
                if nums[v] in value_to_index:
                    old_index = value_to_index[nums[v]]
                
                path_nodes.append(v)
                if nums[v] in value_to_index and value_to_index[nums[v]] >= path_start:
                    idx = value_to_index[nums[v]]
                    path_start = idx + 1
                value_to_index[nums[v]] = len(path_nodes) - 1
                
                # Evaluate current path
                front = path_nodes[path_start]
                path_length = cum_len[v] - cum_len[front]
                node_count = depth[v] - depth[front] + 1
                if path_length > best_len or (path_length == best_len and node_count < best_nodes):
                    best_len = path_length
                    best_nodes = node_count
                
                dfs(v, u)
                
                # Backtrack
                path_nodes.pop()
                if old_index != -1:
                    value_to_index[nums[v]] = old_index
                else:
                    if nums[v] in value_to_index:
                        del value_to_index[nums[v]]
                path_start = old_path_start
        
        # Start from root
        path_nodes.append(0)
        value_to_index[nums[0]] = 0
        # Root is a valid path of length 0 with 1 node
        # best_len and best_nodes already initialized
        
        dfs(0, -1)
        
        return [best_len, best_nodes]