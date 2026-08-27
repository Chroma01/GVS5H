The problem asks for the K-th largest value among $N^3$ combinations of the form $A_iB_j + B_jC_k + C_kA_i$. Since $N$ is up to $2 \times 10^5$, we cannot generate all values. However, $K$ is relatively small ($5 \times 10^5$), suggesting we can use binary search on the answer. For a candidate value $X$, we need to count how many triplets $(i, j, k)$ satisfy $A_iB_j + B_jC_k + C_kA_i \ge X$. This condition can be rewritten as $B_j(A_i + C_k) + C_kA_i \ge X$. By sorting arrays $A$ and $C$, for each pair $(j, k)$, we can efficiently count valid $i$'s or vice versa. Given the constraints and the structure, a binary search approach with an optimized counting function (likely $O(N^2 \log N)$ or $O(N^2)$ with bitsets/optimizations, but given $K$ is small, maybe we can iterate differently) is needed. Actually, since $K$ is small, we might not need to check all $N^2$ pairs if we can prune, but the standard approach for "K-th largest" with $N^3$ space is Binary Search on Answer + Counting. The counting function needs to be efficient. Let's re-evaluate: $B_j(A_i + C_k) + C_kA_i \ge X$. Fix $j$. We need $A_i + C_k \ge (X - C_kA_i)/B_j$. This looks like a 2D range query or similar. However, note that $K$ is small. Is it possible to just generate the top $K$? No, $N^3$ is too big.
Wait, let's look at the constraints again. $K \le 5 \times 10^5$. The binary search range is $[0, 3 \times 10^{18}]$. The check function must be fast.
Let's rewrite the inequality: $A_iB_j + B_jC_k + C_kA_i \ge X$.
This is symmetric in a way.
Actually, a common trick for this specific problem (which appears in contests like AtCoder) is that we can iterate over $j$ and $k$, and for each pair, find how many $i$ satisfy the condition. But that's $O(N^2 \log N)$ per check, which is too slow ($2 \cdot 10^5 \times 2 \cdot 10^5$ is huge).
Wait, $K$ is small. Maybe we can use the fact that we only need the top $K$.
Alternative approach: Sort $A, B, C$ descending. The largest values come from largest indices.
Actually, the standard solution for this specific problem (ABC 277 F? No, it's likely a specific contest problem) involves binary search on the answer. The check function: Count pairs $(i, k)$ such that there exists $j$ with $B_j(A_i+C_k) + C_kA_i \ge X$.
Let $S_{ik} = A_i + C_k$ and $P_{ik} = C_k A_i$. We need $B_j S_{ik} + P_{ik} \ge X \implies B_j \ge (X - P_{ik}) / S_{ik}$.
For a fixed pair $(i, k)$, we need the number of $j$ such that $B_j \ge \text{threshold}$. If we sort $B$, we can find this count in $O(\log N)$.
Total complexity of check: $O(N^2 \log N)$. With $N=2 \cdot 10^5$, $N^2$ is $4 \cdot 10^{10}$, which is TLE.
Is there a constraint I missed? $K \le 5 \cdot 10^5$.
Ah, maybe we don't need to check all $N^2$ pairs. We only care if the count $\ge K$.
But we don't know which pairs contribute.
Wait, if $N$ is large, maybe the intended solution is different.
Let's reconsider the expression: $A_iB_j + B_jC_k + C_kA_i$.
This is $(A_i + C_k)B_j + C_kA_i$.
If we sort $A, B, C$ descending.
The maximum value is roughly $A_{max}B_{max} + B_{max}C_{max} + C_{max}A_{max}$.
Is it possible that we only need to check $O(K)$ pairs? No.
Let's look at similar problems. This looks like "K-th largest sum of three arrays" but with a specific cross term.
Actually, if $K$ is small, maybe we can use a priority queue to generate the top $K$ values?
State: $(i, j, k)$. Start with $(0, 0, 0)$ (using 0-based sorted indices).
When we pop $(i, j, k)$, we can push neighbors. But the dependency is complex.
However, notice the structure: $f(i, j, k) = A_i B_j + B_j C_k + C_k A_i$.
If we fix $j$, we want to maximize $A_i B_j + C_k A_i + B_j C_k = B_j(A_i+C_k) + C_k A_i$.
Let $g(i, k) = A_i + C_k$ and $h(i, k) = C_k A_i$. We want $B_j g(i, k) + h(i, k)$.
This doesn't decompose nicely into $f(i) + f(j) + f(k)$.
Wait, there is a known technique for this specific problem (AtCoder ABC 327 F? No).
Let's re-read the constraints. $N \le 2 \cdot 10^5$, $K \le 5 \cdot 10^5$.
The binary search approach with $O(N^2)$ check is definitely too slow.
Is it possible that we can iterate over $j$ and use a data structure?
For a fixed $j$, we want to count pairs $(i, k)$ such that $B_j(A_i+C_k) + C_kA_i \ge X$.
Let $Y = X - B_j(A_i+C_k)$. We need $C_k A_i \ge Y$.
This still feels like $O(N^2)$.
Maybe the constraints on $A_i, B_i, C_i$ help? They are up to $10^9$.
Wait, could it be that we only need to consider the top $M$ elements of each array where $M \approx K$?
If we take the top $K$ elements of $A$, $B$, and $C$, does the answer lie within their combinations?
Suppose the optimal triplet uses an index $i$ that is not in the top $K$ of $A$. Then $A_i$ is small.
$A_i B_j + B_j C_k + C_k A_i = B_j(A_i+C_k) + C_k A_i$.
If $A_i$ is very small, the term $C_k A_i$ is small, and $B_j A_i$ is small.
However, $B_j C_k$ is independent of $i$. So if we pick a very small $A_i$, the value is $B_j C_k + \text{small}$.
The maximum possible value of $B_j C_k$ is bounded by the top elements of $B$ and $C$.
If we fix $j$ and $k$, the best $i$ is the one that maximizes $A_i(B_j + C_k)$. Since $B_j, C_k \ge 0$ (actually $\ge 1$), we should pick the largest $A_i$.
So for any fixed pair $(j, k)$, the optimal $i$ is the index with the largest $A_i$.
Wait, the problem asks for the K-th largest among ALL $N^3$ combinations.
It does NOT ask to maximize over $i$ for fixed $j,k$. It asks for the K-th largest of the set $\{ A_iB_j + B_jC_k + C_kA_i \mid \forall i,j,k \}$.
So we have $N^2$ pairs of $(j, k)$, and for each pair, we have $N$ values corresponding to $i=1..N$.
Since $A_i \ge 1$, the term $A_i(B_j+C_k)$ is increasing with $A_i$.
Thus, for a fixed $(j, k)$, the values are sorted by $A_i$. The largest value for $(j, k)$ is with the largest $A_i$, the second largest with the second largest $A_i$, etc.
So, the set of all values is the union over all $(j, k)$ of the sequence $\{ A_{(1)}B_j + B_jC_k + C_kA_{(1)}, A_{(2)}B_j + B_jC_k + C_kA_{(2)}, \dots \}$ where $A_{(1)} \ge A_{(2)} \dots$.
Actually, since $B_j, C_k \ge 1$, the coefficient of $A_i$ is $B_j + C_k \ge 2$.
So for a fixed $(j, k)$, the values are strictly increasing with $A_i$.
Therefore, the largest values in the entire set must come from the largest values of $A$.
Specifically, if we want the K-th largest, we only need to consider the top $K$ values of $A$?
Let's verify. Suppose we have $N=100, K=5$.
We have $100 \times 100 = 10000$ pairs of $(j, k)$.
For each pair, we have 100 values.
The largest value overall is $A_{max} B_{max} + B_{max} C_{max} + C_{max} A_{max}$.
The next largest could be $A_{max} B_{2nd} + \dots$ or $A_{2nd} B_{max} + \dots$.
In general, the top $K$ values of the entire set must involve indices from the top $K$ of $A$, top $K$ of $B$, and top $K$ of $C$?
Not necessarily top $K$ of $C$ because $C_k$ appears in $B_j C_k$ and $C_k A_i$.
But notice: For a fixed $j$, the term $B_j C_k + C_k A_i = C_k (B_j + A_i)$.
This is increasing in $C_k$.
So for fixed $i, j$, the best $k$ is the one with largest $C_k$.
Similarly, for fixed $j, k$, the best $i$ is the one with largest $A_i$.
And for fixed $i, k$, the best $j$ is the one with largest $B_j$.
This implies that the global maximum is at $(i_{max}, j_{max}, k_{max})$.
What about the K-th largest?
Since the function is monotonic in each variable (assuming positive values), the top $K$ values will likely be formed by indices from the top $K$ of each array.
Let's assume we only need to consider the top $M$ elements of $A$, $B$, and $C$, where $M$ is slightly larger than $K$.
If we sort $A, B, C$ descending, and take the first $M$ elements, the number of triplets is $M^3$.
If $M \approx K^{1/3}$? No, $K$ is up to $5 \cdot 10^5$. $M^3 \ge K \implies M \ge 800$.
If we take top $800$ of each, $800^3 = 512,000,000$, which is too big to sort.
But wait, we established that for fixed $j, k$, the values are sorted by $A_i$.
So we have $N^2$ lists, each of size $N$, sorted.
We want the K-th largest element in the union of these lists.
This is equivalent to merging $N^2$ sorted lists and finding the K-th element.
Since $N^2$ is huge, we can't merge all.
However, we only need the top $K$.
We can use a priority queue.
Start with the largest element from each list? No, there are $N^2$ lists.
But notice the structure: The lists are generated by $(j, k)$.
The largest element of list $(j, k)$ is $val(j, k, 1) = A_1 B_j + B_j C_k + C_k A_1$.
The second largest is $val(j, k, 2)$, etc.
We can put all "heads" of the lists into a priority queue. But there are $N^2$ heads.
We can't put $N^2$ items in the PQ.
However, observe that the "head" of list $(j, k)$ depends on $j$ and $k$.
Maybe we can iterate on $j$?
For a fixed $j$, we have $N$ lists (one for each $k$).
The head of list $(j, k)$ is $A_1 B_j + B_j C_k + C_k A_1 = B_j(A_1+C_k) + C_k A_1$.
This is a function of $k$. Let's call it $f_j(k)$.
Since $A_1, B_j$ are fixed, and $C_k$ is sorted descending, is $f_j(k)$ sorted?
$f_j(k) = B_j A_1 + C_k (B_j + A_1)$.
Since $B_j, A_1 \ge 1$, the coefficient of $C_k$ is positive.
So for a fixed $j$, as $k$ increases (index in sorted $C$), $C_k$ decreases, so $f_j(k)$ decreases.
Thus, for a fixed $j$, the list of values over $k$ (with optimal $i=1$) is sorted descending.
But we have $N$ choices for $i$ for each $k$.
Actually, the full set of values for fixed $j$ is $\{ A_i B_j + B_j C_k + C_k A_i \mid i, k \}$.
For fixed $j$, this is a 2D grid of values.
Row $k$ (fixed $k$, varying $i$) is sorted by $i$.
Column $i$ (fixed $i$, varying $k$) is sorted by $k$.
So for a fixed $j$, we have an $N \times N$ matrix where rows and columns are sorted descending.
We want the K-th largest value in the union of these matrices for all $j$.
Since the matrix for each $j$ is sorted, and the values generally decrease as $j$ increases (since $B_j$ is in the positive terms), the largest values are concentrated in the top-left of the matrices for small $j$.
Specifically, the global maximum is at $j=1, i=1, k=1$.
The next candidates are neighbors in the $(i, j, k)$ space.
We can use a priority queue to explore the state space $(i, j, k)$.
State: $(i, j, k)$.
Initial: Push $(1, 1, 1)$.
When popping $(i, j, k)$, we can push neighbors.
Which neighbors?
Since the function is monotonic, the next largest values must be adjacent to the current one in the sorted order of indices.
Specifically, if we sort $A, B, C$ descending, then $A_1 \ge A_2 \dots$, etc.
The value $V(i, j, k) = A_i B_j + B_j C_k + C_k A_i$.
Consider $(i+1, j, k)$, $(i, j+1, k)$, $(i, j, k+1)$.
Are these the only candidates?
Not necessarily, because the function is not separable.
However, in such "K-th largest in monotonic grid" problems, we usually push $(i+1, j, k)$, $(i, j+1, k)$, $(i, j, k+1)$ and handle duplicates.
But the state space is $N^3$. We only visit $K$ states.
Since $K \le 5 \cdot 10^5$, we can visit $K$ states.
Algorithm:
1. Sort $A, B, C$ descending.
2. Use a min-heap (or max-heap? We want K-th largest, so we extract largest K times) to store candidates.
   Actually, we want the K-th largest. So we extract the largest, then the second largest, etc., K times.
   Use a Max-Heap.
3. Push $(1, 1, 1)$ with value $V(1, 1, 1)$.
4. Maintain a `visited` set to avoid duplicates.
5. Loop K times:
   a. Pop max $(i, j, k)$ with value $V$.
   b. Record $V$ as the current K-th largest (on the K-th iteration).
   c. Push neighbors $(i+1, j, k)$, $(i, j+1, k)$, $(i, j, k+1)$ if valid and not visited.
6. Output the K-th extracted value.

Complexity: $O(K \log K)$.
$K = 5 \cdot 10^5$, $\log K \approx 19$. Operations $\approx 10^7$, well within time limits (usually 2s for $10^8$ ops).
Memory: $O(K)$ for the heap and visited set. $5 \cdot 10^5$ integers is fine.
Wait, is it guaranteed that the K-th largest is reachable by only moving +1 in indices?
Yes, because if we have a value at $(i, j, k)$, any value at $(i', j', k')$ with $i' \le i, j' \le j, k' \le k$ is $\ge V(i, j, k)$.
The set of values is a "lattice" where values decrease as indices increase.
The standard algorithm for K-th largest in such a structure is exactly this BFS on the lattice.
We start at $(1,1,1)$. The neighbors are $(2,1,1), (1,2,1), (1,1,2)$.
When we pop $(i,j,k)$, we add $(i+1,j,k), (i,j+1,k), (i,j,k+1)$.
We must ensure we don't add duplicates. A set of visited tuples $(i,j,k)$ works.
Since $K$ is up to $5 \cdot 10^5$, the number of visited states is $K$.
The coordinates are up to $N=2 \cdot 10^5$.
Tuple hashing in Python is efficient enough.
One detail: The problem uses 1-based indexing in description, but 0-based in implementation is easier.
Constraints: $A_i, B_i, C_i \ge 1$. So monotonicity holds.
Is it possible that $N$ is small and $K$ is large? $K \le N^3$. If $N=2$, $N^3=8$, $K \le 8$.
If $N$ is large, $K$ is limited to $5 \cdot 10^5$.
So the number of states we visit is $\min(K, N^3)$.
This approach seems correct and efficient.