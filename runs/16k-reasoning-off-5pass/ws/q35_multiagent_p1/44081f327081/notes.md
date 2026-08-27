
## ideation
The core difficulty is efficiently determining, for each element A_i, the largest GCD `g` such that there are at least K elements in the array that are multiples of `g` (including A_i itself).

Key observations:
1. If we want to check if GCD `g` is achievable for A_i, we need:
   - A_i must be a multiple of g
   - There must be at least K elements in A that are multiples of g

2. We can iterate `g` from max_value (10^6) down to 1. For each `g`, we count how many elements in A are multiples of `g`. If the count >= K, then all indices i where A_i is a multiple of g can potentially have answer g. Since we iterate from large to small, the first `g` that satisfies the condition for a given A_i will be the maximum possible GCD for that A_i.

3. Efficient approach:
   - Precompute frequency of each value in A
   - For each candidate g, count multiples by summing frequencies of g, 2g, 3g, ...
   - If count >= K, then for each A_i that is a multiple of g and hasn't been answered yet, set answer[i] = g

4. To avoid checking all multiples for each g (which could be O(N log N) or worse), we can:
   - First compute for each g, the total count of multiples in A
   - Then iterate g from max down to 1
   - For each g with count >= K, iterate through all indices i where A_i is a multiple of g, and if answer[i] is not set, set it to g

5. The challenge is efficiently finding all indices i where A_i is a multiple of g. We can precompute this by:
   - For each value v present in A, find all divisors of v
   - For each divisor d of v, add the index i to a list for d
   - This way, for each g, we have a list of indices where A_i is a multiple of g

6. However, storing all these lists might use too much memory. Alternative: for each g, we can iterate through multiples of g and check if they exist in A, but we need the actual indices.

7. Better approach: 
   - Create an array `count[g]` = number of elements in A that are multiples of g
   - Create an array `ans[i]` initialized to 0
   - For each g from max down to 1:
     - If `count[g] >= K`:
       - For each index i where A_i is a multiple of g and ans[i] == 0:
         - Set ans[i] = g

8. To efficiently get indices for each g, we can precompute `multiples[g]` = list of indices i where A_i % g == 0. This can be done by iterating each A_i and adding i to all divisors of A_i.

9. Memory consideration: N up to 1.2 * 10^6, A_i up to 10^6. The total number of divisor additions across all A_i could be large, but on average each number has O(log A_i) divisors, so it should be manageable.

## worker: (None)
The solution works as follows:

1. **Frequency counting**: We first count the frequency of each value in A and store indices for each value.

2. **Count multiples**: For each candidate GCD `g` from 1 to 10^6, we count how many elements in A are multiples of `g`. This is done by summing `freq[multiple]` for all multiples of `g`.

3. **Greedy assignment from largest to smallest**: We iterate `g` from 10^6 down to 1. For each `g` where `count[g] >= K`, we know that any element which is a multiple of `g` can be part of a subset of size K with GCD divisible by `g`. Since we're iterating from largest to smallest, the first `g` that satisfies the condition for a given `A[i]` is the maximum possible GCD for that element.

4. **Efficient index lookup**: For each valid `g`, we iterate through all multiples of `g` and for each multiple `v`, we look up all indices where `A[i] == v`. If `ans[i]` hasn't been set yet, we set it to `g`.

The time complexity is O(M log M + N * d(A_i)) where M = 10^6 and d(A_i) is the number of divisors, but we're using the multiple iteration approach which gives O(M log M) for counting and O(sum of divisors) for the assignment phase. In practice, this is efficient enough given the constraints.
