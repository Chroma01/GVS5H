
## ideation
Core difficulty: counting substrings divisible by their last digit efficiently for n up to 1e5. The last digit d ∈ {1..9} is small, which is the key exploitable constraint. A naive per-ending backward scan is O(n²) worst case (e.g., all '9's), too slow.

Key observations:
- Substrings ending in '0' never qualify (division by zero / non-zero last digit required).
- Single non-zero digit substrings always qualify (covered naturally by the remainder counting).
- For a fixed divisor d, as we extend the string by one character x, every active suffix remainder r transforms to (r*10 + x) mod d, and a new suffix (just x) appears. Since remainders mod d number at most d ≤ 9, we can maintain a frequency array of size d and remap it in O(d) per character.
- Doing this independently for each d ∈ 1..9 gives O(n · Σd) = O(45n) ≈ 4.5e6 operations — fine.
- At each position j with digit d = int(s[j]), if d ≥ 1, add cnt_d[0] (number of suffixes ending at j with remainder 0 mod d) to the answer.

Pitfalls:
- Don't forget substrings ending in '0' contribute nothing (but '0' still extends suffixes for other divisors' passes — actually each d-pass processes all characters regardless).
- Leading zeros are allowed, so no special handling needed.
- Answer can be up to ~n(n+1)/2 ≈ 5e9, so use 64-bit (Python int is fine).
- Alternative approach: for each j, backward scan with early termination — risky worst case; the 9-pass remainder-remap method is safest.
- Another alternative: per d, two-pointer/prefix-hash with powers of 10 mod d — messy because substring value mod d = (P[j] - P[i-1]*10^{j-i+1}) mod d requires tracking length-dependent scaling; the suffix-remap avoids this.

## worker: Implement the solution: single pass over s, mainta
- **Algorithm**: For each divisor d ∈ 1..9, maintain a frequency array `cnt[d]` of size d counting remainders of all suffixes of the current prefix. When a new digit x arrives, every suffix value transforms as `v → (v*10 + x) mod d`, so we remap the array in O(d), then add the new single-digit suffix. If x ≠ 0, all suffixes with remainder 0 mod x are exactly the substrings ending at this position divisible by their last digit x, so add `cnt[x][0]` to the answer. Substrings ending in '0' never qualify (last digit must be non-zero).
- **Correctness check on examples**:
  - "12936" → 11 ✓ (verified by brute force: 15 total substrings, 4 fail).
  - "5701283" → 18 ✓.
  - "1010101010" → 25 ✓ (only substrings ending in '1' count: positions 1,3,5,7,9 contribute 1+2+3+4+5... wait, ending at index j (0-based) with digit '1' gives j+1 substrings: indices 0,2,4,6,8 → 1+3+5+7+9 = 25 ✓).
- **Edge cases**: single character "5" → 1; "0" → 0; all zeros "000" → 0; leading zeros handled naturally since substring values are computed numerically.
- **Complexity**: Time O(n · Σ_{d=1..9} d) = O(45n) ≈ 4.5·10⁶ operations for n = 10⁵ — well within limits. Space O(Σd) = O(45) = O(1).
- Python ints handle the answer up to ~5·10⁹ without overflow concerns.
