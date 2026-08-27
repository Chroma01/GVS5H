
## ideation
- **Core Difficulty**: The problem is a maximum matching problem on a specific constraint graph ($a \le b/2$). Since $N$ is up to $5 \times 10^5$, an $O(N^2)$ solution is impossible. We need an $O(N)$ or $O(N \log N)$ approach. The input is already sorted, which is a huge hint for a linear scan.
- **Candidate Approaches**:
  1. **Greedy with Two Pointers**: Iterate with two pointers. One pointer (`left`) tracks the smallest available "top" mochi. Another pointer (`right`) tracks the smallest available "bottom" mochi.
     - If $A[\text{left}] \le A[\text{right}] / 2$, we can form a pair. Increment count, move both pointers.
     - If not, the current `right` is too small to cover `left`. We must try a larger `right`. Move `right` pointer.
     - *Why this works*: Using the smallest valid `right` for a given `left` saves larger `right` values for potentially larger `left` values later, maximizing the total pairs.
  2. **Binary Search on Answer**: Check if it's possible to make $K$ pairs. To check $K$, we need to find $K$ disjoint pairs. This check might be complex to implement efficiently without a greedy strategy inside, making the two-pointer approach superior.
  3. **Dynamic Programming**: $O(N^2)$ space/time, too slow.
- **Pitfalls**:
  - Integer division vs floating point: The condition is $a \le b/2$. In integer arithmetic, this is $2a \le b$.
  - Pointer logic: Ensure we don't skip potential pairs or use the same element twice. The two-pointer logic naturally handles distinct elements if we advance indices correctly.
  - Edge cases: $N$ is small, no pairs possible, all pairs possible.

## worker: Implement the two-pointer greedy algorithm in Pyth
- **Algorithm**: The solution uses a greedy strategy with two pointers. Since the input array $A$ is sorted, we can efficiently find the maximum number of pairs.
- **Logic**:
  - `left` points to the smallest available mochi (potential top).
  - `right` points to the next available mochi (potential bottom).
  - If $2 \times A[\text{left}] \le A[\text{right}]$, we form a pair because $A[\text{left}]$ is the smallest possible top, and $A[\text{right}]$ is the smallest valid bottom for it. This is optimal because using a larger bottom for this small top would waste a potentially useful large bottom for a larger top later.
  - If the condition fails, $A[\text{right}]$ is too small to cover $A[\text{left}]$. Since the array is sorted, no subsequent `left` (which will be larger or equal) can be covered by the current `right`. Thus, we must increment `right` to find a larger bottom mochi.
- **Complexity**: Time complexity is $O(N)$ because both pointers traverse the array at most once. Space complexity is $O(N)$ to store the input.
- **Edge Cases**: Handled naturally. If no pairs can be formed, `k` remains 0. If $N$ is small, the loop terminates correctly.

## worker: Verify the solution against the provided sample in
The solution implements a greedy strategy using two pointers, which is optimal for this problem given the sorted input.
1.  **Logic Verification**:
    *   **Sample 1**: `2 3 4 4 7 10`.
        *   `left=0 (2)`, `right=1 (3)`: $2*2 \le 3$? No ($4 \le 3$ False). `right` becomes 2.
        *   `left=0 (2)`, `right=2 (4)`: $2*2 \le 4$? Yes. Pair (2,4). `k=1`, `left=1`, `right=3`.
        *   `left=1 (3)`, `right=3 (4)`: $2*3 \le 4$? No ($6 \le 4$ False). `right` becomes 4.
        *   `left=1 (3)`, `right=4 (7)`: $2*3 \le 7$? Yes. Pair (3,7). `k=2`, `left=2`, `right=5`.
        *   `left=2 (4)`, `right=5 (10)`: $2*4 \le 10$? Yes. Pair (4,10). `k=3`, `left=3`, `right=6`.
        *   Loop ends. Output 3. Correct.
    *   **Sample 2**: `387 388 389`.
        *   `left=0 (387)`, `right=1 (388)`: $2*387 \le 388$? No. `right` becomes 2.
        *   `left=0 (387)`, `right=2 (389)`: $2*387 \le 389$? No. `right` becomes 3.
        *   Loop ends. Output 0. Correct.
2.  **Complexity**: The `left` pointer moves forward only when a pair is formed, and `right` moves forward otherwise. Both pointers traverse the array at most once. Time complexity is $O(N)$. Space complexity is $O(N)$ to store the input.
3.  **Constraints**: $N \le 5 \times 10^5$ fits well within time limits for an $O(N)$ solution. Values up to $10^9$ fit in standard 64-bit integers (Python handles arbitrarily large integers automatically).
