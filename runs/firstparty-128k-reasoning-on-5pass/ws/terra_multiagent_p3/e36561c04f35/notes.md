- **Run formulation:** Compress the sequence into maximal equal runs. If there are initially `R` runs, deleting every run separately costs `R` operations.

- **Useful swap:** A swap gives a net improvement exactly for four consecutive runs `X^p, Y, X, Y^q`, where the two middle runs are singletons. Swapping the middle `Y, X` yields `X^(p+1), Y^(q+1)`, reducing the run count by two for one swap, hence saving one total operation.

- **Optimal answer:** Swaps that reduce the number of runs by at most one cannot improve the final operation count, because their swap cost is at least the deletion operations they save. Thus the answer is initial run count minus the maximum number of profitable reductions.

- **Greedy selection:** Always applying the leftmost currently reducible four-run window is optimal. Overlapping reductions occur only in alternating local patterns; selecting the leftmost one can be exchanged with another valid selection without reducing the number of eventual reductions.

- **Data structure:** Each run is a node in a doubly linked list. A reduction starting at `x` removes its next two nodes and joins `x` to the fourth node. The endpoint run sizes both increase by one.

- **Candidate maintenance:** After a reduction, only starts at `x`, the three predecessors of `x`, and the new right neighbor can have changed reducibility. A min-heap lazily selects the leftmost valid candidate.

- **Complexity:** Run compression is `O(N)`. Each reduction removes two nodes and causes only `O(1)` candidate checks and heap insertions. Total time is `O(N log N)` per aggregate input and memory is `O(N)`. Since total `N` is at most `2e5`, this meets the limits.

- **Edge cases:** All elements equal gives one run and answer `1`. All distinct gives `N` runs and no profitable reduction, so answer `N`. Arrays with no eligible singleton middle runs also return their run count. Lazy heap entries are revalidated before use.
