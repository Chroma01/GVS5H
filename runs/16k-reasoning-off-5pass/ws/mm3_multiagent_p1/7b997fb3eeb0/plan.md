We need to answer for each query on a subarray `A[L..R]` the maximum number of disjoint pairs `(small, big)` such that `small <= big / 2` (equivalently `2*small <= big`). Since the array is sorted globally, any subarray is also sorted. This is a classic "maximum matching with a 2-constraint" on a sorted array, solvable greedily: repeatedly take the smallest remaining element as the "top" and find the smallest remaining element that is at least twice it as the "bottom". The count is the number of successful pairings.

The naive greedy per query is O(length) → too slow. We precompute, for each position `i`, the index `nxt[i]` = smallest `j > i` such that `A[j] >= 2*A[i]`. With the array sorted, `nxt[i]` can be found in O(N) total using a two-pointer sweep (since `i` and `j` only move forward).

Then we can answer each query with a "skip-list" style traversal: starting at `i = L`, while `i <= R`:
- let `j = nxt[i]`. If `j > R`, stop (no more valid bottoms).
- count one pair, then set `i = j + 1` (skip the used bottom). Because each used element is never revisited, the total work across all queries could be O(total length of queries) in the worst case, which is still too large for Q up to 2e5.

We need faster per query: build a binary lifting table `jump[k][i]` = the new position after greedily starting at `i` and performing `2^k` pairings (or the position after the last successful pairing among those). With `nxt` we can build this in O(N log N). Then each query is answered by binary lifting in O(log N) by finding the largest K such that the `K`-th pairing fits inside `[L, R]`.

The query answer is therefore the maximum K such that after `K` greedy steps starting from `L`, all chosen positions stay ≤ R. This is exactly the "reach within range" query on a functional graph (the "next" position after using one pair is `nxt[i] + 1`). With binary lifting, each query is O(log N), and preprocessing is O(N log N).

Edge cases:
- `nxt[i]` may be `N+1` (no valid bottom); encode as `N+1`.
- When `i > R` or `nxt[i] > R`, the current `i` cannot start a pair within the subarray; we need to advance `i` to the first index where a pairing might start. The standard binary lifting approach already handles this because we only "use" steps whose target positions are ≤ R.

Implementation details:
- 0-indexed arrays.
- `nxt[i]`: use two pointers `i` from 0..N-1, `j` starting from previous value. While `j < N and A[j] < 2*A[i]`, advance `j`. Then `nxt[i] = j`.
- `jump[0][i] = nxt[i] + 1` if `nxt[i] < N` else `N`. This is the position after one pairing starting at `i`. If `nxt[i] >= N`, no pairing possible; we set `jump[0][i] = N` (a sentinel).
- `jump[k][i] = jump[k-1][ jump[k-1][i] ]` (sentinel `N` stays `N`).
- For query `(L, R)` (1-indexed in input, convert to 0-indexed, so subarray is `A[L..R-1]` inclusive in 0-index, length `len = R-L+1`):
  - Let `pos = L`. We want max K such that the position after K pairings is still ≤ R. Equivalently, we want the largest K such that `jump[K_steps](pos) <= R`, where we try powers of two from high to low.
  - Actually the binary lifting on "how many pairings fit" can be done greedily: maintain `cur = L`, `ans = 0`. For `k` from LOG down to 0: if `jump[k][cur] <= R`, then we can do `2^k` pairings safely: `ans += 2^k`, `cur = jump[k][cur]`. After the loop, we've counted the maximum number of pairings that fit entirely inside `[L, R]`. This works because if after `2^k` pairings the cursor is still ≤ R, all those pairings used distinct elements within the range.

This yields O((N+Q) log N) time and O(N log N) memory.