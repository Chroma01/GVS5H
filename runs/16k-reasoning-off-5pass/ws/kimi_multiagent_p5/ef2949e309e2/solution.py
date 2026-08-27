from typing import List
from collections import Counter

MOD = 10**9 + 7


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0

        # right frequency map: initially everything except index 0
        right = Counter(nums[1:])
        # sumC2 = sum over values x of C(right[x], 2), maintained incrementally
        sumC2 = 0
        for c in right.values():
            sumC2 += c * (c - 1) // 2

        def c2(k: int) -> int:
            return k * (k - 1) // 2

        for i in range(n):
            v = nums[i]
            # move nums[i] out of the right side (it becomes the middle)
            if right[v] > 0:
                sumC2 -= c2(right[v])
                right[v] -= 1
                sumC2 += c2(right[v])
                if right[v] == 0:
                    del right[v]

            m = n - i - 1  # number of elements on the right
            if m >= 2 and i >= 2:
                cntV = right.get(v, 0)
                bothV = c2(cntV)                      # right pairs (v, v)
                oneV = cntV * (m - cntV)              # right pairs (v, x), x != v
                nonV = m - cntV                       # non-v elements on right
                # sum over x != v of C(f[x], 2)
                sumC2_notV = sumC2 - c2(cntV)
                totalRightPairs = c2(m)

                # enumerate left pairs (a, b), a < b < i
                for b in range(i):
                    y = nums[b]
                    for a in range(b):
                        x = nums[a]
                        if x == v and y == v:
                            # lv = 2: every right pair works
                            ans += totalRightPairs
                        elif x == v or y == v:
                            # lv = 1, other left value is w != v
                            w = y if x == v else x
                            fw = right.get(w, 0)
                            # valid: both v; one v one anything;
                            # two distinct non-v values, neither equal to w
                            pairs_with_w = c2(fw) + fw * (nonV - fw)
                            same_notV_notW = sumC2_notV - c2(fw)
                            valid = (bothV + oneV
                                     + c2(nonV) - pairs_with_w
                                     - same_notV_notW)
                            ans += valid
                        elif x == y:
                            # lv = 0, both left equal w != v: only (v, v) works
                            ans += bothV
                        else:
                            # lv = 0, left values y1 != y2, both != v
                            fy1 = right.get(x, 0)
                            fy2 = right.get(y, 0)
                            ans += bothV + cntV * (nonV - fy1 - fy2)
                        ans %= MOD

        return ans % MOD


# ---------------- verification harness ----------------
def brute_force(nums: List[int]) -> int:
    from itertools import combinations
    n = len(nums)
    total = 0
    for idxs in combinations(range(n), 5):
        seq = [nums[j] for j in idxs]
        mid = seq[2]
        cnt = Counter(seq)
        maxc = max(cnt.values())
        if cnt[mid] == maxc and list(cnt.values()).count(maxc) == 1:
            total += 1
    return total % MOD


if __name__ == "__main__":
    import random

    sol = Solution()

    # given examples
    examples = [
        ([1, 1, 1, 1, 1, 1], 6),
        ([1, 2, 2, 3, 3, 4], 4),
        ([0, 1, 2, 3, 4, 5, 6, 7, 8], 0),
    ]
    for arr, exp in examples:
        got = sol.subsequencesWithMiddleMode(arr)
        bf = brute_force(arr)
        assert got == exp == bf, (arr, got, exp, bf)
    print("examples OK")

    # random small arrays, exhaustive check
    random.seed(12345)
    for trial in range(3000):
        n = random.randint(5, 8)
        # small value pool to force many collisions / ties
        arr = [random.randint(0, 3) for _ in range(n)]
        got = sol.subsequencesWithMiddleMode(arr)
        exp = brute_force(arr)
        assert got == exp, (arr, got, exp)
    print("random small-pool OK")

    # random arrays with larger values (fewer collisions)
    for trial in range(2000):
        n = random.randint(5, 8)
        arr = [random.randint(-10**9, 10**9) for _ in range(n)]
        got = sol.subsequencesWithMiddleMode(arr)
        exp = brute_force(arr)
        assert got == exp, (arr, got, exp)
    print("random large-pool OK")

    # structured edge patterns
    edge_cases = [
        [5] * 5,
        [5] * 8,
        [1, 1, 2, 2, 1],
        [2, 2, 1, 1, 1, 2, 2],
        [1, 2, 1, 2, 1, 2, 1, 2],
        [0, 0, 0, 1, 0, 0, 0, 1],
        [3, 1, 3, 1, 3, 1, 3, 1],
    ]
    for arr in edge_cases:
        got = sol.subsequencesWithMiddleMode(arr)
        exp = brute_force(arr)
        assert got == exp, (arr, got, exp)
    print("edge patterns OK")

    print("ALL TESTS PASSED")