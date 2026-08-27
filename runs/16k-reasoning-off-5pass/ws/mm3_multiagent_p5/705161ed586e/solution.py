class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        INF = 10 ** 9

        # State: (k, c) where k in {1,2,3} (3 means run length >= 3)
        # dp[(k, c)] = (cost, string) – best for processed prefix so far
        dp = {}

        first_char_val = ord(caption[0]) - ord('a')
        for c in range(26):
            cost = 0 if c == first_char_val else 1
            dp[(1, c)] = (cost, chr(ord('a') + c))

        for idx in range(1, n):
            ndp = {}
            orig_val = ord(caption[idx]) - ord('a')
            for (k_prev, c_prev), (cost_prev, str_prev) in dp.items():
                # 1) Extend the current run with the same character c_prev
                if k_prev < 3:
                    new_k = k_prev + 1
                else:
                    new_k = 3  # stay at >=3
                add_cost = 0 if c_prev == orig_val else 1
                new_cost = cost_prev + add_cost
                new_str = str_prev + chr(ord('a') + c_prev)
                key = (new_k, c_prev)
                if key not in ndp:
                    ndp[key] = (new_cost, new_str)
                else:
                    old_cost, old_str = ndp[key]
                    if new_cost < old_cost or (new_cost == old_cost and new_str < old_str):
                        ndp[key] = (new_cost, new_str)

                # 2) Close current run (only if k_prev == 3) and start a new run with a possibly different character
                if k_prev == 3:
                    for c_new in range(26):
                        add_cost2 = 0 if c_new == orig_val else 1
                        new_cost2 = cost_prev + add_cost2
                        new_str2 = str_prev + chr(ord('a') + c_new)
                        key2 = (1, c_new)
                        if key2 not in ndp:
                            ndp[key2] = (new_cost2, new_str2)
                        else:
                            old_cost2, old_str2 = ndp[key2]
                            if new_cost2 < old_cost2 or (new_cost2 == old_cost2 and new_str2 < old_str2):
                                ndp[key2] = (new_cost2, new_str2)

            dp = ndp

        # After processing all characters, the final run must be long enough (k == 3)
        best_cost = INF
        best_str = ""
        for (k, c), (cost, s) in dp.items():
            if k == 3:
                if cost < best_cost or (cost == best_cost and s < best_str):
                    best_cost = cost
                    best_str = s

        return best_str if best_cost < INF else ""