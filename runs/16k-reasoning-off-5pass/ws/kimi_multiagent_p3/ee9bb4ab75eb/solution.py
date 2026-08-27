from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # ---------- build trie ----------
        # children: list of dicts char -> node id
        children = [dict()]
        cnt = [0]          # number of words passing through node
        depth = [0]        # depth of node (root = 0)

        paths = []         # per word: list of node ids along its path (incl. root)

        for w in words:
            node = 0
            path = [0]
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append(dict())
                    cnt.append(0)
                    depth.append(depth[node] + 1)
                node = nxt
                path.append(node)
            for nd in path:
                cnt[nd] += 1
            paths.append(path)

        max_depth = max(depth)

        # ---------- per-depth qualifying info (cnt >= k) ----------
        # qual_count[d] = number of nodes at depth d with cnt >= k
        # qual_node[d]  = the node id if qual_count[d] == 1 else -1
        qual_count = [0] * (max_depth + 1)
        qual_node = [-1] * (max_depth + 1)
        for nd in range(len(children)):
            d = depth[nd]
            if cnt[nd] >= k:
                qual_count[d] += 1
                qual_node[d] = nd if qual_count[d] == 1 else -1

        # next_qual[d] = largest depth <= d that has at least one qualifying node
        next_qual = [-1] * (max_depth + 1)
        last = -1
        for d in range(max_depth + 1):
            if qual_count[d] > 0:
                last = d
            next_qual[d] = last

        # ---------- answer each removal ----------
        ans = [0] * n
        for i, path in enumerate(paths):
            # candidate A: deepest node ON this word's path with cnt >= k+1
            # (after removing word i its count is still >= k)
            best = 0
            for nd in reversed(path):
                if cnt[nd] >= k + 1:
                    best = depth[nd]
                    break

            # candidate B: deepest qualifying node (cnt >= k) NOT on the path.
            # A path contains at most one node per depth, so scan depths
            # descending; a depth is blocked only if it has exactly one
            # qualifying node and that node lies on this path.
            d = next_qual[max_depth]
            L = len(path) - 1  # max depth present on this path
            while d > best:
                if qual_count[d] >= 2:
                    best = d
                    break
                # qual_count[d] == 1
                if d > L or path[d] != qual_node[d]:
                    best = d
                    break
                d = next_qual[d - 1]
            ans[i] = best

        return ans