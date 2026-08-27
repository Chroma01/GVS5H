from typing import List
from collections import deque
from itertools import combinations
import random


def _lcp(a: str, b: str) -> int:
    m = min(len(a), len(b))
    i = 0
    while i < m and a[i] == b[i]:
        i += 1
    return i


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        def sliding_min(arr: List[int], m: int) -> List[int]:
            if m <= 0:
                return [0] * len(arr)
            if m > len(arr):
                return []
            dq = deque()
            res = []
            for i, x in enumerate(arr):
                while dq and arr[dq[-1]] >= x:
                    dq.pop()
                dq.append(i)
                while dq and dq[0] <= i - m:
                    dq.popleft()
                if i >= m - 1:
                    res.append(arr[dq[0]])
            return res

        pairs = sorted((w, i) for i, w in enumerate(words))
        sw = [w for w, _ in pairs]
        pos = [0] * n
        for p, (_, idx) in enumerate(pairs):
            pos[idx] = p

        adj = [_lcp(sw[i], sw[i + 1]) for i in range(n - 1)]

        if k == 1:
            W1 = [len(w) for w in sw]
        else:
            W1 = sliding_min(adj, k - 1)
        W2 = sliding_min(adj, k)

        L1 = len(W1)
        pref = [0] * L1
        cur = 0
        for i, v in enumerate(W1):
            if v > cur:
                cur = v
            pref[i] = cur

        suff = [0] * L1
        cur = 0
        for i in range(L1 - 1, -1, -1):
            if W1[i] > cur:
                cur = W1[i]
            suff[i] = cur

        L2 = len(W2)
        ans_sorted = [0] * n
        dq = deque()

        for p in range(n):
            if p < L2:
                v = W2[p]
                while dq and W2[dq[-1]] <= v:
                    dq.pop()
                dq.append(p)

            low = p - k
            while dq and dq[0] < low:
                dq.popleft()

            best2 = W2[dq[0]] if dq else 0

            best1 = 0
            li = p - k
            if li >= 0:
                if li >= L1:
                    li = L1 - 1
                if li >= 0:
                    best1 = pref[li]

            ri = p + 1
            if ri < L1 and suff[ri] > best1:
                best1 = suff[ri]

            ans_sorted[p] = best1 if best1 > best2 else best2

        return [ans_sorted[p] for p in pos]


def _brute(words: List[str], k: int) -> List[int]:
    n = len(words)
    res = []
    for i in range(n):
        rem = words[:i] + words[i + 1:]
        if len(rem) < k:
            res.append(0)
            continue
        best = 0
        for comb in combinations(rem, k):
            v = len(comb[0])
            for x in comb[1:]:
                v = min(v, _lcp(comb[0], x))
                if v == 0:
                    break
            if v > best:
                best = v
        res.append(best)
    return res


if __name__ == "__main__":
    sol = Solution()

    assert sol.longestCommonPrefix(["jump", "run", "run", "jump", "run"], 2) == [3, 4, 4, 3, 4]
    assert sol.longestCommonPrefix(["dog", "racer", "car"], 2) == [0, 0, 0]
    assert sol.longestCommonPrefix(["a"], 1) == [0]
    assert sol.longestCommonPrefix(["a", "b"], 2) == [0, 0]
    assert sol.longestCommonPrefix(["a", "b"], 1) == [1, 1]
    assert sol.longestCommonPrefix(["a", "b", "c"], 1) == [1, 1, 1]
    assert sol.longestCommonPrefix(["a", "aa", "aaa"], 2) == [2, 1, 1]
    assert sol.longestCommonPrefix(["run", "run", "run"], 2) == [3, 3, 3]
    assert sol.longestCommonPrefix(["a", "ab", "abc", "abcd"], 2) == [3, 3, 2, 2]
    assert sol.longestCommonPrefix(["a", "aa", "aaa", "b"], 3) == [0, 0, 0, 1]

    random.seed(12345)
    for _ in range(500):
        n = random.randint(1, 8)
        k = random.randint(1, n)
        words = []
        for __ in range(n):
            L = random.randint(1, 4)
            words.append(''.join(random.choice('ab') for _ in range(L)))
        if n > 1 and random.random() < 0.5:
            a = random.randrange(n)
            b = random.randrange(n - 1)
            if b >= a:
                b += 1
            words[a] = words[b]

        expected = _brute(words, k)
        got = sol.longestCommonPrefix(words, k)
        assert got == expected, (words, k, expected, got)

    print("All tests passed")