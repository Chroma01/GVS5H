from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        children = [{}]
        count = [0]
        max_len = 0

        for word in words:
            node = 0
            max_len = max(max_len, len(word))

            for ch in word:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    count.append(0)

                node = nxt
                count[node] += 1

        depth = [0] * len(children)
        valid_at_depth = [0] * (max_len + 1)

        stack = [0]
        while stack:
            node = stack.pop()

            for child in children[node].values():
                depth[child] = depth[node] + 1
                if count[child] >= k:
                    valid_at_depth[depth[child]] += 1
                stack.append(child)

        size = 1
        while size <= max_len:
            size <<= 1

        seg = [0] * (size * 2)
        for d in range(1, max_len + 1):
            if valid_at_depth[d] > 0:
                seg[size + d] = d

        for pos in range(size - 1, 0, -1):
            seg[pos] = max(seg[pos * 2], seg[pos * 2 + 1])

        def update(d: int, active: bool) -> None:
            pos = size + d
            seg[pos] = d if active else 0
            pos //= 2

            while pos:
                value = max(seg[pos * 2], seg[pos * 2 + 1])
                if seg[pos] == value:
                    break
                seg[pos] = value
                pos //= 2

        answer = [0] * n

        for i, word in enumerate(words):
            node = 0
            changed = []

            for d, ch in enumerate(word, 1):
                node = children[node][ch]

                if count[node] == k:
                    valid_at_depth[d] -= 1
                    changed.append(d)

                    if valid_at_depth[d] == 0:
                        update(d, False)

            answer[i] = seg[1]

            for d in changed:
                valid_at_depth[d] += 1

                if valid_at_depth[d] == 1:
                    update(d, True)

        return answer