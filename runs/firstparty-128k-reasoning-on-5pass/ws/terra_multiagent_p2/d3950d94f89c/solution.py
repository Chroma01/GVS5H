from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        graph = [[] for _ in range(n)]

        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))

        last_depth = {}
        path_dist = [0] * n

        best_length = 0
        best_nodes = 1
        left = 0

        # Enter event: (0, node, parent, depth, distance)
        # Exit event:  (1, value, previous_depth, previous_left)
        stack = [(0, 0, -1, 0, 0)]

        while stack:
            event = stack.pop()

            if event[0] == 1:
                _, value, previous_depth, previous_left = event
                if previous_depth == -1:
                    del last_depth[value]
                else:
                    last_depth[value] = previous_depth
                left = previous_left
                continue

            _, node, parent, depth, distance = event
            path_dist[depth] = distance

            value = nums[node]
            previous_depth = last_depth.get(value, -1)
            previous_left = left

            if previous_depth != -1:
                left = max(left, previous_depth + 1)

            last_depth[value] = depth

            length = distance - path_dist[left]
            node_count = depth - left + 1

            if length > best_length or (
                length == best_length and node_count < best_nodes
            ):
                best_length = length
                best_nodes = node_count

            stack.append((1, value, previous_depth, previous_left))

            for neighbor, weight in graph[node]:
                if neighbor != parent:
                    stack.append(
                        (0, neighbor, node, depth + 1, distance + weight)
                    )

        return [best_length, best_nodes]