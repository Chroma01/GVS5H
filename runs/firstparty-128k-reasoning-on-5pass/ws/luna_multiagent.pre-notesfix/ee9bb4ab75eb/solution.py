from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        if n - 1 < k:
            return [0] * n

        # Trie representation.
        children = [{}]
        count = [0]
        depth = [0]
        max_depth = 0

        for word in words:
            node = 0
            count[node] += 1

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

            if len(word) > max_depth:
                max_depth = len(word)

        # valid[d] is the number of trie nodes at depth d whose count >= k.
        valid = [0] * (max_depth + 1)
        for node in range(1, len(children)):
            if count[node] >= k:
                valid[depth[node]] += 1

        # Iterative segment tree storing whether each depth is currently valid.
        size = 1
        while size < max_depth + 1:
            size <<= 1

        tree = [0] * (2 * size)
        for d in range(1, max_depth + 1):
            if valid[d] > 0:
                tree[size + d] = 1

        for pos in range(size - 1, 0, -1):
            tree[pos] = max(tree[pos << 1], tree[pos << 1 | 1])

        def update(position: int, value: int) -> None:
            p = size + position
            tree[p] = value
            p >>= 1
            while p:
                tree[p] = max(tree[p << 1], tree[p << 1 | 1])
                p >>= 1

        def deepest_valid_depth() -> int:
            if tree[1] == 0:
                return 0

            node = 1
            while node < size:
                right = node << 1 | 1
                if tree[right]:
                    node = right
                else:
                    node <<= 1

            answer = node - size
            return answer if answer <= max_depth else 0

        answer = [0] * n

        for i, word in enumerate(words):
            node = 0
            removed_depths = []

            # Only nodes with count exactly k become invalid after removal.
            for ch in word:
                node = children[node][ch]
                if count[node] == k:
                    d = depth[node]
                    valid[d] -= 1
                    if valid[d] == 0:
                        update(d, 0)
                    removed_depths.append(d)

            answer[i] = deepest_valid_depth()

            # Restore the temporarily removed word.
            for d in removed_depths:
                if valid[d] == 0:
                    update(d, 1)
                valid[d] += 1

        return answer