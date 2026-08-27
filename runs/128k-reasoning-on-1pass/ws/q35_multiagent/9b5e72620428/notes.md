
## ideation
The problem asks whether we can fill missing values (-1) in sequences $A$ and $B$ and permute $A$ such that $A_i + B_i = S$ for all $i$, with all elements non-negative.

1.  **Key Insight**: The condition $A_i + B_i = S$ for all $i$ means we need to pair each element of $A$ with an element of $B$ such that their sum is $S$. The $-1$s can be chosen freely to satisfy the sum $S$, provided $S$ is large enough to keep the chosen values non-negative. Specifically, if we pair a known value $a$ with a wildcard, we need $S \ge a$. Similarly for $b$ with a wildcard, we need $S \ge b$. Thus, we need $S \ge \max(\max(K_A), \max(K_B))$, where $K_A$ and $K_B$ are the lists of known (non -1) values in $A$ and $B$.

2.  **Wildcard Handling**: Let $U_A$ and $U_B$ be the number of $-1$s in $A$ and $B$. The number of known values are $|K_A| = N - U_A$ and $|K_B| = N - U_B$.
    If we pair $m$ known values from $A$ with known values from $B$ such that their sum is $S$, then the remaining $|K_A| - m$ known values in $A$ must be paired with wildcards in $B$, and the remaining $|K_B| - m$ known values in $B$ must be paired with wildcards in $A$.
    This requires:
    - $U_B \ge |K_A| - m \implies m \ge |K_A| + |K_B| - N$
    - $U_A \ge |K_B| - m \implies m \ge |K_A| + |K_B| - N$
    Let $req = |K_A| + |K_B| - N$. We need to find an integer $S \ge \max(\max(K_A), \max(K_B))$ such that the number of pairs $(a, b)$ with $a \in K_A, b \in K_B$ and $a+b=S$ is at least $req$.

3.  **Algorithm**:
    - If $req \le 0$, we have enough wildcards to cover all known values. We can always choose a large enough $S$, so output "Yes".
    - If $req = 1$, we need at least one pair $(a, b)$ with $a+b=S \ge \max(\max(K_A), \max(K_B))$. We can always choose $S = \max(K_A) + \max(K_B)$, which satisfies the condition. So output "Yes".
    - If $req \ge 2$, we need to find $S \ge \max(\max(K_A), \max(K_B))$ such that the number of pairs summing to $S$ is at least $req$. We can compute the frequency of each sum $a+b$ for $a \in K_A, b \in K_B$. If any sum $S \ge \max(\max(K_A), \max(K_B))$ has count $\ge req$, output "Yes". Otherwise, "No".

4.  **Complexity**: The number of distinct values in $K_A$ and $K_B$ is at most $N$. Iterating over all pairs takes $O(N^2)$ time, which is acceptable for $N \le 2000$.

## worker: Read input, extract known values $K_A, K_B$ and co
The problem requires pairing elements of $A$ and $B$ such that their sums are equal to some constant $S$, with all elements non-negative. Wildcards (-1) can be chosen freely to satisfy $A_i + B_i = S$ as long as $S \ge \max(\text{known values paired with wildcards})$. This implies we need $S \ge \max(\max(K_A), \max(K_B))$.

Let $req = |K_A| + |K_B| - N$ be the minimum number of known-known pairs required. If $req \le 0$, we have enough wildcards to cover all knowns, so we can always pick a large enough $S$ and output "Yes". If $req = 1$, we can always find a pair summing to $\max(K_A) + \max(K_B) \ge min\_S$, so "Yes". For $req \ge 2$, we must find an $S \ge min\_S$ that can be formed by at least $req$ disjoint pairs of known values. We compute the frequency of each possible sum $a+b$ for $a \in K_A, b \in K_B$. If any sum $S \ge min\_S$ has frequency $\ge req$, we output "Yes", otherwise "No". The algorithm runs in $O(N^2)$ time, which fits within the constraints ($N \le 2000$).
