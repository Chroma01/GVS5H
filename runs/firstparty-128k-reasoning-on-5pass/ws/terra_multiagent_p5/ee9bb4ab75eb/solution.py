from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        # After removing one word, too few words remain to choose k of them.
        if n - 1 < k:
            return [0] * n

        # Trie arrays:
        # children[node]: mapping character -> child node
        # count[node]: number of words passing through this prefix
        # depth[node]: prefix length represented by this node
        children = [{}]
        count = [0]
        depth = [0]
        word_paths = []

        for word in words:
            node = 0
            path = []

            for ch in word:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    count.append(0)
                    depth.append(depth[node] + 1)

                node = nxt
                count[node] += 1
                path.append(node)

            word_paths.append(path)

        max_depth = max(map(len, words))

        # Number of trie nodes at each depth whose count is at least k.
        qualifying_per_depth = [0] * (max_depth + 1)
        for node in range(1, len(children)):
            if count[node] >= k:
                qualifying_per_depth[depth[node]] += 1

        # Segment tree: maximum currently feasible prefix depth.
        size = 1
        while size <= max_depth:
            size <<= 1

        seg = [0] * (2 * size)
        for d in range(1, max_depth + 1):
            if qualifying_per_depth[d] > 0:
                seg[size + d] = d

        for pos in range(size - 1, 0, -1):
            seg[pos] = max(seg[pos * 2], seg[pos * 2 + 1])

        def update_depth(d: int) -> None:
            pos = size + d
            seg[pos] = d if qualifying_per_depth[d] > 0 else 0
            pos //= 2

            while pos:
                value = max(seg[pos * 2], seg[pos * 2 + 1])
                if seg[pos] == value:
                    break
                seg[pos] = value
                pos //= 2

        answer = [0] * n

        for i, path in enumerate(word_paths):
            changed_depths = []

            # Only prefixes with original count exactly k become invalid
            # after removing one word from their path.
            for node in path:
                if count[node] == k:
                    d = depth[node]
                    qualifying_per_depth[d] -= 1
                    update_depth(d)
                    changed_depths.append(d)

            answer[i] = seg[1]

            # Restore state for the next removal query.
            for d in changed_depths:
                qualifying_per_depth[d] += 1
                update_depth(d)

        return answer