class Solution:
    def makeStringGood(self, s: str) -> int:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1

        max_count = max(count)
        answer = len(s)

        for k in range(1, max_count + 1):
            # dp[0/1]: minimum cost through the current letter when its
            # final frequency is respectively 0 or k.
            dp = [count[0], abs(count[0] - k)]

            for i in range(1, 26):
                next_dp = [10**9, 10**9]

                for previous_kept in range(2):
                    previous_target = k if previous_kept else 0
                    surplus = max(0, count[i - 1] - previous_target)

                    for current_kept in range(2):
                        current_target = k if current_kept else 0
                        deficit = max(0, current_target - count[i])

                        # Converting a surplus previous letter into a deficit
                        # current letter costs 1 instead of delete + insert,
                        # saving one operation per converted character.
                        saving = min(surplus, deficit)

                        next_dp[current_kept] = min(
                            next_dp[current_kept],
                            dp[previous_kept]
                            + abs(count[i] - current_target)
                            - saving,
                        )

                dp = next_dp

            answer = min(answer, dp[0], dp[1])

        return answer