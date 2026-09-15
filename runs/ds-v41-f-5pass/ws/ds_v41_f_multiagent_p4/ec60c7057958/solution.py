from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Factorials up to n (max odd/even count is ceil(n/2) <= 50).
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i

        def count_completions(o: int, e: int, start_odd: bool) -> int:
            # Number of alternating arrangements of `o` odd and `e` even
            # numbers whose FIRST slot has parity start_odd (True -> odd).
            # The parity pattern is forced, so it is feasible iff the counts
            # match the number of odd/even slots; then count = o! * e!.
            if o < 0 or e < 0:
                return 0
            if start_odd:
                if o == e or o == e + 1:
                    return fact[o] * fact[e]
            else:
                if e == o or e == o + 1:
                    return fact[o] * fact[e]
            return 0

        unused = list(range(1, n + 1))
        cur_odd = (n + 1) // 2   # number of odd values in 1..n
        cur_even = n // 2        # number of even values in 1..n
        prev_odd = None          # parity of the previously placed element
        result = []

        for _ in range(n):
            chosen = None
            for c in unused:                     # ascending -> lexicographic
                c_odd = (c & 1) == 1
                if prev_odd is not None and c_odd == prev_odd:
                    continue                     # would violate alternation
                o_rem = cur_odd - (1 if c_odd else 0)
                e_rem = cur_even - (0 if c_odd else 1)
                # next element must have opposite parity to c
                block = count_completions(o_rem, e_rem, not c_odd)
                if k > block:
                    k -= block                   # skip this whole block
                    continue
                chosen = c
                break
            if chosen is None:                   # fewer than k permutations
                return []
            result.append(chosen)
            unused.remove(chosen)
            if chosen & 1:
                cur_odd -= 1
                prev_odd = True
            else:
                cur_even -= 1
                prev_odd = False

        return result