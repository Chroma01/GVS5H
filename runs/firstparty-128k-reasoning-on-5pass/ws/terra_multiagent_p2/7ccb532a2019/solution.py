class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1

        n = len(s)

        # Empty string is good: delete everything.
        answer = n

        for k in range(1, n + 1):
            # dp[state]:
            # minimum cost after processing the previous letter.
            # state 0 means its target frequency is 0;
            # state 1 means its target frequency is k.
            dp = [cnt[0], abs(cnt[0] - k)]

            for i in range(1, 26):
                ndp = [10**9, 10**9]

                for cur_state in range(2):
                    cur_target = k if cur_state else 0
                    base_cost = abs(cnt[i] - cur_target)

                    for prev_state in range(2):
                        prev_target = k if prev_state else 0

                        # Converting an excess of letter i - 1 into a
                        # missing letter i costs 1, rather than one deletion
                        # plus one insertion, which costs 2.
                        surplus = cnt[i - 1] - prev_target
                        deficit = cur_target - cnt[i]

                        saving = 0
                        if surplus > 0 and deficit > 0:
                            saving = min(surplus, deficit)

                        ndp[cur_state] = min(
                            ndp[cur_state],
                            dp[prev_state] + base_cost - saving
                        )

                dp = ndp

            answer = min(answer, dp[0], dp[1])

        return answer