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

        # last[value] = deepest depth on the current root-to-node path
        # where this value occurs. A dictionary avoids relying on max(nums).
        last = {}

        dist_node = [0] * n
        path_nodes = []

        best_len = 0
        best_nodes = 1
        start_depth = 0

        # (node, parent, distance_from_root, depth, is_enter, old_last, old_start_depth)
        stack = [(0, -1, 0, 0, True, -1, 0)]

        while stack:
            u, parent, dist, depth, enter, old_last, old_start = stack.pop()

            if enter:
                val = nums[u]

                old_last = last.get(val, -1)
                old_start = start_depth

                if old_last >= start_depth:
                    start_depth = old_last + 1

                last[val] = depth
                path_nodes.append(u)
                dist_node[u] = dist

                ancestor = path_nodes[start_depth]
                length = dist - dist_node[ancestor]
                nodes = depth - start_depth + 1

                if length > best_len or (length == best_len and nodes < best_nodes):
                    best_len = length
                    best_nodes = nodes

                stack.append((u, parent, dist, depth, False, old_last, old_start))

                for v, w in adj[u]:
                    if v != parent:
                        stack.append((v, u, dist + w, depth + 1, True, -1, 0))

            else:
                val = nums[u]

                if old_last == -1:
                    last.pop(val, None)
                else:
                    last[val] = old_last

                start_depth = old_start
                path_nodes.pop()

        return [best_len, best_nodes]