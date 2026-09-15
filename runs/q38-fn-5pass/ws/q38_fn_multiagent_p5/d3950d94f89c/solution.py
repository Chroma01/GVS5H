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

        best_len = 0
        best_nodes = 1

        # dist_by_depth[d] = distance from root to the node at depth d
        # on the current root-to-node DFS path.
        dist_by_depth = []

        # left is the earliest depth on the current path such that
        # path[left .. current_depth] has all unique values.
        left = 0

        # Event tuple:
        # (node, parent, depth, dist, state, old_left, prev_last)
        # state = 0 -> enter node, state = 1 -> exit node
        stack = [(0, -1, 0, 0, 0, 0, -1)]

        while stack:
            node, parent, depth, dist, state, old_left, prev_last = stack.pop()

            if state == 0:
                val = nums[node]

                prev_last = last[val]
                old_left = left

                if prev_last != -1 and prev_last + 1 > left:
                    left = prev_last + 1

                last[val] = depth
                dist_by_depth.append(dist)

                cur_len = dist - dist_by_depth[left]
                cur_nodes = depth - left + 1

                if cur_len > best_len or (cur_len == best_len and cur_nodes < best_nodes):
                    best_len = cur_len
                    best_nodes = cur_nodes

                # Exit event must be processed after all children.
                stack.append((node, parent, depth, dist, 1, old_left, prev_last))

                for nei, w in adj[node]:
                    if nei != parent:
                        stack.append((nei, node, depth + 1, dist + w, 0, 0, -1))

            else:
                val = nums[node]
                last[val] = prev_last
                left = old_left
                dist_by_depth.pop()

        return [best_len, best_nodes]