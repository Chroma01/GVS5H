The problem asks for the largest possible value `t` such that we can pick a subset of foods with total calories ≤ X and the total amount of each vitamin (1, 2, 3) is at least `t`.  
Because each food provides exactly one vitamin, the three vitamins are independent – a food for vitamin 1 never contributes to vitamin 2 or 3.  
Hence, for a fixed `t` we can compute, for each vitamin separately, the minimum calories needed to obtain at least `t` units of that vitamin (a classic 0/1 knapsack).  
If the sum of those three minimal calorie requirements does not exceed `X`, then `t` is achievable; otherwise it is not.  
We binary‑search the maximum feasible `t`.  
The knapsack DP is performed over the calorie dimension (0…X), which is at most 5000, giving `O(N·X)` time and `O(X)` memory per vitamin.