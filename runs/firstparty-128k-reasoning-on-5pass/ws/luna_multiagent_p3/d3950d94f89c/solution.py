from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        graph = [[] for _ in range(n)]
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))

        # last[value] is the latest depth of that value on the active path.
        last = [-1] * (max(nums) + 1)

        # Prefix distances and current valid starting-depth boundary.
        prefix = [0]
        left = 0

        best_length = 0
        best_nodes = 1

        # Event format:
        # enter: (0, node, parent, edge_weight)
        # exit:  (1, node, parent, old_left, old_last)
        stack = [(0, 0, -1, 0)]

        while stack:
            event = stack.pop()

            if event[0] == 0:
                _, node, parent, edge_weight = event

                if parent != -1:
                    prefix.append(prefix[-1] + edge_weight)

                depth = len(prefix) - 1
                value = nums[node]

                old_left = left
                old_last = last[value]

                # Any start must be below the previous occurrence of this value.
                left = max(left, old_last + 1)
                last[value] = depth

                length = prefix[depth] - prefix[left]
                node_count = depth - left + 1

                if length > best_length:
                    best_length = length
                    best_nodes = node_count
                elif length == best_length:
                    best_nodes = min(best_nodes, node_count)

                stack.append((1, node, parent, old_left, old_last))

                for child, weight in reversed(graph[node]):
                    if child != parent:
                        stack.append((0, child, node, weight))
            else:
                _, node, parent, old_left, old_last = event
                value = nums[node]

                left = old_left
                last[value] = old_last

                if parent != -1:
                    prefix.pop()

        return [best_length, best_nodes]