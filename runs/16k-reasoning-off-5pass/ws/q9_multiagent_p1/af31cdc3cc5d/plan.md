The problem asks us to maximize the sum of absolute differences of adjacent pairs removed until only one element remains. This process effectively pairs up $N-1$ elements, leaving exactly one element unpaired. If we decide to leave the element at index $i$ (0-indexed) as the survivor, then all other elements must be paired up. A key observation is that for any element $A_i$ that is *not* the survivor, it must be paired with either its left neighbor or its right neighbor in the original sequence (considering the dynamic nature of removals, this simplifies to a parity argument). Specifically, if we fix the survivor, the optimal strategy is to pair every other element with its immediate neighbor in the original array to maximize differences. However, a simpler greedy approach exists: the total score is the sum of differences of all pairs. It turns out the maximum score is achieved by summing $|A_i - A_{i+1}|$ for all $i$, but we must be careful about the parity. Actually, the correct logic is that we can pair $(A_1, A_2), (A_3, A_4), \dots$ or $(A_2, A_3), (A_4, A_5), \dots$ etc. But wait, the operation allows removing *any* adjacent pair. Let's re-evaluate.
Consider the contribution of each $A_i$. In the final sum, each $A_i$ is added or subtracted. The survivor is neither added nor subtracted (or effectively cancels out in a specific way). Actually, a known result for this specific problem (Codeforces/AtCoder style) is that the maximum score is $\sum_{i=1}^{N-1} |A_i - A_{i+1}|$? No, that's not right.
Let's look at the sample 1: 1, 2, 5, 3. Pairs (2,5) -> 3, then (1,3) -> 2. Total 5.
Notice $|1-2| + |2-5| + |5-3| = 1 + 3 + 2 = 6$. The answer is 5.
Notice $|1-5| + |2-3| = 4 + 1 = 5$.
The correct insight is that we can pair $(A_1, A_2), (A_3, A_4), \dots$ if $N$ is even? Or maybe we can just sum $|A_i - A_{i+1}|$ for all $i$ and subtract the minimum possible "waste"?
Actually, there is a very simple pattern: The maximum score is $\sum_{i=1}^{N-1} |A_i - A_{i+1}|$ is incorrect.
Let's reconsider the structure. We remove $N-1$ pairs. The survivor is one element.
If we remove $(A_i, A_{i+1})$, they contribute $|A_i - A_{i+1}|$.
The problem is equivalent to: Select $N-1$ disjoint pairs of indices $(i, j)$ such that they can be removed sequentially. This is always possible if we just pick adjacent pairs in the original array? No, removing $(A_2, A_3)$ makes $A_1$ and $A_4$ adjacent.
Actually, the set of removed pairs corresponds to a matching on the path graph $1-2-\dots-N$ where edges can be "crossed" via removals? No.
Let's look at the parity. If $N$ is even, we can pair $(1,2), (3,4), \dots, (N-1, N)$. The score is $\sum |A_{2k-1} - A_{2k}|$.
Can we do better? In Sample 1 ($N=4$): $|1-2|+|5-3| = 1+2=3$. But answer is 5. The pairing was $(2,5)$ and $(1,3)$. These are not disjoint in the original indices? Wait, indices are 1,2,3,4. Pairs are (2,3) and (1,4).
Indices used: 2,3 and 1,4. All indices used exactly once except... wait, $N=4$, we remove 2 pairs, so 4 elements removed? No, "until the sequence has length at most 1".
Start: 4 elements.
Op 1: Remove 2 elements. Length becomes 2.
Op 2: Remove 2 elements. Length becomes 0?
Wait, "until the sequence has length at most 1".
If $N=4$:
Start: 4.
Remove 2 -> 2 left.
Remove 2 -> 0 left?
But the problem says "length at most 1".
If we have 2 elements, we remove them, length becomes 0. Is 0 <= 1? Yes.
So for $N=4$, we perform 2 operations, removing all 4 elements.
Wait, Sample 1 explanation: "First remove A2 and A3... Next remove A1 and A4".
Original: 1, 2, 5, 3.
Remove 2, 5 (indices 2,3). Score 3. Remaining: 1, 3.
Remove 1, 3. Score 2. Remaining: empty.
Total 5.
So all elements are removed.
The constraint is we stop when length <= 1.
If $N$ is even, we remove all elements. If $N$ is odd, we remove $N-1$ elements, leaving 1.
So we are partitioning the sequence into pairs (and possibly one singleton if $N$ is odd).
The pairs must be formable by adjacent removals.
It turns out that ANY pairing of the sequence into pairs (and one singleton) is valid?
No. Consider 1, 2, 3.
Option 1: Pair (1,2), leave 3. Score 1.
Option 2: Pair (2,3), leave 1. Score 1.
Can we pair (1,3)? No, they are not adjacent initially.
So we can only pair adjacent elements in the *current* sequence.
However, it is a known theorem that for this specific problem, the maximum score is simply the sum of $|A_i - A_{i+1}|$ for all $i$ from 1 to $N-1$?
Let's check Sample 1: $|1-2| + |2-5| + |5-3| = 1 + 3 + 2 = 6$. Answer is 5. So no.
What if we sum $|A_i - A_{i+1}|$ but skip one?
Actually, the optimal strategy is to pair $(A_1, A_2), (A_3, A_4), \dots$ if $N$ is even?
Sample 1: $|1-2| + |5-3| = 1 + 2 = 3$. Not optimal.
The optimal pairing in Sample 1 was (2,5) and (1,3).
Notice that in the optimal solution, the pairs are $(A_2, A_3)$ and $(A_1, A_4)$.
This looks like we are summing $|A_i - A_{i+1}|$ for all $i$, but we have to subtract the "gap" created?
Let's try a different perspective.
Total Score = $\sum |x - y|$.
Consider the contribution of each $A_i$.
In the sum of absolute differences, each number $A_i$ is either added or subtracted.
If we have a pair $(u, v)$, contribution is $|u-v| = \pm u \pm v$.
The total sum is $\sum c_i A_i$ where $c_i \in \{1, -1\}$.
For the sum to be valid, the signs must alternate in some way?
Actually, there is a much simpler solution for this problem which appears in competitive programming archives (e.g., AtCoder ABC 176 F? No. Maybe ABC 200? No).
Let's re-read carefully. "Choose two adjacent numbers and remove both".
This is equivalent to finding a matching in the path graph $1-2-\dots-N$ such that the edges in the matching are "compatible".
Actually, it is known that we can achieve ANY matching that respects the parity?
Wait, if $N$ is even, we can pair $(1,2), (3,4), \dots$.
We can also pair $(2,3), (4,5), \dots$ leaving 1 and $N$? No, we must remove everything.
If $N$ is even, we remove everything. The set of pairs must cover all vertices.
Is it true that we can form any perfect matching?
In a path graph, a perfect matching is unique? No.
Path 1-2-3-4. Matchings: {(1,2), (3,4)} or {(2,3), (1,4)? No, (1,4) is not an edge}.
Wait, the operation allows removing adjacent elements, which makes non-adjacent elements adjacent.
So we can effectively pair $(1,4)$ in 1-2-3-4 by removing 2 and 3 first.
So yes, we can form the pairing {(2,3), (1,4)}.
Can we form {(1,2), (3,4)}? Yes, remove (1,2) then (3,4).
Can we form {(1,3), (2,4)}?
Remove (2,4)? No, 2 and 4 are not adjacent.
Remove (1,2)? Then 3,4 adjacent. Pair (3,4). Left with nothing? No, we paired (1,2) and (3,4).
Can we pair (1,3)? To pair 1 and 3, we must remove 2 first? But we remove 2 with someone.
If we remove (2,3), 1 and 4 become adjacent. We can pair (1,4).
If we remove (1,2), 3 and 4 become adjacent. We can pair (3,4).
So for N=4, possible pairings:
1. (1,2) and (3,4). Score $|1-2| + |3-4|$.
2. (2,3) and (1,4). Score $|2-3| + |1-4|$.
Are there others?
What about (1,3) and (2,4)?
To pair (1,3), we need to remove 2. But 2 must be paired with someone.
If 2 is paired with 1, then 1 is gone. Can't pair 1 with 3.
If 2 is paired with 3, then 3 is gone. Can't pair 1 with 3.
So (1,3) cannot be part of a valid pairing for N=4.
So for N=4, only two types of pairings: "even-odd" splits or "shifted" splits.
Generally, for a path graph where we can dynamically connect endpoints, the valid matchings are those where we pair $(i, i+1)$ for all odd $i$, OR pair $(i, i+1)$ for all even $i$?
Let's check N=4.
Type 1: (1,2), (3,4). Indices: (1,2), (3,4).
Type 2: (2,3), (1,4). Indices: (2,3), (1,4).
Wait, (1,4) is not an edge in the original graph, but it becomes one.
Is there a Type 3? (1,2) and (3,4) is one.
(2,3) and (1,4) is another.
What about (1,2) and (3,4) vs (2,3) and (1,4).
Is it possible to have (1,2) and (3,4) is the only way to keep 1 and 2 together?
Actually, the pattern is: We can choose to pair $(A_1, A_2), (A_3, A_4), \dots$ OR $(A_2, A_3), (A_4, A_5), \dots$?
For N=4:
Option A: (1,2), (3,4).
Option B: (2,3), (1,4).
Note that Option B is essentially shifting the start.
For N=5 (odd): We leave 1 element.
Possible survivors?
If we leave $A_1$: Pair (2,3), (4,5).
If we leave $A_2$: Pair (1,3)? No. Pair (1,?) and (3,4)?
If we leave $A_2$, we must pair (1, something). 1 must pair with 2? No, 2 is survivor.
1 must pair with 3? Impossible as discussed.
1 must pair with 2? No, 2 is survivor.
So 1 must pair with... wait.
If 2 is survivor, 1 must be paired with someone.
The only neighbor of 1 is 2. But 2 is survivor.
So 1 cannot be removed?
Wait, if 2 is survivor, 1 must be removed. To remove 1, it must be paired with an adjacent number.
Initially, 1 is adjacent to 2.
If we don't pair (1,2), can 1 become adjacent to anyone else?
Only if 2 is removed. But 2 is the survivor, so 2 is never removed.
Therefore, 1 can NEVER be removed if 2 is the survivor.
This implies: If $A_i$ is the survivor, then $A_{i-1}$ (if exists) and $A_{i+1}$ (if exists) CANNOT be removed?
No, that logic is flawed.
If 2 is survivor, 1 is adjacent to 2.
To remove 1, we must pick a pair containing 1. The only available neighbor is 2.
So we MUST pick (1,2). But 2 is survivor. Contradiction.
So, if $A_i$ is the survivor, then $A_{i-1}$ and $A_{i+1}$ cannot be removed?
Wait, if 2 is survivor, 1 is stuck next to 2. We can never remove 1.
So 1 must also be a survivor? But we can only have 1 survivor.
Thus, for $N > 1$, the survivor MUST be at an end?
Let's re-read the operation. "Choose two adjacent numbers and remove both".
If 2 is survivor, 1 is adjacent to 2.
Can we remove 1? Only by pairing with 2. But 2 is survivor.
So 1 cannot be removed.
So 1 remains.
But we need to reduce to length 1.
If 1 and 2 remain, and we stop at length 1, we must remove one more pair?
No, if we have 1 and 2, we remove them. Then 0 remain.
But we assumed 2 is survivor.
If 2 is survivor, we must end with just 2.
So 1 must be removed.
But 1 can only be removed with 2.
So 2 must be removed. Contradiction.
Conclusion: The survivor MUST be one of the endpoints ($A_1$ or $A_N$)?
Let's check Sample 1: 1, 2, 5, 3. Survivor?
Pairs: (2,5) and (1,3).
Remaining: None. (N=4, even).
Wait, for even N, there is no survivor. All removed.
For odd N, there is 1 survivor.
Sample 3: 1, 1, 1, 1, 1. N=5.
Output 0.
Any pairing gives 0.
Let's try N=3: 1, 2, 3.
Options:
1. Remove (1,2). Left: 3. Score 1.
2. Remove (2,3). Left: 1. Score 1.
Can we remove (1,3)? No.
So for N=3, survivor is 1 or 3.
Hypothesis: For odd N, the survivor must be $A_1$ or $A_N$.
Proof sketch: If $A_k$ ($1 < k < N$) is the survivor, then $A_{k-1}$ and $A_{k+1}$ must be removed.
$A_{k-1}$ must be paired with someone. Its neighbors are $A_{k-2}$ and $A_k$.
If $A_k$ is survivor, it's never removed. So $A_{k-1}$ must pair with $A_{k-2}$.
Similarly, $A_{k+1}$ must pair with $A_{k+2}$.
This propagates outwards.
Eventually, $A_1$ must pair with $A_2$.
But $A_2$ must pair with $A_3$ (since $A_1$ is gone? No).
Let's trace N=5, survivor $A_3$.
$A_2$ must pair with $A_1$ (since $A_3$ safe).
$A_4$ must pair with $A_5$ (since $A_3$ safe).
So pairs: (1,2) and (4,5).
Remaining: $A_3$.
This works!
So survivor can be internal.
My previous deduction was wrong because I assumed $A_{k-1}$ has no other choice, but it pairs with $A_{k-2}$.
So for N=5, survivor $A_3$ is possible with pairs (1,2) and (4,5).
Score: $|A_1-A_2| + |A_4-A_5|$.
Survivor $A_1$: Pairs (2,3), (4,5). Score $|A_2-A_3| + |A_4-A_5|$.
Survivor $A_2$: Pairs (1,3)? No.
If survivor $A_2$:
$A_1$ must pair with... only neighbor is $A_2$ (safe). So $A_1$ cannot be removed.
So $A_1$ remains.
But we need only 1 survivor.
So $A_1$ and $A_2$ both remain.
We must remove one more pair? No, we stop when length <= 1.
If we have 1 and 2, length is 2. We must remove them.
So $A_2$ is removed. Contradiction.
So $A_2$ cannot be the survivor.
Generalizing: If $A_k$ is survivor, then $A_{k-1}$ must pair with $A_{k-2}$, ..., $A_1$ must pair with $A_2$.
This requires $k-1$ to be even?
Number of elements to the left of $k$ is $k-1$.
We need to pair them all up. So $k-1$ must be even.
Similarly, $N-k$ must be even.
So $k$ must be odd (if 1-indexed).
So for odd N, the survivor must be at an odd index $1, 3, 5, \dots, N$.
For even N, no survivor (all paired).
Wait, for N=4 (even), can we have a survivor? No, we remove everything.
So for even N, we just need a perfect matching.
Possible matchings for N=4:
1. (1,2), (3,4).
2. (2,3), (1,4).
Are there others?
What about (1,2) and (3,4) vs (2,3) and (1,4).
Is (1,3) and (2,4) possible? No.
So for even N, we have two main patterns?
Actually, the problem is simpler.
The maximum score is $\sum_{i=1}^{N-1} |A_i - A_{i+1}|$ MINUS something?
Let's calculate for Sample 1: 1, 2, 5, 3.
Sum of diffs: $|1-2| + |2-5| + |5-3| = 1 + 3 + 2 = 6$.
Answer 5.
Difference is 1.
Sample 2: 3, 1, 4, 1, 5, 9, 2. N=7.
Diffs: $|3-1|=2, |1-4|=3, |4-1|=3, |1-5|=4, |5-9|=4, |9-2|=7$.
Sum = 2+3+3+4+4+7 = 23.
Answer 14.
Difference 9.
This doesn't look like a simple subtraction.

Let's rethink the structure.
We are selecting $N-1$ pairs (if N odd, $N-1$ pairs? No, if N odd, we remove $N-1$ elements, so $(N-1)/2$ pairs? No.)
N=5. Remove 4 elements. 2 pairs. 1 survivor.
N=4. Remove 4 elements. 2 pairs.
So we always form $\lfloor N/2 \rfloor$ pairs.
For N=4, 2 pairs.
For N=5, 2 pairs.
The pairs must be disjoint in indices.
And they must be "realizable".
Realizable condition: A set of disjoint pairs is realizable if and only if...
Actually, it is known that for this problem, the answer is simply the sum of $|A_i - A_{i+1}|$ for all $i$, but we can choose to skip one term?
No.
Let's look at the "survivor" logic again.
If N is odd, survivor must be at odd index $k$.
Then we pair $(1,2), (3,4), \dots, (k-2, k-1)$ and $(k+1, k+2), \dots, (N-2, N-1)$.
Wait, if survivor is $A_3$ in 1,2,3,4,5.
Left: 1,2. Pair (1,2).
Right: 4,5. Pair (4,5).
Score: $|A_1-A_2| + |A_4-A_5|$.
If survivor is $A_1$.
Left: none.
Right: 2,3,4,5. Pair (2,3), (4,5).
Score: $|A_2-A_3| + |A_4-A_5|$.
If survivor is $A_5$.
Left: 1,2,3,4. Pair (1,2), (3,4).
Score: $|A_1-A_2| + |A_3-A_4|$.
So for odd N, we can choose any odd index $k$ as survivor, and the score is sum of diffs of pairs $(2i-1, 2i)$ for $i < k/2$ and $(2j+1, 2j+2)$ for $j \ge k/2$?
Basically, we partition the array into pairs $(A_{2i-1}, A_{2i})$ except we skip the survivor and shift the pairing?
Actually, if survivor is $A_k$ (odd), the pairs are:
$(1,2), (3,4), \dots, (k-2, k-1)$
$(k+1, k+2), \dots, (N-2, N-1)$.
This corresponds to summing $|A_{2i-1} - A_{2i}|$ for all $i$, EXCEPT we skip the terms involving $k$?
No, $k$ is not in any pair.
The pairs are fixed as $(1,2), (3,4), \dots$.
If $k=3$, pairs are $(1,2)$ and $(4,5)$.
If $k=1$, pairs are $(2,3), (4,5)$.
If $k=5$, pairs are $(1,2), (3,4)$.
So for odd N, we can choose to shift the pairing pattern?
Pattern 1: $(1,2), (3,4), \dots, (N-2, N-1)$. Survivor $A_N$.
Pattern 2: $(2,3), (4,5), \dots, (N-1, N)$. Survivor $A_1$.
Pattern 3: $(1,2), (3,4), \dots, (k-2, k-1), (k+1, k+2), \dots$.
Wait, if we pick survivor $A_3$, we get $(1,2)$ and $(4,5)$.
This is NOT a simple shift of the whole array.
However, note that $|A_1-A_2| + |A_4-A_5|$ is a subset of the full sum?
Actually, the maximum score for odd N is $\max($
  $\sum_{i=1}^{(N-1)/2} |A_{2i-1} - A_{2i}|$,
  $\sum_{i=1}^{(N-1)/2} |A_{2i} - A_{2i+1}|$
$)$.
Let's test this hypothesis on Sample 1 (N=4, even).
Hypothesis for even N:
Option A: $(1,2), (3,4), \dots$.
Option B: $(2,3), (4,5), \dots$?
For N=4:
A: $|1-2| + |3-4| = 1 + 1 = 2$.
B: $|2-3| + |1-4|$? No, the pattern for even N is different.
For even N, we can have:
1. $(1,2), (3,4), \dots, (N-1, N)$.
2. $(2,3), (4,5), \dots, (N-2, N-1)$? No, that leaves 1 and N.
But we must remove ALL elements.
So for even N, we must have a perfect matching.
The only perfect matchings in a path graph that are "realizable" are:
1. $(1,2), (3,4), \dots, (N-1, N)$.
2. $(2,3), (4,5), \dots$? No, this leaves 1 and N unpaired.
Wait, can we pair (1, N)?
Yes, if we remove everything in between.
So for even N, we can have:
1. $(1,2), (3,4), \dots, (N-1, N)$.
2. $(2,3), (4,5), \dots, (N-2, N-1)$ AND $(1, N)$.
Is $(1, N)$ allowed?
Yes, remove $2..N-1$ in pairs, then 1 and N become adjacent.
So for even N, we have two strategies:
Strategy 1: Sum of $|A_{2i-1} - A_{2i}|$.
Strategy 2: Sum of $|A_{2i} - A_{2i+1}|$ for $i=1..N/2 - 1$ PLUS $|A_1 - A_N|$.
Let's check Sample 1: 1, 2, 5, 3.
Strat 1: $|1-2| + |5-3| = 1 + 2 = 3$.
Strat 2: $|2-5| + |1-3| = 3 + 2 = 5$.
Max is 5. Correct.

Sample 2: 3, 1, 4, 1, 5, 9, 2. N=7 (odd).
Strategies for odd N:
We can leave $A_1$, $A_3$, $A_5$, $A_7$.
If leave $A_1$: Pairs $(2,3), (4,5), (6,7)$. Score $|1-4| + |5-9| + |9-2| = 3 + 4 + 7 = 14$.
If leave $A_3$: Pairs $(1,2), (4,5), (6,7)$. Score $|3-1| + |5-9| + |9-2| = 2 + 4 + 7 = 13$.
If leave $A_5$: Pairs $(1,2), (3,4), (6,7)$. Score $|3-1| + |4-1| + |9-2| = 2 + 3 + 7 = 12$.
If leave $A_7$: Pairs $(1,2), (3,4), (5,6)$. Score $|3-1| + |4-1| + |5-9| = 2 + 3 + 4 = 9$.
Max is 14. Correct.

So the algorithm is:
If N is even:
  Ans = max( Sum(|A[2i-1]-A[2i]|), Sum(|A[2i]-A[2i+1]| for i=1..N/2-1) + |A[1]-A[N]| )
If N is odd:
  Ans = max over k in {1, 3, ..., N} of ( Sum(|A[2i-1]-A[2i]| for i < k) + Sum(|A[2j+1]-A[2j+2]| for j >= k) )
  Wait, the pattern for odd N is simpler:
  We can just consider two main patterns?
  Pattern A: $(1,2), (3,4), \dots, (N-2, N-1)$. Survivor $A_N$.
  Pattern B: $(2,3), (4,5), \dots, (N-1, N)$. Survivor $A_1$.
  Are there intermediate survivors?
  For N=5, survivor $A_3$ gave $|1-2| + |4-5|$.
  Pattern A (survivor 5): $|1-2| + |3-4|$.
  Pattern B (survivor 1): $|2-3| + |4-5|$.
  Is $|1-2| + |4-5|$ better than A or B?
  It depends on values.
  But notice: $|1-2| + |4-5|$ is NOT one of the two patterns above.
  However, we can generalize:
  For odd N, we can choose any odd index $k$ as survivor.
  The score is $\sum_{i=1}^{(k-1)/2} |A_{2i-1} - A_{2i}| + \sum_{j=(k+1)/2}^{(N-1)/2} |A_{2j+1} - A_{2j+2}|$?
  Wait, indices.
  If survivor is $A_k$ (1-indexed, odd).
  Left part: $1..k-1$. Pairs $(1,2), (3,4), \dots, (k-2, k-1)$.
  Right part: $k+1..N$. Pairs $(k+1, k+2), \dots, (N-2, N-1)$.
  This covers all cases.
  So we just need to iterate over all odd $k$ and compute the sum.
  Since $N$ up to $3 \times 10^5$, $O(N)$ is required.
  We can precompute prefix sums of the "odd-even" diffs and suffix sums of the "even-odd" diffs?
  Actually, the pattern is always $(2i-1, 2i)$.
  So for a fixed $k$, the score is:
  Sum of $|A_{2i-1} - A_{2i}|$ for $i=1$ to $(k-1)/2$.
  Plus Sum of $|A_{2j+1} - A_{2j+2}|$ for $j=(k+1)/2$ to $(N-1)/2$.
  Wait, the right part indices:
  If $k=3$, right part starts at 4. Pairs $(4,5), (6,7) \dots$.
  So indices are $2j, 2j+1$? No.
  Original indices: $k+1, k+2, \dots$.
  We pair $(k+1, k+2), (k+3, k+4) \dots$.
  So yes, it's the same pattern $(2m-1, 2m)$ relative to the start of the segment.
  So we can precompute an array $D[i] = |A_{2i-1} - A_{2i}|$ for $i=1..N/2$.
  Then for a survivor $k$ (odd), the score is sum of $D[1..(k-1)/2]$ + sum of $D[(k+1)/2 .. (N-1)/2]$?
  Wait, if $k=3$, $(k+1)/2 = 2$.
  We need pairs starting from 4.
  Pair 1: (1,2) -> D[1].
  Pair 2: (3,4) -> D[2].
  If survivor is 3, we skip pair 2?
  No, if survivor is 3, we pair (1,2) and (4,5).
  (4,5) is NOT D[2] (which is 3,4).
  So the pattern shifts on the right side.
  Right side pairs: $(k+1, k+2), (k+3, k+4) \dots$.
  These correspond to $D$ indices shifted?
  Let's define $D[i] = |A_{2i-1} - A_{2i}|$.
  Left part: $1..k-1$. Pairs $(1,2), \dots, (k-2, k-1)$. Sum $D[1] + \dots + D[(k-1)/2]$.
  Right part: $k+1..N$. Pairs $(k+1, k+2), \dots$.
  The first pair is $(k+1, k+2)$.
  If $k=3$, pair is $(4,5)$.
  In terms of global indices, this is $|A_4 - A_5|$.
  This is not $D[2]$ ($|A_3-A_4|$).
  So we need another array $E[i] = |A_{2i} - A_{2i+1}|$.
  Then for survivor $k$:
  Left: Sum $D[1..(k-1)/2]$.
  Right: Sum $E[(k+1)/2 .. (N-1)/2]$.
  Check $k=3$: Left $D[1]$. Right $E[2]$.
  $E[2] = |A_4 - A_5|$. Correct.
  Check $k=1$: Left empty. Right $E[1..(N-1)/2]$.
  $E[1] = |A_2 - A_3|$. Correct.
  Check $k=N$: Left $D[1..(N-1)/2]$. Right empty.
  Correct.
  So for odd N, we compute prefix sums of D and suffix sums of E.
  For even N, we have two options:
  1. Sum $D[1..N/2]$.
  2. Sum $E[1..N/2-1] + |A_1 - A_N|$.
  Wait, is there any other option for even N?
  What if we leave a "gap" in the middle and connect ends?
  No, for even N, we must pair everyone.
  The only two valid perfect matchings are the "standard" one and the "shifted" one with ends connected.
  So the plan is solid.