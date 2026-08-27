
## ideation
**Core difficulty**

We have N pieces on a number line. The operation chooses four consecutive pieces (by order) with coordinates `a < b < c < d`. Let `M = (a + d) / 2`. Then:
- The piece at `b` moves to `M + (M - b) = 2M - b = a + d - b`.
- The piece at `c` moves to `M - (c - M) = 2M - c = a + d - c`.

Let's verify the ordering after the move:
- `a + d - c`: Since `c < d`, `a + d - c > a`. Since `c > a`, `a + d - c < d`. Also compare with `b`: `a + d - c < a + d - b` because `c > b`. So `a + d - c < a + d - b`.
- `a + d - b`: Since `b > a`, `a + d - b < d`. Since `b < d`, `a + d - b > a`. So new `c` (at `a + d - c`) < new `b` (at `a + d - b`).

So after the operation the four pieces are at `a, a+d-c, a+d-b, d`.
The gaps become:
- Original gaps: `b-a`, `c-b`, `d-c`.
- New gaps: `(a+d-c) - a = d-c`, `a+d-b - (a+d-c) = c-b`, `d - (a+d-b) = b-a`.

So the operation **swaps the first and third gaps** while keeping the middle gap fixed. This is the key insight.

## worker: Implement the solution as described and verify wit
**Analysis of the operation:**

Given four consecutive pieces at positions `a < b < c < d`, the operation computes `M = (a+d)/2` and moves:
- the piece at `b` to `a + d - b`
- the piece at `c` to `a + d - c`

This results in new positions `a, a+d-c, a+d-b, d`. The gaps between consecutive pieces change from `(b-a, c-b, d-c)` to `(d-c, c-b, b-a)`. So **the first and third gaps are swapped, while the middle gap stays the same**.

**Key insight:** By performing a sequence of such operations (essentially adjacent swaps of gaps at even distance), we can independently permute all gaps at even indices (0,2,4,...) among themselves, and all gaps at odd indices (1,3,5,...) among themselves. This is a classic observation: the operation is equivalent to swapping the first and third elements in a 4-element window, which allows arbitrary permutations within each parity class.

**Optimization:** The sum of coordinates is:
$$\text{sum} = N \cdot X_0 + \sum_{i=0}^{N-2} (N-1-i) \cdot g_i$$
where `g_i` is the gap after piece `i`. The weights `(N-1-i)` are decreasing. To minimize the sum, we assign the **smallest** gap to the **largest** weight. Since weights decrease with index, we place smaller gaps at smaller indices. Given the parity constraint, we sort the even-indexed gaps ascending and assign them to positions 0, 2, 4, ...; and similarly for odd-indexed gaps to positions 1, 3, 5, ...

**Proof of reachability:** Any permutation of even-indexed gaps can be achieved by a sequence of the allowed operations. The operation swaps gaps at positions `i` and `i+2` (for `i` and `i+3` in the piece indexing). Repeated applications allow bubble-sort style sorting within each parity class.

**Complexity:** `O(N log N)` for sorting the two gap arrays, `O(N)` for the final sum computation. This easily handles `N` up to `2*10^5` and coordinates up to `10^12`.

**Verification with samples:**
- Sample 1: `N=4, X=[1,5,7,10]`. Gaps: `[4,2,3]`. Even gaps (indices 0,2): `[4,3]` sorted `[3,4]`. Odd gaps (index 1): `[2]`. Opt gaps: `[3,2,4]`. Sum = `4*1 + 3*3 + 2*2 + 1*4 = 4 + 9 + 4 + 4 = 21`. Matches.
- Sample 2: `N=6, X=[0,1,6,10,14,16]`. Gaps: `[1,5,4,4,2]`. Even gaps: `[1,4,2]` sorted `[1,2,4]`. Odd gaps: `[5,4]` sorted `[4,5]`. Opt gaps: `[1,4,2,5,4]`. Sum = `6*0 + 5*1 + 4*4 + 3*2 + 2*5 + 1*4 = 0+5+16+6+10+4 = 41`. Matches.
