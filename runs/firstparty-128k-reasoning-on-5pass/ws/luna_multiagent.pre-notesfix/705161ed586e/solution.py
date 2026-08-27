from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        source = [ord(ch) - ord("a") for ch in caption]
        INF = 10**9

        # dp1[c][i]: minimum cost for positions i..n-1 when the current
        # run is character c and currently has length exactly 1.
        # dp2[c][i]: same, with current run length exactly 2.
        # dp3[c][i]: same, with current run length at least 3.
        dp1 = [array("i", [INF]) * (n + 1) for _ in range(26)]
        dp2 = [array("i", [INF]) * (n + 1) for _ in range(26)]
        dp3 = [array("i", [INF]) * (n + 1) for _ in range(26)]

        # At the end, only a completed run is valid.
        for c in range(26):
            dp3[c][n] = 0

        for i in range(n - 1, -1, -1):
            value = source[i]

            # Cost of switching to each possible new character.
            switch_cost = [
                abs(value - nxt) + dp1[nxt][i + 1]
                for nxt in range(26)
            ]

            # Find the smallest and second-smallest switch costs.
            best1 = INF
            best2 = INF
            best_char = -1

            for nxt, cost in enumerate(switch_cost):
                if cost < best1:
                    best2 = best1
                    best1 = cost
                    best_char = nxt
                elif cost < best2:
                    best2 = cost

            for c in range(26):
                cost = abs(value - c)

                # Runs of lengths 1 and 2 must continue.
                dp1[c][i] = cost + dp2[c][i + 1]
                dp2[c][i] = cost + dp3[c][i + 1]

                # A completed run may continue or switch character.
                best_switch = best2 if c == best_char else best1
                dp3[c][i] = min(
                    cost + dp3[c][i + 1],
                    best_switch,
                )

        # Choose the first character.
        best_cost = INF
        first_char = -1

        for c in range(26):
            cost = abs(source[0] - c) + dp1[c][1]
            if cost < best_cost:
                best_cost = cost
                first_char = c

        if first_char == -1 or best_cost >= INF:
            return ""

        # Greedily reconstruct the lexicographically smallest optimal answer.
        answer = [first_char]
        current_char = first_char
        state = 0  # 0: length 1, 1: length 2, 2: length at least 3

        for i in range(1, n):
            if state == 0:
                target_cost = dp1[current_char][i]
            elif state == 1:
                target_cost = dp2[current_char][i]
            else:
                target_cost = dp3[current_char][i]

            for nxt in range(26):
                if nxt == current_char:
                    next_state = min(2, state + 1)
                else:
                    if state != 2:
                        continue
                    next_state = 0

                if next_state == 0:
                    suffix_cost = dp1[nxt][i + 1]
                elif next_state == 1:
                    suffix_cost = dp2[nxt][i + 1]
                else:
                    suffix_cost = dp3[nxt][i + 1]

                candidate = abs(source[i] - nxt) + suffix_cost

                if candidate == target_cost:
                    answer.append(nxt)
                    current_char = nxt
                    state = next_state
                    break

        return "".join(chr(c + ord("a")) for c in answer)