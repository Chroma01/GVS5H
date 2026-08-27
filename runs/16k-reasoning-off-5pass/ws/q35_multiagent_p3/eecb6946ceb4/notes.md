
## ideation
The problem asks us to count the number of "fine triplets" (A, B, C) from a given set S of N distinct positive integers, such that A < B < C and B - A = C - B. This condition is equivalent to A + C = 2B, meaning A, B, C form an arithmetic progression.

Constraints:
- N up to 10^6.
- Values S_i up to 10^6.

A naive O(N^2) approach checking all pairs is too slow (10^12 operations).
An approach iterating over each B and checking possible differences d is also potentially slow if the range of values is large, though the max value is 10^6. Specifically, for each B, the number of possible d's is roughly min(B, MaxVal - B). In the worst case (e.g., S contains all integers from 1 to 10^6), this is O(MaxVal^2) which is 10^12, still too slow.

The key insight is to use polynomial multiplication (via FFT) to count pairs (A, C) that sum to a specific value.
Let's define a binary array `P` of size M (where M is slightly larger than max(S), e.g., 2*10^6 + 1) such that `P[i] = 1` if `i` is in S, and `0` otherwise.
If we compute the convolution of `P` with itself, the resulting array `Q` will have `Q[k]` equal to the number of pairs (A, C) such that A + C = k, where A and C are in S. Note that this counts ordered pairs, so (A, C) and (C, A) are both counted if A != C, and (A, A) is counted once if A is in S.

For a fixed B in S, we want to count the number of pairs (A, C) in S such that A + C = 2B and A < C.
The total number of pairs (A, C) with A + C = 2B is given by `Q[2*B]`.
This count includes:
1. Pairs where A = C = B. This happens if B is in S (which it is) and 2B = B + B. So we subtract 1 if B is in S (which it always is in our loop).
2. Pairs where A != C. These come in symmetric pairs (A, C) and (C, A). Since we want A < C, we take half of the remaining count.

So, for each B in S, the number of valid pairs (A, C) with A < C and A + C = 2B is:
`count = (Q[2*B] - 1) // 2`
Note: We subtract 1 because the pair (B, B) is included in `Q[2*B]` (since B is in S). The problem requires distinct A, B, C, so A != C is required. Since A < C implies A != C, this is consistent.

Algorithm:
1. Read input.
2. Determine max_val = max(S).
3. Create a polynomial `P` of size next power of 2 >= 2 * max_val + 1, with `P[i] = 1` if `i` in S, else 0.
4. Compute FFT of P.
5. Point-wise square the FFT result.
6. Compute inverse FFT to get the convolution array Q.
7. Initialize answer = 0.
8. For each B in S:
   - If 2*B < len(Q):
     - num_pairs = Q[2*B]
     - Since B is in S, the pair (B, B) contributes 1 to Q[2*B].
     - The number of pairs with A != C is num_pairs - 1.
     - The number of pairs with A < C is (num_pairs - 1) // 2.
     - Add this to answer.
9. Print answer.

Complexity: FFT takes O(M log M) where M is the size of the polynomial (approx 2*10^6). This is efficient enough.

Pitfalls:
- Floating point precision issues with FFT. Using complex numbers in Python's `cmath` or `numpy` might lead to small errors. Rounding to nearest integer is necessary.
- Size of FFT: Must be large enough to hold the convolution result. The max sum is 2 * 10^6, so size should be at least 2*10^6 + 1. Next power of 2 is 2^21 = 2097152, which is sufficient.
- The problem states distinct positive integers, so A, B, C are distinct. The condition A < B < C ensures this. Our formula counts pairs (A, C) with A < C. Since B is the midpoint, A < B < C is automatically satisfied if A < C and A + C = 2B?
  - A + C = 2B => B = (A+C)/2.
  - If A < C, then A < (A+C)/2 < C is true. So yes, A < B < C holds.
  - We must ensure A, B, C are in S. A and C are in S by construction. B is in S because we iterate over B in S.
  - So the logic holds.

Let's implement this using Python's `cmath` for FFT to avoid external dependencies like numpy, although numpy is faster. Given the constraints and Python's overhead, a pure Python FFT might be slow. However, 2^21 is about 2 million, and O(N log N) is roughly 2*10^6 * 21 ~ 4*10^7 operations, which might be tight in pure Python. Using `numpy` is preferred if allowed, but the prompt doesn't specify. Standard library only? `cmath` is standard. Let's try to use `numpy` if possible, but to be safe and standard, I'll implement a simple FFT or use `cmath`. Actually, for competitive programming in Python, `numpy` is often available. But to be strictly standard, I'll write a recursive FFT or use an iterative one. Given time limits, an iterative FFT is better.

Wait, there's a simpler approach without FFT?
Since max value is 10^6, we can use a boolean array `exists`.
For each B in S, we want to count d > 0 such that B-d in S and B+d in S.
This is equivalent to counting intersections of shifted sets.
But this is still potentially slow.

Let's stick with FFT. I'll use `numpy` if I can import it, otherwise I'll implement a basic FFT. The problem doesn't forbid imports. I'll assume standard libraries are fine. `numpy` is not a standard library. I should probably implement FFT or use a different method.

Alternative: Bitset?
In C++, `std::bitset` can do this efficiently. In Python, integers act as bitsets.
Let `mask` be an integer where the i-th bit is 1 if i is in S.
We want to count for each B, the number of d such that bit (B-d) and bit (B+d) are set.
This is equivalent to counting set bits in `(mask & (mask >> d))`? No, that's for fixed d.
We need to sum over d.
Actually, the convolution approach is the most straightforward.

Let's implement a simple iterative FFT in Python. It might be slow but let's try. Or, since N and max_val are up to 10^6, maybe the number of elements is small? No, N is up to 10^6.

Actually, there is a known trick:
The number of arithmetic progressions of length 3 in a set S is related to the number of solutions to A+C=2B.
We can use the fact that the values are small (10^6).
Let's use `numpy` if available. If not, I'll write a simple FFT.

I'll write a solution using `numpy` for speed, as it's commonly available in such environments. If not, I'll fallback. But the prompt says "standard input", implying a general environment. I'll try to use `numpy`.

Wait, I should check if `numpy` is allowed. Usually, in these problems, only standard library is guaranteed. I'll implement a basic FFT.

To optimize, I'll use an iterative FFT.

Steps:
1. Read input.
2. Create array `P` of size M (power of 2, >= 2*10^6+1).
3. Set `P[i] = 1` if `i` in S.
4. FFT(P).
5. Square each element.
6. Inverse FFT.
7. Round results to nearest integer.
8. Sum up counts for each B in S.

Let's code this.

## worker: Implement the iterative FFT, read input, compute c
1. **Problem Analysis**: The problem asks for the number of triplets $(A, B, C)$ from a set $S$ such that $A < B < C$ and $B - A = C - B$. This condition is equivalent to $A + C = 2B$, meaning $A, B, C$ form an arithmetic progression.
2. **Algorithm Choice**: A naive $O(N^2)$ approach is too slow for $N \le 10^6$. Using FFT (Fast Fourier Transform) allows us to compute the number of pairs $(A, C)$ that sum to a specific value efficiently.
3. **FFT Implementation**:
   - We create a binary polynomial $P$ where the coefficient of $x^i$ is 1 if $i \in S$, and 0 otherwise.
   - The convolution $P * P$ gives a polynomial where the coefficient of $x^k$ is the number of pairs $(A, C)$ such that $A + C = k$.
   - We compute this convolution using FFT: $FFT(P)$, square the result point-wise, then apply inverse FFT.
4. **Counting Triplets**:
   - For each $B \in S$, we look at the coefficient of $x^{2B}$ in the convolution result, denoted $Q[2B]$.
   - $Q[2B]$ counts all ordered pairs $(A, C)$ with $A, C \in S$ and $A+C=2B$. This includes $(B, B)$ since $B+B=2B$.
   - Since we require distinct $A, B, C$ and $A < C$, we exclude the case $A=C=B$. The remaining pairs come in symmetric pairs $(A, C)$ and $(C, A)$.
   - The number of valid pairs with $A < C$ is $(Q[2B] - 1) // 2$.
   - Summing this over all $B \in S$ gives the total number of fine triplets.
5. **Complexity**: The FFT size is $O(\max(S))$, which is up to $2 \cdot 10^6$. The FFT runs in $O(M \log M)$ where $M$ is the size of the array. This is efficient enough for the given constraints.
6. **Precision**: Using complex numbers in Python's `cmath` (via `complex`) and rounding the real part of the inverse FFT result handles precision issues adequately for integer counts.
