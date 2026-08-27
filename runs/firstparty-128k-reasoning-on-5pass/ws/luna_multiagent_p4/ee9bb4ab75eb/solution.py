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

        active_by_depth = [0] * (max_depth + 1)
        for node in range(1, len(children)):
            if count[node] >= k:
                active_by_depth[depth[node]] += 1

        size = 1
        while size <= max_depth:
            size <<= 1

        tree = [0] * (2 * size)
        for d, value in enumerate(active_by_depth):
            tree[size + d] = value

        for pos in range(size - 1, 0, -1):
            tree[pos] = max(tree[pos * 2], tree[pos * 2 + 1])

        def update(position: int, delta: int) -> None:
            pos = size + position
            tree[pos] += delta
            pos >>= 1
            while pos:
                tree[pos] = max(tree[pos * 2], tree[pos * 2 + 1])
                pos >>= 1

        def maximum_active_depth() -> int:
            if tree[1] == 0:
                return 0

            pos = 1
            while pos < size:
                right = pos * 2 + 1
                if tree[right] > 0:
                    pos = right
                else:
                    pos *= 2

            return pos - size

        answer = [0] * n

        for i, path in enumerate(paths):
            changed = []

            for node in path:
                if count[node] == k:
                    d = depth[node]
                    update(d, -1)
                    changed.append(d)

            answer[i] = maximum_active_depth()

            for d in changed:
                update(d, 1)

        return answer