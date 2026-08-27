1. **Understand the Alkane Structure**: An alkane is a tree where every vertex has degree 1 or 4, with at least one degree-4 vertex. In the subgraph, the degrees are constrained by the original tree's structure. We need to find the largest such subgraph.

2. **Key Insight**: Since the subgraph must be a tree and every node has degree 1 or 4, we can think of this as selecting a subtree where internal nodes have exactly 4 children (in a rooted sense) or degree 4, and leaves have degree 1. This is similar to finding a "4-ary" tree structure within the given tree.

3. **Dynamic Programming on Trees**: We can use DP on trees. For each node, we compute the maximum size of an alkane-like structure rooted at that node, considering different states based on how many "branches" are connected to it. Specifically, we need to track how many children are attached to form degree 4.

4. **State Definition**: For each node u, define dp[u][k] as the maximum number of vertices in a valid partial structure rooted at u, where u has exactly k connections to its children in the subgraph (so the total degree of u in the subgraph is k, plus possibly one connection to its parent). We need k to be 0, 1, 2, 3, or 4. However, since the final alkane requires degree 1 or 4, we need to be careful:
   - If u is a leaf in the alkane, it has degree 1 (connected to parent only, so k=0 in child connections).
   - If u is an internal node, it must have degree 4. If u is connected to its parent, it needs 3 children (k=3). If u is the root of the alkane, it needs 4 children (k=4).

5. **DP Transitions**: For each node, we compute dp[u][k] for k=0,1,2,3,4. We sort the children's contributions and use a knapsack-like approach to select the best k children. The base case is a leaf: dp[u][0] = 1, and dp[u][k] = -infinity for k>0.

6. **Final Answer**: The answer is the maximum over all nodes u of:
   - dp[u][4] (u is the root of the alkane, degree 4)
   - dp[u][3] + 1 (u is connected to parent, so total degree 4, and we add the parent's contribution? No, we need to be careful. Actually, if u is not the root, it needs degree 4, which means 3 children and 1 parent. So dp[u][3] represents the size of the subtree rooted at u with 3 children. The total alkane including the parent would be computed when processing the parent. So we just take max(dp[u][4]) for all u as potential roots, and also consider that an alkane might not have a single root in the traditional sense. Actually, any alkane has a root if we root it arbitrarily. So we can root the entire tree at vertex 1 and then:
     - For each node u, if it serves as the root of an alkane subgraph, the size is dp[u][4].
     - But wait, the alkane subgraph might not include the root of the original tree. So we need to consider all possible roots. By rooting the original tree at 1, we can compute dp for all nodes. The maximum alkane size is max over all u of dp[u][4]. However, we also need to ensure that the alkane has at least one degree-4 vertex. Since dp[u][4] implies u has degree 4, this condition is satisfied.

7. **Edge Cases**: If no alkane exists, output -1.