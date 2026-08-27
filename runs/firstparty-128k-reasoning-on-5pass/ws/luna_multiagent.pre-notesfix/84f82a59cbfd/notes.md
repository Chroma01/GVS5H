
## ideation
The core difficulty is supporting up to \(2\times10^5\) queries while \(A\) may be as large as \(10^{12}\). The key reformulation is that a valid number is exactly the square of an integer whose prime-factor set has size two: \(N=x^2\), where \(x=p^a q^b\) for distinct primes \(p,q\) and positive exponents. Thus \(x\le 10^6\), making complete precomputation feasible. After generating all such squares, each query reduces to a predecessor search.

Potential pitfalls include counting distinct prime factors rather than total multiplicity, excluding numbers with only one or more than two distinct primes, handling duplicate values if generation is done by multiple prime-power combinations, and ensuring the generated bound is \(x\le\lfloor\sqrt{10^{12}}\rfloor=10^6\). The answer is guaranteed to exist, but the search should still correctly select the largest value not exceeding \(A\).

## worker: Implement the complete Python solution using an SP
A valid number is exactly \(x^2\), where \(x\) has exactly two distinct prime factors. Since \(A \le 10^{12}\), it is enough to consider \(x \le 10^6\).

The sieve computes the smallest prime factor of every \(x\). Using
`x = p * y`, the number of distinct prime factors is derived from that of `y`. All squares corresponding to exactly two distinct factors are stored and sorted naturally during enumeration. Each query is answered with `bisect_right`.
