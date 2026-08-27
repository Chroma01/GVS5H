from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        graph = [[] for _ in range(n)]

        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))

        last_depth = {}
        path_distances = []

        best_length = 0
        best_nodes = 1

        # Enter event:
        # (0, node, parent, depth, root_distance, left_boundary)
        # Exit event:
        # (1, value, previous_depth)
        stack = [(0, 0, -1, 0, 0, 0)]

        while stack:
            event = stack.pop()

            if event[0] == 1:
                _, value, previous_depth = event
                if previous_depth == -1:
                    del last_depth[value]
                else:
                    last_depth[value] = previous_depth
                path_distances.pop()
                continue

            _, node, parent, depth, root_distance, left_boundary = event

            value = nums[node]
            previous_depth = last_depth.get(value, -1)

            if previous_depth != -1:
                left_boundary = max(left_boundary, previous_depth + 1)

            last_depth[value] = depth
            path_distances.append(root_distance)

            candidate_length = root_distance - path_distances[left_boundary]
            candidate_nodes = depth - left_boundary + 1

            if (candidate_length > best_length or
                    (candidate_length == best_length and candidate_nodes < best_nodes)):
                best_length = candidate_length
                best_nodes = candidate_nodes

            stack.append((1, value, previous_depth))

            for neighbor, weight in graph[node]:
                if neighbor != parent:
                    stack.append((
                        0,
                        neighbor,
                        node,
                        depth + 1,
                        root_distance + weight,
                        left_boundary
                    ))

        return [best_length, best_nodes]