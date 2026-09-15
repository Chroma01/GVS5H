from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # After removing one word, only n-1 words remain.
        if n - 1 < k:
            return [0] * n

        # Build trie. Node 0 is root.
        children = [{}]
        cnt = [0]          # number of words passing through node
        depth = [0]        # depth of node (== prefix length)
        word_paths = []    # node ids along each word's path (depth 1..len)
        maxlen = 0

        for w in words:
            node = 0
            path = []
            d = 0
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
                path.append(node)
                d += 1
            word_paths.append(path)
            if d > maxlen:
                maxlen = d

        # cnt_ge[L] = number of nodes at depth L with original count >= k
        cnt_ge = [0] * (maxlen + 1)
        for v in range(1, len(children)):
            if cnt[v] >= k:
                cnt_ge[depth[v]] += 1

        res = []
        for i in range(n):
            path = word_paths[i]
            plen = len(path)
            lo, hi = 0, maxlen
            while lo < hi:
                mid = (lo + hi + 1) >> 1
                ok = False
                if mid <= plen:
                    c = cnt[path[mid - 1]]
                    if c >= k + 1:
                        # on-path node still has >= k after removal
                        ok = True
                    else:
                        # off-path nodes at depth mid with count >= k
                        off = cnt_ge[mid] - (1 if c >= k else 0)
                        if off >= 1:
                            ok = True
                else:
                    # prefix longer than this word: only off-path matters
                    if cnt_ge[mid] >= 1:
                        ok = True
                if ok:
                    lo = mid
                else:
                    hi = mid - 1
            res.append(lo)

        return res