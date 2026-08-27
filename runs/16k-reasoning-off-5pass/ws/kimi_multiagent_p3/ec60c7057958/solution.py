from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials 0..n
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i

        CAP = k  # counts larger than k are irrelevant; cap to keep numbers small

        def capped_mul(a: int, b: int) -> int:
            if a > CAP or b > CAP:
                return CAP + 1
            r = a * b
            return r if r <= CAP else CAP + 1

        def count(o: int, e: int, need_odd: bool) -> int:
            # Number of alternating arrangements using o odd and e even numbers,
            # where the next position must be odd (need_odd) or even.
            if need_odd:
                if not (o == e or o == e + 1):
                    return 0
            else:
                if not (e == o or e == o + 1):
                    return 0
            return capped_mul(fact[o], fact[e])

        odds = [x for x in range(1, n + 1) if x % 2 == 1]
        evens = [x for x in range(1, n + 1) if x % 2 == 0]
        o, e = len(odds), len(evens)

        # Total valid permutations: start with odd or start with even
        total = count(o, e, True) + count(o, e, False)
        if k > total:
            return []

        res = []
        prev_odd = None  # parity of previous element; None means no constraint yet
        io = ie = 0      # pointers into odds / evens lists (both kept sorted)

        for _ in range(n):
            # Candidate pools in ascending order
            if prev_odd is None:
                candidates = [(v, True) for v in odds[io:]] + [(v, False) for v in evens[ie:]]
                candidates.sort(key=lambda t: t[0])
            elif prev_odd:
                candidates = [(v, False) for v in evens[ie:]]
            else:
                candidates = [(v, True) for v in odds[io:]]

            for v, is_odd in candidates:
                no, ne = (o - 1, e) if is_odd else (o, e - 1)
                # After choosing v, next position must be opposite parity
                block = count(no, ne, not is_odd)
                if k > block:
                    k -= block
                else:
                    res.append(v)
                    if is_odd:
                        io += 1
                        o -= 1
                    else:
                        ie += 1
                        e -= 1
                    prev_odd = is_odd
                    break

        return res