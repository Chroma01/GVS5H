from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        if k <= 0:
            return []

        # All counts only need to be distinguished up to the requested rank.
        CAP = k

        # Saturated factorials: fact[i] = min(i!, CAP)
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            if fact[i - 1] > CAP // i:
                fact[i] = CAP
            else:
                fact[i] = fact[i - 1] * i

        total_odd = (n + 1) // 2
        total_even = n // 2

        used = [False] * (n + 1)
        used_odd = 0
        used_even = 0

        ans = []
        req = -1  # -1 means no parity is forced yet; 0 = even, 1 = odd

        def completions(odd_left: int, even_left: int, next_parity: int) -> int:
            """
            Number of valid ways to fill the remaining positions, given:
            - odd_left unused odd numbers
            - even_left unused even numbers
            - next_parity required at the next position
            """
            if odd_left < 0 or even_left < 0:
                return 0

            m = odd_left + even_left

            if next_parity == 1:  # next position must be odd
                need_odd = (m + 1) // 2
                need_even = m // 2
            else:                 # next position must be even
                need_even = (m + 1) // 2
                need_odd = m // 2

            if odd_left != need_odd or even_left != need_even:
                return 0

            # If the parity slots match, any ordering of remaining odds among
            # odd slots and evens among even slots is valid.
            if fact[odd_left] > CAP // fact[even_left]:
                return CAP
            return fact[odd_left] * fact[even_left]

        for _ in range(n):
            chosen = -1

            # Try possible next values in increasing numeric order.
            for x in range(1, n + 1):
                if used[x]:
                    continue

                parity = x & 1
                if req != -1 and parity != req:
                    continue

                if parity == 1:
                    odd_left = total_odd - used_odd - 1
                    even_left = total_even - used_even
                else:
                    odd_left = total_odd - used_odd
                    even_left = total_even - used_even - 1

                cnt = completions(odd_left, even_left, 1 - parity)

                if k > cnt:
                    k -= cnt
                else:
                    chosen = x
                    break

            if chosen == -1:
                return []

            used[chosen] = True
            ans.append(chosen)

            if chosen & 1:
                used_odd += 1
                req = 0
            else:
                used_even += 1
                req = 1

        return ans