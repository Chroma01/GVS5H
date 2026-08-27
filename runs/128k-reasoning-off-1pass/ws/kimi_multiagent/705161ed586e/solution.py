class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        a = [ord(c) - 97 for c in caption]
        INF = float('inf')

        # best[L][i] = (min cost to make caption[i:i+L] uniform, smallest optimal letter)
        best = {}
        for L in (3, 4, 5):
            arr = [None] * (n + 1)
            for i in range(n - L + 1):
                seg = a[i:i + L]
                s = sorted(seg)
                # smallest median: odd L -> middle; even L (4) -> lower of the two medians
                m = s[L // 2] if L % 2 == 1 else s[L // 2 - 1]
                cost = 0
                for x in seg:
                    d = x - m
                    cost += d if d >= 0 else -d
                arr[i] = (cost, m)
            best[L] = arr

        dpCost = [INF] * (n + 1)
        dpStr = [None] * (n + 1)
        choice = [None] * (n + 1)
        dpCost[n] = 0
        dpStr[n] = ""

        for i in range(n - 3, -1, -1):
            bestCost = INF
            bestString = None
            bestChoice = None
            for L in (3, 4, 5):
                j = i + L
                if j > n or dpCost[j] == INF:
                    continue
                c0, ch = best[L][i]
                candCost = c0 + dpCost[j]
                candStr = chr(ch + 97) * L + dpStr[j]
                if (candCost < bestCost or
                        (candCost == bestCost and
                         (bestString is None or candStr < bestString))):
                    bestCost = candCost
                    bestString = candStr
                    bestChoice = (ch, L)
            if bestString is not None:
                dpCost[i] = bestCost
                dpStr[i] = bestString
                choice[i] = bestChoice
            # free strings that will never be referenced again
            if i + 5 <= n:
                dpStr[i + 5] = None

        if dpCost[0] == INF:
            return ""

        # reconstruct from choices
        parts = []
        i = 0
        while i < n:
            ch, L = choice[i]
            parts.append(chr(ch + 97) * L)
            i += L
        return "".join(parts)