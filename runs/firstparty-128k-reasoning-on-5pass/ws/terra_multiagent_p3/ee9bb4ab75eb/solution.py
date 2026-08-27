from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        if n - 1 < k:
            return [0] * n

        children = [{}]
        count = [0]
        depth = [0]
        max_depth = 0

        for word in words:
            node = 0
            for ch in word:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    count.append(0)
                    depth.append(depth[node] + 1)
                    max_depth = max(max_depth, depth[-1])

                node = nxt
                count[node] += 1

        valid_nodes = [0] * (max_depth + 1)
        best_depth = 0

        for node in range(1, len(children)):
            d = depth[node]
            if count[node] >= k:
                valid_nodes[d] += 1
                if d > best_depth:
                    best_depth = d

        answer = [0] * n
        stamp = [0] * (best_depth + 1)

        for query_id, word in enumerate(words, start=1):
            node = 0

            for ch in word:
                node = children[node][ch]
                d = depth[node]
                if d <= best_depth and count[node] == k and valid_nodes[d] == 1:
                    stamp[d] = query_id

            result = best_depth
            while result > 0 and stamp[result] == query_id:
                result -= 1

            answer[query_id - 1] = result

        return answer