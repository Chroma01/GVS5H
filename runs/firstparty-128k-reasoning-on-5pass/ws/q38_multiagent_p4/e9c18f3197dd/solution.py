from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        # Remove duplicate targets and targets that divide another target.
        # If t divides u, any multiple of u is also a multiple of t.
        uniq = sorted(set(target))
        reduced = [t for t in uniq if not any(u % t == 0 for u in uniq if u != t)]

        m = len(reduced)
        if m == 0:
            return 0

        full = (1 << m) - 1
        size = 1 << m

        # Safe upper bound: assign each reduced target to a distinct nums element.
        upper = sum(reduced)
        INF = upper + 1

        # Exact LCM for every non-empty target subset.
        lcm = [0] * size
        for mask in range(1, size):
            lsb = mask & -mask
            idx = lsb.bit_length() - 1
            prev = mask ^ lsb
            if prev == 0:
                lcm[mask] = reduced[idx]
            else:
                a = lcm[prev]
                b = reduced[idx]
                lcm[mask] = (a // gcd(a, b)) * b

        # For each already-covered mask, precompute non-empty submasks of uncovered targets.
        submasks = [None] * size
        for mask in range(size):
            rem = full ^ mask
            subs = []
            sub = rem
            while sub:
                subs.append((sub, mask | sub))
                sub = (sub - 1) & rem
            submasks[mask] = tuple(subs)

        dp = [INF] * size
        dp[0] = 0

        # Cache costs by distinct nums value.
        cost_cache = {}

        for x in nums:
            costs = cost_cache.get(x)
            if costs is None:
                costs = [0] * size
                for mask in range(1, size):
                    # Cost to raise x to the next multiple of lcm[mask].
                    c = (-x) % lcm[mask]
                    if c > upper:
                        c = INF
                    costs[mask] = c
                cost_cache[x] = costs

            # Snapshot DP so this nums element is used at most once.
            new_dp = dp[:]
            for mask in range(size):
                base = dp[mask]
                if base >= INF:
                    continue

                for sub, next_mask in submasks[mask]:
                    c = costs[sub]
                    if c >= INF:
                        continue

                    val = base + c
                    if val < new_dp[next_mask]:
                        new_dp[next_mask] = val

            dp = new_dp

            # Zero is the global lower bound.
            if dp[full] == 0:
                return 0

        return dp[full]


def _run_tests() -> None:
    sol = Solution()
    tests = [
        ("example1", [1, 2, 3], [4], 1),
        ("example2", [8, 4], [10, 5], 2),
        ("example3", [7, 9, 10], [7], 0),
        ("target_one", [5, 7], [1], 0),
        ("target_one_with_others", [5, 5], [1, 2], 1),
        ("duplicate_targets", [3, 5], [4, 4], 1),
        ("divisor_targets", [3, 5], [2, 4], 1),
        ("divisor_targets_multi", [3, 5, 7], [2, 4, 5], 1),
        ("already_satisfied", [6, 10, 15], [2, 3, 5], 0),
        ("already_satisfied_single", [12, 1, 1], [3, 4, 6], 0),
        ("large_lcms", [1, 1, 1, 1], [9999, 10000, 9998, 9997], 39990),
        ("large_lcms_mixed", [10000, 1, 1, 1], [10000, 9999, 9998, 9997], 29991),
        ("multiple_increments", [1], [10000], 9999),
        ("multiple_increments_synergy", [29, 101], [6, 10], 1),
        ("multiple_increments_no_synergy", [1, 1], [6, 10], 14),
        ("synergy_4_6", [11, 100], [4, 6], 1),
        ("no_synergy_4_6", [1, 1], [4, 6], 8),
        ("mixed_4_6", [8, 9], [4, 6], 3),
        ("divisor_redundant_all", [5, 6, 8], [4, 6, 12], 4),
    ]

    for name, nums, target, expected in tests:
        actual = sol.minimumIncrements(nums, target)
        status = "ok" if actual == expected else "mismatch"
        print(f"{name}: actual={actual} expected={expected} {status}")


if __name__ == "__main__":
    _run_tests()