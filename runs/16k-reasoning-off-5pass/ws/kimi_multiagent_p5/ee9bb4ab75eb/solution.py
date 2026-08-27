from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie. children stored as dict per node; cnt = words passing through node.
        children = []   # list of dict
        cnt = []        # list of int
        children.append({})
        cnt.append(0)

        word_nodes = []  # per word: list of node ids along path, index = depth (0..len)
        max_len = 0
        for w in words:
            path = [0]
            node = 0
            cnt[node] += 1
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    cnt.append(0)
                node = nxt
                cnt[node] += 1
                path.append(node)
            word_nodes.append(path)
            if len(w) > max_len:
                max_len = len(w)

        # good[d] = number of nodes at depth d with cnt >= k
        good = [0] * (max_len + 1)
        depth = [0] * len(children)
        stack = [0]
        order = [0]
        while stack:
            u = stack.pop()
            for v in children[u].values():
                depth[v] = depth[u] + 1
                order.append(v)
                stack.append(v)
        for u in order:
            if cnt[u] >= k:
                good[depth[u]] += 1

        # suf_best[L] = deepest d > L with good[d] > 0, else -1
        # Depths beyond len(word) are unaffected by removing that word.
        suf_best = [-1] * (max_len + 2)
        best = -1
        for L in range(max_len, -1, -1):
            if L + 1 <= max_len and good[L + 1] > 0:
                if L + 1 > best:
                    best = L + 1
            suf_best[L] = best

        ans = [0] * n
        for i, w in enumerate(words):
            L = len(w)
            path = word_nodes[i]
            res = suf_best[L]  # unaffected deep depths
            if res < 0:
                res = 0
            # Walk path depths deep -> shallow; adjusted good count at depth d is
            # good[d] - (1 if the path node had cnt == k, since it drops below k).
            for d in range(L, -1, -1):
                g = good[d]
                if cnt[path[d]] == k:
                    g -= 1
                if g > 0:
                    if d > res:
                        res = d
                    break
            ans[i] = res
        return ans