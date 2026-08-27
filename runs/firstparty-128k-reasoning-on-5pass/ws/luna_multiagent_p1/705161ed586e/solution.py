from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 10**9
        values = [ord(ch) - ord('a') for ch in caption]
        states = 26 * 3

        # layers[i][letter * 3 + run_class]:
        # minimum cost for positions i..n-1, assuming the preceding run
        # has the given letter and length class.
        # run_class: 0 => length 1, 1 => length 2, 2 => length at least 3.
        layers = [None] * (n + 1)

        terminal = array('i', [INF]) * states
        for c in range(26):
            terminal[c * 3 + 2] = 0
        layers[n] = terminal

        for i in range(n - 1, 0, -1):
            nxt = layers[i + 1]
            cur = array('i', [0]) * states
            w = values[i]

            # Minimum and second minimum costs for switching to a new
            # character. A new run starts with length class 0.
            best1 = INF
            best2 = INF
            best_letter = -1

            for x in range(26):
                val = nxt[x * 3] + abs(w - x)
                if val < best1:
                    best2 = best1
                    best1 = val
                    best_letter = x
                elif val < best2:
                    best2 = val

            for c in range(26):
                base = c * 3
                cost_same = abs(w - c)

                # A run of length 1 must continue.
                cur[base] = cost_same + nxt[base + 1]

                # A run of length 2 must continue to become valid.
                cur[base + 1] = cost_same + nxt[base + 2]

                # A valid run may continue or switch to another character.
                switch_cost = best1 if best_letter != c else best2
                extend_cost = cost_same + nxt[base + 2]
                cur[base + 2] = min(extend_cost, switch_cost)

            layers[i] = cur

        # Select the lexicographically smallest first character among
        # all globally minimum-cost choices.
        first_cost = INF
        first_letter = -1

        for c in range(26):
            cost = abs(values[0] - c) + layers[1][c * 3]
            if cost < first_cost:
                first_cost = cost
                first_letter = c

        if first_letter < 0 or first_cost >= INF:
            return ""

        result = [chr(first_letter + ord('a'))]
        current_letter = first_letter
        run_class = 0

        for i in range(1, n):
            target_cost = layers[i][current_letter * 3 + run_class]
            chosen = -1
            next_class = -1

            # Testing letters in order guarantees lexicographically smallest
            # reconstruction among all optimal solutions.
            for x in range(26):
                if x == current_letter:
                    nc = min(2, run_class + 1)
                elif run_class == 2:
                    nc = 0
                else:
                    continue

                candidate = (
                    abs(values[i] - x)
                    + layers[i + 1][x * 3 + nc]
                )

                if candidate == target_cost:
                    chosen = x
                    next_class = nc
                    break

            if chosen < 0:
                return ""

            result.append(chr(chosen + ord('a')))
            current_letter = chosen
            run_class = next_class

        return ''.join(result)