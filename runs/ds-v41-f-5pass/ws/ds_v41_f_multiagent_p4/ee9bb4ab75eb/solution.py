from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # Removing one element leaves n-1 < k strings.
        if k == n:
            return [0] * n

        # ---- build trie ----
        cnt = [0]          # number of words passing through this node
        depth = [0]        # prefix length (root = 0)
        parent = [-1]
        cchar = [-1]       # edge char code from parent (lowercase 0..25)
        edge = {}          # (node<<5 | c) -> child
        for w in words:
            node = 0
            cnt[0] += 1
            for ch in w:
                c = ord(ch) - 97
                key = (node << 5) | c
                nxt = edge.get(key)
                if nxt is None:
                    nxt = len(cnt)
                    edge[key] = nxt
                    cnt.append(0)
                    depth.append(depth[node] + 1)
                    parent.append(node)
                    cchar.append(c)
                node = nxt
                cnt[node] += 1

        # ---- bucket nodes by depth ----
        maxd = max(depth)
        gek = [0] * (maxd + 1)    # nodes with count >= k
        gek1 = [0] * (maxd + 1)   # nodes with count >= k+1
        eqk = [0] * (maxd + 1)    # nodes with count == k
        eqnode = [-1] * (maxd + 1)
        for v in range(len(cnt)):
            d = depth[v]
            cv = cnt[v]
            if cv >= k:
                gek[d] += 1
                if cv >= k + 1:
                    gek1[d] += 1
                elif cv == k:
                    eqk[d] += 1
                    eqnode[d] = v

        # D_all: deepest depth usable for every removal
        #        (>=2 nodes count>=k, or >=1 node count>=k+1)
        # D2   : deepest depth with exactly one node count==k
        D_all = -1
        D2 = -1
        d2node = -1
        for d in range(maxd + 1):
            if gek[d] >= 2 or gek1[d] >= 1:
                D_all = d
            if eqk[d] == 1:
                D2 = d
                d2node = eqnode[d]

        base = D_all if D_all > 0 else 0

        if D2 > D_all:
            # Reconstruct the prefix of the unique count==k node at depth D2.
            chars = []
            v = d2node
            while v > 0:
                chars.append(chr(cchar[v] + 97))
                v = parent[v]
            prefix = ''.join(reversed(chars))
            L = len(prefix)
            res = []
            for w in words:
                # words having that prefix lose it when removed -> D_all,
                # everyone else keeps it -> D2
                if len(w) >= L and w[:L] == prefix:
                    res.append(base)
                else:
                    res.append(D2)
            return res

        return [base] * n