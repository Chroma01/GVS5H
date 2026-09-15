from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, l in edges:
            adj[u].append((v, l))
            adj[v].append((u, l))

        max_val = max(nums) if nums else 0
        last = [-1] * (max_val + 1)
        pref = [0] * (n + 1)

        best_len = 0
        best_nodes = 1

        # stack entries:
        # type 0 (enter): (0, node, parent, depth, parent_m0, edge_len)
        # type 1 (exit):  (1, node, old_last_value)
        stack = [(0, 0, -1, 0, 0, 0)]

        while stack:
            item = stack.pop()
            if item[0] == 1:
                _, v, old = item
                last[nums[v]] = old
            else:
                _, v, p, depth, parent_m0, elen = item
                x = nums[v]
                prev = last[x]
                m0 = parent_m0
                if prev != -1 and prev + 1 > m0:
                    m0 = prev + 1

                pref[depth] = (pref[depth - 1] if depth > 0 else 0) + elen
                cur_len = pref[depth] - pref[m0]
                cur_nodes = depth - m0 + 1

                if cur_len > best_len or (cur_len == best_len and cur_nodes < best_nodes):
                    best_len = cur_len
                    best_nodes = cur_nodes

                old = last[x]
                last[x] = depth
                stack.append((1, v, old))

                for to, l in adj[v]:
                    if to != p:
                        stack.append((0, to, v, depth + 1, m0, l))

        return [best_len, best_nodes]