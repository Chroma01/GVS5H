from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # If removing one element leaves fewer than k strings, answer is always 0.
        if n - 1 < k:
            return [0] * n

        # Build a trie. children stored as dicts; cnt = number of words passing
        # through the node (root is node 0 at depth 0).
        children = []          # children[v]: dict char -> node index
        cnt = []               # cnt[v]: number of words passing through node v
        depth_of = []          # depth_of[v]: depth of node v
        children.append({})
        cnt.append(0)
        depth_of.append(0)

        word_nodes = []        # word_nodes[i]: list of node indices along word i's path (excluding root)

        for w in words:
            v = 0
            cnt[v] += 1
            path = []
            for ch in w:
                nxt = children[v].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[v][ch] = nxt
                    children.append({})
                    cnt.append(0)
                    depth_of.append(depth_of[v] + 1)
                v = nxt
                cnt[v] += 1
                path.append(v)
            word_nodes.append(path)

        max_len = max((len(w) for w in words), default=0)

        # For each depth, find the top two counts among nodes at that depth,
        # and the node index achieving the best count.
        best1 = [0] * (max_len + 1)   # highest count at depth d
        best1_node = [-1] * (max_len + 1)
        best2 = [0] * (max_len + 1)   # second highest count at depth d

        for v in range(1, len(children)):
            d = depth_of[v]
            c = cnt[v]
            if c > best1[d]:
                best2[d] = best1[d]
                best1[d] = c
                best1_node[d] = v
            elif c > best2[d]:
                best2[d] = c

        answer = [0] * n
        for i, path in enumerate(word_nodes):
            # For each depth along word i's path, the node at that depth is on
            # the path, so its count effectively decreases by 1 after removal.
            # Nodes not on the path keep their counts.
            best_depth = 0
            for v in path:
                d = depth_of[v]
                if best1_node[d] == v:
                    # The best node at this depth is on word i's path.
                    effective = max(best1[d] - 1, best2[d])
                else:
                    effective = best1[d]
                if effective >= k:
                    best_depth = d
                # Depths increase along the path, so the last valid d is the max.
            answer[i] = best_depth

        return answer