class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def feasible(limit: int) -> bool:
            if limit == 1:
                mismatch_start_zero = 0
                mismatch_start_one = 0

                for i, ch in enumerate(s):
                    if ch != ('0' if i % 2 == 0 else '1'):
                        mismatch_start_zero += 1
                    if ch != ('1' if i % 2 == 0 else '0'):
                        mismatch_start_one += 1

                return min(mismatch_start_zero, mismatch_start_one) <= numOps

            flips_needed = 0
            run_length = 1

            for i in range(1, n + 1):
                if i < n and s[i] == s[i - 1]:
                    run_length += 1
                else:
                    flips_needed += run_length // (limit + 1)
                    if flips_needed > numOps:
                        return False
                    run_length = 1

            return True

        left, right = 1, n

        while left < right:
            mid = (left + right) // 2
            if feasible(mid):
                right = mid
            else:
                left = mid + 1

        return left