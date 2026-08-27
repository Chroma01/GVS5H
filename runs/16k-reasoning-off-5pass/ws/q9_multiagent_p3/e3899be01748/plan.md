The problem requires counting substrings divisible by their last non-zero digit. A brute-force approach checking all substrings would be O(N^2), which is too slow for N up to 10^5. Instead, we can iterate through each position `i` as the end of a substring and check backwards. However, a more efficient observation is that for a substring ending at `i` with last non-zero digit `d`, the substring is divisible by `d` if the number formed is divisible by `d`. Since we only care about the last non-zero digit, we can precompute the position of the last non-zero digit for every suffix or simply iterate backwards from each `i`. Actually, a simpler O(N) or O(N log N) approach exists: For each ending position `i`, let `d` be the last non-zero digit in `s[0...i]`. If `d` is 0, no substring ending at `i` is valid (since the divisor must be non-zero). If `d` is not 0, we need to count how many starting positions `j` (0 <= j <= i) make `int(s[j:i+1]) % d == 0`. This still seems hard to optimize directly for arbitrary digits. 

Wait, re-reading the constraints and examples: The divisor is the *last non-zero digit* of the substring. If the substring ends with '0', the last non-zero digit is some digit earlier in the substring. If the substring ends with a non-zero digit `d`, then the divisor is `d`.
Let's reconsider the structure.
For a fixed ending index `i`:
1. If `s[i]` is not '0', the divisor is `d = int(s[i])`. We need to count `j` such that `int(s[j:i+1]) % d == 0`.
2. If `s[i]` is '0', the divisor is the last non-zero digit in `s[j:i+1]`. This implies we need to look back to find the last non-zero digit.

Actually, the constraints and typical CP patterns suggest an O(N) solution. Let's analyze the divisibility condition.
If the substring ends with a non-zero digit `d`, we need `num % d == 0`.
If the substring ends with '0', say `...k0`, the divisor is `k` (the last non-zero digit). So we need `num % k == 0`.
This looks like we can iterate `i` from 0 to N-1. Maintain the current number modulo some values? No, the modulus changes.
Alternative approach: Iterate `i` from 0 to N-1. Let `last_nonzero` be the index of the last non-zero digit in `s[0...i]`. If no non-zero digit exists, count is 0.
Actually, let's look at the property again.
For a substring `s[j:i+1]`, let `k` be the last non-zero digit in this substring. We need `val % k == 0`.
If `s[i] != '0'`, then `k = s[i]`. We need `val % s[i] == 0`.
If `s[i] == '0'`, then `k` is the last non-zero digit before `i`.
This suggests we can group substrings by their last non-zero digit.
But maybe there's a simpler observation.
Consider the contribution of each digit as the "last non-zero digit".
For a digit `d` at index `i` to be the last non-zero digit of a substring `s[j:i+1]`, it must be that `s[k] == '0'` for all `k` in `i+1` to `end`? No, the substring ends at some `end >= i`.
Let's reverse the thinking. Fix the position `i` of the last non-zero digit in the substring. Let the substring be `s[j:i+1]` where `s[i]` is non-zero and `s[k]` can be anything for `k < i`? No, `s[i]` is the last non-zero digit, so `s[i+1...end]` must be all zeros? No, the substring is defined by start `j` and end `end`. The last non-zero digit in `s[j:end]` is at some index `p`. Then `s[p]` is non-zero, and `s[p+1...end]` are all zeros.
So, for a fixed `end` and a fixed `p` (where `p <= end` and `s[p]` is the last non-zero digit in `s[j:end]`), the condition is `int(s[j:end]) % s[p] == 0`.
Since `s[p+1...end]` are zeros, `int(s[j:end]) = int(s[j:p+1]) * 10^(end-p)`.
So we need `int(s[j:p+1]) * 10^(end-p) % s[p] == 0`.
Let `val = int(s[j:p+1])`. We need `val * 10^(end-p) % s[p] == 0`.
This must hold for all `j` such that `s[j...p]` has no non-zero digits after `p`? No, `p` is the *last* non-zero digit in `s[j:end]`. This means `s[j...p]` contains `s[p]` as non-zero, and `s[j...p-1]` can have zeros and non-zeros? No, if there was a non-zero after `p` in `s[j:end]`, then `p` wouldn't be the last. But `s[p+1...end]` are all zeros by definition of `p` being the last non-zero in `s[j:end]`.
Wait, if `s[j:end]` has last non-zero at `p`, then `s[p]` is non-zero, and `s[p+1...end]` are all zeros. The digits `s[j...p-1]` can be anything, but they must not contain any non-zero digit that is "after" `p`? No, `p` is the largest index in `j...end` with non-zero. So `s[p+1...end]` are zeros. `s[j...p-1]` can have non-zeros, but if they did, say at `q < p`, then `p` is still the last non-zero because `q < p`.
So for a fixed `end` and a fixed `p` (where `s[p]` is non-zero and `s[p+1...end]` are all zeros), we need to count `j` such that `int(s[j:end]) % s[p] == 0`.
Note that `int(s[j:end]) = int(s[j:p+1]) * 10^(end-p)`.
Let `mod = s[p]`. We need `int(s[j:p+1]) * 10^(end-p) % mod == 0`.
This condition depends on `end`. As `end` increases (adding zeros), `10^(end-p)` increases.
Since `mod` is a single digit (1-9), `10` and `mod` are coprime unless `mod` is 5.
If `mod` is not 5, `gcd(10, mod) = 1`. Then `10^(end-p)` is invertible modulo `mod`. So `int(s[j:p+1]) % mod == 0`.
If `mod` is 5, `gcd(10, 5) = 5`. Then `10^(end-p)` is divisible by 5.
Case 1: `s[p]` is not 5.
Condition: `int(s[j:p+1]) % s[p] == 0`.
This condition is independent of `end` (as long as `s[p+1...end]` are zeros).
Case 2: `s[p]` is 5.
Condition: `int(s[j:p+1]) * 10^(end-p) % 5 == 0`.
Since `10^(end-p)` is always divisible by 5 for `end > p`, the condition is always true for `end > p`.
For `end = p`, `10^0 = 1`, so we need `int(s[j:p+1]) % 5 == 0`.

Algorithm:
1. Identify all positions `p` where `s[p]` is non-zero.
2. For each `p`, determine the range of `end` such that `s[p+1...end]` are all zeros. Let this range be `end` from `p` to `next_nonzero_index - 1`.
3. For each such `end`, count valid `j`.
   - If `s[p] != 5`: Count `j` in `[0, p]` such that `int(s[j:p+1]) % s[p] == 0`. This count is constant for all valid `end`. Multiply by the number of valid `end`s.
   - If `s[p] == 5`:
     - For `end = p`: Count `j` such that `int(s[j:p+1]) % 5 == 0`.
     - For `end > p`: All `j` in `[0, p]` are valid (since `10^k` is divisible by 5). So add `(p + 1)` for each `end > p`.

We can precompute the counts for each `p` and `mod`.
Actually, we can iterate `p` from right to left or left to right.
Let's refine the "valid `end`" part.
For a fixed `p`, the valid `end`s are `p, p+1, ..., q-1` where `q` is the next index with non-zero digit (or `n`).
Number of such `end`s is `q - p`.
For `end = p`, we check divisibility.
For `end > p`, if `s[p] != 5`, condition is same as `end=p`. If `s[p] == 5`, condition is always true.

So the plan:
1. Find next non-zero index for each position.
2. Iterate `p` from 0 to n-1. If `s[p] == '0'`, skip.
3. Let `mod = int(s[p])`.
4. Find `q` = next non-zero index after `p`. If none, `q = n`.
5. Count `j` in `0..p` such that `int(s[j:p+1]) % mod == 0`. Let this be `cnt`.
6. If `mod != 5`:
   - Total for this `p` = `cnt * (q - p)`.
7. If `mod == 5`:
   - For `end = p`: add `cnt`.
   - For `end` in `p+1..q-1`: add `(p + 1)` for each.
   - Total = `cnt + (q - p - 1) * (p + 1)`.

To efficiently compute `cnt` for each `p`:
We need `int(s[j:p+1]) % mod == 0`.
This is equivalent to `(prefix_val[p] - prefix_val[j-1]) * inv(10^(p-j)) % mod == 0`? No, standard prefix sums don't work for division.
However, `mod` is small (1-9). We can maintain counts of remainders.
Iterate `p` from 0 to n-1.
Maintain an array `rem_counts` of size 10, where `rem_counts[r]` is the number of `j <= p` such that `int(s[j:p+1]) % mod == r`.
Wait, `mod` changes with `p`. So we can't maintain one global array.
But `mod` is just `s[p]`. When we move from `p` to `p+1`, the `mod` changes.
We can recompute `cnt` for the current `p` in O(p) time? That would be O(N^2).
We need O(1) or O(log N) per `p`.
Observation: `int(s[j:p+1]) = int(s[j:p]) * 10 + s[p]`.
Let `val_j_p = int(s[j:p])`. Then `val_j_p_new = val_j_p * 10 + s[p]`.
We need `val_j_p_new % s[p] == 0`.
This depends on `s[p]`.
Since `s[p]` is small, maybe we can maintain the counts of remainders for the current `s[p]`?
No, `s[p]` varies.
Alternative: Precompute for each digit `d` in 1..9, the positions `j` where `int(s[j:p+1]) % d == 0`?
Actually, we can iterate `p` and update the remainder counts for the current `mod`.
But `mod` changes every step.
Wait, we only need `cnt` for the specific `mod = s[p]`.
Can we compute `cnt` faster?
`int(s[j:p+1]) % d == 0` <=> `int(s[j:p+1])` is a multiple of `d`.
Since `d` is small, we can maintain for each `d` in 1..9, the count of `j` such that `int(s[j:p+1]) % d == 0`.
Let `counts[d][r]` be the number of `j` such that `int(s[j:p+1]) % d == r`.
When moving from `p` to `p+1`:
For each `d` in 1..9:
  New value `v' = v * 10 + s[p+1]`.
  `r' = (r * 10 + s[p+1]) % d`.
  Update `counts[d]` by shifting remainders.
This is O(9) per step, so O(N).
Total complexity O(N).

Steps:
1. Initialize `counts` array of size 10x10 (d from 1 to 9, r from 0 to 9). `counts[d][r]` stores count of substrings ending at current `p` with remainder `r` modulo `d`.
   Actually, we need `counts[d][0]` which is the number of `j` such that `int(s[j:p+1]) % d == 0`.
2. Precompute `next_nonzero` array.
3. Iterate `p` from 0 to n-1:
   - Update `counts` for all `d` in 1..9.
     - For each `d`, new remainder `r' = (r * 10 + int(s[p])) % d`.
     - Shift counts.
   - Let `mod = int(s[p])`.
   - If `mod == 0`, continue (cannot be last non-zero).
   - Find `q` = next non-zero after `p`.
   - `cnt = counts[mod][0]`.
   - If `mod != 5`: add `cnt * (q - p)`.
   - If `mod == 5`: add `cnt + (q - p - 1) * (p + 1)`.

Corner case: `p+1` to `q-1` might be empty if `q = p+1`. Then `q-p-1 = 0`. Correct.

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # Precompute next non-zero index
        next_nonzero = [n] * n
        last = n
        for i in range(n - 1, -1, -1):
            if s[i] != '0':
                last = i
            next_nonzero[i] = last
        
        # counts[d][r] = number of substrings ending at current position with remainder r modulo d
        # d ranges from 1 to 9
        counts = [[0] * 10 for _ in range(10)]
        
        total = 0
        for p in range(n):
            digit = int(s[p])
            
            # Update counts for all d in 1..9
            # We need to shift remainders: new_r = (old_r * 10 + digit) % d
            # But we must do this carefully. We can create a new state or update in place if careful.
            # Since we need old values to compute new, use a copy or temporary array.
            # Actually, for a fixed d, we can update in place if we iterate? No, dependency on old r.
            # Better: create new_counts for current step.
            
            # Optimization: only need to update for d where we might need it later? 
            # We need counts for all d because any future p might have s[p] as any digit 1-9.
            
            # Let's update counts for d=1..9
            for d in range(1, 10):
                new_counts = [0] * 10
                for r in range(10):
                    if counts[d][r] > 0:
                        new_r = (r * 10 + digit) % d
                        new_counts[new_r] += counts[d][r]
                counts[d] = new_counts
            
            if digit == 0:
                continue
            
            mod = digit
            q = next_nonzero[p]
            cnt = counts[mod][0]
            
            if mod != 5:
                total += cnt * (q - p)
            else:
                # For end = p: cnt
                # For end > p: (q - p - 1) * (p + 1)
                total += cnt + (q - p - 1) * (p + 1)
                
        return total
```

Double check logic for `mod == 5`.
If `s[p] == 5`, then for `end = p`, we need `int(s[j:p+1]) % 5 == 0`. Count is `cnt`.
For `end > p` (up to `q-1`), the substring is `s[j:p+1]` followed by zeros.
Value = `int(s[j:p+1]) * 10^k`.
Since `k >= 1`, `10^k` is divisible by 5. So value is divisible by 5 regardless of `int(s[j:p+1])`.
So all `j` in `0..p` are valid. Count is `p+1`.
Number of such `end`s is `q - p - 1`.
Total for `mod=5` is `cnt + (q - p - 1) * (p + 1)`.
Correct.

Wait, what if `q = p + 1`? Then `q - p - 1 = 0`. Correct.
What if `q = p`? Impossible since `s[p]` is non-zero, so `next_nonzero[p] > p`.

One detail: `counts` initialization. Before loop, `counts` should represent empty prefix?
Actually, the loop starts with `p=0`.
Before processing `p=0`, there are no substrings ending at `p-1`.
So `counts` should be all zeros initially.
Inside loop, we update `counts` to reflect substrings ending at `p`.
The update logic: `new_r = (r * 10 + digit) % d`.
If `counts` was all zeros, after update, `counts[d][digit % d] = 1` (for the substring `s[0:p+1]`? No).
Wait, `counts[d][r]` stores number of `j` such that `int(s[j:p+1]) % d == r`.
For `p=0`:
`digit = s[0]`.
`counts` initially all 0.
Update: `new_r = (0 * 10 + digit) % d = digit % d`.
`counts[d][digit % d] = 1`.
This corresponds to `j=0`. Correct.
Then we use `counts[mod][0]`. If `digit % mod == 0`, then `cnt=1`. Correct.

Seems solid.