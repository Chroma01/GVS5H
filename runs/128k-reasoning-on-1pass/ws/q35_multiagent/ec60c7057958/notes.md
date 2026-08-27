
## ideation
The core difficulty lies in efficiently counting valid alternating permutations that can be formed given a fixed prefix and remaining counts of odd/even numbers, without enumerating them. Since adjacent elements must alternate parity, the parity pattern for the entire permutation is strictly determined by the parity of the first element (or second, if the first is fixed). This means once we pick a candidate for the current position, the required parity for all subsequent positions is fixed. 

We can use a greedy approach: iterate through available numbers in lexicographical order. For each candidate, calculate how many valid completions exist. If `k` is within this count, we pick the candidate and proceed to the next position. Otherwise, we subtract the count from `k` and try the next candidate. The number of valid completions is simply `rem_o! * rem_e!` if the remaining counts match the required alternating pattern, otherwise 0. We precompute factorials capped at `10^15 + 7` to handle large `k` efficiently. The time complexity is `O(n^2)` due to list operations, which is well within limits for `n <= 100`.

## worker: finalize
The solution uses a greedy approach to construct the k-th alternating permutation position by position:

1. **Precompute factorials** capped at `10^15 + 7` to handle large k values efficiently.

2. **Count total alternating permutations**: For even n, both parity patterns (starting odd or even) are valid, giving `2 * (n/2)! * (n/2)!`. For odd n, only the pattern starting with odd is valid, giving `((n+1)/2)! * (n/2)!`.

3. **Greedy construction**: At each position, iterate through available numbers in lexicographic order. For each candidate, compute how many valid completions exist:
   - Once the first element's parity is fixed, the entire parity pattern is determined.
   - The number of valid completions is `rem_o! * rem_e!` if remaining odd/even counts match required positions, else 0.
   - If k falls within the count, select the candidate; otherwise subtract and try the next.

4. **O(1) position counting**: The number of odd/even positions remaining can be computed directly from the remaining count and the first remaining position's parity, avoiding O(n) loops.

Time complexity: O(n²) — at most n candidates per position, each taking O(1) to evaluate.
Space complexity: O(n) for the result and tracking arrays.
