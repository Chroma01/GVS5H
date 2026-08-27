from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if k >= n:
            return [0] * n

        children = [{}]
        count = [0]
        depth = [0]
        term_head = [-1]
        next_term = [-1] * n

        for i, w in enumerate(words):
            u = 0
            for ch in w:
                nxt = children[u].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[u][ch] = nxt
                    children.append({})
                    count.append(0)
                    depth.append(depth[u] + 1)
                    term_head.append(-1)
                u = nxt
                count[u] += 1
            next_term[i] = term_head[u]
            term_head[u] = i

        count[0] = n

        on = [0] * n
        idx_to_pos = [0] * n
        start_at = [0] * n
        end_at = [0] * n

        pos = 0
        need_on = k + 1
        stack = [(0, 0, 0)]

        while stack:
            u, state, cur = stack.pop()
            if state == 0:
                du = depth[u]
                if count[u] >= need_on and du > cur:
                    cur = du
                if count[u] >= k and du > start_at[pos]:
                    start_at[pos] = du

                t = term_head[u]
                while t != -1:
                    on[t] = cur
                    idx_to_pos[t] = pos
                    pos += 1
                    t = next_term[t]

                stack.append((u, 1, 0))
                for v in children[u].values():
                    stack.append((v, 0, cur))
            else:
                last_pos = pos - 1
                du = depth[u]
                if count[u] >= k and du > end_at[last_pos]:
                    end_at[last_pos] = du

        children = None
        count = None
        depth = None
        term_head = None
        next_term = None

        off = [0] * n
        best = 0
        for p in range(n):
            if p:
                e = end_at[p - 1]
                if e > best:
                    best = e
            off[p] = best

        best = 0
        for p in range(n - 1, -1, -1):
            if p != n - 1:
                s = start_at[p + 1]
                if s > best:
                    best = s
            if best > off[p]:
                off[p] = best

        ans = [0] * n
        for i in range(n):
            val = on[i]
            o = off[idx_to_pos[i]]
            if o > val:
                val = o
            ans[i] = val
        return ans