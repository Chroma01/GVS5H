from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        if n - 1 < k:
            return [0] * n

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

        valid_at_depth = [0] * (max_depth + 1)

        for node in range(1, len(children)):
            if counts[node] >= k:
                valid_at_depth[depths[node]] += 1

        size = 1
        while size <= max_depth:
            size <<= 1

        segment_tree = [0] * (2 * size)

        for depth in range(1, max_depth + 1):
            if valid_at_depth[depth] > 0:
                segment_tree[size + depth] = depth

        for pos in range(size - 1, 0, -1):
            segment_tree[pos] = max(
                segment_tree[pos << 1],
                segment_tree[pos << 1 | 1],
            )

        def update_depth(depth: int, present: bool) -> None:
            pos = size + depth
            segment_tree[pos] = depth if present else 0
            pos >>= 1

            while pos:
                segment_tree[pos] = max(
                    segment_tree[pos << 1],
                    segment_tree[pos << 1 | 1],
                )
                pos >>= 1

        answer = [0] * n

        for i in range(n):
            changed_depths = []

            for node in paths[i]:
                if counts[node] == k:
                    depth = depths[node]
                    valid_at_depth[depth] -= 1

                    if valid_at_depth[depth] == 0:
                        update_depth(depth, False)

                    changed_depths.append(depth)

            answer[i] = segment_tree[1]

            for depth in changed_depths:
                if valid_at_depth[depth] == 0:
                    update_depth(depth, True)
                valid_at_depth[depth] += 1

        return answer