We model each character independently: changing `caption[i]` to a target letter `c` costs `|caption[i] - c|`.  
The target string must consist of maximal blocks of the same character, each of length at least 3.  
We use DP with state `(i, c, k)` where `k` is the length of the current run capped at 3 (1, 2, ≥3).  
Forward DP stores the minimal cost to reach each state; backward DP stores the minimal cost to finish from each state.  
The optimal total cost is the minimum forward cost at the last position with `k=3`.  
To get the lexicographically smallest optimal string we reconstruct greedily left‑to‑right, always picking the smallest character that can still achieve the optimal total cost while respecting the run‑length constraints.