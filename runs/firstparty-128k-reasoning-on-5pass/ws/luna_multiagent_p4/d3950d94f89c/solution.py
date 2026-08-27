from typing import List
import heapq


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        graph = [[] for _ in range(n)]

        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))

        # For each value on the active root-to-current path:
        # latest[value]   = latest position of that value
        # conflict[value] = previous position of that value, or -1
        latest = {}
        conflict = {}
        version = {}
        heap = []

        # Root distances for the active path, indexed by path position.
        path_dist = []

        best_length = 0
        best_nodes = 1

        # Enter event: (node, parent, distance, 1)
        # Exit event:  (node, previous_latest, previous_conflict, 0)
        stack = [(0, -1, 0, 1)]

        while stack:
            node, second, third, is_enter = stack.pop()
            value = nums[node]

            if is_enter:
                parent = second
                distance = third
                position = len(path_dist)
                path_dist.append(distance)

                previous_latest = latest.get(value, -1)
                previous_conflict = conflict.get(value, -1)

                latest[value] = position
                conflict[value] = previous_latest
                version[value] = version.get(value, 0) + 1
                current_version = version[value]

                if previous_latest >= 0:
                    heapq.heappush(
                        heap,
                        (-previous_latest, value, current_version),
                    )

                # Discard heap entries that do not describe the current
                # active state of their value.
                while heap:
                    neg_position, heap_value, heap_version = heap[0]
                    position_in_heap = -neg_position
                    if (
                        version.get(heap_value, 0) == heap_version
                        and conflict.get(heap_value, -1) == position_in_heap
                    ):
                        break
                    heapq.heappop(heap)

                boundary = -heap[0][0] if heap else -1
                start = boundary + 1

                current_length = distance - path_dist[start]
                current_nodes = position - boundary

                if (
                    current_length > best_length
                    or (
                        current_length == best_length
                        and current_nodes < best_nodes
                    )
                ):
                    best_length = current_length
                    best_nodes = current_nodes

                stack.append((node, previous_latest, previous_conflict, 0))

                for neighbor, weight in graph[node]:
                    if neighbor != parent:
                        stack.append(
                            (neighbor, node, distance + weight, 1)
                        )

            else:
                previous_latest = second
                previous_conflict = third

                if previous_latest >= 0:
                    latest[value] = previous_latest
                else:
                    latest.pop(value, None)

                if previous_conflict >= 0:
                    conflict[value] = previous_conflict
                else:
                    conflict.pop(value, None)

                version[value] = version.get(value, 0) + 1
                restored_version = version[value]

                if previous_conflict >= 0:
                    heapq.heappush(
                        heap,
                        (-previous_conflict, value, restored_version),
                    )

                path_dist.pop()

        return [best_length, best_nodes]