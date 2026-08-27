1. **Initial Inversion Count**: Compute the inversion number for $k=0$ (i.e., for the original array $A$) using a Fenwick Tree (Binary Indexed Tree) or Merge Sort in $O(N \log N)$ time.
2. **Frequency Array**: Count the frequency of each value in $A$. Let `cnt[x]` be the number of times $x$ appears in $A$.
3. **Transition Logic**: When moving from $k$ to $k+1$, every element $A_i$ becomes $(A_i + 1) \pmod M$.
   - Elements that were $M-1$ become $0$. These elements "wrap around".
   - For an element wrapping from $M-1$ to $0$:
     - It was greater than all elements in $[0, M-2]$. Now it is smaller than all elements in $[1, M-1]$ (which are now shifted to $[2, M]$ effectively, but relative order among non-wrapping elements stays same).
     - Specifically, let $W$ be the set of indices where $A_i = M-1$. Let $c = |W|$.
     - The change in inversions comes from pairs involving these wrapping elements and non-wrapping elements.
     - Before wrap: Wrapping elements ($M-1$) are greater than all non-wrapping elements ($0 \dots M-2$). So each pair $(i, j)$ with $i \in W, j \notin W$ and $i < j$ contributed 1 inversion. Each pair with $i \notin W, j \in W$ and $i < j$ contributed 0 inversions (since $A_i < A_j$).
     - After wrap: Wrapping elements become $0$. Non-wrapping elements become $A_i+1 \in [1, M-1]$. So wrapping elements are now smaller than all non-wrapping elements.
     - Pairs $(i, j)$ with $i \in W, j \notin W$ and $i < j$: Previously $A_i > A_j$ (inv=1). Now $A_i=0 < A_j+1$ (inv=0). Loss of 1 inversion per such pair.
     - Pairs $(i, j)$ with $i \notin W, j \in W$ and $i < j$: Previously $A_i < A_j$ (inv=0). Now $A_i+1 > 0$ (inv=1). Gain of 1 inversion per such pair.
     - Pairs within $W$: Relative order doesn't change values (both become 0), so no change in inversion status between them? Wait, if $A_i=A_j=M-1$, they are equal. Inversions require strict inequality. So pairs within $W$ never contribute. Same for pairs within non-$W$.
     - So, $\Delta = (\text{# pairs } i \notin W, j \in W, i < j) - (\text{# pairs } i \in W, j \notin W, i < j)$.
     - Let $c$ be the count of $M-1$. Let $pos$ be the list of indices where $A_i = M-1$.
     - Number of non-wrapping elements is $N-c$.
     - For each $j \in W$ (index $j$), the number of non-wrapping elements before it is $j - (\text{number of wrapping elements before or at } j)$. Since $j$ is in $W$, let's say there are $k_j$ wrapping elements at indices $\le j$. Then non-wrapping before $j$ is $j - k_j$. These form pairs $(i, j)$ with $i < j, i \notin W, j \in W$.
     - For each $i \in W$ (index $i$), the number of non-wrapping elements after it is $(N - i) - (c - k_i)$, where $k_i$ is number of wrapping elements $\le i$. These form pairs $(i, j)$ with $i < j, i \in W, j \notin W$.
     - Alternatively, total pairs between $W$ and $V \setminus W$ is $c(N-c)$.
     - Let $P_{before}$ be pairs $(i, j)$ with $i \in W, j \notin W, i < j$.
     - Let $P_{after}$ be pairs $(i, j)$ with $i \notin W, j \in W, i < j$.
     - $P_{before} + P_{after} = c(N-c)$.
     - We need $P_{after} - P_{before}$.
     - $P_{after} - P_{before} = P_{after} - (c(N-c) - P_{after}) = 2 P_{after} - c(N-c)$.
     - So we need to compute $P_{after}$: for each $j \in W$, count non-wrapping elements before $j$.
     - This can be done by iterating through the array and maintaining a count of wrapping elements seen so far.
4. **Efficient Update**: Instead of recomputing from scratch, we can update the inversion count iteratively.
   - However, the wrap-around logic above is for $k=0 \to k=1$. What about $k=1 \to k=2$?
   - At step $k$, elements are $B_i = (A_i + k) \pmod M$.
   - When moving to $k+1$, elements with $B_i = M-1$ wrap to $0$.
   - $B_i = M-1 \iff A_i + k \equiv M-1 \pmod M \iff A_i = M - 1 - k$.
   - So at step $k$, the elements that wrap are those with $A_i = M - 1 - k$.
   - Let $val = M - 1 - k$. The elements with $A_i = val$ will wrap.
   - Let $c_k$ be the count of $A_i = val$.
   - The change in inversions is $2 P_{after}^{(k)} - c_k (N - c_k)$, where $P_{after}^{(k)}$ is the number of pairs $(i, j)$ such that $i < j$, $A_i = val$, $A_j \neq val$, and $A_j$ does NOT wrap? No, the logic above assumed only one group wraps.
   - Yes, only elements equal to $M-1$ in the current $B$ wrap. These correspond to $A_i = M - 1 - k$.
   - So we just need to know, for the current set of wrapping elements (indices where $A_i = M - 1 - k$), how many non-wrapping elements are before/after them.
   - We can precompute the positions of each value.
   - For each $k$, identify the set of indices $W_k = \{ i \mid A_i = M - 1 - k \}$.
   - Compute $P_{after}^{(k)}$: sum over $j \in W_k$ of (number of non-wrapping elements before $j$).
   - "Non-wrapping" means $A_i \neq M - 1 - k$.
   - This can be computed efficiently if we maintain a data structure or just iterate if the total size of $W_k$ over all $k$ is small? No, sum of $|W_k|$ is $N$. So we can iterate over all elements once per wrap event.
   - Algorithm:
     1. Compute initial inversions for $k=0$.
     2. Store indices for each value $v \in [0, M-1]$.
     3. For $k = 0$ to $M-1$:
        - Print current inversion count.
        - If $k < M-1$:
          - Let $val = M - 1 - k$.
          - Let $W$ be the list of indices where $A_i = val$.
          - Let $c = |W|$.
          - Compute $P_{after}$: For each $j \in W$, count number of $i < j$ such that $A_i \neq val$.
            - This is $j - (\text{number of elements in } W \text{ that are } \le j)$.
            - Since we process $W$ in sorted order, we can do this in $O(c)$.
          - $\Delta = 2 P_{after} - c(N - c)$.
          - Update inversion count: $inv = inv + \Delta$.