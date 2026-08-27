from typing import List
import random


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        by_r = [[] for _ in range(n + 1)]
        m = len(conflictingPairs)

        for idx, (a, b) in enumerate(conflictingPairs):
            if a < b:
                l, r = a, b
            else:
                l, r = b, a
            by_r[r].append((l, idx))

        max1 = 0
        max2 = 0
        cnt1 = 0
        owner = -1
        base = 0
        gains = [0] * m

        for r in range(1, n + 1):
            for l, idx in by_r[r]:
                if l > max1:
                    max2 = max1
                    max1 = l
                    cnt1 = 1
                    owner = idx
                elif l == max1:
                    cnt1 += 1
                    owner = -1
                elif l > max2:
                    max2 = l

            base += r - max1
            if cnt1 == 1 and owner != -1:
                gains[owner] += max1 - max2

        return base + (max(gains) if m else 0)


def _count_valid_direct(n: int, pairs: List[List[int]]) -> int:
    total = 0
    for s in range(1, n + 1):
        for e in range(s, n + 1):
            ok = True
            for a, b in pairs:
                if s <= a <= e and s <= b <= e:
                    ok = False
                    break
            if ok:
                total += 1
    return total


def _brute_direct(n: int, pairs: List[List[int]]) -> int:
    if not pairs:
        return n * (n + 1) // 2

    best = 0
    for rem in range(len(pairs)):
        remaining = pairs[:rem] + pairs[rem + 1:]
        total = _count_valid_direct(n, remaining)
        if total > best:
            best = total
    return best


def _run_tests() -> bool:
    sol = Solution()
    try:
        if sol.maxSubarrays(4, [[2, 3], [1, 4]]) != 9:
            raise AssertionError("example 1 failed")
        if sol.maxSubarrays(5, [[1, 2], [2, 5], [3, 5]]) != 12:
            raise AssertionError("example 2 failed")
        if sol.maxSubarrays(2, [[1, 2]]) != 3:
            raise AssertionError("single pair n=2 failed")
        if sol.maxSubarrays(2, [[1, 2], [1, 2]]) != 2:
            raise AssertionError("duplicate pair n=2 failed")
        if sol.maxSubarrays(3, [[1, 3]]) != 6:
            raise AssertionError("single pair n=3 failed")
        if sol.maxSubarrays(3, [[1, 2], [2, 3]]) != 4:
            raise AssertionError("adjacent pairs n=3 failed")

        rng = random.Random(20240525)
        for _ in range(500):
            n = rng.randint(2, 6)
            m = rng.randint(1, 2 * n)
            pairs = []
            for _ in range(m):
                a = rng.randint(1, n)
                b = rng.randint(1, n)
                while b == a:
                    b = rng.randint(1, n)
                pairs.append([a, b])

            expected = _brute_direct(n, pairs)
            got = sol.maxSubarrays(n, pairs)
            if got != expected:
                raise AssertionError(f"n={n} pairs={pairs} expected={expected} got={got}")
    except AssertionError as exc:
        print(f"Assertion failed: {exc}")
        return False
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return False
    return True


if __name__ == "__main__":
    if _run_tests():
        print("SAMPLE TESTS: PASS")
    else:
        print("SAMPLE TESTS: FAIL")