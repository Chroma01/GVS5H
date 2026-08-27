from typing import List
import itertools


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        if k < 1:
            return []

        CAP = 10**15 + 1

        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(CAP, fact[i - 1] * i)

        def count_suffix(rem_odd: int, rem_even: int, next_parity: int) -> int:
            m = rem_odd + rem_even
            if m == 0:
                return 1

            if next_parity == 1:
                req_odd = (m + 1) // 2
                req_even = m // 2
            else:
                req_odd = m // 2
                req_even = (m + 1) // 2

            if req_odd != rem_odd or req_even != rem_even:
                return 0

            return min(CAP, fact[rem_odd] * fact[rem_even])

        total_odd = (n + 1) // 2
        total_even = n // 2

        total = 0
        for x in range(1, n + 1):
            p = x & 1
            if p:
                ro = total_odd - 1
                re = total_even
            else:
                ro = total_odd
                re = total_even - 1

            if ro < 0 or re < 0:
                continue

            total += count_suffix(ro, re, 1 - p)
            if total >= CAP:
                total = CAP
                break

        if k > total:
            return []

        used = [False] * (n + 1)
        used_odd = 0
        used_even = 0
        ans = []

        for pos in range(n):
            chosen = None
            required_parity = None if pos == 0 else 1 - (ans[-1] & 1)

            for x in range(1, n + 1):
                if used[x]:
                    continue

                p = x & 1
                if required_parity is not None and p != required_parity:
                    continue

                if p:
                    ro = total_odd - used_odd - 1
                    re = total_even - used_even
                else:
                    ro = total_odd - used_odd
                    re = total_even - used_even - 1

                if ro < 0 or re < 0:
                    continue

                block = count_suffix(ro, re, 1 - p)
                if block == 0:
                    continue

                if k > block:
                    k -= block
                else:
                    chosen = x
                    break

            if chosen is None:
                return []

            ans.append(chosen)
            used[chosen] = True
            if chosen & 1:
                used_odd += 1
            else:
                used_even += 1

        return ans


def is_alternating(perm: List[int]) -> bool:
    return all((perm[i] & 1) != (perm[i + 1] & 1) for i in range(len(perm) - 1))


def is_permutation(perm: List[int], n: int) -> bool:
    return len(perm) == n and sorted(perm) == list(range(1, n + 1))


def brute_alternating(n: int) -> List[List[int]]:
    res = []
    for perm in itertools.permutations(range(1, n + 1)):
        if all((perm[i] & 1) != (perm[i + 1] & 1) for i in range(n - 1)):
            res.append(list(perm))
    return res


def rank_alternating(perm: List[int], n: int) -> int:
    if not is_permutation(perm, n) or not is_alternating(perm):
        raise ValueError("rank_alternating requires a valid alternating permutation")

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i

    def count_suffix(rem_odd: int, rem_even: int, next_parity: int) -> int:
        m = rem_odd + rem_even
        if m == 0:
            return 1

        if next_parity == 1:
            req_odd = (m + 1) // 2
            req_even = m // 2
        else:
            req_odd = m // 2
            req_even = (m + 1) // 2

        if req_odd != rem_odd or req_even != rem_even:
            return 0

        return fact[rem_odd] * fact[rem_even]

    total_odd = (n + 1) // 2
    total_even = n // 2

    used = [False] * (n + 1)
    used_odd = 0
    used_even = 0
    rank = 1

    for i, val in enumerate(perm):
        required_parity = None if i == 0 else 1 - (perm[i - 1] & 1)

        for x in range(1, val):
            if used[x]:
                continue

            p = x & 1
            if required_parity is not None and p != required_parity:
                continue

            if p:
                ro = total_odd - used_odd - 1
                re = total_even - used_even
            else:
                ro = total_odd - used_odd
                re = total_even - used_even - 1

            if ro < 0 or re < 0:
                continue

            rank += count_suffix(ro, re, 1 - p)

        if required_parity is not None and (val & 1) != required_parity:
            raise ValueError("invalid parity in rank")

        used[val] = True
        if val & 1:
            used_odd += 1
        else:
            used_even += 1

    return rank


def main() -> None:
    sol = Solution()

    assert sol.permute(4, 6) == [3, 4, 1, 2], "example 1 failed"
    assert sol.permute(3, 2) == [3, 2, 1], "example 2 failed"
    assert sol.permute(2, 3) == [], "example 3 failed"

    for n in range(1, 9):
        expected = brute_alternating(n)
        length = len(expected)

        for idx, perm in enumerate(expected, 1):
            assert rank_alternating(perm, n) == idx, (
                f"rank checker failed for n={n}, idx={idx}"
            )

            got = sol.permute(n, idx)
            if got != perm:
                raise AssertionError(
                    f"n={n}, k={idx}: got {got}, expected {perm}"
                )

        assert sol.permute(n, length + 1) == [], (
            f"n={n}, k={length + 1} should be empty"
        )

    assert sol.permute(1, 0) == [], "k=0 should be empty"

    res1 = sol.permute(100, 1)
    assert res1 == list(range(1, 101)), "n=100 k=1 failed"
    assert rank_alternating(res1, 100) == 1, "rank n=100 k=1 failed"

    big_k = 10**15

    res_big = sol.permute(100, big_k)
    assert is_permutation(res_big, 100), "n=100 k=1e15 not a permutation"
    assert is_alternating(res_big), "n=100 k=1e15 not alternating"
    assert rank_alternating(res_big, 100) == big_k, "rank n=100 k=1e15 failed"

    res_big2 = sol.permute(100, big_k - 1)
    assert is_permutation(res_big2, 100) and is_alternating(res_big2)
    assert rank_alternating(res_big2, 100) == big_k - 1, (
        "rank n=100 k=1e15-1 failed"
    )

    res99 = sol.permute(99, big_k)
    assert is_permutation(res99, 99) and is_alternating(res99)
    assert rank_alternating(res99, 99) == big_k, "rank n=99 k=1e15 failed"

    assert sol.permute(8, 1153) == [], "n=8 out of range failed"
    assert sol.permute(1, 2) == [], "n=1 out of range failed"

    print("All validation tests passed")


if __name__ == "__main__":
    main()