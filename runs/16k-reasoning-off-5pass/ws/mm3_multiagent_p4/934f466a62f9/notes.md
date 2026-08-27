
## ideation
The problem is from AtCoder ABC400 (Patisserie). We need to select K disjoint pairs from N cakes, each with attributes (X,Y,Z), to maximize the sum of `max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)` over the pairs. N ≤ 10^5, so an O(N^2) solution is impossible.

The known solution for this problem involves trying all 6 permutations of the dimensions. For each permutation, sort the cakes lexicographically by the three dimensions (in the order of the permutation), all in descending order. Then consider the first 2K cakes. Among these, we try two pairing strategies:
1. Pair adjacent: (1,2), (3,4), ..., (2K-1,2K)
2. Pair extremes: (1, K+1), (2, K+2), ..., (K, 2K)

We compute the total price for each strategy and take the maximum over all 6 permutations and both strategies. This works because the optimal solution can be represented as one of these pairings in some sorted order. The reasoning is that the max function is convex, so the optimal non-crossing matching under some sorting will follow one of these simple patterns. The complexity is O(N log N) per test case due to sorting, and we only try constant number of permutations and pairings.

Edge cases: K=1, or when N=2K (all cakes used). Need to handle large values up to 1e9, so use 64-bit integers.

## worker: Implement the solution in Python: for each test ca
The solution implements the known approach for the "Patisserie" problem from AtCoder ABC400. For each of the 6 permutations of the three dimensions, we sort all cakes in descending order according to that permutation. We then consider only the top 2K cakes. Within this set, we evaluate two pairing strategies: adjacent pairing (1st with 2nd, 3rd with 4th, etc.) and extreme pairing (1st with (K+1)th, 2nd with (K+2)th, etc.). The maximum total price over all permutations and strategies is the answer. This runs in O(N log N) per test case due to sorting, and uses 64-bit integers automatically via Python's arbitrary precision.
