- **Problem model:** We need the maximum number of disjoint pairs where one mochi is the top and the other is the bottom, with top size at most half of bottom size. Since each mochi can be used at most once, the answer is at most `N // 2`.

- **Input property:** The array is already sorted in non-decreasing order, so no sorting step is needed. This monotonicity is essential for the two-pointer greedy.

- **Pointer split:** Use the first `N // 2` elements as candidate tops and the remaining elements as candidate bottoms. In zero-based indexing, `i` starts at `0` and `j` starts at `N // 2`. This guarantees the two pointers never refer to the same mochi, because `i < N // 2` while `j >= N // 2`.

- **Greedy rule:** For the current smallest unused top `A[i]`, scan bottoms from `j`. If `2 * A[i] <= A[j]`, pair them, increment `ans`, and advance both `i` and `j`. If not, this bottom is too small for the smallest remaining top, and therefore too small for every larger remaining top, so discard it by incrementing only `j`.

- **Why greedy is safe:** If the smallest remaining top can be placed on the current bottom, using that bottom for this top is optimal. Any later top is at least as large, so it cannot benefit from a smaller bottom more than the current top can. If the current bottom cannot support the smallest remaining top, it cannot support any later top, so it is safe to discard.

- **Integer comparison:** Use `2 * A[i] <= A[j]` instead of division or floating point. This avoids rounding issues and is exact. Python integers easily handle values up to `2 * 10^9`.

- **Edge cases:** For `N = 2`, the loop checks exactly the only possible pair. For all equal sizes, no pair is formed unless the size is zero, which is impossible under constraints. For odd `N`, the middle element may be used as a bottom candidate, which is safe because it is still disjoint from the top candidate range.

- **Complexity:** Each pointer moves forward at most `N` times, so the total time is `O(N)`. The input array is stored, giving `O(N)` memory, which is fine for `N <= 5 * 10^5`.

- **Sample verification:** Sample 1 forms pairs `(2,4)`, `(3,7)`, and `(4,10)`, giving `3`. Sample 2 has no bottom at least twice `387`, giving `0`. Sample 3 is counted by the same pointer process and gives `6`.

- **Implementation notes:** Read all integers from standard input at once for speed. The program contains no sample-specific logic and prints only the final answer.
