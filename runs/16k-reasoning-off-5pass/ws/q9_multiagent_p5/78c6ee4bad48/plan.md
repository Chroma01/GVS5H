The operation allows us to take four consecutive pieces (in sorted order) at indices $i, i+1, i+2, i+3$ and transform their coordinates $x_i, x_{i+1}, x_{i+2}, x_{i+3}$ into $x_i, 2M-x_{i+1}, 2M-x_{i+2}, x_{i+3}$ where $M = (x_i + x_{i+3})/2$. This transformation preserves the sum of the four coordinates because $(2M-x_{i+1}) + (2M-x_{i+2}) = 4M - (x_{i+1}+x_{i+2}) = 2(x_i+x_{i+3}) - (x_{i+1}+x_{i+2})$, so the new sum is $x_i + x_{i+3} + 2(x_i+x_{i+3}) - (x_{i+1}+x_{i+2}) = 3(x_i+x_{i+3}) - (x_{i+1}+x_{i+2})$. Wait, let's re-calculate the sum change.
Original sum of 4: $S = x_i + x_{i+1} + x_{i+2} + x_{i+3}$.
New sum of 4: $S' = x_i + (2M - x_{i+1}) + (2M - x_{i+2}) + x_{i+3} = x_i + x_{i+3} + 4M - (x_{i+1} + x_{i+2})$.
Since $2M = x_i + x_{i+3}$, then $4M = 2(x_i + x_{i+3})$.
$S' = x_i + x_{i+3} + 2(x_i + x_{i+3}) - (x_{i+1} + x_{i+2}) = 3(x_i + x_{i+3}) - (x_{i+1} + x_{i+2})$.
The change in sum is $\Delta = S' - S = 2(x_i + x_{i+3}) - 2(x_{i+1} + x_{i+2}) = 2[(x_i + x_{i+3}) - (x_{i+1} + x_{i+2})]$.
To minimize the total sum, we want to perform operations where $(x_i + x_{i+3}) < (x_{i+1} + x_{i+2})$, reducing the sum by $2[(x_{i+1} + x_{i+2}) - (x_i + x_{i+3})]$.
This looks like we can greedily reduce the sum as long as there exists a window of 4 where the outer sum is less than the inner sum. However, the order matters and the values change.
Actually, this problem is equivalent to finding the minimum sum achievable. It turns out that we can always sort the final configuration such that the pieces are "compressed" towards the left as much as possible.
Let's reconsider the invariant or the final state.
Notice that the operation on $x_i, x_{i+1}, x_{i+2}, x_{i+3}$ effectively swaps the relative order of the middle two with respect to the outer two in a specific way, but more importantly, it allows us to reduce the sum if the "inner" pair is "heavier" than the "outer" pair.
Actually, there is a known result for this specific problem (AtCoder ABC 234 Problem D? No, this is likely a different contest). Let's trace the logic carefully.
The operation is: $x_{i+1} \leftarrow x_i + x_{i+3} - x_{i+1}$ and $x_{i+2} \leftarrow x_i + x_{i+3} - x_{i+2}$.
Sum change: $\Delta = 2(x_i + x_{i+3} - x_{i+1} - x_{i+2})$.
We want to make $\Delta$ negative.
Consider the sequence of differences $d_i = x_{i+1} - x_i$.
The operation changes the differences.
However, a simpler observation is often that we can perform operations until the sequence becomes "convex" or satisfies some property.
But wait, the sample 1: 1, 5, 7, 10. $x_1+x_4 = 11$, $x_2+x_3 = 12$. $11 < 12$, so we can reduce.
New values: $x_1=1, x_4=10$. $M=5.5$.
$x_2' = 5.5 + (5.5-5) = 6$.
$x_3' = 5.5 - (7-5.5) = 4$.
New set: 1, 4, 6, 10. Sorted: 1, 4, 6, 10. Sum = 21.
Original sum = 23. Reduction = 2.
Formula check: $2(11 - 12) = -2$. Correct.
Can we do more? Now $x_1+x_4 = 11$, $x_2+x_3 = 10$. $11 > 10$. No reduction possible with $i=1$.
So the minimum is 21.

Is it possible that we can always reach a state where $x_i + x_{i+3} \ge x_{i+1} + x_{i+2}$ for all $i$?
If so, the minimum sum is the sum of the initial array minus the maximum possible reduction.
But the operations change the values, so the condition might become true later or false later.
Actually, this problem is equivalent to: we can reorder the elements? No, the relative order of $i$ and $i+3$ is fixed, and $i+1, i+2$ are swapped in terms of their relation to $M$, but they remain between $i$ and $i+3$.
Wait, in the example: 1, 5, 7, 10 -> 1, 4, 6, 10. The set of values changed.
Key Insight: The operation preserves the sum of the 4 elements if $x_i+x_{i+3} = x_{i+1}+x_{i+2}$. If not, it changes.
Actually, there is a simpler invariant. Consider the sum of all elements.
Let's look at the constraints and the nature of the operation.
This problem is actually **ABC 234 D** is not it. This is **ABC 234 E**? No.
This is **AtCoder Grand Contest 038 A**? No.
It is **AtCoder Beginner Contest 234 Problem D**? No.
Let's search for the problem statement pattern. "N pieces placed on a number line... midpoint between i and i+3... move i+1 and i+2".
This is **AtCoder Beginner Contest 314 Problem D**? No.
It is **AtCoder Beginner Contest 234 Problem C**? No.
Ah, this is **AtCoder Beginner Contest 234 Problem D** is "AtCoder Express 3".
Wait, the problem is **AtCoder Beginner Contest 234 Problem D** is not it.
Let's re-read carefully.
The operation is defined on indices $i, i+1, i+2, i+3$.
This is **AtCoder Beginner Contest 234 Problem D** is definitely not it.
Maybe it's **ABC 234 Problem D** is "AtCoder Express 3".
Okay, let's ignore the contest number and solve it.
The operation allows us to decrease the sum if $x_i + x_{i+3} < x_{i+1} + x_{i+2}$.
Is it possible to reach a state where we cannot decrease the sum anymore? Yes, when $x_i + x_{i+3} \ge x_{i+1} + x_{i+2}$ for all valid $i$.
Does the order of operations matter?
Suppose we have 1, 10, 11, 20. $1+20=21, 10+11=21$. No change.
Suppose 1, 2, 10, 11. $1+11=12, 2+10=12$. No change.
Suppose 1, 5, 6, 10. $1+10=11, 5+6=11$. No change.
Suppose 1, 2, 3, 10. $1+10=11, 2+3=5$. $11 > 5$. No reduction.
Wait, if $x_i + x_{i+3} > x_{i+1} + x_{i+2}$, the sum increases. We want to minimize, so we only apply if sum decreases.
Can we get stuck in a local minimum?
Actually, there is a known result for this specific problem (it appeared in **AtCoder Beginner Contest 234** as Problem **D**? No, Problem **D** is AtCoder Express 3. Problem **E**? No.
Wait, I found it. It is **AtCoder Beginner Contest 234 Problem D** is not it.
It is **AtCoder Beginner Contest 234 Problem D** is "AtCoder Express 3".
Maybe it is **ABC 234 Problem D** is not it.
Let's try to derive the solution.
The operation is linear.
$x_{i+1}' = x_i + x_{i+3} - x_{i+1}$
$x_{i+2}' = x_i + x_{i+3} - x_{i+2}$
Notice that $x_{i+1}' + x_{i+2}' = 2(x_i + x_{i+3}) - (x_{i+1} + x_{i+2})$.
Also $x_{i+1}' - x_{i+2}' = x_{i+2} - x_{i+1}$. The difference between the middle two is preserved (just sign flipped? No).
$x_{i+1}' - x_{i+2}' = (x_i + x_{i+3} - x_{i+1}) - (x_i + x_{i+3} - x_{i+2}) = x_{i+2} - x_{i+1}$.
So the difference $x_{i+2} - x_{i+1}$ is invariant!
Wait, if $x_{i+2} - x_{i+1}$ is invariant, then the relative order of $i+1$ and $i+2$ doesn't change their difference.
But their values change.
However, the difference between $x_{i+1}$ and $x_i$ changes.
Let's look at the differences $d_j = x_{j+1} - x_j$.
The operation affects $d_i, d_{i+1}, d_{i+2}$.
$d_i' = x_{i+1}' - x_i = x_i + x_{i+3} - x_{i+1} - x_i = x_{i+3} - x_{i+1} = d_{i+1} + d_{i+2}$.
$d_{i+1}' = x_{i+2}' - x_{i+1}' = x_{i+2} - x_{i+1} = d_{i+1}$. (Invariant!)
$d_{i+2}' = x_{i+3} - x_{i+2}' = x_{i+3} - (x_i + x_{i+3} - x_{i+2}) = x_{i+2} - x_i = d_i + d_{i+1}$.
So the differences transform as:
$d_i \to d_{i+1} + d_{i+2}$
$d_{i+1} \to d_{i+1}$
$d_{i+2} \to d_i + d_{i+1}$
And $d_{i+3}$ is unchanged.
We want to minimize the sum $\sum x_k$.
Note that $x_N = x_1 + \sum_{j=1}^{N-1} d_j$.
So minimizing $\sum x_k$ is equivalent to minimizing $\sum_{k=1}^N (N-k+1) d_k$? No.
$\sum_{k=1}^N x_k = \sum_{k=1}^N \sum_{j=1}^{k-1} d_j + N x_1$? No.
$x_k = x_1 + \sum_{j=1}^{k-1} d_j$.
Sum $= N x_1 + \sum_{k=1}^N \sum_{j=1}^{k-1} d_j = N x_1 + \sum_{j=1}^{N-1} (N-j) d_j$.
Since $x_1$ is invariant (it's never the $i+1$ or $i+2$ or $i+3$ in the first position? Wait, $i$ goes from $1$ to $N-3$. So $x_1$ is never moved?
If $i=1$, we move $x_2, x_3$. $x_1$ is $x_i$. It stays $x_i$.
If $i=2$, we move $x_3, x_4$. $x_1$ is untouched.
So $x_1$ is always invariant.
Thus, minimizing the sum is equivalent to minimizing $\sum_{j=1}^{N-1} (N-j) d_j$.
The transformation on differences:
$d_i, d_{i+1}, d_{i+2} \to d_{i+1}+d_{i+2}, d_{i+1}, d_i+d_{i+1}$.
This looks like we can shift the "weight" of the differences.
Actually, notice that the operation allows us to replace $(d_i, d_{i+2})$ with $(d_{i+1}+d_{i+2}, d_i+d_{i+1})$ while keeping $d_{i+1}$ same.
This looks like we can move the "mass" of the differences to the left or right?
Actually, the operation is reversible?
If we apply the operation again on the same $i$:
New $d_i' = d_{i+1} + d_{i+2}$.
New $d_{i+2}' = d_i + d_{i+1}$.
Apply again:
$d_i'' = d_{i+1}' + d_{i+2}' = d_{i+1} + (d_i + d_{i+1}) = d_i + 2d_{i+1}$.
This doesn't seem to revert immediately.
However, note that the sum of differences $\sum d_j$ is invariant?
Old sum: $d_i + d_{i+1} + d_{i+2}$.
New sum: $(d_{i+1}+d_{i+2}) + d_{i+1} + (d_i+d_{i+1}) = d_i + 3d_{i+1} + 2d_{i+2}$.
Not invariant.
Wait, let's re-evaluate the sum change.
$\Delta S = 2[(x_i+x_{i+3}) - (x_{i+1}+x_{i+2})] = 2[(d_i+d_{i+1}+d_{i+2}) - (d_{i+1}+d_{i+2})] = 2 d_i$?
$x_i + x_{i+3} = x_i + (x_i + d_i + d_{i+1} + d_{i+2}) = 2x_i + d_i + d_{i+1} + d_{i+2}$.
$x_{i+1} + x_{i+2} = (x_i + d_i) + (x_i + d_i + d_{i+1}) = 2x_i + 2d_i + d_{i+1}$.
Difference: $(2x_i + d_i + d_{i+1} + d_{i+2}) - (2x_i + 2d_i + d_{i+1}) = d_{i+2} - d_i$.
So $\Delta S = 2(d_{i+2} - d_i)$.
We want to minimize sum, so we want $d_{i+2} < d_i$.
If $d_i > d_{i+2}$, we can reduce the sum by $2(d_i - d_{i+2})$.
The operation transforms $d_i, d_{i+1}, d_{i+2}$ to $d_{i+1}+d_{i+2}, d_{i+1}, d_i+d_{i+1}$.
Let's check the new difference condition.
New $d_i' = d_{i+1} + d_{i+2}$.
New $d_{i+2}' = d_i + d_{i+1}$.
We want to check if we can continue reducing.
Actually, this looks like we can sort the differences?
Consider the sequence of differences $d_1, d_2, \dots, d_{N-1}$.
The operation at $i$ replaces $d_i, d_{i+2}$ with $d_{i+1}+d_{i+2}, d_i+d_{i+1}$? No.
It replaces $d_i \to d_{i+1}+d_{i+2}$ and $d_{i+2} \to d_i+d_{i+1}$.
And $d_{i+1}$ stays same.
This operation increases the sum of differences?
Old sum part: $d_i + d_{i+2}$.
New sum part: $d_{i+1}+d_{i+2} + d_i+d_{i+1} = d_i + d_{i+2} + 2d_{i+1}$.
So the sum of differences increases by $2d_{i+1}$.
But we only do this if $d_i > d_{i+2}$.
Wait, if $d_i > d_{i+2}$, then $d_{i+2} - d_i < 0$, so $\Delta S < 0$.
So we reduce the total coordinate sum.
Can we perform this until no such $i$ exists?
The condition for no reduction is $d_i \le d_{i+2}$ for all $i$.
This means the sequence of differences $d_1, d_2, \dots, d_{N-1}$ must satisfy $d_1 \le d_3 \le d_5 \le \dots$ and $d_2 \le d_4 \le d_6 \le \dots$.
Basically, the odd-indexed differences are non-decreasing, and the even-indexed differences are non-decreasing.
Is it possible to reach this state from any initial state?
The operation allows us to "mix" $d_i$ and $d_{i+2}$ using $d_{i+1}$.
Actually, notice that $d_i$ and $d_{i+2}$ are updated, but $d_{i+1}$ is not.
This suggests we can process the array from left to right or right to left.
Actually, there is a simpler invariant.
Consider the sum of differences with weights.
We want to minimize $\sum (N-j) d_j$.
The operation changes $d_i, d_{i+2}$ to $d_{i+1}+d_{i+2}, d_i+d_{i+1}$.
Change in objective function:
$\Delta Obj = (N-i)(d_{i+1}+d_{i+2} - d_i) + (N-(i+2))(d_i+d_{i+1} - d_{i+2})$.
$= (N-i)(d_{i+1}+d_{i+2}-d_i) + (N-i-2)(d_i+d_{i+1}-d_{i+2})$.
$= (N-i)(d_{i+1}+d_{i+2}-d_i) + (N-i-2)(d_i+d_{i+1}-d_{i+2})$.
Let $A = d_{i+1}+d_{i+2}-d_i$ and $B = d_i+d_{i+1}-d_{i+2}$.
Note $A+B = 2d_{i+1}$.
Also $A-B = 2d_{i+2} - 2d_i$.
$\Delta Obj = (N-i)A + (N-i-2)B = (N-i)(A+B) - 2B = (N-i)2d_{i+1} - 2(d_i+d_{i+1}-d_{i+2})$.
$= 2(N-i)d_{i+1} - 2d_i - 2d_{i+1} + 2d_{i+2} = 2[(N-i-1)d_{i+1} - d_i + d_{i+2}]$.
We want to minimize the objective, so we want $\Delta Obj < 0$.
This happens if $d_i - d_{i+2} > (N-i-1)d_{i+1}$.
Wait, this contradicts the simple condition $d_i > d_{i+2}$.
The condition for reducing the sum of coordinates was $d_i > d_{i+2}$.
The condition for reducing the weighted sum is different.
However, the problem asks to minimize the sum of coordinates.
The operation is valid if $d_i > d_{i+2}$.
If we keep applying operations where $d_i > d_{i+2}$, do we eventually reach a state where $d_i \le d_{i+2}$ for all $i$?
Yes, because the operation tends to equalize or sort the differences?
Actually, the operation $d_i \to d_{i+1}+d_{i+2}$ and $d_{i+2} \to d_i+d_{i+1}$ makes the new values larger than the old ones (assuming positive differences).
Since $X_i$ are increasing, $d_j > 0$.
So $d_i' = d_{i+1}+d_{i+2} > d_{i+2}$ (since $d_{i+1}>0$).
And $d_{i+2}' = d_i+d_{i+1} > d_i$.
So the new $d_i'$ is definitely greater than the old $d_{i+2}$.
And the new $d_{i+2}'$ is definitely greater than the old $d_i$.
So if we had $d_i > d_{i+2}$, after one operation:
$d_i' = d_{i+1}+d_{i+2}$.
$d_{i+2}' = d_i+d_{i+1}$.
Is it possible that $d_i' > d_{i+2}'$?
$d_{i+1}+d_{i+2} > d_i+d_{i+1} \iff d_{i+2} > d_i$.
But we started with $d_i > d_{i+2}$. So $d_i' < d_{i+2}'$.
So the inequality flips!
After one operation, we have $d_i' < d_{i+2}'$.
So we cannot apply the operation again on the same $i$.
Can we apply it on $i-1$ or $i+1$?
This suggests that we can perform a greedy strategy: whenever $d_i > d_{i+2}$, apply the operation.
But the order matters.
Actually, since the operation flips the inequality for the pair $(i, i+2)$, and increases the values, maybe we can just sort the differences?
Wait, the operation is only allowed on $i, i+1, i+2, i+3$.
The condition is $d_i > d_{i+2}$.
If we have a sequence of differences, we can swap the roles of $d_i$ and $d_{i+2}$ effectively?
Actually, notice that $d_i$ and $d_{i+2}$ are updated to $d_{i+1}+d_{i+2}$ and $d_i+d_{i+1}$.
This looks like we are adding $d_{i+1}$ to both.
But the relative order flips.
If we have $d_1, d_2, d_3, d_4, \dots$.
If $d_1 > d_3$, we update $d_1 \to d_2+d_3, d_3 \to d_1+d_2$. Now $d_1 < d_3$.
Can we then use $d_2$ and $d_4$?
This looks like we can propagate the "largeness" to the right?
Actually, the final state where $d_i \le d_{i+2}$ for all $i$ is the target.
In this state, the odd indices are non-decreasing and even indices are non-decreasing.
Is the final configuration unique?
Yes, because the operation is deterministic in terms of reducing the sum?
Actually, we can just simulate the process: while there exists $i$ such that $d_i > d_{i+2}$, apply the operation.
Since the values grow, will it terminate?
The sum of coordinates decreases. Since coordinates are integers? No, they can be half-integers.
But the sum decreases by $2(d_i - d_{i+2})$.
Since $d_i$ are derived from integers, they might be integers or half-integers?
Initial $X_i$ are integers. $d_i$ are integers.
Operation: $d_i' = d_{i+1}+d_{i+2}$ (integer).
So all $d_i$ remain integers.
The sum of coordinates decreases by an integer amount.
Since the sum is bounded below (by $N \times \min(X)$), it must terminate.
So the algorithm is:
1. Calculate initial differences $d_1, \dots, d_{N-1}$.
2. While there exists $i \in [1, N-3]$ such that $d_i > d_{i+2}$:
   Apply operation: $d_i \leftarrow d_{i+1} + d_{i+2}$, $d_{i+2} \leftarrow d_i + d_{i+1}$ (using old $d_i$).
   Wait, the update rule for $d$ was:
   $d_i' = d_{i+1} + d_{i+2}$
   $d_{i+1}' = d_{i+1}$
   $d_{i+2}' = d_i + d_{i+1}$
   So we update $d_i$ and $d_{i+2}$.
3. Compute the final sum.

However, $N$ is up to $2 \times 10^5$. A naive simulation might be too slow if we do many operations.
But notice that each operation makes $d_i$ and $d_{i+2}$ larger.
Also, the condition $d_i > d_{i+2}$ flips to $d_i < d_{i+2}$.
So we can't do it again on the same $i$.
Can we do it on $i+1$?
$d_{i+1}$ and $d_{i+3}$.
The operation at $i$ changes $d_{i+1}$? No, $d_{i+1}$ is unchanged.
So the condition at $i+1$ depends on $d_{i+1}$ and $d_{i+3}$.
Since $d_{i+1}$ is unchanged, and $d_{i+3}$ is unchanged, the condition at $i+1$ is unchanged.
What about $i-1$? Depends on $d_{i-1}$ and $d_{i+1}$. $d_{i+1}$ unchanged.
So the operation at $i$ only affects the condition at $i$ (which becomes false) and potentially $i-1$ and $i+1$?
Wait, $d_i$ changes. So condition at $i-1$ (involving $d_{i-1}$ and $d_{i+1}$) is unaffected?
Condition at $i-1$: $d_{i-1} > d_{i+1}$. Unaffected.
Condition at $i+1$: $d_{i+1} > d_{i+3}$. Unaffected.
Condition at $i$: $d_i > d_{i+2}$. Becomes false.
So each operation only resolves the conflict at $i$.
But wait, if we resolve $i$, does it create a new conflict?
No, because $d_i$ becomes larger than $d_{i+2}$? No, $d_i' < d_{i+2}'$.
So the conflict at $i$ is gone.
Are there other conflicts?
The values $d_i$ and $d_{i+2}$ increase.
Could this cause $d_{i-1} > d_{i+1}$ to become true? No, $d_{i+1}$ is unchanged.
Could it cause $d_{i+1} > d_{i+3}$ to become true? No.
So it seems we can just iterate from left to right?
If $d_i > d_{i+2}$, we fix it.
But wait, if we fix $i$, we change $d_i$ and $d_{i+2}$.
Does this affect $i+1$? No.
Does this affect $i-1$? No.
So the operations are independent?
Wait, if we have $d_1 > d_3$, we fix it.
Then we check $d_2 > d_4$.
If we fix $d_2 > d_4$, we change $d_2, d_4$.
Does this affect $d_1 > d_3$? No.
So we can just scan from $i=1$ to $N-3$.
If $d_i > d_{i+2}$, apply operation.
Then move to $i+1$.
Is it possible that fixing $i$ creates a problem for $i+1$?
No, because $d_{i+1}$ is unchanged.
So the strategy is simply:
Iterate $i$ from $1$ to $N-3$.
If $d_i > d_{i+2}$, update $d_i, d_{i+2}$.
Wait, if we update $d_i$, does it affect $d_{i-1}$?
Condition at $i-1$ is $d_{i-1} > d_{i+1}$. Unaffected.
So the order doesn't matter?
Let's trace Sample 1: 1, 5, 7, 10.
$d_1 = 4, d_2 = 2, d_3 = 3$.
$i=1$: $d_1=4, d_3=3$. $4 > 3$.
Update: $d_1 \leftarrow 2+3=5$, $d_3 \leftarrow 4+2=6$.
$d_2$ remains 2.
New diffs: 5, 2, 6.
Check $i=2$: $N=4$, so $i$ goes to $1$. Done.
Reconstruct $X$:
$x_1 = 1$.
$x_2 = 1+5=6$.
$x_3 = 6+2=8$.
$x_4 = 8+6=14$.
Sum = $1+6+8+14 = 29$.
But sample output is 21.
Where is the mistake?
Ah, the operation on $X$ changes the values.
My derivation of $d$ update was:
$d_i' = d_{i+1} + d_{i+2}$
$d_{i+2}' = d_i + d_{i+1}$
Let's re-verify with Sample 1.
Initial: 1, 5, 7, 10.
$d_1 = 4, d_2 = 2, d_3 = 3$.
Operation $i=1$:
$x_1=1, x_4=10, M=5.5$.
$x_2' = 6, x_3' = 4$.
New array: 1, 4, 6, 10.
New diffs:
$d_1' = 4-1=3$.
$d_2' = 6-4=2$.
$d_3' = 10-6=4$.
So new diffs are 3, 2, 4.
My formula gave $d_1' = 2+3=5$. Incorrect.
Let's re-derive the difference update.
$x_{i+1}' = x_i + x_{i+3} - x_{i+1}$.
$x_{i+2}' = x_i + x_{i+3} - x_{i+2}$.
$d_i' = x_{i+1}' - x_i = x_{i+3} - x_{i+1} = d_{i+1} + d_{i+2}$.
Wait, $x_{i+3} - x_{i+1} = (x_{i+1}+d_{i+1}+d_{i+2}) - x_{i+1} = d_{i+1}+d_{i+2}$.
So $d_i' = d_{i+1} + d_{i+2}$.
In Sample 1: $d_1' = d_2 + d_3 = 2+3=5$.
But actual $d_1' = 3$.
Why?
$x_1=1, x_2=5, x_3=7, x_4=10$.
$x_2' = 6, x_3' = 4$.
$d_1' = x_2' - x_1 = 6-1=5$.
Ah, in the sample explanation, the new array is 1, 4, 6, 10?
"2nd piece ... moves to 6. 3rd piece ... moves to 4."
So the pieces are at 1, 4, 6, 10?
Wait, the problem says "move each of the (i+1)-th and (i+2)-th pieces ... to positions symmetric to M".
The order of pieces is maintained by coordinate?
"all pieces always occupy distinct coordinates".
But the problem says "i-th and (i+3)-rd pieces in ascending order".
After the move, the pieces might change their rank?
"it can be proved that all pieces always occupy distinct coordinates".
But do they maintain the order $i, i+1, i+2, i+3$?
In Sample 1:
Original: 1 (1st), 5 (2nd), 7 (3rd), 10 (4th).
Move 2nd and 3rd.
2nd becomes 6. 3rd becomes 4.
New positions: 1, 4, 6, 10.
The piece that was 2nd is now at 6 (3rd rank).
The piece that was 3rd is now at 4 (2nd rank).
So the RANKS changed!
The operation is defined on the RANKS at the time of operation.
So after the operation, the piece at rank 2 is the one that was at rank 3?
Yes.
So the sequence of values changes, and the indices $i, i+1, i+2, i+3$ refer to the current sorted order.
This means my difference analysis based on fixed indices is wrong because the indices refer to sorted order, and the values swap ranks.
In Sample 1, after operation, the sorted order is 1, 4, 6, 10.
The values are $x_1=1, x_2=4, x_3=6, x_4=10$.
The sum is 21.
My previous calculation with fixed indices gave 29.
The key is that the operation swaps the middle two elements in terms of their values relative to the outer two?
Actually, $x_{i+1}' = 2M - x_{i+1}$ and $x_{i+2}' = 2M - x_{i+2}$.
Since $x_{i+1} < M < x_{i+2}$ (because $x_{i+1} < x_{i+2}$ and $M$ is midpoint of $x_i, x_{i+3}$? Not necessarily. $M = (x_i+x_{i+3})/2$. $x_{i+1}, x_{i+2}$ are between $x_i$ and $x_{i+3}$. So $x_i < x_{i+1} < x_{i+2} < x_{i+3}$.
Then $x_i < M < x_{i+3}$.
Is $x_{i+1} < M$? Not necessarily.
But $x_{i+1} < x_{i+2}$.
After reflection: $x_{i+1}' = 2M - x_{i+1}$. $x_{i+2}' = 2M - x_{i+2}$.
Since $x_{i+1} < x_{i+2}$, $x_{i+1}' > x_{i+2}'$.
So the two middle pieces swap their relative order!
So the new sorted order will have the piece that was $i+2$ at position $i+1$ and the piece that was $i+1$ at position $i+2$.
So the sequence of values effectively becomes $x_i, x_{i+2}', x_{i+1}', x_{i+3}$.
Wait, $x_{i+2}' < x_{i+1}'$.
So the new sorted sequence is $x_i, x_{i+2}', x_{i+1}', x_{i+3}$.
So the operation replaces $(x_{i+1}, x_{i+2})$ with $(x_{i+2}', x_{i+1}')$ where $x_{k}' = 2M - x_{k}$.
And since $x_{i+2}' < x_{i+1}'$, the new values at ranks $i+1, i+2$ are $x_{i+2}'$ and $x_{i+1}'$.
So the operation is:
$x_{i+1} \leftarrow 2M - x_{i+2}$
$x_{i+2} \leftarrow 2M - x_{i+1}$
Where $M = (x_i + x_{i+3})/2$.
This is equivalent to:
$x_{i+1} \leftarrow x_i + x_{i+3} - x_{i+2}$
$x_{i+2} \leftarrow x_i + x_{i+3} - x_{i+1}$
Notice that the sum $x_{i+1} + x_{i+2}$ becomes $(x_i+x_{i+3} - x_{i+2}) + (x_i+x_{i+3} - x_{i+1}) = 2(x_i+x_{i+3}) - (x_{i+1}+x_{i+2})$.
This is the same sum change as before.
And the new values are swapped in rank.
So the operation is: swap the middle two, and reflect them around the midpoint of the outer two.
This is equivalent to: $x_{i+1} \leftarrow x_i + x_{i+3} - x_{i+2}$, $x_{i+2} \leftarrow x_i + x_{i+3} - x_{i+1}$.
And since we want to minimize the sum, we do this whenever $x_{i+1} + x_{i+2} > x_i + x_{i+3}$.
Because then the new sum is smaller.
Can we do this repeatedly?
Yes, until $x_{i+1} + x_{i+2} \le x_i + x_{i+3}$ for all $i$.
This condition is $x_{i+1} + x_{i+2} \le x_i + x_{i+3}$.
Rearranging: $x_{i+3} - x_{i+2} \ge x_{i+1} - x_i$.
Or $d_{i+2} \ge d_i$.
So we want $d_i \le d_{i+2}$ for all $i$.
This is the same condition as before!
And the operation updates the values such that the new $d_i$ and $d_{i+2}$ satisfy the condition?
Let's check Sample 1 again with this logic.
Initial: 1, 5, 7, 10. $d_1=4, d_2=2, d_3=3$.
$i=1$: $d_1=4, d_3=3$. $4 > 3$. Condition violated.
Operation:
$x_2' = 1+10-7 = 4$.
$x_3' = 1+10-5 = 6$.
New array: 1, 4, 6, 10.
New diffs: $d_1=3, d_2=2, d_3=4$.
Now $d_1=3, d_3=4$. $3 \le 4$. Condition satisfied.
Sum = 21.
So the algorithm is:
While there exists $i$ such that $d_i > d_{i+2}$:
  Apply operation: $x_{i+1} \leftarrow x_i + x_{i+3} - x_{i+2}$, $x_{i+2} \leftarrow x_i + x_{i+3} - x_{i+1}$.
  (Note: this updates the values, which updates the diffs).
Since $N$ is large, we need an efficient way.
But notice that the operation only affects $x_{i+1}, x_{i+2}$.
And the condition $d_i > d_{i+2}$ is local.
Also, the operation makes $d_i$ and $d_{i+2}$ "swap" in a way that satisfies the condition?
In Sample 1: $d_1=4, d_3=3 \to d_1=3, d_3=4$.
It seems the operation simply swaps $d_i$ and $d_{i+2}$?
Let's check.
$d_i' = x_{i+1}' - x_i = (x_i+x_{i+3}-x_{i+2}) - x_i = x_{i+3}-x_{i+2} = d_{i+2}$.
$d_{i+2}' = x_{i+3} - x_{i+2}' = x_{i+3} - (x_i+x_{i+3}-x_{i+1}) = x_{i+1}-x_i = d_i$.
$d_{i+1}' = x_{i+2}' - x_{i+1}' = (x_i+x_{i+3}-x_{i+1}) - (x_i+x_{i+3}-x_{i+2}) = x_{i+2}-x_{i+1} = d_{i+1}$.
So the operation simply SWAPS $d_i$ and $d_{i+2}$!
And $d_{i+1}$ remains unchanged.
This is a huge simplification!
The operation is: if $d_i > d_{i+2}$, swap $d_i$ and $d_{i+2}$.
We want to reach a state where $d_i \le d_{i+2}$ for all $i$.
This means we want to sort the differences such that $d_1 \le d_3 \le d_5 \dots$ and $d_2 \le d_4 \le d_6 \dots$.
Since we can swap any $d_i, d_{i+2}$ if $d_i > d_{i+2}$, we can bubble sort the odd-indexed differences and even-indexed differences independently.
So the algorithm is:
1. Compute initial differences $d_1, \dots, d_{N-1}$.
2. Sort the subsequence $d_1, d_3, d_5, \dots$ in ascending order.
3. Sort the subsequence $d_2, d_4, d_6, \dots$ in ascending order.
4. Reconstruct the final array $X$ from the sorted differences.
5. Compute the sum.

Let's verify with Sample 1.
$d = [4, 2, 3]$.
Odd indices: $d_1=4, d_3=3$. Sorted: $3, 4$.
Even indices: $d_2=2$. Sorted: $2$.
New $d$: $3, 2, 4$.
Reconstruct:
$x_1 = 1$.
$x_2 = 1+3=4$.
$x_3 = 4+2=6$.
$x_4 = 6+4=10$.
Sum = 21. Correct.

Sample 2: 0, 1, 6, 10, 14, 16.
$d = [1, 5, 4, 4, 2]$.
Odd: $d_1=1, d_3=4, d_5=2$. Sorted: $1, 2, 4$.
Even: $d_2=5, d_4=4$. Sorted: $4, 5$.
New $d$: $1, 4, 2, 5, 4$.
Reconstruct:
$x_1 = 0$.
$x_2 = 0+1=1$.
$x_3 = 1+4=5$.
$x_4 = 5+2=7$.
$x_5 = 7+5=12$.
$x_6 = 12+4=16$.
Sum = $0+1+5+7+12+16 = 41$. Correct.

So the solution is:
1. Read N and X.
2. Compute differences $d_i = X_{i+1} - X_i$.
3. Separate $d$ into odds and evens.
4. Sort both lists.
5. Merge back into $d$.
6. Compute sum of $X$ using the new $d$.
   $X_1$ is unchanged.
   $X_k = X_1 + \sum_{j=1}^{k-1} d_j$.
   Sum $= N X_1 + \sum_{j=1}^{N-1} (N-j) d_j$.

Complexity: $O(N \log N)$ due to sorting. $N=2 \times 10^5$, feasible.