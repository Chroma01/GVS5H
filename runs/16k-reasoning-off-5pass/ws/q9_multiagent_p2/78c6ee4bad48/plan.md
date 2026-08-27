The operation allows us to reflect the $(i+1)$-th and $(i+2)$-th pieces across the midpoint of the $i$-th and $(i+3)$-th pieces. Mathematically, if the coordinates are $x_i, x_{i+1}, x_{i+2}, x_{i+3}$, the new coordinates become $x_i, 2M-x_{i+1}, 2M-x_{i+2}, x_{i+3}$ where $M = (x_i + x_{i+3})/2$. This transformation preserves the sum of the four involved coordinates ($x_i + x_{i+3} + (2M-x_{i+1}) + (2M-x_{i+2}) = x_i + x_{i+3} + (x_i+x_{i+3}) - (x_{i+1}+x_{i+2}) + (x_{i+1}+x_{i+2}) = 2(x_i+x_{i+3})$? Wait, let's re-calculate the sum change.
Original sum of 4: $S = x_i + x_{i+1} + x_{i+2} + x_{i+3}$.
New sum of 4: $S' = x_i + (2M - x_{i+1}) + (2M - x_{i+2}) + x_{i+3} = x_i + x_{i+3} + 4M - (x_{i+1} + x_{i+2})$.
Since $2M = x_i + x_{i+3}$, then $4M = 2(x_i + x_{i+3})$.
$S' = x_i + x_{i+3} + 2(x_i + x_{i+3}) - (x_{i+1} + x_{i+2}) = 3(x_i + x_{i+3}) - (x_{i+1} + x_{i+2})$.
Change in sum: $\Delta = S' - S = 2(x_i + x_{i+3}) - 2(x_{i+1} + x_{i+2}) = 2[(x_i + x_{i+3}) - (x_{i+1} + x_{i+2})]$.
To minimize the total sum, we want to perform operations where $x_i + x_{i+3} < x_{i+1} + x_{i+2}$, making the sum decrease.
Notice that this operation is equivalent to swapping the relative order of the middle two elements with respect to the outer two in a specific way, or more simply, it allows us to "bubble" the smallest elements to the left and largest to the right.
Actually, consider the effect on the sorted order. The problem states pieces remain distinct and we can repeat operations. The key insight in similar problems is that we can effectively sort the array such that the smallest elements are at the beginning and largest at the end, but the operation is local.
However, there is a simpler invariant or reachable state. Let's look at the operation again.
$x_{i+1}' = x_i + x_{i+3} - x_{i+1}$
$x_{i+2}' = x_i + x_{i+3} - x_{i+2}$
This looks like we are reflecting the middle pair.
Consider the case where we want to minimize the sum. We should try to make the left elements as small as possible and right elements as small as possible? No, the sum is just the sum. We want to reduce the sum.
If $x_i + x_{i+3} < x_{i+1} + x_{i+2}$, we can reduce the sum.
Can we reach a state where the array is sorted? The input is already sorted.
Wait, if the array is sorted $x_1 < x_2 < x_3 < x_4$, then $x_1+x_4$ vs $x_2+x_3$.
If $x_1+x_4 < x_2+x_3$, we can reduce the sum.
Example 1: 1, 5, 7, 10. $1+10 = 11$, $5+7=12$. $11 < 12$, so we can reduce.
Result: 1, 6, 4, 10. Sorted: 1, 4, 6, 10. Sum = 21.
Notice the new set of values is $\{1, 4, 6, 10\}$. The original was $\{1, 5, 7, 10\}$.
It seems we can transform the array into a state where the values are "more balanced" or specifically, we can achieve the state where the array is sorted but the values are the "median" of the original segments?
Actually, there is a known result for this specific problem (AtCoder ABC 244 F? No, likely a different contest).
Let's re-evaluate the operation's capability.
The operation on indices $i, i+1, i+2, i+3$ transforms $(a, b, c, d)$ to $(a, a+d-b, a+d-c, d)$.
Notice that $a+d-b + a+d-c = 2(a+d) - (b+c)$.
The set of values changes.
However, observe the sum of the first $k$ elements or some prefix sums.
Let's look at the sample 2: 0, 1, 6, 10, 14, 16.
Pairs: (0,16) sum 16, (1,14) sum 15. $16 > 15$, no reduction possible with $i=1$?
Wait, $x_1+x_4 = 0+10=10$, $x_2+x_3 = 1+6=7$. $10 > 7$. No reduction.
$x_2+x_5 = 1+14=15$, $x_3+x_4 = 6+10=16$. $15 < 16$. Reduction possible at $i=2$.
Operation on 2,3,4,5 (values 1, 6, 10, 14):
$M = (1+14)/2 = 7.5$.
New 3rd: $7.5 - (6-7.5) = 8.5$? No.
Formula: $x_{i+1}' = 2M - x_{i+1} = (x_i+x_{i+3}) - x_{i+1}$.
$x_3' = 1+14 - 6 = 9$.
$x_4' = 1+14 - 10 = 5$.
New array: 0, 1, 9, 5, 14, 16. Sorted: 0, 1, 5, 9, 14, 16.
Sum change: Old sum of 4 was $1+6+10+14=31$. New sum $1+9+5+14=29$. Decrease by 2.
New total sum: $0+1+5+9+14+16 = 45$. Original sum: $0+1+6+10+14+16 = 47$.
Can we do more?
Check $i=1$: $0+9=9$, $1+5=6$. $9>6$. No.
Check $i=2$: $1+14=15$, $5+9=14$. $15>14$. No.
Check $i=3$: $9+16=25$, $14+?$. Wait, indices 3,4,5,6: $9, 5, 14, 16$.
$x_3+x_6 = 9+16=25$. $x_4+x_5 = 5+14=19$. $25>19$. No.
It seems we reached a local minimum.
Is there a pattern?
In Sample 1: 1, 5, 7, 10 -> 1, 4, 6, 10.
Original: 1, 5, 7, 10.
New: 1, 4, 6, 10.
Notice $4 = (1+7)/2$? No. $4 = 1+7-5$? No.
$4 = 1+10-7 = 4$. $6 = 1+10-5 = 6$.
So the new values are $x_1, x_1+x_4-x_3, x_1+x_4-x_2, x_4$.
Basically, we replaced $x_2, x_3$ with $x_1+x_4-x_3, x_1+x_4-x_2$.
This operation is reversible? If we apply it again on the new sorted array?
The problem asks for the MINIMUM sum.
Hypothesis: We can sort the array such that the final configuration is the sorted version of the array where we have "flattened" the convex hulls?
Actually, consider the operation $x_{i+1} \leftarrow x_i + x_{i+3} - x_{i+1}$.
This is equivalent to $x_{i+1} - x_i = x_{i+3} - x_{i+1}'$.
Let $d_k = x_{k+1} - x_k$.
Then $x_{i+1}' - x_i = (x_i + x_{i+3} - x_{i+1}) - x_i = x_{i+3} - x_{i+1} = d_{i+1} + d_{i+2}$.
And $x_{i+2}' - x_{i+1}' = (x_i + x_{i+3} - x_{i+2}) - (x_i + x_{i+3} - x_{i+1}) = x_{i+1} - x_{i+2} = -d_{i+2}$.
Wait, the order of elements changes.
The new sequence of differences for the 4 elements:
$d_i' = x_{i+1}' - x_i = d_{i+1} + d_{i+2}$.
$d_{i+1}' = x_{i+2}' - x_{i+1}' = x_{i+1} - x_{i+2} = -d_{i+2}$. (This would imply negative distance if we keep order, but the pieces are just points. The problem says "ascending order". So we must re-sort the points after each operation?
"Choose an integer i... move...". The pieces are distinct. After moving, their coordinates change. The "i-th piece" refers to the piece currently at the i-th position in the sorted order.
So the operation is dynamic based on current sorted order.
However, notice the sample 1 result: 1, 4, 6, 10.
Differences: 3, 2, 4.
Original: 1, 5, 7, 10. Differences: 4, 2, 3.
It seems we swapped the differences 4 and 3?
Original diffs: $d_1=4, d_2=2, d_3=3$.
New diffs: $3, 2, 4$.
It looks like the operation swaps $d_i$ and $d_{i+2}$?
Let's check Sample 2.
Original: 0, 1, 6, 10, 14, 16.
Diffs: 1, 5, 4, 4, 2.
Operation at $i=2$ (indices 2,3,4,5 in 1-based sorted array):
Values involved: $x_2=1, x_3=6, x_4=10, x_5=14$.
New values: $x_2'=1+14-6=9$, $x_3'=1+14-10=5$.
New array: 0, 1, 5, 9, 14, 16.
New diffs: $1, 4, 4, 5, 2$.
Original segment diffs (indices 2 to 5): $d_2=5, d_3=4, d_4=4$.
New segment diffs: $d_2'=4, d_3'=4, d_4'=5$.
It seems the operation swaps $d_i$ and $d_{i+2}$?
Original: $d_2=5, d_3=4, d_4=4$.
New: $d_2=4, d_3=4, d_4=5$.
Yes! $d_2$ and $d_4$ were swapped. $d_3$ stayed same.
Wait, $d_2$ was 5, became 4. $d_4$ was 4, became 5. $d_3$ was 4, stayed 4.
So the operation allows swapping $d_i$ and $d_{i+2}$ for any $i$ from $1$ to $N-3$.
This means we can perform adjacent swaps on the array of differences with stride 2?
We can swap $d_1, d_3, d_5, \dots$ among themselves arbitrarily.
And we can swap $d_2, d_4, d_6, \dots$ among themselves arbitrarily.
We cannot swap an odd-indexed difference with an even-indexed difference.
The total sum of coordinates is $\sum x_i = \sum_{k=1}^N (N-k+1) d_k$ (assuming $x_0=0$? No, $x_1 = d_1$, $x_2 = d_1+d_2$, etc. $x_k = \sum_{j=1}^k d_j$).
Sum $S = \sum_{k=1}^N x_k = \sum_{k=1}^N \sum_{j=1}^k d_j = \sum_{j=1}^N d_j (N-j+1)$.
To minimize $S$, we need to assign the smallest differences to the largest coefficients $(N-j+1)$.
The coefficients are $N, N-1, \dots, 1$.
We have two independent sets of differences:
Set A (odd indices): $d_1, d_3, d_5, \dots$
Set B (even indices): $d_2, d_4, d_6, \dots$
We can sort Set A in ascending order and place them at positions $1, 3, 5, \dots$.
We can sort Set B in ascending order and place them at positions $2, 4, 6, \dots$.
This will minimize the weighted sum because larger coefficients get smaller values.
Wait, is it possible to swap $d_i$ and $d_{i+2}$?
The operation on $i$ swaps $d_i$ and $d_{i+2}$.
Yes, this is a standard bubble sort logic on the subsequence of odd indices and even indices separately.
So the algorithm is:
1. Calculate initial differences $d_1, d_2, \dots, d_{N-1}$.
2. Separate them into two lists: `odds` (indices 1, 3, ...) and `evens` (indices 2, 4, ...).
3. Sort both lists in ascending order.
4. Reconstruct the differences array by placing sorted `odds` back into odd positions and sorted `evens` back into even positions.
5. Compute the prefix sums to get $x_i$, then sum them up.

Let's double check with Sample 1.
X: 1, 5, 7, 10.
Diffs: $d_1=4, d_2=2, d_3=3$.
Odds: $[4, 3]$. Sorted: $[3, 4]$.
Evens: $[2]$. Sorted: $[2]$.
Reconstructed: $d_1=3, d_2=2, d_3=4$.
X: $3, 3+2=5, 5+4=9$?
Wait. $x_1 = 3$. $x_2 = 3+2=5$. $x_3 = 5+4=9$. $x_4 = 9+?$.
Ah, the number of differences is $N-1$.
Sample 1 has $N=4$, so 3 diffs.
Reconstructed: $d_1=3, d_2=2, d_3=4$.
$x_1 = 3$.
$x_2 = 3+2=5$.
$x_3 = 5+4=9$.
$x_4 = 9 + d_4$? No, $d_4$ doesn't exist.
Wait, the coordinates are $X_1, \dots, X_N$.
$X_1 = d_1$.
$X_2 = d_1+d_2$.
$X_3 = d_1+d_2+d_3$.
$X_4 = d_1+d_2+d_3+d_4$? No, $X_N$ is the last coordinate.
The differences are $X_2-X_1, X_3-X_2, \dots, X_N-X_{N-1}$.
There are $N-1$ differences.
In Sample 1: $X_1=1, X_2=5, X_3=7, X_4=10$.
$d_1 = 5-1=4$.
$d_2 = 7-5=2$.
$d_3 = 10-7=3$.
Odds: $d_1, d_3 \to \{4, 3\}$. Sorted: $\{3, 4\}$.
Evens: $d_2 \to \{2\}$.
New diffs: $d_1=3, d_2=2, d_3=4$.
New coords:
$X_1 = 3$.
$X_2 = 3+2=5$.
$X_3 = 5+4=9$.
$X_4 = ?$
Wait, the sum of coordinates must be calculated from the new $X$'s.
But the problem says "minimize sum of coordinates".
Is $X_1$ fixed?
The operation changes the coordinates.
Let's re-read the operation carefully.
"Move each of the (i+1)-th and (i+2)-th pieces... to positions symmetric to M".
The 1st and (i+3)-th pieces (which are $x_i$ and $x_{i+3}$) do NOT move.
So $x_i$ and $x_{i+3}$ remain fixed.
In my diff swap logic:
$d_i = x_{i+1}-x_i$.
$d_{i+2} = x_{i+3}-x_{i+1}$.
After op: $x_{i+1}' = x_i + x_{i+3} - x_{i+1}$.
$d_i' = x_{i+1}' - x_i = x_{i+3} - x_{i+1} = d_{i+2}$.
$d_{i+2}' = x_{i+3} - x_{i+2}' = x_{i+3} - (x_i + x_{i+3} - x_{i+2}) = x_{i+2} - x_i = d_i + d_{i+1}$?
Wait.
$x_{i+2}' = x_i + x_{i+3} - x_{i+2}$.
$d_{i+1}' = x_{i+2}' - x_{i+1}' = (x_i + x_{i+3} - x_{i+2}) - (x_i + x_{i+3} - x_{i+1}) = x_{i+1} - x_{i+2} = -d_{i+1}$.
This implies the order of points might flip?
But the problem says "ascending order".
If $x_{i+1} < x_{i+2}$ initially, then $x_{i+1}' > x_{i+2}'$?
$x_{i+1}' - x_{i+2}' = -(x_{i+1}-x_{i+2}) = x_{i+2}-x_{i+1} > 0$.
So $x_{i+1}' < x_{i+2}'$ is FALSE.
$x_{i+1}' = x_i + x_{i+3} - x_{i+1}$.
$x_{i+2}' = x_i + x_{i+3} - x_{i+2}$.
Since $x_{i+1} < x_{i+2}$, then $-x_{i+1} > -x_{i+2}$, so $x_{i+1}' > x_{i+2}'$.
So the new positions are swapped in terms of magnitude relative to the original middle pair?
But the problem says "move ... to positions symmetric".
Then we must re-sort the array to identify the $k$-th piece for the next operation.
The "i-th piece" in the next step refers to the piece with the $i$-th smallest coordinate.
So the set of coordinates changes, and we re-sort.
My previous deduction about swapping $d_i$ and $d_{i+2}$ assumed the indices $i, i+1, i+2, i+3$ refer to the sorted order BEFORE the operation, and the result is also sorted?
Let's check Sample 1 again.
Start: 1, 5, 7, 10. Sorted.
$i=1$. Pieces 1, 2, 3, 4.
$x_1=1, x_2=5, x_3=7, x_4=10$.
$M = 5.5$.
$x_2' = 5.5 + (5.5-5) = 6$.
$x_3' = 5.5 - (7-5.5) = 4$.
New coords: 1, 6, 4, 10.
Sorted: 1, 4, 6, 10.
The pieces that were at 2 and 3 are now at 4 and 6.
The piece that was at 1 is at 1.
The piece that was at 4 is at 10.
So the set of values is $\{1, 4, 6, 10\}$.
Diffs of new sorted array:
$4-1=3$.
$6-4=2$.
$10-6=4$.
Diffs: 3, 2, 4.
Original diffs: 4, 2, 3.
So indeed, $d_1$ (4) became 3 ($d_3$), $d_3$ (3) became 4 ($d_1$). $d_2$ (2) stayed 2.
So the operation on the sorted array effectively swaps $d_i$ and $d_{i+2}$ in the difference array of the sorted configuration.
And since we can do this for any $i$, we can sort the odd-indexed diffs and even-indexed diffs independently.
The logic holds.

Sample 2 Check:
0, 1, 6, 10, 14, 16.
Diffs: 1, 5, 4, 4, 2.
Odds (indices 1, 3, 5): 1, 4, 2. Sorted: 1, 2, 4.
Evens (indices 2, 4): 5, 4. Sorted: 4, 5.
Reconstructed diffs:
$d_1=1, d_2=4, d_3=2, d_4=5, d_5=4$.
Coords:
$x_1 = 1$.
$x_2 = 1+4=5$.
$x_3 = 5+2=7$.
$x_4 = 7+5=12$.
$x_5 = 12+4=16$.
$x_6 = 16 + d_6$? No, $N=6$, so 5 diffs.
Wait, $x_6$ is the last coordinate.
$x_6 = x_5 + d_5 = 16+4=20$?
But the original $x_6$ was 16.
Did the sum of diffs change?
Original sum of diffs: $1+5+4+4+2 = 16$.
New sum of diffs: $1+4+2+5+4 = 16$.
The total span $X_N - X_1$ is invariant?
In Sample 1: $10-1=9$. New: $10-1=9$.
In Sample 2: $16-0=16$. New: $20-1=19$?
Wait, $x_1$ is not necessarily 0.
In Sample 2, original $x_1=0$.
New $x_1 = d_1 = 1$.
So the whole array shifted?
The operation fixes $x_i$ and $x_{i+3}$.
In Sample 2, we operated on $i=2$ (indices 2,3,4,5).
$x_2$ and $x_5$ were fixed?
Original: $x_2=1, x_5=14$.
New: $x_2'=9, x_5'=14$?
Wait, in Sample 2 manual trace:
Original: 0, 1, 6, 10, 14, 16.
$i=2$ (pieces 2,3,4,5).
$x_2=1, x_3=6, x_4=10, x_5=14$.
$M = (1+14)/2 = 7.5$.
$x_3' = 7.5 + (7.5-6) = 9$.
$x_4' = 7.5 - (10-7.5) = 5$.
New set: 0, 1, 9, 5, 14, 16.
Sorted: 0, 1, 5, 9, 14, 16.
Here $x_1=0$ (unchanged). $x_6=16$ (unchanged).
The diffs of sorted new array:
$1-0=1$.
$5-1=4$.
$9-5=4$.
$14-9=5$.
$16-14=2$.
Diffs: 1, 4, 4, 5, 2.
Original diffs: 1, 5, 4, 4, 2.
Odds (1, 3, 5): 1, 4, 2. Sorted: 1, 2, 4.
Evens (2, 4): 5, 4. Sorted: 4, 5.
Reconstructed: 1, 4, 2, 5, 4.
Matches the manual trace diffs: 1, 4, 4, 5, 2?
Wait.
Manual trace: 1, 4, 4, 5, 2.
My reconstruction: 1, 4, 2, 5, 4.
Mismatch at index 3 and 5.
Manual: $d_3=4, d_5=2$.
Reconstructed: $d_3=2, d_5=4$.
Why?
Odds in manual trace: $d_1=1, d_3=4, d_5=2$.
Sorted odds: 1, 2, 4.
Placed at 1, 3, 5: $d_1=1, d_3=2, d_5=4$.
So reconstructed should be 1, 4, 2, 5, 4.
But manual trace gave 1, 4, 4, 5, 2.
Let's re-calculate manual trace diffs.
Sorted new: 0, 1, 5, 9, 14, 16.
$d_1 = 1-0=1$.
$d_2 = 5-1=4$.
$d_3 = 9-5=4$.
$d_4 = 14-9=5$.
$d_5 = 16-14=2$.
Diffs: 1, 4, 4, 5, 2.
Odds: $d_1=1, d_3=4, d_5=2$.
Evens: $d_2=4, d_4=5$.
Sorted Odds: 1, 2, 4.
Sorted Evens: 4, 5.
If we sort them, we get $d_1=1, d_3=2, d_5=4$ and $d_2=4, d_4=5$.
Resulting diffs: 1, 4, 2, 5, 4.
Sum of coords for this:
$x_1=1$.
$x_2=5$.
$x_3=7$.
$x_4=12$.
$x_5=16$.
$x_6=20$.
Sum = $1+5+7+12+16+20 = 61$.
But Sample 2 output is 41.
Original sum: $0+1+6+10+14+16 = 47$.
My manual trace sum: $0+1+5+9+14+16 = 45$.
The sample output 41 is lower.
So we can do more operations.
From 0, 1, 5, 9, 14, 16 (sum 45).
Diffs: 1, 4, 4, 5, 2.
Can we swap more?
Odds: 1, 4, 2. Evens: 4, 5.
We can swap $d_1, d_3$ (1 and 4) -> 4, 1.
Or $d_3, d_5$ (4 and 2) -> 2, 4.
We want to minimize $\sum (N-i+1) d_i$.
Coeffs: 6, 5, 4, 3, 2, 1 (for $x_1 \dots x_6$).
Wait, $x_k = \sum_{j=1}^k d_j$.
Sum = $\sum_{k=1}^6 x_k = \sum_{k=1}^6 \sum_{j=1}^k d_j = \sum_{j=1}^5 d_j (6-j+1) = 6d_1 + 5d_2 + 4d_3 + 3d_4 + 2d_5$.
Current: $1, 4, 4, 5, 2$.
Cost: $6(1) + 5(4) + 4(4) + 3(5) + 2(2) = 6 + 20 + 16 + 15 + 4 = 61$.
Wait, why did I get 45 earlier?
$x_1=0$?
Ah, the coordinates are absolute.
$x_1 = d_1$? No.
$x_1$ is the first coordinate.
If we change the diffs, does $x_1$ change?
In the operation, $x_i$ and $x_{i+3}$ are fixed.
In Sample 2, $x_1=0$ and $x_6=16$ are fixed because they are never part of the "middle" pair?
Actually, $x_1$ can be part of a middle pair if $i=0$? No $i \ge 1$.
So $x_1$ is never moved?
$i \ge 1$. The pieces involved are $i, i+1, i+2, i+3$.
$x_1$ is involved if $i=1$ (as the first piece). It is fixed.
$x_2$ is involved if $i=1$ (as second) or $i=2$ (as first).
If $i=1$, $x_2$ moves.
So $x_1$ is always fixed?
Yes, $x_1$ is only $x_i$ for $i=1$. It is never $x_{i+1}, x_{i+2}, x_{i+3}$ for $i \ge 1$.
So $x_1$ is constant.
Similarly $x_N$ is constant?
$x_N$ is $x_{i+3}$ for $i=N-3$. It is fixed.
So $x_1$ and $x_N$ are fixed.
In Sample 2, $x_1=0, x_6=16$.
So the sum of diffs is $x_6 - x_1 = 16$.
My calculated sum of diffs was 16.
But the sum of coordinates depends on the prefix sums.
$x_1 = 0$.
$x_2 = x_1 + d_1 = d_1$.
$x_3 = x_1 + d_1 + d_2$.
...
Sum = $N x_1 + \sum_{k=1}^{N-1} (N-k) d_k$.
For Sample 2: $N=6, x_1=0$.
Sum = $5d_1 + 4d_2 + 3d_3 + 2d_4 + 1d_5$.
Current diffs: 1, 4, 4, 5, 2.
Sum = $5(1) + 4(4) + 3(4) + 2(5) + 1(2) = 5 + 16 + 12 + 10 + 2 = 45$.
Matches manual trace.
Target: 41.
We need to reduce the cost.
Coeffs: 5, 4, 3, 2, 1.
Values: 1, 4, 4, 5, 2.
Odds (indices 1, 3, 5): 1, 4, 2.
Evens (indices 2, 4): 4, 5.
Sort Odds: 1, 2, 4.
Sort Evens: 4, 5.
Assign:
$d_1=1, d_3=2, d_5=4$.
$d_2=4, d_4=5$.
New diffs: 1, 4, 2, 5, 4.
Cost: $5(1) + 4(4) + 3(2) + 2(5) + 1(4) = 5 + 16 + 6 + 10 + 4 = 41$.
Matches Sample 2 output!

So the algorithm is confirmed:
1. Read N and X.
2. Compute diffs $d_1 \dots d_{N-1}$.
3. Separate into odds and evens.
4. Sort both.
5. Reconstruct diffs.
6. Compute sum using formula $\sum_{k=1}^{N-1} (N-k) d_k + N \cdot x_1$.
   Note: $x_1$ is the first element of input.