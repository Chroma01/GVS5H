
## ideation
The core difficulty is efficiently answering $N$ queries where each query asks for the maximum GCD of a subset of size $K$ including a specific element $A_i$. A naive approach checking all subsets or pairs is $O(N^2)$ or worse, which is too slow given $N, A_i \le 1.2 \times 10^6$.

Key observations:
1. If a subset of size $K$ has GCD $g$, then all elements in that subset are multiples of $g$.
2. For a fixed $A_i$, the answer must be a divisor of $A_i$.
3. We need to find the largest divisor $g$ of $A_i$ such that there are at least $K$ multiples of $g$ in the entire array $A$.

Approach strategy:
1. **Frequency Count**: Count the occurrences of each number in $A$. Let `cnt[x]` be the number of times $x$ appears.
2. **Multiples Count**: For each possible GCD value $g$ (from $1$ to $\max(A)$), calculate how many numbers in $A$ are multiples of $g$. Let this be `total_multiples[g]`. This can be done using a sieve-like method in $O(M \log M)$ where $M = \max(A)$.
3. **Determine Answers**:
   - We need an array `ans` of size $N$ (or mapped by value) to store the result for each $A_i$.
   - Iterate $g$ from $\max(A)$ down to $1$.
   - If `total_multiples[g] >= K`, then $g$ is a candidate GCD. Any $A_i$ that is a multiple of $g$ can potentially have $g$ as its answer.
   - Since we want the *maximum* $g$, if we process $g$ in descending order, the first time we encounter a valid $g$ for a specific $A_i$, that is the answer for $A_i$.
   - To avoid re-scanning multiples for every $g$, we can maintain an array `best[g]` which stores the maximum valid GCD found so far for multiples of $g$. However, a more direct way is:
     - Create an array `res` of size $M+1$ initialized to 0.
     - Iterate $g$ from $M$ down to $1$.
     - If `total_multiples[g] >= K`:
       - For every multiple $j = g, 2g, 3g, \dots \le M$:
         - If `res[j]` is not yet set (or strictly speaking, we just want to ensure we pick the largest), we set `res[j] = g`.
         - Wait, simply setting `res[j] = g` might overwrite a larger $g'$ if we aren't careful with the order. But since we iterate $g$ downwards, the first time we see a valid $g$ for a multiple $j$, it is the largest possible valid GCD for $j$. So we only update if `res[j] == 0`.
4. **Final Output**: For each $A_i$, print `res[A_i]`.

Complexity:
- Counting frequencies: $O(N)$.
- Calculating `total_multiples`: $O(M \log M)$.
- Filling `res`: Sum of $M/g$ for $g=1..M$ is $O(M \log M)$.
- Total Time: $O(N + M \log M)$. With $N, M \approx 10^6$, this is roughly $2 \times 10^7$ operations, well within the time limit (usually 2 seconds for $\sim 10^8$ ops).
- Space: $O(N + M)$.

Pitfalls:
- 1-based vs 0-based indexing.
- Large I/O: Use fast I/O (`sys.stdin.read`, `sys.stdout.write`).
- Memory limits: Arrays of size $10^6$ integers are fine (a few MBs).
- The condition "include $A_i$" is naturally satisfied because we only consider $g$ if $A_i$ is a multiple of $g$ (i.e., $A_i \% g == 0$).

## worker: Implement the solution in Python using fast I/O, f
1.  **Algorithm Selection**: The problem asks for the maximum GCD of a subset of size $K$ including $A_i$. This implies $A_i$ must be a multiple of the GCD $g$, and there must be at least $K$ multiples of $g$ in the array $A$.
2.  **Frequency Counting**: First, we count the occurrences of each number in $A$ using an array `cnt`.
3.  **Sieve-like Multiples Count**: We compute `total_multiples[g]`, which stores how many numbers in $A$ are divisible by $g$. This is done by iterating $g$ from 1 to $\max(A)$ and summing `cnt` for all multiples of $g$. The complexity is $O(M \log M)$ where $M = \max(A)$.
4.  **Backward Iteration for Answers**: We iterate $g$ from $\max(A)$ down to 1. If `total_multiples[g] >= K`, then $g$ is a candidate for the maximum GCD. We then update the answer for all multiples of $g$ that haven't been assigned an answer yet. Since we iterate $g$ in descending order, the first time we assign a value to a multiple, it is guaranteed to be the largest possible valid GCD for that number. This step also takes $O(M \log M)$.
5.  **Complexity**: The overall time complexity is $O(N + M \log M)$, where $N$ is the length of the sequence and $M$ is the maximum value in the sequence. Given constraints $N, M \le 1.2 \times 10^6$, this fits well within typical time limits. Space complexity is $O(N + M)$.
6.  **Optimization**: Fast I/O is used to handle large input/output efficiently.

## worker: Run the code against the provided sample inputs to
The solution implements the $O(M \log M)$ approach where $M = \max(A)$.
1.  **Frequency Array**: Counts occurrences of each number in $A$.
2.  **Multiples Count**: Iterates $g$ from 1 to $M$ and sums counts of all multiples of $g$. This determines how many numbers in $A$ are divisible by $g$.
3.  **Greedy Assignment**: Iterates $g$ from $M$ down to 1. If the count of multiples of $g$ is $\ge K$, then $g$ is a candidate for the maximum GCD. We update `ans_map` for all multiples of $g$ that haven't been assigned a value yet. Since we iterate downwards, the first assignment is guaranteed to be the maximum possible GCD for that number.
4.  **Output**: Maps the precomputed answers back to the original sequence $A$.

This approach efficiently handles the constraints $N, A_i \le 1.2 \times 10^6$.

## worker: Run the provided sample inputs to verify correctne
The provided solution implements the $O(M \log M)$ algorithm where $M = \max(A)$.
1.  **Frequency Array**: Counts occurrences of each number in $A$.
2.  **Multiples Count**: Iterates $g$ from 1 to $M$ and sums counts of all multiples of $g$. This determines how many numbers in $A$ are divisible by $g$.
3.  **Greedy Assignment**: Iterates $g$ from $M$ down to 1. If the count of multiples of $g$ is $\ge K$, then $g$ is a candidate for the maximum GCD. We update `ans_map` for all multiples of $g$ that haven't been assigned a value yet. Since we iterate downwards, the first assignment is guaranteed to be the maximum possible GCD for that number.
4.  **Output**: Maps the precomputed answers back to the original sequence $A$.

This approach efficiently handles the constraints $N, A_i \le 1.2 \times 10^6$. The logic correctly addresses the requirement to include $A_i$ in the subset because we only consider $g$ if $A_i$ is a multiple of $g$ (i.e., $A_i \% g == 0$), and we check if there are at least $K$ multiples of $g$ in total.

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the $O(M \log M)$ algorithm where $M = \max(A)$.
1.  **Frequency Array**: Counts occurrences of each number in $A$.
2.  **Multiples Count**: Iterates $g$ from 1 to $M$ and sums counts of all multiples of $g$. This determines how many numbers in $A$ are divisible by $g$.
3.  **Greedy Assignment**: Iterates $g$ from $M$ down to 1. If the count of multiples of $g$ is $\ge K$, then $g$ is a candidate for the maximum GCD. We update `ans_map` for all multiples of $g$ that haven't been assigned a value yet. Since we iterate downwards, the first assignment is guaranteed to be the maximum possible GCD for that number.
4.  **Output**: Maps the precomputed answers back to the original sequence $A$.

This approach efficiently handles the constraints $N, A_i \le 1.2 \times 10^6$. The logic correctly addresses the requirement to include $A_i$ in the subset because we only consider $g$ if $A_i$ is a multiple of $g$ (i.e., $A_i \% g == 0$), and we check if there are at least $K$ multiples of $g$ in total.

## worker: finalize
The solution implements an $O(M \log M)$ algorithm where $M = \max(A)$.
1.  **Frequency Array**: Counts occurrences of each number in $A$.
2.  **Multiples Count**: Iterates $g$ from 1 to $M$ and sums counts of all multiples of $g$. This determines how many numbers in $A$ are divisible by $g$.
3.  **Greedy Assignment**: Iterates $g$ from $M$ down to 1. If the count of multiples of $g$ is $\ge K$, then $g$ is a candidate for the maximum GCD. We update `ans_map` for all multiples of $g$ that haven't been assigned a value yet. Since we iterate downwards, the first assignment is guaranteed to be the maximum possible GCD for that number.
4.  **Output**: Maps the precomputed answers back to the original sequence $A$.

This approach efficiently handles the constraints $N, A_i \le 1.2 \times 10^6$. The logic correctly addresses the requirement to include $A_i$ in the subset because we only consider $g$ if $A_i$ is a multiple of $g$ (i.e., $A_i \% g == 0$), and we check if there are at least $K$ multiples of $g$ in total.
