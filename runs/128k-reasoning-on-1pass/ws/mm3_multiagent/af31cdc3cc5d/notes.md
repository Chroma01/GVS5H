
## ideation
**Core difficulty**  
The operation “delete two adjacent numbers, gain |difference|” forces a *non‑crossing* perfect matching on the original indices (except possibly one left over when N is odd). Turning the process into a sign‑assignment problem (“+” for the larger element of each pair, “–” for the smaller) reduces the whole task to maximizing a sum of signed values under the balance constraint (equal number of + and –).  

**Key observations**  
1. Any valid sequence of deletions corresponds to a non‑crossing matching, which can be interpreted as a choice of signs for each position.  
2. For a fixed sign vector, the total score is simply Σ sign[i]·A[i].  
3. By the rearrangement inequality, to maximise this sum we should put “+” on the largest numbers and “–” on the smallest numbers.  
4. Such a sign vector can always be realized by repeatedly deleting an adjacent “+–” pair (a simple invariant: as long as counts are equal, an opposite adjacent pair exists).  
5. The optimal total score therefore equals:  
   \[
   \text{answer} = \bigl(\text{sum of }K\text{ largest}\bigr) - \bigl(\text{sum of }K\text{ smallest}\bigr),\qquad K = \left\lfloor\frac N2\right\rfloor .
   \]

**Candidate approaches**  
- **Sort + prefix/suffix sums** – sort the array once, compute the sum of the first K elements (smallest) and the last K elements (largest). O(N log N) time, O(N) memory.  
- **Quickselect / nth‑element** – find the K‑th smallest and split the sum without full sorting. O(N) average time, more complex but unnecessary given constraints.  
- **DP on intervals** – could model the problem as DP on intervals (optimal pairing of adjacent elements), but this is O(N²) and far too slow.  
- **Greedy with stack** – simulate deletions while maintaining current adjacent differences; may seem intuitive but does not guarantee optimality for arbitrary values.

**Pitfalls & edge cases**  
- **Odd N**: exactly one element remains and contributes nothing; ignore the middle element after sorting.  
- **Large sums**: each A_i ≤ 10⁹, N ≤ 3·10⁵, so total sum can be up to ~1.5·10¹⁴ – need 64‑bit integer (Python int is fine).  
- **Empty input** (should not happen per constraints) – guard against it.  
- **Fast I/O**: N up to 3·10⁵, use `sys.stdin.buffer` for speed.  
- **Correct indexing when K = 0** (N = 0 or 1) – answer must be 0.  
- **Understanding the “non‑crossing” property** – crucial for the sign‑assignment reduction; forgetting it could lead to an incorrect DP or greedy.

**Proof sketch (for later implementation)**  
- Show any feasible sequence ↔ non‑crossing matching ↔ sign vector with equal +/–.  
- Show optimal sign vector is “largest K → +, smallest K → –”.  
- Prove realizability: repeated deletion of any adjacent opposite sign pair works (invariant of equal counts).  
- Conclude the formula (2) is both an upper bound and achievable.

## worker: finalize
- The process of repeatedly deleting adjacent numbers corresponds to a non‑crossing matching of positions, which can be represented by a sign assignment (+ for the larger element of a pair, – for the smaller).  
- The total score equals the sum of `sign[i]·A[i]` with the number of `+1` equal to the number of `‑1` (⌊N/2⌋ each).  
- By the rearrangement inequality, the sum is maximised when the `+1` signs are placed on the largest numbers and `‑1` on the smallest numbers.  
- Such a sign vector can always be realised: as long as equal numbers of `+` and `‑` remain, an adjacent opposite pair exists and can be deleted, preserving the counts.  
- Therefore the optimal total score is  
  \[
  \text{answer} = \bigl(\text{sum of K largest}\bigr) - \bigl(\text{sum of K smallest}\bigr),\quad K = \lfloor N/2\rfloor .
  \]  
- The algorithm sorts the array, computes the two sums, and outputs their difference.  
- Complexity: sorting `O(N log N)`, memory `O(N)`.  
- Edge cases (odd `N`, `K = 0`) are handled automatically.
