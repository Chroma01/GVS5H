
## ideation
The core difficulty is balancing three independent vitamin totals under one shared calorie limit. Since every food belongs to exactly one vitamin type, the choices for the three types are disjoint, but their calorie costs compete globally. The objective is max-min, so a natural reformulation is: for a candidate target T, can we obtain at least T units of every vitamin within X calories?

The key monotonicity is that feasibility for T implies feasibility for every smaller target, enabling binary search. For each vitamin type, one can independently determine the minimum calories needed to obtain at least T units, or equivalently the maximum vitamin amount obtainable for each calorie budget. The three minimum costs can then be added because the corresponding food sets are disjoint.

Important pitfalls include treating the calorie bound as “exactly” rather than “at most,” accidentally reusing a food in a 0/1 knapsack transition, and using an unsafe upper bound for the binary search due to large A_i values. The answer can safely be zero when some vitamin cannot be obtained at all.

## worker: Implement the complete Python solution: partition 
For each vitamin type, a descending 0/1 knapsack computes the maximum vitamin intake obtainable for every calorie capacity. The minimum capacity achieving a target intake is found with `bisect_left`.

Because each food belongs to exactly one vitamin group, the target is feasible precisely when the three independently required capacities sum to at most `X`. Feasibility is monotone in the target, so binary search finds the maximum value.
