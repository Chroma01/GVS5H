from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        CAP = 10**15

        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(CAP, fact[i - 1] * i)

        def count_suffix(odd_left: int, even_left: int, next_is_odd: int) -> int:
            length = odd_left + even_left
            needed_first = (length + 1) // 2
            needed_other = length // 2

            if next_is_odd:
                if odd_left != needed_first or even_left != needed_other:
                    return 0
            else:
                if even_left != needed_first or odd_left != needed_other:
                    return 0

            return min(CAP, fact[odd_left] * fact[even_left])

        odd_left = (n + 1) // 2
        even_left = n // 2
        used = [False] * (n + 1)
        answer = []
        previous_parity = -1  # 1 for odd, 0 for even

        for _ in range(n):
            chosen = False

            for value in range(1, n + 1):
                if used[value]:
                    continue

                parity = value & 1
                if previous_parity != -1 and parity == previous_parity:
                    continue

                next_odd_left = odd_left - parity
                next_even_left = even_left - (1 - parity)

                block_size = count_suffix(
                    next_odd_left,
                    next_even_left,
                    1 - parity
                )

                if k > block_size:
                    k -= block_size
                    continue

                answer.append(value)
                used[value] = True
                odd_left = next_odd_left
                even_left = next_even_left
                previous_parity = parity
                chosen = True
                break

            if not chosen:
                return []

        return answer