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

        # last[value] = deepest depth on the current root-to-node path
        # where this value occurred.
        last = {}

        # dist_at_depth[d] = root distance of the ancestor at depth d
        # on the current DFS path.
        dist_at_depth = [0] * n

        best_len = -1
        best_nodes = 0
        left = 0

        # Stack entry:
        # (node, parent, depth, root_dist, state, prev_last, old_left)
        # state = 0 -> enter, state = 1 -> exit
        stack = [(0, -1, 0, 0, 0, -1, 0)]

        while stack:
            u, parent, depth, dist, state, prev_last, old_left = stack.pop()

            if state == 0:
                val = nums[u]

                prev_last = last.get(val, -1)
                old_left = left

                # If the same value is already inside the current unique window,
                # shrink the window to start just after its previous occurrence.
                if prev_last >= left:
                    left = prev_last + 1

                last[val] = depth
                dist_at_depth[depth] = dist

                cur_len = dist - dist_at_depth[left]
                cur_nodes = depth - left + 1

                if cur_len > best_len:
                    best_len = cur_len
                    best_nodes = cur_nodes
                elif cur_len == best_len and cur_nodes < best_nodes:
                    best_nodes = cur_nodes

                # Exit event must be processed after all children.
                stack.append((u, parent, depth, dist, 1, prev_last, old_left))

                for v, w in adj[u]:
                    if v != parent:
                        stack.append((v, u, depth + 1, dist + w, 0, -1, 0))

            else:
                val = nums[u]

                # Restore last occurrence state for this value.
                if prev_last == -1:
                    last.pop(val, None)
                else:
                    last[val] = prev_last

                # Restore window left boundary.
                left = old_left

        return [best_len, best_nodes]


def _run_tests() -> None:
    tests = [
        # Provided sample 1.
        (
            [[0, 1, 2], [1, 2, 3], [1, 3, 5], [1, 4, 4], [2, 5, 6]],
            [2, 1, 2, 1, 3, 1],
            [6, 2],
        ),
        # Provided sample 2.
        (
            [[1, 0, 8]],
            [2, 2],
            [0, 1],
        ),
        # Duplicate values on a chain.
        (
            [[0, 1, 1], [1, 2, 2], [2, 3, 3]],
            [1, 2, 1, 2],
            [3, 2],
        ),
        # All unique values on a chain.
        (
            [[0, 1, 5], [1, 2, 7], [2, 3, 10]],
            [1, 2, 3, 4],
            [22, 4],
        ),
        # Star-shaped tree, all unique.
        (
            [[0, 1, 4], [0, 2, 6], [0, 3, 5]],
            [1, 2, 3, 4],
            [6, 2],
        ),
        # Star-shaped tree, one child duplicates the root.
        (
            [[0, 1, 4], [0, 2, 6], [0, 3, 5]],
            [1, 1, 2, 3],
            [6, 2],
        ),
        # All values duplicate on a chain, only length-0 paths are valid.
        (
            [[0, 1, 10], [1, 2, 20]],
            [5, 5, 5],
            [0, 1],
        ),
        # Tie on length, choose fewer nodes.
        (
            [[0, 1, 10], [0, 2, 5], [2, 3, 5]],
            [0, 1, 2, 3],
            [10, 2],
        ),
        # Duplicate forces the window start to the current node, but another
        # longer unique path exists earlier.
        (
            [[0, 1, 100], [1, 2, 1], [2, 3, 1]],
            [1, 2, 3, 2],
            [101, 3],
        ),
        # Duplicate root and leaf creates two equal-length paths.
        (
            [[0, 1, 5], [1, 2, 5]],
            [1, 2, 1],
            [5, 2],
        ),
        # Sibling duplicate values must not contaminate each other.
        (
            [[0, 1, 10], [0, 2, 20]],
            [1, 2, 2],
            [20, 2],
        ),
        # Two-node unique edge.
        (
            [[0, 1, 7]],
            [1, 2],
            [7, 2],
        ),
        # Two-node duplicate edge.
        (
            [[0, 1, 7]],
            [1, 1],
            [0, 1],
        ),
        # Duplicate in the middle of a chain.
        (
            [[0, 1, 10], [1, 2, 20], [2, 3, 30]],
            [1, 2, 1, 3],
            [50, 3],
        ),
        # Duplicate occurrence outside the current window.
        (
            [[0, 1, 1], [1, 2, 100], [2, 3, 1], [3, 4, 100]],
            [1, 2, 1, 2, 3],
            [101, 3],
        ),
        # Single-node path.
        (
            [],
            [5],
            [0, 1],
        ),
    ]

    sol = Solution()
    failures = []

    for edges, nums, expected in tests:
        got = sol.longestSpecialPath(edges, nums)
        if got != expected:
            failures.append((edges, nums, expected, got))

    if failures:
        print("FAIL")
        for edges, nums, expected, got in failures:
            print(f"edges={edges} nums={nums} expected={expected} got={got}")
    else:
        print("PASS")


if __name__ == "__main__":
    _run_tests()