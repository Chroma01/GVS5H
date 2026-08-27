class Solution:
    def makeStringGood(self, s: str) -> int:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord('a')] += 1

        n = len(s)
        answer = n

        candidates = {1}
        for value in counts:
            if value > 0:
                candidates.add(value)

        for i in range(26):
            for j in range(i + 1, 26):
                total = counts[i] + counts[j]
                candidates.add(total // 2)
                candidates.add((total + 1) // 2)

        inf = 10**18

        for target in candidates:
            if target <= 0 or target > n:
                continue

            dp = [inf] * (target + 1)
            dp[0] = 0

            for original in counts[:25]:
                prefix = [inf] * (target + 1)
                best = inf
                for incoming in range(target + 1):
                    best = min(best, dp[incoming] - incoming)
                    prefix[incoming] = best

                suffix = [inf] * (target + 1)
                best = inf
                for incoming in range(target, -1, -1):
                    best = min(best, dp[incoming] + incoming)
                    suffix[incoming] = best

                next_dp = [inf] * (target + 1)

                for final_count in (0, target):
                    shift = original - final_count

                    for outgoing in range(target + 1):
                        t = outgoing - shift

                        if t < 0:
                            transition = suffix[0] - t
                        elif t > target:
                            transition = prefix[target] + t
                        else:
                            transition = min(
                                prefix[t] + t,
                                suffix[t] - t,
                            )

                        next_dp[outgoing] = min(
                            next_dp[outgoing],
                            transition + outgoing,
                        )

                dp = next_dp

            original = counts[25]
            best_final = inf

            for incoming, base in enumerate(dp):
                best_final = min(
                    best_final,
                    base + original + incoming,
                    base + abs(original + incoming - target),
                )

            answer = min(answer, best_final)

        return answer