class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def feasible(limit: int) -> bool:
            if limit == 1:
                changes_start_with_zero = 0
                changes_start_with_one = 0

                for i, ch in enumerate(s):
                    expected_if_zero = '0' if i % 2 == 0 else '1'
                    if ch != expected_if_zero:
                        changes_start_with_zero += 1
                    else:
                        changes_start_with_one += 1

                return min(changes_start_with_zero, changes_start_with_one) <= numOps

            operations = 0
            i = 0

            while i < n:
                j = i + 1
                while j < n and s[j] == s[i]:
                    j += 1

                operations += (j - i) // (limit + 1)
                if operations > numOps:
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