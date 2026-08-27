
## ideation
The problem is a classic DP over a string with a “run length ≥ 3” constraint.  
For each position we can change the character to any letter at a cost equal to the alphabet distance, because each unit step costs 1.  
We need the minimum total cost to obtain a good caption, and among all optimal captions the lexicographically smallest one.  
If the length `n` is 1 or 2 it is impossible, otherwise a solution always exists (a single block of length `n` works).

**Key observations**
* The target string consists of blocks of equal letters, each block length at least 3.  
* The cost of changing `caption[i]` to a target letter `c` is `|caption[i] - c|`.  
* A state can be described by `(position, current letter, current run length)`.  
  The run length can be capped at 3 because any longer run behaves the same for the constraints.  
* We compute a backward DP `g[i][c][len]` = minimal cost to finish the suffix `i … n‑1` given that position `i` already has letter `c` and the current run length (including `i`) is `len` (1, 2 or ≥ 3).  
  The recurrence is:
  * `continue` – keep the same letter `c` at `i+1`, the new run length becomes `min(len+1, 3)`.
  * `end` – only possible if `len == 3` (run already ≥ 3). Start a new block with any `c' ≠ c` of length 1.
* The optimal total cost is `min_c g[0][c][1]` (the first character starts a new block of length 1).  
* To obtain the lexicographically smallest optimal string we reconstruct greedily from left to right.  
  At each step we try the 26 letters in increasing order, simulate the transition, and check whether the total cost (already accumulated prefix cost + cost of the current character + the optimal suffix cost computed from `g`) equals the global optimum.  
  The first feasible letter is taken, guaranteeing the smallest possible prefix.

## worker: *Cost table**: Compute `cost[i][c] = abs(ord(capti
The solution uses a suffix dynamic programming with a small state (position, current character, capped run length 1/2/3).  
For each position we compute the minimal cost to finish the remaining string given the current run length.  
The transition handles two possibilities at a step: continue the same block (run length increases, capped at 3) or, only when the current run already has length 3, start a new block of a different character.  
The cost of changing a character to any target is the absolute alphabet distance, matching the problem’s operation cost.  

After computing the DP we obtain the global minimum cost `total_cost`.  
To recover the lexicographically smallest optimal caption we greedily scan the string from left to right. At each position we try characters in increasing order and keep the first one that can still reach the optimal total cost according to the pre‑computed suffix DP. This yields the lexicographically smallest string among all optimal solutions.  

The algorithm runs in O(n·26) time (≈ 1.3 · 10⁶ operations for n = 5·10⁴) and uses O(n·26·3) memory for the DP table, which fits easily in the limits.

## worker: Correct the DP recurrence to a forward DP (left‑to
- The forward DP computes the minimal cost in O(n·26) time using two rows and pre‑computed minima for the “change” transition.
- The suffix DP (backward pass) is used for reconstruction; it also runs in O(n·26) time.
- Greedy left‑to‑right reconstruction with the suffix DP guarantees the lexicographically smallest optimal caption.
- The algorithm handles n < 3 by returning an empty string, and always finds a solution for n ≥ 3.

## worker: Test the solution on the provided examples and add
I implemented the DP solution as described in the plan, then added a brute‑force enumerator for small `n` (≤ 9) to verify correctness. The brute‑force method enumerates all possible good captions by generating all partitions of `n` into parts ≥ 3 and trying all 26‑letter assignments for each block, computing the total cost and keeping the lexicographically smallest optimal string. I tested the solution on the three provided examples, several hand‑crafted edge cases (including n=3,4,5,6 with multiple optimal strings), and a series of random strings for each length from 3 to 9. In all cases the DP output matched the brute‑force result, confirming that the algorithm returns the minimal‑cost caption and, when several optimal captions exist, the lexicographically smallest one. The solution also correctly returns an empty string for n < 3.
