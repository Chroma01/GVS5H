The problem asks if we can fill missing values (-1) in sequences A and B, and rearrange A, such that every pair $(A_i, B_i)$ sums to the same constant $S$. Since we can rearrange A arbitrarily, the order of initial values in A doesn't matter; only the multiset of values matters. The core constraint is that for every index $i$, $A_i + B_i = S$. This implies that for any pair of indices $(i, j)$, the difference $A_i - A_j$ must equal $B_j - B_i$. More simply, if we fix the target sum $S$, then for every $i$, $A_i = S - B_i$. Since $A_i \ge 0$, we must have $S \ge B_i$ for all $i$ where $B_i \neq -1$. Similarly, $S \ge A_i$ for all $i$ where $A_i \neq -1$. The sum of all elements in the final arrays must be $N \times S$. We can calculate the sum of known elements in A and B. Let $SumA$ be the sum of known $A_i$'s and $SumB$ be the sum of known $B_i$'s. The total sum of knowns is $SumA + SumB$. The number of missing elements is $cntA + cntB$. The total sum will be $(SumA + SumB) + \text{filled values} = N \times S$. Thus, $N \times S \ge SumA + SumB$. Also, $S$ must be at least $\max(\text{known } A_i, \text{known } B_i)$. If we pick the smallest valid $S$ (which is $\max(\text{known } A_i, \text{known } B_i)$), we check if the remaining "budget" ($N \times S - (SumA + SumB)$) is sufficient to fill the missing slots with non-negative integers. Since we can fill missing slots with any non-negative integer, we just need to ensure that the required sum for the missing slots is non-negative and that we can distribute it. Actually, a simpler necessary and sufficient condition is: Let $M_A = \max(\{A_i \mid A_i \neq -1\} \cup \{0\})$ and $M_B = \max(\{B_i \mid B_i \neq -1\} \cup \{0\})$. The target sum $S$ must be at least $M_A + M_B$? No, $A_i + B_i = S$. So $S \ge A_i$ and $S \ge B_i$. Thus $S \ge \max(M_A, M_B)$. The total sum of the final array is $N \times S$. The sum of currently known numbers is $K = \sum A_i + \sum B_i$ (ignoring -1s). The sum of numbers we need to add is $N \times S - K$. Since we can add any non-negative integers to the -1 positions, we just need $N \times S - K \ge 0$. However, we also need to ensure that we can form pairs. Wait, the rearrangement allows us to pair any $A$ with any $B$. So we just need to check if there exists an $S$ such that:
1. $S \ge \max(\text{known } A)$
2. $S \ge \max(\text{known } B)$
3. $N \times S \ge \sum (\text{known } A) + \sum (\text{known } B)$
Actually, is that enough? Suppose we have $A=[10]$, $B=[0]$. $S \ge 10, S \ge 0$. Min $S=10$. Sum known = 10. $1 \times 10 \ge 10$. OK.
Suppose $A=[10, 0]$, $B=[0, 0]$. $S \ge 10$. Min $S=10$. Sum known = 10. $2 \times 10 = 20 \ge 10$. We need to fill one $A$ or $B$? No, all are known. $10+0=10, 0+0=0 \neq 10$. Ah, the condition is that we can rearrange A. So we pair $10$ with a $0$ and $0$ with a $0$. Sums are $10$ and $0$. Not equal.
The condition "rearrange A" means we can permute A to match B. But B is fixed relative to its indices? No, the problem says "Rearrange the elements of sequence A". It does NOT say we can rearrange B. So B stays in its original positions. A can be permuted.
So we need to find a permutation of A (filled) and values for -1s such that $A_{perm}[i] + B[i] = S$ for all $i$.
This means for each $i$, $A_{perm}[i] = S - B[i]$.
Since $A_{perm}$ is a permutation of the multiset of final A values, the multiset $\{S - B[1], S - B[2], \dots, S - B[N]\}$ must be equal to the multiset of final A values.
Let the final A values be $A'_1, \dots, A'_N$. We know some of them are fixed (non -1). The others are free.
Let $U$ be the set of indices where $A_i \neq -1$. For $i \in U$, $A'_i$ is fixed to $A_i$.
Let $V$ be the set of indices where $B_i \neq -1$. For $i \in V$, the required value from A is $S - B_i$.
So the multiset of required A values is $\{S - B_i \mid i \in V\} \cup \{ \text{free values} \}$.
The multiset of available A values is $\{A_i \mid i \in U\} \cup \{ \text{free values} \}$.
For a valid $S$ to exist, the multiset $\{A_i \mid i \in U\}$ must be a subset of $\{S - B_i \mid i \in V\} \cup \{ \text{free} \}$.
Actually, it's simpler: The multiset of ALL final A values must be exactly $\{S - B_i \mid i=1\dots N\}$.
The known values in A are $\{A_i \mid i \in U\}$. These must be present in the target multiset $\{S - B_i\}$.
So, for every $i \in U$, there must exist some $j$ such that $A_i = S - B_j$.
This implies $S = A_i + B_j$.
This must hold for ALL $i \in U$. So all $A_i + B_j$ must be equal to the same $S$.
Wait, no. The target multiset is fixed by $S$: $T_S = \{S - B_1, S - B_2, \dots, S - B_N\}$.
The known values in A, $K_A = \{A_i \mid i \in U\}$, must be a subset of $T_S$.
So for every $x \in K_A$, there must be some $y \in \{B_1, \dots, B_N\}$ such that $x = S - y \implies S = x + y$.
This means $S$ must be representable as $A_i + B_j$ for some $j$.
Moreover, since $K_A$ is a subset of $T_S$, and $T_S$ is determined by $S$, we can just iterate over possible values of $S$.
What are the possible values of $S$?
$S = A_i + B_j$ for some $i \in U, j \in V$.
Also, we need $S - B_k \ge 0$ for all $k$ (since final A values must be non-negative). So $S \ge \max_{k} B_k$ (considering only $B_k \neq -1$, and if all -1, $S \ge 0$).
And $S - B_k$ must be non-negative.
Also, the count of values in $K_A$ that are "covered" by $T_S$ must be $|U|$.
Actually, the condition is: The multiset $K_A$ must be a sub-multiset of $T_S$.
$T_S = \{S - B_1, \dots, S - B_N\}$.
So we need to check if there exists an $S$ such that:
1. $S \ge \max(B_k \text{ for } B_k \neq -1, 0)$.
2. The multiset $\{A_i \mid A_i \neq -1\}$ is a sub-multiset of $\{S - B_j \mid j=1\dots N\}$.

How to find such $S$?
Note that if such an $S$ exists, then for every $A_i \in K_A$, there is a $B_j$ such that $A_i + B_j = S$.
This implies $S \ge A_i + \min(B_j \text{ where } B_j \neq -1)$.
Actually, let's look at the constraints. $N \le 2000$. We can try all pairs $(i, j)$ where $A_i \neq -1$ and $B_j \neq -1$. Calculate candidate $S = A_i + B_j$. Check if this $S$ works.
If there are no $A_i \neq -1$, then $K_A$ is empty. Any $S \ge \max(B)$ works? Yes, we can just fill A with $S-B_i$.
If there are no $B_j \neq -1$, then $T_S = \{S, S, \dots, S\}$. We need $K_A \subseteq \{S, \dots, S\}$. So all $A_i$ must be equal to $S$. So $S = A_i$ for all $i \in U$. If all $A_i$ are equal, any $S \ge A_i$ works? No, $T_S$ must contain $A_i$. So $S - B_j = A_i$. Since all $B_j = -1$, $T_S = \{S, \dots, S\}$. So we need $A_i = S$. Thus all $A_i$ must be equal. If they are, set $S = A_i$.
Algorithm:
1. Identify $U = \{i \mid A_i \neq -1\}$ and $V = \{j \mid B_j \neq -1\}$.
2. If $U$ is empty:
   - We need $S \ge \max(B_j \text{ for } j \in V, 0)$.
   - We can choose $S = \max(\dots)$. Then fill $A_i = S - B_i$. All non-negative. Yes.
3. If $V$ is empty:
   - We need $K_A \subseteq \{S, \dots, S\}$. So all $A_i$ ($i \in U$) must be equal. Let this value be $v$.
   - If not all equal, No.
   - If equal, set $S = v$. Check if $S \ge 0$ (given). Yes.
4. If both non-empty:
   - Collect all candidate $S$ values: $C = \{A_i + B_j \mid i \in U, j \in V\}$.
   - For each $s \in C$:
     - Check if $s \ge \max(B_j \text{ for } j \in V, 0)$. (Actually, if $s < B_j$, then $s - B_j < 0$, impossible).
     - Construct multiset $T_s = \{s - B_j \mid j=1\dots N\}$. Note: for $B_j = -1$, term is $s$.
     - Check if multiset $K_A = \{A_i \mid i \in U\}$ is a sub-multiset of $T_s$.
     - If yes, return Yes.
   - If no candidate works, return No.

Wait, is it possible that a valid $S$ is not in $C$?
Suppose $K_A = \{10\}$. $B = [-1, -1]$. $C$ is empty. But we handled $V$ empty case.
Suppose $K_A = \{10\}$. $B = [5, -1]$. $U=\{1\}, V=\{1\}$. $C = \{10+5\} = \{15\}$.
Check $S=15$. $T_{15} = \{15-5, 15-(-1)\} = \{10, 16\}$. $K_A=\{10\} \subseteq \{10, 16\}$. Yes.
Is it possible $S$ is not $A_i + B_j$?
We need $A_i \in T_S \implies A_i = S - B_k$ for some $k$. So $S = A_i + B_k$.
Yes, every element in $K_A$ must map to some $B_k$. So $S$ must be of the form $A_i + B_k$.
So iterating over $C$ is sufficient.
Complexity: $|U| \le N, |V| \le N$. $|C| \le N^2$. For each $s$, check takes $O(N \log N)$ or $O(N)$. Total $O(N^3)$. With $N=2000$, $N^3 = 8 \times 10^9$, too slow.
We need a faster check.
Notice that for a fixed $S$, we need to match each $A_i$ to a distinct $B_j$ (or rather, the multiset condition).
Actually, the condition "multiset $K_A$ is sub-multiset of $T_S$" is equivalent to:
Count of each value $x$ in $K_A$ $\le$ Count of $x$ in $T_S$.
Count of $x$ in $T_S$ is the number of $j$ such that $S - B_j = x \iff B_j = S - x$.
So we need: for every value $v$ present in $K_A$, count($v$ in $K_A$) $\le$ count($S-v$ in $B_{\text{known}}$) + count($S-v$ in $B_{\text{unknown}}$).
Wait, $B_{\text{unknown}}$ are the -1s. For $B_j = -1$, the term in $T_S$ is $S - (-1)$? No.
$T_S = \{S - B_1, S - B_2, \dots, S - B_N\}$.
If $B_j = -1$, the term is $S - (-1) = S+1$?
NO. The problem says: "Choose an index i such that $B_i = -1$, and replace $B_i$ with any non-negative integer."
So we can choose $B_j$ to be anything.
Ah! I misread the operation. We can fill -1 in B as well!
"Choose an index i such that $B_i = -1$, and replace $B_i$ with any non-negative integer."
So both A and B can be filled. Only A can be rearranged.
So $B$ is not fixed. We can choose $B_j$ for $j \in V^c$ (where $B_j=-1$) to be whatever we want.
Let's re-evaluate.
We need $A_{perm}[i] + B[i] = S$ for all $i$.
$A_{perm}$ is a permutation of final A.
Final A consists of original $A_i$ (non -1) and filled values for $A_i=-1$.
Final B consists of original $B_i$ (non -1) and filled values for $B_i=-1$.
Let $U = \{i \mid A_i \neq -1\}$, $V = \{i \mid B_i \neq -1\}$.
For $i \in U$, $A_{perm}[i]$ must be one of the original $A$ values? No.
$A_{perm}$ is a permutation of the multiset of final A values.
Let the multiset of final A values be $\mathcal{A}$.
Let the multiset of final B values be $\mathcal{B}$.
We need to pair elements from $\mathcal{A}$ and $\mathcal{B}$ such that sums are equal?
No. The operation is: Rearrange A. Then check $A_1+B_1 = A_2+B_2 = \dots$.
This means after rearrangement, the $i$-th element of A (let's call it $A'_i$) plus $B_i$ equals $S$.
So $A'_i = S - B_i$.
This must hold for all $i=1\dots N$.
So the sequence $A'$ is completely determined by $S$ and $B$.
$A' = (S-B_1, S-B_2, \dots, S-B_N)$.
The condition is that the multiset of values in $A'$ must be equal to the multiset of final A values.
Final A values are: $\{A_i \mid i \in U\} \cup \{ \text{filled values for } i \notin U \}$.
Let $K_A = \{A_i \mid i \in U\}$.
Let $K_B = \{B_i \mid i \in V\}$.
We can choose filled values for $A$ (for $i \notin U$) and $B$ (for $i \notin V$).
Let $N_A = N - |U|$ be the number of fillable A's.
Let $N_B = N - |V|$ be the number of fillable B's.
The multiset $A'$ is $\{S - B_1, \dots, S - B_N\}$.
This multiset must contain $K_A$ as a sub-multiset.
The remaining elements in $A'$ (count $N_A$) can be filled arbitrarily?
Yes, because we can fill the $N_A$ missing spots in A with any values.
Wait, the values in $A'$ are determined by $S$ and $B$.
The values in $B$ are: $K_B$ plus $N_B$ fillable values.
So we need to find $S$ and fillable $B$'s such that:
1. $S - B_i \ge 0$ for all $i$.
2. The multiset $\{S - B_1, \dots, S - B_N\}$ contains $K_A$.
Since we can choose the fillable $B_i$'s freely (as long as $\ge 0$), we can adjust $B$ to make the condition hold.
Specifically, for the indices $i \in V$, $B_i$ is fixed. So $S - B_i$ is fixed.
For $i \notin V$, we can choose $B_i \ge 0$. Then $S - B_i$ can be any value $\le S$.
So the multiset $A'$ consists of:
- Fixed values: $\{S - B_i \mid i \in V\}$.
- Flexible values: $\{S - B_i \mid i \notin V\}$, where each term can be any integer in $[0, S]$.
We need $K_A \subseteq A'$.
So for every $x \in K_A$, we need to find a slot in $A'$ to put $x$.
The slots are either fixed (from $V$) or flexible (from $U^c$).
If $x$ is matched to a fixed slot $i \in V$, we need $x = S - B_i \implies S = x + B_i$.
If $x$ is matched to a flexible slot $i \notin V$, we need $x \le S$ (since $S - B_i = x \implies B_i = S - x \ge 0$).
So the condition is:
There exists $S$ such that:
1. $S \ge \max(K_B \cup \{0\})$. (To ensure fixed $B_i$ allow non-negative $A'$).
2. $S \ge \max(K_A \cup \{0\})$. (To ensure flexible slots can produce values in $K_A$).
3. The number of elements in $K_A$ that CANNOT be matched to fixed slots (where $S = x + B_i$) is $\le N_B$ (number of flexible slots).
Actually, it's simpler:
For a fixed $S$, the fixed part of $A'$ is $F_S = \{S - B_i \mid i \in V\}$.
We need $K_A \setminus F_S$ (multiset difference) to be coverable by the flexible part.
The flexible part has size $N_B$, and each element can be any value in $[0, S]$.
So we just need $|K_A \setminus F_S| \le N_B$ AND for every $y \in K_A \setminus F_S$, $y \le S$.
Wait, if $y \in K_A$ and $y \in F_S$, it's covered. If $y \in K_A$ and $y \notin F_S$, we need to cover it with a flexible slot.
The flexible slots can produce ANY value $\le S$. So as long as $y \le S$, we can produce it.
So the condition is:
Count of $y \in K_A$ such that $y \notin F_S$ must be $\le N_B$.
And for all such $y$, $y \le S$.
Note that $y \notin F_S$ means there is no $i \in V$ such that $S - B_i = y \iff B_i = S - y$.
So we need to check if we can form $S$ such that:
- $S \ge \max(K_B, 0)$.
- $S \ge \max(K_A, 0)$.
- Let $cnt(y)$ be the frequency of $y$ in $K_A$.
- Let $fixed\_count(y, S)$ be the frequency of $y$ in $F_S$.
- We need $\sum_{y} \max(0, cnt(y) - fixed\_count(y, S)) \le N_B$.
- And for all $y$ where $cnt(y) > fixed\_count(y, S)$, we must have $y \le S$.

How to find $S$?
$S$ must be such that $S \ge \max(K_B, 0)$.
Also, if we use a flexible slot to cover $y$, we need $S \ge y$.
If we use a fixed slot $i$ to cover $y$, we need $S = y + B_i$.
So $S$ must be either $\ge \max(K_A, 0)$ or equal to some $y + B_i$.
Actually, $S$ must be $\ge \max(K_A, 0)$ anyway.
The critical candidates for $S$ are:
1. $S = \max(K_B, 0)$. (Minimum possible S).
2. $S = y + B_i$ for some $y \in K_A, i \in V$.
Why? Because if $S$ is very large, $fixed\_count(y, S)$ might increase?
$fixed\_count(y, S)$ is the number of $i \in V$ such that $B_i = S - y$.
As $S$ increases, $S-y$ increases. The value $B_i$ is fixed. So $S-y$ matches $B_i$ only for specific $S$.
So $fixed\_count(y, S)$ is non-zero only if $S = y + B_i$.
If $S$ is not of the form $y + B_i$, then $fixed\_count(y, S) = 0$.
So for "generic" large $S$, we rely entirely on flexible slots.
If we pick $S$ very large, say $S = \max(K_A, \max(K_B)) + \text{huge}$, then $fixed\_count(y, S) = 0$ for all $y$ (unless $S-y$ happens to be in $K_B$, but we can just pick $S$ such that $S-y \notin K_B$).
Wait, if $S$ is huge, $S-y$ is huge. $K_B$ is finite. So $S-y$ won't be in $K_B$.
So for large $S$, $fixed\_count = 0$.
Then we need $|K_A| \le N_B$.
If $|K_A| \le N_B$, we can just pick a huge $S$ and fill everything flexibly.
So if $|K_A| \le N_B$, answer is Yes?
Wait, we also need $S \ge \max(K_B)$.
If we pick $S = \max(K_B, \max(K_A))$, then $fixed\_count$ might be non-zero.
If $|K_A| \le N_B$, we can definitely satisfy it by picking $S$ large enough so no fixed slots help (or hurt? Fixed slots help reduce the count needed from flexible slots).
Actually, fixed slots can only help. They reduce the number of flexible slots needed.
So if $|K_A| \le N_B$, we can always succeed?
Yes, because we can pick $S = \max(K_B, \max(K_A))$. Then check. If $|K_A| \le N_B$, even with 0 fixed matches, it works.
What if $|K_A| > N_B$?
Then we MUST use some fixed slots to cover the excess.
We need $\sum \max(0, cnt(y) - fixed\_count(y, S)) \le N_B$.
$\iff \sum fixed\_count(y, S) \ge |K_A| - N_B$.
Let $R = |K_A| - N_B$. We need the number of fixed slots that match values in $K_A$ to be at least $R$.
A fixed slot $i \in V$ matches $y \in K_A$ if $S = y + B_i$.
So we need to find $S$ such that:
1. $S \ge \max(K_B, 0)$.
2. $S \ge \max(K_A, 0)$.
3. Number of pairs $(i \in V, y \in K_A)$ such that $S = y + B_i$ is at least $R$.
Wait, we need to count multiplicities.
Let $M$ be the multiset of sums $y + B_i$ for all $y \in K_A, i \in V$.
We need to find $S$ such that $S \ge \max(K_B, 0)$ and $S \ge \max(K_A, 0)$ and count($S$ in $M$) $\ge R$.
Is that correct?
$count(S \text{ in } M) = \sum_{y \in K_A} \sum_{i \in V} [S = y + B_i] = \sum_{y \in K_A} fixed\_count(y, S)$.
Yes.
So the algorithm is:
1. Calculate $R = |K_A| - N_B$. If $R \le 0$, return Yes.
2. Construct multiset $M = \{ y + B_i \mid y \in K_A, i \in V \}$.
3. Filter $M$ to keep only values $s$ such that $s \ge \max(K_B, 0)$ and $s \ge \max(K_A, 0)$.
4. Check if any value in filtered $M$ has frequency $\ge R$.
5. If yes, Yes. Else No.

Wait, is there any other constraint?
We need $S - B_i \ge 0$ for all $i \in V$.
This means $S \ge B_i$ for all $i \in V$. So $S \ge \max(K_B)$.
We also need $S \ge y$ for all $y$ covered by flexible slots.
If we cover $y$ with flexible slot, we need $S \ge y$.
Since we need to cover all $y \in K_A$ that are not covered by fixed slots, we need $S \ge \max(\text{uncovered } y)$.
But if we pick $S$ from $M$, then $S = y + B_i \ge y$ (since $B_i \ge 0$).
So any $S$ formed by $y+B_i$ satisfies $S \ge y$ for that specific $y$.
What about other $y'$?
If $y'$ is covered by flexible slot, we need $S \ge y'$.
So we need $S \ge \max(K_A)$.
So the condition $S \ge \max(K_A)$ is necessary.
And $S \ge \max(K_B)$ is necessary.
So the filtering $s \ge \max(K_A, \max(K_B))$ is correct.

Corner case: $V$ is empty.
Then $N_B = N$. $R = |K_A| - N \le 0$ (since $|K_A| \le N$). Returns Yes. Correct.
Corner case: $U$ is empty.
Then $K_A = \emptyset, R = -N \le 0$. Returns Yes. Correct.

Complexity:
$|K_A| \le N, |V| \le N$.
Size of $M$ is $|K_A| \times |V| \le N^2$.
Sorting $M$ takes $O(N^2 \log N)$.
Checking frequencies takes $O(N^2)$.
Total time $O(N^2 \log N)$. With $N=2000$, $N^2 = 4 \times 10^6$, times log is fine.

Implementation details:
- Read N.
- Read A, B.
- Identify $K_A$ (list of non -1 A), $K_B$ (list of non -1 B).
- $N_A = N - len(K_A)$, $N_B = N - len(K_B)$.
- $R = len(K_A) - N_B$.
- If $R \le 0$: print Yes.
- Else:
  - $min\_S = \max(\max(K_B, default=0), \max(K_A, default=0))$.
  - Generate $M$: for $y$ in $K_A$, for $b$ in $K_B$: append $y+b$.
  - Count frequencies of each $s \in M$ where $s \ge min\_S$.
  - If any count $\ge R$: print Yes.
  - Else: print No.

Double check Sample 1:
A = [2, 0, -1, 3], B = [3, -1, 4, 2]
N=4.
K_A = [2, 0, 3] (len 3). N_A = 1.
K_B = [3, 4, 2] (len 3). N_B = 1.
R = 3 - 1 = 2.
min_S = max(4, 3) = 4.
M = {2+3, 2+4, 2+2, 0+3, 0+4, 0+2, 3+3, 3+4, 3+2}
= {5, 6, 4, 3, 5, 2, 6, 7, 5}
Filter >= 4: {5, 6, 5, 6, 7, 5} -> {5:3, 6:2, 7:1}.
Max freq is 3 (for 5). 3 >= 2. Yes.
Output: Yes. Matches sample.

Sample 2:
A = [1, 2, 3], B = [1, 2, 4]
K_A = [1, 2, 3], len 3. N_A = 0.
K_B = [1, 2, 4], len 3. N_B = 0.
R = 3 - 0 = 3.
min_S = max(4, 3) = 4.
M = {1+1, 1+2, 1+4, 2+1, 2+2, 2+4, 3+1, 3+2, 3+4}
= {2, 3, 5, 3, 4, 6, 4, 5, 7}
Filter >= 4: {5, 4, 6, 4, 5, 7} -> {4:2, 5:2, 6:1, 7:1}.
Max freq 2. 2 < 3. No.
Output: No. Matches sample.

Sample 3:
A = [1, 2, -1], B = [1, 2, 4]
K_A = [1, 2], len 2. N_A = 1.
K_B = [1, 2, 4], len 3. N_B = 0.
R = 2 - 0 = 2.
min_S = max(4, 2) = 4.
M = {1+1, 1+2, 1+4, 2+1, 2+2, 2+4} = {2, 3, 5, 3, 4, 6}.
Filter >= 4: {5, 4, 6}.
Counts: 5:1, 4:1, 6:1. Max 1. 1 < 2. No.
Output: No. Matches sample.

One edge case: $K_A$ or $K_B$ empty.
If $K_A$ empty, $R = 0 - N_B \le 0$. Yes.
If $K_B$ empty, $min\_S = \max(K_A)$. $M$ is empty?
If $K_B$ empty, loop for M doesn't run. $M$ is empty.
If $R > 0$, we need freq >= R. Empty set has max freq 0. So No.
Is this correct?
If $K_B$ empty, $N_B = N$. $R = |K_A| - N \le 0$. So we return Yes immediately.
So the case where $K_B$ empty and $R > 0$ is impossible.
Correct.

Logic seems solid.

```python
import sys
from collections import Counter

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
        B = []
        for _ in range(N):
            B.append(int(next(iterator)))
    except StopIteration:
        return

    # Extract known values
    K_A = [x for x in A if x != -1]
    K_B = [x for x in B if x != -1]
    
    len_K_A = len(K_A)
    len_K_B = len(K_B)
    
    N_A = N - len_K_A
    N_B = N - len_K_B
    
    R = len_K_A - N_B
    
    if R <= 0:
        print("Yes")
        return

    # Calculate minimum required S
    # S must be >= max(K_B) and S >= max(K_A)
    max_K_B = max(K_B) if K_B else 0
    max_K_A = max(K_A) if K_A else 0
    min_S = max(max_K_B, max_K_A)
    
    # Generate candidate S values from sums y + b
    # We need to count frequencies of s >= min_S
    # M will store s = y + b for y in K_A, b in K_B
    # We only care about s >= min_S
    
    # Optimization: If len(K_A) * len(K_B) is large, we still do O(N^2) which is fine for N=2000
    # 2000^2 = 4,000,000 operations, perfectly fine.
    
    candidates = []
    for y in K_A:
        for b in K_B:
            s = y + b
            if s >= min_S:
                candidates.append(s)
    
    if not candidates:
        print("No")
        return
        
    counts = Counter(candidates)
    
    max_freq = 0
    for s in counts:
        if counts[s] > max_freq:
            max_freq = counts[s]
            
    if max_freq >= R:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()
```

Wait, I should double check the logic about "flexible slots can produce ANY value <= S".
If we use a flexible slot to cover $y$, we set $B_i = S - y$. We need $B_i \ge 0 \implies S \ge y$.
Since we filter $S \ge \max(K_A)$, this is satisfied for all $y \in K_A$.
So yes, any $y \in K_A$ can be covered by a flexible slot if $S \ge y$.
The only constraint is the count of flexible slots available ($N_B$).
The logic holds.

One small detail: `max` on empty sequence.
`max(K_B)` where `K_B` is empty raises ValueError.
I handled it: `max_K_B = max(K_B) if K_B else 0`.
Same for `K_A`.
If `K_A` is empty, `R = 0 - N_B <= 0`, returns Yes.
If `K_B` is empty, `N_B = N`, `R = len(K_A) - N <= 0`, returns Yes.
So the code path for `candidates` generation is safe (at least one of `K_A` or `K_B` must be non-empty if `R > 0`?
If `R > 0`, then `len(K_A) > N_B = N - len(K_B)`.
`len(K_A) + len(K_B) > N`.
Since `len(K_A) <= N` and `len(K_B) <= N`, this implies both are non-zero?
Not necessarily. If `len(K_A) = N`, `len(K_B) = 0`. Then `R = N - N = 0`.
If `len(K_A) = N`, `len(K_B) = 1`. `R = N - (N-1) = 1`.
Then `K_B` is non-empty.
So if `R > 0`, then `len(K_A) > N - len(K_B)`.
If `K_B` is empty, `len(K_B)=0`, `R = len(K_A) - N`. Since `len(K_A) <= N`, `R <= 0`.
So if `R > 0`, `K_B` MUST be non-empty.
Similarly, if `K_A` is empty, `R = -N_B <= 0`.
So if `R > 0`, both `K_A` and `K_B` are non-empty.
Thus `candidates` generation is safe.

Final check on constraints.
$N \le 2000$.
$A_i, B_i \le 10^9$.
Sums can be $2 \cdot 10^9$, fits in integer.
Time complexity $O(N^2 \log N)$ due to Counter or sorting. Python's Counter is $O(N^2)$.
Memory $O(N^2)$ for candidates list. $4 \cdot 10^6$ integers is ~16MB, fine.

```python
# Final check of the code structure
import sys
from collections import Counter

# ... code ...
```
Looks good.

One edge case: N=2.
A=[-1, -1], B=[-1, -1].
K_A=[], K_B=[]. R = 0 - 2 = -2. Yes. Correct.
A=[1, 1], B=[-1, -1].
K_A=[1, 1], K_B=[]. R = 2 - 2 = 0. Yes. Correct.
A=[1, 2], B=[-1, -1].
K_A=[1, 2], K_B=[]. R = 2 - 2 = 0. Yes. Correct.
A=[1, 2], B=[10, 10].
K_A=[1, 2], K_B=[10, 10].
R = 2 - 0 = 2.
min_S = max(10, 2) = 10.
M = {1+10, 1+10, 2+10, 2+10} = {11, 11, 12, 12}.
Filter >= 10: all.
Counts: 11:2, 12:2. Max 2.
2 >= 2. Yes.
Is it possible?
S=11. A' = [11-10, 11-10] = [1, 1].
Original A = [1, 2]. We need to form [1, 1] from [1, 2] and one fillable.
We have [1, 2]. Need [1, 1].
We can change 2 to 1? No, we can only fill -1.
Wait.
Original A = [1, 2]. No -1.
So A is fixed as multiset {1, 2}.
Target A' = {1, 1}.
{1, 2} != {1, 1}.
So should be No.
Where is the error?
Ah, $N_A = N - len(K_A) = 2 - 2 = 0$.
$N_B = 2 - 2 = 0$.
$R = 2 - 0 = 2$.
My logic says Yes.
But we cannot change A.
The condition "multiset $K_A$ is sub-multiset of $T_S$" means $K_A \subseteq T_S$.
Here $K_A = \{1, 2\}$. $T_S = \{1, 1\}$.
$\{1, 2\} \not\subseteq \{1, 1\}$.
So my logic failed.
Why?
I assumed that if $|K_A| \le N_B$, we are good.
Here $|K_A| = 2, N_B = 0$. So $R = 2$.
We need to cover 2 elements using fixed slots.
Fixed slots come from $K_B$.
$K_B = \{10, 10\}$.
$S = 11$. $T_S = \{1, 1\}$.
$K_A = \{1, 2\}$.
$1 \in T_S$ (covered by fixed slot 1).
$2 \notin T_S$.
So we need to cover 2 using flexible slots.
But $N_B = 0$. No flexible slots.
So we fail.
My code checks `max_freq >= R`.
$M = \{1+10, 1+10, 2+10, 2+10\} = \{11, 11, 12, 12\}$.
Counts: 11:2, 12:2.
Max freq 2.
$2 \ge 2$. Returns Yes.
But it should be No.
The issue is that $fixed\_count(y, S)$ counts how many times $y$ appears in $T_S$.
In $T_S = \{1, 1\}$, $y=1$ appears 2 times. $y=2$ appears 0 times.
So $fixed\_count(1, 11) = 2$. $fixed\_count(2, 11) = 0$.
We need to cover $K_A = \{1, 2\}$.
Cover 1: needs 1 fixed slot. Available 2. OK.
Cover 2: needs 1 fixed slot. Available 0. Fail.
Total needed from fixed slots: 1 (for 1) + 1 (for 2) = 2?
No. The condition is:
Number of elements in $K_A$ that are NOT in $T_S$ (counting multiplicity) must be $\le N_B$.
In this case:
$K_A = \{1, 2\}$.
$T_S = \{1, 1\}$.
Intersection: $\{1\}$.
$K_A \setminus T_S = \{2\}$. Size 1.
$N_B = 0$.
$1 \le 0$ is False.
So we need to check if the number of "uncovered" elements is $\le N_B$.
My previous derivation:
$\sum \max(0, cnt(y) - fixed\_count(y, S)) \le N_B$.
In the example:
$y=1: cnt=1, fixed=2 \implies \max(0, -1) = 0$.
$y=2: cnt=1, fixed=0 \implies \max(0, 1) = 1$.
Sum = 1.
$1 \le 0$ False.
So my code logic was wrong.
The code checked `count(S in M) >= R`.
`count(S in M)` is $\sum_{y} fixed\_count(y, S)$.
This is the TOTAL number of fixed matches.
We need the number of FIXED matches to be at least $|K_A| - N_B$.
Wait.
Total elements in $K_A$ is $|K_A|$.
We can cover at most $N_B$ elements using flexible slots.
So we MUST cover at least $|K_A| - N_B$ elements using fixed slots.
So we need $\sum_{y} \min(cnt(y), fixed\_count(y, S)) \ge |K_A| - N_B$?
No.
We need to select a subset of $K_A$ of size $\ge |K_A| - N_B$ that is contained in $T_S$.
Actually, we just need to match as many elements of $K_A$ as possible to $T_S$.
Let $matched = \sum_{y} \min(cnt(y), fixed\_count(y, S))$.
We need $matched \ge |K_A| - N_B$.
In the example:
$y=1: \min(1, 2) = 1$.
$y=2: \min(1, 0) = 0$.
Total matched = 1.
$|K_A| - N_B = 2 - 0 = 2$.
$1 \ge 2$ False.
So the condition is:
Find $S$ such that $\sum_{y} \min(cnt(y), fixed\_count(y, S)) \ge |K_A| - N_B$.
This is different from `count(S in M) >= R`.
`count(S in M)` sums `fixed_count(y, S)` over all $y$.
But we can't use a fixed slot twice if it's the same slot?
No, $fixed\_count(y, S)$ is the number of slots $i \in V$ such that $S - B_i = y$.
These are distinct slots.
So if $T_S$ has two 1s, we can match two 1s from $K_A$.
So `count(S in M)` is indeed $\sum fixed\_count(y, S)$.
But we need to match specific $y$'s.
If $K_A$ has one 1 and one 2. $T_S$ has two 1s.
`count(S in M)` = 2 (two 1s).
But we can only match the 1. The 2 cannot be matched.
So we need to calculate the actual number of matches.
The number of matches is $\sum_{y} \min(cnt(y), fixed\_count(y, S))$.
This is not simply `count(S in M)`.
However, calculating this for every $S$ is hard.
But note: $fixed\_count(y, S)$ is non-zero only if $S = y + B_i$.
So for a fixed $S$, we iterate over all $y \in K_A$ and check if $S - y \in K_B$.
Actually, we can precompute counts of $K_B$.
Let `cntB` be Counter of $K_B$.
For a candidate $S$, `fixed_count(y, S)` = `cntB[S - y]`.
So we need to check:
`matches = 0`
`for y in K_A:`
  `if (S - y) in cntB:`
     `matches += min(cntA[y], cntB[S - y])`
`if matches >= R: return Yes`

This check is $O(|K_A|)$.
Total complexity: $O(N^2 \cdot N) = O(N^3)$.
$2000^3 = 8 \cdot 10^9$. Too slow.
We need a faster way.
Notice that `matches` is the size of the intersection of multisets $K_A$ and $T_S$.
$T_S = \{S - b \mid b \in K_B\} \cup \{S \text{ (N_B times)}\}$.
We need $|K_A \cap T_S| \ge R$.
Since $N_B$ is large, the flexible part can cover the rest.
Actually, if $|K_A \cap T_S| \ge R$, then we are good.
Can we optimize?
$|K_A \cap T_S| = \sum_{y} \min(cntA[y], cntB[S-y])$.
This looks like convolution.
But we only need to check specific $S$.
Candidates for $S$ are $y + b$.
There are $O(N^2)$ candidates.
For each candidate, we do $O(N)$ work. Total $O(N^3)$.
Is there a way to avoid $O(N)$ per candidate?
Maybe we don't need to check all candidates?
Or maybe $N=2000$ allows $O(N^2)$?
Yes, $O(N^2)$ is required.
How to get $O(N^2)$?
We need to check if there exists $S$ such that $\sum \min(cntA[y], cntB[S-y]) \ge R$.
This is equivalent to: Is there an $S$ such that the overlap is large enough.
Maybe we can iterate over $S$ differently?
No, $S$ is discrete.
Wait, if $R$ is small, maybe we only need a few matches?
But $R$ can be up to $N$.
Let's reconsider the condition.
We need to match at least $R$ elements.
If we pick $S$, the number of matches is the number of pairs $(y, b)$ such that $y+b=S$, weighted by multiplicities.
Actually, the number of matches is exactly the number of pairs $(y, b)$ such that $y+b=S$ AND we don't exceed counts?
No.
If $K_A = \{1, 1\}$, $K_B = \{1, 1\}$. $S=2$.
Pairs: $(1,1), (1,1)$. Count 2.
Matches = 2.
If $K_A = \{1, 2\}$, $K_B = \{1, 1\}$. $S=2$.
Pairs: $(1,1), (2,0)$ no.
Only $(1,1)$. Count 1.
Matches = 1.
So the number of matches is the number of pairs $(y, b)$ with $y+b=S$, but limited by counts?
Actually, if we just count pairs $(y, b)$ with $y+b=S$, that is exactly `count(S in M)`.
But we must respect counts.
Example: $K_A=\{1, 1\}$, $K_B=\{1, 1\}$. $S=2$.
Pairs: $(1,1)$ from first 1, $(1,1)$ from second 1. Total 2.
Matches = 2.
Example: $K_A=\{1, 1\}$, $K_B=\{1\}$. $S=2$.
Pairs: $(1,1)$ from first 1. $(1,1)$ from second 1.
But $K_B$ has only one 1.
So we can only match one 1.
Matches = 1.
So `count(S in M)` overcounts if multiplicities exceed.
So we need $\sum \min(cntA[y], cntB[S-y])$.
This is hard to compute fast for all $S$.
However, note that $cntB[S-y]$ is non-zero only if $S-y \in K_B$.
So we are summing over $y \in K_A$ such that $S-y \in K_B$.
This is exactly the number of pairs $(y, b)$ with $y+b=S$, MINUS the overcounting.
Overcounting happens if we have more pairs than available in one set.
But wait.
If we have many pairs, it means we have many matches.
The only case where `count(S in M)` > `matches` is when we have "too many" pairs.
But we need `matches >= R`.
If `count(S in M)` is large, `matches` is likely large.
Is it possible that `count(S in M)` is large but `matches` is small?
Yes, if $K_A$ has many 1s and $K_B$ has many 1s, but $S$ is such that $1+1=S$.
Then `count(S in M)` = $cntA[1] * cntB[1]$.
`matches` = $\min(cntA[1], cntB[1])$.
If $cntA[1]=100, cntB[1]=100$, `count`=10000, `matches`=100.
If $R=100$, both work.
If $R=1000$, `count` works, `matches` fails.
So we need the true `matches`.
But maybe we can bound $R$?
$R = |K_A| - N_B$.
If $R$ is small, we need few matches.
If $R$ is large, we need many matches.
Is there a property?
Actually, if $cntA[y] * cntB[S-y] \ge R$, then `matches` might be small?
No.
Let's go back to $O(N^2)$.
We can iterate over all $y \in K_A$.
For each $y$, we want to find $b \in K_B$ such that $S = y+b$ gives enough matches.
This seems hard.
Wait, $N=2000$. $O(N^2)$ is acceptable.
Can we compute the sum for all $S$ in $O(N^2)$?
Yes.
Let `cntA` and `cntB` be frequency maps.
We want to compute $F[S] = \sum_y \min(cntA[y], cntB[S-y])$.
This is not a standard convolution.
But notice that $\min(a, b) = a + b - \max(a, b)$.
Or $\min(a, b) = \sum_{k=1}^\infty [a \ge k \land b \ge k]$.
$F[S] = \sum_y \sum_{k=1}^{\min(cntA[y], cntB[S-y])} 1$.
This is counting pairs of pairs?
Actually, we can just iterate over all pairs $(y, b)$ and update a count.
Let `pair_counts` be a map where `pair_counts[y+b]` stores the number of pairs $(y, b)$ with that sum.
This is `count(S in M)`.
But we need the "min" version.
However, if we sort $K_A$ and $K_B$, we can do two pointers?
No, we need to check for existence of $S$.
Maybe we can just check the top few candidates?
No.
Wait, if $R$ is large, then $N_B$ is small.
If $N_B$ is small, we need many fixed matches.
If $N_B$ is large, $R$ is small, and we are likely to succeed.
Is it possible that $O(N^2)$ is not enough?
Maybe the constraints allow $O(N^2)$ and the test cases are weak?
No, competitive programming requires correct complexity.
Let's reconsider the condition.
We need to match at least $R$ elements.
If we pick $S$, the number of matches is the size of the intersection.
Is it possible to check this faster?
Actually, if we just compute `count(S in M)` and it is $\ge R$, is it sufficient?
In the example $K_A=\{1, 1\}, K_B=\{1\}, S=2$.
`count` = 2. $R = 2 - 1 = 1$.
$2 \ge 1$. Yes.
True matches = 1. $1 \ge 1$. Yes.
Example $K_A=\{1, 1, 1\}, K_B=\{1\}, S=2$.
`count` = 3. $R = 3 - 1 = 2$.
$3 \ge 2$. Yes.
True matches = 1. $1 \ge 2$. No.
So `count` can be misleading.
But in this case, $N_B = 1$. $R=2$.
We need 2 fixed matches. We have only 1.
So we fail.
The issue is when $cntA[y]$ is large and $cntB[S-y]$ is small.
But if $cntB[S-y]$ is small, then the number of available fixed slots for that $y$ is small.
So we can't match many.
But `count(S in M)` counts $cntA[y] * cntB[S-y]$.
If $cntB[S-y] = 1$, `count` = $cntA[y]$.
But matches = $\min(cntA[y], 1) = 1$.
So if $cntA[y]$ is large, `count` is large, but matches is 1.
So we need to handle this.
But notice: if $cntB[S-y] = k$, then we can match at most $k$ elements of $y$.
So the contribution to matches from $y$ is $\min(cntA[y], k)$.
The contribution to `count` is $cntA[y] * k$.
If $k=1$, contribution to matches is 1, to count is $cntA[y]$.
If $cntA[y]$ is large, count is large.
But we only need $R$ matches.
If $R$ is large, we need many matches.
If $R$ is small, we might get away with `count` being large?
No, we need exact matches.
However, note that if $cntB[S-y] \ge cntA[y]$, then `count` = $cntA[y]^2$? No, $cntA[y] * cntB[S-y]$.
If $cntB[S-y] \ge cntA[y]$, then matches = $cntA[y]$. Count = $cntA[y] * cntB[S-y] \ge cntA[y]$.
So if $cntB[S-y] \ge cntA[y]$, then `count` $\ge$ matches.
The problem is when $cntB[S-y] < cntA[y]$.
Then matches = $cntB[S-y]$. Count = $cntA[y] * cntB[S-y]$.
Here Count can be much larger than matches.
But if $cntB[S-y] < cntA[y]$, then the number of fixed slots available for $y$ is small.
So we can't match many.
But we need to sum over all $y$.
Total matches = $\sum \min(cntA[y], cntB[S-y])$.
Total count = $\sum cntA[y] * cntB[S-y]$.
If we have many $y$ with small $cntB[S-y]$, count can be large but matches small.
But if $cntB[S-y]$ is small for all $y$, then total matches is small.
Specifically, matches $\le \sum cntB[S-y] = \text{total fixed slots used}$.
Wait, $\sum_y cntB[S-y]$ is not well defined because $y$ varies.
Actually, $\sum_y cntB[S-y] = \sum_b cntA[S-b]$.
This is the number of pairs $(y, b)$ with $y+b=S$ where we ignore $cntA$ limit.
No.
Let's just implement the $O(N^2)$ check properly.
We have $O(N^2)$ candidates.
For each candidate, we need to compute matches in $O(N)$? No, that's $O(N^3)$.
But we can optimize the check.
We can iterate over $y \in K_A$. For each $y$, we iterate over $b \in K_B$.
This generates all pairs.
We can store the pairs in a list of $(S, y, b)$.
Then group by $S$.
For each $S$, we have a list of pairs.
We need to compute $\sum_y \min(cntA[y], cntB[S-y])$.
We can compute this by iterating over the unique $y$'s for that $S$.
But the number of pairs is $O(N^2)$.
The number of unique $S$ is $O(N^2)$.
For each $S$, the number of pairs is the number of $y$ such that $S-y \in K_B$.
Sum of number of pairs over all $S$ is $O(N^2)$.
So we can iterate over all pairs, group by $S$, and then for each $S$, compute the matches.
To compute matches for $S$:
We have a list of $y$'s (with multiplicities) and $b$'s (with multiplicities).
Actually, we can just use the counts.
For a fixed $S$, we iterate over all $y$ such that $cntA[y] > 0$ and $cntB[S-y] > 0$.
This is still potentially $O(N)$ per $S$.
But the total number of such $y$ across all $S$ is bounded?
No.
However, we only care if matches $\ge R$.
If we find one $S$ with matches $\ge R$, we stop.
Maybe we can just check the candidates with the highest `count(S in M)`?
If `count(S in M)` is small, matches is definitely small.
If `count(S in M)` is large, matches might be small (if distribution is skewed).
But if `count(S in M)` is very large, it's likely matches is large?
Not necessarily.
But given the constraints and problem type, maybe the intended solution is $O(N^2)$ with a simple check?
Or maybe the number of candidates with high `count` is small?
Actually, let's just implement the $O(N^2)$ grouping.
1. Compute `cntA`, `cntB`.
2. Generate all pairs $(y, b)$, compute $S = y+b$.
3. Store in a dictionary `S -> list of y`? No, we need counts.
4. Better: `S -> list of (y, count)`?
   No, just `S -> list of y` (with duplicates).
   Then for each $S$, we have a list of $y$'s.
   We also know `cntB`.
   For each $y$ in the list, we check `cntB[S-y]`.
   If `cntB[S-y] > 0`, we add `min(cntA[y], cntB[S-y])` to matches.
   But we must not double count if $y$ appears multiple times?
   The list of $y$'s will have duplicates.
   So we can just iterate the list.
   Total size of all lists is $O(N^2)$.
   For each element in the list, we do $O(1)$ work.
   So total time $O(N^2)$.
   Yes!
   Algorithm:
   - `cntA`, `cntB`.
   - `candidates = defaultdict(list)`
   - For `y` in `K_A`:
       For `b` in `K_B`:
           `candidates[y+b].append(y)`
   - `R = len(K_A) - N_B`
   - If `R <= 0`: Yes.
   - `min_S = max(max(K_B), max(K_A))`
   - For `S, ys` in `candidates.items()`:
       - If `S < min_S`: continue
       - `matches = 0`
       - For `y` in `ys`:
           - `b_needed = S - y`
           - `if b_needed in cntB:`
               - `matches += min(cntA[y], cntB[b_needed])`
               - `if matches >= R: return Yes`
   - Return No.

Wait, `matches += min(cntA[y], cntB[b_needed])` inside the loop over `ys` (which has duplicates) will overcount.
Example: $K_A=\{1, 1\}$, $K_B=\{1\}$. $S=2$.
`ys` = [1, 1].
First 1: `matches += min(2, 1) = 1`.
Second 1: `matches += min(2, 1) = 1`.
Total 2. Correct matches = 1.
So we must not iterate duplicates.
We should iterate unique $y$'s with their counts.
`S -> list of (y, count)`?
No, `cntA[y]` is the count.
So `ys` should be unique $y$'s present in `K_A` such that $S-y \in K_B$.
So:
`candidates = defaultdict(list)`
For `y` in `K_A`:
    For `b` in `K_B`:
        `candidates[y+b].append(y)`
Then for each `S`, get unique `y`'s and their counts from `cntA`.
But `candidates[S]` contains duplicates.
We can just use `set(ys)` to get unique $y$'s.
Then for each unique $y$, `matches += min(cntA[y], cntB[S-y])`.
This is $O(\text{number of unique } y \text{ for } S)$.
Sum of unique $y$ over all $S$ is at most $O(N^2)$?
Yes, because each pair $(y, b)$ contributes to one $S$.
The number of unique $y$ for a given $S$ is at most $|K_A|$.
Sum of unique $y$ over all $S$ is $\le \sum_S |K_A| = O(N^3)$?
No.
The number of pairs is $O(N^2)$.
The number of unique $y$ for $S$ is at most the number of pairs for $S$.
So sum of unique $y$ over all $S$ is $\le O(N^2)$.
So total time is $O(N^2)$.
Perfect.

```python
import sys
from collections import Counter, defaultdict

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    K_A = [x for x in A if x != -1]
    K_B = [x for x in B if x != -1]
    
    len_K_A = len(K_A)
    len_K_B = len(K_B)
    
    N_A = N - len_K_A
    N_B = N - len_K_B
    
    R = len_K_A - N_B
    
    if R <= 0:
        print("Yes")
        return

    max_K_B = max(K_B) if K_B else 0
    max_K_A = max(K_A) if K_A else 0
    min_S = max(max_K_B, max_K_A)
    
    cntA = Counter(K_A)
    cntB = Counter(K_B)
    
    # Group y by S = y + b
    # We only need to store y for each S
    # To avoid O(N^3), we iterate pairs and group
    # But we need unique y for each S to compute matches efficiently
    
    # candidates[S] will store a list of y's (with duplicates)
    # Then we convert to unique y's
    candidates = defaultdict(list)
    
    for y in K_A:
        for b in K_B:
            s = y + b
            if s >= min_S:
                candidates[s].append(y)
    
    # Now check each S
    for s, ys in candidates.items():
        # Get unique y's
        unique_ys = set