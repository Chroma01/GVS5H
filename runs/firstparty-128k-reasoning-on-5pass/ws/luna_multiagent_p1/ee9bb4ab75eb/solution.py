from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        if n - 1 < k:
            return [0] * n

        children = [{}]
        count = [0]
        depth = [0]
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
                    count.append(0)
                    depth.append(depth[node] + 1)

                node = nxt
                count[node] += 1
                path.append(node)

            paths.append(path)
            if len(word) > max_depth:
                max_depth = len(word)

        valid_at_depth = [0] * (max_depth + 1)
        for node in range(1, len(children)):
            if count[node] >= k:
                valid_at_depth[depth[node]] += 1

        size = 1
        while size <= max_depth:
            size <<= 1

        tree = [-1] * (2 * size)

        for d in range(1, max_depth + 1):
            if valid_at_depth[d] > 0:
                tree[size + d] = d

        for pos in range(size - 1, 0, -1):
            tree[pos] = max(tree[pos << 1], tree[(pos << 1) | 1])

        def update(depth_value: int) -> None:
            pos = size + depth_value
            tree[pos] = depth_value if valid_at_depth[depth_value] > 0 else -1
            pos >>= 1

            while pos:
                tree[pos] = max(tree[pos << 1], tree[(pos << 1) | 1])
                pos >>= 1

        answer = [0] * n

        for i, path in enumerate(paths):
            for node in path:
                if count[node] == k:
                    d = depth[node]
                    valid_at_depth[d] -= 1
                    update(d)

            answer[i] = max(0, tree[1])

            for node in path:
                if count[node] == k:
                    d = depth[node]
                    valid_at_depth[d] += 1
                    update(d)

        return answer