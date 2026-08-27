from typing import List
import heapq


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
            if len(word) > max_depth:
                max_depth = len(word)

        active_at_depth = [0] * (max_depth + 1)

        for node in range(1, len(children)):
            if counts[node] >= k:
                active_at_depth[depths[node]] += 1

        max_heap = [
            -depth
            for depth in range(1, max_depth + 1)
            if active_at_depth[depth] > 0
        ]
        heapq.heapify(max_heap)

        answer = []

        for path in paths:
            for node in path:
                if counts[node] == k:
                    depth = depths[node]
                    active_at_depth[depth] -= 1

            while max_heap and active_at_depth[-max_heap[0]] == 0:
                heapq.heappop(max_heap)

            answer.append(-max_heap[0] if max_heap else 0)

            for node in path:
                if counts[node] == k:
                    depth = depths[node]
                    if active_at_depth[depth] == 0:
                        heapq.heappush(max_heap, -depth)
                    active_at_depth[depth] += 1

        return answer