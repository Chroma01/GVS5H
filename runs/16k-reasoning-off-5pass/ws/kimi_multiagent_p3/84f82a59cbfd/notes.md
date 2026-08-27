
## ideation
The core insight is that a 400 number is exactly a perfect square whose square root has exactly two distinct prime factors. So for each query A, I need the largest s ≤ floor(sqrt(A)) such that s has exactly 2 distinct prime factors, then output s².

Key considerations:
- A ≤ 10^12, so s ≤ 10^6. A sieve up to 10^6 precomputing distinct-prime-factor counts is feasible (O(n log log n)).
- The main risk: how large can the gap be between consecutive integers with exactly 2 distinct prime factors? If gaps near 10^6 could be large (say thousands), a per-query linear scan with Q = 2×10^5 could TLE in Python. Mitigation: precompute a "previous valid" pointer array (prev[i] = largest valid index ≤ i) in O(n), making each query O(1). This is the safest approach.
- Pitfall: integer square root must be exact — use math.isqrt, not int(sqrt()) with floats (precision issues near 10^12).
- Pitfall: s must have *exactly* 2 distinct prime factors (not ≤2). s=1 (0 factors) and prime powers (1 factor) are invalid.
- Memory: arrays of size 10^6+1 are fine. Use array module or plain lists; lists of ints in Python for 10^6 are ~8MB each (as small ints cached... actually ints up to 10^6 aren't all cached; use array('i') or just lists — two lists of 10^6 ints is acceptable, roughly 16-36MB; could use a single pass with SPF sieve).
- Fast I/O needed for 2×10^5 lines: sys.stdin.buffer.read.

## worker: Write the complete Python solution: sieve distinct
- A 400 number N has exactly two distinct prime factors p, q, each appearing an even number of times, so N = p^{2a} q^{2b} = (p^a q^b)^2. Conversely, any square s² where s has exactly two distinct prime factors is a 400 number. So the answer for query A is s² where s is the largest integer ≤ floor(sqrt(A)) with exactly 2 distinct prime factors.
- Since A ≤ 10^12, s ≤ 10^6. Sieve `omega` (distinct prime factor count) up to 10^6 in O(n log log n): for each prime i (detected by omega[i] == 0), increment omega[j] for all multiples j of i. This correctly counts distinct primes because each prime divides its multiples and contributes exactly 1.
- Build `prev_valid[i]` = largest valid s ≤ i in one O(n) pass, making each query O(1): isqrt, table lookup, square.
- Used math.isqrt for exact integer square root (no float precision issues at 10^12).
- Sample verification:
  - A=404: isqrt=20; numbers ≤20 with exactly 2 distinct prime factors: 6,10,12,14,15,18,20 → s=20, s²=400. ✓
  - A=36: isqrt=6; 6=2·3 valid → 36. ✓
  - A=60: isqrt=7; 7 is prime (1 factor), prev valid is 6 → 36. ✓
  - A=10^12: isqrt=10^6 = 2^6·5^6, exactly 2 distinct primes → 10^12. ✓
  - A=123456789: isqrt=11111; 11111 = 41·271 (2 distinct primes) → 11111² = 123454321. ✓
- Complexity: O(10^6 log log 10^6 + Q) time, O(10^6) memory. Fast bulk I/O via sys.stdin.buffer.read.
