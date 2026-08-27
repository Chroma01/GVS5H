
## ideation
The core difficulty is that changing one leaf can alter several majority decisions along its path, while changing a subtree’s resulting bit may require different numbers of leaf edits depending on its current contents. The natural state for each subtree is therefore the minimum edit cost needed to force its output to 0 or to 1. At a ternary node, the desired output requires at least two of the three child outputs to equal that bit, so the combination must consider all valid child-output patterns, not merely the original majority.

The tree has \(3^N\) leaves and \(O(3^N)\) total nodes, which is feasible for \(N \leq 13\). Costs can be kept as small integers, and the final answer is the cost of forcing the root to the bit opposite its unmodified output.

Potential pitfalls include grouping the input from the correct side, distinguishing “cost to force output 0/1” from the child’s original output, and ensuring that the parent combination permits either all three children or exactly two children to have the desired value. An incorrect shortcut that always chooses only two children can fail when the cheapest valid configuration uses all three.

## worker: Implement and verify the bottom-up ternary-tree DP
For every subtree, `cost0` and `cost1` store the minimum number of leaf changes needed to make its majority result equal to `0` or `1`.

At each ternary node, all eight combinations of child results are considered. Combinations with at least two zeroes determine result `0`, while those with at least two ones determine result `1`. The DP is computed bottom-up for `N` levels, using `O(3^N)` time and memory.

The root’s unchanged result is identified by whichever root cost is zero; the answer is the cost of forcing the opposite result.
