from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        children = [{}]
        counts = [0]
        depths = [0]
        paths = []
        max_depth = 0

        for word in words:
            node = 0
            path = []

            for ch in word:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    counts.append(0)
                    depths.append(depths[node] + 1)

                node = nxt
                counts[node] += 1
                path.append(node)

            paths.append(path)
            max_depth = max(max_depth, len(word))

        valid = [0] * (max_depth + 1)

        for node in range(1, len(counts)):
            if counts[node] >= k:
                valid[depths[node]] += 1

        size = 1
        while size < max_depth + 1:
            size <<= 1

        segment_tree = [-1] * (2 * size)

        for depth in range(1, max_depth + 1):
            if valid[depth] > 0:
                segment_tree[size + depth] = depth

        for pos in range(size - 1, 0, -1):
            segment_tree[pos] = max(
                segment_tree[pos << 1],
                segment_tree[(pos << 1) | 1],
            )

        def update(depth: int) -> None:
            pos = size + depth
            segment_tree[pos] = depth if valid[depth] > 0 else -1
            pos >>= 1

            while pos:
                segment_tree[pos] = max(
                    segment_tree[pos << 1],
                    segment_tree[(pos << 1) | 1],
                )
                pos >>= 1

        answer = [0] * n

        if n - 1 < k:
            return answer

        for i, path in enumerate(paths):
            changed_depths = []

            for node in path:
                if counts[node] == k:
                    depth = depths[node]
                    valid[depth] -= 1
                    update(depth)
                    changed_depths.append(depth)

            answer[i] = max(0, segment_tree[1])

            for depth in changed_depths:
                valid[depth] += 1
                update(depth)

        return answer