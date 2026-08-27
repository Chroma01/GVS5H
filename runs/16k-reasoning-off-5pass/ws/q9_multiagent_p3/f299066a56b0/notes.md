
## ideation
The problem asks us to maximize the number of pairs $(A, B)$ from a sorted array $A$ such that $A \le B/2$. Since the input array is already sorted in ascending order, we can leverage this property for an efficient solution.

**Core Difficulty:**
We need to select $2K$ elements to form $K$ pairs. The constraint $A \le B/2$ implies that for a fixed "bottom" element $B$, we need a "top" element $A$ that is at most half its size. To maximize $K$, we should intuitively try to pair the smallest possible valid $A$ with the smallest possible valid $B$. If we use a very large $B$ for a small $A$, we might "waste" the capacity of $B$ to support a larger $A$ that could only be supported by such a large base. Conversely, if we skip a small valid $B$ hoping to use a larger one, we risk not finding a partner for the small $A$ later (since larger $B$s are harder to find if the array is sparse, though here we just need existence).

**Candidate Approaches:**
1.  **Greedy with Two Pointers:**
    -   Maintain two pointers: `left` (for the top mochi) and `right` (for the bottom mochi).
    -   Start `left` at 0 and `right` at 1.
    -   While `right < N`:
        -   Check if $A[\text{left}] \le A[\text{right}] / 2$.
        -   If yes: We found a pair. Increment count, move `left` to `left + 1`, move `right` to `right + 1`.
        -   If no: The current `left` is too big for the current `right`. We need a larger base. Move `right` to `right + 1`.
        -   *Correction/Refinement*: Actually, if $A[\text{left}] > A[\text{right}] / 2$, the current `right` cannot support `left`. Since the array is sorted, any subsequent `right` will be larger, potentially supporting `left`. However, we must ensure we don't skip a valid `left` that could have been paired with the current `right` if we were looking at it differently? No, the logic is: for the smallest available `left`, find the smallest `right` that satisfies the condition. If the current `right` doesn't satisfy it, we must increase `right`. If it does, we pair them and move both.
        -   Wait, what if $A[\text{left}]$ is too big for $A[\text{right}]$, but $A[\text{left}+1]$ is even bigger? Yes, so if $A[\text{left}] > A[\text{right}]/2$, then $A[\text{left}]$ cannot be paired with $A[\text{right}]$. Can $A[\text{left}]$ be paired with a later element? Yes. Can $A[\text{left}+1]$ be paired with $A[\text{right}]$? No, because $A[\text{left}+1] \ge A[\text{left}] > A[\text{right}]/2$.
        -   So, if the condition fails for `(left, right)`, it means `right` is too small to support `left`. We must increment `right`. We do NOT increment `left` because `left` is still waiting for a valid base.
        -   If the condition holds, we pair them. This is optimal because using the smallest valid base for the smallest available top leaves larger bases for larger tops.

2.  **Binary Search + Greedy:**
    -   For each potential top element, binary search for the smallest valid bottom element.
    -   This is $O(N \log N)$, which is acceptable but likely slower than the $O(N)$ two-pointer approach given the sorted nature.

3.  **Dynamic Programming:**
    -   Overkill. $N$ is up to $5 \times 10^5$, $O(N^2)$ is too slow.

**Pitfalls:**
-   **Off-by-one errors:** Indices and loop conditions.
-   **Integer Division:** The condition is $A \le B/2$. In integer arithmetic, this is equivalent to $2A \le B$ or $A \le \lfloor B/2 \rfloor$. Since inputs are integers, $2A \le B$ is safer and clearer to avoid floating point issues.
-   **Pointer Movement Logic:** Ensuring that when a pair is formed, we advance both pointers correctly, and when a pair cannot be formed, we only advance the "bottom" pointer to find a larger base. We never advance the "top" pointer if the current "bottom" is too small, because the current "top" might still be pairable with a future "bottom".

**Algorithm Selection:**
The Two-Pointer approach is $O(N)$ time and $O(1)$ extra space (excluding input storage), which is optimal.

Steps:
1.  Read $N$ and array $A$.
2.  Initialize `i = 0` (top candidate), `j = 1` (bottom candidate), `count = 0`.
3.  While `j < N`:
    -   If `2 * A[i] <= A[j]`:
        -   Pair found.
        -   `count += 1`
        -   `i += 1`
        -   `j += 1`
    -   Else:
        -   Base too small.
        -   `j += 1`
4.  Print `count`.

Wait, let's trace Sample 1: `2 3 4 4 7 10`
- `i=0` (val 2), `j=1` (val 3). $2*2 = 4 > 3$. Fail. `j` becomes 2.
- `i=0` (val 2), `j=2` (val 4). $4 \le 4$. Success. `count=1`, `i=1`, `j=3`.
- `i=1` (val 3), `j=3` (val 4). $6 > 4$. Fail. `j` becomes 4.
- `i=1` (val 3), `j=4` (val 7). $6 \le 7$. Success. `count=2`, `i=2`, `j=5`.
- `i=2` (val 4), `j=5` (val 10). $8 \le 10$. Success. `count=3`, `i=3`, `j=6`.
- `j=6` which is `N`. Stop. Result 3. Matches sample.

Trace Sample 2: `387 388 389`
- `i=0` (387), `j=1` (388). $774 > 388$. `j` -> 2.
- `i=0` (387), `j=2` (389). $774 > 389$. `j` -> 3.
- Stop. Result 0. Matches sample.

The logic holds.

## worker: Implement the solution in Python using the two-poi
The solution implements the greedy two-pointer strategy described in the ideation phase. 
1. **Input Parsing**: Reads all tokens from standard input to handle potential multi-line formatting efficiently.
2. **Algorithm**: 
   - Initializes two pointers `i` (top candidate) and `j` (bottom candidate).
   - Iterates `j` from 1 to `N-1`.
   - Checks if `2 * A[i] <= A[j]`. If true, a valid pair is formed, incrementing the count `k` and advancing both pointers.
   - If false, the current `A[j]` is too small to support `A[i]`, so only `j` advances to find a larger base.
   - This ensures we use the smallest valid base for the smallest available top mochi, maximizing the total number of pairs.
3. **Complexity**: Time complexity is $O(N)$ as each element is visited at most twice. Space complexity is $O(N)$ to store the input array.
4. **Edge Cases**: Handles cases where no pairs can be formed (output 0) and cases where all elements can be paired (output $N/2$).
