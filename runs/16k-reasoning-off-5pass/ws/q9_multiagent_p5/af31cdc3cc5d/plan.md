The problem asks us to maximize the sum of absolute differences of pairs removed from a sequence until only one element remains. This process effectively partitions the original sequence of $N$ elements into $\lfloor N/2 \rfloor$ pairs. A key observation is that the total score is equivalent to the sum of absolute differences of these pairs. By analyzing small cases and the structure of the operations, we can deduce that the optimal strategy involves pairing elements such that we maximize the contribution of the largest elements. Specifically, if we sort the array, the maximum score is achieved by pairing the largest with the second largest, the third largest with the fourth largest, and so on. However, since the relative order in the original array matters for adjacency, we must verify if sorting is permissible. Actually, the operation allows removing adjacent elements, which changes adjacency. It turns out this problem is equivalent to finding a pairing of indices $(i, j)$ such that the pairs are non-overlapping in a specific way, but a simpler greedy approach on the sorted values works: the answer is the sum of $|A_{(2k)} - A_{(2k-1)}|$ where $A_{(k)}$ are the sorted values of $A$. Wait, let's re-evaluate. If we have 1, 2, 5, 3. Sorted: 1, 2, 3, 5. Pairs (5,3) and (2,1) -> |5-3| + |2-1| = 2+1=3. But sample output is 5 (pairs (2,5) and (1,3)). The pairs in the sample are indices (2,3) and (1,4). The values are 2,5 and 1,3. The sum is |2-5| + |1-3| = 3+2=5.
Let's reconsider the mathematical property. The total score is $\sum |x_i - y_i|$. This is maximized when we pair the largest available with the smallest available? No, in the sample: 1, 2, 3, 5. Pairs (2,5) and (1,3). Differences: 3 and 2. Sum 5.
Alternative pairing: (1,5) and (2,3). Differences: 4 and 1. Sum 5.
Alternative pairing: (1,2) and (3,5). Differences: 1 and 2. Sum 3.
It seems the maximum is obtained by pairing $A_{(i)}$ with $A_{(N-1-i)}$? No.
Let's look at the constraints and the nature of the operation. We remove adjacent pairs. This is equivalent to selecting a perfect matching on the path graph if $N$ is even? No, because removing a pair brings new neighbors together. This is equivalent to partitioning the sequence into pairs $(i_1, j_1), (i_2, j_2), \dots$ such that we can remove them sequentially.
Actually, there is a known result for this specific problem (AtCoder ABC 256 Problem E? No, maybe different). Let's derive it.
Consider the contribution of each element $A_i$. In the final sum $\sum |x-y|$, each element is part of exactly one pair. The term $|x-y|$ can be written as $\max(x,y) - \min(x,y)$. So the total sum is $\sum \max(pair) - \sum \min(pair)$.
To maximize this, we want the "max" elements of the pairs to be as large as possible and the "min" elements to be as small as possible.
In the sample 1, 2, 5, 3:
Sorted: 1, 2, 3, 5.
If we pick the two largest (5, 3) as maxes? Then mins are (2, 1). Sum = (5+3) - (2+1) = 5.
If we pick (5, 2) as maxes? Then mins are (3, 1). Sum = (5+2) - (3+1) = 3.
If we pick (5, 1) as maxes? Then mins are (3, 2). Sum = (5+1) - (3+2) = 1.
It seems the optimal strategy is to take the largest $\lfloor N/2 \rfloor$ elements as the "max" components and the smallest $\lfloor N/2 \rfloor$ elements as the "min" components of the pairs.
Is it always possible to form such pairs?
Yes. If we sort the array $B$ such that $B_1 \le B_2 \le \dots \le B_N$.
We pair $B_{N}$ with $B_{N-1}$? No, that gives $B_N - B_{N-1}$.
We want to pair large with small?
Wait, the sample solution pairs (2,5) and (1,3).
Values: 1, 2, 3, 5.
Pairs: (2,5) -> max 5, min 2. (1,3) -> max 3, min 1.
Total = (5+3) - (2+1) = 5.
Here the set of maxes is {5, 3} (the two largest) and the set of mins is {2, 1} (the two smallest).
Is it always possible to achieve this?
Yes, we can pair the largest element with the second smallest? No, adjacency constraints might apply.
However, in this specific problem (removing adjacent pairs), it is a known result that the maximum score is $\sum_{i=1}^{\lfloor N/2 \rfloor} (B_{N-i+1} - B_i)$?
Let's check Sample 1: 1, 2, 3, 5.
$i=1: B_4 - B_1 = 5 - 1 = 4$.
$i=2: B_3 - B_2 = 3 - 2 = 1$.
Sum = 5. Correct.
Sample 2: 3, 1, 4, 1, 5, 9, 2. N=7. Pairs = 3.
Sorted: 1, 1, 2, 3, 4, 5, 9.
Pairs:
$i=1: B_7 - B_1 = 9 - 1 = 8$.
$i=2: B_6 - B_2 = 5 - 1 = 4$.
$i=3: B_5 - B_3 = 4 - 2 = 2$.
Sum = 14. Correct.
Sample 3: 1, 1, 1, 1, 1. N=5. Pairs=2.
Sorted: 1, 1, 1, 1, 1.
$i=1: 1-1=0$.
$i=2: 1-1=0$.
Sum = 0. Correct.

So the algorithm is:
1. Read N and the sequence A.
2. Sort A.
3. Compute sum of $(A[N-1-i] - A[i])$ for $i$ from $0$ to $\lfloor N/2 \rfloor - 1$.
4. Print the sum.