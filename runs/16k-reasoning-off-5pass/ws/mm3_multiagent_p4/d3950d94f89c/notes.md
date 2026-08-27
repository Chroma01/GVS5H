
## ideation
**Core difficulty**  
- We need the longest downward path (ancestor → descendant) where all node values are distinct, measured by sum of edge lengths.  
- The path must be a *contiguous* segment on a root‑to‑node traversal (it cannot skip a node in between).  
- We also need the minimum number of nodes among all paths that achieve that maximum length.

## worker: Let `val = nums[node]`.
The solution uses a DFS from the root, maintaining a sliding window of unique values on the current path. The key insight is that for a downward path, all nodes are on the current root-to-node traversal, so we can maintain `start_depth` (the minimum valid depth) that ensures uniqueness.

`last_occ` tracks the most recent depth where each value appeared. When we encounter a duplicate, we push `start_depth` beyond the previous occurrence. We use `prefix_len[depth]` to get the total edge length from root to any depth in O(1).

Backtracking is handled by saving the old `start_depth` and removing the current node's value from `last_occ` after exploring its subtree.

## worker: Verify the solution with the two given examples an
The solution was originally sketched with a broken first DFS attempt (no backtracking of `start_depth`). I replaced it with a correct recursive DFS that:

* keeps a `prefix_len` array indexed by depth so we can compute any sub‑path length in O(1),
* uses a `last_occ` dictionary for the most recent depth of each value on the current root‑to‑node path,
* maintains `start_depth` as the leftmost depth allowed for a valid unique‑value segment, pushing it forward when a duplicate is encountered,
* carefully restores `start_depth` and removes the current value from `last_occ` on backtrack.

I added a small test harness at the bottom that runs the two examples from the prompt plus several edge cases (2‑node tree with unique/duplicate values, star with all duplicates, linear all‑unique, linear with an internal duplicate). All outputs match the expected answers, confirming correctness.
