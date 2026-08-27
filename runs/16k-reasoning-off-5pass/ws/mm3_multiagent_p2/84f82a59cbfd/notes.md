
## ideation
The problem asks for the largest number \(N \le A\) that has exactly 2 distinct prime factors and each appears with an even exponent. Such numbers are exactly perfect squares of integers with exactly 2 distinct prime factors. So we need the largest \(M \le \lfloor\sqrt{A}\rfloor\) with exactly 2 distinct prime factors, then output \(M^2\).

The maximum \(A\) is \(10^{12}\), so \(\lfloor\sqrt{A}\rfloor \le 10^6\). We can precompute all integers up to \(10^6\) with exactly 2 distinct prime factors using a sieve that counts the number of distinct prime factors (\(\omega\)). For each prime \(p\), increment \(\omega\) for all multiples of \(p\). Then collect all \(i\) with \(\omega[i] = 2\).

The number of such integers up to \(10^6\) is only around 200,000, so they fit easily in memory. For each query, compute \(s = \lfloor\sqrt{A}\rfloor\), binary search the largest \(M \le s\) in the precomputed list, and output \(M^2\).

Pitfalls:
- The square root \(M\) does not need to be square-free; e.g., \(20 = 2^2 \cdot 5\) gives \(N = 400\).
- Sieve must count distinct prime factors, not total prime factors.
- Use `math.isqrt` for integer square root.
- A \(\ge 36\) guarantees a solution exists.

## worker: Implement a sieve up to 10^6 that counts distinct 
The solution reduces finding a 400 number \(N \le A\) to finding an integer \(M \le \lfloor\sqrt{A}\rfloor\) with exactly two distinct prime factors (no restriction on exponents), then returning \(M^2\).  
A sieve up to \(10^6\) marks multiples of each prime to count distinct prime factors (\(\omega\)). All \(i\) with \(\omega[i]=2\) are stored (about 210k values). Each query uses binary search on this sorted list. Complexity: sieve \(O(10^6 \log\log 10^6)\), query \(O(\log 210k)\) per query, total memory ~ few MB. Works within limits.
