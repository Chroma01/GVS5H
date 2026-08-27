from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        children = [{}]
        cnt = [0]
        depth = [0]

        for w in words:
            node = 0
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    cnt.append(0)
                    depth.append(depth[node] + 1)
                node = nxt
                cnt[node] += 1

        max_d = max(depth)
        top1 = [0] * (max_d + 2)
        top2 = [0] * (max_d + 2)

        for node in range(1, len(children)):
            d = depth[node]
            c = cnt[node]
            if c > top1[d]:
                top2[d] = top1[d]
                top1[d] = c
            elif c > top2[d]:
                top2[d] = c

        suff = [0] * (max_d + 3)
        for d in range(max_d, 0, -1):
            suff[d] = suff[d + 1]
            if top1[d] >= k and suff[d] == 0:
                suff[d] = d

        ans = []
        for w in words:
            L = len(w)
            best = suff[L + 1]
            node = 0
            for d, ch in enumerate(w, 1):
                node = children[node][ch]
                c = cnt[node]
                if c >= k + 1 or (top1[d] >= k and (c < top1[d] or top2[d] >= k)):
                    if d > best:
                        best = d
            ans.append(best)

        return ans