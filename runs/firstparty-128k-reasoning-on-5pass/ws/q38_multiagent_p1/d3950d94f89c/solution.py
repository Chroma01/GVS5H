from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        max_val = max(nums) if nums else 0
        last = [-1] * (max_val + 1)
        path_dist = [0] * n

        best_len = 0
        best_nodes = 1
        bound = 0

        # Enter event: (0, node, parent, depth, dist)
        # Exit event:  (1, node, old_last, old_bound)
        stack = [(0, 0, -1, 0, 0)]

        while stack:
            event = stack.pop()

            if event[0] == 0:
                _, node, parent, depth, dist = event

                val = nums[node]
                prev = last[val]
                parent_bound = bound

                # If this value appeared before at depth prev, any valid path
                # ending here must start strictly below prev.
                if prev + 1 > bound:
                    bound = prev + 1

                last[val] = depth
                path_dist[depth] = dist

                cand_len = dist - path_dist[bound]
                cand_nodes = depth - bound + 1

                if cand_len > best_len or (cand_len == best_len and cand_nodes < best_nodes):
                    best_len = cand_len
                    best_nodes = cand_nodes

                # Restore state after all children are processed.
                stack.append((1, node, prev, parent_bound))

                for nei, w in adj[node]:
                    if nei != parent:
                        stack.append((0, nei, node, depth + 1, dist + w))

            else:
                _, node, old_last, old_bound = event
                bound = old_bound
                last[nums[node]] = old_last

        return [best_len, best_nodes]