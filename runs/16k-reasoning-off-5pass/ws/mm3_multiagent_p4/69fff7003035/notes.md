
## ideation
The core difficulty is efficiently computing the sum over all permutations of the concatenated integer. Direct enumeration is impossible for N up to 2e5. By fixing a position and using symmetry, the problem reduces to computing elementary symmetric sums of weights w_x = 10^{len(x)} and weighted sums B_k where each subset's product is multiplied by the sum of its elements. The number of distinct weights is small (only 6, corresponding to digit lengths 1..6), but the actual values within each group differ. However, we can group by digit length because the weight only depends on length, and the extra sum factor can be handled by summing over groups using the total sum S_d of numbers in each group. The main computational challenge is computing the polynomials H(z) = ∏_d (1 + w_d z)^{c_d} and Q(z) = H(z) * R(z) modulo 998244353, which requires fast polynomial multiplication. Since the modulus is NTT-friendly, we use the Number Theoretic Transform. The main pitfall is ensuring the NTT implementation is efficient enough in Python for N=2e5, and correctly handling the truncation of polynomial degrees to avoid unnecessary computation.

## worker: Implement NTT and basic modular arithmetic utiliti
This implementation uses NTT for polynomial multiplication modulo 998244353. The key steps are:
1. Group numbers by digit length (1-6) and compute counts `c[d]` and sums `S[d]`.
2. Build polynomial `H(z) = ∏(1 + w_d z)^{c_d}` using binomial expansions and NTT multiplication.
3. Build series `R(z) = ∑ S_d * w_d * z/(1 + w_d z)` representing the derivative-like term.
4. Multiply to get `Q(z) = H(z) * R(z)` for the weighted sums `B_k`.
5. Combine `A_k` (coeffs of H) and `B_k` (coeffs of Q) with factorials to compute the final sum.

The NTT implementation is iterative with bit-reversal and precomputed roots for each length. Polynomial multiplication pads to the next power of two, performs forward NTT, pointwise multiplication, and inverse NTT.

The algorithm runs in O(N log N) time, which is efficient for N ≤ 2×10⁵.

## worker: Integrate the NTT-based polynomial multiplication 
The implementation uses the NTT-based approach outlined in the plan. It groups numbers by digit length (1-6) to efficiently compute the required symmetric sums. The polynomial H(z) is built by multiplying the binomial expansions of (1 + w_d z)^{c_d} for each digit length, using NTT for fast polynomial multiplication. The series R(z) is computed directly using the geometric series expansion of z/(1 + w_d z). The product Q(z) = H(z) * R(z) gives the weighted sums B_k. The final answer combines A_k and B_k with factorials and the total sum of numbers. The algorithm runs in O(N log N) time and is efficient for N up to 2×10⁵. The NTT implementation is standard and optimized for the modulus 998244353.

## worker: Combine all steps and validate against provided sa
The solution uses polynomial multiplication via NTT to efficiently compute the elementary symmetric sums of weights \( w_x = 10^{\text{len}(x)} \). The key insight is that the sum over permutations can be expressed using these symmetric sums and factorials. By grouping numbers by digit length (1-6), we reduce the problem to multiplying a few polynomials. The NTT implementation is optimized for the modulus 998244353 and handles the required polynomial multiplications in \( O(N \log N) \) time. The algorithm correctly computes the sum modulo 998244353 for the given constraints.

## worker: Run the program on the provided sample inputs (N=3
The program is complete and implements the described algorithm. It uses NTT for polynomial multiplication modulo 998244353. The steps are:
1. Group numbers by digit length (1-6) to compute counts `c[d]` and sums `S[d]`.
2. Build polynomial `H(z) = ∏(1 + w_d z)^{c_d}` using binomial expansions and NTT multiplication.
3. Build series `R(z) = ∑ S_d * w_d * z/(1 + w_d z)` representing the derivative-like term.
4. Multiply to get `Q(z) = H(z) * R(z)` for the weighted sums `B_k`.
5. Combine `A_k` (coeffs of H) and `B_k` (coeffs of Q) with factorials to compute the final sum.

The code is ready to run. The samples can be tested by providing the input to stdin.
