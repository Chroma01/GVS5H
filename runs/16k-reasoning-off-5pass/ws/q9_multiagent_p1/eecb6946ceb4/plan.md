The problem asks us to count triplets $(A, B, C)$ from a given set $S$ such that $B-A = C-B$, which implies $A + C = 2B$. Since the order in the triplet definition requires $A < B < C$, we can sort the input array $S$ first. After sorting, for every element $B$ at index $i$, we need to count pairs of indices $(j, k)$ such that $j < i < k$ and $S[j] + S[k] = 2 \cdot S[i]$. Given the constraints $N \le 10^6$ and $S_i \le 10^6$, an $O(N^2)$ approach is too slow. We can iterate through each potential middle element $B$ and use a frequency map (or a boolean array since values are bounded) to count how many $A$'s exist such that $C = 2B - A$ also exists in the set with index greater than $B$. However, a more efficient approach for sorted arrays is to iterate through the array and for each $B$, count valid $A$'s to its left and check if the corresponding $C$ exists to its right. Alternatively, we can iterate through all pairs $(A, C)$ and check if their average exists, but that is $O(N^2)$. The best approach given the small value range of $S_i$ ($10^6$) is to use a frequency array. We can iterate through each $B$ in the sorted array. For a fixed $B$, we need to find pairs $(A, C)$ such that $A+C=2B$. Since we need $A < B < C$, we can iterate $A$ from the start up to $B$ (or rather, iterate through all possible $A$ values present in the set less than $B$) and check if $2B-A$ exists in the set and is greater than $B$. To optimize, we can precompute the frequency of each number. Then for each $B$, we iterate through all possible differences $d$ such that $A = B-d$. If $A$ exists and $C = B+d$ exists, we add the count. But iterating $d$ is slow.
Actually, a simpler $O(N \log N)$ or $O(N + \max(S))$ approach: Sort $S$. For each $i$ from $1$ to $N-2$, let $B = S[i]$. We need to count pairs $(j, k)$ with $j < i < k$ such that $S[j] + S[k] = 2S[i]$. This is equivalent to finding pairs summing to $2S[i]$ where one is smaller and one is larger. We can use two pointers for each $i$, but that's $O(N^2)$ worst case.
Wait, the constraints on $S_i$ are small ($10^6$). We can use a frequency array `cnt`.
Algorithm:
1. Read input, sort $S$.
2. Create a frequency map (or array) of elements in $S$.
3. Iterate through each element $B$ in $S$.
4. For each $B$, we want to count pairs $(A, C)$ such that $A+C=2B$, $A < B < C$.
5. Since $S$ is sorted, we can iterate $A$ through elements smaller than $B$. For each $A$, calculate $C = 2B - A$. If $C$ exists in our frequency map and $C > B$, increment the answer.
6. To make step 5 efficient: Instead of iterating all $A$, we can iterate through the sorted array. For a fixed $B$, we can use two pointers on the subarray to the left and right? No, that's still potentially slow if many duplicates or specific structures, but here elements are distinct.
Actually, since elements are distinct and $N$ is up to $10^6$, we cannot iterate all pairs.
Let's reconsider the constraints. $S_i \le 10^6$.
We can iterate through every possible value $x$ from $1$ to $10^6$. If $x$ is in $S$, it can be $A$. If $2x$ is in $S$, it can be $B$. If $3x$ is in $S$, it can be $C$. No, that's specific to arithmetic progression starting at $x$.
Correct approach:
Iterate $B$ through $S$.
We need to count pairs $(A, C)$ in $S$ such that $A+C=2B$ and $A < B < C$.
Since $S$ is sorted, for a fixed $B$, we can iterate $A$ from the beginning of the array up to $B$. But this is $O(N^2)$.
Is there a faster way?
Yes. Iterate $B$ from index $1$ to $N-2$.
We need to count $j < i$ and $k > i$ such that $S[j] + S[k] = 2 S[i]$.
This looks like a variation of the 3SUM problem, but we are counting triplets with a specific property.
Wait, if we just iterate $B$, and for each $B$, we iterate $A$ (where $A < B$), and check if $C = 2B - A$ exists.
Since the values are up to $10^6$, we can use a boolean array `exists` for $O(1)$ lookup.
The loop over $A$ is the bottleneck.
However, note that $A$ and $C$ are symmetric around $B$.
Maybe we can iterate over all pairs $(A, C)$? No, $O(N^2)$.
Is it possible the number of valid $A$'s for a given $B$ is small? Not necessarily.
Let's re-read constraints. $N \le 10^6$, $S_i \le 10^6$.
If $N$ is large, many $S_i$ will be dense.
Actually, the standard solution for this specific problem (often found in competitive programming libraries like AtCoder Library or similar) when $S_i$ is small is:
Iterate $B$ from $1$ to $10^6$. If $B \in S$:
  Iterate $A$ from $1$ to $B-1$. If $A \in S$ and $(2B-A) \in S$ and $(2B-A) > B$, count++.
This is still $O(\max(S)^2)$ in worst case.
Wait, maybe the intended solution is $O(N \log N)$ using FFT? No, that's for sums.
Let's look at the structure again. $A, B, C$ are in arithmetic progression.
If we sort $S$, we can iterate $i$ (index of $B$). Then we need to count pairs $(j, k)$ with $j < i < k$ and $S[j] + S[k] = 2 S[i]$.
This is exactly the problem of counting 3-term arithmetic progressions in a set.
For general sets, this is hard ($O(N^2)$). But with $S_i \le 10^6$, maybe we can do better?
Actually, there is a known optimization.
We can iterate over the common difference $d$.
For a fixed $d$, we look for $A, B=A+d, C=A+2d$ in $S$.
We can iterate $d$ from $1$ to $10^6/2$. For each $d$, we iterate $A$ such that $A, A+d, A+2d \le 10^6$.
If $A \in S$ and $A+d \in S$ and $A+2d \in S$, we count it.
The complexity would be $\sum_{d=1}^{M/2} (M/2d) \approx M \log M$.
Here $M = 10^6$. $M \log M \approx 2 \cdot 10^7$, which is well within the time limit (usually 2 seconds, allowing $\sim 10^8$ ops).
So the plan is:
1. Read input, store in a boolean array `present` of size $10^6+1$.
2. Iterate $d$ from $1$ to $500,000$.
3. Iterate $A$ starting from $1$ up to $10^6 - 2d$.
4. If `present[A]` and `present[A+d]` and `present[A+2d]`, increment count.
5. Print count.