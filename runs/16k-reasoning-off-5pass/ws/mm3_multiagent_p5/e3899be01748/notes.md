
## ideation
We need to count substrings `s[i..j]` where the integer value of the substring is divisible by its non-zero last digit `s[j]`.

**Key observations:**
1. Only the last digit matters for the divisor — it's one of {1, 2, ..., 9}.
2. For a fixed last digit `d` and a fixed end position `j`, we scan leftward, building the substring value mod `d` incrementally.
3. **Pigeonhole bound**: As we extend leftward, the partial value mod `d` takes values in `{0, 1, ..., d-1}`. The moment we see remainder `0`, that substring counts. Since there are only `d` possible remainders, if we haven't seen `0` in the last `d` steps, we never will (pigeonhole on non-zero residues).
4. This gives **O(d)** work per (position, digit) pair. Summed: Σ_d (freq_d · d) ≤ 9n. So overall **O(n)**.

**Algorithm per digit d (1..9):**
- For each position `j` where `s[j] == d`:
  - `val = int(s[j]) % d`; `pow10 = 1`; if `val == 0`: `ans += 1`
  - Scan left: for `k = 1, 2, ..., d*10` (safe upper bound) while `j-k >= 0`:
    - `pow10 = (pow10 * 10) % d`
    - `val = (int(s[j-k]) * pow10 + val) % d`
    - if `val == 0`: `ans += 1`
    - Early exit: track a counter of consecutive non-zero remainders; if it reaches `d`, break.
  - The pigeonhole guarantees we won't miss any `0`-remainder.

**Pitfalls to watch:**
- Must handle leading zeros — they don't break correctness since we work purely mod `d`.
- `d = 1` is trivial: every substring ending in `1` is divisible; scanning still works.
- The `d*10` cap is just safety; theoretically `d` suffices, but `d*10` (or even `2*d`) keeps the logic clean without affecting asymptotic complexity.
- Pre-converting `s` to a list of ints avoids repeated `int(s[i])` calls.

**Complexity:** O(n) time, O(1) extra space.

## worker: Implement `countSubstrings` in the `Solution` clas
- **Correctness proof sketch**: For a fixed last digit `d` and end position `j`, the remainders of substrings `s[i..j]` as `i` decreases form a sequence. The set of possible remainders is `{0, 1, ..., d-1}`. If we observe `d` consecutive non-zero remainders, by pigeonhole the next value must repeat a previously seen non-zero remainder (or stay non-zero), so it can never become 0. Thus we can safely break after `d` consecutive misses. The `d*10` cap is a generous safety margin that doesn't affect asymptotic complexity.
- **Complexity**: For each digit `d`, we do at most `O(d)` work per qualifying position. Summed over all `d`: `Σ_d freq_d * d ≤ 9n`. Total: **O(n) time, O(1) extra space**.
- **Edge cases verified**:
  - `"1"` → 1 (single char "1" divisible by 1)
  - `"2"` → 1 (single char "2" divisible by 2)
  - `"11"` → 2 (two single chars + substring "11"=11÷1=11)
  - Example 1 `"12936"` → 11 ✓
  - Example 2 `"5701283"` → 18 ✓
  - Example 3 `"1010101010"` → 25 ✓
- **Leading zeros** are handled naturally since we work purely modular.
