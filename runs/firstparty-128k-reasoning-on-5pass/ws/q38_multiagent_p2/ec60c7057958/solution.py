from typing import List
from itertools import permutations


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        cap = k + 1

        def cap_mul(a: int, b: int) -> int:
            if a == 0 or b == 0:
                return 0
            if a >= cap or b >= cap:
                return cap
            v = a * b
            return cap if v >= cap else v

        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = cap_mul(fact[i - 1], i)

        odds = list(range(1, n + 1, 2))
        evens = list(range(2, n + 1, 2))
        o = len(odds)
        e = len(evens)

        if n % 2 == 1:
            total = cap_mul(fact[o], fact[e])
        else:
            total = cap_mul(2, cap_mul(fact[o], fact[e]))

        if k > total:
            return []

        ans = []

        if n % 2 == 1:
            block = cap_mul(fact[o - 1], fact[e])
            if block <= 0:
                return []
            idx = (k - 1) // block
            if idx < 0 or idx >= len(odds):
                return []
            x = odds.pop(idx)
            ans.append(x)
            k = (k - 1) % block + 1
            count_odd = o - 1
            count_even = e
            need_odd = False
        else:
            m = n // 2
            block = cap_mul(fact[m - 1], fact[m])
            if block <= 0:
                return []
            idx = (k - 1) // block
            if idx < 0 or idx >= n:
                return []
            x = idx + 1
            ans.append(x)
            k = (k - 1) % block + 1
            if x % 2 == 1:
                odds.pop(x // 2)
                count_odd = m - 1
                count_even = m
                need_odd = False
            else:
                evens.pop(x // 2 - 1)
                count_odd = m
                count_even = m - 1
                need_odd = True

        while count_odd + count_even > 0:
            if need_odd:
                if count_odd <= 0:
                    return []
                block = cap_mul(fact[count_odd - 1], fact[count_even])
                if block <= 0:
                    return []
                idx = (k - 1) // block
                if idx < 0 or idx >= count_odd or idx >= len(odds):
                    return []
                x = odds.pop(idx)
                ans.append(x)
                k = (k - 1) % block + 1
                count_odd -= 1
                need_odd = False
            else:
                if count_even <= 0:
                    return []
                block = cap_mul(fact[count_even - 1], fact[count_odd])
                if block <= 0:
                    return []
                idx = (k - 1) // block
                if idx < 0 or idx >= count_even or idx >= len(evens):
                    return []
                x = evens.pop(idx)
                ans.append(x)
                k = (k - 1) % block + 1
                count_even -= 1
                need_odd = True

        return ans


def _brute_valid(n: int) -> List[List[int]]:
    res: List[List[int]] = []
    for p in permutations(range(1, n + 1)):
        ok = True
        for i in range(n - 1):
            if (p[i] & 1) == (p[i + 1] & 1):
                ok = False
                break
        if ok:
            res.append(list(p))
    res.sort()
    return res


def _is_alternating(a: List[int]) -> bool:
    return all((a[i] & 1) != (a[i + 1] & 1) for i in range(len(a) - 1))


def _run_self_tests() -> None:
    sol = Solution()

    assert sol.permute(4, 6) == [3, 4, 1, 2]
    assert sol.permute(3, 2) == [3, 2, 1]
    assert sol.permute(2, 3) == []

    for n in range(1, 9):
        valid = _brute_valid(n)
        total = len(valid)
        for rank, expected in enumerate(valid, 1):
            got = sol.permute(n, rank)
            assert got == expected, (n, rank, got, expected)
        assert sol.permute(n, total + 1) == []
        assert sol.permute(n, 10 ** 15) == []

    assert sol.permute(1, 1) == [1]
    assert sol.permute(1, 2) == []
    assert sol.permute(2, 1) == [1, 2]
    assert sol.permute(2, 2) == [2, 1]
    assert sol.permute(2, 3) == []

    for n in (99, 100):
        first = sol.permute(n, 1)
        assert first == list(range(1, n + 1))

        second = sol.permute(n, 2)
        assert len(second) == n
        assert sorted(second) == list(range(1, n + 1))
        assert _is_alternating(second)
        assert second != first

    max_k = 10 ** 15
    for n in (99, 100):
        got = sol.permute(n, max_k)
        assert len(got) == n
        assert sorted(got) == list(range(1, n + 1))
        assert _is_alternating(got)


if __name__ == "__main__":
    _run_self_tests()