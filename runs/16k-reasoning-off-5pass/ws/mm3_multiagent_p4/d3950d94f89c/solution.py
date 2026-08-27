from typing import List
import sys
sys.setrecursionlimit(1000000)

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        # prefix_len[d] = total edge length from root (node 0) to the node at depth d on the current path
        prefix_len = [0] * n
        last_occ = {}          # value -> depth of most recent occurrence on current root-to-node path
        start_depth_holder = [0]  # mutable container for the left boundary depth
        
        best_len = 0
        best_nodes = 1
        
        def dfs(node: int, parent: int, depth: int, cur_len: int) -> None:
            nonlocal best_len, best_nodes
            
            # Record the prefix length for the current depth
            prefix_len[depth] = cur_len
            
            val = nums[node]
            
            # Save the current start_depth so we can restore it on backtrack
            old_start_depth = start_depth_holder[0]
            
            # If the value was seen before on the current path, we must exclude up to that occurrence
            if val in last_occ:
                prev_depth = last_occ[val]
                if prev_depth >= start_depth_holder[0]:
                    start_depth_holder[0] = prev_depth + 1
            
            # Record this occurrence
            last_occ[val] = depth
            
            # Evaluate the longest special path ending at this node
            sd = start_depth_holder[0]
            candidate_len = prefix_len[depth] - prefix_len[sd]
            candidate_nodes = depth - sd + 1
            
            if candidate_len > best_len:
                best_len = candidate_len
                best_nodes = candidate_nodes
            elif candidate_len == best_len and candidate_nodes < best_nodes:
                best_nodes = candidate_nodes
            
            # Recurse into children
            for neighbor, weight in adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node, depth + 1, cur_len + weight)
            
            # Backtrack: remove this value's occurrence only if it is the one we stored
            if last_occ.get(val) == depth:
                del last_occ[val]
            
            # Restore the start_depth
            start_depth_holder[0] = old_start_depth
        
        dfs(0, -1, 0, 0)
        return [best_len, best_nodes]


# ----------------------
# Test harness
# ----------------------
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    edges1 = [[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]]
    nums1  = [2,1,2,1,3,1]
    print("Example 1:", sol.longestSpecialPath(edges1, nums1), "expected [6, 2]")
    
    # Example 2
    edges2 = [[1,0,8]]
    nums2  = [2,2]
    print("Example 2:", sol.longestSpecialPath(edges2, nums2), "expected [0, 1]")
    
    # Edge case: n=2, linear, unique values
    edges3 = [[0,1,5]]
    nums3  = [1,2]
    print("Unique 2-node:", sol.longestSpecialPath(edges3, nums3), "expected [5, 2]")
    
    # Edge case: n=2, duplicate values
    edges4 = [[0,1,5]]
    nums4  = [1,1]
    print("Duplicate 2-node:", sol.longestSpecialPath(edges4, nums4), "expected [0, 1]")
    
    # Edge case: all same values, star tree
    # root 0, children 1..4
    edges5 = [[0,1,1],[0,2,1],[0,3,1],[0,4,1]]
    nums5  = [7,7,7,7,7]
    print("All duplicates star:", sol.longestSpecialPath(edges5, nums5), "expected [0, 1]")
    
    # Edge case: linear tree with all unique values
    # 0-1 (2), 1-2 (3), 2-3 (4), 3-4 (5)
    edges6 = [[0,1,2],[1,2,3],[2,3,4],[3,4,5]]
    nums6  = [1,2,3,4,5]
    print("Linear all unique:", sol.longestSpecialPath(edges6, nums6), "expected [14, 5]")
    
    # Edge case: linear with duplicate after some unique prefix
    # values: 1,2,3,2,4  -> best path: 0-1-2-3-4 (length 14) since 2 at node 3 invalidates
    # Wait: nodes: 0:1, 1:2, 2:3, 3:2, 4:4
    # special path ending at 3: values {1,2,3} length 2+3+4=9, nodes=4
    # special path ending at 4: values {1,2,3,2,4} -> dup, must start after prev 2 (node1) so {3,2,4} length 4+5=9, nodes=3
    # special path ending at 0: length 0, nodes=1
    # best is 9 with 3 nodes
    edges7 = [[0,1,2],[1,2,3],[2,3,4],[3,4,5]]
    nums7  = [1,2,3,2,4]
    print("Linear with dup:", sol.longestSpecialPath(edges7, nums7), "expected [9, 3]")