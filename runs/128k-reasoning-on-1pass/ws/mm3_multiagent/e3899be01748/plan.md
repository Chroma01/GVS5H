The problem asks for the number of substrings whose numeric value is divisible by its non‑zero last digit.  
For a substring ending at position `r` with last digit `d = s[r]` (non‑zero), the condition is  

```
pref[r+1] ≡ pref[l] * 10^{L} (mod d)   where L = r-l+1
```

`pref[i]` is the integer value of the prefix `s[0..i-1]`.  
Since `d ≤ 9`, the residues of `10^{L} (mod d)` repeat with a very small period (period ≤ 6, with a short preperiod of length ≤ 9).  

For each digit `d` we maintain a small number of buckets (≤ 15) representing the possible offsets `r-l`.  
Each bucket stores, for the current `r`, how many prefixes `pref[l]` have a given remainder modulo `d`.  
When `r` increases, all offsets shift by one, which is simulated by rotating the buckets and then inserting the new prefix.

For each `r` we only need to examine the digit `d = s[r]` (if non‑zero).  
For each bucket we know the factor `10^{L} mod d`.  
If the factor is `0` we add the whole bucket when `cur == 0`.  
Otherwise we iterate over the at most `d` remainders and add the matching counts.

The whole process runs in `O(n)` time (≈ 200 operations per character) and `O(1)` extra memory.