
## ideation
Core difficulty: the middle segment's distinct count depends on both cut positions (i,j), so a naive O(N^2) approach is impossible for N up to 3e5. Need to decouple the three parts.

Key insight: prefix distinct P[i] and suffix distinct S[j+1] are easy O(N) precomputations. For the middle segment (i+1..j), its distinct count equals the number of positions k in (i+1..j] that are the *first occurrence of their value within the segment*, i.e., positions k with prev[k] <= i (where prev[k] = previous occurrence index of A[k], or 0 if none). So:

answer = max over j of ( S[j+1] + max over i in [1, j-1] of ( P[i] + #{k in (i+1..j] : prev[k] <= i} ) ).

Sweep j from left to right, maintaining a structure over candidate i values. Define val[i] = P[i] + contributions. When we advance j to a new position k=j with prev[j] = p (p >= 1), then for all i in [p, j-1], position j now lies in (i+1..j] and prev[j]=p <= i, so each such i gains +1. That's a range-add on i in [p, j-1]. Then query max val[i] over i in [1, j-1], add S[j+1], and take the global max. Note i must be >= 1 and <= j-1; also i ranges only where subarrays are non-empty: i >= 1, j <= N-1, i < j.

Implementation: segment tree with lazy propagation supporting range add and range max query, size N+2. Initialize val[i] = P[i] for i in 1..N-1 (or all i, but only query i in [1, j-1]). For j from 2 to N-1: first apply the update for position j (if prev[j] > 0, range add [prev[j], j-1] +1), then query max over [1, j-1] and combine with S[j+1]. Wait — order: contributions for segment (i+1..j] must include position j, so update with k=j before querying at this j. Positions with prev[j]=0 (first occurrence ever) contribute to no i (since prev[k]=0 <= i always... actually prev[k]=0 <= i for all i >= 1, so position k always counts as first-in-segment for any i < k). Hmm: for k with prev[k]=0, the condition prev[k] <= i holds for all valid i, so it contributes +1 to all i in [1, k-1]. So range add [1, j-1] when prev[j]=0. Equivalently range [max(prev[j],1), j-1]. Let me double check the condition: position k is in segment (i+1..j] iff i+1 <= k <= j iff i <= k-1 and i >= k-j... for fixed k=j: i in [?, j-1], and i >= 1. And first-in-segment iff no other occurrence of A[k] in (i+1..k-1], iff prev[k] <= i. So i ranges in [max(1, prev[k]), k-1]. Yes: range add [max(1,prev[j]), j-1] by +1 when processing position j. Correct for both cases.

Alternative: BIT-based approach with difference arrays per j is harder; segment tree lazy is straightforward. Could also use a "max-plus range add" via a sorted structure, but segtree is simplest.

Pitfalls:
- 1-indexed vs 0-indexed off-by-one errors in ranges.
- j only goes up to N-1 (third segment non-empty); i from 1 to j-1.
- Initialize segtree with P[i]; P[0]=0 but i>=1 required.
- Answer must be at least 3 (each segment has >=1 distinct), but computation handles it.
- N up to 3e5, O(N log N) fine in Python with iterative segtree or fast lazy propagation; use sys.stdin fast IO. A recursive lazy segtree in Python may be borderline but okay at 3e5 (~6e5 operations). Iterative segment tree with lazy (e.g., atcoder-style) is safer.

## worker: Implement and verify the full solution: write solv
- Formulation: answer = max over j of S[j+1] + max over i in [1, j-1] of (P[i] + #{k in (i+1..j] : prev[k] <= i}).
- Sweep j from 2 to N-1. When processing position k=j, it lies inside segment (i+1..j] for all i <= j-1, and it is the first occurrence of its value within that segment iff prev[j] <= i. Hence it contributes +1 to every candidate i in [max(1, prev[j]), j-1] — a range add.
- The segment tree maintains val[i] = P[i] + accumulated contributions; at each j we query max over i in [1, j-1] and add S[j+1].
- Verified against samples: (3 1 4 1 5) → 5; (2 5 6 4 4 1 1 3 1 4) → 9.
- Stress-tested against an O(N^3) brute force for N in [3, 12] with random values in [1, N] (thousands of trials): all matched.
- Complexity: O(N log N) time, O(N) memory. N = 3e5 runs comfortably.
