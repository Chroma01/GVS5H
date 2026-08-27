from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        if n == 0:
            return [0, 1]

        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        max_val = max(nums)
        last_depth = [-1] * (max_val + 1)
        path_dist = []
        best_len = 0
        best_nodes = 1

        # Enter event: (0, node, parent, depth, dist, parent_start)
        # Exit event:  (1, node, previous_last_depth_for_node_value)
        stack = [(0, 0, -1, 0, 0, 0)]

        while stack:
            item = stack.pop()

            if item[0] == 0:
                _, node, parent, depth, dist, parent_start = item
                val = nums[node]
                prev = last_depth[val]

                if node == 0:
                    start = 0
                elif prev >= parent_start:
                    start = prev + 1
                else:
                    start = parent_start

                path_dist.append(dist)

                cand_len = dist - path_dist[start]
                cand_nodes = depth - start + 1

                if cand_len > best_len:
                    best_len = cand_len
                    best_nodes = cand_nodes
                elif cand_len == best_len and cand_nodes < best_nodes:
                    best_nodes = cand_nodes

                last_depth[val] = depth
                stack.append((1, node, prev))

                for nxt, w in adj[node]:
                    if nxt != parent:
                        stack.append((0, nxt, node, depth + 1, dist + w, start))
            else:
                _, node, prev = item
                val = nums[node]
                last_depth[val] = prev
                path_dist.pop()

        return [best_len, best_nodes]


def _run_sample_tests() -> None:
    tests = [
        ("example1",
         [[0, 1, 2], [1, 2, 3], [1, 3, 5], [1, 4, 4], [2, 5, 6]],
         [2, 1, 2, 1, 3, 1],
         [6, 2]),
        ("example2",
         [[1, 0, 8]],
         [2, 2],
         [0, 1]),
        ("all_duplicates_chain",
         [[0, 1, 1], [1, 2, 1]],
         [1, 1, 1],
         [0, 1]),
        ("chain_unique",
         [[0, 1, 1], [1, 2, 1]],
         [1, 2, 3],
         [2, 3]),
        ("star_unique",
         [[0, 1, 1], [0, 2, 2], [0, 3, 3]],
         [0, 1, 2, 3],
         [3, 2]),
        ("star_root_duplicate",
         [[0, 1, 5], [0, 2, 4], [0, 3, 3]],
         [1, 1, 2, 3],
         [4, 2]),
        ("n2_unique",
         [[0, 1, 7]],
         [1, 2],
         [7, 2]),
        ("n2_duplicate",
         [[0, 1, 7]],
         [1, 1],
         [0, 1]),
        ("tie_two_vs_three_nodes",
         [[0, 1, 5], [0, 2, 2], [2, 3, 3]],
         [0, 1, 2, 3],
         [5, 2]),
        ("edge_weights_tie_min_nodes",
         [[0, 1, 10], [0, 2, 4], [2, 3, 6]],
         [0, 1, 2, 3],
         [10, 2]),
        ("blocker_prev_below_parent_start",
         [[0, 1, 1], [1, 2, 1], [2, 3, 1]],
         [1, 2, 2, 1],
         [1, 2]),
        ("root_value_reappears_deep",
         [[0, 1, 1], [1, 2, 1], [2, 3, 1]],
         [1, 2, 3, 1],
         [2, 3]),
        ("star_duplicate_children",
         [[0, 1, 1], [0, 2, 2], [0, 3, 3]],
         [0, 1, 1, 1],
         [3, 2]),
        ("all_same_star",
         [[0, 1, 1], [0, 2, 2], [0, 3, 3]],
         [1, 1, 1, 1],
         [0, 1]),
        ("single_node",
         [],
         [5],
         [0, 1]),
    ]

    sol = Solution()
    failures = []

    for name, edges, nums, expected in tests:
        got = sol.longestSpecialPath(edges, nums)
        if got != expected:
            failures.append(f"{name}: expected {expected}, got {got}")

    if failures:
        print("SAMPLE TESTS: FAIL")
        for failure in failures:
            print(failure)
    else:
        print("SAMPLE TESTS: PASS")


if __name__ == "__main__":
    _run_sample_tests()