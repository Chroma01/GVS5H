from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 10**18
        states = 78  # 26 letters * 3 run-length categories
        total = (n + 1) * states
        dp = array("q", [INF]) * total

        # At position n, only a completed final run is valid.
        end_base = n * states
        for letter in range(26):
            dp[end_base + 52 + letter] = 0

        # State categories:
        # 0: current run has length 1
        # 1: current run has length 2
        # 2: current run has length at least 3
        for i in range(n - 1, -1, -1):
            cur_base = i * states
            next_base = (i + 1) * states
            original = ord(caption[i]) - ord("a")

            # For switching from a completed run, choose a new letter at i.
            # The suffix then starts with a run of length 1.
            best1 = INF
            best2 = INF
            best_letter = -1

            for letter in range(26):
                value = abs(original - letter) + dp[next_base + letter]
                if value < best1:
                    best2 = best1
                    best1 = value
                    best_letter = letter
                elif value < best2:
                    best2 = value

            for letter in range(26):
                cost = abs(original - letter)

                # Existing run has length 1 and must continue.
                dp[cur_base + letter] = (
                    cost + dp[next_base + 26 + letter]
                )

                # Existing run has length 2 and must continue.
                dp[cur_base + 26 + letter] = (
                    cost + dp[next_base + 52 + letter]
                )

                # Existing run is complete: continue or switch.
                continue_cost = cost + dp[next_base + 52 + letter]
                switch_cost = best2 if best_letter == letter else best1
                dp[cur_base + 52 + letter] = min(
                    continue_cost,
                    switch_cost,
                )

        # Select the smallest initial letter among minimum-cost solutions.
        original = ord(caption[0]) - ord("a")
        optimum = INF
        first_letter = -1

        for letter in range(26):
            value = abs(original - letter) + dp[states + 26 + letter]
            if value < optimum:
                optimum = value
                first_letter = letter

        if first_letter == -1 or optimum >= INF:
            return ""

        result = [chr(first_letter + ord("a"))]
        current_letter = first_letter
        category = 0  # The first output character creates a run of length 1.

        # Greedily choose the lexicographically smallest valid next character.
        for i in range(1, n):
            base = i * states
            next_base = (i + 1) * states
            original = ord(caption[i]) - ord("a")
            required = dp[base + category * 26 + current_letter]

            chosen = -1
            chosen_category = -1

            for letter in range(26):
                cost = abs(original - letter)

                if letter == current_letter:
                    next_category = min(2, category + 1)
                    value = (
                        cost
                        + dp[next_base + next_category * 26 + letter]
                    )
                    if value == required:
                        chosen = letter
                        chosen_category = next_category
                        break

                elif category == 2:
                    # Switching is allowed only after a completed run.
                    value = cost + dp[next_base + letter]
                    if value == required:
                        chosen = letter
                        chosen_category = 0
                        break

            if chosen == -1:
                return ""

            result.append(chr(chosen + ord("a")))
            current_letter = chosen
            category = chosen_category

        return "".join(result)