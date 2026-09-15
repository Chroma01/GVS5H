- **Problem restated:** For each k in [0, M-1], B_i = (A_i + k) mod M; output inversion count of B. N, M up to 2e5. Need O(N log M + M).

- **Per-pair contribution:** For i<j with a = A_i, b = A_j. If a == b, never an inversion. The set of k where the pair (i,j) is an inversion is exactly the circular interval [pos_b, pos_a) where pos_x = (M - x) % M. Start = pos of the later element's value, end = pos of the earlier element's value. Verified against samples.

- **Why:** a'>b' (shifted values) analysis shows inversion iff the wrap boundary M-k lies in the arc from b to a; this yields the interval [pos_b, pos_a). Empty interval iff a == b. Length is M-(a-b) when a>b and b-a when a<b.

- **Difference-array over k:** For a non-circular pair (pos_b < pos_a): +1 at pos_b, -1 at pos_a. For a circular pair (pos_b > pos_a): +1 at pos_b, -1 at pos_a, plus an extra +1 at index 0 (the -1 at index M is ignored since k<M). So ans[k] = prefix sum of D[0..k].

- **Aggregation trick:** Count pairs by start value and end value instead of enumerating.
  - Distinct pairs total = C(N,2) - E, where E = sum over v of C(cnt[v],2).
  - Non-circular pairs = invStrict = #{(i<j): pos_{A_i} > pos_{A_j}} (Fenwick over pos). Circular pairs W = C(N,2) - E - invStrict.
  - Starts at pos_v (pairs with A_j=v, i<j, A_i != v) = sumIdx[v] - C(cnt[v],2) = startVal[v].
  - Ends at pos_v (pairs with A_i=v, i<j, A_j != v) = sumAfter[v] - C(cnt[v],2) = endVal[v].
  - The C(cnt,2) terms cancel, so D[pos_v] += sumIdx[v] - sumAfter[v]; then D[0] += W.

- **Index conventions:** pos_x = (M - x) % M handles x=0 (gives 0) and avoids M. sumIdx uses 0-based indices (i), sumAfter uses (n-1-i). invStrict uses the same pos and counts strictly greater among earlier elements.

- **Fenwick details:** size M (indices 0..M-1 shifted by +1). For each i, query count of inserted pos <= p, add (inserted - that) to invStrict, then insert p. invStrict can be ~2e10; Python ints handle it.

- **Complexity:** O(N log M + M) time, O(N + M) memory. No O(NM) enumeration.

- **Validation (manual, by hand, all pass):**
  - Sample 1: N=3,M=3,A=[2,1,0] -> [3,1,1].
  - Sample 2: N=5,M=6,A=[5,3,5,0,1] -> [7,3,3,1,1,5].
  - Sample 3: N=7,M=7,A=[0,1,2,3,4,5,6] -> [0,6,10,12,12,10,6].
  - Edge N=1: E=0, invStrict=0, W=0, all deltas 0 -> all zeros.
  - Edge M=1 (all A_i=0): E=C(N,2), invStrict=0, W=0, delta=0 -> output 0.

- **Pitfalls addressed:** strict inequality (equal values excluded via E and via equal pos giving empty interval); use modulo to keep pos in range; process D[0] extra term = number of circular pairs; prefix sums give answers in k order 0..M-1.
