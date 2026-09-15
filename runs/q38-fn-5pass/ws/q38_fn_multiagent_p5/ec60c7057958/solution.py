from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        if k <= 0:
            return []

        # Any count larger than the initial k is equivalent for unranking.
        limit = k + 1

        # Capped factorials.
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            if fact[i - 1] > limit // i:
                fact[i] = limit
            else:
                v = fact[i - 1] * i
                fact[i] = limit if v > limit else v

        def mul_cap(a: int, b: int) -> int:
            if a >= limit or b >= limit:
                return limit
            if a > limit // b:
                return limit
            return a * b

        def completions(odd_rem: int, even_rem: int, last_parity: int) -> int:
            """
            Count valid suffixes after the last chosen element has parity last_parity.
            Parity convention: 1 = odd, 0 = even.
            """
            length = odd_rem + even_rem
            if length == 0:
                return 1

            start_parity = 1 - last_parity
            need_start = (length + 1) // 2
            need_other = length // 2

            if start_parity == 1:
                if odd_rem != need_start or even_rem != need_other:
                    return 0
            else:
                if even_rem != need_start or odd_rem != need_other:
                    return 0

            return mul_cap(fact[odd_rem], fact[even_rem])

        odd_total = (n + 1) // 2
        even_total = n // 2

        # Total number of valid permutations, capped at limit.
        total = 0
        for x in range(1, n + 1):
            parity = x & 1
            odd_rem = odd_total - (1 if parity == 1 else 0)
            even_rem = even_total - (1 if parity == 0 else 0)
            cnt = completions(odd_rem, even_rem, parity)

            if total >= limit or cnt >= limit or total > limit - cnt:
                total = limit
            else:
                total += cnt

        if total < k:
            return []

        used = [False] * (n + 1)
        odd_rem = odd_total
        even_rem = even_total
        prev_parity = -1
        ans = []

        # Greedy lexicographic unranking.
        for _ in range(n):
            chosen = -1

            for x in range(1, n + 1):
                if used[x]:
                    continue

                parity = x & 1
                if prev_parity != -1 and parity == prev_parity:
                    continue

                next_odd = odd_rem - (1 if parity == 1 else 0)
                next_even = even_rem - (1 if parity == 0 else 0)
                cnt = completions(next_odd, next_even, parity)

                if cnt >= k:
                    chosen = x
                    break

                k -= cnt

            if chosen == -1:
                return []

            used[chosen] = True
            ans.append(chosen)

            if chosen & 1:
                odd_rem -= 1
            else:
                even_rem -= 1

            prev_parity = chosen & 1

        return ans