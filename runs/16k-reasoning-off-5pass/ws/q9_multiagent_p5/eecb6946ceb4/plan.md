The problem requires counting triplets (A, B, C) from a set S such that they form an arithmetic progression (B-A = C-B). Since the order in the triplet is fixed (A < B < C) and the set elements are distinct, we can sort the array S first. After sorting, for every pair of elements (A, C), the middle element B is uniquely determined as (A+C)/2. If (A+C) is even and the resulting B exists in the set, we count it. To efficiently check existence and count, we can use a frequency array (since values are up to 10^6) or a hash set. Given the constraints (N up to 10^6, values up 10^6), an O(N) or O(N log N) approach is required. We will sort the array, then iterate through possible pairs or use a frequency map to count valid middle elements. A more efficient approach for dense small ranges is to use a boolean array for existence and iterate through all pairs, but that's O(N^2). Instead, we can iterate through each element B as the middle term, then count how many pairs (A, C) exist such that A = B - d and C = B + d. We can precompute the frequency of each number. Then for each B, iterate over possible differences d. However, iterating d for every B is still potentially slow if the range is large. A better approach: Sort S. For each element B (as the middle), we want to count pairs (A, C) such that A+B = B+C => A+C = 2B. This is equivalent to finding pairs summing to 2B. We can iterate through the sorted array and for each B, use two pointers or a hash map to find pairs. Actually, the most efficient standard solution for this specific constraint (values up to 10^6) is to use a frequency array `cnt`. Iterate through each number `x` in S. If `x` can be a middle element, we need to sum `cnt[x-d] * cnt[x+d]` for all `d > 0`. But iterating `d` is slow. 
Wait, the constraints say $S_i \le 10^6$. Let $M = 10^6$. We can iterate over all possible middle values $B$ present in $S$. For a fixed $B$, we need to count pairs $(A, C)$ such that $A+B = B+C \implies A+C = 2B$. This is a standard "count pairs with sum K" problem. Since we need to do this for every $B$, doing it naively is $O(N^2)$. 
Alternative approach: Iterate over all pairs $(A, C)$? No, $O(N^2)$.
Let's reconsider the constraints. $N, S_i \le 10^6$.
Actually, we can iterate over the difference $d$. For a fixed $d$, we count how many $B$ exist such that $B-d$ and $B+d$ are in $S$. This is equivalent to counting $B$ where $B-d \in S$ and $B+d \in S$. We can iterate $d$ from 1 to $M/2$. For each $d$, we iterate through all $B$ such that $B-d \ge 1$. Check if both exist. This is $O(M^2)$ worst case, too slow.

Correct efficient approach:
1. Sort $S$.
2. Iterate through each element $B$ in $S$ considering it as the middle element.
3. We need to count pairs $(A, C)$ in $S$ such that $A < B < C$ and $A+C = 2B$.
4. This can be solved by iterating $A$ from the start of the array up to $B$, and checking if $2B - A$ exists in $S$ and is $> B$.
5. To make this fast, we can use two pointers for each $B$? No, that's still slow if done naively.
6. Better: Use a frequency array `freq` of size $10^6+1$.
7. Iterate $d$ from 1 to $M/2$. For each $d$, the number of triplets with difference $d$ is the number of $B$ such that $B-d \in S$ and $B+d \in S$.
   We can compute this by iterating $B$ from $d+1$ to $M-d$. If `freq[B-d]` and `freq[B+d]` are both 1, increment count.
   Total complexity: $\sum_{d=1}^{M/2} (M-d) \approx O(M^2)$. With $M=10^6$, this is $10^{12}$, too slow.

Wait, $N$ is up to $10^6$. The values are also up to $10^6$.
Is there an $O(N)$ or $O(N \log N)$ way?
Yes. Sort $S$.
Iterate $i$ from $0$ to $N-1$ (let $B = S[i]$).
We want to count $j < i$ and $k > i$ such that $S[j] + S[k] = 2 S[i]$.
This is equivalent to: for a fixed sum $K = 2 S[i]$, count pairs $(x, y)$ with $x < S[i] < y$ and $x+y=K$.
Since the array is sorted, for a fixed $i$, we can use two pointers on the subarray $S[0 \dots i-1]$ and $S[i+1 \dots N-1]$? No, the sums are not monotonic in a simple way for two pointers across the whole array easily without care.
Actually, we can iterate $i$ (middle). Then we have a target sum $T = 2*S[i]$. We need to count pairs in the rest of the array summing to $T$.
Since we process each $i$, and the total number of pairs is $O(N^2)$, we need a faster way.
However, note that the values are small ($10^6$).
Let's go back to the frequency array idea but optimize the loop.
We want $\sum_{B \in S} \sum_{d > 0} [B-d \in S] \cdot [B+d \in S]$.
This looks like a convolution. If we have a binary array $A$ where $A[x]=1$ if $x \in S$, we want to compute the convolution of $A$ with itself, specifically the coefficient of $2B$ in $A * A$, but restricted to $A[B-d]$ and $A[B+d]$.
Actually, the term is $\sum_{d} A[B-d] A[B+d]$. This is exactly the coefficient of $x^{2B}$ in the polynomial $P(x) = \sum A[k] x^k$ multiplied by $P(x)$? No.
Let $P(x) = \sum_{k} A[k] x^k$. Then $P(x)^2 = \sum_{k} (\sum_{j} A[j] A[k-j]) x^k$.
The term we want is $\sum_{d} A[B-d] A[B+d]$. Let $j = B-d, k = B+d$. Then $j+k = 2B$.
So we are looking for the number of pairs $(j, k)$ such that $j+k = 2B$ and $j, k \in S$.
This is exactly the coefficient of $x^{2B}$ in the polynomial square $P(x)^2$, but we must ensure $j < B < k$. Since $A$ is binary (distinct elements), if $j+k=2B$ and $j \neq k$, then one is smaller and one is larger. If $j=k=B$, then $2B=2B$, but we need distinct $A, B, C$, so $j \neq k$.
So the answer is $\sum_{B \in S} (\text{coefficient of } x^{2B} \text{ in } P(x)^2 - A[B])$.
Wait, if $j=k=B$, the term is $A[B]^2 = 1$. We need to subtract this case because $A, B, C$ must be distinct.
So, Algorithm:
1. Create a polynomial (or just an array representing coefficients) $P$ of size $2 \cdot 10^6 + 1$, where $P[x] = 1$ if $x \in S$, else 0.
2. Compute the convolution $Q = P * P$. $Q[s]$ stores the number of pairs $(j, k)$ such that $j+k=s$.
3. The answer is $\sum_{B \in S} (Q[2B] - 1)$. The "-1" removes the case where $j=k=B$.
4. How to compute convolution efficiently? $N, M \le 10^6$. FFT is $O(M \log M)$. $M=10^6$, so $10^6 \log 10^6 \approx 2 \cdot 10^7$ operations, which is feasible in Python if implemented carefully or using `numpy` (but standard library only).
   Implementing FFT in pure Python might be slow due to overhead.
   Is there a simpler $O(N \log N)$ or $O(N)$ approach without FFT?
   
   Let's re-evaluate the constraints and typical CP solutions.
   Usually, for $N=10^6$ and values up to $10^6$, if FFT is intended, the time limit is generous or it's C++. In Python, FFT is risky.
   Is there a counting sort / bucket approach?
   Maybe the number of triplets is small? No, could be $O(N^2)$.
   
   Wait, is it possible to iterate over $d$?
   If we iterate $d$, we check $B-d$ and $B+d$.
   The total number of pairs $(A, C)$ with $A < C$ is $N(N-1)/2$.
   If we iterate over all pairs $(A, C)$, calculate $B = (A+C)/2$, and check if $B \in S$, that is $O(N^2)$.
   
   Let's look at the constraints again. $S_i \le 10^6$.
   Maybe the intended solution is indeed FFT, or there's a trick.
   Actually, many similar problems on AtCoder (this looks like ABC 179 E or similar difficulty) allow $O(N \sqrt{M})$ or similar? No.
   
   Let's reconsider the "iterate $d$" approach.
   If the values are dense, $d$ is small. If sparse, $d$ is large.
   But we don't know the distribution.
   
   Wait, there is a known technique for this specific problem "count arithmetic progressions of length 3".
   If $N$ is large and range is large, FFT is the way.
   If $N$ is large and range is small, we can use FFT.
   Here range is $10^6$, $N$ is $10^6$. FFT is the standard solution.
   Can we implement FFT in Python within time limits?
   Pure Python FFT for size $10^6$ might TLE (Time Limit Exceeded) because of interpreter overhead.
   However, maybe the test cases are weak or $N$ is smaller in practice? No, we must assume worst case.
   
   Is there an $O(N)$ solution?
   What if we iterate $B$ and use a hash set?
   For each $B$, we want to count pairs $(A, C)$ with $A+C=2B$.
   This is equivalent to: for each $B$, iterate $A < B$ and check if $2B-A \in S$.
   This is $O(N^2)$ in worst case (e.g., $S = \{1, 2, ..., N\}$).
   
   Let's check if there is a constraint I missed. "distinct positive integers".
   Maybe the number of arithmetic progressions is small? No.
   
   Okay, let's assume the intended solution is FFT. I will write a standard FFT implementation.
   Wait, is there a simpler way?
   What if we iterate over the difference $d$?
   The number of triplets with difference $d$ is the number of $B$ such that $B-d \in S$ and $B+d \in S$.
   We can compute this by:
   1. Mark presence of each number in a boolean array `present`.
   2. For each $d$ from 1 to $M/2$:
      Iterate $B$ from $d+1$ to $M-d$.
      If `present[B-d]` and `present[B+d]`, count++.
   This is $O(M^2)$. Too slow.
   
   Wait, we can optimize the $d$ loop.
   Instead of iterating $B$, we can iterate over pairs in $S$? No.
   
   Let's go back to the polynomial multiplication.
   $P(x) = \sum x^{S_i}$.
   $Q(x) = P(x)^2 = \sum c_k x^k$.
   $c_{2B}$ is the number of pairs $(A, C)$ such that $A+C = 2B$.
   Since elements are distinct, if $A \neq C$, then one is smaller, one is larger.
   If $A=C=B$, then $2B=2B$.
   So for a fixed $B$, the number of valid triplets with middle $B$ is $c_{2B} - 1$ (removing $B+B$).
   We sum this over all $B \in S$.
   Total answer = $\sum_{B \in S} (c_{2B} - 1)$.
   This is correct.
   Now, how to compute $c_k$ for all $k$? FFT.
   Size of polynomial: $2 \cdot 10^6$.
   FFT size needs to be power of 2, next power of 2 after $2 \cdot 10^6$ is $2^{21} = 2097152$.
   Complexity: $O(M \log M)$.
   In Python, a naive recursive FFT is too slow. Iterative FFT with precomputed roots of unity is better.
   Using `cmath` for complex numbers.
   Given the strict time limit usually associated with $10^6$ in Python, this is borderline.
   However, there is no other obvious $O(N \log N)$ or $O(N)$ algorithm for general inputs.
   Perhaps the problem setters expect FFT.
   
   Wait, is there a constraint on the number of triplets? No.
   Is it possible to use the fact that $S_i$ are distinct?
   
   Let's try to code the iterative FFT.
   Steps:
   1. Read input, create array `a` of size $2^{21}$ initialized to 0.
   2. Set `a[S[i]] = 1`.
   3. Perform FFT on `a`.
   4. Square the magnitude (point-wise multiplication of FFT result with itself).
   5. Perform Inverse FFT.
   6. Extract real parts, round to nearest integer.
   7. Sum `(result[2*B] - 1)` for all $B \in S$.
   
   Optimization: Since inputs are integers, we can use Number Theoretic Transform (NTT) to avoid floating point errors and complex numbers, using a large prime modulus. But we need the exact count, and the count can be up to $N^2 \approx 10^{12}$, which fits in 64-bit integer. NTT requires a prime $P > N^2$. Common primes: $998244353$ is too small ($< 10^{12}$). We need a prime around $10^{12}$ or use multiple moduli (CRT).
   Using floating point FFT (complex numbers) is easier to implement and usually sufficient if precision is handled (double precision has 53 bits significand, $10^{12}$ fits easily).
   
   Let's refine the FFT implementation for Python.
   - Use iterative Cooley-Tukey.
   - Precompute bit reversal.
   - Precompute roots of unity.
   
   Wait, is there a simpler logic?
   What if we iterate $B$ and use a hash set?
   If the test cases are random, average case is good. But worst case $S = \{1, 2, ..., N\}$ gives $O(N^2)$ checks.
   So we must use FFT.
   
   Let's double check if there's an $O(N)$ solution.
   If we sort $S$, can we do something?
   For each $B$, we want $A+C=2B$.
   This is equivalent to finding pairs with sum $2B$.
   If we iterate $B$, and use two pointers on the sorted array to find pairs summing to $2B$?
   For a fixed $B$, we have target $T=2B$.
   We need pairs $(A, C)$ from $S \setminus \{B\}$ such that $A+C=T$.
   Since $S$ is sorted, we can use two pointers $L, R$ on the whole array $S$.
   But we need to do this for every $B$. That's $N$ times two pointers $\to O(N^2)$.
   
   Okay, FFT it is.
   
   Implementation details:
   - Size $N_{fft} = 2^{21}$.
   - Input array size $M = 10^6$.
   - Read $S$, fill array.
   - FFT -> Square -> IFFT.
   - Sum up.
   
   One catch: Python's `complex` numbers might be slow.
   Is there a way to avoid full FFT?
   Maybe the constraints allow $O(N \sqrt{M})$?
   $N=10^6, M=10^6$. $\sqrt{M}=1000$. $10^9$ ops is too slow.
   
   Wait, I might be overthinking. Is it possible the problem is from a contest where $N$ is smaller?
   The problem statement says $N \le 10^6$.
   Okay, I will implement the FFT solution. It's the only mathematically sound approach for the constraints.
   
   Wait, one more check. Is it possible to use the fact that we only care about $2B$?
   We need $c_{2B}$.
   $c_k = \sum_{j} a_j a_{k-j}$.
   We need $\sum_{B} c_{2B}$.
   This is $\sum_{B} \sum_{j} a_j a_{2B-j}$.
   Let $k = 2B-j \implies j+k=2B$.
   Sum is $\sum_{B} \sum_{j} a_j a_{2B-j}$.
   This is exactly the sum of coefficients of $x^{2B}$ in $P(x)^2$ for $B \in S$.
   
   Okay, code structure:
   1. Read N, S.
   2. Determine max value $V = 10^6$.
   3. Size $L = 2^{21}$.
   4. Create array `a` of size $L$.
   5. Fill `a`.
   6. FFT function.
   7. Main logic.
   
   To ensure speed in Python:
   - Use a single list for complex numbers? Or tuples? Tuples are immutable, might be slow. Lists `[r, i]`?
   - Actually, using `cmath` and a list of complex numbers is the standard way.
   - Precompute `roots`.
   
   Let's write the code.