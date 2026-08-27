
## ideation
The core difficulty is that the middle element is fixed by position, while the other four elements must be chosen as two indices on each side. Its value must have a strictly greater frequency than every other value, so ties must be excluded carefully. The useful observation is that, after including the middle element, the middle value can occur from one through five times. If it occurs at least three times, it is automatically the unique mode. If it occurs exactly twice, every other selected value must occur at most once. If it occurs only once, it cannot be a unique mode.

All counting must preserve index order: for a fixed middle index, selections are exactly a pair from the prefix and a pair from the suffix. Duplicate values must be counted by index multiplicity, not merely by distinct-value count.

## worker: Derive and implement the \(O(n^2)\) fixed-middle c
For each fixed middle index, choose two indices on the left and two on the right.

- If at least two of the four chosen values equal the middle value, it appears at least three times total and is automatically the unique mode.
- If exactly one additional copy is chosen, the other three values must be pairwise distinct; otherwise another value ties the middle value.
- With no additional copy, the middle value cannot be a mode.

The algorithm maintains left/right frequency maps while scanning the middle index. Pair counts and the cross-frequency dot product are updated in constant time, so each index is processed in \(O(1)\) amortized time after map operations. Overall complexity is \(O(n)\) expected time and \(O(n)\) space.

## worker: Replace the incorrect distinctness correction term
For a fixed middle index, the middle value must occur at least three times in total.

- With at least two additional copies, it is automatically the unique mode.
- With exactly one additional copy, the remaining three values must be pairwise distinct.
- With no additional copy, the middle value cannot be the unique mode.

The cross-moments maintain duplicate-match corrections in constant time:

- `dot = Σ(l_v r_v)`
- `T = Σ(l_v r_v²)`
- `U = Σ(l_v² r_v)`

When choosing one non-middle value from one side and two distinct values from the other, forbidden equalities are counted using:

- `R0 * dot - T`
- `L0 * dot - U`

All maintained quantities are updated when the sweep moves the middle element from the right partition to the left partition. The complexity is expected `O(n)` time and `O(n)` space.

## worker: Exhaustively validate the current fixed-middle cro
For a fixed middle index, exactly two elements are selected from each side.

The middle value is a unique mode precisely in these cases:

- At least two of the four selected side values equal it, giving frequency at least three.
- Exactly one selected side value equals it, and the remaining three values are pairwise distinct.

The implementation counts both cases using frequency maps and maintains the cross moments:

- `dot = Σ left[v] * right[v]`
- `T = Σ left[v] * right[v]^2`
- `U = Σ left[v]^2 * right[v]`

These moments allow duplicate-value exclusions to be computed in constant time per middle index. The sweep runs in expected `O(n)` time and uses `O(n)` space.

## worker: Run exhaustive brute-force validation of the curre
The implementation counts each fixed middle index by choosing two indices on each side.

A valid subsequence has either:
- at least two additional copies of the middle value, making its frequency at least three; or
- exactly one additional copy, with the other three values pairwise distinct.

The cross moments `dot`, `T`, and `U` remove duplicate-value conflicts in constant time. The sweep maintains all frequency data while moving the middle index from right to left.

The formulas were checked against exhaustive small-array enumeration, the three provided examples, all-equal arrays, all-distinct arrays, and repeated competing values. The complexity is expected `O(n)` time and `O(n)` space.
