
## ideation
The core difficulty is that generating all $N^3$ values is impossible ($N \le 2 \times 10^5$). However, $K$ is small ($K \le 5 \times 10^5$). This suggests that the K-th largest value depends only on a small subset of the largest elements from each sequence.

**Candidate Approaches:**
1.  **Subset Pruning (Greedy):**
    *   Sort $A, B, C$ in descending order.
    *   The maximum possible value is $A_{max}B_{max} + B_{max}C_{max} + C_{max}A_{max}$.
    *   The K-th largest value cannot be formed using an element from $A$ that is smaller than the $(K^{1/3})$-th largest element of $A$, because even if we pair it with the two largest elements of $B$ and $C$, there are fewer than $K$ combinations involving only "better" elements from $B$ and $C$ that could push this specific combination into the top $K$.
    *   More rigorously: If we take the top $M$ elements from each sorted array, where $M \approx K^{1/3}$, the number of combinations is $M^3 \approx K$. Any combination involving an element outside the top $M$ of any sequence will likely be smaller than the smallest value in the top $M^3$ combinations of the top $M$ elements.
    *   We need to determine the exact cutoff $M$. A safe bound is $M = \lceil K^{1/3} \rceil + 2$ or simply iterate $M$ such that $M^3 \ge K$. Given $K=5 \times 10^5$, $M \approx 80$.
    *   Algorithm:
        1. Sort $A, B, C$ descending.
        2. Take top $M$ elements from each (where $M$ is chosen such that $M^3 \ge K$, e.g., $M=800$ to be safe, or dynamically calculated).
        3. Generate all $M^3$ sums.
        4. Sort the generated sums descending.
        5. Return the $(K-1)$-th element (0-indexed).

2.  **Binary Search on Answer:**
    *   Possible values are large, but we can binary search on the value $X$.
    *   Check function: Count how many tuples $(i, j, k)$ satisfy $A_iB_j + B_jC_k + C_kA_i \ge X$.
    *   Counting is hard: $A_iB_j + B_jC_k + C_kA_i \ge X \iff B_j(A_i+C_k) + C_kA_i \ge X$. This doesn't easily separate variables to allow $O(N \log N)$ or $O(N)$ counting.
    *   This approach is likely too complex to implement efficiently compared to the subset pruning.

**Pitfalls:**
*   **Off-by-one errors:** Determining the exact size of the subset to take. If we take too few, we miss the K-th value. If we take too many, we TLE/MLE (though $M=800$ is fine for $N=200,000$).
*   **Integer Overflow:** The sums can exceed $2^{31}-1$. Python handles large integers automatically, so this is not an issue in Python, but worth noting for other languages.
*   **Sorting Time:** Sorting $M^3$ elements where $M \approx 800$ results in $\approx 5 \times 10^8$ elements, which is too slow. We must ensure $M$ is small enough.
    *   $K = 5 \times 10^5$.
    *   $\sqrt[3]{5 \times 10^5} \approx 79.3$.
    *   So taking top $80$ elements gives $80^3 = 512,000$ combinations, which is just enough.
    *   To be safe against edge cases where the distribution is skewed, we might take slightly more, but $M=100$ gives $1,000,000$ operations, which is acceptable in Python if done efficiently (sorting 1M ints takes ~0.5s).
    *   Let's calculate $M$ such that $M^3 \ge K$. $M = \lceil K^{1/3} \rceil$.
    *   Wait, is it guaranteed that the top $K$ values come from the top $M$ of each?
        *   Consider $A=[10, 1], B=[10, 1], C=[10, 1]$.
        *   Values: $10\cdot10+10\cdot10+10\cdot10 = 300$ (1 combo), $10\cdot10+10\cdot1+1\cdot10 = 110$ (2 combos), etc.
        *   The values drop off quickly.
        *   The logic holds: The $K$-th largest value $V$ must satisfy that there are at least $K$ triples with value $\ge V$.
        *   If we restrict $A$ to top $M$, $B$ to top $M$, $C$ to top $M$, we generate a set $S$. Let $min(S)$ be the smallest value in $S$.
        *   We need to ensure that no value outside $S$ is greater than the $K$-th largest value in $S$.
        *   Actually, a simpler bound: The $K$-th largest value is formed by some $A_i, B_j, C_k$. If we sort $A, B, C$ descending, can $i$ be greater than $K$?
        *   Suppose the optimal triple uses $A_i$ where $i > K$. Then there are at least $K$ elements in $A$ larger than $A_i$. Even if we pair $A_i$ with the largest $B$ and largest $C$, we get one value. The values formed by $A_1 \dots A_K$ with $B_1, C_1$ alone might not cover $K$ values if $B$ and $C$ vary.
        *   Correct Logic: The number of triples $(i, j, k)$ such that $A_i \ge A_{M+1}$ is $M \cdot N \cdot N$. This is huge.
        *   The constraint is on the *value* of the expression.
        *   Let's reconsider the bound. If we take top $M$ from each, total combinations $M^3$.
        *   Is it possible that the $K$-th largest value comes from $A_{M+1}, B_1, C_1$?
        *   Yes, if $A_{M+1}$ is very close to $A_M$ and $B_1, C_1$ are huge.
        *   However, if we take $M$ such that $M^3 \ge K$, is it sufficient?
        *   Counter-example logic: Suppose $A=[100, 99, \dots]$, $B=[100, \dots]$, $C=[100, \dots]$.
        *   The values are roughly $30000$. The difference between $A_1$ and $A_{M+1}$ might be small.
        *   But if we take $M$ such that $M^3 \ge K$, then the set of combinations from the top $M$ of each contains at least $K$ elements.
        *   Does it contain the *largest* $K$ elements?
        *   Not necessarily. It's possible that $A_{M+1}B_1C_1$ (conceptually, though the formula is mixed) is larger than some combination in the top $M$ set?
        *   Actually, the function $f(i,j,k) = A_iB_j + B_jC_k + C_kA_i$ is monotonic in each variable if the others are fixed and positive.
        *   Since $A_i, B_j, C_k \ge 1$, increasing any index (moving to a smaller value in sorted array) decreases the sum.
        *   Therefore, the largest values are formed by the smallest indices.
        *   Specifically, if we have a set of indices $I, J, K$, the value is maximized when indices are minimized.
        *   We want the $K$-th largest. This corresponds to finding a threshold $T$ such that the number of triples with value $\ge T$ is $\ge K$.
        *   Consider the set of all triples $(i, j, k)$ where $i, j, k \le M$. This set has size $M^3$.
        *   If $M^3 \ge K$, is the $K$-th largest value of the whole set equal to the $K$-th largest value of this subset?
        *   Yes, because any triple with $i > M$ (or $j > M$ or $k > M$) involves an element strictly smaller than the $M$-th element of that sequence.
        *   Let $A_{M+1} < A_M$. Then for any $j, k$, $A_{M+1}B_j + \dots < A_M B_j + \dots$.
        *   However, we need to compare a "mixed" triple $(M+1, 1, 1)$ with a "deep" triple $(M, M, M)$.
        *   It is possible that $(M+1, 1, 1) > (M, M, M)$?
            *   $A_{M+1}B_1 + B_1C_1 + C_1A_{M+1} = 2 A_{M+1} B_1 + B_1 C_1$ (assuming symmetry for simplicity).
            *   $A_M B_M + B_M C_M + C_M A_M$.
            *   If $B_1, C_1$ are huge and $A_M, B_M, C_M$ are small (but $A_{M+1}$ is close to $A_M$), then yes, the "mixed" triple could be larger.
        *   **Correction**: The simple $M^3 \ge K$ logic is flawed if the sequences are not uniform.
        *   However, note the constraints: $K \le 5 \times 10^5$.
        *   If we take $M$ such that $M^3 \ge K$, say $M=80$, we generate 512,000 values.
        *   Is it possible that the true K-th largest is outside this set?
        *   Let's think about the rank. The total number of triples is $N^3$. We want the $K$-th.
        *   If we sort $A, B, C$ descending.
        *   The maximum value is at $(1,1,1)$.
        *   The next largest are permutations of $(1,1,2)$, $(1,2,1)$, $(2,1,1)$, etc.
        *   Essentially, we are looking for the $K$-th element in the sorted list of $A_i B_j + B_j C_k + C_k A_i$.
        *   Since $K$ is small, the indices $i, j, k$ involved in the top $K$ values cannot be arbitrarily large.
        *   Specifically, if we take $M = \lceil K^{1/3} \rceil + 2$, is it guaranteed?
        *   Let's check the worst case. Suppose $A = [10^9, 10^9, \dots, 1, \dots]$, $B, C$ same.
        *   Then many combinations give the same max value. We just need enough of them.
        *   Suppose $A = [100, 99, 98, \dots]$, $B, C$ same.
        *   The values decrease as indices increase.
        *   The "density" of large values is highest near $(1,1,1)$.
        *   It is a known result for this type of problem (K-th largest sum/product of 3 arrays) that taking top $K^{1/3}$ is sufficient.
        *   Why? Because the number of triples with at least one index $> M$ is $N^3 - (N-M)^3 \approx 3N^2 M$. This doesn't help directly.
        *   Let's re-evaluate: We want to find $K$ triples with the largest sums.
        *   If we pick $M$ such that $M^3 \ge K$, the set $S = \{(i,j,k) | i,j,k \le M\}$ has size $\ge K$.
        *   Let $v_{K}$ be the $K$-th largest value in the full set.
        *   Let $v'_{K}$ be the $K$-th largest value in $S$.
        *   Clearly $v'_{K} \ge v_{K}$ because $S$ is a subset of the full set, so the $K$-th largest in a subset is $\ge$ the $K$-th largest in the superset (since the subset might miss some very small values, pushing the rank up, or miss some large values? No, if we remove elements, the $K$-th largest can only increase or stay same if we remove elements smaller than the $K$-th. If we remove elements larger than the $K$-th, the $K$-th decreases).
        *   Wait, $S$ is the set of "best" candidates. If $S$ contains the top $K$ elements of the full set, then $v'_{K} = v_{K}$.
        *   Does $S$ contain the top $K$?
        *   Suppose there is a triple $t = (i, j, k)$ with $i > M$ such that $val(t) > v'_{K}$.
        *   Then $val(t)$ must be larger than the smallest value in the top $K$ of $S$.
        *   But $val(t) = A_i B_j + B_j C_k + C_k A_i$. Since $i > M$, $A_i \le A_{M+1}$.
        *   Also, in $S$, we have triples like $(M, M, M)$.
        *   If $A_{M+1}$ is significantly smaller than $A_M$, then $val(t)$ will be small.
        *   If $A_{M+1} \approx A_M$, then the values are similar.
        *   The critical observation: The number of triples with value $\ge X$ is monotonic.
        *   Actually, there is a stronger bound. If we take $M$ such that $M^3 \ge K$, is it possible that a triple with an index $> M$ is in the top $K$?
        *   Consider $N=10, K=10$. $M=3$ ($3^3=27 \ge 10$).
        *   Could $(4, 1, 1)$ be in the top 10?
        *   If $(4, 1, 1)$ is in top 10, then there are at most 9 values larger than it.
        *   But we have $3 \times 3 \times 3 = 27$ combinations in $S$.
        *   If $(4, 1, 1)$ is larger than the 10th largest in $S$, then $val(4,1,1) > val_{10}(S)$.
        *   This implies that at least 10 values in $S$ are smaller than $val(4,1,1)$.
        *   But $val(4,1,1)$ uses $A_4$. In $S$, we use $A_1, A_2, A_3$.
        *   If $A_4$ is very close to $A_3$, then $val(4,1,1) \approx val(3,1,1)$.
        *   $val(3,1,1)$ is in $S$.
        *   So $val(4,1,1)$ is comparable to elements in $S$.
        *   It seems we might need to take slightly more than $K^{1/3}$.
        *   However, given $K \le 5 \times 10^5$, let's pick $M = 100$. $100^3 = 1,000,000$.
        *   Generating 1 million integers and sorting them is fast enough in Python (approx 0.5-1 second).
        *   Memory: 1 million ints is ~4MB-8MB. Trivial.
        *   So the strategy:
            1. Sort A, B, C descending.
            2. Take top $M=100$ (or dynamically $M$ such that $M^3 \ge K$ and $M \le N$). Let's use $M = \min(N, \lceil K^{1/3} \rceil + 5)$ to be safe.
            3. Generate all sums.
            4. Sort and pick K-th.

**Refinement on M:**
$K=500,000$. $\sqrt[3]{K} \approx 79$.
If we take $M=80$, $80^3 = 512,000$.
Is it possible that the 500,000-th largest value involves index 81?
If $A_{81}$ is slightly smaller than $A_{80}$, the value drops.
But if $B_1, C_1$ are huge, $A_{81}(B_1+C_1) + B_1C_1$ could be close to $A_{80}(B_80+C_80) + B_80C_80$.
However, $B_1, C_1$ are the largest. $B_{80}, C_{80}$ are much smaller.
So $val(81, 1, 1) \approx A_{81} \times (\text{large}) + \text{large}$.
$val(80, 80, 80) \approx A_{80} \times (\text{small}) + \text{small}$.
Clearly $val(81, 1, 1) > val(80, 80, 80)$.
So the "mixed" triples with small indices in B and C but large indices in A can be quite large.
Wait, my previous assumption that "top $M$ of each" covers everything is wrong if we only look at the cube of the top $M$.
The set of top $K$ values might include triples like $(M+1, 1, 1)$.
How many such triples are there?
Triples with $j=1, k=1$ and $i=1 \dots N$. There are $N$ such triples.
If $K$ is large, we might need to consider these.
BUT, $K \le 5 \times 10^5$.
If we take $M$ such that $M^3 \ge K$, do we cover $(M+1, 1, 1)$?
No, $(M+1, 1, 1)$ is not in the set $\{1..M\}^3$.
So we need a different bound.
Actually, the number of triples with $j=1, k=1$ is $N$.
The number of triples with $j=1, k=2$ is $N$.
Total triples with $j=1$ is $N^2$.
This is too big.
However, notice the structure: $A_i B_j + B_j C_k + C_k A_i$.
If $j=1, k=1$, value is $A_i B_1 + B_1 C_1 + C_1 A_i = B_1 C_1 + A_i(B_1+C_1)$.
This is linear in $A_i$.
So for fixed $j, k$, the values are sorted by $A_i$.
We are looking for the global K-th largest.
Since $K$ is small ($5 \times 10^5$), the indices $i, j, k$ involved in the top $K$ values cannot be too large.
Specifically, if we sort $A, B, C$, the indices $i, j, k$ for the top $K$ values will be within some range $[1, M]$.
What is $M$?
Consider the case where $A, B, C$ are all identical and decreasing.
Then the values are symmetric. The top $K$ values will come from indices where $i, j, k$ are small.
Is it possible that $i$ goes up to $N$ while $j, k$ are 1?
Value: $A_i(B_1+C_1) + B_1C_1$.
Compare with $A_1 B_2 + B_2 C_2 + C_2 A_1$.
If $A_1 \approx A_2 \approx \dots \approx A_N$, then $A_i$ is constant.
Then the value depends on $B_j, C_k$.
If $B, C$ are also constant, all values are equal. Then any $K$ works.
If $B, C$ decrease, then $B_1, C_1$ are max.
Then $A_i(B_1+C_1) + B_1C_1$ is maximized when $A_i$ is max (i.e., $i=1$).
So even if $A_i$ is constant, we prefer $i=1$.
If $A_i$ decreases, we prefer small $i$.
So the indices $i, j, k$ for the top $K$ values will be small.
How small?
The number of triples with $\max(i, j, k) \le M$ is $M^3$.
If $M^3 \ge K$, does that mean the top $K$ are all within this box?
Suppose there is a triple $(M+1, 1, 1)$ in the top $K$.
Then its value is $\ge$ the $K$-th largest value.
But we have $M^3$ triples in the box $[1, M]^3$.
The smallest value in the box is roughly $A_M B_M + \dots$.
The value of $(M+1, 1, 1)$ is $A_{M+1}(B_1+C_1) + B_1C_1$.
If $A, B, C$ are strictly decreasing, $A_{M+1} < A_M$, $B_1 > B_M$, $C_1 > C_M$.
It is possible that $(M+1, 1, 1) > (M, M, M)$.
So the box $[1, M]^3$ might not contain the top $K$ if $M^3 = K$.
However, if we choose $M$ such that $M^3 \gg K$, say $M = K^{1/3} \times 2$?
Or simply, since $K \le 500,000$, let's try $M = 100$.
$100^3 = 1,000,000 > K$.
Is it possible that $(101, 1, 1)$ is in the top 500,000?
If $(101, 1, 1)$ is in the top 500,000, then there are at most 499,999 values larger than it.
But we have $100^3 = 1,000,000$ values in the box.
Even if all values in the box are smaller than $(101, 1, 1)$, then $(101, 1, 1)$ would be rank 1,000,001.
So for $(101, 1, 1)$ to be in top 500,000, at least 500,000 values in the box must be smaller than it.
This requires $A_{101}(B_1+C_1) + B_1C_1 > \text{many combinations in box}$.
But the box contains $(1, 1, 1)$ which is the global maximum.
And $(100, 1, 1)$, $(1, 100, 1)$, etc.
The values in the box are generally much larger than those outside because they use larger $B, C$ indices? No, smaller indices in $B, C$ give larger values.
The box $[1, 100]^3$ uses $B_1 \dots B_{100}$.
The triple $(101, 1, 1)$ uses $B_1, C_1$.
The triple $(100, 100, 100)$ uses $B_{100}, C_{100}$.
If $B_{100}$ is much smaller than $B_1$, then $(100, 100, 100)$ is small.
But $(101, 1, 1)$ uses $B_1, C_1$.
So $(101, 1, 1)$ could be larger than $(100, 100, 100)$.
But is it larger than $(1, 100, 100)$?
$(1, 100, 100) = A_1 B_{100} + B_{100} C_{100} + C_{100} A_1$.
$(101, 1, 1) = A_{101} B_1 + B_1 C_1 + C_1 A_{101}$.
If $A_1 \approx A_{101}$, then $(101, 1, 1) \approx A(B_1+C_1) + B_1C_1$.
$(1, 100, 100) \approx A(B_{100}+C_{100}) + B_{100}C_{100}$.
Since $B_1 \gg B_{100}$, $(101, 1, 1)$ is likely much larger.
So $(101, 1, 1)$ could be very high ranked.
But wait, we also have $(1, 1, 101)$, $(101, 1, 1)$, $(101, 101, 1)$, etc.
Basically, if we take $M=100$, we generate $10^6$ values.
The number of values outside the box is huge, but are they larger than the smallest value in the box?
The smallest value in the box is roughly using $A_{100}, B_{100}, C_{100}$.
The largest value outside the box (e.g., $(101, 1, 1)$) uses $A_{101}, B_1, C_1$.
If $B_1 \gg B_{100}$, then $(101, 1, 1)$ is huge.
So we might miss the top $K$ if we only take $[1, 100]^3$ and $K=500,000$?
Wait, if $(101, 1, 1)$ is huge, it should be in the top $K$.
But $(101, 1, 1)$ is NOT in $[1, 100]^3$.
So my assumption that $M=100$ is sufficient is WRONG if the sequences are not uniform.
We need to include indices that give large values.
But $K$ is small.
Actually, if $B_1$ is huge, then $A_i B_1$ dominates.
The values $A_i B_1 + B_1 C_1 + C_1 A_i$ are sorted by $A_i$.
So for $j=1, k=1$, the top values are $A_1, A_2, \dots$.
There are $N$ such values.
Similarly for $j=1, k=2$, etc.
The total number of "lines" where one index is fixed to 1 is $N \times N$.
This is $4 \times 10^{10}$, too big.
BUT, we only need top $K$.
If $K=500,000$, we need to consider combinations.
Notice that if $B_1$ is very large, then $A_i B_1$ is the dominant term.
Then the order is determined by $A_i$.
The top $K$ values would be roughly the top $K$ values of $A_i B_1 + \dots$.
This suggests we need to consider $A_1 \dots A_K$?
No, because we have 3 variables.
Let's reconsider the $M = \lceil K^{1/3} \rceil$ logic.
Is it possible that the problem constraints or the nature of the sum ensures that $M \approx K^{1/3}$ is enough?
In competitive programming, for "K-th largest sum of 3 arrays", the standard solution is indeed taking top $K^{1/3}$.
Why?
Because if we sort $A, B, C$, then $A_i B_j + B_j C_k + C_k A_i \le A_1 B_1 + B_1 C_1 + C_1 A_1$.
Also, if we fix $j, k$, the function is linear in $A_i$.
The number of triples with value $\ge V$ is what we count.
If we take $M$ such that $M^3 \ge K$, then the set $S = \{ (i,j,k) : i,j,k \le M \}$ has size $\ge K$.
Let $v_{min}$ be the minimum value in $S$.
Is it possible that there exists a triple $t \notin S$ with $val(t) > v_{min}$?
Yes, as discussed.
BUT, if $val(t) > v_{min}$, then $t$ is "better" than the worst of the top $M^3$.
If there are many such $t$, then the true $K$-th largest might be $> v_{min}$.
However, note that if $t = (M+1, 1, 1)$, then $val(t) \approx A_{M+1}(B_1+C_1) + B_1C_1$.
Compare with $t' = (M, 1, 1) \in S$. $val(t') = A_M(B_1+C_1) + B_1C_1$.
Since $A_M \ge A_{M+1}$, $val(t') \ge val(t)$.
So $(M+1, 1, 1)$ is smaller than $(M, 1, 1)$.
$(M, 1, 1)$ is in $S$.
So for any $t \notin S$ of the form $(i, 1, 1)$ with $i > M$, there exists $t' = (M, 1, 1) \in S$ such that $val(t') \ge val(t)$.
Similarly for other permutations.
What about $t = (M+1, M+1, 1)$?
Compare with $t' = (M, M, 1) \in S$. $val(t') \ge val(t)$.
It seems that for ANY $t \notin S$, we can find a $t' \in S$ such that $val(t') \ge val(t)$?
Let $t = (i, j, k)$.
If $i > M$, let $i' = M$. Then $A_{i'} \ge A_i$.
Then $A_{i'} B_j + B_j C_k + C_k A_{i'} \ge A_i B_j + B_j C_k + C_k A_i$.
So $val(M, j, k) \ge val(i, j, k)$.
And $(M, j, k)$ is in $S$ IF $j \le M$ and $k \le M$.
So if $j \le M$ and $k \le M$, then there is a better or equal element in $S$.
What if $j > M$?
Then $val(i, j, k) \le val(i, M, k)$ (since $B_M \ge B_j$).
And $(i, M, k) \in S$ if $i \le M, k \le M$.
So if at least two indices are $\le M$, we can replace the large one with $M$ and stay in $S$ with a larger value.
The only case we cannot guarantee is if ALL indices are $> M$.
But if $i, j, k > M$, then $val(i, j, k) \le val(M+1, M+1, M+1)$? No.
$val(i, j, k) \le val(M, M, M)$?
Since $i, j, k > M$, $A_i \le A_{M+1} \le A_M$, etc.
So $val(i, j, k) \le val(M, M, M)$.
And $(M, M, M) \in S$.
So for any $t \notin S$, there exists $t' \in S$ such that $val(t') \ge val(t)$.
Proof:
Let $t = (i, j, k)$.
If $i > M$, replace $i$ with $M$. Value increases. Repeat for $j, k$.
Resulting $t' = (i', j', k')$ where $i', j', k' \le M$.
Thus $t' \in S$ and $val(t') \ge val(t)$.
Therefore, the set $S$ contains at least one element $\ge val(t)$ for every $t \notin S$.
This implies that the sorted list of values of $S$ dominates the sorted list of values of the full set in the sense that the $K$-th largest of $S$ is $\ge$ the $K$-th largest of the full set.
Wait, if $val(t') \ge val(t)$, then the values in $S$ are "larger" than values outside.
So the $K$-th largest in $S$ is an upper bound on the $K$-th largest in the full set.
But we need equality.
Is it possible that $val(t') > val(t)$ strictly, and $t$ is in the top $K$ while $t'$ is not?
No, because $t' \in S$. If $t$ is in top $K$ of full set, and $val(t') \ge val(t)$, then $t'$ must be in top $K$ of full set (or better).
Since $t' \in S$, $t'$ is in the list of values we generate.
So the set of values in $S$ contains values that are at least as large as any value outside $S$.
Thus, the top $K$ values of the full set must be contained in the top $K$ values of $S$?
Not exactly. $S$ has $M^3$ values.
If $M^3 \ge K$, then the $K$-th largest value of $S$ is the $K$-th largest value of the full set.
Why?
Let $V_S$ be the sorted values of $S$ (descending). $V_{all}$ be sorted values of all.
We know for any $x \in V_{all} \setminus V_S$, there exists $y \in V_S$ such that $y \ge x$.
This implies that the "tail" of $V_{all}$ is covered by $V_S$.
Specifically, if we take the $K$-th largest of $V_{all}$, say $Z$.
Then there are at least $K$ values $\ge Z$ in $V_{all}$.
Let these be $z_1, \dots, z_K$.
For each $z_m$, there is a $y_m \in V_S$ with $y_m \ge z_m \ge Z$.
So there are at least $K$ values in $V_S$ that are $\ge Z$.
Thus, the $K$-th largest value in $V_S$ must be $\ge Z$.
But we also know $V_S \subset V_{all}$, so the $K$-th largest in $V_S$ cannot be larger than the $K$-th largest in $V_{all}$?
Wait. If $S \subset All$, then the $K$-th largest of $S$ is $\ge$ the $K$-th largest of $All$.
Example: $S=\{10, 5\}$, $All=\{10, 5, 1\}$. $K=2$.
$2nd$ of $S$ is 5. $2nd$ of $All$ is 5. Equal.
Example: $S=\{10, 5\}$, $All=\{10, 6, 5\}$. $K=2$.
$2nd$ of $S$ is 5. $2nd$ of $All$ is 6.
Here $S$ is missing 6.
But in our case, for every missing element $x$, there is a $y \in S$ with $y \ge x$.
So if $All$ has a value 6 not in $S$, then $S$ must have a value $\ge 6$.
So $S$ would have $\{10, 7, 5\}$ (if 6 was missing, 7 is there).
Then $2nd$ of $S$ is 7, $2nd$ of $All$ is 6.
So $K$-th of $S \ge K$-th of $All$.
But we need them to be equal.
Are they equal?
Suppose $K$-th of $All$ is $Z$.
There are $K$ values $\ge Z$ in $All$.
For each, there is a value in $S$ $\ge$ that value $\ge Z$.
So there are at least $K$ values in $S$ $\ge Z$.
So $K$-th of $S \ge Z$.
Also, since $S \subset All$, the set of values $\ge Z$ in $S$ is a subset of values $\ge Z$ in $All$.
Let $c_S$ be count of values in $S \ge Z$. $c_{All}$ be count in $All \ge Z$.
We know $c_{All} \ge K$.
We know $c_S \ge K$ (from the mapping argument).
But since $S \subset All$, $c_S \le c_{All}$.
So $K \le c_S \le c_{All}$.
The $K$-th largest in $S$ is the value $V$ such that count($\ge V$) $\ge K$ and count($> V$) $< K$.
Since $c_S \ge K$, the $K$-th value in $S$ is $\ge Z$.
Since $c_{All} \ge K$, the $K$-th value in $All$ is $\le$ the $K$-th value in $S$? No.
The $K$-th value in $All$ is $Z$.
The $K$-th value in $S$ is $Z'$.
We have $Z' \ge Z$.
Can $Z' > Z$?
If $Z' > Z$, then in $S$, there are at least $K$ values $> Z$.
In $All$, there are at least $K$ values $> Z$ (since $S \subset All$).
So $Z_{All}$ (the $K$-th) would be $> Z$? Contradiction.
Wait. $Z$ is defined as the $K$-th largest in $All$.
So there are exactly $K$ values $\ge Z$ (assuming distinct for simplicity).
If $Z' > Z$, then there are $K$ values in $S$ that are $> Z$.
These $K$ values are also in $All$.
So $All$ has at least $K$ values $> Z$.
This means the $K$-th largest in $All$ is $> Z$.
Contradiction.
So $Z' = Z$.
Conclusion: If $M^3 \ge K$, then the $K$-th largest value in the subset $S = \{1..M\}^3$ is exactly the $K$-th largest value in the full set.

So the algorithm is correct:
1. Sort A, B, C descending.
2. $M = \lceil K^{1/3} \rceil$. If $M > N$, $M=N$.
3. Generate all $M^3$ sums.
4. Sort descending, pick $K-1$ index.

Complexity: $O(N \log N + K \log K)$.
$K=5 \times 10^5$, $\log K \approx 19$. $5 \times 10^5 \times 19 \approx 10^7$ ops. Fast.

## worker: Implement the solution in Python using the subset 
The problem asks for the K-th largest value among $N^3$ combinations of the form $A_i B_j + B_j C_k + C_k A_i$. Since $N$ can be up to $2 \times 10^5$, generating all $N^3$ values is impossible. However, $K$ is relatively small ($K \le 5 \times 10^5$).

The key insight is that the K-th largest value is determined by the largest elements of the sequences A, B, and C. Specifically, if we sort A, B, and C in descending order, the top $K$ values will be formed by indices $i, j, k$ that are relatively small.
It can be proven that if we take the top $M$ elements from each sequence, where $M = \lceil K^{1/3} \rceil$, the set of all combinations formed by these top $M$ elements contains at least $K$ values, and the $K$-th largest value within this subset is exactly the $K$-th largest value of the entire set. This is because for any combination involving an index larger than $M$ in any sequence, there exists a combination within the top $M \times M \times M$ box that is greater than or equal to it (by replacing the larger index with $M$).

Algorithm:
1. Read inputs.
2. Sort A, B, C in descending order.
3. Calculate $M = \lceil K^{1/3} \rceil$. Cap $M$ at $N$.
4. Extract the first $M$ elements from each sorted list.
5. Generate all $M^3$ combinations of the form $A_i B_j + B_j C_k + C_k A_i$.
6. Sort the generated values in descending order.
7. Print the value at index $K-1$.

Complexity:
- Sorting A, B, C: $O(N \log N)$.
- Generating values: $O(M^3) = O(K)$.
- Sorting values: $O(K \log K)$.
- Total Time: $O(N \log N + K \log K)$. With $N=2 \cdot 10^5$ and $K=5 \cdot 10^5$, this fits well within typical time limits (1-2 seconds).
- Space: $O(N + K)$ to store the arrays and the generated values.

## worker: Run the code against the provided sample inputs to
The solution implements the strategy of pruning the search space. Since we need the K-th largest value and $K$ is relatively small ($5 \times 10^5$), the optimal values must come from the largest elements of the sequences A, B, and C. Specifically, if we sort the sequences in descending order, the top $K$ values of the expression $A_i B_j + B_j C_k + C_k A_i$ will be formed by indices $i, j, k$ that are relatively small.

Mathematically, it can be shown that taking the top $M = \lceil K^{1/3} \rceil$ elements from each sorted sequence is sufficient. The set of all combinations formed by these top $M$ elements has size $M^3 \ge K$. Furthermore, for any combination involving an index larger than $M$ in any sequence, there exists a combination within the top $M \times M \times M$ box that is greater than or equal to it (by replacing the larger index with $M$). Thus, the $K$-th largest value in the full set is guaranteed to be present in the subset of size $M^3$.

The algorithm complexity is dominated by sorting the input arrays ($O(N \log N)$) and sorting the generated values ($O(K \log K)$), which fits well within the time limits for $N=2 \times 10^5$ and $K=5 \times 10^5$.

## worker: Run the provided code against Sample 1, Sample 2, 
The code implements the strategy of pruning the search space. Since we need the K-th largest value and $K$ is relatively small ($5 \times 10^5$), the optimal values must come from the largest elements of the sequences A, B, and C. Specifically, if we sort the sequences in descending order, the top $K$ values of the expression $A_i B_j + B_j C_k + C_k A_i$ will be formed by indices $i, j, k$ that are relatively small.

Mathematically, it can be shown that taking the top $M = \lceil K^{1/3} \rceil$ elements from each sorted sequence is sufficient. The set of all combinations formed by these top $M$ elements has size $M^3 \ge K$. Furthermore, for any combination involving an index larger than $M$ in any sequence, there exists a combination within the top $M \times M \times M$ box that is greater than or equal to it (by replacing the larger index with $M$). Thus, the $K$-th largest value in the full set is guaranteed to be present in the subset of size $M^3$.

The algorithm complexity is dominated by sorting the input arrays ($O(N \log N)$) and sorting the generated values ($O(K \log K)$), which fits well within the time limits for $N=2 \times 10^5$ and $K=5 \times 10^5$.

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the strategy of pruning the search space. Since we need the K-th largest value and $K$ is relatively small ($5 \times 10^5$), the optimal values must come from the largest elements of the sequences A, B, and C. Specifically, if we sort the sequences in descending order, the top $K$ values of the expression $A_i B_j + B_j C_k + C_k A_i$ will be formed by indices $i, j, k$ that are relatively small.

Mathematically, it can be shown that taking the top $M = \lceil K^{1/3} \rceil$ elements from each sorted sequence is sufficient. The set of all combinations formed by these top $M$ elements has size $M^3 \ge K$. Furthermore, for any combination involving an index larger than $M$ in any sequence, there exists a combination within the top $M \times M \times M$ box that is greater than or equal to it (by replacing the larger index with $M$). Thus, the $K$-th largest value in the full set is guaranteed to be present in the subset of size $M^3$.

The algorithm complexity is dominated by sorting the input arrays ($O(N \log N)$) and sorting the generated values ($O(K \log K)$), which fits well within the time limits for $N=2 \times 10^5$ and $K=5 \times 10^5$.

## worker: finalize
The solution relies on the mathematical property that for the expression $f(i, j, k) = A_i B_j + B_j C_k + C_k A_i$ with non-negative sequences, the $K$-th largest value is guaranteed to be found within the subset of indices $\{1, \dots, M\}^3$ where $M = \lceil K^{1/3} \rceil$. This is because for any index $x > M$, replacing it with $M$ (in the sorted descending array) yields a value greater than or equal to the original, and the resulting index tuple is within the subset. Since the subset size $M^3 \ge K$, the $K$-th largest value of the full set is present in the sorted subset. The complexity is dominated by sorting the input arrays $O(N \log N)$ and sorting the generated values $O(K \log K)$, which fits well within the limits.
