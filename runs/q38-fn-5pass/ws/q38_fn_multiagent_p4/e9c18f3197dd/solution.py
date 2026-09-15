from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        if not target or not nums:
            return 0

        # Deduplicate and remove redundant targets.
        # If t divides u, satisfying u automatically satisfies t.
        uniq = sorted(set(target))
        targets = []
        for i, t in enumerate(uniq):
            redundant = False
            for j, u in enumerate(uniq):
                if i != j and u % t == 0:
                    redundant = True
                    break
            if not redundant:
                targets.append(t)

        k = len(targets)
        if k == 0:
            return 0

        # Only one effective target remains.
        if k == 1:
            t = targets[0]
            if t == 1:
                return 0
            best = t - 1
            for x in nums:
                r = x % t
                c = 0 if r == 0 else t - r
                if c < best:
                    best = c
                    if best == 0:
                        return 0
            return best

        m = 1 << k
        full = m - 1

        # Assigning each reduced target to a distinct nums element gives
        # cost <= sum(t - 1), so this INF is strictly above the optimum.
        INF = sum(t - 1 for t in targets) + 1

        # Count values and cap each value's usable copies at k.
        # At most k elements are ever needed.
        counts = {}
        for x in nums:
            counts[x] = counts.get(x, 0) + 1

        max_val = max(counts.keys())
        LIMIT = max_val + INF - 1

        # LCM for every target subset. If LCM > LIMIT, no element can cover
        # that subset with cost < INF.
        lcms = [1] * m
        mask_valid = [False] * m

        for mask in range(1, m):
            lsb = mask & -mask
            idx = lsb.bit_length() - 1
            prev = mask ^ lsb

            a = lcms[prev]
            b = targets[idx]

            if a > LIMIT:
                lcms[mask] = LIMIT + 1
            else:
                g = gcd(a, b)
                a_div = a // g
                if a_div > LIMIT // b:
                    lcms[mask] = LIMIT + 1
                else:
                    lcms[mask] = a_div * b

            if lcms[mask] <= LIMIT:
                mask_valid[mask] = True

        valid_masks = [mask for mask in range(1, m) if mask_valid[mask]]

        # Precompute increment costs for each distinct nums value.
        value_costs = {}
        for v in counts:
            row = [INF] * m
            for mask in valid_masks:
                L = lcms[mask]
                r = v % L
                c = 0 if r == 0 else L - r
                if c < INF:
                    row[mask] = c
            value_costs[v] = row

        # Build the reduced list of elements to process.
        limited_nums = []
        for v, c in counts.items():
            if c > k:
                c = k
            limited_nums.extend([v] * c)

        # Precompute transitions: from old mask, choose a nonempty submask
        # of currently uncovered targets.
        trans = [[] for _ in range(m)]
        for old in range(m):
            rem = full ^ old
            sub = rem
            while sub:
                if mask_valid[sub]:
                    trans[old].append((sub, old | sub))
                sub = (sub - 1) & rem

        # dp[mask] = minimum cost after processed elements.
        dp = [INF] * m
        dp[0] = 0

        for x in limited_nums:
            costs = value_costs[x]
            new = dp[:]  # not using this element

            for old, base in enumerate(dp):
                if base == INF:
                    continue

                for sub, nm in trans[old]:
                    c = costs[sub]
                    if c != INF:
                        val = base + c
                        if val < new[nm]:
                            new[nm] = val

            dp = new

            if dp[full] == 0:
                return 0

        return dp[full]


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([1, 2, 3], [4], 1),
        ([8, 4], [10, 5], 2),
        ([7, 9, 10], [7], 0),
        ([1], [1], 0),
        ([1], [2], 1),
        ([2, 3], [2, 3], 0),
        ([1, 2], [2, 3], 2),
        ([5, 5], [2, 3], 1),
        ([5, 5], [2, 5], 1),
        ([1, 1, 1], [2, 3, 5], 7),
        ([5, 5, 5], [2, 3, 5], 1),
        ([10000, 1], [9999, 10000], 9998),
        ([2, 4], [3, 4], 1),
        ([1, 1, 1], [6, 10, 15], 28),
        ([5, 5, 5], [6, 10, 15], 16),
        ([1, 1, 1, 1], [2, 3, 5, 7], 13),
        ([5, 5, 5, 5], [2, 3, 5, 7], 3),
        ([1, 2, 3], [1, 2, 3], 0),
        ([1, 1], [1, 2], 1),
        ([1, 2, 3], [2, 4, 8], 5),
        ([1, 5, 5], [6, 10, 15], 20),
        ([13, 13], [4, 6], 8),
        ([11, 11], [4, 6], 1),
        ([1, 2, 3], [2, 2], 0),
    ]

    failures = []
    for nums, target, expected in tests:
        actual = sol.minimumIncrements(nums, target)
        if actual != expected:
            failures.append((len(nums) + len(target), nums, target, expected, actual))

    if not failures:
        print("PASS")
    else:
        failures.sort(key=lambda item: (item[0], item[1], item[2]))
        _, nums, target, expected, actual = failures[0]
        print(f"FAIL nums={nums} target={target} expected={expected} actual={actual}")