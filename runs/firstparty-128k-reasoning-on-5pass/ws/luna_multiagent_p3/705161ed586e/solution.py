from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        values = [ord(ch) - ord("a") for ch in caption]
        INF = 10**9

        # State: character * 3 + maturity
        # maturity 0: current run has length 1
        # maturity 1: current run has length 2
        # maturity 2: current run has length at least 3
        dp = [array("i", [INF]) * (n + 1) for _ in range(78)]

        # At the end, only a mature final run is valid.
        for c in range(26):
            dp[c * 3 + 2][n] = 0

        for i in range(n - 1, -1, -1):
            source = values[i]
            nxt = [dp[state][i + 1] for state in range(78)]

            # Cost of changing position i to x and starting a new run.
            change_cost = [
                abs(source - x) + nxt[x * 3]
                for x in range(26)
            ]

            # Best and second-best values, allowing exclusion of one character.
            best1 = INF
            best2 = INF
            best_char = -1

            for x, value in enumerate(change_cost):
                if value < best1:
                    best2 = best1
                    best1 = value
                    best_char = x
                elif value < best2:
                    best2 = value

            for c in range(26):
                base = c * 3
                cost = abs(source - c)

                # Continue a run of length 1 or 2.
                dp[base][i] = cost + nxt[base + 1]
                dp[base + 1][i] = cost + nxt[base + 2]

                # Continue a mature run, or switch to another character.
                continue_same = cost + nxt[base + 2]
                switch = best2 if c == best_char else best1
                dp[base + 2][i] = min(continue_same, switch)

        # Select the lexicographically smallest optimal first character.
        best_total = INF
        first_char = -1

        for c in range(26):
            total = abs(values[0] - c) + dp[c * 3][1]
            if total < best_total:
                best_total = total
                first_char = c

        if first_char == -1 or best_total >= INF:
            return ""

        result = [chr(first_char + ord("a"))]
        current_char = first_char
        maturity = 0

        for i in range(1, n):
            state = current_char * 3 + maturity
            target_cost = dp[state][i]

            chosen = -1
            next_maturity = -1

            # Trying characters in ascending order enforces lexicographic
            # minimality among all globally optimal solutions.
            for x in range(26):
                if x == current_char:
                    nm = min(2, maturity + 1)
                else:
                    if maturity != 2:
                        continue
                    nm = 0

                candidate = (
                    abs(values[i] - x)
                    + dp[x * 3 + nm][i + 1]
                )

                if candidate == target_cost:
                    chosen = x
                    next_maturity = nm
                    break

            if chosen == -1:
                return ""

            result.append(chr(chosen + ord("a")))
            current_char = chosen
            maturity = next_maturity

        if maturity != 2:
            return ""

        return "".join(result)