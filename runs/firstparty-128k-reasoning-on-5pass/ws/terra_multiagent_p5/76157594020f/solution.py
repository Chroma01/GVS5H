class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def feasible(max_run: int) -> bool:
            if max_run == 1:
                flips_start_zero = 0
                flips_start_one = 0

                for i, ch in enumerate(s):
                    if ch != ('0' if i % 2 == 0 else '1'):
                        flips_start_zero += 1
                    if ch != ('1' if i % 2 == 0 else '0'):
                        flips_start_one += 1

                return min(flips_start_zero, flips_start_one) <= numOps

            needed = 0
            run_length = 1

            for i in range(1, n):
                if s[i] == s[i - 1]:
                    run_length += 1
                else:
                    needed += run_length // (max_run + 1)
                    if needed > numOps:
                        return False
                    run_length = 1

            needed += run_length // (max_run + 1)
            return needed <= numOps

        left, right = 1, n

        while left < right:
            mid = (left + right) // 2
            if feasible(mid):
                right = mid
            else:
                left = mid + 1

        return left