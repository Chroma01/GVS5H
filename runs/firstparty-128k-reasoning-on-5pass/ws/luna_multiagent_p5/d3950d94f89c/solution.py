from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        graph = [[] for _ in range(n)]

        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))

        # latest[value] is the depth of its latest occurrence on the
        # current root-to-node path.
        latest = {}

        # Every valid path ending at the current node must start at a
        # depth greater than boundary.
        boundary = -1

        # prefix_dist[i] is the distance from the root to the node at
        # depth i on the current path.
        prefix_dist = []

        best_length = -1
        best_nodes = n

        # Enter event: (0, node, parent, distance_from_root)
        # Exit event:  (1, node, previous_latest, previous_boundary)
        stack = [(0, 0, -1, 0)]

        while stack:
            event = stack.pop()

            if event[0] == 0:
                _, node, parent, distance = event
                depth = len(prefix_dist)

                previous_latest = latest.get(nums[node], -1)
                previous_boundary = boundary

                prefix_dist.append(distance)
                latest[nums[node]] = depth
                if previous_latest > boundary:
                    boundary = previous_latest

                start_depth = boundary + 1
                path_length = distance - prefix_dist[start_depth]
                path_nodes = depth - boundary

                if (
                    path_length > best_length
                    or (
                        path_length == best_length
                        and path_nodes < best_nodes
                    )
                ):
                    best_length = path_length
                    best_nodes = path_nodes

                stack.append(
                    (1, node, previous_latest, previous_boundary)
                )

                for neighbor, weight in reversed(graph[node]):
                    if neighbor != parent:
                        stack.append(
                            (0, neighbor, node, distance + weight)
                        )
            else:
                _, node, previous_latest, previous_boundary = event

                prefix_dist.pop()

                if previous_latest == -1:
                    del latest[nums[node]]
                else:
                    latest[nums[node]] = previous_latest

                boundary = previous_boundary

        return [best_length, best_nodes]