class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        runs = []
        start = 0
        for i in range(1, n + 1):
            if i == n or s[i] != s[start]:
                runs.append(i - start)
                start = i

        def feasible(limit: int) -> bool:
            if limit == 1:
                flips_start_zero = 0
                flips_start_one = 0

                for i, ch in enumerate(s):
                    if ch != ('0' if i % 2 == 0 else '1'):
                        flips_start_zero += 1
                    if ch != ('1' if i % 2 == 0 else '0'):
                        flips_start_one += 1

                return min(flips_start_zero, flips_start_one) <= numOps

            needed = 0
            for length in runs:
                needed += length // (limit + 1)
                if needed > numOps:
                    return False
            return True

        left, right = 1, n
        while left < right:
            mid = (left + right) // 2
            if feasible(mid):
                right = mid
            else:
                left = mid + 1

        return left