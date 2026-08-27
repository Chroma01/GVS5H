
## ideation
We need to find the maximum number of disjoint pairs (a,b) with a ≤ b/2 (equivalently 2a ≤ b) from a sorted list of N mochi. This is a classic greedy matching problem: to maximize pairs, pair the smallest remaining mochi with the smallest possible larger mochi that satisfies the size condition. This can be done with two pointers.

Approach:
- Let `i` point to the smallest unused mochi (starting at 0), `j` point to the first mochi that could serve as the larger one (starting at 1).
- While `i < j` and `j < N`:
  - If `2 * A[i] <= A[j]`, then we can form a kagamimochi: increment answer, move `i` to `i+1`, move `j` to `j+1`.
  - Otherwise, `A[j]` is too small to pair with `A[i]`, so advance `j` to find a larger mochi.
- This greedy works because pairing the smallest possible left with the smallest possible right leaves the remaining elements as large as possible for future pairings.

Complexities:
- O(N) time, O(1) extra space.
- N up to 5e5, values up to 1e9, so 2*A[i] fits in 64-bit.

Edge cases:
- N < 2 -> answer 0 (but N≥2 by constraints).
- No valid pairs -> answer 0.
- Duplicate sizes allowed; condition uses ≤.

Pitfalls:
- Must use 64-bit integer for multiplication (2*A[i]).
- Ensure `i` does not overtake `j`; loop condition handles that.
- After pairing, `i` moves to next, `j` to next; but what if `j` is already used? Since each mochi can be used at most once, we must ensure that we never use a mochi as both a top and a bottom. The pointer movement guarantees disjointness because both `i` and `j` always move forward, never reusing indices.

## worker: Implement the greedy two-pointer solution in Pytho
- The two-pointer greedy works: pair the smallest available mochi with the smallest larger mochi that satisfies `2*a[i] <= a[j]`.
- When `2*a[i] > a[j]`, `a[j]` is too small to be the base for `a[i]`, so we advance `j` to look for a larger base.
- When a pair is formed, both pointers advance, ensuring each mochi is used at most once.
- Time complexity: O(N), space complexity: O(1) beyond the input array.
- The product `2*a[i]` fits in Python's arbitrary precision integers, so no overflow concerns.
