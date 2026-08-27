
## ideation
The core difficulty is efficiently computing the sum of absolute differences $\sum_{i=1}^{X} \sum_{j=1}^{Y} |A_i - B_j|$ for multiple queries $(X, Y)$. A naive $O(N \cdot K)$ approach will time out since $N \le 10^5$ and $K \le 10^4$.

Key observations and strategy:
1.  **Sorting**: The value of $|A_i - B_j|$ depends on the relative order of $A_i$ and $B_j$. Sorting both arrays $A$ and $B$ allows us to handle the absolute value by splitting the sum into two parts: where $A_i \le B_j$ and where $A_i > B_j$.
2.  **Prefix Sums**: After sorting, we can precompute prefix sums for both arrays. This allows calculating the sum of elements in any prefix in $O(1)$.
3.  **Split Point Calculation**: For a specific $A_i$ (from the prefix $A[1..X]$), we need to know how many elements in $B[1..Y]$ are greater than or equal to $A_i$. However, since the query is on a *prefix* of $A$ and a *prefix* of $B$, the split isn't just a single point.
    *   Actually, a better approach for the query $(X, Y)$ is:
        Sum $= \sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
        Since $A$ and $B$ are sorted, for a fixed $i$, the values of $B_j$ (for $j \le Y$) are also sorted. We can find the index $p$ in $B$ such that $B_p \ge A_i$ and $B_{p-1} < A_i$.
        Then the inner sum splits at $p$. But $p$ can vary with $i$.
    *   **Optimization**: Instead of iterating $i$, notice that the condition $A_i \le B_j$ defines a region in the $(i, j)$ grid. Since both arrays are sorted, this boundary is monotonic.
    *   **Alternative Efficient Approach**:
        Let's consider the contribution of each $A_i$ against the prefix $B[1..Y]$.
        $\sum_{j=1}^Y |A_i - B_j| = \sum_{j=1}^Y (B_j - A_i)$ if $B_j \ge A_i$, else $(A_i - B_j)$.
        Let $pos$ be the largest index in $B[1..Y]$ such that $B_{pos} < A_i$. If no such element exists, $pos=0$.
        Then:
        Sum $= \sum_{j=1}^{pos} (A_i - B_j) + \sum_{j=pos+1}^Y (B_j - A_i)$
        $= pos \cdot A_i - \text{sum}(B, 1, pos) + (\text{sum}(B, pos+1, Y)) - (Y - pos) \cdot A_i$.
        
        Wait, $pos$ depends on $A_i$. Since we are summing over $i=1$ to $X$, and $A$ is sorted, $A_i$ is non-decreasing. Thus, $pos$ (the count of elements in $B[1..Y]$ smaller than $A_i$) is non-decreasing as $i$ increases.
        We can iterate $i$ from $1$ to $X$, maintaining the current split point in $B$. However, $X$ can be up to $10^5$, and doing this for each of $10^4$ queries would be $O(N \cdot K)$ in the worst case (if $X$ is large every time).
        
        **Is there an $O(\log N)$ per query solution?**
        Yes. We don't need to iterate $i$.
        The total sum is $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
        This looks like we are summing over a rectangle in the sorted grid.
        Let's reconsider the formula:
        Total Sum $= \sum_{i=1}^X \left( \sum_{j=1}^Y |A_i - B_j| \right)$.
        For a fixed $i$, let $k_i$ be the number of elements in $B[1..Y]$ that are smaller than $A_i$. Since $B$ is sorted, these are $B_1, \dots, B_{k_i}$.
        The inner sum is $k_i A_i - \sum_{j=1}^{k_i} B_j + \sum_{j=k_i+1}^Y B_j - (Y - k_i) A_i$.
        $= (2k_i - Y) A_i + (\text{sum}(B, k_i+1, Y) - \text{sum}(B, 1, k_i))$.
        
        The problem is that $k_i$ changes with $i$. Since $A$ is sorted, $k_i$ is non-decreasing.
        Can we compute $\sum_{i=1}^X (2k_i - Y) A_i + \dots$ efficiently?
        $k_i$ is determined by `bisect_left(B, A[i], lo=1, hi=Y)`.
        Since $k_i$ is non-decreasing, we can find the ranges of $i$ where $k_i$ is constant.
        Specifically, $k_i$ takes values $0, 1, \dots, Y$.
        We can find the split points in $A$ where $k_i$ increments.
        Actually, $k_i$ increments when $A_i > B_{k_i}$.
        Since $B$ is sorted, the values of $A_i$ that cause $k_i$ to jump to $v$ are those where $B_{v-1} < A_i \le B_v$ (with boundary checks).
        
        **Algorithm Refined**:
        1. Sort $A$ and $B$. Compute prefix sums for both.
        2. For each query $(X, Y)$:
           We need to sum over $i \in [1, X]$.
           The term $k_i$ (count of $B_j < A_i$ within $j \le Y$) is constant for a range of $i$.
           Specifically, for a fixed count $c \in [0, Y]$, the condition is $B_c < A_i \le B_{c+1}$ (handling $B_0 = -\infty, B_{Y+1} = \infty$).
           We can find the range of indices $[L_c, R_c]$ in $A$ such that for all $i$ in this range, the count of smaller elements in $B[1..Y]$ is exactly $c$.
           Actually, simpler:
           Iterate $c$ from $0$ to $Y$? No, $Y$ is large.
           But notice that $k_i$ only changes when $A_i$ crosses a value in $B$.
           Since we only care about $i \le X$, we can find the split points in $A$ using binary search against the values of $B$.
           
           Let's define the transition points.
           $k_i = c$ implies $B_c < A_i \le B_{c+1}$ (conceptually, with $B_0 = -\infty, B_{Y+1} = \infty$).
           We need to sum over $i \in [1, X]$ grouped by $k_i$.
           The values of $k_i$ will be $0, 1, \dots, Y$.
           However, $k_i$ cannot exceed $Y$. Also $k_i$ cannot exceed $i$ (trivially, but not useful).
           More importantly, $k_i$ is the index in $B$ (1-based) of the first element $\ge A_i$, clamped to $Y+1$ if all $B_j < A_i$.
           Actually, `bisect_left` on $B$ gives the first index where $B[idx] \ge A_i$. Let this be `idx`. Then count of smaller is `idx-1`.
           Since $A$ is sorted, `idx` is non-decreasing.
           We can find the ranges of $i$ where `idx` is constant.
           The `idx` values can only be $1, 2, \dots, Y+1$.
           We can find the largest $i$ such that `bisect_left(B, A[i], lo=1, hi=Y+1)` returns a specific value.
           
           Wait, doing a binary search for each distinct value of $k$ might still be slow if we iterate $k$.
           But note: we only care about $i \le X$.
           The sequence $k_1, k_2, \dots, k_X$ is non-decreasing.
           We can find the split points in $A$ corresponding to $B_1, B_2, \dots, B_Y$.
           Specifically, find the largest index $i_0$ such that $A_{i_0} \le B_1$. Then for $i \in [1, i_0]$, $k_i = 0$.
           Find largest $i_1$ such that $A_{i_1} \le B_2$. Then for $i \in [i_0+1, i_1]$, $k_i = 1$.
           ...
           Find largest $i_{Y}$ such that $A_{i_{Y}} \le B_Y$. Then for $i \in [i_{Y-1}+1, i_{Y}]$, $k_i = Y$.
           And for $i > i_Y$, $k_i = Y$ (since all $B_j < A_i$).
           
           So we have at most $Y+1$ segments. Summing over these segments:
           For a segment $[l, r]$ where $k_i = c$:
           Contribution $= \sum_{i=l}^r [ (2c - Y) A_i + (\text{sum}(B, c+1, Y) - \text{sum}(B, 1, c)) ]$.
           $= (2c - Y) \sum_{i=l}^r A_i + (r-l) \times (\text{sum}(B, c+1, Y) - \text{sum}(B, 1, c))$.
           Using prefix sums of $A$ and $B$, this is $O(1)$.
           
           How to find the split points $i_0, i_1, \dots$ efficiently?
           We can use `bisect_right` on $A$ with values $B_1, B_2, \dots$.
           But iterating $c$ from $0$ to $Y$ is $O(Y)$, which is $O(N)$. Total $O(NK)$ is too slow.
           
           **Correction**: We don't need to iterate all $c$.
           The relevant $c$ values are those where the interval $[l, r]$ actually intersects $[1, X]$.
           Also, notice that we only need to check $c$ up to $Y$.
           Is there a way to jump?
           Actually, the number of distinct values of $k_i$ for $i \in [1, X]$ is at most $X$ and at most $Y$.
           But we can find the split points by binary searching on $A$ for each $B_j$? No.
           
           Let's reverse the thinking.
           We need $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
           This is equal to:
           $\sum_{i=1}^X \sum_{j=1}^Y (B_j - A_i) \cdot \mathbb{I}(B_j \ge A_i) + \sum_{i=1}^X \sum_{j=1}^Y (A_i - B_j) \cdot \mathbb{I}(A_i > B_j)$.
           $= \sum_{j=1}^Y \sum_{i=1}^X (B_j - A_i) \mathbb{I}(B_j \ge A_i) + \sum_{i=1}^X \sum_{j=1}^Y (A_i - B_j) \mathbb{I}(A_i > B_j)$.
           
           Let's analyze the first term: $\sum_{j=1}^Y \sum_{i=1}^X (B_j - A_i) \mathbb{I}(A_i \le B_j)$.
           For a fixed $j$, we need to count how many $i \in [1, X]$ satisfy $A_i \le B_j$. Let this count be $cnt_j$.
           Then the inner sum is $cnt_j \cdot B_j - \sum_{i \in [1, X], A_i \le B_j} A_i$.
           Since $A$ is sorted, the condition $A_i \le B_j$ defines a prefix of $A$. Let $idx_j$ be the largest index such that $A_{idx_j} \le B_j$ (clamped to $X$).
           Then $cnt_j = idx_j$ and the sum of $A$ is `prefA[idx_j]`.
           So Term1 $= \sum_{j=1}^Y (idx_j \cdot B_j - \text{prefA}[idx_j])$.
           
           Similarly, Term2 $= \sum_{i=1}^X \sum_{j=1}^Y (A_i - B_j) \mathbb{I}(B_j < A_i)$.
           For a fixed $i$, we need count of $j \in [1, Y]$ such that $B_j < A_i$. Let this be $cnt'_i$.
           Inner sum: $cnt'_i \cdot A_i - \sum_{j \in [1, Y], B_j < A_i} B_j$.
           Let $idx'_i$ be the largest index such that $B_{idx'_i} < A_i$ (clamped to $Y$).
           Then Term2 $= \sum_{i=1}^X (idx'_i \cdot A_i - \text{prefB}[idx'_i])$.
           
           Now, calculating Term1:
           We need to sum over $j=1 \dots Y$.
           $idx_j$ is `min(X, bisect_right(A, B[j]))`.
           Since $B$ is sorted, $idx_j$ is non-decreasing.
           We can find the ranges of $j$ where $idx_j$ is constant.
           $idx_j$ changes value when $B_j$ crosses an element of $A$.
           Specifically, $idx_j = k$ for $j$ in some range.
           The values of $idx_j$ go from $0$ to $X$.
           We can find the split points in $B$ using binary search on $A$?
           Actually, we can find the largest $j$ such that $B_j \le A_k$ for each $k$.
           But we need to sum over $j$.
           Notice that $idx_j$ is constant for a range of $j$.
           Let's find the indices $j$ where $idx_j$ increments.
           $idx_j$ increments when $B_j > A_{prev\_idx}$.
           Actually, simpler:
           $idx_j = \min(X, \text{bisect\_right}(A, B[j]))$.
           Since $B$ is sorted, we can find the ranges of $j$ where $\text{bisect\_right}(A, B[j])$ is constant.
           This happens when $B[j]$ falls between two elements of $A$.
           The critical values for $B[j]$ are $A_1, A_2, \dots, A_X$.
           We can find the range of $j$ such that $A_k \le B[j] < A_{k+1}$.
           This corresponds to $j \in [\text{bisect\_left}(B, A_k), \text{bisect\_left}(B, A_{k+1}) - 1]$.
           We can iterate $k$ from $0$ to $X$.
           For each $k$, we find the range of $j$ in $[1, Y]$ where the count of $A$'s $\le B_j$ is exactly $k$.
           Wait, if $B_j < A_1$, count is 0.
           If $A_k \le B_j < A_{k+1}$, count is $k$.
           So we iterate $k$ from $0$ to $X$.
           Find $j_{start} = \text{bisect\_left}(B, A_k)$ (if $k=0$, $j_{start}=1$).
           Find $j_{end} = \text{bisect\_left}(B, A_{k+1}) - 1$.
           Intersect with $[1, Y]$.
           If the intersection is non-empty, add contribution.
           Contribution for this range:
           Number of $j$'s is $len$.
           Sum of $B_j$ in range: `prefB[j_end] - prefB[j_start-1]`.
           Term1 part: $\sum (k \cdot B_j - \text{prefA}[k]) = k \cdot \text{sum}(B) - len \cdot \text{prefA}[k]$.
           
           Complexity:
           We iterate $k$ from $0$ to $X$. Inside, we do binary search on $B$.
           Total complexity $O(X \log N)$. Since $X \le N$, this is $O(N \log N)$.
           Doing this for $K$ queries gives $O(K \cdot N \log N)$, which is too slow ($10^4 \cdot 10^5 \cdot 17 \approx 1.7 \cdot 10^{10}$).
           
           **We need $O(\log N)$ or $O(1)$ per query.**
           Let's re-evaluate the summation.
           Term1 $= \sum_{j=1}^Y (\min(X, \text{bisect\_right}(A, B_j)) \cdot B_j - \text{prefA}[\min(X, \text{bisect\_right}(A, B_j))])$.
           Let $f(j) = \min(X, \text{bisect\_right}(A, B_j))$.
           We need $\sum_{j=1}^Y f(j) B_j - \sum_{j=1}^Y \text{prefA}[f(j)]$.
           
           Notice that $f(j)$ is a step function of $j$.
           The steps occur when $B_j$ crosses $A_k$.
           The values of $f(j)$ are $0, 1, \dots, X$.
           The transition points in $B$ are determined by $A_1, A_2, \dots, A_X$.
           Specifically, $f(j) = k$ when $A_k \le B_j < A_{k+1}$ (with boundaries).
           The range of $j$ for a specific $k$ is $[L_k, R_k]$.
           $L_k = \text{bisect\_left}(B, A_k)$.
           $R_k = \text{bisect\_left}(B, A_{k+1}) - 1$.
           We need to sum over $j \in [1, Y] \cap [L_k, R_k]$.
           This is still iterating $k$.
           
           **Is there a way to avoid iterating $k$?**
           Maybe we can swap the loops or use a different perspective.
           Total Sum $= \sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
           Consider the contribution of each pair $(A_i, B_j)$.
           This is equivalent to calculating the area between the step function of cumulative sums?
           
           Let's try a different decomposition.
           $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j| = \sum_{i=1}^X \sum_{j=1}^Y (B_j - A_i) \text{sgn}(B_j - A_i)$.
           $= \sum_{j=1}^Y \sum_{i=1}^X B_j \text{sgn}(B_j - A_i) - \sum_{i=1}^X \sum_{j=1}^Y A_i \text{sgn}(B_j - A_i)$.
           $= \sum_{j=1}^Y B_j \left( \sum_{i=1}^X \text{sgn}(B_j - A_i) \right) - \sum_{i=1}^X A_i \left( \sum_{j=1}^Y \text{sgn}(B_j - A_i) \right)$.
           
           Let $S_1(j) = \sum_{i=1}^X \text{sgn}(B_j - A_i)$.
           $\text{sgn}(B_j - A_i) = 1$ if $B_j > A_i$, $-1$ if $B_j < A_i$, $0$ if equal.
           Assuming distinct for simplicity (or handling equality carefully), let's say $+1$ if $A_i < B_j$, $-1$ if $A_i > B_j$.
           Let $cnt_{<}(j)$ be count of $i \in [1, X]$ with $A_i < B_j$.
           Let $cnt_{>}(j)$ be count of $i \in [1, X]$ with $A_i > B_j$.
           $S_1(j) = cnt_{<}(j) - cnt_{>}(j)$.
           Note $cnt_{<}(j) + cnt_{>}(j) = X$ (ignoring equality for a moment).
           So $S_1(j) = cnt_{<}(j) - (X - cnt_{<}(j)) = 2 cnt_{<}(j) - X$.
           $cnt_{<}(j)$ is simply the number of elements in $A[1..X]$ strictly less than $B_j$.
           Since $A$ is sorted, this is `bisect_left(A, B[j], lo=1, hi=X)`. Let this be $k_j$.
           So $S_1(j) = 2 k_j - X$.
           
           Similarly, $S_2(i) = \sum_{j=1}^Y \text{sgn}(B_j - A_i) = cnt_{<}(i) - cnt_{>}(i)$ where counts are over $B[1..Y]$.
           $cnt_{<}(i)$ is count of $j \in [1, Y]$ with $B_j < A_i$. Let this be $m_i$.
           $S_2(i) = 2 m_i - Y$.
           
           Total Sum $= \sum_{j=1}^Y B_j (2 k_j - X) - \sum_{i=1}^X A_i (2 m_i - Y)$.
           $= 2 \sum_{j=1}^Y B_j k_j - X \sum_{j=1}^Y B_j - 2 \sum_{i=1}^X A_i m_i + Y \sum_{i=1}^X A_i$.
           
           Now we need to compute:
           1. $\sum_{j=1}^Y B_j k_j$ where $k_j = \text{count of } A_i < B_j \text{ for } i \in [1, X]$.
           2. $\sum_{i=1}^X A_i m_i$ where $m_i = \text{count of } B_j < A_i \text{ for } j \in [1, Y]$.
           
           Let's analyze term 1: $\sum_{j=1}^Y B_j \cdot (\text{count of } A_i < B_j \text{ in } A[1..X])$.
           $k_j$ is non-decreasing with $j$.
           $k_j$ takes values $0, 1, \dots, X$.
           The value $k_j = c$ when $A_c \le B_j < A_{c+1}$ (with $A_0=-\infty, A_{X+1}=\infty$).
           We need to sum $B_j$ over ranges where $k_j$ is constant, multiplied by that constant.
           Range for $k_j = c$: $j \in [\text{bisect\_left}(B, A_c), \text{bisect\_left}(B, A_{c+1}) - 1]$.
           Intersect with $[1, Y]$.
           Sum of $B_j$ in this range is `prefB`.
           So term 1 is $\sum_{c=0}^{X} c \cdot (\text{sum of } B_j \text{ in range})$.
           This still requires iterating $c$ from $0$ to $X$. $O(X \log N)$ or $O(X)$. Too slow per query.
           
           **Wait, is there a property I'm missing?**
           Maybe we can compute this using a 2D data structure? No, too complex.
           Maybe the constraints allow $O(N \sqrt N)$? No, $K=10^4, N=10^5$.
           $O(K \sqrt N)$ is $3 \cdot 10^7$, which is acceptable.
           Can we do $O(\sqrt N)$ per query?
           We can iterate $c$ in blocks?
           Or maybe the number of distinct values of $k_j$ is small? No.
           
           Let's reconsider the problem constraints and typical solutions for "sum of absolute differences in subarrays".
           Usually, this is solved by sorting and prefix sums.
           Is it possible that $X$ and $Y$ are small? No.
           
           Let's look at the structure again.
           $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
           This is the sum of distances between two sets of points on a line, restricted to prefixes.
           If we fix the split point in the combined sorted array of $A$ and $B$, we can compute it.
           But the split point depends on the specific values.
           
           **Alternative Idea**:
           Since $K$ is up to $10^4$ and $N$ up to $10^5$, maybe $O(K \cdot \sqrt N)$ is intended?
           Or maybe $O(K \log^2 N)$?
           How to get $O(\log N)$?
           We need $\sum_{j=1}^Y B_j \cdot k_j$.
           $k_j = \min(X, \text{bisect\_left}(A, B_j))$.
           This function $k_j$ is a step function.
           The steps are at values $A_1, A_2, \dots, A_X$.
           The values of $j$ where steps occur are $j$ such that $B_j \ge A_k$.
           The indices where $k_j$ changes are $j_k = \text{bisect\_left}(B, A_k)$.
           So $k_j$ changes at $j_1, j_2, \dots, j_X$.
           These indices are sorted.
           We need to sum $B_j \cdot k_j$ for $j \in [1, Y]$.
           This is $\sum_{k=1}^X k \cdot (\text{sum of } B_j \text{ where } j \in [j_k, j_{k+1}-1] \cap [1, Y])$.
           The intervals $[j_k, j_{k+1}-1]$ are disjoint and cover $[1, Y]$.
           The number of intervals is $X$.
           We cannot iterate all $X$ intervals.
           
           **However**, notice that we only care about $j \le Y$.
           The relevant intervals are those that overlap with $[1, Y]$.
           The intervals are defined by $j_k = \text{bisect\_left}(B, A_k)$.
           We need to sum over $k$ such that $[j_k, j_{k+1}-1]$ overlaps $[1, Y]$.
           Since $j_k$ is increasing, we can find the range of $k$ such that $j_k \le Y$.
           Let $K_{max} = \text{bisect\_right}(j\_list, Y)$.
           Then we only need to sum for $k$ from $1$ to $K_{max}$.
           Wait, $j_k$ can be up to $N$. $Y$ is up to $N$.
           In the worst case, $K_{max} \approx Y$. Still $O(Y)$.
           
           **Is there a way to compute $\sum_{j=1}^Y B_j \cdot k_j$ faster?**
           $k_j = \sum_{i=1}^X \mathbb{I}(A_i < B_j)$.
           So $\sum_{j=1}^Y B_j k_j = \sum_{j=1}^Y B_j \sum_{i=1}^X \mathbb{I}(A_i < B_j) = \sum_{i=1}^X \sum_{j=1}^Y B_j \mathbb{I}(A_i < B_j)$.
           $= \sum_{i=1}^X (\text{sum of } B_j \text{ for } j \in [1, Y] \text{ s.t. } B_j > A_i)$.
           For a fixed $i$, the condition $B_j > A_i$ defines a suffix of $B[1..Y]$.
           Let $p_i = \text{bisect\_right}(B, A_i, lo=1, hi=Y)$.
           Then the sum is `prefB[Y] - prefB[p_i]`.
           So Term1 $= \sum_{i=1}^X (\text{prefB}[Y] - \text{prefB}[p_i])$.
           $= X \cdot \text{prefB}[Y] - \sum_{i=1}^X \text{prefB}[p_i]$.
           
           Now we need to compute $\sum_{i=1}^X \text{prefB}[p_i]$ where $p_i = \text{bisect\_right}(B, A_i, lo=1, hi=Y)$.
           $p_i$ is non-decreasing with $i$.
           $p_i$ takes values in $0 \dots Y$.
           The value $p_i = v$ when $B_{v-1} \le A_i < B_v$ (roughly).
           The transition points in $A$ are $B_1, B_2, \dots, B_Y$.
           We can find the ranges of $i$ where $p_i$ is constant.
           Range for $p_i = v$: $i \in [\text{bisect\_left}(A, B_v), \text{bisect\_left}(A, B_{v+1}) - 1]$.
           Intersect with $[1, X]$.
           Sum over these ranges: $v \cdot (\text{count of } i) \cdot \text{prefB}[v]$.
           Wait, $\text{prefB}[p_i]$ is constant for the range? Yes, if $p_i = v$.
           So we need $\sum_{v} v \cdot \text{prefB}[v] \cdot (\text{count of } i \text{ in range})$.
           The count of $i$ is the length of the intersection.
           The ranges are defined by $B_1, \dots, B_Y$.
           We iterate $v$ from $0$ to $Y$.
           This is $O(Y \log N)$. Still too slow.
           
           **BUT**, notice that $p_i$ is determined by $A_i$.
           $p_i = \text{bisect\_right}(B, A_i)$.
           We need $\sum_{i=1}^X \text{prefB}[\text{bisect\_right}(B, A_i)]$.
           This looks like we are summing a function of $A_i$.
           Since $A$ is sorted, $p_i$ is sorted.
           The values of $p_i$ change only when $A_i$ crosses a value in $B$.
           The number of changes is at most $Y$.
           Is there a way to jump?
           Maybe we can use the fact that $K$ is small? No, $K$ is $10^4$.
           
           **Wait, let's re-read the constraints.**
           $N \le 10^5, K \le 10^4$.
           $O(K \cdot N)$ is $10^9$, definitely TLE.
           $O(K \cdot \sqrt N)$ is $3 \cdot 10^7$, acceptable.
           Can we do $O(\sqrt N)$?
           We can iterate $v$ in blocks of size $\sqrt N$?
           Or maybe the number of distinct values of $p_i$ is small? No.
           
           **Is there an $O(\log N)$ solution?**
           Let's reconsider the formula:
           Total $= 2 \sum_{j=1}^Y B_j k_j - X \sum B_j - 2 \sum_{i=1}^X A_i m_i + Y \sum A_i$.
           We reduced it to computing $\sum_{i=1}^X \text{prefB}[p_i]$ and $\sum_{j=1}^Y \text{prefA}[q_j]$.
           Where $p_i = \text{bisect\_right}(B, A_i)$ and $q_j = \text{bisect\_right}(A, B_j)$.
           
           Notice symmetry.
           $\sum_{i=1}^X \text{prefB}[p_i]$.
           $p_i$ is the index in $B$ where $A_i$ fits.
           If we consider the pairs $(A_i, B_j)$, we are summing `prefB` at the position of $A_i$.
           
           **Actually, there is a known technique for this.**
           If we sort $A$ and $B$, the function $f(i) = \text{prefB}[\text{bisect\_right}(B, A_i)]$ is piecewise constant.
           The pieces are determined by the values of $B$.
           The number of pieces is at most $Y$.
           But we only need to sum up to $X$.
           If $X$ is small, we iterate $i$. If $X$ is large, we iterate $j$ (the other way).
           Wait, if we iterate $j$ for the second term:
           $\sum_{j=1}^Y \text{prefA}[q_j]$.
           $q_j = \text{bisect\_right}(A, B_j)$.
           This is symmetric.
           
           So we have two terms.
           Term A: $\sum_{i=1}^X \text{prefB}[p_i]$.
           Term B: $\sum_{j=1}^Y \text{prefA}[q_j]$.
           
           For Term A:
           $p_i$ is constant for ranges of $i$.
           The ranges are $[L_v, R_v]$ where $p_i = v$.
           $L_v = \text{bisect\_left}(A, B_v)$.
           $R_v = \text{bisect\_left}(A, B_{v+1}) - 1$.
           We need to sum $v \cdot \text{prefB}[v] \cdot \text{count}$.
           The ranges are defined by $B_1, \dots, B_Y$.
           We can find the split points in $A$ corresponding to $B_1, \dots, B_Y$.
           Let these split points be $idx_1, idx_2, \dots, idx_Y$.
           $idx_k = \text{bisect\_left}(A, B_k)$.
           These indices are sorted.
           We need to sum over $i \in [1, X]$.
           The intervals are $[1, idx_1-1], [idx_1, idx_2-1], \dots$.
           We can iterate $k$ from $1$ to $Y$.
           But $Y$ can be $10^5$.
           However, we only care about intervals that overlap $[1, X]$.
           Since $idx_k$ is increasing, we can stop when $idx_k > X$.
           In the worst case, $idx_k$ increases by 1 each time, so we iterate $X$ times.
           $O(X \log N)$ per query.
           
           **Is there any constraint I missed?**
           Maybe $N, K$ are such that $O(N \sqrt K)$ or something?
           No.
           
           **Wait, what if we precompute something?**
           The queries are offline? No, we can read all and process offline.
           If we process offline, can we use a Fenwick tree?
           We want $\sum_{i=1}^X \text{prefB}[\text{bisect\_right}(B, A_i)]$.
           This is $\sum_{i=1}^X \sum_{j=1}^{\text{bisect\_right}(B, A_i)} \text{val}_j$ where $\text{val}_j$ is $B_j$? No, `prefB[v]` is sum of $B$.
           $\text{prefB}[p_i] = \sum_{j=1}^{p_i} B_j$.
           So Term A $= \sum_{i=1}^X \sum_{j=1}^{p_i} B_j = \sum_{j=1}^N B_j \cdot (\text{count of } i \in [1, X] \text{ s.t. } p_i \ge j)$.
           $p_i \ge j \iff \text{bisect\_right}(B, A_i) \ge j \iff B_j \le A_i$.
           So count is number of $i \in [1, X]$ such that $A_i \ge B_j$.
           Since $A$ is sorted, this is $X - \text{bisect\_left}(A, B_j) + 1$ (clamped).
           So Term A $= \sum_{j=1}^N B_j \cdot \max(0, X - \text{bisect\_left}(A, B_j) + 1)$.
           But we only sum $j$ up to $N$? No, $p_i$ can be up to $N$.
           Wait, $p_i = \text{bisect\_right}(B, A_i)$. This is index in $B$.
           So $p_i \le N$.
           Term A $= \sum_{i=1}^X \text{prefB}[p_i] = \sum_{j=1}^N B_j \cdot (\text{count of } i \in [1, X] \text{ s.t. } p_i \ge j)$.
           Condition $p_i \ge j \iff A_i \ge B_j$.
           Count $= \max(0, X - \text{bisect\_left}(A, B_j))$. (Assuming 1-based indexing for count).
           Let $cnt(j) = \max(0, X - \text{bisect\_left}(A, B_j))$.
           Then Term A $= \sum_{j=1}^N B_j \cdot cnt(j)$.
           But we only care about $j$ where $cnt(j) > 0$, i.e., $B_j \le A_X$.
           Also, we need to sum only up to $N$.
           This is still $O(N)$ per query.
           
           **Wait, is it possible that the intended solution is $O(K \cdot \sqrt N)$?**
           Yes, block decomposition.
           Divide $A$ into blocks of size $B = \sqrt N$.
           For a query $(X, Y)$:
           1. Iterate full blocks in $A$ up to $X$.
           2. Iterate remaining elements.
           Inside, we need to sum $\text{prefB}[p_i]$.
           $p_i$ depends on $A_i$.
           For a block of $A$, $A_i$ are in range $[L, R]$.
           $p_i$ will be constant or change slowly?
           $p_i = \text{bisect\_right}(B, A_i)$.
           If $A_i$ range is small, $p_i$ might not change much.
           But $B$ is large.
           
           **Actually, let's look at the constraints again.**
           $N=10^5, K=10^4$.
           Time limit is usually 2s.
           $10^9$ ops is too much.
           $3 \cdot 10^7$ is fine.
           So $O(K \sqrt N)$ is the target.
           How to achieve $O(\sqrt N)$?
           We can iterate $i$ in blocks.
           For a block of $A$, say indices $[l, r]$, we need $\sum_{i=l}^r \text{prefB}[p_i]$.
           $p_i$ is non-decreasing.
           The values of $p_i$ are in range $[p_l, p_r]$.
           The number of distinct values of $p_i$ in a block is at most $r-l+1$ (size of block) and also at most $N$.
           If we choose block size $S \approx \sqrt N$, then we have $\sqrt N$ blocks.
           For each block, we can compute the sum in $O(S \log N)$ or $O(S)$.
           Total $O(K \cdot \sqrt N \log N)$.
           $10^4 \cdot 316 \cdot 17 \approx 5 \cdot 10^7$. This is acceptable!
           
           **Algorithm with Block Decomposition**:
           1. Sort $A, B$. Precompute prefix sums.
           2. Divide $A$ into blocks of size $S \approx \sqrt N$.
           3. For each query $(X, Y)$:
              a. Identify full blocks and partial block in $A[1..X]$.
              b. For each full block $[l, r]$:
                 We need $\sum_{i=l}^r \text{prefB}[\text{bisect\_right}(B, A_i)]$.
                 Since $A$ is sorted, $\text{bisect\_right}(B, A_i)$ is non-decreasing.
                 The values of $p_i = \text{bisect\_right}(B, A_i)$ will change at most $S$ times (actually, it changes whenever $A_i$ crosses a $B_j$).
                 But we can just iterate $i$ from $l$ to $r$ and compute $p_i$.
                 Cost: $S \log N$.
              c. For the partial block, iterate $i$ from $l$ to $X$. Cost: $S \log N$.
              d. Total cost per query: $O(\sqrt N \log N)$.
              e. Total time: $O(K \sqrt N \log N)$.
           
           With $N=10^5, S=320$, $K=10^4$, $\log N \approx 17$.
           Ops $\approx 10^4 \cdot 320 \cdot 17 \approx 5.4 \cdot 10^7$.
           This should pass within 2 seconds in Python if optimized (PyPy).
           In C++, definitely. In Python, might be tight but likely okay given simple operations.

## worker: Implement the solution using block decomposition o
The solution implements the block decomposition strategy on array $A$ to handle the multiple queries efficiently.
1.  **Sorting**: Both arrays $A$ and $B$ are sorted. This allows us to use binary search to determine the split point for absolute differences.
2.  **Mathematical Derivation**:
    For a query $(X, Y)$, we want $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
    By splitting the inner sum based on whether $B_j \le A_i$ or $B_j > A_i$, we derived the formula:
    $$ \text{Total} = Y \sum_{i=1}^X A_i - 2 \sum_{i=1}^X (p_i \cdot A_i) + X \sum_{j=1}^Y B_j - 2 \sum_{i=1}^X \text{prefB}[p_i] $$
    where $p_i$ is the count of elements in $B[1..Y]$ that are less than or equal to $A_i$. This is found using `bisect_right`.
3.  **Complexity**:
    -   Sorting takes $O(N \log N)$.
    -   Prefix sums take $O(N)$.
    -   For each query, we iterate through blocks of $A$. With block size $S \approx \sqrt{N}$, there are $\sqrt{N}$ blocks.
    -   Inside each block, we iterate up to $S$ elements and perform a binary search ($O(\log N)$).
    -   Total per query: $O(\sqrt{N} \log N)$.
    -   Total time: $O(N \log N + K \sqrt{N} \log N)$.
    -   With $N=10^5, K=10^4$, this is approximately $5 \times 10^7$ operations, which fits within the time limit.
4.  **Implementation Details**:
    -   Input reading is optimized using `sys.stdin.read`.
    -   Block decomposition is implemented by precomputing block start and end indices.
    -   The logic handles the summation terms carefully to avoid floating point issues (though inputs are integers) and ensures correct indexing.

## worker: Run the code against the provided sample inputs to
The solution implements a block decomposition strategy to handle the multiple queries efficiently.
1.  **Sorting**: Both arrays $A$ and $B$ are sorted. This allows us to use binary search (`bisect_right`) to determine the split point for absolute differences in $O(\log N)$ time.
2.  **Mathematical Derivation**:
    For a query $(X, Y)$, we want $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
    By splitting the inner sum based on whether $B_j \le A_i$ or $B_j > A_i$, we derived the formula:
    $$ \text{Total} = 2 \sum_{i=1}^X (p_i \cdot A_i) - Y \sum_{i=1}^X A_i + X \sum_{j=1}^Y B_j - 2 \sum_{i=1}^X \text{prefB}[p_i] $$
    where $p_i$ is the count of elements in $B[1..Y]$ that are less than or equal to $A_i$. This is found using `bisect_right`.
3.  **Complexity**:
    -   Sorting takes $O(N \log N)$.
    -   Prefix sums take $O(N)$.
    -   For each query, we iterate through blocks of $A$. With block size $S \approx \sqrt{N}$, there are $\sqrt{N}$ blocks.
    -   Inside each block, we iterate up to $S$ elements and perform a binary search ($O(\log N)$).
    -   Total per query: $O(\sqrt{N} \log N)$.
    -   Total time: $O(N \log N + K \sqrt{N} \log N)$.
    -   With $N=10^5, K=10^4$, this is approximately $5 \times 10^7$ operations, which fits within the time limit.
4.  **Implementation Details**:
    -   Input reading is optimized using `sys.stdin.read`.
    -   Block decomposition is implemented by precomputing block start and end indices.
    -   The logic handles the summation terms carefully to ensure correct indexing and formula application.

## worker: Run the provided sample inputs to verify correctne
The solution implements a block decomposition strategy on array $A$ to handle the multiple queries efficiently.
1.  **Sorting**: Both arrays $A$ and $B$ are sorted. This allows us to use binary search (`bisect_right`) to determine the split point for absolute differences in $O(\log N)$ time.
2.  **Mathematical Derivation**:
    For a query $(X, Y)$, we want $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
    By splitting the inner sum based on whether $B_j \le A_i$ or $B_j > A_i$, we derived the formula:
    $$ \text{Total} = 2 \sum_{i=1}^X (p_i \cdot A_i) - Y \sum_{i=1}^X A_i + X \sum_{j=1}^Y B_j - 2 \sum_{i=1}^X \text{prefB}[p_i] $$
    where $p_i$ is the count of elements in $B[1..Y]$ that are less than or equal to $A_i$. This is found using `bisect_right`.
3.  **Complexity**:
    -   Sorting takes $O(N \log N)$.
    -   Prefix sums take $O(N)$.
    -   For each query, we iterate through blocks of $A$. With block size $S \approx \sqrt{N}$, there are $\sqrt{N}$ blocks.
    -   Inside each block, we iterate up to $S$ elements and perform a binary search ($O(\log N)$).
    -   Total per query: $O(\sqrt{N} \log N)$.
    -   Total time: $O(N \log N + K \sqrt{N} \log N)$.
    -   With $N=10^5, K=10^4$, this is approximately $5 \times 10^7$ operations, which fits within the time limit.
4.  **Implementation Details**:
    -   Input reading is optimized using `sys.stdin.read`.
    -   Block decomposition is implemented by precomputing block start and end indices.
    -   The logic handles the summation terms carefully to ensure correct indexing and formula application.

## worker: finalize
The solution implements a block decomposition strategy on array $A$ to handle the multiple queries efficiently.
1.  **Sorting**: Both arrays $A$ and $B$ are sorted. This allows us to use binary search (`bisect_right`) to determine the split point for absolute differences in $O(\log N)$ time.
2.  **Mathematical Derivation**:
    For a query $(X, Y)$, we want $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
    By splitting the inner sum based on whether $B_j \le A_i$ or $B_j > A_i$, we derived the formula:
    $$ \text{Total} = 2 \sum_{i=1}^X (p_i \cdot A_i) - Y \sum_{i=1}^X A_i + X \sum_{j=1}^Y B_j - 2 \sum_{i=1}^X \text{prefB}[p_i] $$
    where $p_i$ is the count of elements in $B[1..Y]$ that are less than or equal to $A_i$. This is found using `bisect_right`.
3.  **Complexity**:
    -   Sorting takes $O(N \log N)$.
    -   Prefix sums take $O(N)$.
    -   For each query, we iterate through blocks of $A$. With block size $S \approx \sqrt{N}$, there are $\sqrt{N}$ blocks.
    -   Inside each block, we iterate up to $S$ elements and perform a binary search ($O(\log N)$).
    -   Total per query: $O(\sqrt{N} \log N)$.
    -   Total time: $O(N \log N + K \sqrt{N} \log N)$.
    -   With $N=10^5, K=10^4$, this is approximately $5 \times 10^7$ operations, which fits within the time limit.
4.  **Implementation Details**:
    -   Input reading is optimized using `sys.stdin.read`.
    -   Block decomposition is implemented by precomputing block start and end indices.
    -   The logic handles the summation terms carefully to ensure correct indexing and formula application.
