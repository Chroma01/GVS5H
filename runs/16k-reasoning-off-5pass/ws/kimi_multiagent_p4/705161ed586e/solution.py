class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        a = [ord(ch) - 97 for ch in caption]

        # pref[k][i] = number of occurrences of letter k in caption[:i]
        pref = [[0] * (n + 1) for _ in range(26)]
        for i, v in enumerate(a):
            for k in range(26):
                pref[k][i + 1] = pref[k][i]
            pref[v][i + 1] += 1

        INF = float('inf')

        # suff[i] = min cost to make caption[i:] good (partition into blocks of len>=3)
        suff = [INF] * (n + 1)
        suff[n] = 0
        for i in range(n - 3, -1, -1):
            best = INF
            for L in (3, 4, 5):
                j = i + L
                if j > n:
                    break
                if suff[j] == INF:
                    continue
                # letter counts in caption[i:j]
                cnt = [pref[k][j] - pref[k][i] for k in range(26)]
                # cost(c) = sum_l cnt[l] * |l - c|; cost(0) = sum cnt[l]*l
                cost = 0
                for l in range(26):
                    cost += cnt[l] * l
                min_block = cost
                total = L
                left = cnt[0]          # letters with index <= c (c=0)
                right = total - cnt[0] # letters with index > c
                cur = cost
                for c in range(1, 26):
                    # cost(c) = cost(c-1) + (#letters <= c-1) - (#letters > c-1)
                    cur = cur + left - right
                    if cur < min_block:
                        min_block = cur
                    left += cnt[c]
                    right -= cnt[c]
                cand = min_block + suff[j]
                if cand < best:
                    best = cand
            suff[i] = best

        if suff[0] == INF:
            return ""

        # Greedy lexicographic reconstruction:
        # at each position try the smallest target char first; for that char,
        # any length achieving optimal total cost is valid (prefix is c*L either
        # way, suffix is optimal), pick the first that matches suff[i].
        res = []
        i = 0
        while i < n:
            target_cost = suff[i]
            found = False
            for c in range(26):
                for L in (3, 4, 5):
                    j = i + L
                    if j > n:
                        break
                    if suff[j] == INF:
                        continue
                    # cost of block caption[i:j] to char c
                    cost = 0
                    for k in range(26):
                        cntk = pref[k][j] - pref[k][i]
                        if cntk:
                            d = k - c
                            cost += cntk * (d if d >= 0 else -d)
                    if cost + suff[j] == target_cost:
                        res.append(chr(97 + c) * L)
                        i = j
                        found = True
                        break
                if found:
                    break
            if not found:
                return ""  # unreachable when suff[0] is finite
        return "".join(res)