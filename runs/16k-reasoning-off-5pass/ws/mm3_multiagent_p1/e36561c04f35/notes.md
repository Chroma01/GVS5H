
## ideation
**Problem restatement**  
We have an array `A` of length `N`. Two operations are allowed any number of times:
1. **Swap** the `i`‑th and `(i+1)`‑st elements (1‑based, `i < K`, where `K` is current length). Costs 1 operation.
2. **Delete** a prefix `1…i` such that all elements in that prefix are equal. Costs 1 operation.

Goal: empty the whole array with the minimum number of operations.

**Key observations**
- Deletions are only possible on a *homogeneous* prefix. Hence we must first create such a prefix (by swaps) and then delete it.
- The process can be viewed as repeatedly: bring some equal elements to the front (paying swaps equal to how many elements we move), then delete them.
- Because deletions only remove the front, elements that are further right become closer to the front after each deletion.
- The array values are bounded (`1…N`) but the exact bound is not crucial.

**Greedy/stack idea**  
Process the array from left to right while maintaining a stack of blocks. Each block represents a *consecutive* group of equal values that currently occupy the front of the *remaining* array.  
When we read the next value `v`:
- If the top of the stack already has value `v`, we just increase its count (that element naturally joins the top block after all deletions so far).
- Otherwise we push a new block `(v, 1)` on the stack – this new value is now at the front of the *unprocessed* part.

Whenever the top two blocks on the stack have the *same* value, we can merge them: take the lower block, swap each of its elements upward (cost = size of the lower block) so they become adjacent to the top block, then delete the whole merged block in one deletion operation.  
Thus we pop the second block, add its size to the top block’s size, and add that size to the answer (as the number of swaps needed). The deletion itself costs 1 operation, but because we eventually delete *every* element exactly once, the total number of deletions is exactly `N`. So the answer we compute (sum of all merged block sizes) is the total number of swaps; the minimal total operations = swaps + `N`.

**Why this is optimal**
- Any sequence of operations can be rearranged to: read array left‑to‑right, whenever a value equals the current front value we can keep it; when it differs we must pay at least one swap to bring a matching value (if any exists later) to the front, or we must eventually delete a mismatched value after bringing it to the front. The stack algorithm captures exactly the number of times a value is “lifted” over a block of different values.
- The merging step corresponds to eliminating a whole block of a value that appears later by moving it over the intervening different values. Any optimal solution must move that later block over the same number of different elements, incurring at least the same swap cost. Therefore the algorithm yields the minimum swaps.

## worker: Implement the solution: for each test case, comput
The algorithm processes the array left‑to‑right maintaining a stack of blocks of equal values that are at the front of the *remaining* part.  
When a new value `v` is read:  
- If it matches the top block, we just extend that block.  
- Otherwise we push a new block `(v, 1)`.  

Whenever the two top blocks have the same value, they can be merged: the lower block must be swapped upward (cost = its size) to join the top block, after which the whole block can be deleted in one operation. The total number of swaps is accumulated, and the final answer is `swaps + N` because each element is deleted exactly once (one operation per deletion). The approach is O(N) per test case and fits the constraints (total N ≤ 2·10⁵).
