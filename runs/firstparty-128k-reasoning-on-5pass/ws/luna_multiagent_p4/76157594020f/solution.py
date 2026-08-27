class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def can(max_run: int) -> bool:
            # With maximum run length one, the final string must alternate.
            if max_run == 1:
                mismatches_start_0 = 0
                mismatches_start_1 = 0

                for i, ch in enumerate(s):
                    expected0 = '0' if i % 2 == 0 else '1'
                    expected1 = '1' if i % 2 == 0 else '0'
                    mismatches_start_0 += ch != expected0
                    mismatches_start_1 += ch != expected1

                return min(mismatches_start_0, mismatches_start_1) <= numOps

            inf = n + 1

            # dp[bit][run_length - 1] is the minimum flips needed after
            # processing the current prefix, ending with bit and this run length.
            dp0 = [inf] * max_run
            dp1 = [inf] * max_run

            dp0[0] = (s[0] != '0')
            dp1[0] = (s[0] != '1')

            for ch in s[1:]:
                cost0 = ch != '0'
                cost1 = ch != '1'
                ndp0 = [inf] * max_run
                ndp1 = [inf] * max_run

                # Change the final bit, starting a new run of length one.
                ndp0[0] = min(dp1) + cost0
                ndp1[0] = min(dp0) + cost1

                # Keep the final bit, extending its run.
                for run_index in range(1, max_run):
                    ndp0[run_index] = dp0[run_index - 1] + cost0
                    ndp1[run_index] = dp1[run_index - 1] + cost1

                dp0, dp1 = ndp0, ndp1

            return min(min(dp0), min(dp1)) <= numOps

        left, right = 1, n
        while left < right:
            mid = (left + right) // 2
            if can(mid):
                right = mid
            else:
                left = mid + 1

        return left