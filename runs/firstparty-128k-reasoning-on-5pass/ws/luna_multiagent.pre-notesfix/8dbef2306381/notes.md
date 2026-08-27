
## ideation
The core difficulty is that \(N\) is enormous, while the jump length is bounded by \(B \le 20\). Directly computing reachability for every square is impossible, and blocked positions occur in intervals. The useful observation is that reachability at position \(x\) depends only on the previous \(B\) reachability values, so a rolling \(B\)-bit state can represent the entire relevant history. In a free position the next state is a fixed deterministic transformation; in a bad position the newly appended bit is forced to zero. The algorithm must process interval endpoints and long free gaps without expanding them one square at a time.

Care is needed with the initial state, since square 1 is the starting square and is not bad under the constraints. A destination is reachable only if its bit is set, and bad intervals must be treated inclusively. Transitions near \(N\) must also respect the requirement that jumps land at most at \(N\); equivalently, one can compute reachability only through position \(N\), with nonexistent positions treated as unreachable.

## worker: Derive and implement a provably efficient free-gap
The rolling mask stores reachability of the current square and the previous `B-1` squares. A free transition shifts the mask and sets its lowest bit if any position `A` through `B` steps behind is reachable. A bad position always appends zero.

For `A < B`, choose one reachable position represented by a set bit. Since jumps of lengths `A` and `A+1` are available, every integer distance at least `A(A-1)` can be formed from these jumps. Therefore, after at most `A(A-1)+B-1` free transitions, all of the last `B` positions are reachable, so the mask becomes all ones. The all-ones mask remains unchanged across free positions.

For `A = B`, the free transition is a cyclic rotation of the `B`-bit mask, so an arbitrary-length free gap is handled using rotation by `count mod A`.

A bad interval appends only zeroes. After `B` consecutive bad positions, the entire rolling mask is zero; shorter intervals are handled by a bounded shift. Thus the total work is `O(M * B^2)` for `A < B` and `O(M)` for `A = B`.

## worker: Fix `advance_free` for `A < B`: the bound `A*(A-1)
For `A < B`, let `T = A(A-1)`. Every integer at least `T` is representable as a sum of jumps `A` and `A+1`.

From any reachable position in the rolling state, take a first jump of length `B`; this lands strictly in the future regardless of which of the last `B` positions was reachable. Any sufficiently large subsequent distance can then be formed using jumps `A` and `A+1`. After at most `T + 2B - 1` free transitions, all of the last `B` positions are reachable, so the state is all ones and remains fixed.

This gives a safe bounded simulation for each free gap. Bad intervals are handled by shifting the mask and appending zeroes; after `B` consecutive bad squares the state becomes zero.
