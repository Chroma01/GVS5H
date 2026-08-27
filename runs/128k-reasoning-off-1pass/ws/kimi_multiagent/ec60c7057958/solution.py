from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials up to n
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i

        # Counts of odd/even numbers in [1..n]
        odd_total = (n + 1) // 2
        even_total = n // 2

        def count_completions(odd_rem: int, even_rem: int, next_parity, slots_rem: int) -> int:
            """
            Number of ways to fill `slots_rem` remaining positions given
            odd_rem/even_rem remaining numbers and the parity required at the
            next position (0 = even, 1 = odd, None = either).
            The parity pattern of the remaining slots is fully determined.
            """
            if next_parity is None:
                # First position: try both starting parities and sum.
                total = 0
                for p in (0, 1):
                    total += count_completions(odd_rem, even_rem, p, slots_rem)
                return total
            # slots_rem positions, next one must have parity next_parity,
            # alternating thereafter.
            # Count required slots of each parity.
            # Positions 0..slots_rem-1 (relative), position i has parity
            # next_parity if i even, else 1 - next_parity.
            slots_next = (slots_rem + 1) // 2  # slots with parity == next_parity
            slots_other = slots_rem // 2       # slots with the other parity
            if next_parity == 1:  # next is odd
                need_odd, need_even = slots_next, slots_other
            else:                 # next is even
                need_even, need_odd = slots_next, slots_other
            if need_odd != odd_rem or need_even != even_rem:
                return 0
            return fact[odd_rem] * fact[even_rem]

        used = [False] * (n + 1)
        result = []
        odd_rem, even_rem = odd_total, even_total

        # Quick total check: if k exceeds total valid permutations, return []
        total = count_completions(odd_rem, even_rem, None, n)
        if k > total:
            return []

        prev_parity = None  # parity required at current position (None = first)
        for pos in range(n):
            slots_after = n - pos - 1  # slots remaining after choosing this position
            found = False
            for v in range(1, n + 1):
                if used[v]:
                    continue
                p = v & 1  # 1 = odd, 0 = even
                if prev_parity is not None and p == prev_parity:
                    continue  # adjacent same parity not allowed
                # Choose v: remaining counts
                if p == 1:
                    o_rem, e_rem = odd_rem - 1, even_rem
                else:
                    o_rem, e_rem = odd_rem, even_rem - 1
                # Next position (if any) must have parity 1 - p
                nxt = (1 - p) if slots_after > 0 else None
                if slots_after == 0:
                    cnt = 1  # last element, exactly one completion
                else:
                    cnt = count_completions(o_rem, e_rem, nxt, slots_after)
                if cnt == 0:
                    continue
                if k > cnt:
                    k -= cnt
                else:
                    # Select v
                    result.append(v)
                    used[v] = True
                    odd_rem, even_rem = o_rem, e_rem
                    prev_parity = p
                    found = True
                    break
            if not found:
                return []
        return result