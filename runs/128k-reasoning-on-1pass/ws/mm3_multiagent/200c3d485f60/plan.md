The condition “exactly k equal adjacencies” means the array can be split into `runs = n - k` maximal constant blocks.  
First decide which of the `n‑1` adjacency positions are equal: choose `k` positions → `C(n‑1, k)` ways.  
Then assign values to the runs: the first run can be any of the `m` values, and every later run must differ from the previous one → `m * (m‑1)^{runs‑1}` ways.  
The total count is the product of these two independent choices, taken modulo `10^9+7`.  
We compute the binomial coefficient with pre‑computed factorials and modular inverses, and the power with fast exponentiation; edge cases (`k` out of range, `m = 1`, `n = 1`) are automatically handled by the formula.