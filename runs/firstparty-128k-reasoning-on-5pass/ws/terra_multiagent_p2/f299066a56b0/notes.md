
## ideation
The core difficulty is maximizing the number of disjoint pairs under the asymmetric condition “top size × 2 ≤ bottom size.” Since the sizes are already sorted, the problem is a structured bipartite matching problem: smaller mochi should serve as tops and larger ones as bottoms.

The supplied plan is valid. For a fixed target number of pairs K, it is sufficient to consider the smallest K mochi as candidate tops and seek K compatible bottoms among later mochi. A greedy left-to-right matching with the smallest currently compatible bottom is correct because using a larger bottom unnecessarily can only reduce future options. Feasibility is monotone in K, so binary search can find the maximum K.

However, binary search is not necessary. There is a direct O(N) two-pointer greedy algorithm that exploits the sorted sequence and achieves the optimum in one scan. This is preferable conceptually and asymptotically.

Important pitfalls:
- The required condition is A[top] ≤ A[bottom] / 2, which should be tested as 2 × A[top] ≤ A[bottom] using integers; avoid floating-point division.
- A mochi cannot be used in more than one pair.
- It is not always correct to simply compare arbitrary adjacent mochi or greedily pair every small item immediately without respecting the division between candidate tops and candidate bottoms.
- For a target K, bottoms must be selected so that they are distinct and come from positions not used as tops.
- Although 2 × A_i fits easily in typical integer ranges here, implementations in fixed-width languages should still use a sufficiently wide integer type.
