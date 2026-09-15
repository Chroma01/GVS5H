from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        if n <= 0 or k < 1:
            return []

        # Any count larger than this is guaranteed to be >= every possible k.
        CAP = 10**15 + 1

        def cap_mul(a: int, b: int) -> int:
            if a == 0 or b == 0:
                return 0
            if a >= CAP or b >= CAP:
                return CAP
            if a > CAP // b:
                return CAP
            return a * b

        def cap_add(a: int, b: int) -> int:
            s = a + b
            return CAP if s >= CAP else s

        odd_count = (n + 1) // 2
        even_count = n // 2

        if abs(odd_count - even_count) > 1:
            return []

        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = cap_mul(fact[i - 1], i)

        # Total number of valid alternating permutations, capped.
        total = cap_mul(fact[odd_count], fact[even_count])
        if odd_count == even_count:
            total = cap_add(total, total)

        if total < k:
            return []

        def completions(ro: int, re: int, next_parity: int) -> int:
            """
            Count valid suffixes using ro remaining odd numbers and re remaining
            even numbers, where the next position must have parity next_parity.
            Parity is represented as 1 for odd and 0 for even.
            """
            m = ro + re
            if m == 0:
                return 1

            need_next = (m + 1) // 2
            need_other = m // 2

            if next_parity == 1:  # next position must be odd
                if ro != need_next or re != need_other:
                    return 0
            else:                 # next position must be even
                if re != need_next or ro != need_other:
                    return 0

            return cap_mul(fact[ro], fact[re])

        ans = []
        used = [False] * (n + 1)
        rem_odd = odd_count
        rem_even = even_count
        prev_parity = None

        for _ in range(n):
            chosen = False

            # Try candidates in lexicographic order.
            for x in range(1, n + 1):
                if used[x]:
                    continue

                p = x & 1
                if prev_parity is not None and p == prev_parity:
                    continue

                ro = rem_odd - (1 if p == 1 else 0)
                re = rem_even - (1 if p == 0 else 0)

                cnt = completions(ro, re, 1 - p)

                if cnt >= k:
                    ans.append(x)
                    used[x] = True

                    if p == 1:
                        rem_odd -= 1
                    else:
                        rem_even -= 1

                    prev_parity = p
                    chosen = True
                    break

                k -= cnt

            if not chosen:
                return []

        return ans


def _verify() -> None:
    from itertools import permutations

    sol = Solution()

    # Given samples.
    assert sol.permute(4, 6) == [3, 4, 1, 2]
    assert sol.permute(3, 2) == [3, 2, 1]
    assert sol.permute(2, 3) == []

    # Edge cases.
    assert sol.permute(1, 1) == [1]
    assert sol.permute(1, 2) == []
    assert sol.permute(2, 1) == [1, 2]
    assert sol.permute(2, 2) == [2, 1]
    assert sol.permute(2, 3) == []
    assert sol.permute(3, 1) == [1, 2, 3]
    assert sol.permute(3, 3) == []
    assert sol.permute(4, 1) == [1, 2, 3, 4]
    assert sol.permute(4, 8) == [4, 3, 2, 1]
    assert sol.permute(5, 1) == [1, 2, 3, 4, 5]
    assert sol.permute(5, 12) == [5, 4, 3, 2, 1]
    assert sol.permute(5, 13) == []
    assert sol.permute(0, 1) == []
    assert sol.permute(3, 10**15) == []

    # Large-n sanity checks.
    assert sol.permute(100, 1) == list(range(1, 101))
    assert len(sol.permute(100, 10**15)) == 100

    # Exhaustive verification for small n.
    for small_n in range(1, 7):
        valid = []
        for p in permutations(range(1, small_n + 1)):
            ok = True
            for i in range(small_n - 1):
                if (p[i] & 1) == (p[i + 1] & 1):
                    ok = False
                    break
            if ok:
                valid.append(p)

        valid.sort()

        for idx, expected in enumerate(valid, 1):
            assert sol.permute(small_n, idx) == list(expected)

        assert sol.permute(small_n, len(valid) + 1) == []


if __name__ == "__main__":
    _verify()