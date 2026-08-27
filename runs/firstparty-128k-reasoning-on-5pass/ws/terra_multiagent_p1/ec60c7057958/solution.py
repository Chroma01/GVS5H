from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        cap = k + 1

        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(cap, fact[i - 1] * i)

        def count_completions(odd_left: int, even_left: int, next_parity: int) -> int:
            remaining = odd_left + even_left
            if remaining == 0:
                return 1

            first_slots = (remaining + 1) // 2
            second_slots = remaining // 2

            if next_parity == 1:
                if odd_left != first_slots or even_left != second_slots:
                    return 0
            else:
                if even_left != first_slots or odd_left != second_slots:
                    return 0

            return min(cap, fact[odd_left] * fact[even_left])

        odd_left = (n + 1) // 2
        even_left = n // 2
        unused = list(range(1, n + 1))
        result = []
        previous_parity = -1

        for _ in range(n):
            chosen = False

            for i, value in enumerate(unused):
                parity = value & 1
                if previous_parity != -1 and parity == previous_parity:
                    continue

                next_odd = odd_left - (parity == 1)
                next_even = even_left - (parity == 0)
                ways = count_completions(next_odd, next_even, 1 - parity)

                if k > ways:
                    k -= ways
                else:
                    result.append(value)
                    unused.pop(i)
                    odd_left = next_odd
                    even_left = next_even
                    previous_parity = parity
                    chosen = True
                    break

            if not chosen:
                return []

        return result