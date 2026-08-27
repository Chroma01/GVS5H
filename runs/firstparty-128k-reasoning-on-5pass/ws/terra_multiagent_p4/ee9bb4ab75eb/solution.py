from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        if n - 1 < k:
            return [0] * n

        children = [{}]
        count = [0]
        depth = [0]
        max_len = 0

        for word in words:
            max_len = max(max_len, len(word))
            node = 0

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

        valid_at_depth = [0] * (max_len + 1)

        for node in range(1, len(children)):
            if count[node] >= k:
                valid_at_depth[depth[node]] += 1

        size = 1
        while size <= max_len:
            size <<= 1

        seg = [0] * (2 * size)

        for d in range(1, max_len + 1):
            if valid_at_depth[d] > 0:
                seg[size + d] = d

        for pos in range(size - 1, 0, -1):
            seg[pos] = max(seg[pos << 1], seg[pos << 1 | 1])

        def update(depth_value: int, value: int) -> None:
            pos = size + depth_value
            seg[pos] = value
            pos >>= 1

            while pos:
                new_value = max(seg[pos << 1], seg[pos << 1 | 1])

                if seg[pos] == new_value:
                    break

                seg[pos] = new_value
                pos >>= 1

        answer = [0] * n

        for i, word in enumerate(words):
            node = 0
            removed_depths = []

            for ch in word:
                node = children[node][ch]
                d = depth[node]

                if count[node] == k and valid_at_depth[d] == 1:
                    update(d, 0)
                    removed_depths.append(d)

            answer[i] = seg[1]

            for d in removed_depths:
                update(d, d)

        return answer