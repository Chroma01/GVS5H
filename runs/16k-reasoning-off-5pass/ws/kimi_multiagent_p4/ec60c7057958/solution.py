from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # k <= 1e15, so cap all counts to keep arithmetic cheap.
        CAP = 10 ** 15 + 1

        # fact[i] = min(i!, CAP)
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(fact[i - 1] * i, CAP)

        def count(o: int, e: int, next_parity: int) -> int:
            """Number of alternating arrangements using o odds and e evens,
            where the next element must have parity next_parity (1=odd, 0=even).
            Once the next parity is fixed, the whole parity pattern is forced:
            it needs exactly ceil((o+e)/2) numbers of that parity. If feasible,
            values can be assigned to parity slots in o! * e! ways."""
            m = o + e
            if m == 0:
                return 1
            need = (m + 1) // 2
            if next_parity == 1:
                if o != need:
                    return 0
            else:
                if e != need:
                    return 0
            return min(fact[o] * fact[e], CAP)

        odds = [x for x in range(1, n + 1) if x % 2 == 1]
        evens = [x for x in range(1, n + 1) if x % 2 == 0]
        o, e = len(odds), len(evens)

        # Total valid permutations; first position may start with either parity.
        total = min(count(o, e, 1) + count(o, e, 0), CAP)
        if k > total:
            return []

        result = []
        last_parity = -1  # -1 = no constraint yet (first position)

        for _ in range(n):
            # Remaining candidate values in increasing numeric order,
            # keeping only parities allowed by the adjacency constraint.
            candidates = []
            if last_parity != 1:
                candidates.extend(odds)
            if last_parity != 0:
                candidates.extend(evens)
            candidates.sort()

            # Skip whole lexicographic blocks until k lands inside one.
            chosen = None
            for v in candidates:
                if v % 2 == 1:
                    c = count(o - 1, e, 0)  # next must be even
                else:
                    c = count(o, e - 1, 1)  # next must be odd
                if k > c:
                    k -= c
                else:
                    chosen = v
                    break

            result.append(chosen)
            if chosen % 2 == 1:
                odds.remove(chosen)
                o -= 1
                last_parity = 1
            else:
                evens.remove(chosen)
                e -= 1
                last_parity = 0

        return result