
## ideation
The problem requires computing $\sum_{L,R} f(L,R)$, where $f(L,R)$ is the minimum number of operations to erase the subarray $A[L \dots R]$. The operation allows erasing a contiguous range of values present on the blackboard. This is equivalent to finding the number of connected components in the set of values present in the subarray, where connectivity is defined by $|x-y|=1$.

Let $S_{L,R}$ be the set of distinct values in $A[L \dots R]$. The number of connected components is $|S_{L,R}| - \sum_{v} \mathbb{I}(v \in S_{L,R} \land v-1 \in S_{L,R})$.
Thus, we need to compute:
1. $\sum_{L,R} |S_{L,R}|$: This is the sum of the number of distinct elements in all subarrays. We can compute this by summing the contribution of each element $A_i$ as the first occurrence of its value in the subarray. For each $i$, the number of subarrays where $A_i$ is the first occurrence is $(i - \text{prev\_occ}(A_i)) \times (N - i + 1)$.
2. $\sum_{L,R} \sum_{v} \mathbb{I}(v \in S_{L,R} \land v-1 \in S_{L,R})$: This counts the number of pairs $(L,R)$ such that both $v$ and $v-1$ are present. For a fixed $R$, the condition that both are present is $L \le \min(\text{last\_occ}_R(v), \text{last\_occ}_R(v-1))$. We can maintain the sum of these minimums efficiently as we iterate $R$ from 1 to $N$. When $A[R]$ is processed, only terms involving $v=A[R]$ and $v=A[R]+1$ change, allowing $O(1)$ update.

Total complexity is $O(N)$.

## worker: (none)
The solution uses the formula: number of connected components = |S| - Σ_v I(v ∈ S ∧ v-1 ∈ S).

**Part 1** (sum of distinct elements): For each position i, A[i] contributes to |S_{L,R}| when it's the first occurrence of its value in the subarray. This happens for L ∈ (prev_occ(A[i]), i] and R ∈ [i, N], giving (i - prev_occ) × (N - i + 1) subarrays.

**Part 2** (sum of adjacent pairs): For fixed R, the number of L's where both v and v-1 are present equals min(last_occ_R(v), last_occ_R(v-1)). As we iterate R, only last_occ(A[R]) changes, affecting exactly two terms in the sum: min(last_occ(val), last_occ(val-1)) and min(last_occ(val+1), last_occ(val)). This allows O(1) updates per step.

Total time: O(N), space: O(N).
