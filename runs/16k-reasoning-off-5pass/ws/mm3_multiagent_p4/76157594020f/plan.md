We need the minimum possible maximum run length after at most `numOps` flips.  
Binary‑search the answer `L` (1 … n). For a given `L`, we can greedily check if it's possible to ensure every run of equal characters has length ≤ L.  
Greedy check: for each position, if the current run of equal chars (matching `s[i-1]`) reaches length `L`, we must flip `s[i]` to break it (costing 1 op). This locally optimal greedy works because flipping earlier positions never reduces later costs.  
If the total flips needed ≤ numOps, then `L` is feasible. The overall answer is the smallest feasible `L`.