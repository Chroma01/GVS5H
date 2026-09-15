from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n == 0:
            return []

        # Trie arrays:
        # children[node] maps character -> child node
        # count[node] = number of words having this prefix
        # depth[node] = prefix length
        # term_head[node] / next_term[i] store terminal word indices as linked lists
        children = [{}]
        count = [0]
        depth = [0]
        term_head = [-1]
        next_term = [-1] * n

        for i, w in enumerate(words):
            count[0] += 1
            node = 0
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    count.append(0)
                    depth.append(depth[node] + 1)
                    term_head.append(-1)
                node = nxt
                count[node] += 1

            next_term[i] = term_head[node]
            term_head[node] = i

        # pos_to_orig[pos] = original index of the word assigned to DFS position pos
        pos_to_orig = [0] * n

        # For prefixes with count == k, their terminal positions form an interval [l, r].
        # They are valid for deletions outside that interval.
        best_start = [0] * n
        best_end = [0] * n

        global_best = 0
        need_global = k + 1
        pos = 0

        # Iterative DFS. State 0 = enter, state 1 = exit.
        # On enter, assign terminal positions, then process children, then exit.
        stack = [(0, 0, 0)]  # node, state, start position
        while stack:
            node, state, start = stack.pop()

            if state == 0:
                start = pos

                idx = term_head[node]
                while idx != -1:
                    pos_to_orig[pos] = idx
                    pos += 1
                    idx = next_term[idx]

                stack.append((node, 1, start))
                for child in children[node].values():
                    stack.append((child, 0, 0))

            else:
                end = pos - 1
                c = count[node]
                d = depth[node]

                if c >= need_global:
                    if d > global_best:
                        global_best = d
                elif c == k:
                    if d > best_start[start]:
                        best_start[start] = d
                    if d > best_end[end]:
                        best_end[end] = d

        # suffix[p] = max depth of a count == k interval starting after p
        suffix = [0] * n
        running = 0
        for p in range(n - 1, -1, -1):
            suffix[p] = running
            if best_start[p] > running:
                running = best_start[p]

        # Combine global prefixes and count == k prefixes outside each position.
        ans = [0] * n
        running = 0
        for p in range(n):
            outside = running if running > suffix[p] else suffix[p]
            ans[pos_to_orig[p]] = global_best if global_best > outside else outside

            if best_end[p] > running:
                running = best_end[p]

        return ans


if __name__ == "__main__":
    sol = Solution()
    assert sol.longestCommonPrefix(["jump", "run", "run", "jump", "run"], 2) == [3, 4, 4, 3, 4]
    assert sol.longestCommonPrefix(["dog", "racer", "car"], 2) == [0, 0, 0]
    print("sample tests passed")