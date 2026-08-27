
## ideation
**Core difficulty** – Efficiently answering up to 2·10⁵ queries (each A ≤ 10¹²) for the largest integer ≤ A that has exactly two distinct prime factors, each with an even exponent.

**Key observation**  
A 400‑number is a perfect square whose square root has exactly two distinct prime factors:
```
N = m² ,  ω(m) = 2            (ω = number of distinct primes)
```
Because A ≤ 10¹², we have m ≤ √10¹² = 10⁶. So all candidate squares come from m in [2, 10⁶].

**Candidate approaches**
1. **Pre‑compute all m with ω(m)=2 (≤10⁶) and store m²**  
   – Use a linear/Euler sieve to obtain the distinct‑prime count for every integer ≤10⁶ in O(N) time.  
   – Build a sorted list `ans` of all squares `m²` where the count equals 2.  
   – For each query perform a binary search (`bisect_right`) to get the largest element ≤ A.

2. **Generate numbers directly from primes**  
   Enumerate all pairs of distinct primes p<q and all positive even exponents a,b with p^{2a}·q^{2b} ≤ 10¹².  
   – Too many combinations (≈10⁵ primes → O(10¹⁰) pairs) – infeasible.

3. **Factor each A on the fly**  
   For each query factor A, find the largest square ≤ A with two primes.  
   – Factoring up to 10¹² repeatedly is far too slow for 2·10⁵ queries.

Hence approach 1 is the only viable one.

**Pitfalls & details to watch**
- **Correctness of the sieve** – Must count *distinct* primes, not total exponents. The linear sieve variant that stops after the first prime factor of i gives exactly that.
- **Range limits** – m starts at 2 (m=1 has 0 distinct primes). The smallest 400‑number is 2²·3² = 36, guaranteeing an answer for the minimal A=36.
- **Binary search** – Use `bisect_right(ans, A) - 1` to obtain the last element ≤ A. Ensure the list is sorted (it is, because m grows).
- **Memory** – Storing `cnt` as a Python list of ints (~28 MiB) is acceptable, but a `bytearray` or `array('b')` would be more compact. Either fits typical limits.
- **Overflow** – In Python, `m*m` is safe (unbounded integer). Ensure the sieve upper bound is `10⁶`.
- **Time** – O(10⁶) sieve + O(Q·log|ans|) ≈ O(10⁶ + 2·10⁵·18) easily within limits.

## worker: finalize
The problem asks for the largest integer ≤ A that has exactly two distinct prime factors, each occurring with an even exponent. Such a number is a perfect square whose square root has exactly two distinct prime factors:

```
N = m²  with  ω(m) = 2
```

Since A ≤ 10¹², we have m ≤ √10¹² = 10⁶. Therefore all candidate numbers are of the form m² with 2 ≤ m ≤ 10⁶ and ω(m)=2.

We compute ω(m) for all m up to 10⁶ using a linear (Euler) sieve. The sieve runs in O(MAX) time and also stores the smallest prime factor of each number; from that we derive the count of distinct prime factors.

After the sieve we iterate over all m and collect m² whenever cnt[m] == 2. The resulting list `ans` is sorted in increasing order and contains every 400‑number ≤ 10¹².

For each query we perform a binary search (`bisect_right`) on `ans` to find the greatest element ≤ A, which is the required answer.

Complexity:
- Precomputation: O(10⁶) time, O(10⁶) memory.
- Each query: O(log |ans|) ≤ O(log 2·10⁵) time.
- Total time: O(10⁶ + Q · log 2·10⁵) ≤ about 4 · 10⁶ operations, well within limits.
- Memory: about 30 MiB.

The implementation follows exactly this plan and handles all edge cases (the smallest 400‑number is 36, and an answer always exists for the given A).
