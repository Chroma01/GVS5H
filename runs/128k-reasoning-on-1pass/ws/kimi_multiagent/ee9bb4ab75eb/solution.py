from typing import List
import heapq
import itertools
import os
import random


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # Removing any element leaves fewer than k strings.
        if n - 1 < k:
            return [0] * n

        # ---------- Build the trie ----------
        # child[v]: dict char -> node id
        # cnt[v]:   number of words passing through node v
        # depth[v]: depth of node v (root = 0)
        # term[v]:  list of word indices ending exactly at node v
        child = [{}]
        cnt = [0]
        depth = [0]
        term = [[]]

        for idx, w in enumerate(words):
            node = 0
            cnt[0] += 1
            for ch in w:
                nxt = child[node].get(ch)
                if nxt is None:
                    nxt = len(child)
                    child[node][ch] = nxt
                    child.append({})
                    cnt.append(0)
                    depth.append(depth[node] + 1)
                    term.append([])
                node = nxt
                cnt[node] += 1
            term[node].append(idx)

        # ---------- Per-depth count of "good" nodes (cnt >= k) ----------
        max_depth = max(depth)
        good_cnt = [0] * (max_depth + 1)
        for v in range(len(child)):
            if cnt[v] >= k:
                good_cnt[depth[v]] += 1

        # off_cnt[d] = number of good nodes at depth d NOT on the current DFS path.
        off_cnt = good_cnt[:]
        # Max-heap (via negation) of depths with off_cnt > 0, lazy deletion.
        heap = [-d for d in range(max_depth + 1) if off_cnt[d] > 0]
        heapq.heapify(heap)

        ans = [0] * n
        on_path = []  # depths of current-path nodes with cnt >= k+1 (increasing order)

        # ---------- Iterative DFS with enter/exit events ----------
        stack = [(0, True)]  # (node, is_entering)
        while stack:
            node, entering = stack.pop()
            d = depth[node]
            c = cnt[node]
            if entering:
                # Temporarily remove this node from the off-path structure.
                if c >= k:
                    off_cnt[d] -= 1
                # Track on-path nodes that survive removal (need cnt >= k+1).
                if c >= k + 1:
                    on_path.append(d)

                if term[node]:
                    # Best off-path depth: clean stale heap top entries.
                    while heap and off_cnt[-heap[0]] == 0:
                        heapq.heappop(heap)
                    best = on_path[-1] if on_path else -1
                    if heap and -heap[0] > best:
                        best = -heap[0]
                    if best < 0:
                        best = 0
                    for idx in term[node]:
                        ans[idx] = best

                stack.append((node, False))
                for nxt in child[node].values():
                    stack.append((nxt, True))
            else:
                # Restore this node into the off-path structure.
                if c >= k:
                    off_cnt[d] += 1
                    if off_cnt[d] == 1:
                        heapq.heappush(heap, -d)
                if c >= k + 1:
                    on_path.pop()

        return ans


# ---------------- Brute forces for verification ----------------

def lcp_len(a: str, b: str) -> int:
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    return i


def brute_combinations(words: List[str], k: int) -> List[int]:
    """Exhaustive: try every k-subset of remaining words (feasible for tiny n)."""
    n = len(words)
    ans = []
    for i in range(n):
        rem = [words[j] for j in range(n) if j != i]
        if len(rem) < k:
            ans.append(0)
            continue
        best = 0
        for combo in itertools.combinations(rem, k):
            best = max(best, len(os.path.commonprefix(list(combo))))
        ans.append(best)
    return ans


def brute_sorted(words: List[str], k: int) -> List[int]:
    """Sort remaining words; best k-subset is k consecutive in sorted order,
    and its common prefix equals LCP of the window's two endpoints."""
    n = len(words)
    ans = []
    for i in range(n):
        rem = sorted(words[j] for j in range(n) if j != i)
        if len(rem) < k:
            ans.append(0)
            continue
        best = 0
        for s in range(len(rem) - k + 1):
            best = max(best, lcp_len(rem[s], rem[s + k - 1]))
        ans.append(best)
    return ans


# ---------------- Test harness ----------------

def run_tests() -> None:
    sol = Solution()

    # Provided examples.
    assert sol.longestCommonPrefix(["jump", "run", "run", "jump", "run"], 2) == [3, 4, 4, 3, 4]
    assert sol.longestCommonPrefix(["dog", "racer", "car"], 2) == [0, 0, 0]
    print("Provided examples: OK")

    # Hand-picked edge cases.
    edge_cases = [
        (["a", "b"], 2),                       # k == n -> all zeros
        (["abc", "ab", "xyz"], 1),             # k = 1
        (["ab", "ab", "ab"], 2),               # all duplicates
        (["a", "ab", "abc"], 2),               # one word a prefix of another
        (["aaaa", "aaaa", "aaab", "aaab"], 3), # deep shared prefixes
        (["x"], 1),                            # single word, k == n
        (["m", "m"], 1),                       # duplicates with k = 1
        (["abcd", "abce", "abcf", "z"], 3),    # branching near the end
    ]
    for words, k in edge_cases:
        got = sol.longestCommonPrefix(words, k)
        exp = brute_combinations(words, k)
        assert got == exp, f"edge case failed: {words}, k={k}: got {got}, want {exp}"
        exp2 = brute_sorted(words, k)
        assert got == exp2, f"edge case failed (sorted): {words}, k={k}: got {got}, want {exp2}"
    print("Edge cases: OK")

    rng = random.Random(12345)

    # Small randomized tests vs exhaustive combinations brute force.
    for trial in range(3000):
        n = rng.randint(1, 8)
        alpha = rng.choice(["a", "ab", "abc"])
        words = ["".join(rng.choice(alpha) for _ in range(rng.randint(1, 6)))
                 for _ in range(n)]
        k = rng.randint(1, n)
        got = sol.longestCommonPrefix(words, k)
        exp = brute_combinations(words, k)
        assert got == exp, (
            f"trial {trial} failed: words={words}, k={k}: got {got}, want {exp}"
        )
    print("Randomized small tests (3000 trials vs combinations brute force): OK")

    # Medium randomized tests vs sorted-window brute force.
    for trial in range(500):
        n = rng.randint(1, 60)
        alpha = rng.choice(["ab", "abc", "abcd"])
        words = ["".join(rng.choice(alpha) for _ in range(rng.randint(1, 12)))
                 for _ in range(n)]
        k = rng.randint(1, n)
        got = sol.longestCommonPrefix(words, k)
        exp = brute_sorted(words, k)
        assert got == exp, (
            f"medium trial {trial} failed: words={words}, k={k}: got {got}, want {exp}"
        )
    print("Randomized medium tests (500 trials vs sorted-window brute force): OK")

    # Sanity: total length constraint scale, longer words.
    for trial in range(100):
        n = rng.randint(2, 30)
        alpha = "ab"
        words = ["".join(rng.choice(alpha) for _ in range(rng.randint(1, 40)))
                 for _ in range(n)]
        k = rng.randint(1, n)
        got = sol.longestCommonPrefix(words, k)
        exp = brute_sorted(words, k)
        assert got == exp, (
            f"long-word trial {trial} failed: k={k}: got {got}, want {exp}"
        )
    print("Randomized long-word tests (100 trials): OK")

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    run_tests()