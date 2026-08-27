- **Bottleneck characterization:** \(f(x,y)\leq w\) exactly when \(x\) and \(y\) are connected using only edges of weight at most \(w\). Thus, Kruskal's process describes the first threshold at which every pair becomes feasible.

- **Component balance:** For each DSU component, maintain `balance = number of unmatched A occurrences - number of unmatched B occurrences` after optimally matching all occurrences that can be matched at smaller thresholds. Positive balance means unmatched A occurrences; negative balance means unmatched B occurrences.

- **Merge operation:** When two components merge through an edge of weight \(w\), only opposite residuals from the two components can form newly available pairs. Their count is `min(positive_balance, negative_balance)`, and every such pair has bottleneck value exactly \(w\). Add this count multiplied by \(w\), then store the summed balance.

- **Optimality:** Before a merge, all pairs between the two components require threshold at least \(w\), while all already matched pairs have smaller or equal thresholds. Matching as many opposite residuals as possible at the first threshold where they become connected is exchange-optimal; postponing any of these matches cannot reduce their cost and can only replace them with pairs of threshold at least \(w\).

- **Equal weights:** Arbitrary ordering of edges with the same weight is harmless. Within one equal-weight connected region, each merge contributes
  \[
  \frac{|d_1|+|d_2|-|d_1+d_2|}{2}
  \]
  new matches, where \(d_1,d_2\) are component balances. These contributions telescope to a quantity depending only on the final components, so their total is independent of merge order.

- **Complexity:** Sorting takes \(O(M\log M)\); all DSU operations take \(O(M\alpha(N))\). The answer uses Python integers, safely covering 64-bit requirements.
