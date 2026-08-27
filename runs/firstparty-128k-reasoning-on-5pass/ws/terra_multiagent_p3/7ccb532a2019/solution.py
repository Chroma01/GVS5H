class Solution:
    def makeStringGood(self, s: str) -> int:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1

        max_count = max(count)
        answer = len(s)

        for k in range(1, max_count + 1):
            # dp[state] is the minimum cost through the previous letter.
            # state 0: previous letter is excluded (target count 0)
            # state 1: previous letter is included (target count k)
            dp = [count[0], abs(count[0] - k)]

            for i in range(1, 26):
                next_dp = [0, 0]

                for current_state in range(2):
                    current_target = current_state * k
                    base_cost = abs(count[i] - current_target)

                    best = float("inf")
                    for previous_state in range(2):
                        previous_target = previous_state * k

                        # A conversion from i - 1 to i costs 1, while
                        # deleting then inserting costs 2, so each useful
                        # adjacent conversion saves exactly 1 operation.
                        surplus_previous = max(
                            0, count[i - 1] - previous_target
                        )
                        deficit_current = max(
                            0, current_target - count[i]
                        )
                        saving = min(surplus_previous, deficit_current)

                        best = min(
                            best,
                            dp[previous_state] + base_cost - saving
                        )

                    next_dp[current_state] = best

                dp = next_dp

            answer = min(answer, dp[0], dp[1])

        return answer