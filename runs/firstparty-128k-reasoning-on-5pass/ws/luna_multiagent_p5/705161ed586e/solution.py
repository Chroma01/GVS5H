class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 10**18
        # State IDs:
        # 0..25   : current run length is 1
        # 26..51  : current run length is 2
        # 52..77  : current run length is at least 3
        A, B, C = 0, 26, 52
        STATES = 78

        values = [ord(ch) - ord('a') for ch in caption]

        prev_cost = [INF] * STATES
        prev_rank = [INF] * STATES

        # Parent state for every position/state. 255 means start of string.
        parent = bytearray([255]) * (n * STATES)

        for pos, value in enumerate(values):
            cur_cost = [INF] * STATES
            cur_parent = [-1] * STATES

            # Two best completed runs, ordered by cost and then
            # lexicographic rank, are enough to start a different run.
            best1 = (-1, INF, INF)
            best2 = (-1, INF, INF)

            if pos > 0:
                for ch in range(26):
                    item = (ch, prev_cost[C + ch], prev_rank[C + ch])
                    key = (item[1], item[2])
                    if key < (best1[1], best1[2]):
                        best2 = best1
                        best1 = item
                    elif key < (best2[1], best2[2]):
                        best2 = item

            for ch in range(26):
                edit = abs(value - ch)

                # Start a new run of length 1.
                if pos == 0:
                    cur_cost[A + ch] = edit
                    cur_parent[A + ch] = 255
                else:
                    chosen = best1 if best1[0] != ch else best2
                    if chosen[0] != -1 and chosen[1] < INF:
                        cur_cost[A + ch] = chosen[1] + edit
                        cur_parent[A + ch] = C + chosen[0]

                # Extend a run of length 1 to length 2.
                if prev_cost[A + ch] < INF:
                    cur_cost[B + ch] = prev_cost[A + ch] + edit
                    cur_parent[B + ch] = A + ch

                # Extend a run of length 2 or an already completed run.
                b_cost = prev_cost[B + ch]
                c_cost = prev_cost[C + ch]

                if b_cost < INF:
                    b_total = b_cost + edit
                else:
                    b_total = INF

                if c_cost < INF:
                    c_total = c_cost + edit
                else:
                    c_total = INF

                if b_total < c_total:
                    cur_cost[C + ch] = b_total
                    cur_parent[C + ch] = B + ch
                elif c_total < b_total:
                    cur_cost[C + ch] = c_total
                    cur_parent[C + ch] = C + ch
                elif b_total < INF:
                    # Equal-cost transitions must use the lexicographically
                    # smaller predecessor prefix.
                    if prev_rank[B + ch] <= prev_rank[C + ch]:
                        cur_cost[C + ch] = b_total
                        cur_parent[C + ch] = B + ch
                    else:
                        cur_cost[C + ch] = c_total
                        cur_parent[C + ch] = C + ch

            # Assign lexicographic ranks to all retained prefixes.
            # Every new prefix is predecessor_prefix + current character.
            order = []
            for state in range(STATES):
                if cur_cost[state] < INF:
                    p = cur_parent[state]
                    predecessor_rank = 0 if p == 255 else prev_rank[p]
                    order.append((predecessor_rank, state % 26, state))

            order.sort()
            cur_rank = [INF] * STATES
            for rank, (_, _, state) in enumerate(order):
                cur_rank[state] = rank

            base = pos * STATES
            for state in range(STATES):
                if cur_parent[state] != -1:
                    parent[base + state] = cur_parent[state]

            prev_cost = cur_cost
            prev_rank = cur_rank

        # The final run must have length at least 3.
        final_state = -1
        for ch in range(26):
            state = C + ch
            if prev_cost[state] >= INF:
                continue

            if final_state == -1 or (
                prev_cost[state],
                prev_rank[state],
            ) < (
                prev_cost[final_state],
                prev_rank[final_state],
            ):
                final_state = state

        if final_state == -1:
            return ""

        result = []
        state = final_state

        for pos in range(n - 1, -1, -1):
            result.append(chr(ord('a') + state % 26))
            state = parent[pos * STATES + state]

        result.reverse()
        return "".join(result)