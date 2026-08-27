from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        graph = [[] for _ in range(n)]

        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))

        last = [-1] * (max(nums) + 1)
        path_dist = []

        best_length = 0
        best_nodes = 1
        boundary = 0

        # Enter event: (0, node, parent, distance, depth)
        # Exit event:  (1, node, previous_last, previous_boundary)
        stack = [(0, 0, -1, 0, 0)]

        while stack:
            event = stack.pop()

            if event[0] == 0:
                _, node, parent, distance, depth = event

                value = nums[node]
                previous_last = last[value]
                previous_boundary = boundary

                if previous_last != -1:
                    boundary = max(boundary, previous_last + 1)

                last[value] = depth
                path_dist.append(distance)

                current_length = distance - path_dist[boundary]
                current_nodes = depth - boundary + 1

                if current_length > best_length:
                    best_length = current_length
                    best_nodes = current_nodes
                elif current_length == best_length:
                    best_nodes = min(best_nodes, current_nodes)

                stack.append((1, node, previous_last, previous_boundary))

                for neighbor, weight in graph[node]:
                    if neighbor != parent:
                        stack.append(
                            (
                                0,
                                neighbor,
                                node,
                                distance + weight,
                                depth + 1,
                            )
                        )
            else:
                _, node, previous_last, previous_boundary = event
                last[nums[node]] = previous_last
                boundary = previous_boundary
                path_dist.pop()

        return [best_length, best_nodes]