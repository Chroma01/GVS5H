from typing import List
import random
from itertools import combinations


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        children = [{}]
        count = [0]
        depth = [0]
        terminal = [0] * n

        for i, word in enumerate(words):
            node = 0
            count[0] += 1
            for c in word:
                nxt = children[node].get(c)
                if nxt is None:
                    nxt = len(children)
                    children[node][c] = nxt
                    children.append({})
                    count.append(0)
                    depth.append(depth[node] + 1)
                node = nxt
                count[node] += 1
            terminal[i] = node

        m = len(children)
        base = -1
        need = k + 1
        for u in range(m):
            if count[u] >= need and depth[u] > base:
                base = depth[u]

        desc = [-1] * m
        best_sub = [-1] * m
        for u in range(m - 1, -1, -1):
            deepest = -1
            for v in children[u].values():
                bv = best_sub[v]
                if bv > deepest:
                    deepest = bv
            desc[u] = deepest
            best = deepest
            if count[u] == k and depth[u] > best:
                best = depth[u]
            best_sub[u] = best

        side = [-1] * m
        for u in range(m):
            top1 = -1
            top2 = -1
            top1_id = -1
            for v in children[u].values():
                bv = best_sub[v]
                if bv > top1:
                    top2 = top1
                    top1 = bv
                    top1_id = v
                elif bv > top2:
                    top2 = bv

            su = side[u]
            for v in children[u].values():
                other = top2 if v == top1_id else top1
                side[v] = su if su > other else other

        ans = [0] * n
        for i, v in enumerate(terminal):
            a = base
            if a < 0:
                a = 0
            if desc[v] > a:
                a = desc[v]
            if side[v] > a:
                a = side[v]
            ans[i] = a
        return ans


def _lcp(a: str, b: str) -> int:
    m = min(len(a), len(b))
    i = 0
    while i < m and a[i] == b[i]:
        i += 1
    return i


def _brute(words: List[str], k: int) -> List[int]:
    n = len(words)
    if n - 1 < k:
        return [0] * n

    ans = []
    for i in range(n):
        rem = [j for j in range(n) if j != i]
        best = 0
        for comb in combinations(rem, k):
            if k == 1:
                cur = len(words[comb[0]])
            else:
                first = words[comb[0]]
                cur = len(first)
                for j in comb[1:]:
                    cur = _lcp(first, words[j])
                    if cur == 0:
                        break
            if cur > best:
                best = cur
        ans.append(best)
    return ans


def _run_verification() -> None:
    sol = Solution()

    cases = [
        (["jump", "run", "run", "jump", "run"], 2, [3, 4, 4, 3, 4]),
        (["dog", "racer", "car"], 2, [0, 0, 0]),
        (["a"], 1, [0]),
        (["a", "b"], 2, [0, 0]),
        (["a", "b"], 1, [1, 1]),
        (["a", "ab", "abc"], 2, [2, 1, 1]),
        (["a", "a", "ab", "abc"], 2, [2, 2, 1, 1]),
        (["a", "ab", "ab"], 2, [2, 1, 1]),
        (["abc", "abd", "xyz"], 2, [0, 0, 2]),
        (["a", "a", "b"], 2, [0, 0, 1]),
        (["dog", "racer", "car"], 1, [5, 3, 5]),
        (["same"] * 5, 3, [4] * 5),
        (["a", "b", "c"], 2, [0, 0, 0]),
    ]

    for words, k, expected in cases:
        got = sol.longestCommonPrefix(words, k)
        assert got == expected, (words, k, got, expected)

    random.seed(12345)
    for _ in range(1000):
        n = random.randint(1, 7)
        k = random.randint(1, n)
        words = []
        for _ in range(n):
            length = random.randint(1, 4)
            words.append(''.join(random.choice('abc') for _ in range(length)))
        expected = _brute(words, k)
        got = sol.longestCommonPrefix(words, k)
        assert got == expected, (words, k, got, expected)

    large = ["a" * 10000] * 10
    got = sol.longestCommonPrefix(large, 5)
    assert got == [10000] * 10, got

    large2 = ["a"] * 100000
    got2 = sol.longestCommonPrefix(large2, 50000)
    assert all(x == 1 for x in got2), got2[:10]

    print("All verification tests passed")


if __name__ == "__main__":
    _run_verification()