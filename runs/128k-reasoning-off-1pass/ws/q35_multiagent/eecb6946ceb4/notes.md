
## ideation
The core difficulty is efficiently counting arithmetic progressions of length 3 within a set of integers where $N$ and the maximum value $M$ are both up to $10^6$. A naive $O(N^2)$ approach checking all pairs for each middle element will time out. The constraints allow for an approach based on the value range $M$ rather than just the count $N$.

Key observations:
1. A "fine triplet" $(A, B, C)$ satisfies $A+C = 2B$, meaning they form an arithmetic progression with common difference $d = B-A = C-B$.
2. We can iterate over the common difference $d$. For a fixed $d$, we need to count how many $B$ exist such that $B-d \in S$, $B \in S$, and $B+d \in S$.
3. The maximum value in $S$ is $M = 10^6$. The maximum possible difference $d$ is $M/2$.
4. For a fixed $d$, the number of valid $B$ values is at most $M$. However, summing over all $d$ from $1$ to $M/2$, the total number of checks is $\sum_{d=1}^{M/2} (M - 2d) \approx \frac{M^2}{4}$, which is too slow ($10^{12}$ operations).
5. Wait, the plan suggested $O(M \log M)$ by iterating $B$ for each $d$. Let's re-evaluate. The number of triplets is small? No.
6. Actually, a better approach is to iterate over the middle element $B$. For each $B$, we want to count pairs $(A, C)$ such that $A = B-d$ and $C = B+d$ are both in $S$. This is equivalent to counting $d > 0$ such that $B-d \in S$ and $B+d \in S$.
7. If we iterate $B$ and then iterate $d$, it's still potentially slow if many $B$ have many neighbors.
8. However, notice that we can iterate over the difference $d$. For a fixed $d$, we check all $B$ such that $B-d \ge 1$ and $B+d \le M$. The number of such $B$ is $M - 2d$. The total complexity is $\sum_{d=1}^{M/2} (M - 2d) \approx M^2/4$. With $M=10^6$, $M^2/4 = 2.5 \times 10^{11}$, which is too slow for Python (and likely C++ within 2 seconds).
9. We need a faster method. Let's reconsider the constraints. $N \le 10^6$ and $S_i \le 10^6$.
10. Alternative: Use Fast Fourier Transform (FFT).
    - Let $P$ be a polynomial where the coefficient of $x^i$ is 1 if $i \in S$, else 0.
    - We want to find the number of triplets $(A, B, C)$ such that $A+C = 2B$.
    - Consider the polynomial $Q(x) = P(x) \cdot P(x)$. The coefficient of $x^k$ in $Q(x)$ is the number of pairs $(A, C)$ such that $A+C = k$.
    - We are interested in $k = 2B$. So for each $B \in S$, we look at the coefficient of $x^{2B}$ in $Q(x)$.
    - The total count is $\sum_{B \in S} [x^{2B}] Q(x)$.
    - However, this counts pairs $(A, C)$ including cases where $A=C$ or $A, C$ not distinct from $B$ in the required way? The problem states distinct integers $A < B < C$.
    - The FFT approach counts all pairs $(A, C)$ summing to $2B$. We must subtract cases where $A=B$ (implies $C=B$, so $A=B=C$, not allowed as distinct) or $C=B$ (same). Also need to ensure $A \neq C$.
    - Actually, since $A, B, C$ are distinct elements from $S$, and $A < B < C$, we have $A \neq C$.
    - The condition $A+C=2B$ with $A, C \in S$ and $B \in S$ is necessary.
    - The FFT gives us the count of pairs $(A, C)$ for each sum.
    - Complexity: $O(M \log M)$ with $M=10^6$. This is feasible.
    - Steps:
        1. Create array `arr` of size $2^{19} \approx 524288$ (next power of 2 greater than $2 \times 10^6$).
        2. Set `arr[i] = 1` if $i \in S$.
        3. Compute FFT of `arr`.
        4. Square the FFT coefficients.
        5. Compute inverse FFT.
        6. The real part of the coefficient at index $2B$ gives the number of pairs $(A, C)$ such that $A+C=2B$.
        7. Sum these values for all $B \in S$.
        8. Subtract invalid cases:
           - The pair $(B, B)$ contributes to the sum for $2B$. Since $A=B$ and $C=B$, this is not a valid triplet ($A<B<C$ fails). We must subtract 1 for each $B \in S$ because the pair $(B, B)$ is counted in the convolution.
           - Are there other invalid cases? What if $A=C$? If $A=C$, then $2A=2B \implies A=B$. So $A=C=B$. This is the same case.
           - So for each $B$, the convolution count includes the pair $(B, B)$. We subtract 1.
           - Does it include $(A, C)$ and $(C, A)$? Yes, convolution counts ordered pairs. Since $A < C$ is required for $A < B < C$, and the triplet is unordered in the set but ordered in value, we need to be careful.
           - The problem asks for triplets $(A, B, C)$ with $A < B < C$.
           - For a fixed $B$, the valid pairs are $(A, C)$ with $A < B < C$.
           - The convolution counts all $(A, C)$ such that $A+C=2B$.
           - If $A < B < C$, then $A \neq C$.
           - The pair $(A, C)$ and $(C, A)$ are both counted.
           - We only want the case where $A < B$ (which implies $C > B$).
           - So for each $B$, we take the total count from convolution, subtract the case $(B, B)$, and divide by 2.
           - Result: $\sum_{B \in S} \frac{(\text{conv}[2B] - 1)}{2}$.

11. Implementation detail: Python's `cmath` or `numpy`? Standard library doesn't have FFT. We might need to implement it or use `numpy` if allowed. The prompt doesn't restrict libraries, but typically competitive programming environments might not have numpy. However, for $10^6$, a pure Python FFT might be slow.
12. Let's check if $O(N \sqrt{M})$ or similar is possible.
13. Another approach: Iterate over $B$. For each $B$, iterate $d$ such that $B-d \ge 1$ and $B+d \le M$. Check if $B-d \in S$ and $B+d \in S$.
    - This is $O(N \cdot M)$ worst case.
    - But we can optimize: Only iterate $d$ where $B-d$ is in $S$.
    - For each $B$, let $L$ be the list of elements in $S$ less than $B$. For each $A \in L$, check if $2B-A \in S$.
    - This is $O(N^2)$ worst case.
14. Given $M=10^6$, FFT is the standard solution for "count arithmetic progressions".
15. I will implement a simple FFT in Python. To speed it up, I'll use iterative Cooley-Tukey.

Pitfalls:
- Floating point precision issues with FFT for large $N$. Using `complex` types in Python might lose precision for counts up to $10^6$. However, the maximum count for a specific sum is $N$, so precision should be fine if we round to nearest integer.
- Size of FFT: Need size $> 2 \times 10^6$. Next power of 2 is $2^{21} = 2097152$.
- Time limit: Python FFT might be slow for $2^{21}$. $2^{21} \log(2^{21}) \approx 2 \times 10^6 \times 21 \approx 4.2 \times 10^7$ operations. In Python, this might TLE.
- Is there a non-FFT approach?
- Let's reconsider the $O(M \log M)$ iteration over $d$.
    - For $d$ from 1 to $M/2$:
        - Count $B$ such that $B-d, B, B+d \in S$.
        - This is equivalent to counting intersections of $S$ with shifted versions.
        - We can use bitsets? Python integers act as bitsets.
        - Create a bitmask `mask` where the $i$-th bit is 1 if $i \in S$.
        - For each $d$, compute `count = (mask & (mask << d) & (mask >> d)).bit_count()`.
        - Wait, `mask << d` shifts bits to higher positions. `mask >> d` shifts to lower.
        - We want $B-d, B, B+d$ all present.
        - Let `mask` represent the set $S$.
        - `mask & (mask << d)` gives bits at position $B$ where $B-d \in S$ and $B \in S$? No.
        - If bit $i$ is set in `mask`, it means $i \in S$.
        - `mask << d` has bit $i+d$ set if $i \in S$. So bit $j$ is set if $j-d \in S$.
        - `mask >> d` has bit $i-d$ set if $i \in S$. So bit $j$ is set if $j+d \in S$.
        - We want $B$ such that $B-d \in S$, $B \in S$, $B+d \in S$.
        - This corresponds to bit $B$ being set in `mask`, bit $B$ being set in `mask << d` (which means $B-d \in S$), and bit $B$ being set in `mask >> d` (which means $B+d \in S$).
        - So, `common = mask & (mask << d) & (mask >> d)`.
        - The number of set bits in `common` is the number of valid $B$'s for difference $d$.
        - Sum these counts for all $d$.
        - Complexity: $M$ iterations. Each iteration involves bitwise operations on integers of $10^6$ bits.
        - Bitwise AND of $10^6$ bits is fast? In Python, large integer operations are $O(N/word\_size)$. $10^6$ bits is $\approx 125$ KB.
        - Doing this $500,000$ times might be slow. $5 \times 10^5 \times 125$ KB operations?
        - Actually, Python's large int bitwise ops are optimized. But $5 \times 10^5$ ops on 125KB chunks is $6 \times 10^{10}$ bit operations. This is likely too slow.
        - However, we can skip $d$ where the count is likely 0? No.
        - But note: if $S$ is sparse, we can iterate over elements.
        - If $S$ is dense, bitset is good.
        - Given $N, M \le 10^6$, bitset approach is risky in Python.

Let's stick to FFT but optimize or check if bitset is viable.
Actually, for $N=10^6$, the bitset approach in C++ is standard. In Python, it might TLE.
Let's try the FFT approach. It's $O(M \log M)$ with a small constant if implemented well.

Wait, I can use `numpy` if available? The prompt says "solve the problem", usually implying standard library. I should avoid numpy.

Let's refine the FFT plan.
Size $N_{fft} = 2^{21}$.
Implement iterative FFT.

## worker: Implement a fast iterative FFT in Python.
1. **Problem Analysis**: The problem asks for the number of arithmetic progressions of length 3 $(A, B, C)$ from a given set $S$. This is equivalent to finding triplets such that $A+C = 2B$.
2. **Algorithm Selection**: 
   - A naive $O(N^2)$ approach is too slow for $N=10^6$.
   - An approach iterating over differences $d$ using bitsets is $O(M^2/word\_size)$ which is risky in Python.
   - **FFT (Fast Fourier Transform)** is the optimal choice. We construct a polynomial $P(x)$ where the coefficient of $x^i$ is 1 if $i \in S$. The convolution $P(x) \cdot P(x)$ gives coefficients representing the number of pairs $(A, C)$ summing to each index.
   - Specifically, the coefficient of $x^{2B}$ in $P(x)^2$ is the number of pairs $(A, C)$ such that $A+C=2B$.
3. **Implementation Details**:
   - **FFT Size**: Determined by the maximum value in $S$ ($M \le 10^6$). We need size $> 2M$. Next power of 2 is $2^{21} = 2097152$.
   - **Iterative FFT**: Implemented to avoid recursion depth issues and overhead. Includes bit-reversal permutation and Cooley-Tukey butterfly operations.
   - **Inverse FFT**: Obtained by conjugating inputs, running forward FFT, conjugating outputs, and dividing by $N$.
   - **Counting**: For each $B \in S$, we look at the coefficient at index $2B$. This count includes the pair $(B, B)$. We subtract 1 for this self-pair. The remaining count represents ordered pairs $(A, C)$ with $A \neq C$. Since $A+C=2B$, $A < B \iff C > B$. Exactly half of these pairs have $A < B$. So we divide by 2.
4. **Complexity**: $O(M \log M)$ where $M = \max(S)$. With $M=10^6$, this is roughly $2 \cdot 10^7$ operations, which fits within time limits for Python if implemented efficiently.
5. **Precision**: Floating point errors are handled by rounding to the nearest integer. Given the counts are integers and not excessively large (max $N$), standard double precision is sufficient.
