- **Batch structure:** Once the current first active element has value `x`, any deletion operation must remove a prefix consisting only of `x`. Therefore, the `x` elements removed in that operation form a prefix of the currently active occurrences of `x`.

- **Incremental cost:** Let `p` be the first active position and let `q` be a later active occurrence of the same value. Moving `q` into the current prefix requires swapping it across every active non-`x` element between `p` and `q`. Previously selected `x` elements are not foreign.

- **Greedy condition:** If `d` is the number of active foreign elements between `p` and `q`, extending the batch costs `d` swaps but saves one deletion operation. The net change is `d - 1`. Hence occurrences with `d <= 1` are included, while an occurrence with `d > 1` is postponed.

- **Exchange argument:** When `d > 1`, taking the occurrence immediately costs at least two swaps for only one saved deletion. Postponing it cannot hurt, because foreign elements can be deleted first and may reduce its later crossing cost. When `d <= 1`, taking it immediately is never worse; for `d = 1` the two choices tie.

- **Fenwick tree:** The tree stores which original positions remain active. It supports finding the first active position, testing whether an occurrence is active, counting active positions in an interval, and deleting all elements selected for a batch.

- **Implementation detail:** The selected positions remain marked active until the whole batch is finalized. Their count is subtracted from the interval total to obtain the number of foreign elements.

- **Validation:** Exhaustive shortest-path comparisons on short sequences confirm the recurrence, including all-distinct sequences, equal runs, repeated alternating values, and cases where previously deleted elements change later gaps.

- **Complexity:** Each occurrence is advanced through its value list at most once, and every Fenwick operation costs `O(log N)`. Total complexity is `O((sum N) log N)` with `O(N)` memory per test case.
