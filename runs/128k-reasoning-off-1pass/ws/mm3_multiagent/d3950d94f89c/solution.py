from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        # Build adjacency list: (neighbor, length)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        best_len = 0
        best_nodes = 1
        
        # Current path state (root -> ... -> current)
        path_vals = []      # values of nodes in current path
        path_node_ids = []  # actual node ids in current path
        path_lens = []      # path_lens[i] = total edge-length sum from path start to node at index i
        last_pos = {}       # value -> latest index in path_vals where it appears
        
        # Iterative DFS: (node, parent, edge_len_from_parent, state)
        # state 0 = enter, 1 = leave
        stack = [(0, -1, 0, 0)]
        
        while stack:
            node, parent, plen, state = stack.pop()
            if state == 0:
                val = nums[node]
                
                # If value already exists in current path, trim up to (and including) its previous occurrence
                if val in last_pos:
                    prev_idx = last_pos[val]
                    cut = prev_idx + 1
                    if cut > 0:
                        # Remove the values being trimmed from last_pos so the map stays consistent
                        for i in range(cut):
                            removed_val = path_vals[i]
                            if last_pos.get(removed_val) == i:
                                del last_pos[removed_val]
                        del path_vals[:cut]
                        del path_node_ids[:cut]
                        del path_lens[:cut]
                
                # Add current node to the path
                path_vals.append(val)
                path_node_ids.append(node)
                if len(path_lens) == 0:
                    path_lens.append(0)
                else:
                    path_lens.append(path_lens[-1] + plen)
                last_pos[val] = len(path_vals) - 1
                
                # Update global best with the path ending at this node
                cur_len = path_lens[-1]
                cur_nodes = len(path_vals)
                if cur_len > best_len:
                    best_len = cur_len
                    best_nodes = cur_nodes
                elif cur_len == best_len and cur_nodes < best_nodes:
                    best_nodes = cur_nodes
                
                # Push leave action
                stack.append((node, parent, plen, 1))
                
                # Push children
                for neighbor, weight in adj[node]:
                    if neighbor != parent:
                        stack.append((neighbor, node, weight, 0))
            else:
                # Backtrack: remove this node from the current path
                idx = len(path_vals) - 1
                if idx >= 0 and path_node_ids[idx] == node:
                    val = path_vals[idx]
                    if last_pos.get(val) == idx:
                        del last_pos[val]
                    path_vals.pop()
                    path_node_ids.pop()
                    path_lens.pop()
        
        return [best_len, best_nodes]