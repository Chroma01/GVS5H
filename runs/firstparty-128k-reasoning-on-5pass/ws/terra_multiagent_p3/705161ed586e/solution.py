from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        m = 26
        INF = 1_000_000_000
        vals = [ord(ch) - ord('a') for ch in caption]

        # d1[i, c], d2[i, c], d3[i, c]:
        # minimum suffix cost beginning at i when the previous output
        # character is c and its run currently has length 1, 2, or >= 3.
        size = (n + 1) * m
        d1 = array('i', [INF]) * size
        d2 = array('i', [INF]) * size
        d3 = array('i', [INF]) * size

        # At the end, only a completed final run is valid.
        end = n * m
        for c in range(m):
            d3[end + c] = 0

        for i in range(n - 1, -1, -1):
            base = i * m
            nxt = base + m
            source = vals[i]

            best1 = INF
            best2 = INF
            best_idx = -1

            # Find min over x != c of:
            # abs(source - x) + d1[i + 1][x]
            for c in range(m):
                value = abs(source - c) + d1[nxt + c]
                if value < best1:
                    best2 = best1
                    best1 = value
                    best_idx = c
                elif value < best2:
                    best2 = value

            for c in range(m):
                change_cost = abs(source - c)

                # Short runs are forced to continue.
                d1[base + c] = change_cost + d2[nxt + c]
                d2[base + c] = change_cost + d3[nxt + c]

                # A completed run may continue or start a different run.
                continue_cost = change_cost + d3[nxt + c]
                switch_cost = best2 if c == best_idx else best1
                d3[base + c] = min(continue_cost, switch_cost)

        # Select the smallest first character among minimum-cost answers.
        optimal = INF
        first = 0
        for c in range(m):
            value = abs(vals[0] - c) + d1[m + c]
            if value < optimal:
                optimal = value
                first = c

        result = [chr(first + ord('a'))]
        prev = first
        run_state = 1

        # At every unrestricted position, choose the smallest character that
        # realizes the already-computed optimal suffix cost.
        for i in range(1, n):
            base = i * m
            nxt = base + m
            source = vals[i]

            if run_state == 1:
                chosen = prev
                run_state = 2
            elif run_state == 2:
                chosen = prev
                run_state = 3
            else:
                current_best = d3[base + prev]
                chosen = prev

                for c in range(m):
                    if c == prev:
                        value = abs(source - c) + d3[nxt + c]
                    else:
                        value = abs(source - c) + d1[nxt + c]

                    if value == current_best:
                        chosen = c
                        break

                run_state = 3 if chosen == prev else 1

            result.append(chr(chosen + ord('a')))
            prev = chosen

        return "".join(result)