from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        graph = [[] for _ in range(n)]
        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))

        prefix_dist = [0] * n
        last_seen = {}

        best_length = 0
        min_nodes = 1

        # Enter event: (0, node, parent, depth, distance, window_left)
        # Exit event:  (1, value, previous_depth)
        stack = [(0, 0, -1, 0, 0, 0)]

        while stack:
            event = stack.pop()

            if event[0] == 1:
                _, value, previous_depth = event
                if previous_depth == -1:
                    del last_seen[value]
                else:
                    last_seen[value] = previous_depth
                continue

            _, node, parent, depth, distance, window_left = event
            value = nums[node]

            previous_depth = last_seen.get(value, -1)
            new_window_left = max(window_left, previous_depth + 1)

            last_seen[value] = depth
            prefix_dist[depth] = distance

            path_length = distance - prefix_dist[new_window_left]
            node_count = depth - new_window_left + 1

            if path_length > best_length:
                best_length = path_length
                min_nodes = node_count
            elif path_length == best_length and node_count < min_nodes:
                min_nodes = node_count

            stack.append((1, value, previous_depth))

            for neighbor, edge_length in graph[node]:
                if neighbor != parent:
                    stack.append((
                        0,
                        neighbor,
                        node,
                        depth + 1,
                        distance + edge_length,
                        new_window_left
                    ))

        return [best_length, min_nodes]