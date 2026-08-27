
## ideation
The core difficulty lies in efficiently computing the inversion number for $M$ different shifts of the array $A$, where $N$ and $M$ are up to $2 \times 10^5$. A naive $O(N^2)$ or even $O(N \log N)$ per query approach would be too slow ($O(MN \log N)$).

The key insight is that the transition from $k$ to $k+1$ involves adding 1 to all elements modulo $M$. This operation only changes the relative order of pairs where one element wraps around from $M-1$ to $0$ and the other does not.
- Pairs where neither element wraps: relative order unchanged.
- Pairs where both elements wrap: both become 0, relative order unchanged (equal).
- Pairs where $A_i = M-1$ (wraps) and $A_j < M-1$ (doesn't wrap) with $i < j$:
  - Original: $A_i > A_j$ (inversion).
  - New: $0 < A_j+1$ (not an inversion).
  - Change: -1.
- Pairs where $A_i < M-1$ (doesn't wrap) and $A_j = M-1$ (wraps) with $i < j$:
  - Original: $A_i < A_j$ (not an inversion).
  - New: $A_i+1 > 0$ (inversion).
  - Change: +1.

Thus, the change in inversion count $\Delta$ when moving from $k$ to $k+1$ is:
$\Delta = (\text{# pairs } (i,j) \text{ with } i<j, A_i < M-1, A_j = M-1) - (\text{# pairs } (i,j) \text{ with } i<j, A_i = M-1, A_j < M-1)$.

This $\Delta$ is constant for all $k$ because the set of indices where $A_i = M-1$ doesn't change (only their values change, but the condition "is $M-1$" refers to the original value $A_i$ before the shift $k$ is applied? No, wait.
Let's re-read carefully.
$B_i = (A_i + k) \pmod M$.
When we go from $k$ to $k+1$, $B_i$ becomes $(B_i + 1) \pmod M$.
An element "wraps" in this step if its current value $B_i$ is $M-1$.
$B_i = M-1 \iff (A_i + k) \pmod M = M-1 \iff A_i + k \equiv -1 \pmod M \iff A_i \equiv -1 - k \pmod M$.
So the set of indices that wrap depends on $k$. The delta is NOT constant.

My previous plan was flawed. The set of wrapping elements changes with $k$.
However, notice that as $k$ increments, the "threshold" for wrapping shifts.
Specifically, an element $A_i$ wraps at step $k \to k+1$ if $A_i + k \equiv M-1 \pmod M$, i.e., $A_i \equiv M-1-k \pmod M$.
Let $target = (M - 1 - k) \pmod M$. The elements that wrap are those with $A_i = target$.
Let $S$ be the set of indices $i$ where $A_i = target$.
The change $\Delta_k$ is:
$\Delta_k = (\sum_{j \in S} (\text{count of } i < j \text{ with } A_i \neq target)) - (\sum_{i \in S} (\text{count of } j > i \text{ with } A_j \neq target))$.

Let $C_v$ be the count of value $v$ in $A$.
Let $Pos_v$ be the sorted list of indices where $A_i = v$.
For a value $v$, let $W = Pos_v$.
Term 1: For each $j \in W$, count $i < j$ with $A_i \neq v$. This is $j - (\text{number of elements in } W \text{ before } j)$.
Term 2: For each $i \in W$, count $j > i$ with $A_j \neq v$. This is $(N - 1 - i) - (\text{number of elements in } W \text{ after } i)$.

We can precompute the contribution of each value $v$ to the delta.
Let $Add_v$ be the term 1 sum for value $v$.
Let $Sub_v$ be the term 2 sum for value $v$.
Then $\Delta_k = Add_{target} - Sub_{target}$, where $target = (M - 1 - k) \pmod M$.

Algorithm:
1. Compute initial inversion count for $k=0$ using BIT/Fenwick Tree. $O(N \log N)$.
2. Group indices by value $A_i$. Store sorted lists of positions for each value $0 \dots M-1$.
3. For each value $v \in 0 \dots M-1$:
   - Compute $Add_v$: Sum over $j \in Pos_v$ of $(j - \text{rank of } j \text{ in } Pos_v)$.
   - Compute $Sub_v$: Sum over $i \in Pos_v$ of $((N - 1 - i) - \text{rank of } i \text{ in } Pos_v \text{ from end})$.
   - Store $\Delta_v = Add_v - Sub_v$.
4. Iterate $k$ from $0$ to $M-1$:
   - Print current inversion count.
   - Update inversion count: $inv = inv + \Delta_{(M - 1 - k) \pmod M}$.
     - Note: The transition is from $k$ to $k+1$. The problem asks for $k=0, \dots, M-1$.
     - After printing for $k$, we prepare for $k+1$. The change from state $k$ to $k+1$ depends on which elements wrap when we add 1.
     - Elements wrapping are those with $A_i + k \equiv M-1 \pmod M \implies A_i \equiv M-1-k \pmod M$.
     - So we add $\Delta_{(M-1-k) \pmod M}$ to the current inversion count.

Pitfalls:
- Indexing: Ensure 0-based vs 1-based consistency.
- Modulo arithmetic for negative numbers in Python: `(M - 1 - k) % M` works correctly.
- Large numbers: Inversion count can be up to $N(N-1)/2 \approx 2 \cdot 10^{10}$, so use 64-bit integers (Python handles this automatically).
- Efficiency: Precomputing $Add_v$ and $Sub_v$ takes $O(N)$ total because each index belongs to exactly one value group. The loop over $k$ is $O(M)$. Total time $O(N \log N + M)$.

## worker: none
1. **Initial Inversion Count**: Computed using a Fenwick Tree in $O(N \log M)$ time. For each element $A_i$, we count how many previously processed elements are greater than $A_i$. This is done by maintaining a frequency array in the BIT and querying the count of elements $\le A_i$.
2. **Delta Calculation**: The key insight is that the change in inversion count when shifting from $k$ to $k+1$ depends only on which elements wrap around from $M-1$ to $0$. An element $A_i$ wraps at step $k \to k+1$ if $A_i + k \equiv M-1 \pmod M$. The change $\Delta$ is determined by pairs involving one wrapping element and one non-wrapping element.
   - Specifically, $\Delta = (\text{# pairs } (i,j) \text{ with } i<j, A_i \text{ doesn't wrap}, A_j \text{ wraps}) - (\text{# pairs } (i,j) \text{ with } i<j, A_i \text{ wraps}, A_j \text{ doesn't wrap})$.
   - This $\Delta$ depends only on the value $v$ that wraps, i.e., $v = (M-1-k) \pmod M$.
   - We precompute this $\Delta_v$ for each possible value $v \in [0, M-1]$ by iterating through the positions of each value in the original array. This takes $O(N)$ total time.
3. **Iteration**: We start with the inversion count for $k=0$. Then for each $k$ from $0$ to $M-2$, we update the inversion count by adding $\Delta_{(M-1-k) \pmod M}$ and store the result for $k+1$. This loop runs in $O(M)$ time.
4. **Complexity**: Total time complexity is $O(N \log M + N + M) = O(N \log M + M)$, which fits within the constraints $N, M \le 2 \times 10^5$. Space complexity is $O(N + M)$.
