from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        ALPHA = 26
        STATES = 78
        INF = 1_000_000_000

        # dp[i][run_category][character]:
        # Minimum cost for positions i..n-1, given that the previous
        # output character is character and its current run category is:
        # 0: length 1, 1: length 2, 2: length at least 3.
        dp = array("I", [INF]) * ((n + 1) * STATES)

        # At the end, the final run must already have length at least 3.
        base = n * STATES
        for c in range(ALPHA):
            dp[base + 2 * ALPHA + c] = 0

        chars = [ord(ch) - ord("a") for ch in caption]

        for i in range(n - 1, -1, -1):
            cur = i * STATES
            nxt = (i + 1) * STATES
            source = chars[i]

            # Best cost of beginning a new run with each possible target.
            # Obtain the best value excluding any given current character
            # through the global best and second-best values.
            best1 = INF
            best2 = INF
            best_char = -1

            for target in range(ALPHA):
                value = abs(source - target) + dp[nxt + target]
                if value < best1:
                    best2 = best1
                    best1 = value
                    best_char = target
                elif value < best2:
                    best2 = value

            for c in range(ALPHA):
                change_cost = abs(source - c)

                # Continuing a run of length 1 makes it length 2.
                dp[cur + c] = change_cost + dp[nxt + ALPHA + c]

                # Continuing a run of length 2 makes it valid.
                dp[cur + ALPHA + c] = (
                    change_cost + dp[nxt + 2 * ALPHA + c]
                )

                # A valid run may continue or switch to another character.
                continue_cost = change_cost + dp[nxt + 2 * ALPHA + c]
                switch_cost = best2 if best_char == c else best1
                dp[cur + 2 * ALPHA + c] = min(continue_cost, switch_cost)

        # Select the lexicographically smallest optimal first character.
        optimal = INF
        first_char = -1
        for c in range(ALPHA):
            value = abs(chars[0] - c) + dp[STATES + c]
            if value < optimal:
                optimal = value
                first_char = c

        result = [chr(ord("a") + first_char)]
        current_char = first_char
        run_category = 0

        # Greedily take the smallest character preserving optimal DP cost.
        for i in range(1, n):
            state_value = dp[
                i * STATES + run_category * ALPHA + current_char
            ]
            source = chars[i]

            for target in range(ALPHA):
                if target == current_char:
                    next_category = min(2, run_category + 1)
                else:
                    if run_category != 2:
                        continue
                    next_category = 0

                value = abs(source - target) + dp[
                    (i + 1) * STATES + next_category * ALPHA + target
                ]

                if value == state_value:
                    result.append(chr(ord("a") + target))
                    current_char = target
                    run_category = next_category
                    break

        return "".join(result)