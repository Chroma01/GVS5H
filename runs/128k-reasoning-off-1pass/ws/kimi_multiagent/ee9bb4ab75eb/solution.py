from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # If removing any element leaves fewer than k strings, all answers are 0.
        if n - 1 < k:
            return [0] * n

        # ---------- Build trie ----------
        # children: list of dicts char -> node id
        children = [dict()]
        cnt = [0]          # number of words passing through node
        depth = [0]        # depth of node (root = 0)
        paths = []         # per word: list of node ids along its path (excluding root)

        for w in words:
            node = 0
            path = []
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append(dict())
                    cnt.append(0)
                    depth.append(depth[node] + 1)
                node = nxt
                cnt[node] += 1
                path.append(node)
            paths.append(path)

        num_nodes = len(children)
        max_depth = max(depth) if num_nodes > 1 else 0

        # ---------- Per-depth top-2 qualifying nodes (count >= k) ----------
        # A root-to-leaf path contains at most one node per depth, so keeping
        # two distinct qualifying nodes per depth suffices to find one off-path.
        top1 = [-1] * (max_depth + 1)
        top2 = [-1] * (max_depth + 1)
        qualifying_depths = []
        for v in range(1, num_nodes):
            if cnt[v] >= k:
                d = depth[v]
                if top1[d] == -1:
                    top1[d] = v
                    qualifying_depths.append(d)
                elif top2[d] == -1:
                    top2[d] = v
        qualifying_depths.sort(reverse=True)

        # ---------- Per-word answers ----------
        seen = [0] * num_nodes  # timestamped visited marks for path membership
        ans = [0] * n

        for i, path in enumerate(paths):
            stamp = i + 1
            best_on = 0  # P_i: max depth on path with count-1 >= k
            for v in path:
                seen[v] = stamp
                if cnt[v] - 1 >= k and depth[v] > best_on:
                    best_on = depth[v]

            # Q_i: max qualifying depth with a qualifying node not on this path
            best_off = 0
            for d in qualifying_depths:
                a, b = top1[d], top2[d]
                if seen[a] != stamp or (b != -1 and seen[b] != stamp):
                    best_off = d
                    break

            ans[i] = best_on if best_on > best_off else best_off

        return ans