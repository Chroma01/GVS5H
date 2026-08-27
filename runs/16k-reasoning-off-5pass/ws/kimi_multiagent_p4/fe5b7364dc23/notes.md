
## ideation
Core difficulty: N up to 2e5 makes O(N²) enumeration of subarrays impossible; K ≤ 10 is small, so the key trick is algebraic expansion. Using prefix sums S_0..S_N (S_0 = 0), each subarray sum is S_j − S_i with i < j. Then (S_j − S_i)^K expands binomially into products of powers of S_j and S_i. Maintaining running power sums P_m = Σ_{i<j} S_i^m for m = 0..K lets us process each j in O(K), giving O(N·K) total. Pitfalls: (1) handle signs (−1)^{K−t} carefully mod 998244353; (2) include S_0 = 0 in the initial power sums (P_0 = 1, others 0) so subarrays starting at index 1 are counted; (3) A_i can be 0 and prefix sums must be reduced mod p; (4) binomial coefficients are tiny (K ≤ 10) so precompute directly; (5) note subarray sum mod p then raised to power — since we want (sum)^K mod p, working entirely mod p is valid because the expansion is a polynomial identity over integers, hence valid mod p.

## worker: Implement the full Python solution: read N, K and 
- **Algorithm**: Every subarray sum equals $S_j - S_i$ for prefix sums $S_0=0, S_1, \dots, S_N$ with $i < j$. So the answer is $\sum_{0 \le i < j \le N} (S_j - S_i)^K$.
- **Binomial expansion**: $(S_j - S_i)^K = \sum_{t=0}^{K} \binom{K}{t} S_j^t (-S_i)^{K-t}$. Summing over all previous $i$ gives $\sum_t \binom{K}{t} (-1)^{K-t} S_j^t \cdot P_{K-t}$ where $P_m = \sum_{i<j} S_i^m$.
- **One pass**: For each $j$, compute powers $s^t$ incrementally, evaluate the $O(K)$ contribution, then add $s^m$ into $P[m]$. Total time $O(NK) = O(2 \times 10^5 \cdot 10)$, memory $O(K)$.
- **Correctness checks**:
  - Sample 1: prefix sums 0,3,4,6. Pairs: $(3)^2+(4)^2+(6)^2+(4-3)^2+(6-3)^2+(6-4)^2 = 9+16+36+1+9+4 = 75$. ✓
  - Sample 2: prefix sums 0,0; only pair is $(0-0)^{10} = 0$. ✓
- **Edge cases**: $A_i = 0$ handled naturally; signs handled via parity of $K-t$ with modular subtraction; initialization $P[0]=1$ accounts for $S_0 = 0$ so subarrays starting at index 1 are included; all arithmetic mod 998244353, valid since the expansion is a polynomial identity over the integers.
