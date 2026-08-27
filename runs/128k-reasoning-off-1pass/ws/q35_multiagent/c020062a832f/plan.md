1. **Initial Calculation**: Compute the inversion number for $k=0$ (where $B_i = A_i$) using a standard $O(N \log N)$ method (e.g., Merge Sort or Fenwick Tree/BIT).
2. **Transition Analysis**: When moving from $k$ to $k+1$, each $B_i$ becomes $(A_i + k + 1) \pmod M$. This is equivalent to adding 1 to each element, and if an element was $M-1$, it wraps around to 0.
3. **Effect of Wrap-around**: An element $A_i$ wraps around from $M-1$ to $0$ when $k+1 = M - A_i$. Let's call this "wrap event". When an element $x$ wraps to 0, it effectively moves from being the largest value to the smallest.
4. **Change in Inversions**: 
   - For any pair $(i, j)$ with $i < j$:
     - If neither wraps, their relative order doesn't change because both increase by 1.
     - If both wrap, their relative order doesn't change.
     - If only $A_i$ wraps (so $B_i$ becomes 0) and $A_j$ doesn't (so $B_j$ becomes $A_j+1 > 0$), then previously $A_i = M-1$ and $A_j < M-1$, so $A_i > A_j$ (inversion). After wrap, $0 < A_j+1$, so no inversion. We lose 1 inversion.
     - If only $A_j$ wraps and $A_i$ doesn't, previously $A_i < M-1 = A_j$, so no inversion. After wrap, $A_i+1 > 0$, so $B_i > B_j$ (new inversion). We gain 1 inversion.
   - So, for each step $k \to k+1$, the change in inversion count is:
     $\Delta = (\text{count of } j > i \text{ where } A_j \text{ wraps and } A_i \text{ doesn't}) - (\text{count of } i < j \text{ where } A_i \text{ wraps and } A_j \text{ doesn't})$.
   - Actually, it's easier to think globally: When all elements that are currently $M-1$ wrap to 0, they were greater than all non-wrapping elements. After wrapping, they are smaller than all non-wrapping elements.
   - Let $W$ be the set of indices that wrap at this step. Let $S$ be the set of indices that don't.
   - Pairs within $W$: relative order unchanged.
   - Pairs within $S$: relative order unchanged.
   - Pairs $(i, j)$ with $i \in W, j \in S$: Previously $B_i = M-1 > B_j$. Now $B_i = 0 < B_j$. So all such pairs lose their inversion status. Count = number of pairs $(i, j)$ with $i < j$, $i \in W, j \in S$.
   - Pairs $(i, j)$ with $i \in S, j \in W$: Previously $B_i < M-1 = B_j$. Now $B_i > 0 = B_j$. So all such pairs gain an inversion. Count = number of pairs $(i, j)$ with $i < j$, $i \in S, j \in W$.
   - Net change = (Count of $i \in S, j \in W, i < j$) - (Count of $i \in W, j \in S, i < j$).
5. **Efficient Update**: We can precompute the "wrap time" for each element: $t_i = M - A_i$ if $A_i > 0$, else $t_i = M$ (since $A_i=0$ wraps at $k=M-1 \to k=0$? No, $A_i=0$ becomes $1$ at $k=1$. It wraps when $A_i+k = M \Rightarrow k=M$. But $k$ goes $0 \dots M-1$. So $A_i=0$ never wraps in the range $k=0 \dots M-1$? Wait. $B_i = (A_i+k) \pmod M$. If $A_i=0$, $B_i = k$. It wraps when $k$ goes from $M-1$ to $M$? But we stop at $k=M-1$. So $A_i=0$ never wraps. Generally, $A_i$ wraps when $A_i + k \ge M \Rightarrow k \ge M - A_i$. The first wrap is at $k = M - A_i$. If $A_i=0$, $k=M$, which is outside our range. So only $A_i > 0$ wrap.
   - We can process the steps $k=0 \to M-1$. At each step, we identify which elements wrap. We can use a Fenwick tree to maintain the positions of elements. Initially, all elements are in the BIT. When an element wraps, we remove it from the BIT? No, we need to count pairs.
   - Alternative: Precompute for each $k$, the set of wrapping indices. Use a BIT to count how many non-wrapping elements are to the left/right of wrapping elements.
   - Actually, we can compute the initial inversion count. Then for each $k$ from $0$ to $M-2$, we transition to $k+1$. The elements that wrap are those with $A_i = M - 1 - k$. We can group indices by their wrap value.
   - Let's store indices by $A_i$. For each value $v \in [1, M-1]$, the elements with $A_i=v$ wrap at $k = M-v$.
   - We iterate $k$ from $0$ to $M-1$. At step $k$, we calculate the answer. Then we prepare for $k+1$ by handling all elements with $A_i = M - 1 - k$ (if $k < M-1$).
   - To efficiently calculate the change, we can use a BIT that stores the positions of the "active" (non-wrapped) elements? No, all elements are always present, just their values change.
   - The change formula: $\Delta = \sum_{j \in W} (\text{# } i < j, i \notin W) - \sum_{i \in W} (\text{# } j > i, j \notin W)$.
   - Let $L_j$ be the number of non-wrapping elements to the left of $j$. Let $R_i$ be the number of non-wrapping elements to the right of $i$.
   - $\Delta = \sum_{j \in W} L_j - \sum_{i \in W} R_i$.
   - We can maintain a BIT of all indices $1 \dots N$. Initially, all are "non-wrapping". When an element wraps, it is still in the sequence, but for the purpose of the *transition*, we treat it as wrapping. The "non-wrapping" set is $S$.
   - We can pre-calculate the total number of non-wrapping elements $|S| = N - |W|$.
   - For each $j \in W$, $L_j = (\text{number of elements in } S \text{ with index } < j)$. This can be computed if we have a BIT of indices in $S$.
   - Algorithm:
     1. Compute initial inversions for $k=0$.
     2. Create a list `wrappers[v]` = list of indices $i$ such that $A_i = v$.
     3. Initialize a BIT with all indices $1 \dots N$ marked as 1.
     4. For $k = 0$ to $M-1$:
        - Print current inversion count.
        - If $k < M-1$:
          - Let $v = M - 1 - k$. These are the elements that will wrap when moving to $k+1$.
          - Let $W$ be the list of indices with $A_i = v$.
          - For each $j \in W$:
            - $L_j = \text{query\_bit}(j-1)$ (count of active/non-wrapping elements to the left).
            - $R_j = (\text{total active}) - \text{query\_bit}(j)$ (count of active/non-wrapping elements to the right).
            - Add $L_j$ to `gain`, subtract $R_j$ from `gain`? No.
            - $\Delta += L_j - R_j$.
          - Update inversion count: $inv += \Delta$.
          - Remove all $j \in W$ from the BIT (update position $j$ with -1).