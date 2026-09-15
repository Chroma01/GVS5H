- **Problem reduction:** Removing word `w`, a prefix `P` supports `k` remaining strings iff remaining count `>= k`. If `P` is a prefix of `w` its count drops by one, so require `cnt[P] >= k+1`; otherwise require `cnt[P] >= k`. Answer = max depth over both sets.

- **Trie:** iterative build; `cnt[node]` = number of words having that prefix; root index 0 has count `n`. Only counts matter, not which indices.

- **On-path best:** Walk each word; track deepest node with `cnt >= k+1`. Counts are non-increasing down a path, so the last valid depth is the max. Start `best_on = 0` (empty prefix valid whenever `n > k`, which is exactly the non-trivial case).

- **Off-path via heavy nodes (`cnt >= k`):** Let `G` = max depth of a non-root heavy node. Cases: (a) no heavy node → off = 0; (b) `>= 2` heavy nodes at depth `G` → any word's path holds at most one, so off = `G` for all; (c) exactly one heavy node `v` at depth `G` → words not containing `v` get off = `G`, words containing `v` get off = `G2` = deepest heavy node that is NOT an ancestor of `v`.

- **Why `G2` is exact:** if `w` contains `v`, every prefix of `w` up to depth `G` is an ancestor of `v` (same branch), and no heavy node exists beyond depth `G`. So the heavy off-path nodes for `w` are precisely the heavy non-ancestors of `v`; deepest gives `G2`.

- **Short words:** a word shorter than `G` cannot contain `v`, so `reached_v` stays False and it correctly takes off = `G` (node `v` is genuinely off its path).

- **Special cases:** `n <= k` → all zeros (covers `n == k` and `k = 1, n = 1`). `k = 1` → every non-root node is heavy; `G` = longest word length, logic unchanged.

- **Verification (SAMPLE TESTS):** sample examples `["jump",...],2 -> [3,4,4,3,4]` and `["dog","racer","car"],2 -> [0,0,0]` → PASS. Edge cases: `["a"],1 -> [0]`, `["a","b"],2 -> [0,0]`, all-dup `["a","a","a"],2 -> [1,1,1]`, unique longest `["abcd","ab","xy"],1 -> [2,4,4]`, short-word `["abc","ab","xy"],1 -> [2,3,3]`, `["abc","abc","abd"],2 -> [2,2,3]` → PASS. Randomized stress: 20000 cases, `n in 1..8`, `k in 1..n`, alphabet `{a,b}`, lengths 1..4, compared against naive brute force → PASS, no counterexample found.

- **Complexity:** Time O(sum |words|), memory O(sum |words|). Fully iterative; safe for total length 1e5 and single words up to 1e4.

- **Harness placement:** the brute force + stress test live under `if __name__ == "__main__"`, so importing the module / grading the class has no side effects.

- **Earlier plan dropped:** the per-depth top-two + binary-search approach was replaced by this O(sum) method; it is the single source of truth now.
