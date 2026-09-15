from typing import List
import random


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # Removing one index leaves n-1 strings; if fewer than k remain the answer is 0.
        if n <= k:
            return [0] * n

        # Build trie: each node is a prefix, cnt[node] = number of words having it as a prefix.
        children = [{}]
        cnt = [0]
        parent = [-1]
        depth = [0]

        for w in words:
            cur = 0
            for ch in w:
                nxt = children[cur].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[cur][ch] = nxt
                    children.append({})
                    cnt.append(0)
                    parent.append(cur)
                    depth.append(depth[cur] + 1)
                cur = nxt
                cnt[cur] += 1

        m = len(children)

        # Heavy node: cnt >= k (a prefix shared by at least k words).
        # G = max depth among non-root heavy nodes; v_id = that node if unique, else -1.
        G = -1
        v_id = -1
        heavy_at_G = 0
        for i in range(1, m):
            if cnt[i] >= k:
                di = depth[i]
                if di > G:
                    G = di
                    v_id = i
                    heavy_at_G = 1
                elif di == G:
                    heavy_at_G += 1

        unique = False
        G2 = 0
        off_all = 0
        if G == -1:
            # No non-root prefix is shared by k words.
            off_all = 0
        elif heavy_at_G >= 2:
            # >=2 heavy nodes at the deepest heavy depth; any word's path contains at most one
            # of them, so another depth-G heavy node is off-path -> off contribution is G.
            off_all = G
        else:
            # Unique deepest heavy node v. Words not having v as a prefix get off = G.
            unique = True
            off_all = G
            # G2 = deepest heavy node that is NOT an ancestor of v, valid for words containing v.
            anc = set()
            x = v_id
            while x != -1:
                anc.add(x)
                x = parent[x]
            for i in range(1, m):
                if cnt[i] >= k and i not in anc and depth[i] > G2:
                    G2 = depth[i]

        kp1 = k + 1
        ans = [0] * n
        for idx in range(n):
            w = words[idx]

            # On-path best: deepest prefix of w whose remaining count (cnt-1) >= k,
            # i.e. cnt >= k+1. Counts are non-increasing along the path; root (empty) is valid.
            best_on = 0
            cur = 0
            d = 0
            reached_v = False
            for ch in w:
                cur = children[cur][ch]
                d += 1
                if cnt[cur] >= kp1:
                    best_on = d
                if unique and cur == v_id:
                    reached_v = True

            off = G2 if (unique and reached_v) else off_all
            ans[idx] = best_on if best_on >= off else off

        return ans


def _brute(words, k):
    n = len(words)
    res = []
    for i in range(n):
        rem = words[:i] + words[i + 1:]
        if len(rem) < k:
            res.append(0)
            continue
        pc = {}
        for w in rem:
            for L in range(1, len(w) + 1):
                p = w[:L]
                pc[p] = pc.get(p, 0) + 1
        best = 0
        for p, c in pc.items():
            if c >= k and len(p) > best:
                best = len(p)
        res.append(best)
    return res


def _run_tests():
    sol = Solution()

    ex = [
        (["jump", "run", "run", "jump", "run"], 2, [3, 4, 4, 3, 4]),
        (["dog", "racer", "car"], 2, [0, 0, 0]),
    ]
    ok = True
    for words, k, want in ex:
        got = sol.longestCommonPrefix(words, k)
        if got != want:
            ok = False
            print("EXAMPLE FAIL", words, k, got, want)
    print("sample examples:", "PASS" if ok else "FAIL")

    edge = [
        (["a"], 1, [0]),
        (["a", "b"], 2, [0, 0]),
        (["a", "a", "a"], 2, [1, 1, 1]),
        (["abcd", "ab", "xy"], 1, [2, 4, 4]),
        (["abc", "ab", "xy"], 1, [2, 3, 3]),
        (["abc", "abc", "abd"], 2, [2, 2, 3]),
    ]
    eok = True
    for words, k, want in edge:
        got = sol.longestCommonPrefix(words, k)
        if got != want:
            eok = False
            print("EDGE FAIL", words, k, got, want)
    print("edge cases:", "PASS" if eok else "FAIL")

    random.seed(12345)
    fail = None
    for _ in range(20000):
        n = random.randint(1, 8)
        k = random.randint(1, n)
        words = []
        for _ in range(n):
            L = random.randint(1, 4)
            words.append("".join(random.choice("ab") for _ in range(L)))
        got = sol.longestCommonPrefix(words, k)
        want = _brute(words, k)
        if got != want:
            fail = (words, k, got, want)
            break
    if fail:
        print("random stress: FAIL", fail)
        ok = False
    else:
        print("random stress (20000 cases): PASS")
    return ok and eok


if __name__ == "__main__":
    _run_tests()