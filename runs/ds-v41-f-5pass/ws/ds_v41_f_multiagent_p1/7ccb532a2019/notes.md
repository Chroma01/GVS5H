- **Problem restated:** For a fixed target frequency k, every letter must end with 0 or k occurrences. The answer is the minimum over all valid k.

- **Core cost model:** For fixed k and per-letter target d_i in {0,k}, base cost = sum |c_i - d_i|. A change operation moves a character one step forward (i -> i+1), saving 1 compared to delete+insert. Only adjacent shifts matter; shifting distance >= 2 costs at least as much as delete+insert, so it never improves the minimum.

- **Savings independence:** For fixed targets, letter i is either excess (d_i=0) or deficit (d_i=k), never both. The saving on edge (i-1 -> i) is min(excess_{i-1}, deficit_i). Edges do not conflict, so savings can be summed.

- **DP over letters:** dp0, dp1 = minimum cost for the prefix ending at the current letter, with target count 0 or k. Transition:
  ndp0 = c + min(dp0, dp1)
  ndp1 = |c - k| + min(dp0 - s01, dp1 - s11)
  where s01 = min(prev_c, max(0, k - c)), s11 = min(max(0, prev_c - k), max(0, k - c)).
  Here prev_c is the count of the previous letter.

- **Complexity:** O(26 * n) time, O(1) extra space. For n = 20000 this is about 500k inner steps, which runs well under 0.1s in Python.

- **Verification:** Samples: "acab" -> 1, "wddw" -> 0, "aaabc" -> 2. All PASS. Stress test: brute-force BFS over count vectors for reduced alphabets (3–5 letters, lengths 3–8) on 1000 random cases. Every case matched the DP. No mismatches. Worst-case timing: n = 20000 runs in <0.1s.

- **Disproven ideas:** Meet-in-the-middle over subsets is too slow. Naive carried-excess DP with carry as a value is O(26*k) per k. Multi-step flow models incorrectly allow a letter to both send and receive. Submodular min-cut works but DP is simpler and faster.

- **Edge cases:** k = 0 handled by best = n initially. k > n cannot beat deleting all. Zero-count letters are handled naturally. No wraparound edge (z cannot change to a).
