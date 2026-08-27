
## ideation
**Core difficulty:** For each position `i`, we must find the maximum possible GCD of a size‑`K` subset that contains `A_i`.  
**Key observation:** Any GCD `d` of such a subset must divide `A_i`. So the answer is the largest divisor `d` of `A_i` for which at least `K` numbers in the whole array are multiples of `d` (so we can fill the remaining `K‑1` slots).  
**Candidate approaches:**  
1. Naive O(N·K·something) – too slow.  
2. For each `i` iterate over all divisors of `A_i`, checking frequency of multiples – feasible because `A_i ≤ 10^6` and the number of divisors is small (≤ ~240).  
3. For each `d` pre‑compute `freq[d]` = number of array elements divisible by `d` using a sieve on the frequency array. Then query in O(number of divisors of A_i).  

**Pitfalls:**  
- `K` can be as large as `N`; we need `freq[d] ≥ K` (not `> K`).  
- `A_i` itself is guaranteed to be a multiple of `d`, so the condition automatically counts it.  
- Must handle the case where no divisor other than 1 works → answer is 1 (gcd of any set is at least 1).  
- Input size up to 1.2·10^6, values up to 10^6 → frequency array size ~1e6+1 fits in memory.  
- Divisor enumeration should be done by iterating `p` from 1 to sqrt(A_i) to generate pairs, then sorted decreasing to pick the largest valid one.  
- Use fast I/O (sys.stdin.buffer, sys.stdout.write) because of large N.

## worker: Implement the solution in Python: read input, comp
The solution uses the observation that the GCD of any K‑element subset containing A_i must be a divisor of A_i. Pre‑computing `freq[d]` = number of array elements divisible by d via a sieve on the value frequencies lets us check in O(number of divisors) per query whether we can pick K such elements. We enumerate divisors of each A_i, sort them descending, and output the first with `freq[d] >= K`. Complexity: building `freq` is O(MAXV log MAXV) ≈ 1.4·10⁷ operations, and answering N queries is O(N·√A_i) ≈ 2·10⁶, both well within limits. Memory usage is two integer arrays of size 10⁶+1 (~8 MB each). Fast I/O is used to handle N up to 1.2·10⁶.
