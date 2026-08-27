from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # ---- build trie iteratively (array based) ----
        children = [{}]
        cnt = [0]
        depth = [0]
        maxlen = 0
        for w in words:
            if len(w) > maxlen:
                maxlen = len(w)
            node = 0
            for ch in w:
                ch_map = children[node]
                nxt = ch_map.get(ch)
                if nxt is None:
                    nxt = len(children)
                    ch_map[ch] = nxt
                    children.append({})
                    cnt.append(0)
                    depth.append(depth[node] + 1)
                node = nxt
                cnt[node] += 1

        # ---- cntd[d] = number of nodes at depth d with cnt >= k ----
        cntd = [0] * (maxlen + 2)
        for v in range(1, len(children)):
            if cnt[v] >= k:
                cntd[depth[v]] += 1

        M1 = 0
        M2 = 0
        for d in range(maxlen, 0, -1):
            c = cntd[d]
            if c >= 1 and M1 == 0:
                M1 = d
            if c >= 2 and M2 == 0:
                M2 = d
            if M1 and M2:
                break

        kp1 = k + 1
        ans = [0] * n
        for i in range(n):
            w = words[i]
            node = 0
            d = 0
            D = 0
            A = 0
            for ch in w:
                node = children[node][ch]
                d += 1
                c = cnt[node]
                if c < k:
                    break
                D = d
                if c >= kp1:
                    A = d
            best = A
            if M2 > best:
                best = M2
            if M1 > D and M1 > best:
                best = M1
            ans[i] = best
        return ans