from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        if n == 0:
            return [0, 0]

        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        max_val = max(nums)
        last_depth = [-1] * (max_val + 1)

        depth = [0] * n
        dist = [0] * n
        start = [0] * n
        path = []

        best_len = 0
        best_nodes = 1

        # state 0 = enter, state 1 = exit
        # enter: (0, node, parent, weight_from_parent, _)
        # exit:  (1, node, _, _, prev_last_depth)
        stack = [(0, 0, -1, 0, 0)]

        while stack:
            state, node, parent, weight, prev_last = stack.pop()

            if state == 0:
                if parent == -1:
                    depth[node] = 0
                    dist[node] = 0
                    parent_start = 0
                else:
                    depth[node] = depth[parent] + 1
                    dist[node] = dist[parent] + weight
                    parent_start = start[parent]

                val = nums[node]
                prev = last_depth[val]

                # The highest valid ancestor depth for this endpoint.
                s = parent_start if parent_start >= prev + 1 else prev + 1
                start[node] = s

                path.append(node)

                length = dist[node] - dist[path[s]]
                nodes = depth[node] - s + 1

                if length > best_len:
                    best_len = length
                    best_nodes = nodes
                elif length == best_len and nodes < best_nodes:
                    best_nodes = nodes

                last_depth[val] = depth[node]

                stack.append((1, node, -1, 0, prev))

                for nei, w in adj[node]:
                    if nei != parent:
                        stack.append((0, nei, node, w, 0))
            else:
                val = nums[node]
                last_depth[val] = prev_last
                path.pop()

        return [best_len, best_nodes]

if __name__ == "__main__":
    sol = Solution()
    print(sol.longestSpecialPath(
        [[0, 1, 2], [1, 2, 3], [1, 3, 5], [1, 4, 4], [2, 5, 6]],
        [2, 1, 2, 1, 3, 1]
    ))
    print(sol.longestSpecialPath(
        [[1, 0, 8]],
        [2, 2]
    ))