from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        cap = k

        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(cap, fact[i - 1] * i)

        def suffix_count(odd_left: int, even_left: int, next_parity: int) -> int:
            length = odd_left + even_left

            if next_parity == 1:
                needed_odd = (length + 1) // 2
                needed_even = length // 2
            else:
                needed_odd = length // 2
                needed_even = (length + 1) // 2

            if odd_left != needed_odd or even_left != needed_even:
                return 0

            return min(cap, fact[odd_left] * fact[even_left])

        unused = list(range(1, n + 1))
        odd_left = (n + 1) // 2
        even_left = n // 2
        result = []
        required_parity = None

        for _ in range(n):
            selected = False

            for i, value in enumerate(unused):
                parity = value & 1

                if required_parity is not None and parity != required_parity:
                    continue

                next_odd = odd_left - (parity == 1)
                next_even = even_left - (parity == 0)
                ways = suffix_count(next_odd, next_even, 1 - parity)

                if ways < k:
                    k -= ways
                    continue

                result.append(value)
                unused.pop(i)
                odd_left = next_odd
                even_left = next_even
                required_parity = 1 - parity
                selected = True
                break

            if not selected:
                return []

        return result