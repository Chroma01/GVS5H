from typing import List
from itertools import permutations


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials up to n.
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i

        def completions(o: int, e: int, req: int) -> int:
            # Ways to fill remaining positions with `o` unused odd numbers,
            # `e` unused even numbers, next position requiring parity `req`
            # (1 = odd, 0 = even).
            t = o + e
            if req == 1:
                odd_slots = (t + 1) // 2
                even_slots = t // 2
            else:
                even_slots = (t + 1) // 2
                odd_slots = t // 2
            if odd_slots == o and even_slots == e:
                return fact[o] * fact[e]
            return 0

        used = [False] * (n + 1)
        o = (n + 1) // 2  # count of odd numbers 1..n
        e = n // 2        # count of even numbers 1..n
        prev_parity = -1  # parity of previously placed element (-1 = none)

        res: List[int] = []
        for _ in range(n):
            chosen = -1
            for c in range(1, n + 1):
                if used[c]:
                    continue
                p = c & 1  # 1 = odd, 0 = even
                if prev_parity != -1 and p == prev_parity:
                    continue
                o2 = o - (1 if p == 1 else 0)
                e2 = e - (1 if p == 0 else 0)
                block = completions(o2, e2, 1 - p)
                if k > block:
                    k -= block
                else:
                    chosen = c
                    res.append(c)
                    used[c] = True
                    o, e = o2, e2
                    prev_parity = p
                    break
            if chosen == -1:
                return []
        return res


def _is_alt(p):
    for i in range(len(p) - 1):
        if (p[i] & 1) == (p[i + 1] & 1):
            return False
    return True


def brute(n):
    valid = [list(p) for p in permutations(range(1, n + 1)) if _is_alt(p)]
    valid.sort()
    return valid


def main():
    sol = Solution()
    all_ok = True
    for n in range(1, 9):
        valid = brute(n)
        total = len(valid)
        for k in range(1, total + 3):
            expected = valid[k - 1] if k <= total else []
            got = sol.permute(n, k)
            if got != expected:
                all_ok = False
                print(f"MISMATCH n={n} k={k}: got={got} expected={expected}")
    if all_ok:
        print("ALL OK")


if __name__ == "__main__":
    main()