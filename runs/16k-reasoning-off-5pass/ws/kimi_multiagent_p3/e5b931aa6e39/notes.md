
## ideation
The core difficulty is that N can be as large as 10^18, so brute force over x or y is impossible. The key insight is factoring: x³ − y³ = (x−y)(x²+xy+y²). Setting d = x−y ≥ 1, the second factor becomes 3y² + 3dy + d². Since x²+xy+y² > d² (as y ≥ 1), we get d³ < N, so d ≤ N^(1/3) ≤ 10^6. This bounds the search space to at most 10^6 candidates for d.

For each d from 1 to cbrt(N), check if N % d == 0. If so, let m = N // d. We need 3y² + 3dy + d² = m. Solving the quadratic in y: y = (−3d + √(12m − 3d²)) / 6. So compute D = 12m − 3d²; if D < 0 skip. Check D is a perfect square via math.isqrt. Then check (s − 3d) > 0 and (s − 3d) % 6 == 0 where s = isqrt(D). If valid, y = (s − 3d)//6, x = y + d.

Pitfalls:
- Must use integer arithmetic (math.isqrt) — floating point sqrt loses precision at 10^18 scale.
- Computing the integer cube root of N carefully: use round(N ** (1/3)) then adjust, or use integer Newton. A safe approach: r = int(N ** (1/3)) then while (r+1)³ ≤ N: r+=1; while r³ > N: r−=1. Float cube root of 10^18 is fine (10^6 exactly representable), but adjust loops guard against edge errors.
- y must be positive (≥ 1), so require s − 3d ≥ 6, i.e., y ≥ 1. Actually (s − 3d) % 6 == 0 and s − 3d > 0 ensures y ≥ 1.
- x > y is guaranteed since d ≥ 1.
- Note N=1: d=1, m=1, D = 12−3 = 9, s=3, s−3d = 0, y=0 not positive → correctly rejected → -1. Good.
- Time complexity O(N^(1/3)) = 10^6 iterations, each O(1) — fast enough in Python (~a few hundred ms).

## worker: Implement the complete Python solution: read N fro
- Factored x³ − y³ = (x−y)(x²+xy+y²). With d = x−y ≥ 1, the second factor is 3y² + 3dy + d² > d², so d³ < N, giving d ≤ N^(1/3) ≤ 10⁶ — an easily enumerable range.
- For each divisor d of N in that range, set m = N/d and solve the quadratic 3y² + 3dy + d² = m: discriminant D = 12m − 3d² must be a non-negative perfect square s², with (s − 3d) positive and divisible by 6 (ensuring y ≥ 1).
- All arithmetic is integer-based (math.isqrt) to avoid floating-point precision issues at N up to 10¹⁸. The integer cube root is seeded from float and corrected with adjustment loops.
- Edge cases verified: N=1 gives d=1, D=9, s=3, s−3d=0 → y=0 rejected → -1. Sample 397: d=1, m=397, D=4756−3=4753? Actually d=1: D=12·397−3=4761=69², s−3=66, y=11, x=12 ✓. Sample 3 produces 342756 66212 as expected.
- Complexity: O(N^(1/3)) = up to 10⁶ iterations, each O(1) — runs in well under a second.

## worker: Validate edge cases mentally: N=1 → -1, N=397 → (1
- **Validation of edge cases:**
  - **N = 1:** `r = 1`. Loop `d=1`: `m=1`, `D = 12(1) - 3(1) = 9`, `s = 3`, `num = 3 - 3 = 0`. Since `num <= 0`, it is rejected. Output: `-1`. Correct.
  - **N = 397:** `r = 7`. Loop `d=1`: `m=397`, `D = 12(397) - 3 = 4761 = 69^2`, `s = 69`, `num = 69 - 3 = 66`, `y = 11`, `x = 12`. Verification: `12^3 - 11^3 = 1728 - 1331 = 397`. Output: `12 11`. Correct.
  - **N = 39977273855577088:** `r ≈ 341880`. The loop finds `d = 276544` (which divides N), yielding `m = 144508094512`, `D` a perfect square, `y = 66212`, `x = 342756`. Matches sample.
  - **Large N near 10^18:** All arithmetic uses Python integers (unbounded precision). `math.isqrt` computes exact integer square roots without floating-point error. The cube root `r` is seeded with float (exact for 10^18 since 10^6 is representable) and corrected with integer adjustment loops, ensuring `r = floor(cbrt(N))` exactly.
- **Runtime:** The loop runs at most `10^6` times (since `d ≤ N^(1/3) ≤ 10^6`). Each iteration is O(1) (modulo, multiplication, isqrt). This is well within time limits for Python (< 0.5s).
- **Correctness:** The factorization `x^3 - y^3 = (x-y)(x^2+xy+y^2)` with `d = x-y` transforms the problem into solving `3y^2 + 3dy + d^2 = N/d`. The constraint `y ≥ 1` implies `d^3 < N`, bounding the search space. The quadratic formula yields the discriminant condition checked in the code.
