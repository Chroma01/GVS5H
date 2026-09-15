from typing import List


class Solution:
    def _prefix_depth_sum(self, n: int) -> int:
        """
        Returns sum_{x=1}^n d(x), where d(x) is the number of times
        x must be divided by 4 to become zero.
        """
        if n <= 0:
            return 0

        total = 0
        start = 1
        depth = 1

        # d(x) = depth for all x in [4^(depth-1), 4^depth - 1]
        while start <= n:
            end = min(n, start * 4 - 1)
            total += (end - start + 1) * depth
            start *= 4
            depth += 1

        return total

    def minOperations(self, queries: List[List[int]]) -> int:
        ans = 0
        prefix = self._prefix_depth_sum

        for l, r in queries:
            total_depth = prefix(r) - prefix(l - 1)
            ans += (total_depth + 1) // 2

        return ans


def _depth(x: int) -> int:
    """Independent helper used only by the validation harness."""
    d = 0
    while x > 0:
        x //= 4
        d += 1
    return d


def _general_optimal(depths: List[int]) -> int:
    """
    For an arbitrary multiset of remaining division counts, the true minimum
    number of operations is max(ceil(total / 2), max_depth).
    """
    if not depths:
        return 0
    total = sum(depths)
    mx = max(depths)
    return max((total + 1) // 2, mx)


def _run_validation() -> bool:
    """
    Optional validation harness. It is guarded by __name__ == "__main__",
    so normal judge execution of Solution is unaffected.
    """
    sol = Solution()
    ok = True

    def check(name: str, got: int, expected: int) -> None:
        nonlocal ok
        if got != expected:
            ok = False
            print(f"FAIL {name}: got {got}, expected {expected}")

    # Prefix helper sanity checks.
    check("prefix 0", sol._prefix_depth_sum(0), 0)
    for n in range(1, 300):
        expected = sum(_depth(x) for x in range(1, n + 1))
        check(f"prefix {n}", sol._prefix_depth_sum(n), expected)

    # Provided samples.
    check("sample 1", sol.minOperations([[1, 2], [2, 4]]), 3)
    check("sample 2", sol.minOperations([[2, 6]]), 4)

    # Odd total depths.
    check("odd total [1,3]", sol.minOperations([[1, 3]]), 2)
    check("odd total [1,4]", sol.minOperations([[1, 4]]), 3)
    check("odd crossing [3,4]", sol.minOperations([[3, 4]]), 2)

    # Ranges crossing powers of 4.
    check("cross 4", sol.minOperations([[3, 4]]), 2)
    check("cross 16", sol.minOperations([[15, 16]]), 3)
    check("cross 64", sol.minOperations([[63, 64]]), 4)
    check("cross 256", sol.minOperations([[255, 256]]), 5)
    check("after 16", sol.minOperations([[16, 17]]), 3)
    check("after 64", sol.minOperations([[64, 65]]), 4)

    # Large ranges and boundary cases.
    check("large [1,1e9]", sol.minOperations([[1, 10**9]]), 7321043037)
    check("large full depth14", sol.minOperations([[1, 268435455]]), 1834308950)
    check("large boundary", sol.minOperations([[268435455, 268435456]]), 15)
    check("large after boundary", sol.minOperations([[268435456, 268435457]]), 15)
    check("large top", sol.minOperations([[999999999, 1000000000]]), 15)

    # Many queries: exercises summation and the main loop.
    check("many small queries", sol.minOperations([[1, 2]] * 100000), 100000)

    # Exhaustive small-range validation against the general optimal formula.
    for l in range(1, 60):
        for r in range(l + 1, 60):
            depths = [_depth(x) for x in range(l, r + 1)]
            expected = _general_optimal(depths)
            got = sol.minOperations([[l, r]])
            if got != expected:
                ok = False
                print(f"FAIL small [{l},{r}]: got {got}, expected {expected}")

    print("PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _run_validation()