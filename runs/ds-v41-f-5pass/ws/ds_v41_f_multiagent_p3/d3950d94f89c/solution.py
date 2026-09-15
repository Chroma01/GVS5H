from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        best_len = 0
        best_nodes = 1          # a single node is always a valid special path
        last = {}               # value -> depth of nearest ancestor on current path
        pref = [0] * (n + 1)    # pref[d] = root-to-node prefix length at depth d

        # stack frames: (kind, ...)  kind 0 = enter, kind 1 = exit
        # enter frame: (0, node, parent, depth, m_parent, w)
        # exit frame:  (1, node, saved_prev_last)
        stack = [(0, 0, -1, 0, -1, 0)]

        while stack:
            frame = stack.pop()
            if frame[0] == 1:
                _, node, saved = frame
                last[nums[node]] = saved
            else:
                _, node, parent, depth, m_parent, w = frame
                v = nums[node]
                prev = last.get(v, -1)              # previous occurrence depth on path
                m = m_parent if m_parent > prev else prev  # max prev over root..node
                if depth == 0:
                    pref[0] = 0
                else:
                    pref[depth] = pref[depth - 1] + w
                start = m + 1                        # earliest valid start depth
                length = pref[depth] - pref[start]
                cnt = depth - start + 1
                if length > best_len or (length == best_len and cnt < best_nodes):
                    best_len = length
                    best_nodes = cnt

                stack.append((1, node, prev))
                last[v] = depth
                for nxt, nw in adj[node]:
                    if nxt != parent:
                        stack.append((0, nxt, node, depth + 1, m, nw))

        return [best_len, best_nodes]