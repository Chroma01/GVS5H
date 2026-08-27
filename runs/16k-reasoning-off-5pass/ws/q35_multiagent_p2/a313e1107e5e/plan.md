The problem asks for the length of the longest strictly increasing subsequence (LIS) in the prefix $A[1..R_i]$ such that all elements are $\le X_i$. This is a 2D range query problem: we want the LIS length considering only elements in index range $[1, R_i]$ and value range $[1, X_i]$.

We can solve this using an offline approach with a Fenwick Tree (Binary Indexed Tree) or Segment Tree. The key insight is that the standard $O(N \log N)$ LIS algorithm maintains an array `tails` where `tails[k]` is the smallest ending element of an increasing subsequence of length `k+1`. However, here we have a value constraint $X_i$.

A better approach is to process queries offline. Sort the queries by $R_i$. As we iterate through the array $A$ from $1$ to $N$, we maintain a data structure that can answer: "What is the maximum length of an increasing subsequence ending with a value $\le V$?" using only elements processed so far (indices $\le$ current $R_i$).

Actually, the condition is "subsequence of $A[1..R_i]$ with values $\le X_i$". This is equivalent to finding the LIS in the set $\{ A_j \mid 1 \le j \le R_i, A_j \le X_i \}$.

We can use a persistent segment tree or an offline sweep-line. Let's use an offline sweep-line with a Fenwick Tree over the values.
1. Coordinate compress the values of $A$ and all $X_i$ to the range $[1, M]$.
2. Store queries as $(R_i, X_i, \text{query_index})$.
3. Sort queries by $R_i$.
4. Iterate $i$ from $1$ to $N$. For each element $A_i$, we want to update our data structure. The standard LIS DP state is $DP[v] = $ max length of an increasing subsequence ending with value $v$. But we need the max length for values $\le X_i$.
   Let $L[v]$ be the length of the longest increasing subsequence ending with a value exactly $v$ (among processed elements). Then the answer for a query $(R, X)$ is $\max_{v \le X} L[v]$.
   When we process $A_i$, we can compute the longest increasing subsequence ending at $A_i$ using the current state: $len = 1 + \max_{v < A_i} L[v]$. Then we update $L[A_i] = \max(L[A_i], len)$.
   We can maintain the array $L$ in a Fenwick Tree that supports point updates and prefix maximum queries. The Fenwick Tree will store the maximum LIS length ending with a value in a certain range.
   
   Algorithm:
   1. Collect all unique values from $A$ and all $X_i$ for coordinate compression.
   2. Store queries grouped by $R_i$.
   3. Initialize a Fenwick Tree (for prefix max) over the compressed value domain.
   4. Iterate $i$ from $1$ to $N$:
      a. Let $v = A_i$. Find the max LIS length ending with a value $< v$ using the Fenwick Tree (query prefix max on $[1, \text{comp}(v)-1]$). Let this be $k$.
      b. The new length ending at $v$ is $k+1$.
      c. Update the Fenwick Tree at position $\text{comp}(v)$ with value $k+1$ (point update: `tree[comp(v)] = max(tree[comp(v)], k+1)`).
      d. For all queries with $R_i = i$, answer them by querying the Fenwick Tree for prefix max on $[1, \text{comp}(X_i)]$.
   5. Print answers in original order.

   Complexity: $O((N+Q) \log (\text{coordinate space}))$.