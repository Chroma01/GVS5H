
## ideation
The core difficulty is to characterize an optimal deletion order. Every deletion removes one nonempty monochromatic prefix, so after accounting for swaps, the original elements must be rearranged into a sequence of monochromatic blocks. The cost is the number of blocks plus the minimum adjacent-swap cost needed to realize that block order. Equal-valued elements must retain their relative order, while different values may be reordered at an inversion cost.

A useful abstraction is to assign each original element a block index. Elements with the same block index must have the same value, block indices must be nondecreasing within each value’s original occurrence order, and the number of distinct consecutive block groups is the deletion cost. The swap cost is the number of pairs whose relative order changes, with care taken that equal-valued pairs never contribute.

Potential formulations include dynamic programming over the last emitted value/block, incremental inversion counting, or reductions to weighted path/min-cost flow problems. The main pitfalls are that splitting occurrences of one value into multiple blocks may be beneficial, consecutive blocks of the same value should be merged, and simply counting inversions against a fixed value ordering is insufficient because the block ordering itself is part of the optimization.

## worker: Derive a complete polynomial-time optimization alg
Represent the sequence by maximal equal runs. Initially, deleting each run costs one operation, so the cost is the number of runs.

A useful swap is exactly a local pattern
\(x^p\,y\,x\,y^q\), where the two middle runs have length one. Swapping the middle \(y\) and \(x\) changes it to
\(x^{p+1}\,y^{q+1}\). Thus one swap costs 1, while the number of deletion operations decreases by 2, improving the total by 1.

All other adjacent swaps improve the run count by at most 1, so they cannot reduce the total cost and are unnecessary in an optimum. Therefore the problem reduces to maximizing the number of reductions of the above pattern.

The reduction is local and can be applied greedily with a stack. After each reduction, only the suffix can create a new reducible pattern, so repeatedly checking the stack suffix is sufficient. If the initial number of runs is \(R\) and the stack performs \(q\) reductions, the answer is \(R-q\).

The algorithm runs in \(O(N)\) per test case, with \(O(N)\) memory.
