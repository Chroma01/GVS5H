We need to count substrings s[i..j] where the numeric value of the substring modulo its last digit (non-zero) equals zero. Length up to 1e5 requires O(n) or O(n log n) per digit.

For each possible last digit d (1..9), we process substrings ending at positions where s[pos] == d. Let the substring be from i to pos. Its value mod d must be 0.

We can iterate i from pos down to 0, building the number mod d incrementally: val = (val * 10 + int(s[i])) % d. Stop early if val == 0 and count it. However, worst-case O(n^2) per d.

Key insight: We only need to check substrings where the value mod d is 0. As we extend leftward, the number of distinct remainders is at most d-1 (since 0 is a "stop" but we can have at most d-1 non-zero residues before we must have seen 0, due to pigeonhole on the sequence of partial values). So for each ending position, we scan left at most d steps, giving O(n * sum(1/d)) = O(n log n) overall.

Implementation: For each digit d from 1 to 9, iterate pos from 0 to n-1. If s[pos] != d, skip. Otherwise, build remainders leftward: val = 0, count = 0. For i from pos down to max(0, pos - 1000) (or up to d*10): val = (int(s[i]) * pow10 + val) % d where pow10 = 10^(pos-i) mod d. Precompute pow10 mod d on the fly. If val == 0: increment answer and break (we've found the leftmost i giving remainder 0; all longer substrings won't have remainder 0 again until we see 0, so we break).

Wait - we need to count ALL substrings ending at pos with last digit d that are divisible. If we break at first val==0 going left, we miss substrings that start further left. E.g., "12" with d=2: scanning from pos=1 leftward: i=1 -> val=2%2=0 (substring "2"). Continue? i=0 -> val=(1*10+2)%2 = 0 (substring "12"). Both valid.

We shouldn't break; we should count every i where val==0, and continue scanning up to d steps (since after d steps without val==0, by pigeonhole no further will be 0). So: scan up to min(pos+1, d*2) or just d*10 steps. Actually the bound is d-1 non-zero residues possible, so at most d iterations. Set limit = min(pos+1, d*10) to be safe. For each i, update val; if val==0, ans++. After d iterations without val==0, break.

Total work: each pos with digit d does O(d) work. Sum over all d of (count of pos with digit d * d) <= n * max_d = 9n. So O(n) per digit d means O(9n) = O(n). Wait that's O(n) total! Let me reconsider: for each d we iterate all n positions but only do O(d) work at the d-positions. So total = sum_d (freq_d * d) <= 9n. That's linear!

Simpler: just for d in 1..9, for each pos where s[pos]==d, scan left up to d*10 (or just d*10) steps, count val==0 occurrences. 

To compute value mod d efficiently: val_new = (digit * 10^len + val_old) % d. Precompute powers of 10 mod d, or update incrementally: keep pow10 = 1, then val = (digit * pow10 + val) % d, then pow10 = (pow10 * 10) % d. But careful with order: when scanning from pos leftward to pos-k, the new digit is s[pos-k] and it's added as the most significant digit. So if current value represents s[i..pos], adding s[i-1] on left: new_val = (s[i-1] * 10^(pos-i+1) + current_val) % d. So track pow10 = 10^(length) % d.

Algorithm for fixed d, fixed pos:
- pow10 = 1  (represents 10^0 for current substring of length 1, just s[pos])
- val = int(s[pos]) % d
- if val == 0: ans += 1
- For k = 1, 2, ..., while pos-k >= 0 and k < some_limit (e.g., d*10 or just min(d*10, pos+1)):
    - pow10 = (pow10 * 10) % d
    - val = (int(s[pos-k]) * pow10 + val) % d
    - if val == 0: ans += 1
  After d steps without finding 0, break (pigeonhole).
  
Limit: d*10 is safe upper bound. Actually d suffices theoretically, but use d*10 for safety.