
## ideation
- For each index i we must choose K numbers from the whole array that include A_i and maximize their GCD.
- Any GCD of a set that contains A_i must be a divisor of A_i.  
  Hence the answer for i is the **largest divisor d of A_i such that at least K elements of the whole array are divisible by d**.
- So the problem reduces to two sub‑problems:  
  1. For every possible d (1 … max A) compute `cnt[d] =` how many array elements are multiples of d.  
  2. For each value v, find the largest divisor d of v with `cnt[d] ≥ K`.
- Computing `cnt` can be done with a classic divisor‑sieve:  
  `cnt[d] = Σ freq[m]` over all multiples m of d, where `freq[x]` is the frequency of value x in the array.
- After we know which d are “good” (`cnt[d] ≥ K`), we can fill the answer for every value in a second sieve that scans d **from large to small**.  
  When we encounter a good d we assign `ans[m] = d` for each multiple m that has not been assigned yet. Because we go downward, the first assignment is the maximal good divisor.
- The final answer for index i is simply `ans[A_i]`.

**Key points / pitfalls**
- N and max A are up to 1.2·10⁶ and 10⁶ respectively → O(M log M) (M = max A) is fast enough.
- Need fast I/O (`sys.stdin.buffer`) and efficient output (`'\n'.join(...)`).
- Memory: storing three plain Python lists of length ≈ 10⁶ would be heavy (≈ 100 MB).  
  Use `array('I', …)` (unsigned 32‑bit) for `freq`, `cnt`, and `ans` – only a few megabytes.
- `cnt[1] = N` is always ≥ K, guaranteeing that every value gets an answer (at least 1).
- K = 1 → answer is the element itself; K = N → answer is the GCD of the whole array. Both are handled automatically.
- Descending scan ensures the assigned divisor is maximal; an element gets its answer only once.
