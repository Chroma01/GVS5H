import itertools
import random


class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def minFlips(L: int) -> int:
            # Minimum flips so that the longest run of identical chars <= L.
            if L == 1:
                # String must alternate: compare against "0101..." and "1010..."
                mism0 = 0
                for i, ch in enumerate(s):
                    expected = '0' if i % 2 == 0 else '1'
                    if ch != expected:
                        mism0 += 1
                return min(mism0, n - mism0)

            # L >= 2: handle each maximal run independently.
            flips = 0
            i = 0
            while i < n:
                j = i
                while j < n and s[j] == s[i]:
                    j += 1
                run = j - i
                flips += run // (L + 1)
                i = j
            return flips

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if minFlips(mid) <= numOps:
                hi = mid
            else:
                lo = mid + 1
        return lo


def bruteForce(s: str, numOps: int) -> int:
    """Try every subset of up to numOps flip positions; return min achievable longest run."""
    n = len(s)
    best = n

    def longestRun(t: str) -> int:
        mx = cur = 1
        for k in range(1, len(t)):
            if t[k] == t[k - 1]:
                cur += 1
                mx = max(mx, cur)
            else:
                cur = 1
        return mx

    indices = range(n)
    for k in range(0, min(numOps, n) + 1):
        for combo in itertools.combinations(indices, k):
            t = list(s)
            for idx in combo:
                t[idx] = '1' if t[idx] == '0' else '0'
            best = min(best, longestRun(''.join(t)))
            if best == 1:
                return 1
    return best


def validate():
    sol = Solution()
    # Exhaustive: all binary strings up to length 9, all numOps values.
    for n in range(1, 10):
        for bits in itertools.product('01', repeat=n):
            s = ''.join(bits)
            for numOps in range(0, n + 1):
                got = sol.minLength(s, numOps)
                exp = bruteForce(s, numOps)
                assert got == exp, f"MISMATCH s={s} numOps={numOps}: got {got}, expected {exp}"
    # Random larger sanity checks against brute force on moderate n.
    rng = random.Random(12345)
    for _ in range(300):
        n = rng.randint(1, 12)
        s = ''.join(rng.choice('01') for _ in range(n))
        numOps = rng.randint(0, n)
        got = sol.minLength(s, numOps)
        exp = bruteForce(s, numOps)
        assert got == exp, f"MISMATCH s={s} numOps={numOps}: got {got}, expected {exp}"
    # Spot-check the tricky L=1 case.
    assert sol.minLength("0110", 2) == 1
    assert sol.minLength("0110", 1) == 2
    assert sol.minLength("000001", 1) == 2
    assert sol.minLength("0000", 2) == 1
    assert sol.minLength("0101", 0) == 1
    print("All validation tests passed.")


if __name__ == "__main__":
    validate()