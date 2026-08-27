from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        cap = k

        # Saturated factorials: any value above the initial rank is equivalent
        # for all comparisons performed during unranking.
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(cap, fact[i - 1] * i)

        def suffix_count(odd_left: int, even_left: int, next_parity: int) -> int:
            """
            Count valid alternating arrangements of all remaining values when
            the next value must have parity next_parity (1 = odd, 0 = even).
            """
            remaining = odd_left + even_left
            if remaining == 0:
                return 1

            first_parity_slots = (remaining + 1) // 2
            other_parity_slots = remaining // 2

            if next_parity == 1:
                if odd_left != first_parity_slots or even_left != other_parity_slots:
                    return 0
            else:
                if even_left != first_parity_slots or odd_left != other_parity_slots:
                    return 0

            return min(cap, fact[odd_left] * fact[even_left])

        odd_left = (n + 1) // 2
        even_left = n // 2
        used = [False] * (n + 1)
        answer = []
        previous_parity = -1

        for pos in range(n):
            chosen = False

            for value in range(1, n + 1):
                if used[value]:
                    continue

                parity = value & 1
                if previous_parity != -1 and parity == previous_parity:
                    continue

                next_odd_left = odd_left - (parity == 1)
                next_even_left = even_left - (parity == 0)
                remaining = n - pos - 1

                if remaining == 0:
                    count = 1
                else:
                    count = suffix_count(
                        next_odd_left,
                        next_even_left,
                        1 - parity,
                    )

                if count < k:
                    k -= count
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