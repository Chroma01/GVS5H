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

        max_depth = max(depth)
        qualifying_at_depth = [0] * (max_depth + 1)

        for node in range(1, len(children)):
            if count[node] >= k:
                qualifying_at_depth[depth[node]] += 1

        best_global = 0
        for d in range(max_depth, 0, -1):
            if qualifying_at_depth[d] > 0:
                best_global = d
                break

        answer = []

        for path in paths:
            if len(path) < best_global:
                answer.append(best_global)
                continue

            candidate = best_global

            while candidate > 0:
                node = path[candidate - 1]

                # This node is invalidated only when it originally has
                # exactly k words and is the only qualifying node at depth.
                if count[node] == k and qualifying_at_depth[candidate] == 1:
                    candidate -= 1
                else:
                    break

            answer.append(candidate)

        return answer