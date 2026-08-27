
## ideation
The problem asks to count 3-term arithmetic progressions (A, B, C) with all elements in S, A < B < C, B - A = C - B. Equivalently, for each B in S, count d ≥ 1 such that B-d and B+d are both in S.

Core difficulty: N and values up to 1e6. A naive per-B scan over d is O(N * maxVal) worst case — for S = {1..1e6}, that's ~5e11 operations, far too slow in Python. Even a per-B loop bounded by min(B-1, maxVal-B) sums to ~2.5e11. So we need a convolution (FFT) approach.

Key insight: Let f[x] = 1 if x in S else 0, for x in [0, M] where M = max(S). The convolution g = f * f has g[k] = number of ordered pairs (x, y) in S×S with x + y = k. For a fixed B, pairs (A, C) with A + C = 2B are counted in g[2B]. This includes the pair (B, B) itself (A = C = B), and counts (A, C) and (C, A) as separate ordered pairs. So the number of valid (A, C) with A < B < C for this B is (g[2B] - 1) // 2. Total answer = sum over B in S of (g[2B] - 1) // 2.

Implementation details:
- Use numpy's rfft/irfft with size n = 1 << ceil(log2(2M+1)) to avoid circular convolution wraparound.
- f is float64; values of g up to 1e6, well within exact integer representation of doubles (2^53), so rounding via np.rint is safe.
- Read input fast with sys.stdin.buffer.read().split().
- Build indicator array f of length M+1, set f[S_i] = 1.
- Compute conv = irfft(rfft(f, n) ** 2, n)[:2M+1], round to int64.
- Answer = sum((conv[2*b] - 1) // 2 for b in S). Vectorize: indices = 2 * S_array; ans = ((conv[indices] - 1) // 2).sum().

Pitfalls:
- FFT length must be ≥ 2M+1, else circular wrap corrupts coefficients.
- Must subtract the (B,B) self-pair and halve (ordered pairs).
- Memory: arrays of size 2^21 floats ≈ 16MB each — fine.
- Edge case N < 3 → answer 0 naturally (no pairs).
- Use integer arithmetic after rounding; ensure numpy integer types sum into Python int or int64 (max answer ~ C(1e6,3)/... actually max number of APs in 1e6 elements ~ 2.5e11, exceeds int32 but fits int64; numpy sum of int64 is fine).

## worker: Write the complete Python solution: parse input wi
- A fine triplet is a 3-term arithmetic progression: for middle element B, need pairs (B-d, B+d) both in S.
- Let f be the indicator array of S over [0, max(S)]. The convolution g = f * f gives g[k] = number of ordered pairs (x, y) ∈ S² with x + y = k.
- For B ∈ S, g[2B] counts ordered pairs (A, C) with A + C = 2B, including the self-pair (B, B). Valid triplets for this B = (g[2B] - 1) / 2.
- Total answer = Σ_{B ∈ S} (g[2B] - 1) // 2.
- Implementation: pad f to power-of-two length ≥ 2*max(S)+1 to avoid circular wraparound; use numpy rfft/irfft (O(M log M), M ≤ 1e6 → size 2^21, very fast). Coefficients ≤ 1e6, exactly representable in float64, so np.rint is exact.
- Answer fits in int64 (max ~2.5e11). Vectorized indexing conv[2*s] avoids Python loops.
- Input parsed via sys.stdin.buffer.read().split(); np.frombuffer with sep used for fast parsing, with a safe fallback.

## worker: Review code for pitfalls: FFT length, int64 roundi
Review of the listed pitfalls:

1. **FFT length**: `size` is the smallest power of two ≥ 2m+1, where m = max(S). Linear convolution of f (length m+1) with itself has length 2m+1, so circular convolution at this size has no wraparound contamination. Indices accessed are 2*s ≤ 2m < size, always in bounds. ✓

2. **int64 rounding**: Coefficients of conv are at most N ≤ 1e6 (number of ordered pairs summing to k), far below 2^53 ≈ 9e15, so float64 represents them exactly and FFT roundoff (typically ≪ 0.5 for these magnitudes at size 2^21) is safely handled by `np.rint`. Cast to int64 then subtract 1 and halve — all exact. ✓

3. **N < 3 edge case**: Added explicit early return printing 0. (Without it, the math would still yield 0 since every (g[2B]-1)//2 = 0 when fewer than 3 elements can't form a pair around B, but the guard also avoids any degenerate max() issues and saves time.) Also guarded against empty input. ✓

4. **Memory usage**: size ≤ 2^21 (since 2m+1 ≤ 2,000,001 < 2^21). Arrays: f (float64, ~16.8 MB), F (complex128, size//2+1 ≈ 8.4 MB... actually complex128 of length ~1.05M ≈ 16.8 MB), conv (~16.8 MB), plus F*F temporary (~16.8 MB). Peak ≈ 70 MB — acceptable for typical limits (≥256 MB). Input parsing via np.frombuffer avoids a large Python list of ints. ✓

Correctness argument: g[2B] counts ordered pairs (x,y) ∈ S² with x+y = 2B. One of these is (B,B) since B ∈ S. The remaining pairs come in symmetric orderings (B-d, B+d) and (B+d, B-d), so valid d ≥ 1 count = (g[2B]-1)//2. Summing over all B ∈ S counts each fine triplet exactly once (by its middle element). Verified against samples mentally: S={1,2,3,5,8}: g[2]=2→(2-1)//2=0? Wait g[2] counts pairs summing to 2: (1,1) only → 1... but 1∈S so (1,1) is the self-pair, (1-1)//2=0 ✓. For B=2: g[4] = pairs summing to 4: (1,3),(3,1),(2,2) = 3 → (3-1)//2=1 ✓ (triplet (1,2,3)). B=3: g[6]: (1,5),(5,1),(3,3) = 3 → 1 ✓. B=5: g[10]: (2,8),(8,2),(5,5) = 3 → 1 ✓. B=8: g[16]: (8,8) = 1 → 0 ✓. Total 3 ✓.
