
## ideation
The core difficulty lies in efficiently determining, for each element $A_i$, the largest divisor $d$ of $A_i$ such that there are at least $K$ elements in the entire array $A$ divisible by $d$. 

Key observations:
1. Since $A_i$ must be included in the chosen subset, the GCD $g$ must divide $A_i$.
2. For a candidate GCD $g$ to be valid for $A_i$, we need at least $K$ elements in $A$ that are divisible by $g$. Since $g$ divides $A_i$, $A_i$ itself is one of those elements. So we just need `count[g] >= K`, where `count[g]` is the number of elements in $A$ divisible by $g$.
3. The answer for $A_i$ is the maximum divisor $d$ of $A_i$ such that `count[d] >= K`.

Algorithm plan:
1. Read input $N, K$ and array $A$.
2. Compute a frequency array `freq` where `freq[x]` is the number of times $x$ appears in $A$.
3. Compute `count[g]` for all $g$ from 1 to $M = 10^6$ (max value in $A$). This can be done efficiently using a sieve-like method: for each $g$ from 1 to $M$, sum up `freq[j]` for all multiples $j$ of $g$. This takes $O(M \log M)$ time.
4. For each $A_i$, find all its divisors. For each divisor $d$, check if `count[d] >= K`. The answer is the maximum such $d$.
   - To efficiently find divisors for each $A_i$, we can precompute divisors for all numbers up to $M$, or compute them on the fly. Given $N$ up to $1.2 \times 10^6$ and $M$ up to $10^6$, precomputing divisors might use too much memory. Instead, we can iterate over possible divisors by checking numbers up to $\sqrt{A_i}$, but that could be slow if done naively for each $A_i$.
   - Alternative: Since we want the maximum divisor $d$ of $A_i$ with `count[d] >= K`, we can iterate $d$ from $A_i$ down to 1, but that's too slow.
   - Better: Precompute for each number $x$ from 1 to $M$, the largest divisor $d$ of $x$ such that `count[d] >= K`. Let's call this `ans[x]`. Then the answer for $A_i$ is `ans[A_i]`.
   - To compute `ans[x]` for all $x$: For each $g$ from $M$ down to 1, if `count[g] >= K`, then for all multiples $x$ of $g$, if `ans[x]` is not yet set, set `ans[x] = g`. But this is still complex.
   - Simpler: For each $A_i$, find all divisors. The number of divisors for a number up to $10^6$ is small (at most 240 for highly composite numbers, but typically much less). So for each $A_i$, we can find all divisors, check the condition, and take the max. Finding divisors for each $A_i$ can be done in $O(\sqrt{A_i})$ time, which is acceptable since $\sqrt{10^6} = 1000$, and $N \le 1.2 \times 10^6$, so total time $O(N \sqrt{M}) \approx 1.2 \times 10^9$ operations, which might be too slow in Python.
   - Optimization: Precompute divisors for all numbers up to $M$ using a sieve. This uses $O(M \log M)$ time and space, which is feasible for $M = 10^6$.

Let's refine:
1. Compute `count[g]` for all $g \in [1, M]$ using sieve.
2. Precompute divisors for all numbers up to $M$: `divisors[x]` = list of divisors of $x$.
3. For each $A_i$, iterate over `divisors[A_i]`, find the maximum $d$ such that `count[d] >= K`.

Pitfalls:
- Memory usage for precomputing divisors for all numbers up to $10^6$ might be high. The total number of divisors for all numbers up to $M$ is $O(M \log M)$, which for $M=10^6$ is about $1.4 \times 10^7$ integers, which is manageable in Python if done carefully.
- Time limit: Precomputing divisors and counts should be efficient enough.

## worker: [todo] **Task 1**: Read input, compute frequency o
The solution works as follows:
1. **Frequency Array**: We first compute the frequency of each number in the input array $A$.
2. **Count Array**: Using a sieve-like approach, we compute `count[g]` for all $g$ from 1 to $MAX\_VAL$. `count[g]` represents the number of elements in $A$ that are divisible by $g$. This is done by iterating over each $g$ and summing up the frequencies of all its multiples. This step runs in $O(M \log M)$ time where $M = MAX\_VAL$.
3. **Answer Array**: We compute `ans[x]` for all $x$ from 1 to $MAX\_VAL$. `ans[x]` is the largest divisor $d$ of $x$ such that `count[d] >= K`. We iterate $g$ from $MAX\_VAL$ down to 1. For each $g$ with `count[g] >= K`, we set `ans[x] = g` for all multiples $x$ of $g$ that haven't been assigned a value yet. This ensures that for each $x$, `ans[x]` is the largest valid divisor. This step also runs in $O(M \log M)$ time.
4. **Output**: For each element $A_i$ in the input array, we output `ans[A_i]`.

This approach efficiently handles the constraints with $N$ up to $1.2 \times 10^6$ and $A_i$ up to $10^6$.
