
## ideation
**Core difficulty** – We must count unordered triples \((A,B,C)\) taken from a set of up to \(10^6\) distinct integers (values also ≤ \(10^6\)) satisfying  
\(A < B < C\) and \(B-A = C-B\).  
Equivalently, for a fixed middle element \(B\) we need the number of unordered pairs \(\{A,C\}\subseteq S\) with \(A+C = 2B\).

A naïve double loop over all \((A,C)\) is \(O(N^2)\) and far too slow.  
The natural way to obtain all pair‑sum frequencies in sub‑quadratic time is to view the problem as a convolution of the characteristic function of \(S\) with itself:

\[
P[i] = 1 \text{ iff } i\in S,\qquad
C[s] = (P*P)[s] = \sum_{i+j=s} P[i]P[j]
\]

gives the number of **ordered** pairs \((i,j)\) whose sum is \(s\).

From \(C[2B]\) we can obtain the number of unordered pairs with sum \(2B\) by subtracting the self‑pair \((B,B)\) (which exists exactly once because \(B\in S\)) and halving:

\[
\text{unordered}(2B) = \frac{C[2B] - 1}{2}.
\]

Thus the answer is \(\sum_{B\in S} \text{unordered}(2B)\).

**Candidate approaches**

1. **FFT‑based convolution** – Build the binary array \(P\) of length \(L\) (power of two, \(L > 2\max S\)), compute the real FFT, square the spectrum, inverse FFT, round to integers.  
   - Time: \(O(L\log L) \approx 4\cdot10^7\) operations for the worst case.  
   - Memory: \(O(L) \approx 2\cdot10^6\) doubles (≈ 16 MiB).  
   - Very fast using `numpy.fft` (C implementation).

2. **Number Theoretic Transform (NTT)** – Use a modulus with a suitable primitive root (e.g., \(998244353\)) to perform an exact integer convolution.  
   - No rounding errors, but pure‑Python modular arithmetic is slower than NumPy’s FFT; may be borderline for the required size.

3. **Hash‑set / direct enumeration** – For each \(B\) iterate over possible differences \(d\) and test presence of \(B-d\) and \(B+d\). In the worst case this is \(O(N\cdot\max S)\) and too slow.

4. **Bitset convolution with bitwise tricks** – Represent \(S\) as a bitset and use bitwise AND after shifting. This is essentially the same as FFT but can be done with built‑in integers on 64‑bit words; however, the shift‑and‑AND approach would still be \(O(\max S/wordsize)\) per shift, i.e., too many shifts.

**Pitfalls / things to watch**

- **Self‑pair handling** – The ordered count \(C[2B]\) always includes the pair \((B,B)\). Must subtract it before halving, otherwise the answer would be off by \(\frac{N}{2}\).
- **Even‑sum check** – Only even sums can correspond to a valid middle element because \(2B\) is even. The formula still works; we just never look at odd indices.
- **Floating‑point rounding** – After inverse FFT, entries are floating point. Use `np.rint` (or `round`) and cast to integer before using them as counts.
- **Array size** – Must be a power of two and strictly larger than \(2\max S\) to avoid index‑out‑of‑bounds after multiplication.
- **Input size** – Up to \(10^6\) numbers; use fast I/O (`sys.stdin.buffer.read`) and possibly NumPy vectorised initialisation.
- **Output size** – Answer can be as large as \(\binom{10^6}{3}\approx 1.6\times10^{17}\); Python’s arbitrary‑precision int handles it, but intermediate `int64` arrays are sufficient.
- **Library availability** – If `numpy` is not allowed on the judge, we must fall back to a hand‑written FFT (or NTT) in pure Python, which may be slower but still feasible for \(2^{21}\) points.

## worker: finalize
- A fine triplet \((A,B,C)\) satisfies \(A<B<C\) and \(B-A=C-B\), i.e. \(B\) is the arithmetic mean of \(A\) and \(C\):
  \[
  A+C = 2B .
  \]
- For a fixed middle element \(B\) we must count unordered pairs \(\{A,C\}\subseteq S\) with sum \(2B\).
- Let \(P\) be the indicator array of the set \(S\).  The convolution \(C = P*P\) satisfies  
  \(C[s] =\) number of **ordered** pairs \((x,y)\) with \(x,y\in S\) and \(x+y=s\).
- The ordered count for sum \(2B\) includes the self‑pair \((B,B)\) exactly once.  
  Hence the number of unordered pairs with sum \(2B\) is \(\frac{C[2B]-1}{2}\).
- The convolution is computed with a real FFT (NumPy), which is fast enough for the limits
  \((N,\max S\le 10^6)\).  The FFT size is the smallest power of two greater than \(2\max S\)
  (≤ \(2^{21}\) for the worst case), giving \(O(\max S\log\max S)\) time and \(O(\max S)\) memory.
- After rounding the inverse‑FFT result we obtain exact integer counts.  
  The answer is the sum of the unordered counts for all \(B\in S\).

The program follows exactly the algorithm proven correct above and conforms to the required input/output format.
