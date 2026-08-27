
## ideation
**Core difficulty:** Counting arithmetic progressions of length 3 (fine triplets) in a set of up to 1e6 distinct positive integers (values ≤ 1e6). A direct triple loop is O(N³) and a pair loop checking sums is O(N²) – both are too slow. The required output is a count, not the triplets themselves.

**Mathematical reformulation:** For a triplet (A, B, C) with A < B < C, B - A = C - B ⇔ A + C = 2B. So we can iterate over B in S and count the number of unordered pairs {A, C} ⊂ S \ {B} with A + C = 2B.

**Candidate approaches:**

1. **Sort + two-pointer/binary search:** O(N²) worst case – too slow for N = 1e6.
2. **Hash-set lookups:** For each B, iterate over all A < B in S, check if 2B - A is in S and > B. This is O(N²) in the worst case.
3. **FFT-based convolution (the intended O(M log M) solution):**
   - Build a binary array `f[0..M]` where M = max(S) (≤ 1e6). f[x] = 1 if x ∈ S, else 0.
   - Convolve `g = f * f` using FFT (real-valued via numpy.fft.rfft). `g[k]` = number of ordered pairs (a, b) with a, b ∈ S, a + b = k.
   - For each B in S, the number of ordered pairs (A, C) with A + C = 2B is `g[2B]`. The one pair (B, B) must be removed. The number of unordered pairs (A, C) with A ≠ C is `(g[2B] - 1) // 2`. Since all elements are distinct and B is not equal to A or C, A < C is automatically satisfied.
   - Sum `(g[2B] - 1) // 2` for all B ∈ S.
   - Complexity: O(M log M) with M ≈ 2^21. With numpy this runs in well under 1 second in Python.

**Pitfalls:**
- Integer precision: convolution results must be rounded/cast to nearest integer because FFT is floating-point.
- Array size: need power of 2 ≥ 2M; using M = 2^ceil(log2(2*max(S)+1)) works.
- Edge case: when `g[2B] == 0` (no pair sums to 2B) the answer contributes 0; careful with the `-1` only when g ≥ 1.
- Alternative: NTT (Number Theoretic Transform) would give exact integers but is more code; numpy FFT is acceptable since values fit well in float64 precision (max g[2B] ≤ N).
- Counting only A < C: since all values are distinct, (A, C) and (C, A) are two different ordered pairs, so dividing by 2 is correct after removing the (B, B) self-pair.

## worker: Implement the FFT-based solution in Python: read N
The solution uses the FFT-based convolution trick:
- Represent the set S as a binary indicator array `f` of length `M = 2^ceil(log2(2*max(S)+1))`.
- Compute `g = f * f` via real FFT (`np.fft.rfft` + `np.fft.irfft`). `g[k]` counts ordered pairs (a, b) in S with a + b = k.
- For each B in S, the number of valid unordered pairs {A, C} with A + C = 2B and A ≠ B, C ≠ B is `(g[2B] - 1) // 2` (subtracting the self-pair (B, B), then dividing by 2 to get unordered pairs).
- Summing over all B gives the total number of fine triplets (A, B, C) with A < B < C.
- Complexity: O(M log M) where M ≈ 2^21 for max S ≤ 10^6. Memory: O(M). The code is concise and runs in well under the time limit.
