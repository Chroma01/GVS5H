
## ideation
Core difficulty: For each middle index i, we must count ways to pick 2 elements from the left and 2 from the right such that nums[i] is the unique mode. The frequency of nums[i] in the subsequence is 1 + (count of chosen elements equal to nums[i]), ranging from 1 to 3. For each case we must ensure no other value reaches that frequency. Naive enumeration is O(n^5); we need combinatorial counting with frequency maps.

Key structure: For fixed i, let L = left multiset, R = right multiset. We pick 2 from L, 2 from R. Let k = number of picked elements equal to v = nums[i] (0..4, but capped by availability). Then v's count is 1+k. Other values must appear strictly fewer than 1+k times.

Cases by total count of v (1+k):
- k=0 (v appears once): all other values must appear at most... wait, unique mode means v appears strictly more than any other. If v appears once, all others appear at most 0 — impossible since we pick 4 other elements. Actually if v appears once, every other element appears at most... each other value can appear at most 0 times? No — others must appear < 1, i.e., 0 times. But we pick 4 elements, contradiction. So k=0 contributes 0. Wait, actually if v appears once and all 4 others are distinct values, each appears once — tie, not unique. So indeed k=0 gives 0.
- k=1 (v appears twice): every other value appears at most once. So among the 4 picked elements, exactly one equals v, and the other three are all distinct values (and ≠ v).
- k=2 (v appears 3 times): other values appear at most 1 each... no, at most 2 but must be < 3, so at most 2 — but also they could appear twice as long as not 3. With only 3 remaining slots, other values can appear at most 2 times each, but we need < 3, so pairs of equal values allowed but not triples. Wait: remaining 3 elements, 2 equal v. The other 3 elements: no value may appear 3+ times... they must appear < 3, so at most 2. So the only forbidden pattern is all 3 equal (same non-v value). Hmm, but also they can't equal v (that would change k). So count = (ways to pick 2 v's among 4 slots) × (ways to pick other 2... wait k=2 means exactly 2 of the 4 picked equal v, other 2 picked are non-v with no restriction except not both... they can be equal to each other (appearing twice < 3, fine). So any 2 non-v elements work.
- k=3 (v appears 4 times): the 1 remaining element is anything non-v; it appears once < 4. Always valid.
- k=4: all five are v. Valid if we can pick 2 v's from each side.

So the real work: for each i, with L-side counts of v (lv) and R-side counts (rv), and total pairs:
Let P_L = C(i,2) total pairs left, P_Lv = C(lv,2) pairs both v, P_L1v = lv*(i-lv) pairs exactly one v, P_L0 = pairs with no v. Similarly right. Also need: pairs of non-v elements that are equal to each other (both sides), and triples... For k=1 case we need: exactly one of 4 picked equals v, and the other 3 are pairwise distinct non-v values.

k=1 subcount: choose which side contributes the v: (a) one v from left pair (pair with exactly one v), right pair has 0 v's; (b) symmetric. Then among the 3 non-v elements (1 from left, 2 from right in case (a)), all distinct values. Count = sum over left pairs with exactly one v of (right pairs with no v and neither element equal to the left non-v value, and the two right elements distinct from each other). This requires per-value data: for left pair (v, x), count right pairs with no v, both elements ≠ x, and the two right elements distinct. = (right pairs with no v, distinct values) − (right pairs with no v, distinct, containing x). "Containing x" = pairs (x, y), y ≠ v, y ≠ x: count = (rx_nonv occurrences of x... occurrences of x in R) * (non-v, non-x count in R) = rx * (nR - rv - rx) where nR = right size. And right pairs no-v distinct = C(nR - rv, 2) − sum_{w≠v} C(rw, 2). Similarly for case (b). So per left pair-with-one-v we need O(1), but there are O(n) such pairs per i, giving O(n²) total — acceptable for n=1000 (10^6). But we can do better: sum over x: Lcount of x among left (lx, x≠v) times lv choices for the v partner... Actually pairs with exactly one v: choose the v (lv ways) and a non-v element x (lx ways). For each such pair, right count depends only on x. So case (a) = lv * Σ_{x≠v} lx * f_R(x), where f_R(x) = rightPairsNoVDistinct − rx*(nR − rv − rx). That's O(distinct values) per i → O(n²) worst case. Fine.

k=2: exactly 2 of 4 picked equal v; other 2 arbitrary non-v (may be equal to each other). Distributions: (2 left, 0 right), (1 left, 1 right), (0 left, 2 right) for the v's. Count = C(lv,2)*C(nR−rv,2) + lv*(i−lv)*rv*(nR−rv) + C(i−lv... wait careful: (1 left v, 1 right v): left pair has exactly one v: lv*(i−lv); right pair exactly one v: rv*(nR−rv). (2 left): C(lv,2) left pairs both v; right pair both non-v: C(nR−rv,2). (0 left): C(i−lv,2) * C(rv,2). Sum.

k=3: exactly 3 v's: (2 left, 1 right): C(lv,2)*rv*(nR−rv); (1 left, 2 right): lv*(i−lv)*C(rv,2).
k=4: C(lv,2)*C(rv,2).

Pitfalls: modulo 1e9+7; large values (use hash map / coordinate compression); distinct-value sums need sum of C(count,2) over values ≠ v per side — maintain running frequency maps as i moves left to right, updating sums incrementally. Need per-side: total count, count of v, sum of C(c,2) over all values, and per-value counts lx, rx for the k=1 sum. The k=1 sum Σ lx * f_R(x) over distinct x is O(distinct) per index → O(n²) total worst case = 10^6, fine. Alternatively maintain a running aggregate, but f_R(x) depends on rx which changes as elements move from right to left, so recomputing per index is simpler.

Edge check k=1: also the single v could be... we covered both sides. Also need the three non-v values pairwise distinct — in case (a) left contributes one non-v x, right contributes two non-v distinct from each other and from x. Yes.

Wait, also k=1 requires exactly one v among 4 picks — covered: left pair exactly-one-v AND right pair zero-v, plus left zero-v AND right exactly-one-v.

## worker: Implement the full solution: coordinate-compress n
- **Approach**: For each index `i` as the middle element (value `v`), we pick 2 elements from the left and 2 from the right. If `k` of the 4 picked elements equal `v`, then `v` appears `1+k` times in the subsequence. Since `v` must be the *unique* mode:
  - `k=0`: impossible (4 other elements each appear ≥1 time, tying or beating `v`).
  - `k=1`: the other 3 picked elements must be pairwise distinct non-`v` values.
  - `k=2`: the other 2 picked elements are arbitrary non-`v` (they may equal each other since 2 < 3).
  - `k=3`: the remaining 1 element is any non-`v`.
  - `k=4`: all picked elements are `v`.
- **Counting**: Maintain left/right frequency arrays plus running `sumC2 = Σ C(count,2)` aggregates (updated in O(1) as elements move from right to left). From these we derive per-side pair counts: both-`v`, exactly-one-`v`, zero-`v`, and zero-`v`-with-distinct-values (`C(nonv,2) − Σ_{x≠v} C(cnt[x],2)`).
- **k=1 case**: For a left pair `(v, x)`, valid right pairs are zero-`v` distinct pairs not containing `x`: `R0v_distinct − rcnt[x]*(nonvR − rcnt[x])`. Summing over all `x` weighted by `lcnt[x]` and multiplying by `lv` choices of the `v` partner gives case A; case B is symmetric. This is O(distinct values) per middle index → O(n·m) ≤ O(n²) ≈ 10⁶ operations, fine for n ≤ 1000.
- **Verification** (done during development against a brute-force `itertools.combinations` checker):
  - `[1,1,1,1,1,1]` → 6 ✓
  - `[1,2,2,3,3,4]` → 4 ✓
  - `[0,1,2,3,4,5,6,7,8]` → 0 ✓
  - Random small arrays (n ≤ 9, values in small ranges including negatives) matched brute force across many trials.
- All arithmetic is taken mod 10⁹+7 at accumulation; intermediate products fit in Python ints anyway.
