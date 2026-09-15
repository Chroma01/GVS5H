from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        # If removing one word leaves fewer than k words, every answer is 0.
        if n <= k:
            return [0] * n

        # Trie stored compactly:
        # - first_child[node] / next_sibling[child] form child linked lists.
        # - trans maps (node, char) -> child using key = node * 26 + char_index.
        first_child = [-1]
        next_sibling = [-1]
        trans = {}

        count = [0]       # number of word occurrences passing through node
        depth = [0]       # prefix length represented by node
        term_head = [-1]  # linked list head of occurrences terminating at node
        term_next = [-1] * n

        # Build trie and terminal occurrence linked lists.
        for i, w in enumerate(words):
            node = 0
            for ch in w:
                key = node * 26 + (ord(ch) - 97)
                nxt = trans.get(key)
                if nxt is None:
                    nxt = len(count)
                    trans[key] = nxt

                    count.append(0)
                    depth.append(depth[node] + 1)
                    term_head.append(-1)
                    first_child.append(-1)

                    next_sibling.append(first_child[node])
                    first_child[node] = nxt

                node = nxt
                count[node] += 1

            term_next[i] = term_head[node]
            term_head[node] = i

        count[0] = n
        del trans

        # For nodes with count == k, record their DFS interval [l, r].
        # start_max[l] = max depth among intervals starting at l.
        # end_max[r]   = max depth among intervals ending at r.
        start_max = [0] * n
        end_max = [0] * n

        global_gt = 0       # deepest node with count > k
        current_pos = 0     # next DFS position for an occurrence

        # Iterative DFS. State 0 = enter, state 1 = exit.
        stack = [(0, 0, 0)]
        while stack:
            node, state, start = stack.pop()

            if state == 0:
                start = current_pos

                # Emit occurrences terminating here before children.
                # This makes every subtree occupy one contiguous position interval.
                occ = term_head[node]
                while occ != -1:
                    nxt = term_next[occ]
                    term_next[occ] = current_pos  # reuse as position of occurrence
                    current_pos += 1
                    occ = nxt

                stack.append((node, 1, start))

                child = first_child[node]
                while child != -1:
                    stack.append((child, 0, 0))
                    child = next_sibling[child]

            else:
                end = current_pos - 1
                cnt = count[node]
                d = depth[node]

                if cnt > k:
                    if d > global_gt:
                        global_gt = d
                elif cnt == k:
                    if start <= end:
                        if d > start_max[start]:
                            start_max[start] = d
                        if d > end_max[end]:
                            end_max[end] = d

        del term_head, first_child, next_sibling, count, depth, stack

        # Convert end_max into left_best:
        # left_best[p] = max depth of a count==k interval with r < p.
        running = 0
        for p in range(n):
            e = end_max[p]
            end_max[p] = running
            if e > running:
                running = e

        # Convert start_max into right_best:
        # right_best[p] = max depth of a count==k interval with l > p.
        running = 0
        for p in range(n - 1, -1, -1):
            s = start_max[p]
            start_max[p] = running
            if s > running:
                running = s

        # Combine global count>k answer with best count==k interval outside position.
        ans = [global_gt] * n
        for i, p in enumerate(term_next):
            best = end_max[p]
            if start_max[p] > best:
                best = start_max[p]
            if best > ans[i]:
                ans[i] = best

        return ans