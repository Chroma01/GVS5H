from typing import List
from collections import defaultdict, Counter
import random
import time


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        NEG = -10**18

        total = 0
        mx = NEG
        neg_count = 0
        for v in nums:
            total += v
            if v > mx:
                mx = v
            if v < 0:
                neg_count += 1

        if neg_count == 0:
            return total
        if mx <= 0:
            return mx

        size = 1 << (n - 1).bit_length()
        sm = [0] * (2 * size)
        pf = [NEG] * (2 * size)
        sf = [NEG] * (2 * size)
        bs = [NEG] * (2 * size)
        groups = defaultdict(list)

        for i, v in enumerate(nums):
            p = size + i
            sm[p] = v
            pf[p] = v
            sf[p] = v
            bs[p] = v
            if v < 0:
                groups[v].append(i)

        for p in range(size - 1, 0, -1):
            l = p << 1
            r = l + 1
            lsm = sm[l]
            rsm = sm[r]
            sm[p] = lsm + rsm

            a = pf[l]
            b = lsm + pf[r]
            if a < b:
                a = b
            pf[p] = a

            a = sf[r]
            b = rsm + sf[l]
            if a < b:
                a = b
            sf[p] = a

            a = bs[l]
            b = bs[r]
            if a < b:
                a = b
            c = sf[l] + pf[r]
            if c > a:
                a = c
            bs[p] = a

        ans = bs[1]

        def set_pos(i, v, sm=sm, pf=pf, sf=sf, bs=bs, size=size, NEG=NEG):
            p = size + i
            if v is None:
                sm[p] = 0
                pf[p] = NEG
                sf[p] = NEG
                bs[p] = NEG
            else:
                sm[p] = v
                pf[p] = v
                sf[p] = v
                bs[p] = v
            p >>= 1
            while p:
                l = p << 1
                r = l + 1
                lsm = sm[l]
                rsm = sm[r]
                sm[p] = lsm + rsm

                a = pf[l]
                b = lsm + pf[r]
                if a < b:
                    a = b
                pf[p] = a

                a = sf[r]
                b = rsm + sf[l]
                if a < b:
                    a = b
                sf[p] = a

                a = bs[l]
                b = bs[r]
                if a < b:
                    a = b
                c = sf[l] + pf[r]
                if c > a:
                    a = c
                bs[p] = a
                p >>= 1

        for x, idxs in groups.items():
            if len(idxs) < n:
                for i in idxs:
                    set_pos(i, None)
                if bs[1] > ans:
                    ans = bs[1]
                for i in idxs:
                    set_pos(i, x)

        return ans


def kadane(a: List[int]) -> int:
    best = cur = a[0]
    for v in a[1:]:
        if cur + v < v:
            cur = v
        else:
            cur += v
        if cur > best:
            best = cur
    return best


def brute_force(nums: List[int]) -> int:
    n = len(nums)
    ans = kadane(nums)
    cnt = Counter(nums)
    for x in cnt:
        if cnt[x] == n:
            continue
        arr = [v for v in nums if v != x]
        val = kadane(arr)
        if val > ans:
            ans = val
    return ans


def run_tests() -> None:
    sol = Solution()
    failures = []

    def check(nums: List[int], label: str, verbose: bool = False) -> None:
        expected = brute_force(nums)
        actual = sol.maxSubarraySum(nums)
        if expected != actual:
            failures.append(f"{label}: nums={nums} expected={expected} actual={actual}")
            print(f"FAIL {label}: nums={nums} expected={expected} actual={actual}")
        elif verbose:
            print(f"PASS {label}: {actual}")

    check([-3, 2, -2, -1, 3, -2, 3], "example1", verbose=True)
    check([1, 2, 3, 4], "example2", verbose=True)

    targeted = [
        [-1], [0], [5],
        [-1, -1], [0, 0], [2, 2],
        [-1, -2, -3], [0, -1, 0], [1, -1, 1],
        [-1, 2, -1, 2, -1], [1, -2, 1, -2, 1],
        [-1, -1, -1, 2, 2, -1, -1],
        [1, 1, -2, -2, -2, 1, 1],
        [-5, 1, -5, 1, -5],
        [3, -1, -1, 3],
        [2, -3, 2, -3, 2],
        [0, -1, 1, -1, 0],
    ]
    for i, nums in enumerate(targeted):
        check(nums, f"targeted{i}")

    rng = random.Random(2024)
    for t in range(3000):
        n = rng.randint(1, 8)
        cat = rng.randrange(5)
        if cat == 0:
            nums = [rng.randint(-5, -1) for _ in range(n)]
        elif cat == 1:
            v = rng.randint(-3, 3)
            nums = [v] * n
        elif cat == 2:
            nums = [rng.randint(-1, 1) for _ in range(n)]
        elif cat == 3:
            nums = [rng.randint(-3, 3) for _ in range(n)]
        else:
            nums = []
            rem = n
            while rem > 0:
                v = rng.randint(-3, 3)
                k = min(rem, rng.randint(1, 3))
                nums.extend([v] * k)
                rem -= k
        check(nums, f"random{t}")

    n = 100000
    nums = [1] + [-(i + 1) for i in range(n - 1)]
    start = time.perf_counter()
    res = sol.maxSubarraySum(nums)
    elapsed = time.perf_counter() - start
    lower = max(nums)
    upper = sum(v for v in nums if v > 0)
    if lower <= res <= upper and elapsed < 10.0:
        print(f"PASS performance: n={n} time={elapsed:.3f}s result={res}")
    else:
        failures.append(f"performance: n={n} time={elapsed:.3f}s result={res} lower={lower} upper={upper}")
        print(f"FAIL performance: n={n} time={elapsed:.3f}s result={res} lower={lower} upper={upper}")

    if failures:
        print(f"RESULT: FAIL ({len(failures)} failures)")
    else:
        print("RESULT: PASS")


if __name__ == "__main__":
    run_tests()