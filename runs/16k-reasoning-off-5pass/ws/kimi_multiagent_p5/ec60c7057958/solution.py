from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Cap for counts: anything >= k is "big enough" since we only compare against k.
        CAP = 10 ** 18  # > max k (10^15), keeps arithmetic small and safe

        # Precompute capped factorials fact[i] = min(i!, CAP)
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(fact[i - 1] * i, CAP)

        def count_completions(o: int, e: int, next_parity: int) -> int:
            """
            Number of ways to fill remaining slots using o odd and e even numbers,
            given the next slot must have parity `next_parity` (1 = odd, 0 = even).
            The parity pattern is then forced to strictly alternate.
            Returns 0 if infeasible, else min(o! * e!, CAP).
            """
            total = o + e
            if total == 0:
                return 1
            # Slots of each parity when starting with next_parity and alternating.
            first_slots = (total + 1) // 2   # slots having parity == next_parity
            second_slots = total // 2        # slots having the opposite parity
            if next_parity == 1:  # next must be odd
                if o != first_slots or e != second_slots:
                    return 0
            else:                 # next must be even
                if e != first_slots or o != second_slots:
                    return 0
            return min(fact[o] * fact[e], CAP)

        # Total number of valid alternating permutations (capped).
        total_odds = (n + 1) // 2
        total_evens = n // 2
        total = 0
        for start_parity in (0, 1):
            total += count_completions(
                total_odds - (1 if start_parity == 1 else 0),
                total_evens - (1 if start_parity == 0 else 0),
                1 - start_parity,
            )
            total = min(total, CAP)

        if k > total:
            return []

        remaining = list(range(1, n + 1))
        odds_left = total_odds
        evens_left = total_evens
        prev_parity = -1  # -1 means no previous element (first position)
        result = []

        for pos in range(n):
            for idx, val in enumerate(remaining):
                p = val & 1
                # Adjacent parities must differ.
                if prev_parity != -1 and p == prev_parity:
                    continue
                o_after = odds_left - (1 if p == 1 else 0)
                e_after = evens_left - (1 if p == 0 else 0)
                c = count_completions(o_after, e_after, 1 - p)
                if c == 0:
                    continue
                if k > c:
                    k -= c  # skip this whole block
                else:
                    # The k-th permutation lives in this block; choose val.
                    result.append(val)
                    remaining.pop(idx)
                    odds_left, evens_left = o_after, e_after
                    prev_parity = p
                    break

        return result