from typing import List
from itertools import combinations
from collections import Counter
import random


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        n = len(nums)

        comp = {v: i for i, v in enumerate(sorted(set(nums)))}
        arr = [comp[v] for v in nums]
        V = len(comp)

        def C2(k):
            if k < 2:
                return 0
            return (k * (k - 1) // 2) % MOD

        a = [0] * V          # counts of indices 0..m-1
        b = [0] * V          # counts of indices m+1..n-1
        for j in range(1, n):
            b[arr[j]] += 1
        Lsize = 0
        Rsize = n - 1

        sumCb = 0
        for bv in b:
            sumCb += bv * (bv - 1) // 2
        P_L_full = 0
        P_R_full = (C2(Rsize) - sumCb) % MOD
        S_ab_full = 0
        Q1_full = 0
        Q2_full = 0

        ans = 0
        for m in range(n):
            L = m
            R = n - 1 - m
            if L >= 2 and R >= 2:
                x = arr[m]
                lx = a[x]
                rx = b[x]
                Ln = L - lx
                Rn = R - rx

                total = C2(L) * C2(R) % MOD
                C0 = C2(Ln) * C2(Rn) % MOD
                C1 = (lx * Ln % MOD * C2(Rn) + rx * Rn % MOD * C2(Ln)) % MOD

                PL = (P_L_full - lx * Ln) % MOD
                PR = (P_R_full - rx * Rn) % MOD
                Sab = (S_ab_full - lx * rx) % MOD
                Q1 = (Q1_full - lx * rx * rx) % MOD
                Q2 = (Q2_full - rx * lx * lx) % MOD

                A = lx * ((PR * Ln - Rn * Sab + Q1) % MOD) % MOD
                B = rx * ((PL * Rn - Ln * Sab + Q2) % MOD) % MOD

                contrib = (total - C0 - C1 + A + B) % MOD
                ans = (ans + contrib) % MOD

            if m + 1 < n:
                v = arr[m]
                av = a[v]
                P_L_full = (P_L_full + (Lsize - av)) % MOD
                S_ab_full = (S_ab_full + b[v]) % MOD
                Q1_full = (Q1_full + b[v] * b[v]) % MOD
                Q2_full = (Q2_full + b[v] * (2 * av + 1)) % MOD
                a[v] = av + 1
                Lsize += 1

                w = arr[m + 1]
                bw = b[w]
                P_R_full = (P_R_full - (Rsize - bw)) % MOD
                S_ab_full = (S_ab_full - a[w]) % MOD
                Q1_full = (Q1_full - a[w] * (2 * bw - 1)) % MOD
                Q2_full = (Q2_full - a[w] * a[w]) % MOD
                b[w] = bw - 1
                Rsize -= 1

        return ans % MOD


def brute(nums):
    n = len(nums)
    cnt = 0
    for idx in combinations(range(n), 5):
        c = Counter(nums[i] for i in idx)
        x = nums[idx[2]]
        mx = max(c.values())
        if c[x] == mx and sum(1 for v in c.values() if v == mx) == 1:
            cnt += 1
    return cnt


def main():
    sol = Solution()
    all_ok = True

    examples = [
        ([1, 1, 1, 1, 1, 1], 6),
        ([1, 2, 2, 3, 3, 4], 4),
        ([0, 1, 2, 3, 4, 5, 6, 7, 8], 0),
    ]
    for nums, exp in examples:
        got = sol.subsequencesWithMiddleMode(nums)
        ok = (got == exp)
        all_ok &= ok
        print(f"{'PASS' if ok else 'FAIL'} example {nums} expected={exp} got={got}")

    random.seed(20240607)
    state = {"all_ok": True, "first_fail": None, "tests": 0}

    def check(nums):
        exp = brute(nums)
        got = sol.subsequencesWithMiddleMode(list(nums))
        state["tests"] += 1
        if got != exp:
            state["all_ok"] = False
            if state["first_fail"] is None:
                state["first_fail"] = (list(nums), exp, got)
            print(f"MISMATCH nums={nums} expected={exp} got={got}")

    for _ in range(3000):
        n = random.randint(5, 10)
        k = min(random.choice([1, 2, 2, 3, 3, 4, 5]), n)
        check([random.randint(0, k - 1) for _ in range(n)])

    for _ in range(500):
        n = random.randint(11, 13)
        k = min(random.choice([2, 3, 4, 5, 7, n]), n)
        check([random.randint(0, k - 1) for _ in range(n)])

    for _ in range(40):
        n = random.randint(14, 17)
        k = min(random.choice([3, 4, 5, n]), n)
        check([random.randint(0, k - 1) for _ in range(n)])

    targeted = [
        [1] * 6, [1] * 7, [5] * 10,
        [1, 2, 3, 4, 5],
        [1, 1, 2, 2, 3],
        [1, 2, 2, 2, 3],
        [1, 2, 2, 2, 1],
        [1, 2, 3, 2, 1],
        [1, 1, 1, 2, 3],
        [1, 2, 1, 3, 1],
        [2, 5, 1, 3, 1, 4],
        [1, 2, 1, 2, 1, 2],
        [0, 5, 0, 5, 1, 0],
        [1, 1, 2, 2, 1, 1, 2, 2],
        [3, 3, 3, 1, 2, 3, 3],
    ]
    for nums in targeted:
        check(nums)

    all_ok &= state["all_ok"]
    print(f"total tests: {state['tests']}")
    if all_ok:
        print("RESULT: ALL TESTS PASSED")
    else:
        print(f"RESULT: FAIL first mismatch {state['first_fail']}")


if __name__ == "__main__":
    main()