from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        # If removing one word leaves fewer than k words, every answer is 0.
        if n - 1 < k:
            return [0] * n

        # Trie storage.
        # children[node] is either None (leaf so far) or a dict char -> child node.
        children = [None]
        count = [0]       # number of words passing through this node
        depth = [0]       # depth of this node in the trie
        paths = []        # paths[i] = node ids on word i's path, one per character
        max_len = 0

        for w in words:
            node = 0
            path = []

            for ch in w:
                d = children[node]

                if d is None:
                    nxt = len(children)
                    children[node] = {ch: nxt}
                    children.append(None)
                    count.append(0)
                    depth.append(depth[node] + 1)
                else:
                    nxt = d.get(ch)
                    if nxt is None:
                        nxt = len(children)
                        d[ch] = nxt
                        children.append(None)
                        count.append(0)
                        depth.append(depth[node] + 1)

                node = nxt
                count[node] += 1
                path.append(node)

            paths.append(path)
            if len(w) > max_len:
                max_len = len(w)

        # For each depth d:
        # has_gt[d]      : exists a prefix node at depth d with count > k
        # exact_count[d] : number of prefix nodes at depth d with count == k, capped at 2
        # exact_node[d]  : the unique node id if exact_count[d] == 1, else -1
        has_gt = [False] * (max_len + 1)
        exact_count = [0] * (max_len + 1)
        exact_node = [-1] * (max_len + 1)

        for node in range(1, len(count)):
            c = count[node]
            d = depth[node]

            if c > k:
                has_gt[d] = True
            elif c == k:
                if exact_count[d] < 2:
                    exact_count[d] += 1
                    if exact_count[d] == 1:
                        exact_node[d] = node
                    else:
                        exact_node[d] = -1

        # Trie arrays are no longer needed.
        children = None
        count = None
        depth = None

        ans = [0] * n

        hg = has_gt
        ec_arr = exact_count
        en = exact_node

        for i, w in enumerate(words):
            lo, hi = 0, max_len
            lw = len(w)
            path = paths[i]

            # Binary search the largest feasible prefix length.
            while lo < hi:
                mid = (lo + hi + 1) // 2

                if hg[mid]:
                    ok = True
                else:
                    ec = ec_arr[mid]

                    if ec >= 2:
                        # The removed word can match at most one prefix of this length,
                        # so at least one exact-k prefix remains unaffected.
                        ok = True
                    elif ec == 1:
                        # The only exact-k prefix remains usable iff the removed word
                        # does not have that prefix.
                        if lw < mid:
                            ok = True
                        else:
                            ok = (path[mid - 1] != en[mid])
                    else:
                        ok = False

                if ok:
                    lo = mid
                else:
                    hi = mid - 1

            ans[i] = lo

        return ans