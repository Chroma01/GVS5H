from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        max_val = max(nums) if nums else 0
        last = [-1] * (max_val + 1)

        path_dist = []
        left_at_depth = []

        best_len = 0
        best_nodes = 1

        # node, parent, state (0 = enter, 1 = exit), dist_from_root, old_last_index
        stack = [(0, -1, 0, 0, -1)]

        while stack:
            node, parent, state, dist, old = stack.pop()

            if state == 0:
                depth = len(path_dist)
                val = nums[node]
                prev = last[val]

                if depth == 0:
                    left = 0
                else:
                    left = max(left_at_depth[-1], prev + 1)

                path_dist.append(dist)
                left_at_depth.append(left)
                last[val] = depth

                length = dist - path_dist[left]
                nodes = depth - left + 1

                if length > best_len or (length == best_len and nodes < best_nodes):
                    best_len = length
                    best_nodes = nodes

                stack.append((node, parent, 1, dist, prev))

                for nei, w in adj[node]:
                    if nei != parent:
                        stack.append((nei, node, 0, dist + w, -1))
            else:
                val = nums[node]
                last[val] = old
                path_dist.pop()
                left_at_depth.pop()

        return [best_len, best_nodes]