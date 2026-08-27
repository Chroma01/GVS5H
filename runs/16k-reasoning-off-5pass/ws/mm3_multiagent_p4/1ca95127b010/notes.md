
## ideation
The problem asks whether we can transform binary string S into T using two local “swap” operations that exchange a block of X zeros followed by Y ones with Y ones followed by X zeros (i.e. rotate a contiguous block of length X+Y by X positions). Both operations are inverses of each other and preserve the total number of 1s.

Key observations:
- The total count of ‘1’s in S and T must be equal; otherwise it is impossible.
- Define prefix difference `pref[i] = (number of 1s in S[0..i)) - (number of 1s in T[0..i))`. This represents how many 1s are “too early” at each position.
- Operation A takes a pattern `0^X 1^Y` and turns it into `1^Y 0^X`. In terms of prefix difference, this moves a block of X units of excess 1s rightward by `X+Y` positions (or equivalently moves Y units of excess 0s leftward by `X+Y`).
- Thus the operations allow us to shift excess 1s to the right in steps of size `d = X+Y`. They never move excess leftwards.
- Therefore, a solution exists iff:
  1. For every prefix, `pref[i] >= 0` (we never have a deficit that needs to be moved left, which is impossible).
  2. For each residue class modulo `d`, the net excess at the end of the string is zero (i.e., the last prefix for that residue is 0). Because excess can only move by multiples of `d`, excess in a given residue class can only be cleared within that class.
- These conditions can be checked in O(N) time by maintaining running sums and tracking the minimum prefix difference per residue class.

Plan to implement:
- Read N, X, Y, strings S, T.
- Compute total ones in S and T. If unequal → print “No”.
- Compute prefix differences.
- Group indices by `i % d`. For each residue, track:
  - The minimum prefix value (must be >= 0).
  - The final prefix value at the end (i = N) (must be 0).
- If all residues satisfy these, print “Yes”, else “No”.

## worker: (omitted)
The reasoning follows the plan. The prefix difference `pref[i]` counts excess 1's up to position i. The operations allow shifting excess right by `d = X+Y`. Therefore a necessary and sufficient condition is that for each residue modulo `d`, the minimum prefix difference is non‑negative and the total excess is zero (the latter is already guaranteed by equal counts of 1's). We compute prefix differences in one pass, tracking the minimum per residue.
