
## ideation
The core problem: given N up to 1e18, find positive integers x > y with x³ - y³ = N. The identity (x - y)(x² + xy + y²) = N is key. Direct brute force over x is impossible (x ~ 1e6 for N=1e18). The factor d = x - y is a divisor of N and must satisfy d³ < N (since x³ - (x-d)³ ≥ 3d³ > d³). So d is at most ~N^(1/3) ~ 1e6. We can iterate d from 1 upward, checking only d such that d divides N and 3d³ ≤ N. For each candidate d, we solve the quadratic derived from expanding (x - (x-d))³ = N, giving 3d x² - 3d² x + (d³ - N) = 0. The discriminant D = 3d(4N - d³) must be a perfect square. Then x = (3d² + sqrt(D)) / (6d) must be integer, and y = x - d positive.

Pitfalls:
- N up to 1e18: need 128-bit integer arithmetic (Python handles big ints natively, fine).
- Checking d divides N is O(1) but we still iterate up to ~1e6 steps. That's ~1e6 iterations, each with a few multiplications and an integer square root, perfectly fast in Python (maybe 0.1-0.5s).
- Need to ensure we don't overflow when computing 4N - d³, etc. Python int is arbitrary precision.
- Edge case: N = 0? Constraint says N ≥ 1, so we don't worry.
- Edge case: d must be such that 4N - d³ > 0 for D to be positive, otherwise no solution.
- The quadratic might give x not integer: check denominator divides numerator.

Alternative: iterate over divisors of N. Since N ≤ 1e18, number of divisors is at most ~10^5 (actually much less, ~10^5 in worst case for highly composite numbers, but usually < 10^4). For each divisor d, check if d < N^(1/3) and test. This might be more complex to code and not significantly faster.

Better: iterate d from 1 to floor(N^(1/3)), check if N % d == 0, then test discriminant. This is simple and efficient enough.

Check sample: N=397, N^(1/3)≈7.3, d from 1..7. d=1: D=3*1*(4*397-1)=3*1587=4761=69². x=(3+69)/6=72/6=12, y=11. Works.

Check N=1: N^(1/3)=1, d=1: 4N-d³=3, D=3*1*3=9=3², x=(3+3)/6=1, y=0, not positive. No solution.

Check large sample: N=39977273855577088, N^(1/3)≈342756 (matches x in output). So x - y = d, y = 66212, d = 342756 - 66212 = 276544. But 276544³ is huge, larger than N? Wait, we need d such that d³ < N. 276544³ ≈ 2.1e15, while N ≈ 4e16. So d ≈ 276544, cube ≈ 2.1e15 < 4e16, okay. Actually x-y = 276544. We iterate d up to floor(N^(1/3)) ≈ 342756. 276544 is within range. So the method works.

Implementation details:
- Use integer arithmetic.
- Compute integer sqrt via math.isqrt (Python 3.8+).
- For each d from 1 while d*d*d <= N:
    - if N % d != 0: continue (actually, wait: does d need to divide N? Let's check: x³ - y³ = (x-y)(x²+xy+y²) = d * M = N. So d must divide N. So yes, N % d == 0.)
    - Compute discriminant: D = 3*d*(4*N - d**3). Must be > 0.
    - s = isqrt(D). If s*s != D, continue.
    - numerator = 3*d*d + s
    - denominator = 6*d
    - if numerator % denominator != 0: continue.
    - x = numerator // denominator
    - y = x - d
    - if y > 0: output (x, y) and return.
- If loop finishes, output -1.

Wait: is it true that d must be a divisor of N? Yes, because d = x-y and d * (x²+xy+y²) = N, and both factors are integers. So d | N. So we can skip d not dividing N, but checking N % d == 0 for each d up to 1e6 is cheap.

Alternatively, we can find divisors of N and iterate. But enumerating divisors of a 1e18 number can be done by factoring or trial division up to sqrt(N) which is 1e9 - too slow. So iterating d and checking divisibility is the way.

Time complexity: O(N^(1/3)) ≈ O(1e6) operations. Each operation is a few big integer multiplications and an isqrt. Python can do this within time limits (likely 2 seconds? Might be a bit tight, but should pass with optimized code, maybe using local variables and avoiding repeated attribute lookups).

Potential micro-optimizations:
- Precompute N once.
- Use isqrt from math.
- Break early if 3*d**3 > N? Actually the loop condition d*d*d <= N is fine, but we also need 3d³ <= N? No, the inequality x³ - (x-d)³ >= 3d³ is true for x >= d (since x > d > 0). So if 3d³ > N, no x can satisfy because the minimum difference for that d is > N. So we can tighten loop to while 3*d**3 <= N. That is a slightly smaller bound. Let's compute: we need 3d³ ≤ N => d ≤ (N/3)^(1/3). This is a constant factor smaller, maybe ~0.7 of the cube root. For N=1e18, d_max ~ 6.9e5 instead of 1e6. Marginal speedup. Actually we also need d³ < 4N for discriminant to be positive, but 3d³ ≤ N implies d³ ≤ N/3 < 4N, so that's covered. So loop bound can be while 3*d**3 <= N. But careful: N up to 1e18, d^3 might overflow in some languages, but in Python it's fine. We can compute d^3 safely. But we can also loop while d*d <= N // d (to avoid huge numbers? Not needed in Python). Let's just use while 3*d**3 <= N.

Wait, is the bound 3d³ ≤ N correct? Let's verify: For given d, we want x > d (since y = x-d > 0 => x > d). The minimal value of f(x) = x³ - (x-d)³ occurs at x = d? Let's check derivative: f'(x) = 3x² - 3(x-d)² = 6dx - 3d². Set to zero: x = d/2. Wait, that's a minimum? Let's examine f(x) for x > d. Actually f(x) = 3d x² - 3d² x + d³. This is a quadratic in x, opening upwards (coefficient 3d > 0). The minimum occurs at x = (3d²)/(2*3d) = d/2. But x must be > d, so on the interval (d, ∞), f(x) is increasing (since the vertex is at d/2 < d). So the minimum on x > d is at x = d+1 (or limit as x→d+). Let's compute f(d) = d³ - 0 = d³. But y = x-d = 0, not positive. For x = d+1: f = (d+1)³ - 1³ = 3d² + 3d + 1. For large d, this is ~3d². Wait, that's much smaller than 3d³! Let's check: x³ - y³ = (x-y)(x²+xy+y²). If x = d+1, y = 1, then x-y = d, x²+xy+y² = (d+1)² + (d+1) + 1 = d²+2d+1 + d+1 + 1 = d²+3d+3. So N = d(d²+3d+3) = d³ + 3d² + 3d. For large d, this is ~d³, not 3d³. My earlier claim 3d³ was wrong. Let's re-derive the minimum of f(x) for x > d.

We have f(x) = 3d x² - 3d² x + d³. This is a quadratic in x with positive leading coefficient. The minimum over all real x is at x = d/2, with value f(d/2) = 3d(d/2)² - 3d²(d/2) + d³ = 3d(d²/4) - 3d³/2 + d³ = (3/4)d³ - (3/2)d³ + d³ = (3/4 - 3/2 + 1)d³ = (1/4)d³. So the global minimum of the quadratic is d³/4. But we require x and y positive integers, so x > d ≥ 1. The function f(x) is increasing for x > d/2, so on x > d, f is strictly increasing. The minimum value for integer x > d is f(d+1) = 3d(d+1)² - 3d²(d+1) + d³ = 3d(d²+2d+1) - 3d³ - 3d² + d³ = 3d³ + 6d² + 3d - 3d³ - 3d² + d³ = d³ + 3d² + 3d. So for a given d, the smallest possible N is d(d²+3d+3) = d³ + 3d² + 3d. So we need N ≥ d³ + 3d² + 3d. This is roughly d³ for large d. So the bound d ≤ N^(1/3) is approximately correct, but we can be slightly tighter: d³ + 3d² + 3d ≤ N. For N up to 1e18, d_max is about 1e6 - 1 or 2. The exact bound doesn't matter much; we can just loop d from 1 upward while d³ ≤ N (or d*d*d <= N). That's safe and simple. The earlier bound 3d³ was a mistake. Let's correct: the loop should go while d**3 <= N. Actually, we need to ensure that for x = d+1, f(d+1) = d³+3d²+3d ≤ N. So if d³ > N, then certainly d³+3d²+3d > N. So d³ ≤ N is a necessary condition. So we can loop d from 1 while d**3 <= N. That's safe and simple.

Thus the algorithm:
```
N = int(input())
for d in range(1, 10**6+2):  # or while d**3 <= N
    if d**3 > N:
        break
    if N % d != 0:
        continue
    # check discriminant
    val = 4*N - d**3
    if val <= 0:
        continue
    D = 3*d*val
    s = isqrt(D)
    if s*s != D:
        continue
    num = 3*d*d + s
    den = 6*d
    if num % den != 0:
        continue
    x = num // den
    y = x - d
    if y > 0:
        print(x, y)
        exit()
print(-1)
```
Wait, does d need to divide N? Yes, because N = d * (x²+xy+y²). So N % d == 0. This is a good filter to skip many d. But checking divisibility for each d is cheap.

But wait: could there be a solution where d does not divide N? No, because x²+xy+y² is integer. So d must divide N. So checking N % d == 0 is correct and necessary.

Edge case: N = 1. d=1: 1%1=0. D = 3*1*(4*1-1) = 9. s=3. num = 3+3=6. den=6. x=1. y=0. y>0 fails. d=2: 2³=8 > 1, break. Output -1. Correct.

Check N=2: d=1: 2%1=0. D=3*(8-1)=21, not square. d=2: 8>2 break. -1. Is there a solution? 1³ - 0³ = 1, but y must be positive. So no.

Check N=7: d=1: 7%1=0. D=3*(28-1)=81, s=9. num=3+9=12, den=6, x=2, y=1. 2³-1³=8-1=7. Works. Good.

Check N=26: 3³-1³=27-1=26. d=2: N%2=0. D=3*2*(104-8)=3*2*96=576, s=24. num=3*4+24=36, den=12, x=3, y=1. Good.

Check N=16: d=1: D=3*(64-1)=189 not square. d=2: 2³=8 <=16, 16%2=0. D=3*2*(64-8)=3*2*56=336 not square. d=3: 27>16 break. -1. Is there a solution? 2³-0³=8, 3³-2³=19, 3³-1³=26, 4³-3³=64-27=37. So no.

Now, what about N=39977273855577088? N**(1/3) ≈ 342756. Loop d up to 342756. At d=276544, we should find solution. Let's check if N % 276544 == 0. 39977273855577088 / 276544 = ? Let's compute: 276544 * 144544000... Actually we know x=342756, y=66212, d=276544. N = 342756³ - 66212³. We can trust the sample.

So the algorithm is correct and efficient.

Potential issue: isqrt is available in Python 3.8+. Should be fine for competitive programming.

One more check: the discriminant formula D = 12dN - 3d^4? Let's re-derive to be sure.
Equation: 3d x² - 3d² x + (d³ - N) = 0.
Discriminant: (3d²)² - 4 * 3d * (d³ - N) = 9d^4 - 12d(d³ - N) = 9d^4 - 12d^4 + 12dN = 12dN - 3d^4 = 3d(4N - d³). Yes, matches.

So code is straightforward.

We need to output -1 if no solution.

One more thing: the loop bound. We can compute max_d = int(N**(1/3)) + 2. But careful with floating point. Better to loop while d*d*d <= N. Since d is integer, d**3 grows as integer. But d**3 for d up to 1e6 is up to 1e18, which is within Python int (no overflow). So we can write:
```
d = 1
while d**3 <= N:
    ...
    d += 1
```
This is safe and exact.

Alternatively, we can precompute the limit:
```
while d * d * d <= N:
```
Also fine.

Now, is there any case where d**3 <= N but no solution for that d, yet a solution exists for larger d? No, because if x > y, then d = x-y < x, and x³ - y³ = N. Since x > d, we have x³ > d³, so N = x³ - y³ < x³, but that doesn't bound d directly. Wait, we need to ensure that d cannot be larger than the cube root of N. Suppose x=10, y=9, d=1. N=1000-729=271. Cube root of 271 is ~6.5. d=1 ≤ 6.5. Suppose x=5, y=2, d=3. N=125-8=117. Cube root of 117 ~4.9. d=3 ≤ 4.9. Suppose x=2, y=1, d=1. N=8-1=7. d=1 ≤ 1.91. So indeed d ≤ N^(1/3). Proof: d = x-y < x. And x³ - y³ = N => x³ > N => x > N^(1/3). So d < x, but d could be close to x. However, if d is large, then y = x-d is small. The minimum N for given d is when y=1 (or y minimal positive integer). For y=1, N = x³ - 1 = (d+1)³ - 1 = d³ + 3d² + 3d. This is > d³. So d³ < N. So d < N^(1/3). So the bound d³ ≤ N is correct and safe.

Thus the algorithm is solid.

Complexities: O(N^(1/3)) time, O(1) space.

Now we need to write the solution in the required format: a Python program that reads from stdin, computes, writes to stdout.

Edge Cases:
- N very large, N=10^18. max_d = 10^6. Loop is 1e6 iterations. Python should handle this in < 1 second. Each iteration does a few multiplications and an isqrt. isqrt is fast but not instant. 1e6 isqrt calls might take around 0.5-1 second. That's acceptable.
- N is a perfect cube? e.g., N=8. d=1: 8%1=0. D=3*(32-1)=93 not square. d=2: 8%2=0, d³=8 <=8. D=3*2*(32-8)=3*2*24=144, s=12. num=3*4+12=24, den=12, x=2, y=0 -> invalid. d=3: 27>8 break. Output -1. Indeed, no solution because x³-y³=8 => (x-y)(x²+xy+y²)=8. Possibilities: d=1 => x²+xy+y²=8 => x=2,y=2? but y<x. x=2,y=1 gives 4+2+1=7. x=3,y=2 gives 9+6+4=19. d=2 => x²+xy+y²=4 => x=2,y=1 gives 4+2+1=7. No solution. So -1 correct.

What about N=2? No solution.

What about N=0? Not in constraints.

Now, let's double-check the discriminant condition. We need D to be a perfect square. But also, since x = (3d² + sqrt(D)) / (6d) must be positive. Since sqrt(D) ≥ 0, numerator positive. Denominator positive. So x > 0. But we need x > d to ensure y = x-d > 0. So we must check y > 0.

Also, note that the other root of the quadratic is (3d² - sqrt(D)) / (6d). This would give a smaller x, possibly less than d. We want the larger root because x > y. Actually both roots are positive if D < 9d^4. But the larger root corresponds to x > d/2, and we need x > d. Let's check: the larger root is (3d² + sqrt(D)) / (6d) = d/2 + sqrt(D)/(6d). Since sqrt(D) = sqrt(3d(4N - d³)). For x > d, we need d/2 + sqrt(D)/(6d) > d => sqrt(D) > 3d². Is that guaranteed? Not necessarily. But we can just compute x and check y > 0. If the larger root gives y ≤ 0, the smaller root will give even smaller x, so also y ≤ 0. So checking y > 0 is sufficient.

But wait: what if the smaller root gives a valid x? For example, N=7, d=1. D=81, sqrt=9. Larger root: (3+9)/6=2. Smaller: (3-9)/6 = -1, negative. So only larger root matters. For N=26, d=2. D=576, sqrt=24. Larger: (12+24)/12=3. Smaller: (12-24)/12 = -1. So only larger root is positive. Actually, the product of roots is (d³ - N)/(3d). For N large, this could be negative, so one root positive, one negative. For N small relative to d³, the product is positive. But the sum of roots is d, so both roots sum to d. If one is negative, the other is > d. If both positive, then both are < d? Actually sum = d, so if both positive, each < d. But we need x > d. So if both roots are positive, neither is > d, so no solution with y > 0. But could there be a solution with x < d? No, because x = y + d > d. So the only possible solution is the larger root, which is > d/2. If the larger root is ≤ d, then y ≤ 0. So we must check y > 0.

Thus, the algorithm is:
- For d from 1 while d**3 <= N:
  - if N % d != 0: continue
  - val = 4*N - d**3
  - if val <= 0: continue
  - D = 3*d*val
  - s = isqrt(D)
  - if s*s != D: continue
  - x = (3*d*d + s) // (6*d)
  - if (3*d*d + s) % (6*d) != 0: continue
  - y = x - d
  - if y > 0: print(x, y) and return
- print(-1)

Wait, is the condition 4N - d³ > 0 necessary? If 4N - d³ <= 0, then D <= 0. D = 0 would mean x = d/2, not integer or y=0. D < 0 means no real roots. So we can skip.

But note: if D=0, then x = d/2, y = -d/2, not positive. So skip.

Now, let's test on a random case to be sure. Suppose N = 100. d=1: 100%1=0. val=400-1=399. D=3*399=1197. isqrt=34 (34²=1156, 35²=1225). Not square. d=2: 100%2=0. val=400-8=392. D=3*2*392=2352. isqrt=48 (48²=2304, 49²=2401). No. d=3: 100%3=1 no. d=4: 100%4=0. val=400-64=336. D=3*4*336=4032. isqrt=63 (3969), 64²=4096. No. d=5: 100%5=0. val=400-125=275. D=3*5*275=4125. isqrt=64 (4096), 65²=4225. No. d=6: 100%6=4 no. d=7: 343>100 break. So -1. Is there a solution? Let's check small x,y: 5³-4³=125-64=61. 6³-5³=216-125=91. 7³-6³=343-216=127. 4³-3³=64-27=37. 3³-2³=27-8=19. 2³-1³=8-1=7. None is 100. So -1 correct.

What about N=91? d=1: 91%1=0. val=364-1=363. D=1089=33². s=33. num=3+33=36, den=6, x=6, y=5. 6³-5³=216-125=91. Works.

N=127: d=1: 127%1=0. val=508-1=507. D=1521=39². num=3+39=42, den=6, x=7, y=6. 7³-6³=343-216=127. Works.

N=1728 = 12³. d=1: 1728%1=0. val=6912-1=6911. D=20733, not square. d=2: 1728%2=0. val=6912-8=6904. D=3*2*6904=41424, sqrt 203? 203²=41209, 204²=41616. No. d=3: 1728%3=0. val=6912-27=6885. D=3*3*6885=61965, sqrt 248? 248²=61504, 249²=62001. No. d=4: 1728%4=0. val=6912-64=6848. D=3*4*6848=82176, sqrt 286? 286²=81796, 287²=82369. No. d=6: 1728%6=0. d³=216. val=6912-216=6696. D=3*6*6696=120528, sqrt 347? 347²=120409, 348²=121104. No. d=8: 1728%8=0. d³=512. val=6912-512=6400. D=3*8*6400=153600, sqrt 391? 391²=152881, 392²=153664. No. d=9: 1728%9=0. d³=729. val=6912-729=6183. D=3*9*6183=166941, sqrt 408? 408²=166464, 409²=167281. No. d=12: 1728%12=0. d³=1728. val=6912-1728=5184. D=3*12*5184=186624, sqrt 432? 432²=186624! Yes. s=432. num=3*144+432=432+432=864. den=72. x=12. y=0. Not positive. So no solution with y>0. Indeed, 12³-0³=1728 but y must be positive. Is there any other? x=13, y=5? 13³-5³=2197-125=2072. Too large. So -1.

The algorithm finds the pair where y=0, but we reject it. Good.

Now, what about N=1728-1=1727? d=1: val=6908-1=6907. D=20721, not square. ... d=11: 1331. d=12: d³=1728 >1727, loop ends. So -1. But maybe there is a solution? 12³-11³=1728-1331=397. 13³-12³=2197-1728=469. So 1727 is not a difference. Good.

Now, let's think about the maximum N=1e18. d_max = 10^6. Loop 1e6 times. Each iteration: a few multiplications (each up to 1e18 * 1e6 = 1e24? Actually d up to 1e6, d*d up to 1e12, 3*d*d up to 3e12, D = 3*d*(4N - d³). 4N is 4e18, d³ is 1e18, so 4N - d³ up to 4e18. D up to 3*1e6*4e18 = 1.2e25. That's a 84-bit number. Python handles it fine. isqrt on a 84-bit number is fast. The loop should be fine.

One potential optimization: precompute N % d != 0 check. We can skip d that don't divide N. The density of divisors is low, so we will do the discriminant check for only a few d. Actually, the number of divisors of a random number is small. But worst case N = product of many small primes, number of divisors could be large? For N=1e18, the maximum number of divisors is around 103680 (for N=897612484786617600). But N is up to 1e18, and we only iterate d up to N^(1/3) ~ 1e6. The number of divisors up to 1e6 is not huge. But the loop runs 1e6 times regardless of divisor check. So the bottleneck is the isqrt for each d. Actually, we can skip the discriminant check if N % d != 0, so we only do isqrt for d dividing N. The number of such d is at most the number of divisors of N that are ≤ N^(1/3). For typical N, this is maybe a few hundred. For worst-case N with many small factors, it could be thousands. But 1e6 isqrt calls? No, we only call isqrt when N % d == 0. So we can structure the loop to check divisibility first, and if false, skip the isqrt. That saves time.

But wait: we can also generate only divisors of N up to N^(1/3) by factoring N. Factoring a 1e18 number is non-trivial. We can't trial divide up to 1e9. So we just iterate d and check N % d. That's fine.

But we can also note that d must be such that d | N, so we can find d by iterating over divisors of N. To find divisors, we can trial divide N by primes up to N^(1/3) ~ 1e6. That's 1e6 trial divisions, each with a modulo operation. That's similar cost. But we also need to check the discriminant for each divisor. The number of divisors is usually much less than 1e6, so the divisor enumeration is better. However, factoring N is more code. The simple loop is acceptable.

Let's estimate time: 1e6 iterations. In each iteration, we compute d**3 (or compare d**3 <= N), do N % d, maybe a few multiplications. That's maybe 10-20 operations per iteration. Python can do ~50 million simple operations per second? Actually Python is slower, maybe 10 million simple ops per second. 1e6 iterations with a few multiplications and a modulo might take 0.2-0.5 seconds. That's fine. If we add isqrt only for divisors, it's even faster.

But we must be careful: computing d**3 each iteration might be slow. We can update d_cube incrementally: d_cube = d**3, or just compute d*d*d. In Python, d**3 is fast for integers. But we can also use a while loop with d+=1 and compute d_cube = d**3 each time, or keep a running product? Not needed.

One more thing: the condition d**3 <= N. We can compute max_d = int(round(N ** (1/3))) and then adjust. But integer cube root is safer: we can write a helper to find the largest integer d such that d**3 <= N. But since N up to 1e18, d up to 1e6, we can just loop and break. The break condition is d**3 > N. So:
```
d = 1
while True:
    if d**3 > N:
        break
    if N % d == 0:
        # discriminant check
    d += 1
```
This is clean.

Potential issue: d**3 for d=1e6 is 1e18, which is fine. But computing d**3 in a loop might be slightly slower than d*d*d. Let's use d_cube = d**3 or just d*d*d. It's fine.

Now, let's write the code.

We need to import sys and math.

```python
import sys
import math

def solve():
    N = int(sys.stdin.readline())
    d = 1
    while d ** 3 <= N:
        if N % d == 0:
            val = 4 * N - d ** 3
            if val > 0:
                D = 3 * d * val
                s = math.isqrt(D)
                if s * s == D:
                    num = 3 * d * d + s
                    den = 6 * d
                    if num % den == 0:
                        x = num // den
                        y = x - d
                        if y > 0:
                            print(x, y)
                            return
        d += 1
    print(-1)

if __name__ == "__main__":
    solve()
```

Wait, is there any case where val > 0 but D is not a perfect square, and yet a solution exists? No, because the quadratic must have integer roots.

Let's test with N=397: d=1: 397%1=0. val=1588-1=1587>0. D=3*1*1587=4761. s=69 (69²=4761). num=3+69=72, den=6, x=12, y=11. Print. Good.

Test N=1: d=1: 1%1=0. val=4-1=3>0. D=9. s=3. num=3+3=6, den=6, x=1, y=0. y not >0. d=2: 8>1 break. Print -1. Good.

Test N=2: d=1: 2%1=0. val=8-1=7>0. D=21, s=4 (16), 5²=25. Not square. d=2: 8>2 break. -1. Good.

Test N=7: d=1: 7%1=0. val=28-1=27>0. D=81. s=9. num=12, den=6, x=2, y=1. Good.

Test N=26: d=1: 26%1=0. val=104-1=103>0. D=309, not square. d=2: 26%2=0. val=104-8=96>0. D=3*2*96=576. s=24. num=12+24=36, den=12, x=3, y=1. Good.

Test N=1728: as above, finds x=12,y=0, rejects, then d=13: 2197>1728 break. Print -1. Good.

Test N=0? Not needed.

What about N=9? d=1: 9%1=0. val=36-1=35>0. D=105, not square. d=2: 8<=9, 9%2=1 no. d=3: 27>9 break. -1. Is there a solution? 2³-1³=7, 3³-2³=19. No.

What about N=19? d=1: 19%1=0. val=76-1=75>0. D=225=15². s=15. num=3+15=18, den=6, x=3, y=2. 27-8=19. Good.

What about N=37? d=1: 37%1=0. val=148-1=147>0. D=441=21². s=21. num=3+21=24, den=6, x=4, y=3. 64-27=37. Good.

What about N=61? d=1: 61%1=0. val=244-1=243>0. D=729=27². s=27. num=30, den=6, x=5, y=4. 125-64=61. Good.

What about N=91? Already did.

What about N=127? Did.

It seems correct.

One more check: N=2*10^18? Constraint says N <= 1e18. So fine.

Now, consider the case where N is large and d is large, say N=10^18, d=10^6. d^3 = 10^18. val = 4*10^18 - 10^18 = 3*10^18. D = 3*10^6 * 3*10^18 = 9*10^24. isqrt(9e24) = 3e12. s*s = 9e24, matches. num = 3*10^12 + 3e12 = 6e12. den = 6*10^6 = 6e6. x = 1e6. y = 0. Rejected. So no solution. But maybe there is a solution for some smaller d. The loop will find it if exists.

Now, is it possible that for some d, val > 0 but D is a perfect square, but x is not integer? We check num % den == 0. That's correct.

Could there be a solution where the quadratic gives x but x is not integer? Then no integer solution for that d. So we skip.

Thus the algorithm is correct.

Now, let's think about performance. The loop runs up to 1e6 times. In each iteration, we compute d**3. That's a multiplication. Python integer multiplication for 1e6 is fast. The modulo N % d is also fast. The branch is predictable. The discriminant check is only done for divisors. So the inner block is rarely executed. This should be well within time limits.

But we must be careful: the problem might have a tighter time limit, but usually 1e6 iterations in Python is fine. Some problems require micro-optimizations, but this is standard.

One micro-optimization: use local variables for speed, e.g., assign N to a local variable. But it's not necessary.

Another thought: we can compute the integer cube root of N to get an upper bound for d, and then loop only up to that bound. That might save a few iterations if N^(1/3) is not integer. But computing integer cube root requires a loop or math.pow. Not needed.

Actually, we can compute max_d = int(N ** (1/3)) + 2. But N ** (1/3) uses float, which might have precision issues for large N. For N=10^18, float has 53 bits of mantissa, which is about 15-16 decimal digits. 10^18 is exactly representable? 2^60 ≈ 1.15e18, so 10^18 is not exactly representable, but close. The cube root might be off by 1. So we could overshoot or undershoot. But we can just loop while d**3 <= N. That's exact and safe.

Now, let's consider if there is any mathematical simplification to avoid isqrt. The discriminant D = 3d(4N - d³). For D to be a perfect square, since 3d must be a factor, we need 3d(4N - d³) = k². This is a Diophantine equation. But the direct method is fine.

Another approach: iterate over y, compute x³ = N + y³, check if x³ is a perfect cube. But x would be up to (N + y³)^(1/3). For y up to something. The maximum y is when x = y+1, so N = (y+1)³ - y³ = 3y² + 3y + 1. So y is about sqrt(N/3). For N=1e18, y_max ~ 5.77e8. That's too large. So the d-iteration is better.

Thus the plan is solid.

Now, write the final code. Ensure we handle input reading correctly. The input is a single integer. Use sys.stdin.read or sys.stdin.readline. Use .strip() to remove newline.

Edge case: N=0? Not in constraints, but if N=0, we need x^3 - y^3 = 0 => x=y. But positive integers x,y, so x=y>0 gives 0. But constraints say N>=1, so ignore.

One more check: N=1e18. d=1e6. d^3=1e18. The loop condition d**3 <= N is true for d=1e6. Then d+=1 makes d=1e6+1, d^3 > N, break. So loop runs 1e6 times. That's fine.

Now, is there any case where d**3 overflows in Python? No.

Thus, the code is ready.

But wait, I recall a similar problem from AtCoder or Codeforces. The solution is exactly this. The time limit might be 2 seconds. Python with 1e6 iterations and some big int arithmetic should be okay. But to be safe, we can add a small optimization: precompute d_cube and update it. Or use a for loop with range and break? But we don't know the exact bound. We can compute bound = int(N ** (1/3)) + 1. But as mentioned, float precision. We can write a helper to compute integer cube root:

```python
def icbrt(n):
    # returns floor(cuberoot(n))
    if n < 0:
        return -icbrt(-n)
    x = int(round(n ** (1/3)))
    while x**3 > n:
        x -= 1
    while (x+1)**3 <= n:
        x += 1
    return x
```

But that might be slower than just looping. Actually, for N up to 1e18, the float cube root is accurate to within 1. Because the cube of a 1e6 number is 1e18, and float has 15-16 digits of precision, so the error in cube root is about 1e6 * 1e-15 = 1e-9, so it should be accurate to the nearest integer. But to be absolutely safe, we can just use the while loop condition. It's simple and correct.

Let's consider the possibility of N being up to 10^18, and d up to 10^6. The loop will do 1e6 iterations. In each iteration, we do `d ** 3`. This is a multiplication of two integers. It's fast. The modulo is also fast. The isqrt is only for divisors. So the total time should be well under 1 second.

One more micro-optimization: Instead of `d ** 3`, we can do `d3 = d * d * d`. That's the same. Or maintain `d3` and update: `d3 += 3*d*d + 3*d + 1`? Actually (d+1)^3 - d^3 = 3d^2 + 3d + 1. So we can increment d3 by that. But it's not necessary.

We can also use `range(1, 10**6+2)` but we don't know the exact upper bound. We can compute the integer cube root using `int(N ** (1/3))` and then add 2. Let's do that and use a for loop, but we need to ensure we don't miss a solution. The integer cube root floor might be less than the true d_max. For example, if N=26, true d_max=2 (since 2^3=8<=26, 3^3=27>26). int(26**(1/3)) = int(2.962) = 2. So it's exactly the floor. For N=27, int(3.0)=3, d_max=3. But for N=28, int(28**(1/3))=3 (since 3^3=27<=28, 4^3=64>28). d_max=3. So floor is correct. But due to floating point, int(10^18 ** (1/3)) might be 999999 or 1000000. Let's test: 10^18 = 1000000000000000000. The cube root is 1000000 exactly. In Python, (10**18) ** (1/3) might give 999999.9999999999 or 1000000.0000000001. int() truncates. So we need to be careful. To avoid float issues, we can just use the while loop. It's foolproof.

But for a small speedup, we can do:
```
d = 1
while True:
    if d * d * d > N:
        break
    ...
    d += 1
```
This is clear and correct.

Now, let's think about the discriminant D = 3*d*(4*N - d**3). We can compute 4*N first. That's 4e18, fine. d**3 up to 1e18. So val up to 4e18. D up to 3*1e6*4e18 = 1.2e25. isqrt on that is fast.

One more thing: the problem asks for any pair (x,y) of positive integers. The order is x y. So we output x and y.

Now, is there any edge case where the discriminant is a perfect square but the numerator is negative? No, because sqrt(D) >= 0, 3*d*d > 0.

What about D=0? That happens if 4N = d³. Then s=0. num = 3d², den = 6d => x = d/2. So d must be even, and x = d/2. Then y = x - d = -d/2 < 0. So we reject. Our code checks y > 0, so it's fine.

Now, let's consider if the loop might be too slow because of the large integer arithmetic. 1e6 iterations of `d ** 3` and `N % d`. Each modulo is a big integer modulo small integer, which is fast. The multiplication `d * d` is also fast. The isqrt is only for a few hundred values. So total time is dominated by the 1e6 iterations of simple arithmetic. That should be okay.

But wait: we are using Python. 1e6 iterations might be borderline if each iteration is heavy. Let's estimate: `d ** 3` involves creating a new integer object? No, integers are immutable, so `d**3` creates a new integer. But it's cached for small ints? Not for large. However, we can avoid creating a new integer for the cube check by using `d3` variable. Let's do that to be safe.

```python
d = 1
d3 = 1
while d3 <= N:
    if N % d == 0:
        val = 4 * N - d3
        if val > 0:
            D = 3 * d * val
            s = math.isqrt(D)
            if s * s == D:
                num = 3 * d * d + s
                den = 6 * d
                if num % den == 0:
                    x = num // den
                    y = x - d
                    if y > 0:
                        print(x, y)
                        return
    d += 1
    d3 = d * d * d
```

This updates d3 incrementally. That's a bit faster because we avoid computing d**3 each time. But we need to be careful: d3 = d*d*d. For d up to 1e6, d*d is up to 1e12, then *d is 1e18. That's fine. And we only do this update once per iteration.

Alternatively, we can just use the while d**3 <= N and not worry. Let's test which is faster. In Python, computing d**3 might be optimized to repeated multiplication, but the overhead of the function call or the exponentiation might be slightly higher than multiplication. But it's negligible. 1e6 iterations of `d ** 3` vs `d3 = d*d*d` - both are three multiplications. Actually, `d**3` is a built-in operation, probably as fast as multiplication. But updating d3 incrementally uses two multiplications and an addition: d3 += 3*d*d + 3*d + 1. That's also a few operations. It might be similar.

Given the simplicity, I'll use the while d**3 <= N. It's clean.

But wait: the while loop condition `d ** 3 <= N` is evaluated each iteration. That's an exponentiation. For d up to 1e6, it's fine. But if we want to micro-optimize, we can precompute the bound. However, I think it's fine.

Let's check the AtCoder problem "ABC 166 D - Cubes" or something? Actually, there is a problem "Cubes" from AtCoder Beginner Contest 166 (or similar). The constraints are N up to 10^18. The intended solution is to iterate d up to N^(1/3) and check discriminant. Many Python solutions pass.

So the code is correct.

One more check: the discriminant formula. Let's re-derive carefully to avoid any sign error.

We have x^3 - y^3 = N. Let d = x - y. Then x = y + d. Substitute:
(y + d)^3 - y^3 = N
3y^2 d + 3y d^2 + d^3 = N
3d y^2 + 3d^2 y + d^3 - N = 0

This is a quadratic in y: 3d y^2 + 3d^2 y + (d^3 - N) = 0.
We can solve for y:
y = [-3d^2 ± sqrt(9d^4 - 12d(d^3 - N))] / (6d)
y = [-3d^2 ± sqrt(9d^4 - 12d^4 + 12dN)] / (6d)
y = [-3d^2 ± sqrt(12dN - 3d^4)] / (6d)
y = [-3d^2 ± sqrt(3d(4N - d^3))] / (6d)

Since y must be positive, we take the plus sign:
y = (-3d^2 + sqrt(D)) / (6d)
where D = 3d(4N - d^3).

But wait! This gives y. In my earlier derivation, I had the equation in x. Let's check consistency.
If we solve for x instead: from y = x - d, so x = y + d.
x = [ -3d^2 + sqrt(D) ] / (6d) + d = [ -3d^2 + sqrt(D) + 6d^2 ] / (6d) = (3d^2 + sqrt(D)) / (6d).
Yes, that matches my earlier formula. So both are correct. The discriminant is the same.

So we can also solve for y. Sometimes solving for y might give a smaller numerator? But both work. Using x is fine.

Wait, in the y formula, the numerator is sqrt(D) - 3d^2. This could be negative if sqrt(D) < 3d^2. But y must be positive. So we need sqrt(D) > 3d^2. That is the same condition as x > d. So either way, we need to check the resulting integer is positive.

But note: using y, the denominator is 6d. The numerator is sqrt(D) - 3d^2. For large d, sqrt(D) = sqrt(3d(4N - d^3)). For this to be > 3d^2, we need 3d(4N - d^3) > 9d^4 => 12dN - 3d^4 > 9d^4 => 12dN > 12d^4 => N > d^3. So indeed, if N > d^3, it's possible. If N = d^3, then D = 3d(4d^3 - d^3) = 9d^4, sqrt = 3d^2, y=0. So we need N > d^3 for y>0. Our loop condition d^3 <= N allows d^3 = N, which gives y=0. We will reject it because y>0. So it's fine.

But wait: what if N is slightly larger than d^3? Then y might be 1? Let's check: if y=1, then N = x^3 - 1. And d = x-1. So d^3 = (x-1)^3. N - d^3 = x^3 - 1 - (x-1)^3 = 3x^2 - 3x + 1. For x large, N ≈ d^3. So indeed, for d close to the cube root of N, y can be small positive integer. So the loop bound d^3 <= N is correct.

Thus, everything is consistent.

Now, write the final solution code.

One final check: The problem statement says "positive integers (x,y)". So x >= 1, y >= 1. We must ensure we don't output 0 for y. We check y > 0.

Also, note that the sample input 1: 397, output 12 11. Our code will find d=1, x=12, y=11. Good.

Sample 2: 1 -> -1. Good.

Sample 3: 39977273855577088 -> 342756 66212. Let's verify d = 342756 - 66212 = 276544. d^3 = 276544^3. Let's compute approximate: 276544^3 ≈ (2.76544e5)^3 = 2.11e16. N ≈ 4e16. So d^3 < N. So loop will go up to d ≈ 342756. So it will check d=276544. Will it find it? Let's check: N % 276544 should be 0. D = 3*276544*(4*39977273855577088 - 276544^3). This should be a perfect square. Then x = (3*276544^2 + sqrt(D)) / (6*276544). Should give 342756. y = 342756 - 276544 = 66212. So it works.

Thus the solution is correct.

Potential improvements: use sys.stdout.write for faster output, but print is fine.

Now, I'll write the code in the final answer.</mm:think>### NOTES
The problem asks for positive integers \(x, y\) such that \(x^3 - y^3 = N\) with \(N \le 10^{18}\). The key identity is \(x^3 - y^3 = (x-y)(x^2+xy+y^2)\). Let \(d = x-y\). Then \(d\) must divide \(N\), and we have the equation \(3d x^2 - 3d^2 x + (d^3 - N) = 0\). The discriminant is \(D = 3d(4N - d^3)\), which must be a perfect square. The solution is \(x = \frac{3d^2 + \sqrt{D}}{6d}\). We iterate over possible \(d\) from 1 upward while \(d^3 \le N\) (since \(N > d^3\) is necessary for positive \(y\)). For each \(d\) that divides \(N\), we check if \(D\) is a perfect square and if the resulting \(x\) is an integer with \(y = x-d > 0\). The loop runs at most \(O(N^{1/3}) \approx 10^6\) iterations, which is fast in Python. We only perform the expensive square root check when \(d\) divides \(N\).

## worker: Implement the full solution: read N, loop over d f
The solution iterates over possible values of \(d = x - y\) up to the cube root of \(N\). For each divisor \(d\) of \(N\), it solves the quadratic equation derived from \(x^3 - y^3 = N\) and checks whether the discriminant is a perfect square and the resulting \(x, y\) are positive integers. The loop runs at most \(10^6\) times for the maximum constraint \(N = 10^{18}\), and the expensive square root check is only executed when \(d\) divides \(N\), ensuring the solution is efficient within typical time limits.
