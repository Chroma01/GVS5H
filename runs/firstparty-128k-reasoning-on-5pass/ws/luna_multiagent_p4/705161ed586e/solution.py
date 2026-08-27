class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        # State status:
        # 0 -> current run has length 1
        # 1 -> current run has length 2
        # 2 -> current run has length at least 3
        #
        # nxt[letter][status] is the minimum cost for the suffix after
        # the currently processed position.
        INF = 10**18
        choices = bytearray(n * 78)

        nxt = [[0, 0, 0] for _ in range(26)]
        for letter in range(26):
            nxt[letter][0] = INF
            nxt[letter][1] = INF
            nxt[letter][2] = 0

        for i in range(n - 1, 0, -1):
            cur_char = ord(caption[i]) - 97

            # If we switch from the previous letter to x, the new run
            # has status 0. Find the two smallest values over x.
            best_cost = INF
            best_letter = -1
            second_cost = INF
            second_letter = -1

            for x in range(26):
                value = abs(cur_char - x) + nxt[x][0]
                if value < best_cost or (
                    value == best_cost and x < best_letter
                ):
                    second_cost, second_letter = best_cost, best_letter
                    best_cost, best_letter = value, x
                elif value < second_cost or (
                    value == second_cost and x < second_letter
                ):
                    second_cost, second_letter = value, x

            cur = [[0, 0, 0] for _ in range(26)]
            offset = i * 78

            for previous in range(26):
                change_cost = abs(cur_char - previous)

                # Status 0: only continue the current run.
                cur[previous][0] = change_cost + nxt[previous][1]
                choices[offset + previous * 3] = previous

                # Status 1: only continue the current run.
                cur[previous][1] = change_cost + nxt[previous][2]
                choices[offset + previous * 3 + 1] = previous

                # Status 2: either continue or start a new run.
                continue_cost = change_cost + nxt[previous][2]

                if best_letter != previous:
                    switch_cost = best_cost
                    switch_letter = best_letter
                else:
                    switch_cost = second_cost
                    switch_letter = second_letter

                if continue_cost < switch_cost or (
                    continue_cost == switch_cost
                    and previous < switch_letter
                ):
                    cur[previous][2] = continue_cost
                    choices[offset + previous * 3 + 2] = previous
                else:
                    cur[previous][2] = switch_cost
                    choices[offset + previous * 3 + 2] = switch_letter

            nxt = cur

        # Choose the first character. It starts a run of length 1.
        first_char = ord(caption[0]) - 97
        best_total = INF
        first_letter = 0

        for x in range(26):
            total = abs(first_char - x) + nxt[x][0]
            if total < best_total:
                best_total = total
                first_letter = x

        answer = [chr(first_letter + 97)]
        previous = first_letter
        status = 0

        # Reconstruct using stored locally lexicographically smallest
        # optimal transitions.
        for i in range(1, n):
            index = i * 78 + previous * 3 + status
            current = choices[index]
            answer.append(chr(current + 97))

            if current == previous:
                if status < 2:
                    status += 1
            else:
                previous = current
                status = 0

        return "".join(answer)