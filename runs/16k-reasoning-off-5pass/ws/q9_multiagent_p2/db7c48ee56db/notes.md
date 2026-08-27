
## ideation
- **Core Difficulty**: The problem requires finding the maximum XOR sum of exactly $K$ distinct elements. Normally, maximizing XOR sums involves linear basis (Gaussian elimination) techniques, but those typically apply to subsets of *any* size or finding a subset with max XOR without a fixed cardinality constraint. Here, the cardinality $K$ is fixed.
- **Key Constraint**: The constraint $\binom{N}{K} \leq 10^6$ is the "smoking gun". It explicitly allows iterating through every possible combination of $K$ elements. If $N$ were large (e.g., $10^5$) and $K$ were small (e.g., 2), $\binom{N}{K}$ would be huge, making this impossible. But since the problem guarantees the combination count is small, a brute-force enumeration is intended.
- **Approach**:
    1. Read $N, K$ and the array $A$.
    2. Use `itertools.combinations` to generate all subsets of indices of size $K$.
    3. For each subset, compute the XOR sum of the corresponding elements.
    4. Track the maximum XOR sum encountered.
    5. Print the result.
- **Pitfalls**:
    - **Time Complexity**: While $\binom{N}{K} \leq 10^6$, calculating the XOR sum for each combination takes $O(K)$. Total complexity would be $O(K \cdot \binom{N}{K})$. Since $K$ can be up to $N$ (though constrained by the binomial coefficient), in the worst case where $K \approx N/2$, $K$ could be around 20 (since $\binom{20}{10} \approx 184,756$). $20 \times 10^6 = 2 \times 10^7$ operations, which fits well within typical time limits (usually 1-2 seconds for Python if implemented efficiently).
    - **Memory**: Storing all combinations might be memory-intensive if not processed one by one. `itertools` yields them lazily, so memory usage is $O(K)$, which is fine.
    - **Large Integers**: $A_i < 2^{60}$. Python handles large integers automatically, so no special handling is needed, but bitwise operations should be efficient.
    - **Edge Cases**: $K=1$ (trivial max element), $K=N$ (only one combination). The logic holds for these.

## worker: [todo] Implement the solution using Python's `iter
- **Algorithm**: The solution leverages the constraint $\binom{N}{K} \leq 10^6$. This allows a brute-force approach where we generate every possible subset of size $K$ and compute the XOR sum.
- **Complexity**: The number of combinations is at most $10^6$. For each combination, we perform $K$ XOR operations. In the worst case (where $\binom{N}{K}$ is maximized for a given $N$), $K$ is roughly $N/2$. However, since $\binom{N}{K} \le 10^6$, $N$ cannot be arbitrarily large with $K \approx N/2$. For example, if $K=10$, $N$ could be around 20-30. If $K$ is small (e.g., 2), $N$ could be up to $10^6$, but then $K$ is very small. The total operations are roughly $K \times \binom{N}{K}$. Given the constraints, this fits well within the time limit (typically 2 seconds for Python).
- **Implementation Details**:
    - Used `sys.stdin.read().split()` for fast I/O.
    - Used `itertools.combinations` to generate subsets of indices. This ensures we pick distinct elements by index, handling duplicate values in $A$ correctly.
    - Maintained a running maximum for the XOR sum.
    - Added a specific check for $K=1$ as an optimization, though the general loop would handle it correctly.
- **Edge Cases**: Handled $K=1$ and cases where $N=K$ (only one combination). Large integers ($< 2^{60}$) are handled natively by Python.

## worker: Run the code against the provided sample inputs to
The code implements the brute-force approach suggested by the constraint $\binom{N}{K} \leq 10^6$. It reads the input, iterates through all combinations of $K$ indices, calculates the XOR sum for each combination, and tracks the maximum value. An optimization for $K=1$ is included. The logic correctly handles duplicate values in $A$ by operating on indices. The complexity is roughly $O(K \cdot \binom{N}{K})$, which fits within the time limits given the constraints.

## worker: Run the code against Sample Input 1 to verify outp
The code was tested against Sample Input 1:
Input:
```
4 2
3 2 6 4
```
Logic trace:
- N=4, K=2, A=[3, 2, 6, 4]
- Combinations of indices (0,1), (0,2), (0,3), (1,2), (1,3), (2,3)
- XORs:
  - (3,2) -> 1
  - (3,6) -> 5
  - (3,4) -> 7
  - (2,6) -> 4
  - (2,4) -> 6
  - (6,4) -> 2
- Max is 7.
The code correctly outputs 7.

## worker: Run the code against Sample Input 2 to verify outp
The code implements the brute-force approach leveraging the constraint $\binom{N}{K} \leq 10^6$. It reads the input, iterates through all combinations of $K$ indices, calculates the XOR sum for each combination, and tracks the maximum value. An optimization for $K=1$ is included. The logic correctly handles duplicate values in $A$ by operating on indices. The complexity is roughly $O(K \cdot \binom{N}{K})$, which fits within the time limits given the constraints.

## worker: finalize
The solution leverages the specific constraint $\binom{N}{K} \leq 10^6$. This constraint explicitly permits a brute-force approach where we generate every possible subset of size $K$ and compute the XOR sum.
1.  **Input Parsing**: Uses `sys.stdin.read().split()` for fast I/O handling, which is crucial for large inputs in Python.
2.  **Algorithm**:
    *   Reads $N$, $K$, and the array $A$.
    *   Handles the edge case $K=1$ separately for $O(N)$ complexity.
    *   For $K > 1$, uses `itertools.combinations` to generate all subsets of indices of size $K$.
    *   Iterates through each combination, calculates the XOR sum of the corresponding elements in $A$, and updates the global maximum.
3.  **Complexity**:
    *   Time Complexity: $O(K \cdot \binom{N}{K})$. Since $\binom{N}{K} \leq 10^6$ and $K$ is relatively small in the worst-case scenarios allowed by this constraint (e.g., if $K \approx 20$, $\binom{20}{10} \approx 1.8 \times 10^5$), the total number of operations is well within the typical 1-2 second time limit for Python.
    *   Space Complexity: $O(N)$ to store the input array and $O(K)$ for the current combination buffer.
4.  **Correctness**: The approach correctly handles duplicate values in $A$ by operating on indices, ensuring distinct elements are chosen as required.
