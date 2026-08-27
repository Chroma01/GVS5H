
## ideation
**Core Difficulty**: The problem requires calculating the sum of $K$-th powers of all contiguous subarray sums. A naive $O(N^2)$ approach is too slow for $N=2 \times 10^5$. The key is to expand $(\sum A_i)^K$ into a sum of products $A_{i_1} \dots A_{i_K}$ and count how many subarrays contain the chosen indices. This leads to a summation involving $\min(i)$ and $\max(i)$ of the $K$ indices.

**Candidate Approaches**:
1.  **Contribution Technique**: Rewrite the total sum as $\sum_{\text{tuples } (i_1, \dots, i_K)} (\prod A_{i_j}) \cdot \min(i) \cdot (N - \max(i) + 1)$.
    *   Split this into two parts: $T_1 = (N+1) \sum (\prod A_{i_j}) \min(i)$ and $T_2 = \sum (\prod A_{i_j}) \min(i) \max(i)$.
    *   $T_1$ can be computed by iterating over the minimum index $L$ and using prefix sums of $A$. Specifically, sum over tuples where $\min(i)=L$ is $(\sum_{x=L}^N A_x)^K - (\sum_{x=L+1}^N A_x)^K$.
    *   $T_2$ requires summing over pairs $(L, R)$ where $L=\min(i)$ and $R=\max(i)$. The count of such tuples is derived via inclusion-exclusion on the range $[L, R]$: $(\sum_{x=L}^R A_x)^K - (\sum_{x=L+1}^R A_x)^K - (\sum_{x=L}^{R-1} A_x)^K + (\sum_{x=L+1}^{R-1} A_x)^K$.
    *   Directly summing over all pairs $(L, R)$ is $O(N^2)$.
    *   **Optimization**: Use the Binomial Theorem to expand terms like $(P_R - P_{L-1})^K$. Since $K$ is small ($K \le 10$), we can rewrite the sum as a linear combination of terms like $\sum L \cdot P_{L-1}^j$ and $\sum L \cdot P_L^j$, which can be precomputed in $O(N)$ for each power $j \in [0, K]$.

2.  **Complexity**: With the binomial expansion, the complexity becomes $O(N \cdot K)$, which fits well within the time limit ($2 \times 10^5 \times 10 \approx 2 \times 10^6$ operations).

## worker: Read inputs $N, K$ and array $A$.
The solution implements the derived algorithm:
1.  **Mathematical Transformation**: The problem is transformed into calculating $T_1 = (N+1) \sum (\prod A_{i_j}) \min(i)$ and $T_2 = \sum (\prod A_{i_j}) \min(i) \max(i)$. The final answer is $(N+1)T_1 - T_2$.
2.  **Binomial Expansion**: To handle the $O(N^2)$ summation over ranges $[L, R]$, the terms $(P_R - P_{L-1})^K$ are expanded using the Binomial Theorem. This converts the problem into computing prefix sums of the form $\sum i \cdot P_i^j$, which can be precomputed in $O(N \cdot K)$.
3.  **Complexity**: The precomputation of powers and prefix sums takes $O(N \cdot K)$. The final summation loops take $O(N \cdot K)$. With $N=2 \times 10^5$ and $K=10$, the total operations are roughly $4 \times 10^6$, well within the time limit.
4.  **Modulo Arithmetic**: All additions and multiplications are performed modulo 998244353. Negative results from subtractions are handled by adding the modulus.

## worker: Run the code against the provided sample inputs to
The code implements the mathematical derivation:
1.  **Transformation**: The problem is transformed into calculating $T_1 = (N+1) \sum (\prod A_{i_j}) \min(i)$ and $T_2 = \sum (\prod A_{i_j}) \min(i) \max(i)$. The answer is $(N+1)T_1 - T_2$.
2.  **Binomial Expansion**: To avoid $O(N^2)$ summation over ranges, terms like $(P_R - P_{L-1})^K$ are expanded using the Binomial Theorem. This allows us to compute the required sums using precomputed prefix sums of the form $\sum i \cdot P_i^j$.
3.  **Complexity**: The precomputation of powers and prefix sums takes $O(N \cdot K)$. The final summation loops also take $O(N \cdot K)$. With $N=2 \times 10^5$ and $K=10$, the total operations are roughly $4 \times 10^6$, which is efficient.
4.  **Modulo Arithmetic**: All operations are performed modulo 998244353. Negative results from subtractions are handled by adding the modulus.

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the derived $O(N \cdot K)$ algorithm.
1.  **Mathematical Transformation**: The problem is transformed into calculating $T_1 = (N+1) \sum (\prod A_{i_j}) \min(i)$ and $T_2 = \sum (\prod A_{i_j}) \min(i) \max(i)$. The answer is $(N+1)T_1 - T_2$.
2.  **Binomial Expansion**: To avoid $O(N^2)$ summation over ranges, terms like $(P_R - P_{L-1})^K$ are expanded using the Binomial Theorem. This allows us to compute the required sums using precomputed prefix sums of the form $\sum i \cdot P_i^j$.
3.  **Complexity**: The precomputation of powers and prefix sums takes $O(N \cdot K)$. The final summation loops also take $O(N \cdot K)$. With $N=2 \times 10^5$ and $K=10$, the total operations are roughly $4 \times 10^6$, which is efficient.
4.  **Modulo Arithmetic**: All operations are performed modulo 998244353. Negative results from subtractions are handled by adding the modulus.

## worker: finalize
The solution implements the derived $O(N \cdot K)$ algorithm based on the following steps:
1.  **Mathematical Transformation**: The problem is transformed into calculating $T_1 = (N+1) \sum (\prod A_{i_j}) \min(i)$ and $T_2 = \sum (\prod A_{i_j}) \min(i) \max(i)$. The answer is $(N+1)T_1 - T_2$.
2.  **Binomial Expansion**: To avoid $O(N^2)$ summation over ranges, terms like $(P_R - P_{L-1})^K$ are expanded using the Binomial Theorem. This allows us to compute the required sums using precomputed prefix sums of the form $\sum i \cdot P_i^j$.
3.  **Complexity**: The precomputation of powers and prefix sums takes $O(N \cdot K)$. The final summation loops also take $O(N \cdot K)$. With $N=2 \times 10^5$ and $K=10$, the total operations are roughly $4 \times 10^6$, which is efficient.
4.  **Modulo Arithmetic**: All operations are performed modulo 998244353. Negative results from subtractions are handled by adding the modulus.
