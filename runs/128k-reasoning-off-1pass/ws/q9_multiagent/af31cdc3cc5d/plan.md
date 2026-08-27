The problem asks us to pair up all elements in the sequence such that the sum of absolute differences of paired elements is maximized. Since we remove adjacent pairs until one element remains (or rather, the problem implies pairing up $N-1$ elements if $N$ is even, or $N-1$ elements leaving one out if $N$ is odd? Wait, let's re-read carefully: "until the sequence has length at most 1". Each operation removes 2 elements. So if $N$ is even, we perform $N/2$ operations and remove all elements. If $N$ is odd, we perform $(N-1)/2$ operations and remove $N-1$ elements, leaving 1. In both cases, we are effectively partitioning the sequence into $\lfloor N/2 \rfloor$ pairs of adjacent elements (at the time of removal).

Actually, a key insight for this specific problem (often found in competitive programming contexts like AtCoder) is that the maximum score is achieved by pairing the smallest available number with the largest available number in a specific alternating pattern, or more simply, sorting the array and pairing $A_1$ with $A_2$, $A_3$ with $A_4$, etc., but that's not quite right because adjacency matters.

Let's reconsider the structure. We start with $A_1, A_2, \dots, A_N$. We pick adjacent $A_i, A_{i+1}$, remove them, score $|A_i - A_{i+1}|$. The remaining elements become adjacent.
Consider the contribution of each $A_i$ to the final sum. In any valid sequence of operations, every element except possibly one (if $N$ is odd) will be part of exactly one pair. If $N$ is even, all elements are paired. If $N$ is odd, one element is left out.
To maximize $\sum |x - y|$, we generally want to pair the largest numbers with the smallest numbers.
However, the constraint is adjacency.
Let's look at Sample 1: `1 2 5 3`. Pairs `(2,5)` and `(1,3)`. Score $|2-5| + |1-3| = 3 + 2 = 5$.
Sorted: `1 2 3 5`. If we pair `(1,5)` and `(2,3)`, score $4+1=5$.
Is it possible the answer is simply the sum of differences of sorted elements with a specific pattern?
Actually, there is a known result for this problem. The maximum score is obtained by sorting the array $B$ such that $B_1 \le B_2 \le \dots \le B_N$. Then the answer is $\sum_{i=1}^{N/2} (B_{2i} - B_{2i-1})$? No, that would be pairing smallest with second smallest, etc. That minimizes the sum of differences? No, $|a-b| + |c-d|$. If we have 1, 10, 20, 30.
Pair (1,10) and (20,30) -> 9 + 10 = 19.
Pair (1,30) and (10,20) -> 29 + 10 = 39. But (1,30) are not adjacent initially.
Wait, the operation allows removing adjacent elements, which brings non-adjacent elements together.
So effectively, we can choose ANY partition of the array into pairs $(u, v)$ such that the pairs can be formed by a sequence of adjacent removals.
It turns out that ANY pairing of the elements is possible IF $N$ is even? No.
Let's trace Sample 1 again. `1 2 5 3`.
Option 1: Remove (2,5). Seq: `1 3`. Remove (1,3). Total 5.
Option 2: Remove (1,2). Seq: `5 3`. Remove (5,3). Total $1 + 2 = 3$.
Option 3: Remove (5,3). Seq: `1 2`. Remove (1,2). Total $2 + 1 = 3$.
Max is 5.
Notice that in the optimal solution, we paired 2 with 5 and 1 with 3.
Original indices: 1, 2, 3, 4. Values: 1, 2, 5, 3.
Pairs: (2,5) and (1,3).
Is it true that we can always achieve the sum $\sum_{i=1}^{N/2} (B_{2i} - B_{2i-1})$ where $B$ is sorted?
Sorted: 1, 2, 3, 5.
$B_2-B_1 = 1$, $B_4-B_3 = 2$. Sum = 3. This is not 5.
What about $\sum_{i=1}^{N/2} (B_{2i+1} - B_{2i})$? (1-indexed, skipping first?)
Maybe $\sum_{i=1}^{N/2} (B_{N/2 + i} - B_i)$? No.

Let's rethink the contribution.
In the expression $\sum |x-y|$, to maximize, we want large numbers to be positive and small numbers to be negative in the expansion $\sum s_i A_i$ where $s_i \in \{1, -1\}$.
Specifically, if we have pairs $(x_1, y_1), \dots, (x_k, y_k)$, the sum is $\sum |x_j - y_j|$.
If we sort the final set of paired numbers, say we have $2k$ numbers involved (if $N$ even).
The maximum possible sum of absolute differences for a set of $2k$ numbers is achieved by pairing the smallest with the largest, second smallest with second largest, etc.
Sum = $(L_k + L_{k-1} + \dots + L_1) - (S_k + S_{k-1} + \dots + S_1)$ where $L$ are largest $k$, $S$ are smallest $k$.
Basically, sort the array $A$. The max score is $\sum_{i=k+1}^{2k} A_i - \sum_{i=1}^k A_i$ where $2k=N$.
Let's test this hypothesis on Sample 1: `1 2 5 3`. Sorted: `1 2 3 5`. $N=4, k=2$.
Sum = $(3+5) - (1+2) = 8 - 3 = 5$. Matches!
Sample 2: `3 1 4 1 5 9 2`. $N=7$. We perform 3 operations, removing 6 numbers. One number is left out.
To maximize the score, we should leave out the number that hurts us the least (or helps the most).
If we leave out a number $x$, we are left with 6 numbers. We want to maximize the sum of diffs of the remaining 6.
The formula for $2k$ numbers is $\sum_{i=k+1}^{2k} B_i - \sum_{i=1}^k B_i$.
This is equivalent to $\sum_{i=1}^{2k} c_i B_i$ where $c_i = 1$ for the top $k$ and $c_i = -1$ for the bottom $k$.
The sum of coefficients is 0.
If we have $N$ numbers and remove one, we have $N-1$ numbers. Let $N-1 = 2k$.
We want to choose a subset of size $2k$ and a pairing to maximize the sum.
Actually, the optimal strategy for $N$ numbers (even or odd) is:
Sort $A$.
If $N$ is even, answer is $\sum_{i=N/2+1}^N A_i - \sum_{i=1}^{N/2} A_i$.
If $N$ is odd, we leave out one element. Which one?
The formula for a subset of size $2k$ is $\sum_{j=1}^k (B_{2k+1-j} - B_j)$? No, it's $\sum_{j=1}^k (B_{2k-j+1} - B_j)$?
Let's re-verify the "largest minus smallest" logic.
For set $\{1, 2, 3, 5\}$, pairs $(1,5)$ and $(2,3)$ give $|1-5| + |2-3| = 4+1=5$.
Coefficients: $-1, -1, 1, 1$ for sorted array. Sum = $5+3 - (1+2) = 5$.
Yes, the pattern is: take the largest $k$ elements with coefficient $+1$ and the smallest $k$ elements with coefficient $-1$.
Now, if $N$ is odd, we have $N$ elements. We must leave one out.
We want to maximize $\sum_{i \in S_{large}} A_i - \sum_{j \in S_{small}} A_j$ where $|S_{large}| = |S_{small}| = (N-1)/2$.
This is equivalent to assigning coefficients $+1$ to $(N-1)/2$ elements, $-1$ to $(N-1)/2$ elements, and $0$ to 1 element.
To maximize the sum, we should assign $+1$ to the largest available, $-1$ to the smallest available, and $0$ to the one that minimizes the loss.
Actually, simply: Sort $A$.
We need to choose signs $s_i \in \{-1, 0, 1\}$ such that $\sum s_i = 0$ (since total count of +1 equals total count of -1) and maximize $\sum s_i A_i$.
The optimal assignment is:
$s_i = 1$ for $i \in \{ \frac{N+1}{2} + 1, \dots, N \}$ (the largest $(N-1)/2$)
$s_i = -1$ for $i \in \{ 1, \dots, \frac{N-1}{2} \}$ (the smallest $(N-1)/2$)
$s_i = 0$ for the middle element $i = \frac{N+1}{2}$.
Let's check Sample 2: `3 1 4 1 5 9 2`. Sorted: `1 1 2 3 4 5 9`. $N=7$.
$k = 3$.
Smallest 3: 1, 1, 2. Sum = 4. Coeff -1.
Largest 3: 4, 5, 9. Sum = 18. Coeff +1.
Middle: 3. Coeff 0.
Result: $18 - 4 = 14$. Matches Sample Output 2!
Sample 3: `1 1 1 1 1`. Sorted: `1 1 1 1 1`.
Smallest 2: 1, 1. Sum 2.
Largest 2: 1, 1. Sum 2.
Middle: 1.
Result: $2 - 2 = 0$. Matches Sample Output 3!

So the algorithm is:
1. Read $N$ and array $A$.
2. Sort $A$.
3. If $N$ is even:
   Sum = $\sum_{i=N/2}^{N-1} A[i] - \sum_{i=0}^{N/2-1} A[i]$ (using 0-based indexing).
4. If $N$ is odd:
   Sum = $\sum_{i=(N-1)/2 + 1}^{N-1} A[i] - \sum_{i=0}^{(N-1)/2 - 1} A[i]$.
   Wait, let's re-index carefully.
   Indices $0$ to $N-1$.
   Count of +1: $k = (N-1)/2$. Indices: $N-k$ to $N-1$.
   Count of -1: $k$. Indices: $0$ to $k-1$.
   Index $k$ is 0.
   Example $N=7, k=3$.
   +1: indices $7-3=4$ to $6$ (values 4, 5, 9). Correct.
   -1: indices $0$ to $2$ (values 1, 1, 2). Correct.
   0: index 3 (value 3). Correct.

General formula:
Sort $A$.
Result = $\sum_{i=\lceil N/2 \rceil}^{N-1} A[i] - \sum_{i=0}^{\lceil N/2 \rceil - 1} A[i]$?
If $N=4$, $\lceil 2 \rceil = 2$.
Sum $A[2..3] - A[0..1]$. Correct.
If $N=7$, $\lceil 3.5 \rceil = 4$.
Sum $A[4..6] - A[0..3]$.
Wait, for $N=7$, we want $A[0..2]$ (-1) and $A[4..6]$ (+1). Index 3 is 0.
My previous manual calc: $A[0..2]$ and $A[4..6]$.
The range $0$ to $\lceil N/2 \rceil - 1$ for $N=7$ is $0$ to $3$. That includes index 3 which should be 0.
So the simple split at $N/2$ doesn't work directly for odd $N$ if we just subtract.
Correct logic:
$k = (N-1)//2$.
Sum = (sum of last $k$) - (sum of first $k$).
If $N$ is even, $k = N/2$. Sum = (last $N/2$) - (first $N/2$).
If $N$ is odd, $k = (N-1)/2$. Sum = (last $k$) - (first $k$). The middle element is ignored.

Implementation details:
Read N.
Read list A.
Sort A.
Calculate $k = N // 2$.
If $N$ is even:
  ans = sum(A[N-k:]) - sum(A[:k])
If $N$ is odd:
  ans = sum(A[N-k:]) - sum(A[:k])
  (Note: for odd N, N-k = N - (N-1)/2 = (N+1)/2. The slice A[N-k:] starts at the element after the middle one. A[:k] is the first k. The middle element is at index k, which is excluded from both slices. This works perfectly.)

Wait, check $N=7, k=3$.
$N-k = 4$. A[4:] is indices 4,5,6. Correct.
A[:3] is indices 0,1,2. Correct.
Index 3 is skipped. Correct.
Check $N=4, k=2$.
$N-k = 2$. A[2:] is 2,3. Correct.
A[:2] is 0,1. Correct.
So the logic is simply: $k = N // 2$. Answer is sum of last $k$ minus sum of first $k$.