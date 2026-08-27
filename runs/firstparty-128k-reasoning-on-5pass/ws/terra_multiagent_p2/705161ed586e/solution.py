from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        A = 26
        INF = 10**9
        vals = [ord(ch) - ord('a') for ch in caption]
        size = (n + 1) * A

        # f1/f2/f3[i, c] are minimum suffix costs from i onward when the
        # preceding run uses letter c and currently has length 1, 2, or >= 3.
        f1 = array('i', [INF]) * size
        f2 = array('i', [INF]) * size
        f3 = array('i', [INF]) * size

        end_base = n * A
        for c in range(A):
            f3[end_base + c] = 0

        for i in range(n - 1, -1, -1):
            cur_base = i * A
            next_base = (i + 1) * A
            original = vals[i]

            # Find the lowest and second-lowest costs for beginning a new
            # run at i with each possible target character.
            best1 = INF
            best2 = INF
            best_char = -1

            for x in range(A):
                value = abs(original - x) + f1[next_base + x]

                if value < best1:
                    best2 = best1
                    best1 = value
                    best_char = x
                elif value == best1:
                    # A tied optimum remains usable if best_char is excluded.
                    best2 = best1
                elif value < best2:
                    best2 = value

            for c in range(A):
                change_cost = abs(original - c)

                # A run of length 1 or 2 must continue with its own letter.
                f1[cur_base + c] = change_cost + f2[next_base + c]
                f2[cur_base + c] = change_cost + f3[next_base + c]

                # A completed run can continue, or start a distinct new run.
                continue_cost = change_cost + f3[next_base + c]
                switch_cost = best2 if c == best_char else best1
                f3[cur_base + c] = min(continue_cost, switch_cost)

        # Choose the smallest first letter among all globally optimal choices.
        best_total = INF
        first_char = 0
        for c in range(A):
            cost = abs(vals[0] - c) + f1[A + c]
            if cost < best_total:
                best_total = cost
                first_char = c

        result = [chr(ord('a') + first_char)]
        current_char = first_char
        state = 1

        # Greedily choose the smallest character preserving optimal DP cost.
        for i in range(1, n):
            cur_base = i * A
            next_base = (i + 1) * A

            if state == 1:
                expected = f1[cur_base + current_char]
            elif state == 2:
                expected = f2[cur_base + current_char]
            else:
                expected = f3[cur_base + current_char]

            for x in range(A):
                if x == current_char:
                    next_state = 2 if state == 1 else 3
                else:
                    if state != 3:
                        continue
                    next_state = 1

                if next_state == 1:
                    future = f1[next_base + x]
                elif next_state == 2:
                    future = f2[next_base + x]
                else:
                    future = f3[next_base + x]

                if abs(vals[i] - x) + future == expected:
                    result.append(chr(ord('a') + x))
                    current_char = x
                    state = next_state
                    break

        return "".join(result)