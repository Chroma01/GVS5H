
## ideation
The core difficulty is that the target frequency is shared by every retained letter, while the one-way character-change operation couples neighboring letters. A frequency-only edit-distance calculation is insufficient: changing a character from letter \(i\) to \(i+1\) can be cheaper than deleting and reinserting it, but changes across multiple alphabet positions must be compared against deletion plus insertion. The no-wrap rule at `z` is another boundary condition.

For a fixed positive frequency \(k\), each letter’s target count is either \(0\) or \(k\). The main task is therefore to choose which letters are retained while accounting for possible forward transfers between adjacent letters. The empty-string interpretation should be handled separately if it is considered good.

## worker: Derive and validate the fixed-\(k\) chain DP, incl
For a fixed positive target frequency `k`, each letter must end with either `0` or `k` occurrences.

For a chosen target count `x_i` at letter `i`, define:

```text
d_i = original_count_i - x_i
```

Without character changes, the cost is `|d_i|`: surplus characters are deleted and deficits are filled by insertions.

A direct change from letter `i` to `i+1` can replace one deletion at `i` and one insertion at `i+1`, saving exactly one operation. Therefore, the maximum useful transfer across this edge is:

```text
min(max(d_i, 0), max(-d_{i+1}, 0))
```

Transfers across two or more alphabet positions cost at least as much as deleting and reinserting, so they never improve the optimum. Also, a letter cannot simultaneously have surplus and deficit, so useful transfers on adjacent edges do not conflict. Thus the total cost for a fixed target assignment is the sum of individual absolute differences minus the edge savings.

The target choice for each letter has only two states (`0` or `k`), so a two-state dynamic program over the 26-letter chain evaluates each `k` in constant time. Enumerating `k = 1..n` gives `O(26n)` time and `O(1)` extra space. Deleting every character is included as the fallback cost `n`.

## worker: Exhaustively validate the fixed-\(k\) DP against a
For a fixed common positive frequency `k`, every letter must end with either `0` or `k` occurrences. The DP chooses one of these two targets independently for each letter while processing the alphabet from left to right.

For a chosen target count, `abs(original - target)` is the cost using only deletions and insertions. Changing one letter to its immediate successor can replace one deletion and one insertion, saving one operation exactly when the source has surplus and the destination has deficit. Changes across two or more alphabet positions are never better than deleting and reinserting, so only adjacent transfers need to be considered.

The two DP states represent target frequency `0` and `k` for the current letter. Enumerating all `k` from `1` through `n` gives `O(26n)` time and `O(1)` extra space. The answer is initialized to `n` to cover deleting the entire string.

## worker: Exhaustively validate the implementation against a
The fixed-frequency DP was checked against exhaustive shortest-path reasoning on small strings, including repeated letters, strings involving `z`, and cases where changing a character is cheaper than deleting and inserting.

For a fixed common frequency `k`, each letter's final count is either `0` or `k`. The base cost for a chosen target count is the absolute count discrepancy. A useful change can only move one surplus character from letter `i` to a deficit at letter `i+1`, saving one operation compared with deletion plus insertion. Transfers over multiple alphabet positions are never cheaper, so adjacent transfers suffice.

The two DP states represent whether the current letter has target count `0` or `k`. The transition subtracts the maximum possible saving from a surplus at the previous letter and a deficit at the current letter. All `k` from `1` through `n` are tested, with deleting the entire input handled as an upper-bound fallback.

Complexity: `O(26 * n)` time and `O(1)` extra space.
