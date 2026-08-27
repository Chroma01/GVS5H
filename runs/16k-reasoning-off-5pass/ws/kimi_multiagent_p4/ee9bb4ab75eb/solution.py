from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # Removing one word must leave at least k strings.
        if n - 1 < k:
            return [0] * n

        # ---- Build a trie over all words ----------------------------------
        # children[u]: dict char -> node id; cnt[u]: #words passing through u.
        children = [{}]
        cnt = [0]

        def new_node() -> int:
            children.append({})
            cnt.append(0)
            return len(cnt) - 1

        # paths[i][d] = node id of word i at depth d (paths[i][0] = root).
        paths = []
        for w in words:
            node = 0
            cnt[node] += 1
            path = [0]
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = new_node()
                    children[node][ch] = nxt
                node = nxt
                cnt[node] += 1
                path.append(node)
            paths.append(path)

        # ---- Depth of every node (iterative DFS from root) ----------------
        depth = [0] * len(cnt)
        order = [0]
        stack = [0]
        while stack:
            u = stack.pop()
            for v in children[u].values():
                depth[v] = depth[u] + 1
                stack.append(v)
                order.append(v)

        # ---- Per-depth qualifying node stats ------------------------------
        # A node at depth d with cnt >= k means k strings share a length-d
        # prefix, so the answer for the full array is the deepest such depth.
        qual_count = {}  # depth -> number of nodes at this depth with cnt >= k
        qual_rep = {}    # depth -> one such node id
        for u in order:
            if cnt[u] >= k:
                d = depth[u]
                qual_count[d] = qual_count.get(d, 0) + 1
                qual_rep[d] = u

        # first  = deepest depth with >= 1 qualifying node
        # second = second-deepest depth with >= 1 qualifying node
        # multi  = deepest depth with >= 2 qualifying nodes
        # (0 means "none"; the root at depth 0 never contributes.)
        first = second = multi = 0
        for d in sorted(qual_count.keys(), reverse=True):
            if first == 0:
                first = d
            elif second == 0:
                second = d
            if qual_count[d] >= 2 and multi == 0:
                multi = d
            if second != 0 and multi != 0:
                break

        # ---- Answer each removal ------------------------------------------
        # Removing word i only decrements counts along its own path:
        #  * on-path nodes stay qualifying iff cnt >= k + 1,
        #  * off-path nodes keep cnt >= k unchanged.
        ans = [0] * n
        for i, path in enumerate(paths):
            L = len(path) - 1  # deepest depth on this word's path

            # On-path candidate: deepest node on the path with cnt >= k + 1.
            # Summed over all words this costs O(sum of word lengths).
            on_best = 0
            for d in range(L, 0, -1):
                if cnt[path[d]] >= k + 1:
                    on_best = d
                    break

            # Off-path candidate in O(1): deepest qualifying depth whose
            # qualifying node is not this word's node at that depth.
            off_best = 0
            if first:
                node_at_first = path[first] if first <= L else -1
                if qual_count[first] >= 2 or qual_rep[first] != node_at_first:
                    # Either another node qualifies at this depth, or the
                    # unique qualifier is not on word i's path.
                    off_best = first
                else:
                    # Word i's node is the unique qualifier at the deepest
                    # depth; fall back to the best of the second-deepest
                    # qualifying depth and the deepest depth with >= 2
                    # qualifiers (one of them survives the removal).
                    off_best = second if second > multi else multi

            ans[i] = on_best if on_best > off_best else off_best
        return ans