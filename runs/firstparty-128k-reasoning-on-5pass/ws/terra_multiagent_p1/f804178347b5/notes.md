- **Tree DP model:** Repeated majority-of-three operations form a complete ternary tree. Original string characters are leaves, and the final output is the root value.
- **DP state:** For every subtree store `(cost0, cost1)`, where `costb` is the minimum number of leaf flips needed to make that subtree evaluate to bit `b`.
- **Leaf initialization:** A leaf containing `0` has costs `(0, 1)`, while a leaf containing `1` has costs `(1, 0)`.
- **Majority transition:** To force an internal node to bit `b`, at least two of its three children must be forced to `b`. For child costs `x, y, z`, take the minimum over choosing each pair to become `b`; the third child uses its cheaper output:
  `min(x[b]+y[b]+min(z), x[b]+z[b]+min(y), y[b]+z[b]+min(x))`.
- **Answer:** At the root exactly one forcing cost is zero, corresponding to the current final bit. Print the other cost.
- **Complexity:** Each tree node is processed once. Time is `O(3^N)` and memory is `O(3^N)`, feasible for `N <= 13`.
