from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials as exact big integers.
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i

        def count(o: int, e: int, last_parity: int) -> int:
            """
            Number of ways to fill the remaining o + e positions given
            o odd numbers and e even numbers left, where the previously
            placed element has parity last_parity (1 = odd, 0 = even).

            The parity pattern of the remaining slots is forced:
            the next slot must have parity 1 - last_parity, and it
            alternates from there. Feasible iff the number of odd
            slots equals o and even slots equals e; then the count is
            o! * e! (any bijection of remaining odds/evens to their slots).
            """
            total = o + e
            # Slots at offsets 0, 2, 4, ... have parity 1 - last_parity.
            first_parity = 1 - last_parity
            first_slots = (total + 1) // 2
            second_slots = total // 2
            if first_parity == 1:
                odd_slots, even_slots = first_slots, second_slots
            else:
                even_slots, odd_slots = first_slots, second_slots
            if odd_slots == o and even_slots == e:
                return fact[o] * fact[e]
            return 0

        odds = (n + 1) // 2   # numbers 1, 3, 5, ...
        evens = n // 2        # numbers 2, 4, 6, ...

        # Total valid permutations: sum over feasible starting parities.
        total = 0
        if odds > 0:
            total += count(odds - 1, evens, 1)  # start with an odd number
        if evens > 0:
            total += count(odds, evens - 1, 0)  # start with an even number
        if k > total:
            return []

        remaining = list(range(1, n + 1))
        result = []
        prev_parity = -1  # no constraint for the first position

        for _ in range(n):
            for idx, v in enumerate(remaining):
                p = v & 1
                if prev_parity != -1 and p == prev_parity:
                    continue  # adjacent elements must differ in parity
                o_left = odds - (1 if p == 1 else 0)
                e_left = evens - (1 if p == 0 else 0)
                c = count(o_left, e_left, p)
                if k > c:
                    k -= c
                else:
                    result.append(v)
                    remaining.pop(idx)
                    odds, evens = o_left, e_left
                    prev_parity = p
                    break

        return result