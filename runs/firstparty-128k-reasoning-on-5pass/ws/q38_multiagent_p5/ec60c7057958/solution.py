from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        if n <= 0 or k < 1:
            return []

        LIMIT = 10**15 + 1

        # Capped factorials: exact while <= 10**15, otherwise LIMIT.
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            prev = fact[i - 1]
            if prev >= LIMIT:
                fact[i] = LIMIT
            elif prev > LIMIT // i:
                fact[i] = LIMIT
            else:
                fact[i] = prev * i

        def completions(rem_odd: int, rem_even: int, next_parity: int, length: int) -> int:
            """
            Count valid suffixes of given length that must start with next_parity.
            next_parity is 1 for odd, 0 for even.
            """
            if rem_odd < 0 or rem_even < 0:
                return 0

            if length == 0:
                return 1 if rem_odd == 0 and rem_even == 0 else 0

            if next_parity == 1:
                need_odd = (length + 1) // 2
                need_even = length // 2
            else:
                need_odd = length // 2
                need_even = (length + 1) // 2

            if rem_odd != need_odd or rem_even != need_even:
                return 0

            a = fact[rem_odd]
            b = fact[rem_even]
            if a >= LIMIT or b >= LIMIT:
                return LIMIT
            if a > LIMIT // b:
                return LIMIT
            return a * b

        rem_odd = (n + 1) // 2
        rem_even = n // 2
        used = [False] * (n + 1)
        ans = []
        required = None  # None at position 0; afterwards 1 for odd, 0 for even

        for pos in range(n):
            chosen = None

            for x in range(1, n + 1):
                if used[x]:
                    continue

                p = x & 1
                if required is not None and p != required:
                    continue

                new_odd = rem_odd - (1 if p == 1 else 0)
                new_even = rem_even - (1 if p == 0 else 0)
                length = n - pos - 1

                c = completions(new_odd, new_even, 1 - p, length)

                if k > c:
                    k -= c
                else:
                    chosen = x
                    break

            if chosen is None:
                return []

            ans.append(chosen)
            used[chosen] = True

            p = chosen & 1
            if p == 1:
                rem_odd -= 1
            else:
                rem_even -= 1

            required = 1 - p

        return ans


if __name__ == "__main__":
    from itertools import permutations

    s = Solution()

    # Provided examples.
    assert s.permute(4, 6) == [3, 4, 1, 2]
    assert s.permute(3, 2) == [3, 2, 1]
    assert s.permute(2, 3) == []

    # Basic edge cases.
    assert s.permute(1, 1) == [1]
    assert s.permute(1, 2) == []
    assert s.permute(2, 1) == [1, 2]
    assert s.permute(2, 2) == [2, 1]

    # k equal to total, and k greater than total.
    assert s.permute(4, 8) == [4, 3, 2, 1]
    assert s.permute(4, 9) == []
    assert s.permute(5, 12) == [5, 4, 3, 2, 1]
    assert s.permute(6, 72) == [6, 5, 4, 3, 2, 1]

    # Large n: first permutation and a maximum-size k to exercise capping.
    assert s.permute(100, 1) == list(range(1, 101))
    res = s.permute(100, 10**15)
    assert len(res) == 100
    assert sorted(res) == list(range(1, 101))
    assert all((res[i] ^ res[i + 1]) & 1 for i in range(99))

    # Brute-force verification for small n.
    def is_alternating(p):
        return all((p[i] ^ p[i + 1]) & 1 for i in range(len(p) - 1))

    for n in range(1, 7):
        perms = [list(p) for p in permutations(range(1, n + 1)) if is_alternating(p)]
        for idx, p in enumerate(perms, 1):
            assert s.permute(n, idx) == p
        assert s.permute(n, len(perms) + 1) == []