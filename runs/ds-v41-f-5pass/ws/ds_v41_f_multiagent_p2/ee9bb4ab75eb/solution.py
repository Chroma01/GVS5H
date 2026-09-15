from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n == k:
            return [0] * n

        children = [{}]
        cnt = [0]
        depth = [0]

        for w in words:
            u = 0
            cnt[u] += 1
            for ch in w:
                v = children[u].get(ch)
                if v is None:
                    v = len(children)
                    children[u][ch] = v
                    children.append({})
                    cnt.append(0)
                    depth.append(depth[u] + 1)
                u = v
                cnt[u] += 1

        N = len(children)

        # mx[u] = maximum depth of a node in subtree(u) with cnt >= k
        mx = [-1] * N
        for u in range(N - 1, -1, -1):
            best = depth[u] if cnt[u] >= k else -1
            for v in children[u].values():
                if mx[v] > best:
                    best = mx[v]
            mx[u] = best

        # Top two child-subtree mx values for each node
        best1 = [-1] * N
        best2 = [-1] * N
        bestc = [-1] * N
        for u in range(N):
            b1 = -1
            b2 = -1
            bc = -1
            for v in children[u].values():
                val = mx[v]
                if val > b1:
                    b2 = b1
                    b1 = val
                    bc = v
                elif val > b2:
                    b2 = val
            best1[u] = b1
            best2[u] = b2
            bestc[u] = bc

        ans = [0] * n

        for i, w in enumerate(words):
            u = 0
            best_out = 0   # best usable prefix not on w's path
            best_on = 0    # best usable prefix on w's path, needing cnt >= k+1

            for ch in w:
                v = children[u][ch]

                # Best good node in a sibling subtree of this path step
                if v == bestc[u]:
                    cand = best2[u]
                else:
                    cand = best1[u]
                if cand > best_out:
                    best_out = cand

                u = v
                if cnt[u] >= k + 1:
                    d = depth[u]
                    if d > best_on:
                        best_on = d

            # At the terminal node, all child subtrees branch off the path
            if best1[u] > best_out:
                best_out = best1[u]

            ans[i] = best_out if best_out > best_on else best_on

        return ans