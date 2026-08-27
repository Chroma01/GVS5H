from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        # If after removing any element we have fewer than k strings, answer is 0.
        if n - 1 < k:
            return [0] * n

        # ----------  Special case k == 1  ----------
        # For k == 1 the answer is simply the longest word that stays after removal.
        if k == 1:
            max_len = max(len(w) for w in words)
            cnt_max = sum(1 for w in words if len(w) == max_len)

            # If at least two words have the maximal length, it survives any removal.
            if cnt_max >= 2:
                return [max_len] * n

            # Only one word has maximal length.
            second_len = 0
            for w in words:
                l = len(w)
                if l != max_len:
                    second_len = max(second_len, l)

            ans = [0] * n
            for i, w in enumerate(words):
                if len(w) == max_len:          # the unique maximal word is removed
                    ans[i] = second_len
                else:
                    ans[i] = max_len
            return ans

        # ----------  k >= 2  ----------
        # 1. Build a trie of all words.
        # Each node stores:
        #   children[26] : list of child indices, -1 means absent
        #   cnt           : how many words go through this node
        #   depth         : length of the prefix (1‑based)
        children: List[List[int]] = [[-1] * 26]   # node 0 = root, depth 0
        cnt: List[int] = [0]
        depth: List[int] = [0]

        max_depth = 0
        for w in words:
            node = 0
            for pos, ch in enumerate(w):
                idx = ord(ch) - 97
                nxt = children[node][idx]
                if nxt == -1:
                    nxt = len(children)
                    children.append([-1] * 26)
                    cnt.append(0)
                    depth.append(pos + 1)
                    children[node][idx] = nxt
                node = nxt
                cnt[node] += 1
                max_depth = max(max_depth, pos + 1)

        # 2. For each depth L compute:
        #    M[L] = maximum cnt among prefixes of length L
        #    C[L] = how many prefixes of length L have cnt == k
        M = [0] * (max_depth + 1)
        C = [0] * (max_depth + 1)
        for node in range(1, len(children)):
            d = depth[node]
            c = cnt[node]
            if c > M[d]:
                M[d] = c
            if c == k:
                C[d] += 1

        # 3. Find the largest length L0 that works for every index.
        #    L0 is universal iff M[L] >= k+1  or  (M[L] == k and C[L] >= 2).
        L0 = 0
        for L in range(max_depth, 0, -1):
            if M[L] >= k + 1 or (M[L] == k and C[L] >= 2):
                L0 = L
                break

        # 4. Special lengths: those L > L0 with M[L] == k and C[L] == 1.
        special: List[int] = []
        for L in range(max_depth, L0, -1):
            if M[L] == k and C[L] == 1:
                special.append(L)           # already in decreasing order

        # 5. For every word, collect the special lengths it blocks.
        #    A word blocks a special length L if its own prefix of length L
        #    is the unique prefix that occurs k times.
        Bad: List[set] = [set() for _ in range(n)]
        for idx, w in enumerate(words):
            node = 0
            for pos, ch in enumerate(w):
                node = children[node][ord(ch) - 97]
                L = pos + 1
                if cnt[node] == k and M[L] == k and C[L] == 1:
                    Bad[idx].add(L)

        # 6. Compute the answer for each index.
        ans = [L0] * n
        for i in range(n):
            for L in special:          # decreasing order, first not blocked is the best
                if L not in Bad[i]:
                    ans[i] = L
                    break

        return ans