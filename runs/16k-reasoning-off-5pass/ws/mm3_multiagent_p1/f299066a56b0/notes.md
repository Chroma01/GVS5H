
## ideation
The problem asks for the maximum number of disjoint pairs (a,b) with a ≤ b/2, i.e., 2a ≤ b. Since the array is sorted ascending, a greedy strategy works: repeatedly take the smallest unused mochi as the "top" and pair it with the smallest unused mochi that is at least twice its size. This is a classic two-pointer / matching problem.

Approach details:
- Let `i` be the index for the "top" mochi (smallest remaining).
- Let `j` be the index for the "bottom" mochi (larger remaining).
- Initialize `i = 0`, `j = N // 2` (a safe starting point because at most N/2 pairs can exist).
- While `i < j` and `j < N`:
  - If `2 * A[i] <= A[j]`: we can form a pair. Increment answer, move `i += 1`, `j += 1`.
  - Else: the current bottom is too small; move `j += 1` to find a larger one.
- The answer is the number of successful pairs.

Why this works: The greedy choice always uses the smallest available top and the smallest available bottom that can accommodate it. Any other pairing would not allow more pairs because using a larger bottom earlier would only reduce options for smaller tops later.

Complexities:
- Time: O(N) — each pointer moves at most N times.
- Space: O(1) extra (besides input array).

Pitfalls:
- Use 64-bit integers (Python int is fine) to avoid overflow when doubling.
- Ensure `j` starts at `N // 2` to avoid unnecessary checks, but the loop condition `i < j` is essential.
- Edge cases: N=2, all equal sizes (answer 0), or strictly increasing by factor >2 (answer N//2).

## worker: Read N and the sorted list A.
The greedy two-pointer algorithm pairs the smallest remaining mochi with the smallest larger mochi whose size is at least twice it. Starting `j` at `n//2` is a safe lower bound because at most `n//2` pairs can exist, but the `i < j` guard is what truly ensures correctness. Each pointer advances at most N times, giving O(N) time and O(1) extra space. Python integers handle the doubling safely, so no overflow concerns. Verified against the three samples: 3, 0, 6.
