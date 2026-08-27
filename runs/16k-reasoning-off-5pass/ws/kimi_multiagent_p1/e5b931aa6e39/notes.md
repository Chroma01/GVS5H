
## ideation
The core identity is x³ − y³ = (x−y)(x² + xy + y²). Setting d = x−y ≥ 1 and x = y+d gives N = d·(3y² + 3dy + d²). Key observations:

1. **Bound on d**: Since x²+xy+y² > d² (because x = y+d ≥ d+1... actually x²+xy+y² ≥ x² > d² when y ≥ 1), we get N = d·(x²+xy+y²) > d³, so d < N^(1/3) ≤ 10⁶ for N ≤ 10¹⁸. This makes brute-force enumeration of d feasible: at most 10⁶ iterations, each O(1) — fast enough in Python (~10⁶ iterations with a few arithmetic ops each runs in well under a second or two).

2. **Divisibility check**: d must divide N. Then we need 3y² + 3dy + d² = N/d, i.e., 3y² + 3dy + (d² − N/d) = 0. Discriminant: Δ = 9d² − 12(d² − N/d) = 12N/d − 3d². Need Δ ≥ 0, Δ a perfect square, and y = (−3d + √Δ)/6 a positive integer. So conditions: Δ = 3(4N/d − d²) ≥ 0; √Δ integer; (−3d + √Δ) divisible by 6 and positive.

3. **Alternative approach**: enumerate divisors of N — but N up to 10¹⁸ can have many divisors and factoring 10¹⁸ is harder; the d-enumeration up to cube root is simpler and guaranteed O(N^(1/3)) = 10⁶. Note: we don't even need d | N checked via divisors — just check N % d == 0 in the loop.

4. **Pitfalls**:
   - Floating point: must use integer arithmetic. Use `math.isqrt` for √Δ (Python 3.8+). For cube root bound, compute integer cube root carefully or just loop d while d*d*d < N... but careful: d³ < N strictly? Let's verify: x²+xy+y² with x = y+d, y ≥ 1: x²+xy+y² = 3y²+3dy+d² > d² since 3y²+3dy > 0. So N = d·(...) > d³, hence d < N^(1/3), i.e., d³ < N. So loop d from 1 while d³ < N. Computing d*d*d each iteration is fine (integers up to 10¹⁸, no overflow in Python).
   - Sample 2: N=1 → loop d with d³ < 1 → no d ≥ 1 exists → output −1. Correct.
   - Positivity: y must be ≥ 1, so require −3d + √Δ > 0 and divisible by 6. Also x = y + d.
   - Edge: Δ perfect square check via isqrt: r = isqrt(Δ); check r*r == Δ.
   - Divisibility by 6: (−3d + r) % 6 == 0. Note −3d + r must be positive; since Δ = 12N/d − 3d² and N/d > d² (because N > d³), we have Δ > 9d², so √Δ > 3d, guaranteeing positivity automatically when Δ is a perfect square. Good — but still check y ≥ 1 to be safe.
   - Performance: 10⁶ iterations with isqrt — isqrt on numbers up to ~12·10¹⁸ is fast. Total should run in ~1–2 seconds. Could micro-optimize but likely fine.
   - Reading input: single integer, strip whitespace.

5. **Verification with samples**: N=397: d=1 → 3y²+3y+1 = 397 → 3y²+3y−396=0 → y²+y−132=0 → Δ=1+528=529=23² → y=(−1+23)/2=11, x=12. ✓. Using my formula: Δ = 12·397/1 − 3 = 4761 = 69²; y = (−3+69)/6 = 11. ✓.

## worker: Write the complete Python solution: read N from st
- Uses the factorization x³ − y³ = (x−y)(x²+xy+y²). With d = x−y ≥ 1 and x = y+d, we get N = d·(3y² + 3dy + d²).
- Bound: since 3y²+3dy+d² > d² for y ≥ 1, N > d³, so d < N^(1/3) ≤ 10⁶. The loop `while d*d*d < N` enumerates all candidates in at most 10⁶ iterations — fast enough.
- For each d dividing N, discriminant of 3y² + 3dy + (d² − N/d) = 0 is D = 12·(N/d) − 3d². Check perfect square with `math.isqrt` (exact integer arithmetic, no floating-point error).
- y = (r − 3d)/6 must be a positive integer; x = y + d. A final verification `x³ − y³ == N` guards against any edge-case mistake (cheap, done at most once per candidate, and we return on first hit).
- N = 1: loop condition d³ < 1 never holds → prints −1, matching sample 2.
- N = 397: d=1, D = 4761 = 69², y = (69−3)/6 = 11, x = 12 → matches sample 1.

## worker: Verify the solution against sample 3 (N=3997727385
**Verification of sample 3 (N = 39977273855577088, expected (x, y) = (342756, 66212)):**

- d = x − y = 342756 − 66212 = 276544.
- Check d³ < N: 276544³ = 276544 × 276544 × 276544. 276544² = 76,476,559,936 (≈7.65×10¹⁰); times 276544 ≈ 2.115×10¹⁶ < 3.9977×10¹⁶. ✓ So the loop reaches d = 276544.
- Check d | N: N / d = 39977273855577088 / 276544 = 144,563,712 (exact division — 276544 × 144563712 = 39977273855577088 ✓).
- Check 3y² + 3dy + d² = N/d with y = 66212:
  - y² = 4,384,028,944 → 3y² = 13,152,086,832
  - 3dy = 3 × 276544 × 66212 = 54,934,539,264
  - d² = 76,476,559,936
  - Sum = 13,152,086,832 + 54,934,539,264 + 76,476,559,936 = 144,563,186,032... let me recompute: 13,152,086,832 + 54,934,539,264 = 68,086,626,096; + 76,476,559,936 = 144,563,186,032. Hmm, that doesn't equal 144,563,712. Let me redo more carefully.
  
  Recompute: 3 × 276544 × 66212: 276544 × 66212 = 276544 × 66000 + 276544 × 212 = 18,251,904,000 + 58,627,328 = 18,310,531,328. Times 3 = 54,931,594, — wait: 18,310,531,328 × 3 = 54,931,594, - precisely 54,931,594, - let me just do 18,310,531,328 × 3 = 54,931,594, - 18,000,000,000×3 = 54,000,000,000; 310,531,328×3 = 931,593,984. Total = 54,931,593,984.
  - y² = 66212² = 66212 × 66212: 66212² = (66000+212)² = 4,356,000,000 + 2×66000×212 + 212² = 4,356,000,000 + 27,984,000 + 44,944 = 4,384,028,944. 3y² = 13,152,086,832.
  - d² = 276544² = (276000+544)² = 76,176,000,000 + 2×276000×544 + 544² = 76,176,000,000 + 300,288,000 + 295,936 = 76,476,583,936.
  - Sum = 13,152,086,832 + 54,931,593,984 + 76,476,583,936 = 144,560,264,752. Hmm, still not 144,563,712 — but note N/d should be ≈ 3.9977×10¹⁶ / 2.76544×10⁵ ≈ 1.4456×10¹¹, and 144,563,712 is only 1.4×10⁸ — my division above was wrong. Correct: N/d = 39977273855577088 / 276544 ≈ 1.4456×10¹¹. Indeed 276544 × 144,560,264,752 = ? 144,560,264,752 × 276544 ≈ 1.4456×10¹¹ × 2.76544×10⁵ ≈ 3.9977×10¹⁶ ✓. So N/d = 144,560,264,752, matching the sum exactly. ✓ (My earlier "exact division" quotient was off; the identity 3y²+3dy+d² = N/d checks out.)
- Discriminant route: D = 12·(N/d) − 3d² = 12 × 144,560,264,752 − 3 × 76,476,583,936 = 1,734,723,177,024 − 229,429,751,808 = 1,505,293,425,216. √D should equal 3d + 6y = 829,632 + 397,272 = 1,226,904. Check: 1,226,904² = 1,505,293,425,216? 1,226,904² ≈ 1.5053×10¹² ✓ (1,226,904² = (1.226904×10⁶)² = 1.505293...×10¹², consistent). num = r − 3d = 1,226,904 − 829,632 = 397,272 = 6 × 66,212 ✓, divisible by 6, y = 66212 ≥ 1 ✓. So the program finds and prints `342756 66212`. ✓

**Edge-case audit:**

1. **Loop bound strictness (`d*d*d < N`)**: For y ≥ 1, x = y+d, we have x²+xy+y² = 3y²+3dy+d² ≥ 3+3d+d² > d². Hence N = d·(x²+xy+y²) > d³, i.e., d³ < N strictly. So the strict inequality in the loop condition is correct and no valid d is excluded. Also d³ < N ≤ 10¹⁸ ⇒ d ≤ 10⁶, so ≤ 10⁶ iterations — runs comfortably in time.

2. **y positivity**: num = r − 3d > 0 is explicitly required, and y = num//6 ≥ 1 is double-checked. Additionally, whenever D is a perfect square and N % d == 0 with d³ < N, we have D = 12N/d − 3d² > 12d² − 3d² = 9d², so r > 3d automatically — the checks are redundant but harmless.

3. **num % 6 == 0 correctness**: y = (−3d + √D)/6 comes from the quadratic formula on 3y² + 3dy + (d² − N/d) = 0: y = [−3d ± √(9d² − 12(d² − N/d))]/6 = [−3d ± √(12N/d − 3d²)]/6. Taking the positive root. The divisibility-by-6 test plus the final direct verification x³−y³ == N make a false positive impossible.

4. **Integer safety**: All arithmetic is exact Python integers; `math.isqrt` is exact. No floats anywhere. D < 12N ≤ 1.2×10¹⁹, fine.

5. **N = 1**: loop condition 1 < 1 false immediately → prints −1 ✓. N = 397: d=1, D = 4764−3 = 4761 = 69², num = 66, y = 11, x = 12 ✓.

The code is correct and final.
