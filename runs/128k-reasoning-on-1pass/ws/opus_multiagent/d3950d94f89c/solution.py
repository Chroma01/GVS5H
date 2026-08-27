from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        maxv = max(nums) if nums else 0
        lastIdx = [-1] * (maxv + 1)

        dist = [0]          # dist[i] = root distance of the i-th node on the current chain
        bestLen = 0
        bestNodes = 1

        stack = []
        u = 0
        parent = -1
        start = 0

        while True:
            # ---- enter node u (its distance already appended to `dist`) ----
            k = len(dist) - 1
            val = nums[u]
            old = lastIdx[val]
            if old + 1 > start:
                start = old + 1
            lastIdx[val] = k
            L = dist[k] - dist[start]
            cnt = k - start + 1
            if L > bestLen or (L == bestLen and cnt < bestNodes):
                bestLen = L
                bestNodes = cnt
            stack.append((u, parent, start, val, old, iter(adj[u])))

            # ---- advance: find next child to enter, unwinding finished frames ----
            while stack:
                u2, p2, s2, val2, old2, it = stack[-1]
                nxt = None
                for (v, w) in it:
                    if v != p2:
                        nxt = (v, w)
                        break
                if nxt is None:
                    # exit node u2
                    lastIdx[val2] = old2
                    dist.pop()
                    stack.pop()
                else:
                    v, w = nxt
                    dist.append(dist[-1] + w)
                    u = v
                    parent = u2
                    start = s2
                    break
            else:
                break  # stack empty -> DFS complete

        return [bestLen, bestNodes]