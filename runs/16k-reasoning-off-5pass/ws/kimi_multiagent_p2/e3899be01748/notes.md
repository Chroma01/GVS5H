
## ideation
The core difficulty is counting substrings s[i..j] with value mod d == 0 where d = s[j] (the last digit), in better than O(n²) time for n up to 1e5. Key observations:
- d ∈ {1..9} only (d = 0 never qualifies), so the state space of remainders is tiny (at most 9 per divisor).
- For a fixed end j, substring value mod d = sum of digit_k * 10^{j-k} mod d, which depends on j, so plain prefix-mod hashing fails except when 10 ≡ 1 (mod d) (i.e., d ∈ {1,3,9}).
- The clean trick: maintain, for each divisor d, a small array cnt[d][r] = number of active start positions i such that s[i..j] mod d == r. Advancing j by one with digit c transforms every remainder r → (r*10 + c) % d, which is just an O(d) rebuild of the array (≤ 9 ops). Add the new length-1 substring (start = j) with remainder c % d. Then if s[j] == d ≠ '0', add cnt[d][0] to the answer.
- Total cost: 9 divisors × ≤9 remainders × n steps = O(81n), well within limits.
- Pitfalls: (1) substrings ending in '0' never count — skip adding for d=0, but the digit 0 still participates in extending other substrings (leading zeros allowed, and '0' as an interior/starting digit is fine, e.g. "01" counts). (2) The new single-digit substring must be added to cnt before querying, so single non-zero digits count themselves. (3) Answer can be ~n(n+1)/2 ≈ 5e9, fits in Python int anyway. (4) The remainder transform is not bijective for d sharing factors with 10 (2,4,5,6,8), but that doesn't matter since we rebuild the full array each step.
- Sanity checks: "12936" → 11; "5701283" → 18; "1010101010" → 25 (only endings at '1' count; there are 25 substrings ending at a '1').

## worker: Implement and verify the complete solution: write 
- **Algorithm**: For each divisor `d ∈ 1..9`, maintain `cnt[d][r]` = number of substrings ending at the current position with value ≡ r (mod d). Advancing one character with digit `v` transforms every remainder `r → (r*10 + v) % d`; since `d ≤ 9`, rebuilding the table costs at most `9×9 = 81` operations per character → **O(81n) time, O(81) space**.
- The new length-1 substring is added to the table *before* querying, so single non-zero digits count themselves.
- Substrings ending in `'0'` never qualify (division by zero), but the digit `0` still extends other substrings (leading zeros allowed, e.g. `"01"` counts).
- The transform isn't bijective for `d` sharing factors with 10 (2,4,5,6,8), but that's irrelevant since we rebuild the full array each step.
- **Verification** (traced/tested):
  - `"12936"` → 11 ✓ (total 15 substrings minus "29","129","293","2936")
  - `"5701283"` → 18 ✓
  - `"1010101010"` → 25 ✓ (only substrings ending at '1'; counts 1+2+3+4+5+... wait, endings at positions of '1': 1+2+3+4+5+... = 1+2+3+4+5+... actually 5 ones at indices 0,2,4,6,8 give 1+3+5+7+9 = 25 ✓)
  - `"0"` → 0 ✓, `"7"` → 1 ✓, `"000"` → 0 ✓
  - `"99999"` (all nines, length n): every substring of identical digit 9 is divisible by 9 only if digit-sum divisible by 9 — for "9"*k, value = 10^k - 1 ≡ 0 (mod 9) always, so answer = n(n+1)/2 ✓ (e.g. n=5 → 15).
- Answer magnitude up to ~5×10⁹ fits Python int natively.
