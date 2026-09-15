- **Problem recap:** segment starts on a 1, then follows 2,0,2,0,... along a diagonal; at most one clockwise 90-degree turn to another diagonal is allowed (turn cell counted once). Length = cell count. Return 0 if no segment.

- **Direction convention:** dirs=((1,1),(1,-1),(-1,-1),(-1,1)) = down-right, down-left, up-left, up-right. A clockwise 90-degree turn is exactly i -> (i+1)%4, i.e. cw=(1,2,3,0). Checked against examples 1 and 2.

- **Suffix arrays g2/g0 (turn already spent):** g2[d][cell] = maximal alternating run length strictly AFTER cell in direction d when next required value is 2 (g0 for 0). Recurrence: neighbor 2 -> g2 = 1 + g0[neighbor]; neighbor 0 -> g0 = 1 + g2[neighbor]; else 0. Neighbor value 1 never matches, so it always stops the run.

- **Turn-aware arrays h2/h0 (turn still available):** h2[d][cell] (h0 for next-required 0) = max additional cells after cell in direction d. Options: stop (0); continue straight in d (neighbor 2 -> 1 + h0, neighbor 0 -> 1 + h2); turn clockwise at cell to cd=cw[d] (neighbor 2 -> 1 + g0_cd, neighbor 0 -> 1 + g2_cd). Max of the three. Uses g of the turn direction, which is fully precomputed first, so per-direction processing is valid.

- **Answer:** for every cell with value 1, candidate = 1 + h2[d][cell] over all four d; take the max. Single 1 -> 1; no 1 -> 0. Pure straight (no-turn) segments are naturally included via the straight/stop options.

- **Ordering / dependencies:** process each direction in reverse dependency order: rows descending if dr==1 else ascending; cols descending if dc==1 else ascending. Guarantees the neighbour (r+dr, c+dc) state exists before the current cell for both g and h.

- **Turn-at-start is harmless:** turning immediately at a start 1 yields 1 + g0_cd[neighbor], but starting fresh in direction cd gives 1 + h2_cd[start] >= 2 + g0_cd[neighbor] (h >= straight >= g), so it never inflates the answer even if one considered arm-1 length 1 invalid.

- **Complexity:** O(n*m) per direction, 8 linear passes total (4 for g, 4 for h), O(n*m) memory. n,m <= 500 -> ~250k cells/pass, ~2M cell ops. g stored as array('H') (values <= 500) to keep memory low; h as plain lists for speed.

- **Verification (executed):** provided examples produce exactly 5, 4, 5, 1 (expected 5, 4, 5, 1) -> PASS. Example 1 path (0,2)->(1,3)->(2,4) turn ->(3,3)->(4,2); example 2 path (2,3)->(3,2) turn ->(2,1)->(1,0); example 3 straight (0,0)->(4,4); example 4 single cell.

- **Independent brute force + random cross-check:** brute force enumerates every value-1 start cell, all 4 first-arm directions, alternating required values beginning at 2, and an optional single clockwise turn (turn changes direction at the current cell without consuming a cell; turn flag then blocks any second turn). Compared against the DP over many random grids with n,m <= 6 and values in {0,1,2}. Result: PASS on all trials, no counterexample found. The h/g recurrences are the exact DP counterpart of this enumeration, so they agree by construction.

- **Edge cases handled:** n==1 or m==1 -> no diagonal moves, answer is 1 iff a 1 exists; no 1 -> 0; single cell [[1]] -> 1.
