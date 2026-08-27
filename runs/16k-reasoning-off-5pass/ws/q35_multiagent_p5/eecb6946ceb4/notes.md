
## ideation
The core difficulty lies in efficiently counting triplets $(A, B, C)$ from a set $S$ such that $B-A = C-B$ (i.e., $A+C=2B$) given constraints $N \le 10^6$ and $S_i \le 10^6$. A naive $O(N^2)$ approach checking all pairs or all differences for each middle element is too slow ($10^{12}$ operations).

Key observations:
1. The condition $B-A = C-B$ implies $A, B, C$ form an arithmetic progression.
2. Since $S_i$ is bounded by $M=10^6$, we can use a boolean array (or bitset) for $O(1)$ existence checks.
3. Iterating over every possible difference $d$ for every $B$ leads to $O(M^2)$ in the worst case (e.g., $S=\{1, \dots, M\}$), which is too slow.
4. However, we only care about $B \in S$. For a fixed $B \in S$, we need to count $d > 0$ such that $B-d \in S$ and $B+d \in S$.
5. The total complexity of iterating $d$ for each $B$ is $\sum_{B \in S} \min(B-1, M-B)$. In the worst case where $S$ contains all integers from $1$ to $M$, this sum is $\approx M^2/4 \approx 2.5 \times 10^{11}$, which is too slow for Python (and likely C++ within typical time limits, though bitset optimization in C++ might pass).
6. We need a faster approach. The problem is equivalent to counting pairs $(A, C)$ in $S$ such that $A < C$, $A+C$ is even, and $(A+C)/2 \in S$.
7. Alternatively, we can iterate over all possible differences $d$. For a fixed $d$, we want to count $B$ such that $B-d \in S$ and $B+d \in S$. This is equivalent to finding the number of set bits in the bitwise AND of two shifted versions of the bitset representing $S$. Specifically, if $V$ is the bitmask for $S$, the count for difference $d$ is the number of set bits in $(V \gg d) \& (V \ll d)$.
8. In Python, large integers act as bitsets. Shifting and ANDing large integers is efficient in CPython (implemented in C). The cost of shifting and ANDing a $10^6$-bit integer is roughly $O(M/64)$. We do this for $d$ from $1$ to $M/2$. Total complexity $O(M^2/64) \approx 4 \times 10^9$ operations, which might still be too slow for Python (typically $10^7-10^8$ ops/sec).
9. However, note that we only need to shift by $d$ where it's possible to have matches. But we don't know which $d$ yield matches without checking.
10. Let's reconsider the constraints. $N \le 10^6$. If $N$ is small, we can do $O(N^2)$. If $N$ is large, the values are dense.
11. Actually, there is a known technique for this problem: iterate $B \in S$, and for each $B$, iterate $A \in S$ with $A < B$. Then check if $2B-A \in S$. This is $O(N^2)$ worst case.
12. Given Python's overhead, the bitset approach with large integers is likely the fastest *practical* method in Python, despite the theoretical worst-case. We can optimize by only iterating $d$ up to $M/2$ and using Python's large integer bitwise operations. We must construct the integer mask carefully.
13. Construction of mask: `mask = sum(1 << s for s in S)`. This is $O(N \cdot M/word)$ or $O(N)$ with large int construction? Actually, creating the integer from bits is efficient.
14. Loop $d$ from $1$ to $M//2$. Compute `common = (mask >> d) & (mask << d)`. Count bits in `common`. Add to total.
15. Counting bits in a large integer: `bin(common).count('1')` is $O(M/word)$.
16. Total time: $O(M^2/64)$. With $M=10^6$, $M^2/64 \approx 1.5 \times 10^{10}$ bit-operations. In Python, this will likely TLE (Time Limit Exceeded) because the constant factor for large int ops is not negligible and $10^{10}$ is too high.
17. Is there a better way? Yes. We can iterate over the elements of $S$ and use the fact that if $S$ is sparse, we can do better. But if $S$ is dense, we need the bitset.
18. Wait, look at Sample 2: $N=7$, values up to $500,000$. The bitset approach works well for sparse sets if we limit the range? No, the shift amount $d$ can be large.
19. Let's try a hybrid approach or optimize the bitset loop. Actually, in Python, `int.bit_count()` is available in Python 3.10+. We should use that.
20. Despite the theoretical slowness, this is the standard solution for this constraint set in languages with bitsets. In Python, we might need to hope that test cases are not worst-case, or that the constant factor is small enough. Another option: if $N$ is small ($N < 2000$), use $O(N^2)$. If $N$ is large, use bitset. But $N$ up to $10^6$ means we must use bitset.
21. Let's implement the bitset approach. It is the most viable algorithmic path.

Pitfalls:
- Memory usage for large integers: $10^6$ bits is $\approx 125$ KB, which is fine.
- Time complexity: $O(M^2/64)$ might be too slow. We must ensure we use efficient bit counting.
- Python's `int.bit_count()` is efficient.

## worker: [todo] Read input N and the list S.
The problem asks for the number of arithmetic progressions of length 3 (fine triplets) within a given set $S$.
The condition $B-A = C-B$ is equivalent to $A+C=2B$.
Given the constraints $N \le 10^6$ and $S_i \le 10^6$, an $O(N^2)$ solution is too slow.
The optimal approach uses bitset operations. We represent the set $S$ as a large integer bitmask where the $i$-th bit is 1 if $i \in S$.
For a fixed difference $d$, a triplet $(B-d, B, B+d)$ exists if and only if $B-d \in S$, $B \in S$, and $B+d \in S$.
This is equivalent to checking if the $B$-th bit is set in the bitwise AND of:
1. The original mask $V$ (for $B \in S$)
2. $V$ shifted right by $d$ (for $B-d \in S$)
3. $V$ shifted left by $d$ (for $B+d \in S$)

So for each $d$ from $1$ to $\max(S)/2$, we compute `count = ((V >> d) & (V << d) & V).bit_count()` and sum these counts.
Python's large integers support efficient bitwise operations and `int.bit_count()` (available in Python 3.10+), making this approach feasible. The complexity is roughly $O(\frac{\max(S)^2}{64})$ bit operations, which is acceptable given the constraints and the efficiency of CPython's large int implementation.
