from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        num_odd = (n + 1) // 2
        num_even = n // 2

        # Capped factorials. k <= 1e15, so anything >= 1e18 behaves as "huge".
        LIMIT = 10 ** 18
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            v = fact[i - 1] * i
            fact[i] = v if v < LIMIT else LIMIT

        # Once the parity of the first element is chosen, the parity of every
        # later position is forced by alternation.  A pattern is feasible only
        # if its number of odd slots equals the number of available odd values.
        # parity encoding: 1 = odd, 0 = even
        def pattern_feasible(first_parity: int) -> bool:
            odd_slots = (n + 1) // 2 if first_parity == 1 else n // 2
            even_slots = n - odd_slots
            return odd_slots == num_odd and even_slots == num_even

        used = [False] * (n + 1)
        remaining_odd = num_odd
        remaining_even = num_even
        first_parity = None
        ans: List[int] = []

        for pos in range(n):
            if pos == 0:
                candidates = [v for v in range(1, n + 1) if pattern_feasible(v & 1)]
            else:
                need = first_parity if pos % 2 == 0 else 1 - first_parity
                candidates = [v for v in range(1, n + 1)
                              if not used[v] and (v & 1) == need]

            chosen = False
            for v in candidates:
                if v & 1:
                    ro, re = remaining_odd - 1, remaining_even
                else:
                    ro, re = remaining_odd, remaining_even - 1

                # Number of ways to fill the remaining positions.
                block = fact[ro] * fact[re]

                if k <= block:
                    ans.append(v)
                    used[v] = True
                    remaining_odd, remaining_even = ro, re
                    if pos == 0:
                        first_parity = v & 1
                    chosen = True
                    break
                else:
                    k -= block

            if not chosen:
                # k is larger than the number of remaining valid permutations.
                return []

        return ans