from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        graph = [[] for _ in range(n)]
        for u, v, weight in edges:
            graph[u].append((v, weight))
            graph[v].append((u, weight))

        last_depth = {}
        prefix_dist = []

        best_length = 0
        best_nodes = 1

        # Enter event:
        # (0, node, parent, depth, root_distance, inherited_valid_start)
        # Exit event:
        # (1, value, prior_depth)
        stack = [(0, 0, -1, 0, 0, 0)]

        while stack:
            event = stack.pop()

            if event[0] == 1:
                _, value, prior_depth = event
                prefix_dist.pop()

                if prior_depth == -1:
                    del last_depth[value]
                else:
                    last_depth[value] = prior_depth
                continue

            _, node, parent, depth, distance, inherited_start = event
            value = nums[node]

            prior_depth = last_depth.get(value, -1)
            valid_start = max(inherited_start, prior_depth + 1)

            last_depth[value] = depth
            prefix_dist.append(distance)

            path_length = distance - prefix_dist[valid_start]
            node_count = depth - valid_start + 1

            if path_length > best_length:
                best_length = path_length
                best_nodes = node_count
            elif path_length == best_length and node_count < best_nodes:
                best_nodes = node_count

            stack.append((1, value, prior_depth))

            for neighbor, weight in graph[node]:
                if neighbor != parent:
                    stack.append(
                        (0, neighbor, node, depth + 1, distance + weight, valid_start)
                    )

        return [best_length, best_nodes]