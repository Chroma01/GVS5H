from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        if n == 0:
            return [0, 0]

        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        max_val = max(nums)
        last = [-1] * (max_val + 1)

        path_dist = []
        best_len = 0
        best_nodes = 1
        boundary = -1

        # Stack entries:
        # (node, parent, state, dist, saved_last, saved_boundary)
        # state 0 = enter node, state 1 = exit node
        stack = [(0, -1, 0, 0, -1, -1)]

        while stack:
            node, parent, state, dist, saved_last, saved_boundary = stack.pop()

            if state == 0:
                val = nums[node]

                prev_last = last[val]
                prev_boundary = boundary

                # Only this node's value can create a new duplicate constraint.
                if prev_last > boundary:
                    boundary = prev_last

                path_dist.append(dist)
                depth = len(path_dist) - 1
                last[val] = depth

                # The highest valid ancestor is at depth boundary + 1.
                start_dist = path_dist[boundary + 1]
                cur_len = dist - start_dist
                cur_nodes = depth - boundary

                if cur_len > best_len or (cur_len == best_len and cur_nodes < best_nodes):
                    best_len = cur_len
                    best_nodes = cur_nodes

                # Exit marker must be processed after all children.
                stack.append((node, parent, 1, 0, prev_last, prev_boundary))

                for child, w in adj[node]:
                    if child != parent:
                        stack.append((child, node, 0, dist + w, -1, -1))

            else:
                val = nums[node]
                boundary = saved_boundary
                last[val] = saved_last
                path_dist.pop()

        return [best_len, best_nodes]