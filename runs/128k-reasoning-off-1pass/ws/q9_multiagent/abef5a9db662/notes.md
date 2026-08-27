
## ideation
The core difficulty lies in efficiently simulating the rating changes for $Q$ different initial values, given $N$ contests. A naive simulation for each query would take $O(N \cdot Q)$, which is too slow ($2 \cdot 10^5 \times 3 \cdot 10^5 \approx 6 \cdot 10^{10}$ operations).

However, the constraints on the rating values are small: $L_i, R_i, X \le 5 \times 10^5$. The maximum possible final rating is bounded by $5 \times 10^5 + N \approx 7 \times 10^5$. This suggests we can precompute the answer for every possible starting rating $X$ in the range $[1, 5 \times 10^5]$.

**Approach:**
1.  **Observation:** For a fixed starting rating $X$, the rating increases by 1 in contest $i$ if the current rating is in $[L_i, R_i]$. Since the rating only increases (never decreases), the condition "current rating $\in [L_i, R_i]$" is equivalent to checking if the starting rating $X$ lands in $[L_i, R_i]$ at the moment of contest $i$, *provided* the rating hasn't jumped out of the interval due to previous increments.
    *Wait, let's re-evaluate the logic.*
    Actually, the rating increases sequentially.
    Contest 1: If $X \in [L_1, R_1]$, $X \to X+1$.
    Contest 2: If new $X \in [L_2, R_2]$, $X \to X+1$.
    
    This looks like a path simulation. However, notice that the maximum rating is small. Let $M = 500000$. The max possible rating is $M + N$.
    Can we simply count how many contests a specific starting value $X$ participates in?
    Not directly, because the interval check depends on the *current* rating, which changes.
    
    **Correct Logic via Difference Array (Sweep Line):**
    Let's consider the effect of all contests on the final rating.
    Actually, there is a simpler property. Since the rating only increases, the sequence of ratings is non-decreasing.
    Let $f(X)$ be the final rating starting at $X$.
    $f(X) = X + (\text{number of contests } i \text{ where rating during contest } i \in [L_i, R_i])$.
    
    Is it true that if we start at $X$, we participate in contest $i$ if and only if $X \in [L_i, R_i]$?
    No. Example: Contest 1 is $[1, 2]$. Start $X=1$. Rating becomes 2. Contest 2 is $[3, 4]$. Rating is 2, so no increase.
    If we started at $X=2$, Contest 1: $2 \in [1, 2] \to 3$. Contest 2: $3 \in [3, 4] \to 4$.
    So the path matters.
    
    **Alternative Approach: Dynamic Programming / Prefix Sums on Values**
    Since the max value of $X$ is $5 \cdot 10^5$ and max rating is $\approx 7 \cdot 10^5$, we can compute $f(X)$ for all $X$.
    Notice that $f(X)$ is non-decreasing with respect to $X$. If you start with a higher rating, you are "ahead" in the sequence of contests? Not necessarily, because intervals are static.
    However, consider the state space. The state is just the current rating.
    Let $dp[v]$ be the final rating if we start at rating $v$ *at the beginning of the process*.
    This doesn't help directly because the process is sequential.
    
    Let's flip the perspective. Instead of simulating forward for each $X$, let's simulate the "flow" of ratings.
    Consider the intervals $[L_i, R_i]$.
    If a rating is in $[L_i, R_i]$, it increments.
    This looks like we are moving points on a line.
    
    **Key Insight:**
    The maximum rating is small enough ($V_{max} \approx 700,000$).
    Let's define an array `cnt[v]` which represents how many contests a rating $v$ would trigger an increment for *if it were the current rating*.
    But the current rating changes.
    
    Let's try a different DP state.
    Let $ans[v]$ be the final rating if the initial rating is $v$.
    We know $ans[v] = v + \text{count}$.
    Is there a relation between $ans[v]$ and $ans[v+1]$?
    Suppose we start at $v$.
    Contest 1: Check $v \in [L_1, R_1]$.
    Suppose we start at $v+1$.
    Contest 1: Check $v+1 \in [L_1, R_1]$.
    
    Actually, we can solve this by processing the contests in order and maintaining the "final rating" for all possible current ratings.
    Let $dp[v]$ be the final rating after processing contests $1 \dots k$, given that the rating *before* contest $k+1$ is $v$.
    Initially, for $k=0$, $dp[v] = v$ for all valid $v$.
    Transition for contest $i$ with range $[L_i, R_i]$:
    For any current rating $v$:
    - If $L_i \le v \le R_i$: new rating becomes $v+1$.
    - Else: new rating remains $v$.
    
    So, $dp_{new}[v] = dp_{old}[v]$ if $v \notin [L_i, R_i]$.
    And $dp_{new}[v+1]$ gets contributions from $dp_{old}[v]$ where $v \in [L_i, R_i]$.
    Wait, multiple $v$'s map to the same next state?
    If $v \in [L_i, R_i]$, the rating becomes $v+1$.
    So $dp_{new}[v+1] = \max(dp_{new}[v+1], dp_{old}[v])$? No, the mapping is deterministic.
    Actually, if we start at $v$, the path is unique.
    $dp_{new}[y]$ is the final rating starting at some initial value that ends up at $y$ after contest $i$.
    But we want $dp_{initial}[X]$.
    
    Let's reverse the thinking.
    Let $f_k(v)$ be the rating after contest $k$ given that the rating *before* contest $k$ was $v$.
    $f_k(v) = v + 1$ if $L_k \le v \le R_k$, else $v$.
    We want $f_N(X)$.
    Notice that $f_k(v)$ is a function mapping $v \to v$ or $v \to v+1$.
    Since the domain is small ($500,000$), we can maintain the array of values $A[v] = f_k(v)$.
    Initially $A[v] = v$.
    Update step for $[L, R]$:
    For all $v \in [L, R]$, $A[v] \leftarrow A[v] + 1$.
    Wait, this is wrong. The condition depends on the *current* rating in the simulation, which is the output of the previous step.
    Let $curr[v]$ be the rating after $k$ contests if we started at $v$.
    Initially $curr[v] = v$.
    After contest $k+1$ with range $[L, R]$:
    The new rating for someone who had rating $r$ before this contest is:
    $r' = r + 1$ if $L \le r \le R$, else $r$.
    So, $curr_{new}[v] = curr_{old}[v] + 1$ if $L \le curr_{old}[v] \le R$, else $curr_{old}[v]$.
    
    This looks like we need to update the array based on values.
    Since $curr[v]$ is non-decreasing with $v$ (if you start higher, you stay higher or equal), the values $curr[v]$ will form a non-decreasing sequence.
    The condition $L \le curr[v] \le R$ will be true for a contiguous range of indices $v$.
    Why? Because $curr[v]$ is monotonic. The set of $v$ such that $curr[v] \in [L, R]$ is an interval (or union of intervals, but likely one due to monotonicity and the nature of +1 steps).
    Actually, since $curr[v]$ increases by at most 1 at each step, the "gaps" are small.
    More importantly, we can use a difference array or segment tree to handle range updates.
    
    **Algorithm Refinement:**
    1. Initialize an array `ans` of size $MAX\_VAL + N + 2$ where `ans[v] = v`.
    2. We need to perform $N$ updates. In each update $i$ with $[L_i, R_i]$:
       Find the range of indices $v$ such that $L_i \le ans[v] \le R_i$.
       For these $v$, increment `ans[v]`.
    3. Since `ans` is monotonic, the condition $L_i \le ans[v] \le R_i$ corresponds to $v \in [start\_idx, end\_idx]$.
       We can find $start\_idx$ using `bisect_left` (lower bound) for $L_i$.
       We can find $end\_idx$ using `bisect_right` for $R_i$.
       Then perform a range increment on `ans` from $start\_idx$ to $end\_idx$.
    4. Range increment on an array can be done with a difference array (prefix sum technique) in $O(1)$ update and $O(N)$ total reconstruction, or a segment tree. Given $N, Q \le 3 \cdot 10^5$ and array size $\approx 7 \cdot 10^5$, a difference array is sufficient and faster.
    
    **Complexity:**
    - Initialization: $O(MAX)$.
    - Each query: Binary search $O(\log MAX)$, Difference array update $O(1)$.
    - Total Precomputation: $O(MAX + N \log MAX)$.
    - Answering Queries: $O(1)$ per query.
    - Total Time: $O(MAX + N \log MAX + Q)$.
    - Constraints: $MAX \approx 7 \cdot 10^5$, $N \log MAX \approx 2 \cdot 10^5 \cdot 20 \approx 4 \cdot 10^6$. This fits well within time limits (usually 2s for $\sim 10^8$ ops).
    
    **Pitfalls:**
    - Array bounds: The rating can increase up to $500,000 + 200,000 = 700,000$. Ensure array size covers this.
    - Binary search logic: Careful with inclusive/exclusive bounds.
    - Difference array reconstruction: Apply prefix sums after all updates.
    - Input reading speed: Use fast I/O in Python.

## worker: Implement the solution using the Difference Array 
The solution uses a Segment Tree with lazy propagation to efficiently simulate the rating changes.
1.  **State Representation**: `ans[v]` represents the final rating if the initial rating is `v`. Initially, `ans[v] = v`.
2.  **Monotonicity**: The function `ans[v]` is non-decreasing with respect to `v`. This is crucial because it allows us to find the range of starting values `[start, end]` that satisfy the condition `L_i <= ans[v] <= R_i` using binary search (or segment tree traversal) in $O(\log M)$ time.
3.  **Segment Tree Operations**:
    *   **Initialization**: Build the tree with values `0` to `MAX_M-1`.
    *   **Update**: For each contest `(L_i, R_i)`, find the range `[start, end]` of indices `v` such that `ans[v]` falls within `[L_i, R_i]`. Increment `ans[v]` by 1 for all `v` in this range. This is a range update.
    *   **Query**: After processing all contests, retrieve `ans[X]` for each query `X`.
4.  **Complexity**:
    *   Building the tree: $O(M)$.
    *   Processing contests: $N \times O(\log M)$ for finding the range and updating.
    *   Answering queries: $Q \times O(\log M)$.
    *   Total Time: $O(M + (N+Q)\log M)$. With $M \approx 5 \times 10^5$, $N, Q \approx 3 \times 10^5$, this fits well within the time limit.
5.  **Optimization**: The segment tree stores the minimum value in each range. Since the array is monotonic, the minimum value in a range `[l, r]` is simply `ans[l]`. This allows us to prune the search for the first index $\ge L$ and the first index $> R$ efficiently.

## worker: Implement the solution using the Difference Array 
The solution implements the Difference Array + Binary Search approach as planned.
1.  **Data Structure**: A Binary Indexed Tree (Fenwick Tree) is used to maintain the difference array `diff`. This allows for $O(\log M)$ point updates and $O(\log M)$ prefix sum queries.
2.  **Logic**:
    *   The current rating for an initial value $v$ is $v + \text{prefix\_sum}(v)$.
    *   Since the rating only increases, the function $f(v) = v + \text{prefix\_sum}(v)$ is non-decreasing.
    *   For each contest $(L, R)$, we find the range of initial values $[start, end]$ such that $L \le f(v) \le R$ using binary search.
    *   We then update the difference array for this range: increment at `start` and decrement at `end + 1`.
3.  **Complexity**:
    *   Binary search takes $O(\log M)$ steps.
    *   Each step involves a BIT query ($O(\log M)$).
    *   Total per contest: $O(\log^2 M)$.
    *   Total time: $O(N \log^2 M + Q \log M)$.
    *   With $N, Q \approx 2-3 \times 10^5$ and $M \approx 7 \times 10^5$, $\log M \approx 20$. Operations $\approx 8 \times 10^7$, which fits within typical time limits for Python if I/O is fast.
4.  **Optimization**: Fast I/O is used (`sys.stdin.read`). The BIT is 1-indexed for convenience.

## worker: Run the code against the provided sample inputs to
The code implements the solution using a Binary Indexed Tree (Fenwick Tree) to maintain the difference array of rating increments.
1.  **State**: `ans[v]` represents the final rating if the initial rating is `v`. Initially `ans[v] = v`.
2.  **Update Logic**: For each contest with range `[L, R]`, we need to increment `ans[v]` by 1 for all `v` such that the *current* rating `ans[v]` falls within `[L, R]`.
3.  **Monotonicity**: Since `ans[v]` starts as `v` and only increases, it remains a non-decreasing function of `v`. This allows us to use binary search to find the range of indices `[start, end]` where `L <= ans[v] <= R`.
4.  **Efficiency**:
    *   `get_ans(v)` takes $O(\log M)$ using the BIT.
    *   Binary search takes $O(\log M)$ steps.
    *   Total per contest: $O(\log^2 M)$.
    *   With $N=2 \times 10^5$ and $M \approx 7 \times 10^5$, $\log M \approx 20$, so operations are roughly $8 \times 10^7$, which fits within the time limit for Python.
5.  **Difference Array**: Instead of updating the array directly (which would be $O(M)$), we use the BIT to perform range updates in $O(\log M)$ by updating `diff[start] += 1` and `diff[end] -= 1`. The value `ans[v]` is then `v + prefix_sum(diff, v)`.

## worker: Run the provided sample inputs to verify correctne
The solution implements the "Difference Array + Binary Search" approach.
1.  **State**: `ans[v]` represents the final rating if the initial rating is `v`. Initially `ans[v] = v`.
2.  **Update Logic**: For each contest with range `[L, R]`, we need to increment `ans[v]` by 1 for all `v` such that the *current* rating `ans[v]` falls within `[L, R]`.
3.  **Monotonicity**: Since `ans[v]` starts as `v` and only increases, it remains a non-decreasing function of `v`. This allows us to use binary search to find the range of indices `[start, end]` where `L <= ans[v] <= R`.
4.  **Efficiency**:
    *   `get_ans(v)` takes $O(\log M)$ using the BIT.
    *   Binary search takes $O(\log M)$ steps.
    *   Total per contest: $O(\log^2 M)$.
    *   With $N=2 \times 10^5$ and $M \approx 7 \times 10^5$, $\log M \approx 20$, so operations are roughly $8 \times 10^7$, which fits within the time limit for Python.
5.  **Difference Array**: Instead of updating the array directly (which would be $O(M)$), we use the BIT to perform range updates in $O(\log M)$ by updating `diff[start] += 1` and `diff[end] -= 1`. The value `ans[v]` is then `v + prefix_sum(diff, v)`.

## worker: finalize
The solution implements the "Difference Array + Binary Search" approach efficiently.
1.  **State**: `ans[v]` represents the final rating if the initial rating is `v`. Initially `ans[v] = v`.
2.  **Update Logic**: For each contest with range `[L, R]`, we need to increment `ans[v]` by 1 for all `v` such that the *current* rating `ans[v]` falls within `[L, R]`.
3.  **Monotonicity**: Since `ans[v]` starts as `v` and only increases, it remains a non-decreasing function of `v`. This allows us to use binary search to find the range of indices `[start, end]` where `L <= ans[v] <= R`.
4.  **Efficiency**:
    *   `get_ans(v)` takes $O(\log M)$ using the BIT.
    *   Binary search takes $O(\log M)$ steps.
    *   Total per contest: $O(\log^2 M)$.
    *   With $N=2 \times 10^5$ and $M \approx 7 \times 10^5$, $\log M \approx 20$, so operations are roughly $8 \times 10^7$, which fits within the time limit for Python.
5.  **Difference Array**: Instead of updating the array directly (which would be $O(M)$), we use the BIT to perform range updates in $O(\log M)$ by updating `diff[start] += 1` and `diff[end] -= 1`. The value `ans[v]` is then `v + prefix_sum(diff, v)`.
