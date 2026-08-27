from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 10**9
        width = 26
        total_size = (n + 1) * width

        # State at position i, given that the preceding character is c:
        # d1: current run of c has length 1
        # d2: current run of c has length 2
        # d3: current run of c has length at least 3
        d1 = array("i", [0]) * total_size
        d2 = array("i", [0]) * total_size
        d3 = array("i", [0]) * total_size

        end = n * width
        for c in range(width):
            d1[end + c] = INF
            d2[end + c] = INF
            d3[end + c] = 0

        for i in range(n - 1, -1, -1):
            cur = i * width
            nxt = cur + width
            source = ord(caption[i]) - ord("a")

            best_value = INF
            second_value = INF
            best_char = -1

            # Values for starting a new run with target letter c:
            # abs(source-c) + d1[i+1][c].
            for c in range(width):
                cost = abs(source - c)

                # A run of length 1 or 2 cannot be changed yet.
                d1[cur + c] = cost + d2[nxt + c]
                d2[cur + c] = cost + d3[nxt + c]

                value = cost + d1[nxt + c]
                if value < best_value:
                    second_value = best_value
                    best_value = value
                    best_char = c
                elif value < second_value:
                    second_value = value

            # A valid run can either continue with c or switch to another letter.
            for c in range(width):
                cost = abs(source - c)
                continue_cost = cost + d3[nxt + c]
                switch_cost = second_value if c == best_char else best_value
                d3[cur + c] = min(continue_cost, switch_cost)

        # Select the first target character. Iterating in increasing order
        # automatically handles lexicographic tie-breaking for position 0.
        source0 = ord(caption[0]) - ord("a")
        best_total = INF
        first_char = 0

        for c in range(width):
            value = abs(source0 - c) + d1[width + c]
            if value < best_total:
                best_total = value
                first_char = c

        result = [chr(first_char + ord("a"))]
        prev = first_char
        run_state = 1
        remaining = d1[width + first_char]

        # Reconstruct left to right. At a completed run, choose the smallest
        # letter preserving the optimal remaining DP value.
        for i in range(1, n):
            nxt = (i + 1) * width
            source = ord(caption[i]) - ord("a")

            if run_state == 1:
                result.append(chr(prev + ord("a")))
                remaining = d2[nxt + prev]
                run_state = 2

            elif run_state == 2:
                result.append(chr(prev + ord("a")))
                remaining = d3[nxt + prev]
                run_state = 3

            else:
                for c in range(width):
                    cost = abs(source - c)
                    if c == prev:
                        next_cost = d3[nxt + c]
                        next_state = 3
                    else:
                        next_cost = d1[nxt + c]
                        next_state = 1

                    if cost + next_cost == remaining:
                        result.append(chr(c + ord("a")))
                        prev = c
                        run_state = next_state
                        remaining = next_cost
                        break

        return "".join(result)