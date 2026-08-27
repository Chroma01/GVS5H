from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        cap = k

        # Factorials saturated at cap, since no larger value needs distinction.
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(cap, fact[i - 1] * i)

        def completion_count(odd_left: int, even_left: int, next_is_odd: bool) -> int:
            # A suffix alternating from odd requires o == e or o == e + 1.
            # A suffix alternating from even requires e == o or e == o + 1.
            if next_is_odd:
                if odd_left != even_left and odd_left != even_left + 1:
                    return 0
            else:
                if even_left != odd_left and even_left != odd_left + 1:
                    return 0

            return min(cap, fact[odd_left] * fact[even_left])

        odd_left = (n + 1) // 2
        even_left = n // 2
        used = [False] * (n + 1)
        answer = []
        previous_parity = -1

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

                count = completion_count(
                    next_odd_left,
                    next_even_left,
                    next_is_odd=(parity == 0),
                )

                if k > count:
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