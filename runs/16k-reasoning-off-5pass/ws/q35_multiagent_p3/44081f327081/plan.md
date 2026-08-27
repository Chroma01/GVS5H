1. **Key Insight**: For each index $i$, we need to find the largest $g$ such that $A_i$ is divisible by $g$ and there are at least $K-1$ other elements in $A$ (excluding $A_i$ itself, or including if duplicates exist) that are also divisible by $g$. Since $A_i$ must be included, $g$ must divide $A_i$. So we only consider divisors of $A_i$.

2. **Precomputation**: For each possible GCD value $g$ from 1 to $10^6$, count how many elements in $A$ are divisible by $g$. Let this be `count[g]`.

3. **For each $A_i$**: Iterate over all divisors $d$ of $A_i$. For each divisor $d$, check if there are at least $K$ elements in $A$ divisible by $d$. However, we must ensure $A_i$ is one of them. Since $d$ divides $A_i$, $A_i$ is always counted in `count[d]`. So we just need `count[d] >= K`. The answer for $A_i$ is the maximum such $d$.

4. **Efficiency**: 
   - Computing `count[g]` for all $g$: For each $A_j$, iterate over its divisors. But iterating divisors for each number can be slow if done naively. Instead, we can use a sieve-like approach: for each $g$ from 1 to $10^6$, count multiples of $g$ present in $A$. This is $O(M \log M)$ where $M = 10^6$.
   - For each $A_i$, finding all divisors: We can precompute divisors for all numbers up to $10^6$, or iterate divisors on the fly. Since we need the maximum divisor $d$ of $A_i$ with `count[d] >= K`, we can iterate divisors of $A_i$ and track the max.

5. **Optimization**: Precompute `count[g]` for all $g \in [1, 10^6]$ using a frequency array and sieve. Then for each $A_i$, find all divisors, check the condition, and take the max.