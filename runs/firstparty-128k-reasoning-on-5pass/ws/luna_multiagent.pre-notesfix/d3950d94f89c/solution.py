from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        graph = [[] for _ in range(n)]

        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))

        # latest[value] is the depth of its latest occurrence on the
        # currently active root-to-node path.
        latest = {}

        # Root-to-current-node cumulative distances, indexed by depth.
        path_dist = []

        best_length = 0
        best_nodes = 1

        # Enter event:
        # (0, node, parent, distance, depth, lower_bound)
        #
        # Exit event:
        # (1, node, value, previous_latest_depth)
        stack = [(0, 0, -1, 0, 0, 0)]

        while stack:
            event = stack.pop()

            if event[0] == 0:
                _, node, parent, distance, depth, lower_bound = event

                value = nums[node]
                previous_depth = latest.get(value, -1)

                # The path start must be after the previous occurrence of
                # the current value, as well as after the inherited bound.
                lower_bound = max(lower_bound, previous_depth + 1)

                latest[value] = depth
                path_dist.append(distance)

                current_length = distance - path_dist[lower_bound]
                current_nodes = depth - lower_bound + 1

                if current_length > best_length:
                    best_length = current_length
                    best_nodes = current_nodes
                elif current_length == best_length:
                    best_nodes = min(best_nodes, current_nodes)

                # Restore the previous occurrence information on backtrack.
                stack.append((1, node, value, previous_depth))

                # All child events inherit the updated lower bound.
                for neighbor, edge_length in graph[node]:
                    if neighbor != parent:
                        stack.append(
                            (
                                0,
                                neighbor,
                                node,
                                distance + edge_length,
                                depth + 1,
                                lower_bound,
                            )
                        )
            else:
                _, _, value, previous_depth = event
                path_dist.pop()

                if previous_depth == -1:
                    del latest[value]
                else:
                    latest[value] = previous_depth

        return [best_length, best_nodes]