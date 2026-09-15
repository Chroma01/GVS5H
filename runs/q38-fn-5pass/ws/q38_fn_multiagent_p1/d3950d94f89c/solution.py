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

        max_value = max(nums) if nums else 0
        last = [-1] * (max_value + 1)

        # depth_dist[depth] = weighted distance from root to the current
        # path node at this depth.
        depth_dist = [0] * n

        best_len = 0
        best_nodes = 1

        # start = earliest depth such that path[start..current_depth]
        # has unique node values.
        start = 0

        # Stack entries:
        # enter: (0, node, parent, depth, distance, dummy_prev, dummy_old_start)
        # exit:  (1, node, parent, depth, distance, prev_last_depth, old_start)
        stack = [(0, 0, -1, 0, 0, -1, 0)]

        while stack:
            state, node, parent, depth, d, prev, old_start = stack.pop()

            if state == 0:
                val = nums[node]

                # Save rollback information.
                prev = last[val]
                old_start = start

                # If this value appeared inside the current unique suffix,
                # the suffix must start strictly below that previous occurrence.
                if prev >= start:
                    start = prev + 1

                last[val] = depth
                depth_dist[depth] = d

                # Longest valid special path ending at this node.
                length = d - depth_dist[start]
                nodes = depth - start + 1

                if length > best_len or (length == best_len and nodes < best_nodes):
                    best_len = length
                    best_nodes = nodes

                # Exit event must be processed after all children.
                stack.append((1, node, parent, depth, d, prev, old_start))

                for nxt, w in adj[node]:
                    if nxt != parent:
                        stack.append((0, nxt, node, depth + 1, d + w, -1, 0))

            else:
                # Roll back this node's contribution to the current root-to-node path.
                last[nums[node]] = prev
                start = old_start

        return [best_len, best_nodes]