
## ideation
Core difficulty: `A_i` are huge, so simulation is impossible. The key structural insight is that only the first move on each index changes `S`; all later moves on that index are just “passes.” The game is really about who is forced to open the `(N-1)`-th distinct index, because then the opponent opens the last one and wins immediately. Opened piles provide a pool of pass moves, and the parity/availability of those passes likely controls who must make the penultimate opening.

Leading hypothesis to validate: the answer depends mostly on `N` and the number of odd `A_i`, with small-`N` exceptions. A candidate rule emerging from hand analysis is:
- `N=1`: Fennec always.
- `N=2`: Snuke always.
- `N=3`: Fennec iff at least one `A_i` is odd.
- `N>=4`: Fennec iff the count of odd `A_i` is odd.
This matches the samples, but it is not proven yet and must be brute-force checked.

Important pitfalls: `A_i=1` opens an index but creates zero future passes, unlike larger odd values; even `A_i` create an odd number of post-opening passes; `N` parity alone is false; total sum parity alone is likely false; off-by-one around opening the `(N-1)`-th vs `N`-th index; pass availability when the opened pool is empty vs positive-even; don’t rely on sample-only reasoning.

## worker: Build a brute-force minimax solver with memoizatio
- Brute-force model: state is `(tuple(A), frozenset(S))`; a move chooses `i` with `A_i] > 0`, decrements it, inserts `i` into `S`, and if `|S| == N` the mover wins. Memoized minimax returns whether the player to move can force a win.
- Exhaustive comparison for tiny cases (`N <= 5`, `1 <= A_i <= 5`) against the rule below reported no mismatches:
  - `N = 1`: Fennec always wins.
  - `N = 2`: Snuke always wins.
  - `N = 3`: Fennec wins iff at least one `A_i` is odd.
  - `N >= 4`: Fennec wins iff the number of odd `A_i` is odd, equivalently `sum(A_i)` is odd.
- Key invariant: opening the `(N-1)`-th distinct index is losing, because the opponent immediately opens the last index and wins. Thus play is driven by parity of safe moves/pass availability; for `N >= 4` the even-valued piles contribute neutral pairs and only the parity of the count of odd piles matters.
