We need to find the K-th largest value among N^3 expressions A_i·B_j + B_j·C_k + C_k·A_i.  
Since K ≤ 5e5 we can’t generate all triples, but we can use **binary search on the answer** combined with a **counting routine** that, for a candidate X, counts how many triples give a value ≥ X.  
Counting is done in two stages:
1. For each pair (i,j), compute the minimum required C_k so that the expression ≥ X, then count C values ≥ that threshold using sorted C. This takes O(N^2 log N), but N ≤ 2e5 ⇒ O(N^2) is too large.  
2. Instead, we iterate over B_j in decreasing order (sorted B descending) and for each B_j we consider the best (largest) A_i’s using a max-heap. We stop when we have examined enough A_i to potentially affect the top K triples. Because K is only up to 5e5, we only need to consider at most K pairs (i,j) – we can break early once the current smallest contribution among the kept best (i,j) pairs is already too small to ever reach the threshold.  
3. For each kept pair (i,j) we binary‑search in C to count how many C_k make the expression ≥ X.  
4. The count gives us the number of triples with value ≥ X; we binary‑search for the smallest X such that this count < K, then the answer is the previous X.

The algorithm is O((K + N) log N · log V) which fits easily.