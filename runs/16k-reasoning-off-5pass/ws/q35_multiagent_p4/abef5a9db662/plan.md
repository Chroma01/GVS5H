The key observation is that the rating update rule is monotonic: if a starting rating X results in a final rating F(X), then for any X' > X, F(X') >= F(X). More importantly, the function F(X) - X (the total increase) is non-decreasing. However, a more direct approach leverages the fact that the "increase" function is piecewise constant or has simple structure. Actually, we can simulate the process for all possible ratings from 1 to 500000 efficiently using a difference array / sweep-line technique.

Let's define an array `inc` where `inc[r]` is 1 if rating `r` increases in a given contest, 0 otherwise. For each contest i with range [L_i, R_i], we add 1 to `inc[r]` for all r in [L_i, R_i]. We can compute the total increase for each rating r by processing all N contests. Using a difference array, we can compute the total increase for each rating r in O(N + MAX_R) time.

Let `total_increase[r]` be the total number of contests where rating r falls in [L_i, R_i]. Then the final rating for initial rating X is `X + total_increase[X]`.

Steps:
1. Read N and the N intervals.
2. Use a difference array to compute for each rating r (from 1 to 500000), how many intervals cover r.
3. For each query X, output X + total_increase[X].