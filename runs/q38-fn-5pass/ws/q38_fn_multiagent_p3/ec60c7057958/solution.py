from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        if k <= 0:
            return []

        # Any count >= CAP is indistinguishable from "large enough" for the
        # current k, because k is always strictly less than CAP during unranking.
        CAP = k + 1

        def mul_cap(a: int, b: int) -> int:
            if a == 0 or b == 0:
                return 0
            if a > CAP // b:
                return CAP
            return a * b

        # Capped factorials: i! is stored exactly if it is below CAP,
        # otherwise it is capped at CAP.
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = mul_cap(fact[i - 1], i)

        odd_total = (n + 1) // 2
        even_total = n // 2

        def completions(rem_odd: int, rem_even: int, next_odd: bool) -> int:
            """
            Number of valid suffixes given:
            - rem_odd unused odd numbers
            - rem_even unused even numbers
            - the next position must be odd iff next_odd is True
            """
            length = rem_odd + rem_even
            if length == 0:
                return 1

            if next_odd:
                odd_slots = (length + 1) // 2
                even_slots = length // 2
                if rem_odd != odd_slots or rem_even != even_slots:
                    return 0
            else:
                even_slots = (length + 1) // 2
                odd_slots = length // 2
                if rem_even != even_slots or rem_odd != odd_slots:
                    return 0

            return mul_cap(fact[rem_odd], fact[rem_even])

        # Total valid permutations: odd-start plus even-start.
        total = (
            completions(odd_total, even_total, True)
            + completions(odd_total, even_total, False)
        )
        if total > CAP:
            total = CAP

        if k > total:
            return []

        used = [False] * (n + 1)
        ans = []

        rem_odd = odd_total
        rem_even = even_total
        prev_parity = -1  # -1 means no previous element yet

        for _ in range(n):
            chosen = -1

            # Try possible next values in lexicographic order.
            for x in range(1, n + 1):
                if used[x]:
                    continue

                parity = x & 1
                if prev_parity != -1 and parity == prev_parity:
                    continue

                if parity == 1:
                    new_odd = rem_odd - 1
                    new_even = rem_even
                else:
                    new_odd = rem_odd
                    new_even = rem_even - 1

                if new_odd < 0 or new_even < 0:
                    continue

                # After choosing x, the next parity must be the opposite one.
                cnt = completions(new_odd, new_even, parity == 0)

                if cnt >= k:
                    chosen = x
                    break

                k -= cnt

            if chosen == -1:
                return []

            ans.append(chosen)
            used[chosen] = True

            if chosen & 1:
                rem_odd -= 1
            else:
                rem_even -= 1

            prev_parity = chosen & 1

        return ans