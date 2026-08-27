from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        graph = [[] for _ in range(n)]
        for u, v, weight in edges:
            graph[u].append((v, weight))
            graph[v].append((u, weight))

        last_seen = [-1] * (max(nums) + 1)
        path_dist = []

        best_length = 0
        best_nodes = 1

        # Enter event: (0, node, parent, root_distance, inherited_start_depth)
        # Exit event:  (1, value, previous_last_seen_depth)
        stack = [(0, 0, -1, 0, 0)]

        while stack:
            event = stack.pop()

            if event[0] == 1:
                _, value, previous_depth = event
                last_seen[value] = previous_depth
                path_dist.pop()
                continue

            _, node, parent, distance, inherited_start = event
            depth = len(path_dist)
            value = nums[node]
            previous_depth = last_seen[value]

            valid_start = inherited_start
            if previous_depth != -1:
                valid_start = max(valid_start, previous_depth + 1)

            path_dist.append(distance)
            last_seen[value] = depth

            length = distance - path_dist[valid_start]
            node_count = depth - valid_start + 1

            if length > best_length:
                best_length = length
                best_nodes = node_count
            elif length == best_length and node_count < best_nodes:
                best_nodes = node_count

            stack.append((1, value, previous_depth))

            for neighbor, weight in graph[node]:
                if neighbor != parent:
                    stack.append(
                        (0, neighbor, node, distance + weight, valid_start)
                    )

        return [best_length, best_nodes]