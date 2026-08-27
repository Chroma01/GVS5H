
## ideation
The core difficulty is handling the exponential number of permutations (N! up to 2e5!) and the concatenation structure. The key insight is to decompose the concatenation as a sum of contributions from each position, then use symmetry and grouping by digit length (only 6 distinct lengths for N ≤ 2e5) to reduce the problem to computing elementary symmetric sums of a multiset of weights w_k = 10^{len(k)}. The sum over permutations can be expressed using subset sums weighted by 10^{sum of lengths}, which are exactly the elementary symmetric polynomials. These can be computed via generating function product using NTT (since there are only a few distinct weights). The final formula involves a recurrence for the sum over subsets excluding one element, which relies on the full subset sums F(m). Pitfalls: correctly handling the recurrence G_l(m) = F(m) - w_l * G_l(m-1), ensuring modular inverses of binomial coefficients are computed, and truncating polynomials to degree N to keep NTT efficient.

## worker: Implement NTT for polynomial multiplication modulo
The solution computes the sum over all permutations of the concatenated number by decomposing the contribution of each digit length group. The key steps are:

1. **Grouping by length**: Since N ≤ 2e5, numbers have at most 6 digits. We group numbers by their decimal length l, with count cnt[l] and weight w[l] = 10^l.

2. **Elementary symmetric sums**: Define F(m) as the sum of 10^{sum of lengths} over all subsets of size m from {1..N}. This is the coefficient of x^m in ∏_l (1 + w[l] x)^{cnt[l]}. We compute this polynomial product using NTT (Number Theoretic Transform) modulo 998244353, which is NTT-friendly.

3. **Recurrence for subsets excluding one element**: For a fixed number of length l, the sum over subsets of the remaining numbers of size m, denoted G_l(m), satisfies G_l(0)=1 and G_l(m) = F(m) - w[l] * G_l(m-1).

4. **Final formula**: The total sum is (N-1)! * Σ_l S_w[l] * Σ_{m=0}^{N-1} G_l(m) / C(N-1, m), where S_w[l] is the sum of all numbers of length l, and 1/C(N-1, m) is the modular inverse of the binomial coefficient.

5. **NTT implementation**: The NTT is implemented iteratively with bit-reversal permutation. The convolution function multiplies two polynomials, and we truncate results to degree N to keep the size manageable.

The algorithm runs in O(6 * N log N) time for the NTT multiplications and O(N) for the rest, which is efficient for N up to 2e5.
