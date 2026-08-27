from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        CAP = 10**15 + 1

        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(CAP, fact[i - 1] * i)

        def ways(rem_odd: int, rem_even: int, next_odd: bool) -> int:
            if rem_odd < 0 or rem_even < 0:
                return 0

            m = rem_odd + rem_even
            if m == 0:
                return 1

            if next_odd:
                need_odd = (m + 1) // 2
                need_even = m // 2
            else:
                need_odd = m // 2
                need_even = (m + 1) // 2

            if rem_odd != need_odd or rem_even != need_even:
                return 0

            return min(CAP, fact[rem_odd] * fact[rem_even])

        rem_odd = (n + 1) // 2
        rem_even = n // 2

        # For odd n, the first element must be odd.
        # For even n, either parity can start the permutation.
        required_odd = None if n % 2 == 0 else True

        used = [False] * (n + 1)
        ans = []

        for _ in range(n):
            chosen = None

            for x in range(1, n + 1):
                if used[x]:
                    continue

                x_odd = (x % 2 == 1)

                if required_odd is not None and x_odd != required_odd:
                    continue

                if x_odd:
                    if rem_odd == 0:
                        continue
                    block = ways(rem_odd - 1, rem_even, False)
                else:
                    if rem_even == 0:
                        continue
                    block = ways(rem_odd, rem_even - 1, True)

                if block == 0:
                    continue

                if k > block:
                    k -= block
                else:
                    chosen = x
                    break

            if chosen is None:
                return []

            used[chosen] = True
            ans.append(chosen)

            if chosen % 2 == 1:
                rem_odd -= 1
                required_odd = False
            else:
                rem_even -= 1
                required_odd = True

        return ans