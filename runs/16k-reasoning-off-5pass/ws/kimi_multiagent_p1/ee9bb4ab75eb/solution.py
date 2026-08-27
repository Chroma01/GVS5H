from typing import List
import heapq


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie. children: list of dict char -> node id
        children = [dict()]
        cnt = [0]          # number of words passing through node
        depth = [0]        # depth of node (= prefix length)
        paths = []         # per word: list of node ids along its path (excluding root)

        for w in words:
            node = 0
            path = []
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append(dict())
                    cnt.append(0)
                    depth.append(depth[node] + 1)
                node = nxt
                path.append(node)
            for v in path:
                cnt[v] += 1
            paths.append(path)

        max_depth = max(depth) if depth else 0
        # valid[d] = number of nodes at depth d with cnt >= k
        valid = [0] * (max_depth + 1)
        for v in range(1, len(cnt)):
            if cnt[v] >= k:
                valid[depth[v]] += 1

        # lazy max-heap of depths (store negatives)
        heap = [-d for d in range(1, max_depth + 1) if valid[d] > 0]
        heapq.heapify(heap)

        def current_answer() -> int:
            while heap and valid[-heap[0]] <= 0:
                heapq.heappop(heap)
            return -heap[0] if heap else 0

        def dec(v: int) -> None:
            c = cnt[v]
            if c == k:
                d = depth[v]
                valid[d] -= 1
            cnt[v] = c - 1

        def inc(v: int) -> None:
            c = cnt[v]
            if c == k - 1:
                d = depth[v]
                valid[d] += 1
                heapq.heappush(heap, -d)
            cnt[v] = c + 1

        ans = [0] * n
        for i in range(n):
            path = paths[i]
            for v in path:
                dec(v)
            ans[i] = current_answer()
            for v in path:
                inc(v)
        return ans