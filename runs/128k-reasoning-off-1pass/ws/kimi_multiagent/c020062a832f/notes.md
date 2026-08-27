
## ideation
Core difficulty: M and N are both up to 2e5, so we cannot recompute the inversion number from scratch for each of the M shifts (that would be O(M·N log N)). We need to understand how the inversion count changes as k increments by 1.

Key structural observation: B_i = (A_i + k) mod M. For a pair (i, j) with i < j:
- If A_i == A_j, then B_i == B_j always; never an inversion.
- If A_i ≠ A_j, the comparison between B_i and B_j flips exactly once as k goes from 0 to M-1. Specifically, without wraparound, order is preserved; wraparound happens for the larger of the two values first. The flip occurs at k = M - max(A_i, A_j). At that k, the element with value max wraps to 0 (small), while the other is still large, so the inversion status toggles.

So: answer(k) = answer(k-1) + delta(k), where delta(k) = (number of pairs that flip at exactly this k, weighted by +1 or -1 depending on direction). Actually more carefully: a pair with A_i > A_j (an inversion at k=0) stops being an inversion at k = M - A_i; a pair with A_i < A_j (not an inversion) becomes an inversion at k = M - A_j. So we can compute:
- base = inversion count of A at k=0 (Fenwick tree, O(N log M)).
- For each k, count pairs flipping at k: pairs whose max(A_i, A_j) = M - k. Among those, pairs that were inversions (A_i > A_j, i<j) contribute -1, pairs that were non-inversions (A_i < A_j) contribute +1.

Counting pairs by their max value: for each value v, pairs with max = v are pairs where one element has value v and the other has value < v. Using frequencies freq[v] and prefix sums, total pairs with max = v is freq[v] * (count of elements with value < v). But we also need the split into "earlier element is the larger one" vs "later element is the larger one" — i.e., for each occurrence of value v at position i, count how many previous elements have value < v (those form non-inversion→inversion flips) and how many later elements have value < v (inversion→non-inversion flips). This can be done with a Fenwick tree sweep in O(N log M): process positions left to right; for each A_i = v, query count of previous elements with value < v → contributes +1 flip at k = M - v; and (total elements with value < v) minus (previous with value < v) → contributes -1 flip at k = M - v.

Then answer(k) = answer(k-1) + plus[k] - minus[k], with answer(0) = base.

Pitfalls:
- k ranges 0..M-1; flip point k = M - v ranges from 1 (v = M-1) to M (v = 0). But k only goes up to M-1, and v=0 gives flip at k=M which never happens in range — indeed pairs where max is 0 don't exist (both would be 0, equal). So fine, but size the diff array M+1 to be safe.
- 64-bit integers: inversion count up to ~2e10, must use 64-bit (Python int is fine).
- Verify with sample 3: A = 0..6 sorted, base = 0. Every pair (i<j, A_i<A_j) flips at k = M - A_j. Pairs with max = v: v pairs. So delta(k) = number of pairs with max = M-k = M-k... answer(k) = sum over flip points ≤ k. For k=1: pairs with max=6 → 6 pairs → answer 6. ✓ matches sample.

Alternative approach: derive a formula per k using order statistics, but the flip/delta approach is simpler and O((N+M) log M).

## worker: Implement and verify the flip logic: derive the ex
**Flip logic derivation.** For a pair (i, j), i < j, with A_i ≠ A_j, consider B_i = (A_i + k) mod M, B_j = (A_j + k) mod M. As k increases by 1, both values increase by 1, preserving their order, until the larger one wraps around to 0. The larger value v = max(A_i, A_j) wraps exactly when k = M - v (at that k, v + k = M → 0, while the smaller value u < v gives u + k < M, still positive). At that moment the previously-larger element becomes the smaller one, so the comparison flips, and it flips exactly once for k in [0, M-1] (note k = M - v ≥ 1 since v ≤ M-1, and ≤ M-1 since v ≥ 1; pairs with max v = 0 don't exist as both values would be 0, hence equal).

**Sign of delta.**
- Pair with i < j, A_i > A_j (inversion at k = 0): the larger element is A_i, flip at k = M - A_i; after the flip B_i < B_j, so it stops being an inversion → contributes to `minus[M - A_i]`. Counted by sweeping right-to-left: for each element v, count later elements with value < v.
- Pair with i < j, A_i < A_j (not an inversion at k = 0): the larger element is A_j, flip at k = M - A_j; after the flip B_i > B_j, so it becomes an inversion → contributes to `plus[M - A_j]`. Counted by sweeping left-to-right: for each element v, count earlier elements with value < v.
- Equal pairs never invert and are excluded automatically since we only count strictly-smaller counterparts.

**Algorithm.** One left-to-right Fenwick sweep computes `base` (inversions of A) and `plus[]`; one right-to-left Fenwick sweep computes `minus[]`. Then answer(0) = base, answer(k) = answer(k-1) + plus[k] − minus[k]. Complexity O((N + M) log M), well within limits. Python ints handle the ~2×10¹⁰ counts.

**Sample validation (mental).**
- Sample 1: A = (2,1,0), M=3. base = 3. plus: for v=2, prev_less=0; v=1, prev_less=0 (2 not <1); v=0: 0 → plus all zero except... wait: v=2 at pos1: prev_less=0; v=1 pos2: prev values {2}, less than 1: 0; v=0: 0. So plus = 0. minus (right-to-left): v=0 pos3: 0; v=1 pos2: later less = 1 (the 0) → minus[3-1=2] += 1; v=2 pos1: later less = 2 → minus[1] += 2. Answers: k=0: 3; k=1: 3 − 2 = 1; k=2: 1 − 1 = 0? But expected 1!

Let me recheck. Expected outputs: 3, 1, 1. Hmm — recheck the flip for pair (2,1) at positions (1,2): A_i=2, A_j=1, inversion at k=0. Flip at k = M − max = 3 − 2 = 1. At k=1: B = (0, 2, 1): pair is (0,2), no longer inversion ✓ (−1 at k=1). Pair (2,0) positions (1,3): flip at k = 3−2 = 1: B gives (0,1), not inversion ✓ (−1 at k=1). Pair (1,0) positions (2,3): flip at k = 3−1 = 2: at k=2, B=(1,0,2), pair (0,2) not inversion ✓ (−1 at k=2). So answers: 3, 1, 0? But sample says k=2 gives 1!

Re-examine: at k=2, B = (1, 0, 2). Inversions: (1,0) at positions (1,2) — yes that's an inversion! Which pair is that? Original pair (A_1, A_2) = (2,1). At k=2: B_1 = (2+2) mod 3 = 1, B_2 = (1+2) mod 3 = 0. So B_1 > B_2 — inversion again! My flip analysis was wrong: the flip happens when the larger wraps, but then the *smaller* one also wraps later, flipping back. Pair (2,1): at k=1, larger (2) wraps → (0,2), no inversion. At k=2, smaller (1) wraps → (1,0), inversion again. So each unequal pair flips **twice**: once at k = M − max and once at k = M − min.

Corrected logic: for pair (i<j), values u = min, v = max:
- At k = M − v: order flips (larger wraps).
- At k = M − u: order flips back (smaller wraps).
So for an inversion pair (A_i = v > A_j = u): −1 at k = M − v, +1 at k = M − u. For a non-inversion pair (A_i = u < A_j = v): +1 at k = M − v, −1 at k = M − u.

Implementation fix: for each element with value v at position i:
- earlier elements with value < v (count c1): non-inversion pairs where this is the larger → +1 at k = M − v; also those same pairs flip back at k = M − u for each such u... but counting per-pair at the min's side is easier: for each element v at position i, earlier elements with value > v (count c2): inversion pairs where this element is the smaller (min = v) → those pairs get +1 at k = M − v (flip back). Hmm, cleaner formulation:

For each ordered-by-position pair, handle both endpoints. Equivalent per-element counting with two sweeps:
- Sweep left-to-right. For element v at position i, let L_less = # earlier values < v, L_greater = # earlier values > v.
  - Pairs (earlier u < v, this v): non-inversion, max = v → +1 at k = M − v. (L_less pairs)
  - Pairs (earlier w > v, this v): inversion, min = v → flip-back +1 at k = M − v. (L_greater pairs)
  So plus[M − v] += L_less + L_greater = number of earlier values ≠ v.
- Sweep right-to-left. For element v at position i, let R_less = # later values < v, R_greater = # later values > v.
  - Pairs (this v, later u < v): inversion, max = v → −1 at k = M − v. (R_less)
  - Pairs (this v, later w > v): non-inversion, min = v → flip-back −1 at k = M − v. (R_greater)
  So minus[M − v] += R_less + R_greater = number of later values ≠ v.

Beautiful simplification: plus[M − v] += (i − 1) − (# earlier equal to v), minus[M − v] += (n − i) − (# later equal to v). We can even drop the Fenwick for the deltas and just track equal counts with a frequency array! But Fenwick is already written; simpler to use frequency counts: earlier_not_equal = seen_so_far − freq[v]; then freq[v] += 1. Similarly from the right. That's O(N) for deltas plus O(N log M) for base inversions.

Re-verify sample 1: A=(2,1,0), base=3.
plus (left-to-right): v=2: seen=0 → plus[1]+=0; v=1: seen=1, freq[1]=0 → plus[2]+=1; v=0: seen=2 → plus[3]+=2 (out of range, k=M never used — fine, array size m+1, index m ignored... but wait M−v = 3, k only goes to 2; pairs with min=0 flip back at k=3 which is beyond range — correct, since at k ≤ 2 the smaller element 0 never wraps... 0 wraps at k = M − 0 = 3 = M, i.e., never in [0, M−1] ✓).
minus (right-to-left): v=0: later=0 → minus[3]+=0; v=1: later=1, no equal → minus[2]+=1; v=2: later=2 → minus[1]+=2.
Answers: k=0: 3; k=1: 3 + plus[1](0) − minus[1](2) = 1 ✓; k=2: 1 + plus[2](1) − minus[2](1) = 1 ✓. 

Sample 3 check: A = (0,1,2,3,4,5,6), M=7, base=0. plus[M−v] += seen (no equals): v=0→plus[7]+=0; v=1→plus[6]+=1; v=2→plus[5]+=2; v=3→plus[4]+=3; v=4→plus[3]+=4; v=5→plus[2]+=5; v=6→plus[1]+=6. minus: v=6→minus[1]+=0; v=5→minus[2]+=1; v=4→minus[3]+=2; v=3→minus[4]+=3; v=2→minus[5]+=4; v=1→minus[6]+=5; v=0→minus[7]+=6.
k=0: 0 ✓. k=1: 0+6−0=6 ✓. k=2: 6+5−1=10 ✓. k=3: 10+4−2=12 ✓. k=4: 12+3−3=12 ✓. k=5: 12+2−4=10 ✓. k=6: 10+1−5=6 ✓. All match.

Sample 2 spot check: A=(5,3,5,0,1), M=6. base: pairs: (5,3)✓,(5,5)✗,(5,0)✓,(5,1)✓,(3,5)✗,(3,0)✓,(3,1)✓,(5,0)✓,(5,1)✓,(0,1)✗ → 7 ✓ (matches first output).
plus (left-to-right, seen − freq[v]): v=5: 0 → plus[1]+=0; v=3: 1 → plus[3]+=1; v=5: seen=2, freq[5]=1 → plus[1]+=1; v=0: seen=3 → plus[6]+=3; v=1: seen=4, freq[1]=0 → plus[5]+=4.
minus (right-to-left, later − freq[v]): v=1: 0 → minus[5]+=0; v=0: later=1, freq[0]=0 → minus[6]+=1; v=5: later=2 → minus[1]+=2; v=3: later=3, freq[3]=0 → minus[3]+=3; v=5: later=4, freq[5]=1 → minus[1]+=3.
Answers: k=0: 7 ✓; k=1: 7+1−5=3 ✓; k=2: 3+0−0=3 ✓; k=3: 3+1−3=1 ✓; k=4: 1+0−0=1 ✓; k=5: 1+4−0=5 ✓. All match!

The code above needs to be rewritten to the corrected version (the submitted code block reflects the *first* incorrect derivation — I must output the fixed version). Corrected final code:

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    A = list(map(int, data[2:2 + n]))

    # base inversions via Fenwick
    size = m + 2
    bit = [0] * size
    def add(i, v):
        i += 1
        while i < size:
            bit[i] += v
            i += i & -i
    def sum_(i):
        i += 1
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    base = 0
    for v in A:
        base += sum_(m - 1) - sum_(v)  # earlier values > v
        add(v, 1)

    plus = [0] * (m + 1)
    minus = [0] * (m + 1)

    freq = [0] * m
    seen = 0
    for v in A:
        plus[m - v] += seen - freq[v]   # earlier values != v
        freq[v] += 1
        seen += 1

    freq = [0] * m
    later = 0
    for v in reversed(A):
        minus[m - v] += later - freq[v]  # later values != v
        freq[v] += 1
        later += 1

    out = []
    cur = base
    out.append(str(cur))
    for k in range(1, m):
        cur += plus[k] - minus[k]
        out.append(str(cur))
    sys.stdout.write("\n".join(out) + "\n")

main()
```

Note: index m−v = m occurs when v = 0; arrays sized m+1 accommodate it, and k never reaches m, so it's correctly ignored.

## worker: Replace the solution code with the corrected versi
- Replaced the incorrect single-flip logic with the corrected double-flip derivation: each unequal pair flips at k = M − max (larger wraps to 0) and flips back at k = M − min (smaller wraps). This nets to the simple per-element rule: plus[M−v] += earlier values ≠ v, minus[M−v] += later values ≠ v, which needs only frequency counters (O(N)); the Fenwick tree is used only for the base inversion count (O(N log M)).
- Hand-verified against all three samples: Sample 1 → 3,1,1 ✓; Sample 2 → 7,3,3,1,1,5 ✓; Sample 3 → 0,6,10,12,12,10,6 ✓.
- Edge cases:
  - N=1: base=0, plus/minus all zero → prints 0 on every line. Correct (no pairs).
  - M=1: all A_i = 0, B always all zeros → 0 inversions. Code: base=0; plus/minus indexed at m−v = 1, arrays sized m+1=2, loop over k in range(1,1) is empty → single line 0. Correct.
  - All-equal values: every pair equal → never inversions. base=0; plus/minus get seen−freq[v]=0 and later−freq[v]=0 → all answers 0. Correct.
  - v=0 gives index m−v = m in plus/minus; arrays sized m+1 so no overflow, and k never reaches m (0 wraps only at k=M, outside [0, M−1]). Correct.
- Complexity: O(N log M + N + M) time, O(N + M) memory; Python ints handle counts up to ~2×10¹⁰.
