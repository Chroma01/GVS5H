from typing import List
from itertools import combinations


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        n = len(nums)

        # coordinate compression
        comp = {}
        arr = [0] * n
        for i, v in enumerate(nums):
            j = comp.get(v, -1)
            if j < 0:
                j = len(comp)
                comp[v] = j
            arr[i] = j
        V = len(comp)

        cntL = [0] * V          # counts of nums[:p]
        cntR = [0] * V          # counts of nums[p+1:]
        for v in arr:
            cntR[v] += 1
        sumsqR = 0
        for c in cntR:
            sumsqR += c * c
        sumsqL = 0
        lenL = 0
        lenR = n

        def c2(m):
            return m * (m - 1) // 2 if m >= 2 else 0

        ans = 0
        for p in range(n):
            x = arr[p]
            # move the centre element out of R so R == nums[p+1:]
            c = cntR[x]
            sumsqR += 1 - 2 * c
            cntR[x] = c - 1
            lenR -= 1

            leftX = cntL[x]
            rightX = cntR[x]
            nonxL = lenL - leftX
            nonxR = lenR - rightX

            # ways to pick 2 elements from a side having exactly a copies of x
            wL0 = c2(nonxL)         # a = 0
            wL1 = leftX * nonxL     # a = 1
            wL2 = c2(leftX)         # a = 2
            wR0 = c2(nonxR)
            wR1 = rightX * nonxR
            wR2 = c2(rightX)

            # Case A: #x among the 4 side slots = a+b >= 2  => x freq >= 3 => always valid
            A = (wL0 * wR2 + wL1 * wR1 + wL1 * wR2
                 + wL2 * wR0 + wL2 * wR1 + wL2 * wR2)

            # distinct-valued pairs inside the non-x part of a side
            totalR = (lenR * lenR - sumsqR) // 2
            TR = totalR - rightX * (lenR - rightX)
            totalL = (lenL * lenL - sumsqL) // 2
            TL = totalL - leftX * (lenL - leftX)

            # Case B1: exactly one x, taken from the LEFT (a=1,b=0); x freq 2,
            # need the three non-x values pairwise distinct.
            B1 = 0
            if leftX:
                s = 0
                for v in range(V):
                    if v == x:
                        continue
                    cl = cntL[v]
                    if cl:
                        cr = cntR[v]
                        s += cl * (TR - cr * (nonxR - cr))
                B1 = leftX * s

            # Case B2: exactly one x, taken from the RIGHT (a=0,b=1)
            B2 = 0
            if rightX:
                s = 0
                for v in range(V):
                    if v == x:
                        continue
                    cr = cntR[v]
                    if cr:
                        cl = cntL[v]
                        s += cr * (TL - cl * (nonxL - cl))
                B2 = rightX * s

            ans = (ans + A + B1 + B2) % MOD

            # move the centre element into L so L == nums[:p+1]
            c = cntL[x]
            sumsqL += 2 * c + 1
            cntL[x] = c + 1
            lenL += 1

        return ans % MOD


# ---- brute-force verification harness (does not affect Solution) ----
def _brute(nums):
    from collections import Counter
    n = len(nums)
    total = 0
    for idx in combinations(range(n), 5):
        seq = [nums[i] for i in idx]
        c = Counter(seq)
        mx = max(c.values())
        modes = [v for v, f in c.items() if f == mx]
        if len(modes) == 1 and modes[0] == seq[2]:
            total += 1
    return total


if __name__ == "__main__":
    import random
    sol = Solution()
    ok = True

    examples = [
        ([1, 1, 1, 1, 1, 1], 6),
        ([1, 2, 2, 3, 3, 4], 4),
        ([0, 1, 2, 3, 4, 5, 6, 7, 8], 0),
    ]
    for arr, exp in examples:
        got = sol.subsequencesWithMiddleMode(arr)
        tag = "ok" if got == exp else "FAIL"
        ok = ok and got == exp
        print(f"example {arr} -> {got} (expected {exp}) {tag}")

    random.seed(12345)
    for _ in range(500):
        n = random.randint(5, 8)
        vals = random.randint(1, 4)
        arr = [random.randint(0, vals - 1) for _ in range(n)]
        got = sol.subsequencesWithMiddleMode(arr)
        bf = _brute(arr)
        if got != bf:
            ok = False
            print("MISMATCH", arr, "got", got, "brute", bf)

    print("SAMPLE TESTS:", "PASS" if ok else "FAIL")