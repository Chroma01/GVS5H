- **Core identity:** For a fixed number x, its contribution over all permutations is x times the sum, over subsets B of the other numbers, of `|B|! * (N-1-|B|)! * 10^{total digit length of B}`. This follows because if exactly B is after x, the elements before x and after x can be permuted independently.
- **Grouping by digit length:** There are at most six digit lengths for N <= 2e5. Let c_d be the count of numbers with d digits, S_d their sum, and w_d = 10^d mod MOD.
- **Generating function:** Define `P(z) = product_d (1 + w_d z)^{c_d}`. The coefficient p_k is the sum of `10^{suffix digit length}` over all subsets of size k.
- **Excluding one number:** For every number of digit length d, the relevant polynomial is `P(z) / (1 + w_d z)`. Its coefficients are obtained by synthetic division: `quotient_0 = 1`, `quotient_k = p_k - w_d * quotient_{k-1}`.
- **Multiplier for a length class:** If q_k are coefficients of `P(z)/(1+w_d z)`, the multiplier for each number of length d is `m_d = sum_{k=0}^{N-1} q_k * k! * (N-1-k)!`. The final answer is `sum_d m_d * S_d`.
- **Efficient coefficient computation:** Directly multiplying N linear factors is too slow. Use the grouped polynomial differential recurrence. Let `Q(z) = product_{d present}(1 + w_d z)` and `R(z) = Q(z) * sum_d c_d w_d/(1+w_d z)`. Then `Q(z) P'(z) = P(z) R(z)`.
- **Recurrence details:** With `q_j` and `r_j` as coefficients of Q and R, and p_0 = 1, for n >= 0:
  `(n+1)p_{n+1} = sum_j r_j p_{n-j} - sum_{j>=1} q_j (n-j+1) p_{n-j+1}`.
  Since N < MOD, all `n+1` are invertible modulo MOD.
- **Implementation:** Compute Q and R explicitly because the number of present digit lengths is tiny. Precompute factorials and modular inverses up to N. After computing p, reuse the inverse array as the factorial weight array `k! * (N-1-k)!`.
- **Complexity:** The recurrence is O(LN) with L <= 6, and the synthetic divisions are also O(LN). Memory is O(N).
- **Edge cases:** N=1 works with empty suffix weight 1. Missing digit lengths are simply omitted from Q and R. All arithmetic is modulo 998244353, and negative intermediate values are normalized with `% MOD`.
- **Current status:** The grouped generating function solution with differential recurrence, synthetic division, and factorial weighting is implemented.
