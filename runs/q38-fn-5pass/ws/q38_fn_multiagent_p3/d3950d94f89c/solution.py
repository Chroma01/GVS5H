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

        # last[value] = depth of the most recent occurrence of value
        # on the current root-to-node path.
        last = {}

        # path_dist[d] = distance from root to the node at depth d
        # on the current root-to-node path.
        path_dist = []

        # Shallowest valid start depth for the current path window.
        left = 0

        # A single node is always a valid special path.
        best_len = 0
        best_nodes = 1

        # Stack entries:
        # (state, node, parent, depth, dist_from_root, prev_last, prev_left)
        # state = 0 -> enter node, state = 1 -> exit node and restore state.
        stack = [(0, 0, -1, 0, 0, -1, -1)]

        while stack:
            state, u, parent, depth, dist, prev_last, prev_left = stack.pop()

            if state == 0:
                val = nums[u]

                # Save state needed for restoration on exit.
                prev_last = last.get(val, -1)
                prev_left = left

                # If this value appeared inside the current valid window,
                # the window start must move below that previous occurrence.
                if prev_last != -1 and prev_last + 1 > left:
                    left = prev_last + 1

                last[val] = depth
                path_dist.append(dist)

                # Longest special path ending at u starts at depth `left`.
                cand_len = dist - path_dist[left]
                cand_nodes = depth - left + 1

                if cand_len > best_len:
                    best_len = cand_len
                    best_nodes = cand_nodes
                elif cand_len == best_len and cand_nodes < best_nodes:
                    best_nodes = cand_nodes

                # Exit event is pushed before children so it runs after them.
                stack.append((1, u, parent, depth, dist, prev_last, prev_left))

                for v, w in adj[u]:
                    if v != parent:
                        stack.append((0, v, u, depth + 1, dist + w, -1, -1))

            else:
                # Restore path distance list.
                path_dist.pop()

                # Restore last-seen depth for this node's value.
                val = nums[u]
                if prev_last == -1:
                    last.pop(val, None)
                else:
                    last[val] = prev_last

                # Restore sliding-window left boundary.
                left = prev_left

        return [best_len, best_nodes]