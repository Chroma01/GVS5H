from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        m = 26
        INF = 1_000_000_000
        size = (n + 1) * m

        # dp1[i][c], dp2[i][c], dp3[i][c] are minimum suffix costs where
        # caption[i] is converted to c and its run has current length
        # exactly 1, exactly 2, or at least 3, respectively.
        dp1 = array("i", [INF]) * size
        dp2 = array("i", [INF]) * size
        dp3 = array("i", [INF]) * size

        # A completed run is valid at the virtual end position.
        end = n * m
        for c in range(m):
            dp3[end + c] = 0

        source = [ord(ch) - ord("a") for ch in caption]

        for i in range(n - 1, -1, -1):
            cur = i * m
            nxt = (i + 1) * m

            # Find the smallest and second-smallest dp1 values at i + 1.
            # The second smallest can equal the first due to tied letters.
            best1 = INF
            best2 = INF
            best_char = -1

            for c in range(m):
                value = dp1[nxt + c]
                if value < best1:
                    best2 = best1
                    best1 = value
                    best_char = c
                elif value < best2:
                    best2 = value

            original = source[i]
            for c in range(m):
                change_cost = abs(original - c)

                # A run of length 1 or 2 must continue with the same letter.
                dp1[cur + c] = change_cost + dp2[nxt + c]
                dp2[cur + c] = change_cost + dp3[nxt + c]

                # A completed run may continue or start a different run.
                start_new_cost = best2 if c == best_char else best1
                dp3[cur + c] = change_cost + min(dp3[nxt + c], start_new_cost)

        # The first output character begins a new run.
        first = 0
        optimum = dp1[0]
        for c in range(1, m):
            if dp1[c] < optimum:
                optimum = dp1[c]
                first = c

        answer = [chr(first + ord("a"))]
        current_char = first
        run_status = 1

        for i in range(n - 1):
            cur = i * m
            nxt = (i + 1) * m

            if run_status == 1:
                run_status = 2
            elif run_status == 2:
                run_status = 3
            else:
                remaining_cost = dp3[cur + current_char] - abs(
                    source[i] - current_char
                )

                # First feasible candidate gives lexicographically smallest answer.
                for candidate in range(m):
                    if candidate == current_char:
                        suffix_cost = dp3[nxt + candidate]
                        next_status = 3
                    else:
                        suffix_cost = dp1[nxt + candidate]
                        next_status = 1

                    if suffix_cost == remaining_cost:
                        current_char = candidate
                        run_status = next_status
                        break

            answer.append(chr(current_char + ord("a")))

        return "".join(answer)