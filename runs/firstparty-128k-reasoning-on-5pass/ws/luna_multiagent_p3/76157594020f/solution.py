class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def feasible(limit: int) -> bool:
            if limit == 1:
                flips_start_zero = 0
                flips_start_one = 0

                for i, ch in enumerate(s):
                    expected_zero = '0' if i % 2 == 0 else '1'
                    expected_one = '1' if i % 2 == 0 else '0'

                    if ch != expected_zero:
                        flips_start_zero += 1
                    if ch != expected_one:
                        flips_start_one += 1

                return min(flips_start_zero, flips_start_one) <= numOps

            required = 0
            i = 0

            while i < n:
                j = i + 1
                while j < n and s[j] == s[i]:
                    j += 1

                required += (j - i) // (limit + 1)
                if required > numOps:
                    return False

                i = j

            return True

        left, right = 1, n

        while left < right:
            mid = (left + right) // 2
            if feasible(mid):
                right = mid
            else:
                left = mid + 1

        return left