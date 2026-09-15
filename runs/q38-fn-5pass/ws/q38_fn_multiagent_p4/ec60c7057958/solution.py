from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # All counts only need to be known up to k.  Using k + 1 lets us
        # distinguish "at least k" from "less than k" safely.
        cap = k + 1

        # Capped factorials.
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(cap, fact[i - 1] * i)

        def mul_cap(a: int, b: int) -> int:
            """Return min(cap, a * b) without relying on huge integers."""
            if a == 0 or b == 0:
                return 0
            if a > cap // b:
                return cap
            return min(cap, a * b)

        def count(o: int, e: int, start_parity: int) -> int:
            """
            Number of valid completions with o odd and e even numbers left,
            where the next position must have parity start_parity:
            1 = odd, 0 = even.
            """
            m = o + e

            if start_parity == 1:
                need_o = (m + 1) // 2
                need_e = m // 2
            else:
                need_o = m // 2
                need_e = (m + 1) // 2

            if o != need_o or e != need_e:
                return 0

            return mul_cap(fact[o], fact[e])

        odd_count = (n + 1) // 2
        even_count = n // 2

        # Total number of alternating permutations.
        if n % 2 == 0:
            total = mul_cap(mul_cap(fact[odd_count], fact[even_count]), 2)
        else:
            total = mul_cap(fact[odd_count], fact[even_count])

        if total < k:
            return []

        used = [False] * (n + 1)
        ans = []

        rem_o = odd_count
        rem_e = even_count
        last_parity = -1  # -1 means no previous element yet.

        for _ in range(n):
            chosen = False

            for x in range(1, n + 1):
                if used[x]:
                    continue

                parity = x & 1

                # Adjacent parities must differ.
                if last_parity != -1 and parity == last_parity:
                    continue

                if parity == 1:
                    if rem_o == 0:
                        continue
                    no, ne = rem_o - 1, rem_e
                else:
                    if rem_e == 0:
                        continue
                    no, ne = rem_o, rem_e - 1

                block = count(no, ne, 1 - parity)

                if block == 0:
                    continue

                if k > block:
                    k -= block
                else:
                    used[x] = True
                    ans.append(x)
                    rem_o, rem_e = no, ne
                    last_parity = parity
                    chosen = True
                    break

            if not chosen:
                return []

        return ans