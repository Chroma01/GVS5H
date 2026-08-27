from typing import List
from itertools import permutations
import math
import random


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        CAP = 10 ** 18

        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            if fact[i - 1] > CAP // i:
                fact[i] = CAP
            else:
                fact[i] = fact[i - 1] * i

        def cap_mul(a: int, b: int) -> int:
            if a == 0 or b == 0:
                return 0
            if a >= CAP or b >= CAP:
                return CAP
            if a > CAP // b:
                return CAP
            return a * b

        odd_count = (n + 1) // 2
        even_count = n // 2

        total = cap_mul(fact[odd_count], fact[even_count])
        if n % 2 == 0:
            total = cap_mul(total, 2)

        if total < k:
            return []

        used = [False] * (n + 1)
        rem_odd = odd_count
        rem_even = even_count
        ans = []
        prev_parity = -1

        for pos in range(n):
            future_len = n - pos - 1
            chosen = False

            for x in range(1, n + 1):
                if used[x]:
                    continue

                p = x & 1
                if prev_parity != -1 and p == prev_parity:
                    continue

                if p:
                    no = rem_odd - 1
                    ne = rem_even
                else:
                    no = rem_odd
                    ne = rem_even - 1

                if no < 0 or ne < 0:
                    continue

                req_next = 1 - p
                if req_next:
                    need_odd = (future_len + 1) // 2
                else:
                    need_odd = future_len // 2
                need_even = future_len - need_odd

                if no == need_odd and ne == need_even:
                    block = cap_mul(fact[no], fact[ne])

                    if k > block:
                        k -= block
                    else:
                        ans.append(x)
                        used[x] = True
                        rem_odd = no
                        rem_even = ne
                        prev_parity = p
                        chosen = True
                        break

            if not chosen:
                return []

        return ans


def _brute_alternating(n: int) -> List[List[int]]:
    res = []
    for perm in permutations(range(1, n + 1)):
        ok = True
        for i in range(n - 1):
            if (perm[i] & 1) == (perm[i + 1] & 1):
                ok = False
                break
        if ok:
            res.append(list(perm))
    res.sort()
    return res


def _is_valid(perm: List[int], n: int) -> bool:
    if len(perm) != n:
        return False
    if sorted(perm) != list(range(1, n + 1)):
        return False
    for i in range(n - 1):
        if (perm[i] & 1) == (perm[i + 1] & 1):
            return False
    return True


def _rank(perm: List[int], n: int) -> int:
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i

    used = [False] * (n + 1)
    rem_odd = (n + 1) // 2
    rem_even = n // 2
    rank = 1
    prev_parity = -1

    for pos, x in enumerate(perm):
        future_len = n - pos - 1

        for cand in range(1, x):
            if used[cand]:
                continue

            cp = cand & 1
            if prev_parity != -1 and cp == prev_parity:
                continue

            if cp:
                no = rem_odd - 1
                ne = rem_even
            else:
                no = rem_odd
                ne = rem_even - 1

            if no < 0 or ne < 0:
                continue

            req_next = 1 - cp
            if req_next:
                need_odd = (future_len + 1) // 2
            else:
                need_odd = future_len // 2
            need_even = future_len - need_odd

            if no == need_odd and ne == need_even:
                rank += fact[no] * fact[ne]

        if x & 1:
            rem_odd -= 1
        else:
            rem_even -= 1
        used[x] = True
        prev_parity = x & 1

    return rank


def _fail(msg: str) -> None:
    raise RuntimeError(msg)


def _run_verification() -> None:
    sol = Solution()

    examples = [
        (4, 6, [3, 4, 1, 2]),
        (3, 2, [3, 2, 1]),
        (2, 3, []),
    ]
    for n, k, expected in examples:
        got = sol.permute(n, k)
        if got != expected:
            _fail(f"example n={n} k={k}: got {got}, expected {expected}")

    # Brute-force check for small n. Testing every k from 1 to total+1
    # includes k=1, k=total, k=total+1, and all block-boundary values.
    for n in range(1, 9):
        expected = _brute_alternating(n)
        total = len(expected)
        for k in range(1, total + 2):
            got = sol.permute(n, k)
            if k <= total:
                if got != expected[k - 1]:
                    _fail(f"brute n={n} k={k}: got {got}, expected {expected[k - 1]}")
            else:
                if got != []:
                    _fail(f"brute n={n} k={k}: expected [], got {got}")

    # Independent rank-based sanity checks for slightly larger n.
    rng = random.Random(12345)
    for n in range(1, 13):
        odd = (n + 1) // 2
        even = n // 2
        total = math.factorial(odd) * math.factorial(even)
        if n % 2 == 0:
            total *= 2

        limit = min(total, 10 ** 15)
        test_ks = {1, limit, limit + 1, total, total + 1}
        for _ in range(25):
            test_ks.add(rng.randint(1, limit))

        for k in sorted(test_ks):
            got = sol.permute(n, k)
            if k <= total:
                if not _is_valid(got, n):
                    _fail(f"rank n={n} k={k}: invalid permutation {got}")
                r = _rank(got, n)
                if r != k:
                    _fail(f"rank n={n} k={k}: computed rank {r}, expected {k}")
            else:
                if got != []:
                    _fail(f"rank n={n} k={k}: expected [], got {got}")

    print("verification passed")


if __name__ == "__main__":
    _run_verification()