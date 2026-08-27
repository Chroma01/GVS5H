Compute the number of distinct integers in every prefix (`pref[i]`) and in every suffix (`suff[i]`) in O(N) using a boolean array.  
While sweeping the second split position `j` from left to right, maintain an array `V[i] = pref[i] + distinct(i+1…j)` for all `i < j`.  
When the new element `A[j]` is added to the middle subarray, `V[i]` increases by 1 exactly for those `i` with `i ≥ lastPos[A[j]]` (where `lastPos` is the previous occurrence of `A[j]`).  
Use a segment tree (or a lazy‑propagation tree) that supports range addition and range maximum query to keep the `V` values up‑to‑date and to obtain `max_{i<j} V[i]` in O(log N).  
For each `j` the candidate answer is `maxV + suff[j+1]`; the overall answer is the maximum over all `j`.