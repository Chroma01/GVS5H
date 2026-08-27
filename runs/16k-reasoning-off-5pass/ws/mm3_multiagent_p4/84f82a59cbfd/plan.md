A "400 number" is a positive integer N = p1^(2a) * p2^(2b) where p1, p2 are distinct primes and a, b ≥ 1. Equivalently, N = (p^a * q^b)^2 is a perfect square with exactly 2 distinct prime factors (each raised to at least power 1 inside the square root). So we need, for each A, the largest N ≤ A that is a perfect square with exactly 2 distinct prime factors, each appearing with exponent ≥ 1 in the square root.

Strategy: enumerate all "base" values B = p^a * q^b with p,q distinct primes, a,b ≥ 1, and B^2 ≤ 10^12. Generate all such B, square them, collect into a sorted array. Then answer each query by binary searching the largest value ≤ A.

For efficiency:
- Enumerate prime squares: for each prime p, powers p^2, p^4, ... up to 10^6 (since B ≤ 10^6).
- Enumerate distinct prime pairs (p,q): B = p_i * q_j (simplest a=b=1) covers the densest cases; also include higher powers p^(2a) * q^(2b).
- More efficient: iterate over base B up to 10^6, check if B has exactly 2 distinct prime factors; if so, B^2 is a 400 number. Also try multiplying by square factors: for each B with exactly 2 distinct primes and each square factor t^2 ≤ 10^12 / B^2, compute (B*t)^2. This ensures all exponents can be ≥2.

After generating and sorting all 400 numbers ≤ 10^12 (there are ~few hundred thousand), binary search for each query.