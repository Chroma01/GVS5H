- **Problem model:** The operation replaces every occurrence of a letter x with y. If a letter in S must become two different letters in T, it is impossible (print -1). Otherwise the required mapping f is a functional graph on the letters present in S.
- **Base operations:** Every non-self letter c (f[c] != c) requires at least one operation. Let base be the count of such letters.
- **Cycles:** Each component has one cycle. A cycle of length L>1 normally needs one extra operation to break, because a temporary letter is required. A cycle of length 1 (fixed point) costs nothing extra.
- **Isolated cycle:** A cycle is isolated if no node outside the cycle maps into any node of the cycle (i.e., the component consists solely of the cycle). An isolated cycle needs +1 operation if it can be broken (i.e., a spare letter exists).
- **Tree-attached cycle:** If a cycle has at least one tree node attached (some outside node maps into the cycle), it can be broken without an extra operation by merging a cycle node into a tree node that shares its target.
- **Spare letter:** Needed to break isolated cycles. A spare exists if:
  - Some letter among the 26 never appears in S (len(present) < 26), or
  - All 26 letters appear and f is not injective (some target has ≥2 preimages, i.e. len(set(f[c] for c in present)) < 26).
  If all 26 appear and f is injective (a permutation), no spare exists.
- **Answer:**
  - If no isolated cycles: base.
  - Else if a spare exists: base + (number of isolated cycles).
  - Else: -1.
- **Cycle detection:** With at most 26 nodes, an iterative walk with a current-path index map works. Mark all nodes on the path as done after each walk. Only record cycles of length >1.
- **Verification:** All four samples pass (4, 0, -1, 4). Adversarial cases:
  (a) 26-cycle, all 26 present → -1.
  (b) 2-cycle + fixed point c with incoming d->c (all 26 present) → 4.
  (c) 2-cycle + fixed point with no incoming (all 26 present) → -1.
  (d) N=1: "a"->"a" → 0; "a"->"b" → 1.
  (e) conflict "abac"->"abrc" → -1.
  (f) S==T → 0.
  (g) "abac"->"bcba" → 4.
