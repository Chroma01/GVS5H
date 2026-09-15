from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # After removing one element only n-1 remain; if n == k they are fewer than k.
        if n == k:
            return [0] * n

        # ---- build trie ----
        children = [{}]
        cnt = [0]           # number of word-indices having this node's prefix
        is_term = [False]
        term_idx = [[]]     # original indices of words ending exactly here
        depth = [0]

        for idx, w in enumerate(words):
            node = 0
            cnt[0] += 1
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    cnt.append(0)
                    is_term.append(False)
                    term_idx.append([])
                    depth.append(depth[node] + 1)
                node = nxt
                cnt[node] += 1
            is_term[node] = True
            term_idx[node].append(idx)

        N = len(children)

        # ---- preorder tin for terminal nodes (distinct words) ----
        tin = [-1] * N
        counter = 0
        stack = [0]
        while stack:
            node = stack.pop()
            if is_term[node]:
                tin[node] = counter
                counter += 1
            for child in children[node].values():
                stack.append(child)
        d = counter  # number of distinct words / terminal positions

        # ---- L,R: min/max tin of terminals in each subtree (children have larger index) ----
        L = [d] * N
        R = [-1] * N
        for node in range(N - 1, -1, -1):
            if is_term[node]:
                t = tin[node]
                if t < L[node]:
                    L[node] = t
                if t > R[node]:
                    R[node] = t
            for child in children[node].values():
                if L[child] < L[node]:
                    L[node] = L[child]
                if R[child] > R[node]:
                    R[node] = R[child]

        # nodes with count > k are valid for every deletion
        base = 0
        for node in range(N):
            if cnt[node] > k and depth[node] > base:
                base = depth[node]

        NEG = -1
        # node with count == k is valid only for terminals OUTSIDE its subtree
        # B[l]: node whose subtree starts at l, contributes to positions < l
        # C[r]: node whose subtree ends at r, contributes to positions > r
        B = [NEG] * (d + 1)
        C = [NEG] * d
        for node in range(N):
            if cnt[node] == k:
                l = L[node]
                r = R[node]
                if l > 0 and depth[node] > B[l]:
                    B[l] = depth[node]
                if r < d - 1 and depth[node] > C[r]:
                    C[r] = depth[node]

        # suffix max of B
        suf = [NEG] * (d + 1)
        for i in range(d - 1, -1, -1):
            v = B[i]
            suf[i] = v if v > suf[i + 1] else suf[i + 1]
        # prefix max of C
        pre = [NEG] * d
        cur = NEG
        for i in range(d):
            if C[i] > cur:
                cur = C[i]
            pre[i] = cur

        ans = [0] * n
        for node in range(N):
            if is_term[node]:
                t = tin[node]
                best = base
                a = suf[t + 1]          # count==k nodes with L > t
                if a > best:
                    best = a
                if t >= 1:
                    b = pre[t - 1]      # count==k nodes with R < t
                    if b > best:
                        best = b
                for idx in term_idx[node]:
                    ans[idx] = best
        return ans