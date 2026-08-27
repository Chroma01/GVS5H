from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        graph = [[] for _ in range(n)]

        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))

        parent = [-1] * n
        depth = [0] * n
        distance = [0] * n
        nearest_repeat = [-1] * n

        # Root the tree and determine the nearest equal-valued ancestor
        # for every node. Enter/exit events restore values on backtracking.
        last_depth = {}
        stack = [(0, -1, 0)]  # node, parent, event: 0 = enter, 1 = exit

        while stack:
            node, par, event = stack.pop()

            if event == 0:
                parent[node] = par

                if par != -1:
                    depth[node] = depth[par] + 1

                value = nums[node]
                previous_depth = last_depth.get(value, -1)
                nearest_repeat[node] = previous_depth
                last_depth[value] = depth[node]

                stack.append((node, previous_depth, 1))

                for neighbor, weight in graph[node]:
                    if neighbor == par:
                        continue
                    distance[neighbor] = distance[node] + weight
                    stack.append((neighbor, node, 0))
            else:
                value = nums[node]
                if par == -1:
                    del last_depth[value]
                else:
                    last_depth[value] = par

        # Traverse again while maintaining the current root-to-node path.
        # For each endpoint, compute the earliest valid starting depth.
        valid_start_bound = [-1] * n
        path = []

        best_length = -1
        min_nodes = n + 1

        stack = [(0, 0)]  # node, event: 0 = enter, 1 = exit

        while stack:
            node, event = stack.pop()

            if event == 0:
                path.append(node)

                if parent[node] == -1:
                    valid_start_bound[node] = nearest_repeat[node]
                else:
                    valid_start_bound[node] = max(
                        valid_start_bound[parent[node]],
                        nearest_repeat[node],
                    )

                start_depth = valid_start_bound[node] + 1
                start_node = path[start_depth]

                path_length = distance[node] - distance[start_node]
                node_count = depth[node] - start_depth + 1

                if path_length > best_length:
                    best_length = path_length
                    min_nodes = node_count
                elif path_length == best_length:
                    min_nodes = min(min_nodes, node_count)

                stack.append((node, 1))
                for neighbor, _ in graph[node]:
                    if neighbor != parent[node]:
                        stack.append((neighbor, 0))
            else:
                path.pop()

        return [best_length, min_nodes]