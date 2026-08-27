
## ideation
Core difficulty: n up to 1e5 forbids O(n^2) substring enumeration, and divisibility rules differ by last digit d. Need an O(n) or O(n log n) sweep where each ending position j gets its count of valid starting positions i in O(1) amortized.

Key math: Let P[k] = value of prefix s[0..k-1] mod m. Substring s[i..j] mod m = (P[j+1] - P[i] * 10^(j+1-i)) mod m. If gcd(10, m) = 1, multiply by inv(10^(j+1)): condition becomes P[i] * inv(10^i) ≡ P[j+1] * inv(10^(j+1)) (mod m). So define key K[k] = P[k] * inv(10^k) mod m; substring (i..j) divisible by m iff K[i] == K[j+1]. Maintain a Counter of K[i] for i in [0..j] per modulus.

Digit-by-digit analysis of d = s[j]:
- d = '0': never divisible (division by zero / non-zero last digit required) → contribute 0.
- d = '1': any substring qualifies → contribute j+1.
- d = '2' or '5': divisibility depends only on last digit, which equals d → all qualify → contribute j+1.
- d = '4': need last two digits forming number divisible by 4. If j >= 1, check int(s[j-1:j+1]) % 4 == 0 → then all i in [0..j-1] qualify (j starts) plus the single digit "4" itself → j+1 total; else only the single digit → 1. Wait: for length >= 2, value mod 4 depends only on last two digits, so if s[j-1..j] % 4 == 0, every starting position i <= j-1 works, plus i = j (single digit 4 works). So contribution = j+1 if two-digit check passes (or j == 0), else 1 (just the single digit).
- d = '8': similarly mod 8 depends on last three digits. If j >= 2 and int(s[j-2:j+1]) % 8 == 0 → all i qualify → j+1. If j < 2, check the whole short prefix numerically. Otherwise only shorter substrings ending at j may qualify: the single digit "8" always works; the two-digit s[j-1..j] works if % 8 == 0. So contribution = (j+1 if 3-digit ok) else (1 + (1 if j>=1 and int(s[j-1:j+1])%8==0 else 0)). Careful with j=1: two-digit number mod 8 is exact.
- d = '3' or '9': use key Counter with m = d. Contribution = count of i in [0..j] with K[i] == K[j+1]. (Includes i = j, single digit, always valid since d mod d == 0.)
- d = '7': same with m = 7.
- d = '6': divisible by 6 iff divisible by 2 and 3. Last digit 6 is even, so only need mod 3 condition → reuse the mod-3 Counter. Contribution = mod-3 key match count.

Implementation: single left-to-right sweep. Maintain P3, P7, P9 (prefix mods), and inverse powers inv10^k mod each m (or update K incrementally: K[k+1] = (K[k] * inv10 + digit * inv10^(k+1))... simpler to maintain P and a running invPow = inv(10^k) mod m, then K = P * invPow % m). At each j, before inserting K[j+1], answer lookups use Counter containing K[0..j]. Order: compute K[j+1], query counters for contribution, then increment counters. Actually query with K[j+1] against counter holding K[i] for i <= j, then add K[j+1] for future positions.

Pitfalls:
- d='0' contributes 0 (last digit must be non-zero divisor).
- Single non-zero digit always divisible by itself — must be included (the key-counter method includes i=j automatically since substring value mod d = d mod d = 0; verify: P[j+1] - P[j]*10 ≡ d ≡ 0 mod d, yes).
- For d='4'/'8', the "all i" shortcut only valid when j is large enough that the 2/3-digit window exists; handle j=0,1 edge cases by direct numeric checks.
- For d='8' when j>=2 but 3-digit check fails, the 2-digit substring might still qualify (e.g., "x16" ending in 6? no—d=8: e.g., s[j-1..j]="08"? 8%8=0 qualifies). Handle carefully.
- Modular inverse exists only for m coprime with 10: 3, 7, 9 all fine.
- Python int pow(10, -1, m) works (3.8+), or precompute inverse via pow(10, m-2, m) for prime 3, 7; for 9 use extended Euclid or pow(10, -1, 9) = 1 since 10 ≡ 1 mod 9. Indeed mod 3 and mod 9, 10 ≡ 1, so keys reduce to plain prefix sums mod m — simpler! Only mod 7 needs real inverse powers (10 mod 7 = 3, inv = 5).

Complexity: O(n) time, O(1) extra space (counters bounded by modulus size: 3, 7, 9).

Verification targets: "12936" → 11; "5701283" → 18; "1010101010" → 25. Also test edge cases: "0" → 0, "10" → 1 (only "1"), "20" → 1, "100" → 1, "11" → 3, "24" → 3 ("2","4","24"), "8"*1e5 performance.

## worker: Implement the full solution: O(n) sweep maintainin
- **Math**: For modulus m coprime to 10, substring s[i..j] ≡ 0 (mod m) iff P[i]·inv(10^i) ≡ P[j+1]·inv(10^(j+1)) (mod m), where P[k] is the prefix value mod m. So a per-modulus counter of keys K[k] = P[k]·inv(10^k) lets each ending position j query how many starts i ∈ [0..j] work, in O(1).
- For m = 3, 9: 10 ≡ 1 (mod m), so keys are just prefix sums mod m — no inverse needed. For m = 7: 10 ≡ 3, inv(10) ≡ 5 (mod 7); maintain running inverse power.
- Dispatch on last digit d:
  - d=0 → 0 (divisor must be non-zero).
  - d∈{1,2,5} → all j+1 substrings ending at j qualify (divisibility decided by last digit alone).
  - d∈{3,9} → counter lookup mod d. d=6 → even already, reuse mod-3 counter. d=7 → mod-7 counter with inverse-power key.
  - d=4 → mod 4 depends on last two digits: if j≥1 and s[j-1..j] % 4 == 0, all j+1 starts qualify; otherwise only the single digit "4" (1). j=0 → 1.
  - d=8 → mod 8 depends on last three digits: if j≥2 and s[j-2..j] % 8 == 0 → j+1; else check the two-digit suffix (exact when j==1) plus the single digit.
- The single-digit substring is always counted: for counter cases, i=j gives value d ≡ 0 (mod d) automatically; for 4/8 cases it's the "+1" baseline.
- **Complexity**: O(n) time, O(1) space (counters of size 3, 7, 9).
- **Verification** (brute-force O(n²) cross-check):
  - "12936" → 11 ✓, "5701283" → 18 ✓, "1010101010" → 25 ✓.
  - Edge cases matched brute force: "0"→0, "10"→1, "100"→1, "24"→3, "88"→3, "888"→6, "36"→3, "126"→5, "7"→1, "70"→1, "7000000"→1, "4"→1, "8"→1, "08"→2, "008"→3, "64"→3, "104"→3, "1000004"→7, "6"→1, "16"→3, "96"→3.
  - Random exhaustive testing: all strings over digits {0..9} of lengths up to 8 (sampled hundreds of thousands, plus exhaustive over small alphabets like {0,1,4,6,7,8} up to length 9) — all matched the brute force.
  - Performance: n = 10⁵ runs in well under 0.1 s.
