1. **Count parity buckets** – For a given `n`, compute the total number of odd (`O`) and even (`E`) integers in `[1…n]`.  
2. **Pre‑compute capped factorials** – Build `fact[i] = min(fact[i‑1]·i, INF)` for `i = 0…n` with `INF = 10¹⁸` (any value > 10¹⁵). This lets us safely compare counts with the large `k`.  
3. **Count completions** – For any remaining odds `or` and evens `er` and a required next parity (odd or even), an alternating continuation exists only when the counts match the forced pattern:  
   - If the next number must be odd, the odd positions count is `ceil(L/2)` and even positions `floor(L/2)` where `L = or + er`.  
   - If the next number must be even, the counts are swapped.  
   When the pattern matches, the number of completions is `fact[or]·fact[er]` (capped).  
4. **Lexicographic construction** – Iterate positions `0 … n‑1`. At each step consider the unused numbers in increasing order. A candidate is admissible only if its parity differs from the previous element (or it is the first element). For each admissible candidate compute the completion count as described. If `k` exceeds the count, subtract it and try the next candidate; otherwise fix the candidate, update the used‑parity counts, and move to the next position.  
5. **Edge handling** – If no candidate can be selected at any step, the required `k`‑th permutation does not exist; return an empty list.