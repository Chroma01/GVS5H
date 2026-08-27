class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        n = len(s)
        mx = max(cnt)
        candidates = {1, mx}

        # Breakpoints from contiguous alphabet intervals.
        for left in range(26):
            total = 0
            length = 0
            for right in range(left, 26):
                total += cnt[right]
                length += 1
                candidates.add(total // length)
                candidates.add((total + length - 1) // length)

        # Breakpoints caused by separated positive-frequency letters.
        positive = [x for x in cnt if x]
        for i, x in enumerate(positive):
            for y in positive[i:]:
                candidates.add((x + y) // 2)
                candidates.add((x + y + 1) // 2)

        candidates = sorted(k for k in candidates if 1 <= k <= mx)

        answer = n
        inf = 10**18

        for k in candidates:
            # dp[x] is the minimum cost after processing the current prefix,
            # with x characters forwarded to the next letter.
            dp = [inf] * (k + 1)
            dp[0] = 0

            for letter in range(26):
                c = cnt[letter]

                if letter == 25:
                    best = inf
                    for carried, cost in enumerate(dp):
                        available = c + carried

                        # Omit z, or retain exactly k copies of z.
                        best = min(
                            best,
                            cost + available,
                            cost + abs(available - k),
                        )
                    dp = [best]
                    break

                # suffix[x] = min(dp[u] + u) for u >= x
                suffix = [inf] * (k + 2)
                for x in range(k, -1, -1):
                    suffix[x] = min(suffix[x + 1], dp[x] + x)

                # prefix[x] = min(dp[u] - u) for u <= x
                prefix = [inf] * (k + 1)
                best_prefix = inf
                for x in range(k + 1):
                    best_prefix = min(best_prefix, dp[x] - x)
                    prefix[x] = best_prefix

                next_dp = [inf] * (k + 1)

                # Current letter is absent from the final string.
                for outgoing in range(k + 1):
                    threshold = max(0, outgoing - c)
                    next_dp[outgoing] = c + suffix[threshold]

                # Current letter occurs exactly k times.
                missing = k - c

                if missing > 0:
                    # Incoming characters are insufficient; insert the rest.
                    limit = min(k, missing - 1)
                    if limit >= 0:
                        next_dp[0] = min(
                            next_dp[0],
                            missing + prefix[limit],
                        )

                    # Incoming characters fill the deficit; extras are forwarded.
                    for outgoing in range(k + 1):
                        threshold = missing + outgoing
                        if threshold <= k:
                            next_dp[outgoing] = min(
                                next_dp[outgoing],
                                c - k + suffix[threshold],
                            )
                else:
                    # Native copies already provide k final copies.
                    # Only excess incoming characters may be forwarded.
                    for outgoing in range(k + 1):
                        next_dp[outgoing] = min(
                            next_dp[outgoing],
                            c - k + suffix[outgoing],
                        )

                dp = next_dp

            answer = min(answer, dp[0])

        return answer