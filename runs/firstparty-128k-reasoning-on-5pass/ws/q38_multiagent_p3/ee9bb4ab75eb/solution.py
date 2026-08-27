from typing import List
import heapq


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n <= k:
            return [0] * n

        # Trie nodes:
        # children[node] is None or a dict char -> child node
        # count[node] is the number of original words in this node's subtree
        # depth[node] is the prefix length represented by this node
        # terminals[node] is None or a list of original indices ending here
        children = [None]
        count = [0]
        depth = [0]
        terminals = [None]

        for idx, w in enumerate(words):
            node = 0
            count[node] += 1
            for ch in w:
                d = children[node]
                if d is None:
                    d = {}
                    children[node] = d

                nxt = d.get(ch)
                if nxt is None:
                    nxt = len(children)
                    d[ch] = nxt
                    children.append(None)
                    count.append(0)
                    depth.append(depth[node] + 1)
                    terminals.append(None)

                node = nxt
                count[node] += 1

            if terminals[node] is None:
                terminals[node] = []
            terminals[node].append(idx)

        m = len(children)
        marked = bytearray(m)
        active = bytearray(m)
        heap = []
        global_best = 0
        heappush = heapq.heappush
        heappop = heapq.heappop

        # Nodes with count >= k + 1 are usable after deleting any one word.
        # Nodes with count == k are usable only for deletions outside their subtree.
        for node in range(m):
            c = count[node]
            if c >= k + 1:
                if depth[node] > global_best:
                    global_best = depth[node]
            elif c == k:
                marked[node] = 1
                active[node] = 1
                heappush(heap, (-depth[node], node))

        del count

        ans = [0] * n
        stack = [0]  # non-negative: enter node; negative ~node: exit node

        while stack:
            item = stack.pop()

            if item >= 0:
                node = item

                # Marked nodes on the current root-to-node path are infeasible
                # for words ending in this subtree.
                if marked[node]:
                    active[node] = 0

                # Lazy deletion of inactive marked nodes.
                while heap and not active[heap[0][1]]:
                    heappop(heap)

                best = global_best
                if heap:
                    top_depth = -heap[0][0]
                    if top_depth > best:
                        best = top_depth

                t = terminals[node]
                if t is not None:
                    for idx in t:
                        ans[idx] = best

                # Exit marker first, then children, so children finish before exit.
                stack.append(~node)
                d = children[node]
                if d is not None:
                    stack.extend(d.values())

            else:
                node = ~item
                if marked[node]:
                    active[node] = 1
                    heappush(heap, (-depth[node], node))

        return ans


def _brute_force(words: List[str], k: int) -> List[int]:
    n = len(words)
    ans = [0] * n

    for i in range(n):
        if n - 1 < k:
            continue

        best = 0
        cnt = {}

        for j, w in enumerate(words):
            if j == i:
                continue

            for d in range(1, len(w) + 1):
                p = w[:d]
                c = cnt.get(p, 0) + 1
                cnt[p] = c
                if c >= k and d > best:
                    best = d

        ans[i] = best

    return ans


if __name__ == "__main__":
    sol = Solution()

    assert sol.longestCommonPrefix(["jump", "run", "run", "jump", "run"], 2) == [3, 4, 4, 3, 4]
    assert sol.longestCommonPrefix(["dog", "racer", "car"], 2) == [0, 0, 0]

    assert sol.longestCommonPrefix(["a"], 1) == [0]
    assert sol.longestCommonPrefix(["a", "b"], 1) == [1, 1]
    assert sol.longestCommonPrefix(["a", "ab"], 1) == [2, 1]
    assert sol.longestCommonPrefix(["ab", "ac", "ad"], 2) == [1, 1, 1]
    assert sol.longestCommonPrefix(["a", "a", "b"], 2) == [0, 0, 1]
    assert sol.longestCommonPrefix(["a", "aa", "aaa", "aaaa"], 2) == [3, 3, 2, 2]
    assert sol.longestCommonPrefix(["a", "aa", "aaa", "aaaa"], 1) == [4, 4, 4, 3]
    assert sol.longestCommonPrefix(["ab", "ab", "ac"], 2) == [1, 1, 2]

    import random
    random.seed(2024)

    for _ in range(500):
        n = random.randint(1, 8)
        k = random.randint(1, n)
        words = []

        for _ in range(n):
            length = random.randint(1, 5)
            words.append(''.join(random.choice('abc') for _ in range(length)))

        expected = _brute_force(words, k)
        got = sol.longestCommonPrefix(words, k)
        assert got == expected, (words, k, got, expected)