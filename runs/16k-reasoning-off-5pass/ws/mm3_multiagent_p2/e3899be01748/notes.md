
## ideation
We need to count substrings of a digit string `s` that are divisible by their **non‑zero last digit**.  
The last non‑zero digit of a substring is the rightmost non‑zero character in that substring.  
For a fixed end position `j`, let `p` be the index of the nearest non‑zero digit ≤ `j` (or `-1` if none).  
All valid starts `i` must satisfy `0 ≤ i ≤ p`; the last non‑zero digit is then `d = int(s[p])`.

The divisor `d` can only be 1…9.  
We treat each `d` separately:

* **d = 1, 2, 5** – any integer ending with `0` or `d` is automatically divisible.  
  Hence all `p+1` starts are valid.
* **d = 4** – divisibility depends only on the last two digits.  
  - If `s[j] == '0'` or `'4'` and the tens digit (if it exists) is even, then every start `i ≤ p` works.  
  - If `s[j] == '4'` and the tens digit is odd, only the single‑character substring (`i = j`) is valid.
* **d = 8** – divisibility depends on the last three digits.  
  We split starts into three groups:  
  - `i ≤ j‑2` (length ≥ 3): valid iff the three‑digit suffix `s[j‑2..j]` is divisible by 8.  
  - `i = j‑1` (length 2): valid iff `s[j‑1..j]` is divisible by 8 (and `p = j‑1`).  
  - `i = j` (length 1): always valid when `s[j] == '8'`.
* **d = 3, 7, 9** – 10 is invertible modulo `d`.  
  Let `pref[k]` be the value of `s[0..k‑1]` modulo `d`.  
  Define `tp[k] = pref[k] * inv10^k mod d`.  
  Then substring `s[i..j]` is divisible by `d` iff `tp[i] == tp[j+1]`.  
  We need to count `i ∈ [0, p]` with this equality.  
  Because `p` is non‑decreasing as `j` grows, we can slide a window:  
  keep a frequency array `cnt[0..d‑1]` of `tp` values for indices up to the current `p`.  
  For each `j`, after ensuring all indices `≤ p` are inserted, add `cnt[tp[j+1]]` to the answer.
* **d = 6** – a number ending with `0` or `6` is always even, so divisibility by 6 ⇔ divisibility by 3.  
  Thus we use the same `d = 3` method (only modulo 3) but only for positions where the last non‑zero digit is 6.

The overall complexity is O(n · 9) = O(n) (constant 9·n) and O(n) memory.

## worker: Implement the `Solution` class with the algorithm 
We implemented the algorithm described in the plan. We precomputed `last_nz` to get the nearest non‑zero digit to the left for each position. For each position `j` we determined the divisor `d` from that non‑zero digit.  

- For `d ∈ {1,2,5}` we added `p+1` because divisibility is automatic.  
- For `d = 4` we examined the last two digits: if the tens digit is even, all starts are valid; otherwise only the single‑digit substring (when `s[j]='4'`) counts.  
- For `d = 8` we split the starts into three groups (length ≥ 3, length 2, length 1) and checked the corresponding suffix modulo 8.  
- For `d ∈ {3,6,7,9}` we used a sliding window. Because `p` (the index of the last non‑zero digit) is non‑decreasing, we can maintain frequency arrays of transformed prefixes (or just the modulo‑3 value for `d=3` and `d=6`). We added to the answer the number of earlier indices with the same key that are ≤ `p`.  

The code is O(n) time and O(n) memory (the prefix arrays). It correctly handles the three examples.  

The solution passes the given examples.
