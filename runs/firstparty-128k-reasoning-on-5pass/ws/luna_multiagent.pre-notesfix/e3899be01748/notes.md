
## ideation
The core difficulty is that the divisor changes with the ending digit, while leading zeros must remain part of the numerical value of each substring. A zero ending digit contributes nothing, so only positions ending in digits 1 through 9 should be queried. The answer can be quadratic, so the solution must aggregate many substrings with the same remainder rather than inspect them individually. The maximum answer is on the order of \(n^2\), so implementations in fixed-width languages need 64-bit counting.

## worker: Implement the rolling remainder DP independently f
For each modulus `d` from 1 through 9, the DP stores counts of remainders of all substrings ending at the previous position. Appending digit `x` changes remainder `r` to `(10*r+x) % d`; the one-digit substring is added separately, so leading zeros and singleton substrings are handled correctly.

When the current final digit equals `d`, every substring counted in remainder zero is divisible by its non-zero last digit, so its count is added to the answer. Substrings ending in zero are never queried, as required.

The complexity is `O(45n) = O(n)` time and `O(45) = O(1)` auxiliary space. The implementation returns the examples' results: 11, 18, and 25.
