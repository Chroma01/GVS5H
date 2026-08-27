The problem asks for the sum of the minimum operations to clear all elements in every subarray $A[L \dots R]$. The operation allows removing a contiguous range of *indices* $[l, r]$ if all values $A_l, \dots, A_r$ present on the board are removed. This is equivalent to finding the minimum path cover in a DAG where edges represent valid moves, but more simply, it relates to the structure of "connected components" of values. Specifically, $f(L,R)$ equals the number of connected components if we consider two adjacent indices $i, i+1$ in the range $[L, R]$ as connected if $A_i = A_{i+1}$, plus the number of distinct values that start a new "block" of unique values? No, let's re-evaluate based on the sample.
Sample 1: `1 3 1 4`.
(1,4): `1, 3, 1, 4`.
Op 1: remove indices [1,1] (value 1). Board: `3, 1, 4`. Wait, the rule says "erase all integers from l through r that are on the blackboard". If I pick $l=1, r=1$, I erase all occurrences of the value at index 1? No, the rule says "Choose integers $l, r$ ... erase all integers from $l$ through $r$ that are on the blackboard". This means if the board has values at positions $p_1, p_2, \dots$, and I choose range $[l, r]$, I remove any value $v$ such that its original index was in $[l, r]$? No, the problem says "Write $A_L \dots A_R$". Then "Choose $l, r$ such that every integer from $l$ through $r$ appears at least once". This implies $l$ and $r$ refer to the *values*? No, "integers from $l$ through $r$". The values are $A_i$. So $l$ and $r$ must be values?
Let's re-read carefully: "Choose integers $l, r$ with $l \le r$ such that every integer from $l$ through $r$ appears at least once on the blackboard."
Ah, $l$ and $r$ are **values**, not indices. The condition is that the set of values $\{l, l+1, \dots, r\}$ must be a subset of the values currently on the board. Then we erase all occurrences of these values.
So, in `1, 3, 1, 4`: Values present are $\{1, 3, 4\}$.
Can we pick $l=1, r=1$? Yes, 1 is present. Erase all 1s. Board: `3, 4`.
Can we pick $l=3, r=4$? Yes, 3 and 4 are present. Erase all. Board empty. Total 2 ops.
Is it possible to do 1 op? We need to pick $l, r$ such that $\{l, \dots, r\} \subseteq \{1, 3, 4\}$ and covers everything. The only way to cover $\{1, 3, 4\}$ with a contiguous range of integers is if the range is $[1, 4]$ (covering 1,2,3,4) but 2 is missing. Or $[1, 3]$ (missing 4). So we must split.
This looks like we are covering the set of distinct values $S$ with the minimum number of contiguous integer intervals $[l_k, r_k]$ such that $\bigcup [l_k, r_k] \supseteq S$.
Wait, the condition is "every integer from $l$ through $r$ appears at least once". This means the interval $[l, r]$ cannot contain any "holes" (missing values) relative to the current set of values on the board.
So, if the current set of values is $S$, we can pick an interval $[l, r]$ if $[l, r] \subseteq S$. We remove $[l, r]$ from $S$. We want to partition $S$ into minimum number of such intervals.
This is equivalent to: Given a set of integers $S$, find the minimum number of contiguous segments needed to cover $S$.
If $S = \{v_1, v_2, \dots, v_k\}$ with $v_1 < v_2 < \dots < v_k$, we can merge $v_i$ and $v_{i+1}$ into one segment if and only if $v_{i+1} = v_i + 1$.
Thus, $f(L, R)$ is simply the number of "gaps" in the sorted distinct values of $A[L \dots R]$ plus 1.
Specifically, if distinct values are $u_1 < u_2 < \dots < u_m$, then $f(L, R) = 1 + \sum_{i=1}^{m-1} [u_{i+1} \neq u_i + 1]$.
We need to sum this over all $1 \le L \le R \le N$.
Total Sum = $\sum_{L, R} (1 + \text{gaps}) = \sum_{L, R} 1 + \sum_{L, R} \sum_{i} [u_{i+1} \neq u_i + 1]$.
First part: $N(N+1)/2$.
Second part: Sum over all pairs $(L, R)$ of the number of gaps.
A gap occurs between value $x$ and $x+1$ if both $x$ and $x+1$ are present in $A[L \dots R]$ but they are not "adjacent" in the sorted list of distinct values? No.
The condition for a gap between $x$ and $x+1$ in the sorted distinct values of a subarray is:
Both $x$ and $x+1$ appear in the subarray, BUT there is no requirement for them to be adjacent in the subarray. The sorted distinct values are just the set of unique numbers.
If the set of unique numbers is $\{1, 3, 4\}$, sorted: $1, 3, 4$.
$1 \to 3$: gap ($3 \neq 1+1$).
$3 \to 4$: no gap ($4 = 3+1$).
Total gaps = 1. $f = 1+1=2$. Correct.
So $f(L, R) = (\text{count of distinct values}) - (\text{count of } x \text{ such that } x \in S \text{ and } x+1 \in S)$.
Wait.
If $S = \{1, 2, 4\}$. Sorted: $1, 2, 4$.
Pairs: $(1,2)$ -> $2=1+1$ (ok). $(2,4)$ -> $4 \neq 2+1$ (gap).
Number of gaps = 1. $f = 3 - 1 = 2$.
Formula: $f(L, R) = (\text{# distinct values}) - (\text{# pairs } (x, x+1) \text{ both present})$.
Let $D(L, R)$ be the number of distinct values in $A[L \dots R]$.
Let $G(L, R)$ be the number of $x$ such that $x \in A[L \dots R]$ and $x+1 \in A[L \dots R]$.
Then $f(L, R) = D(L, R) - G(L, R)$.
We need $\sum (D(L, R) - G(L, R)) = \sum D(L, R) - \sum G(L, R)$.

Algorithm:
1. Calculate $\sum D(L, R)$: Standard problem. For each element $A_i$, count how many subarrays $[L, R]$ contain $A_i$ as a unique instance? No, just count how many subarrays contain the value $v$.
Actually, $\sum D(L, R) = \sum_{v} (\text{number of subarrays containing } v)$.
For a fixed value $v$, let its occurrences be at indices $p_1, p_2, \dots, p_k$.
The number of subarrays containing at least one $v$ is Total Subarrays - Subarrays with no $v$.
Subarrays with no $v$ are those strictly between occurrences.
Alternatively, iterate $i$ from $1$ to $N$. Let $prev[i]$ be the index of the previous occurrence of $A_i$. The number of subarrays ending at $i$ that contain $A_i$ (and thus contribute to the count of distinct values for those subarrays) is $i - prev[i]$.
Summing this over all $i$ gives $\sum D(L, R)$.

2. Calculate $\sum G(L, R)$: Sum over all $x$ of (number of subarrays containing both $x$ and $x+1$).
For a fixed $x$, we need to count pairs $(L, R)$ such that $A[L \dots R]$ contains $x$ and $x+1$.
This is equivalent to: Total subarrays - subarrays missing $x$ - subarrays missing $x+1$ + subarrays missing both.
Or simpler: Iterate through the array. We can maintain the last seen positions of $x$ and $x+1$.
Actually, it's easier to sum over $x$. For a specific $x$, let positions of $x$ be $P_x$ and positions of $x+1$ be $P_{x+1}$.
We need to count pairs $(L, R)$ such that $\exists p \in P_x, q \in P_{x+1}$ with $L \le p \le R$ and $L \le q \le R$.
This is equivalent to: The interval $[L, R]$ must cover at least one $p$ and at least one $q$.
This is hard to sum directly for all $x$ efficiently if we do it naively.
Better approach for $\sum G(L, R)$:
Iterate $i$ from $1$ to $N$. Consider the contribution of the pair $(A_i, A_i+1)$? No, $G$ counts the existence of the pair of values.
Let's reverse the thinking. Instead of summing over $x$, sum over the array indices.
For a subarray $[L, R]$, $G(L, R)$ is the count of $x$ such that $x \in A[L \dots R]$ and $x+1 \in A[L \dots R]$.
This is $\sum_{x} [x \in S \land x+1 \in S]$.
We can compute this by iterating $i$ from $1$ to $N$. When we are at index $i$ (value $v = A_i$), we want to count how many $L \le i$ and $R \ge i$ exist such that the subarray $[L, R]$ contains $v$ and $v+1$.
Actually, it's easier to calculate the contribution of each "adjacent value pair" $(v, v+1)$.
For a fixed $v$, let the positions of $v$ be $u_1, u_2, \dots$ and $v+1$ be $w_1, w_2, \dots$.
We need the number of intervals $[L, R]$ that contain at least one $u$ and at least one $w$.
This is Total - (intervals with no $v$) - (intervals with no $v+1$) + (intervals with neither).
Intervals with no $v$: determined by gaps between $u$'s.
Intervals with no $v+1$: determined by gaps between $w$'s.
Intervals with neither: determined by gaps between $u$'s and $w$'s combined.
Since $N$ is up to $3 \times 10^5$, we cannot iterate all $v$ and do $O(N)$ work (that would be $O(N^2)$ worst case if all values are distinct or similar).
However, the sum of occurrences is $N$.
We can process each value $v$ in $O(\text{count}(v))$.
For a fixed $v$, let the sorted positions of $v$ be $U = [u_1, \dots, u_a]$ and $v+1$ be $W = [w_1, \dots, w_b]$.
We need to count pairs $(L, R)$ such that $[L, R] \cap U \neq \emptyset$ and $[L, R] \cap W \neq \emptyset$.
Let $S_U$ be the set of subarrays containing $v$, $S_W$ be the set containing $v+1$. We want $|S_U \cap S_W|$.
$|S_U \cap S_W| = |S_U| + |S_W| - |S_U \cup S_W|$.
$|S_U| = \sum_{k=0}^{a-1} (u_{k+1} - u_k - 1) \dots$ No, standard formula:
Number of subarrays containing at least one occurrence of a set of indices $U$:
Total subarrays $N(N+1)/2$.
Subarrays with NO occurrence: sum over gaps. If $U = \{u_1, \dots, u_a\}$, gaps are $0 \dots u_1-1$, $u_1+1 \dots u_2-1$, etc.
Length of gap before $u_1$ is $u_1-1$. Between $u_i, u_{i+1}$ is $u_{i+1}-u_i-1$. After $u_a$ is $N-u_a$.
Sum of lengths squared? No, number of subarrays in a gap of length $k$ is $k(k+1)/2$.
So we can compute $|S_U|$ and $|S_W|$ easily.
Now $|S_U \cup S_W|$: Subarrays containing at least one $v$ OR at least one $v+1$.
This is equivalent to Total - Subarrays containing NEITHER $v$ nor $v+1$.
Let $V = U \cup W$. Compute gaps in $V$. Sum $k(k+1)/2$ for each gap.
Then $|S_U \cap S_W| = |S_U| + |S_W| - (Total - \text{gaps}(V))$.
We can do this for each $v$. The total complexity will be proportional to $\sum (\text{count}(v) + \text{count}(v+1)) = O(N)$.
This is efficient enough.