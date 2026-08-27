**Solution Explanation**

For three different numbers  

```
A < B < C ,   B‑A = C‑B
```

`B` is the arithmetic mean of `A` and `C`

```
B = (A + C) / 2
```

So a *fine triplet* is exactly a triple `(A , B , C)` taken from the given set `S`
such that  

* `A` and `C` are different,
* `A + C = 2·B`,
* `B` also belongs to `S`.

--------------------------------------------------------------------

#### 1.   Reformulation

For a fixed middle element `B` we have to count unordered pairs `{A , C}`
with `A , C ∈ S , A ≠ C` and `A + C = 2·B`.

If we know, for every possible sum `s`, how many **ordered** pairs
`(x , y)` from `S` satisfy `x + y = s`,
the required number of unordered pairs is easy to obtain:

```
unordered(s) = (ordered(s) – self(s)) / 2
```

`self(s)` is `1` if `s/2` is contained in `S` (the pair `(s/2 , s/2)`),
otherwise `0`.  
Division by `2` removes the double counting of `(x , y)` and `(y , x)`.

Therefore

```
answer = Σ_{B∈S} unordered(2·B)
       = Σ_{B∈S} ( ordered(2·B) – 1 ) / 2
```

The whole problem is reduced to obtaining `ordered(s)` for all sums `s`.

--------------------------------------------------------------------

#### 2.   Ordered pair counts = convolution  

Create a binary array  

```
P[i] = 1   if i ∈ S
     = 0   otherwise          (0 ≤ i ≤ MAX,  MAX = max(S))
```

The convolution `C = P * P` (ordinary polynomial multiplication) satisfies

```
C[s] = Σ_{i + j = s} P[i]·P[j]   =   number of ordered pairs (i , j) with sum s
```

So `ordered(s)` is exactly `C[s]`.

`MAX ≤ 10⁶`, therefore `s` never exceeds `2·MAX ≤ 2·10⁶`.  
The convolution of two length‑`MAX+1` arrays can be computed with an FFT
in `O( MAX log MAX )` time, easily fast enough.

--------------------------------------------------------------------

#### 3.   Algorithm
```
read N and the N numbers S
MAX = max(S)

# length of the FFT (power of two > 2·MAX)
L = 1
while L <= 2·MAX:   L <<= 1

make a float array A of length L, fill A[i] = 1 if i ∈ S else 0

F = FFT(A)                         # complex spectrum
C = inverse_FFT( F * F )           # convolution, real part only
round each entry of C to the nearest integer   (now C[s] = ordered(s))

ans = 0
for each value v in S:
        s = 2·v
        unordered = (C[s] - 1) // 2   # (ordered – self) / 2, self = 1
        ans += unordered

print ans
```

All arithmetic fits into 64‑bit (`C[s] ≤ |S| ≤ 10⁶`), and Python integers can
hold the final result (`≈ 2·10¹¹` in the worst case).

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm outputs the number of fine triplets.

---

##### Lemma 1  
For every integer `s` the value `C[s]` obtained after the inverse FFT
equals the number of ordered pairs `(x , y)` with `x , y ∈ S` and `x + y = s`.

**Proof.**  
`P[i]` is defined as the indicator of the set `S`.  
The (linear) convolution of `P` with itself is

```
(P*P)[s] = Σ_{i+j=s} P[i]·P[j] .
```

Each term is `1` exactly when both `i` and `j` belong to `S`, otherwise `0`.  
Hence the sum counts precisely the ordered pairs `(i , j)` with sum `s`.  
FFT computes the convolution exactly (up to tiny rounding errors),
which we eliminate by rounding to the nearest integer. ∎



##### Lemma 2  
For any `B ∈ S`

```
unordered(2·B) = ( C[2·B] – 1 ) / 2 .
```

**Proof.**  
`C[2·B]` counts ordered pairs `(x , y)` with `x + y = 2·B`.  
If `x = y = B` then the ordered pair `(B , B)` is counted once,
otherwise each unordered pair `{x , y}` (`x ≠ y`) contributes two ordered
pairs `(x , y)` and `(y , x)`.  
Since `B ∈ S`, the self‑pair exists exactly once, i.e. `self = 1`.  
Therefore  

```
unordered(2·B) = ( C[2·B] – 1 ) / 2 .
``` ∎



##### Lemma 3  
For a fixed `B ∈ S` the algorithm adds exactly the number of fine
triplets whose middle element is `B`.

**Proof.**  
A fine triplet `(A , B , C)` must satisfy `A + C = 2·B` and
`A , C ∈ S , A < C`.  
All such unordered pairs `{A , C}` are counted by `unordered(2·B)`.  
By Lemma&nbsp;2 the algorithm adds precisely this number.
∎



##### Lemma 4  
Every fine triplet of `S` is counted exactly once by the algorithm.

**Proof.**  
Let `(A , B , C)` be any fine triplet.  
Its middle element `B` belongs to `S`, and the algorithm processes `B`
once.  
Because `A + C = 2·B`, the unordered pair `{A , C}` belongs to the set
counted by `unordered(2·B)`, so the triple contributes `1` to the sum
added for `B`.  
No other `B' ≠ B` can generate this triple, because the middle element is
unique. ∎



##### Theorem  
The value printed by the algorithm equals the number of fine triplets
`(A , B , C)` with `A , B , C ∈ S` and `A < B < C`.

**Proof.**  
By Lemma&nbsp;3, for each `B ∈ S` the algorithm adds the exact number of
fine triplets with middle element `B`.  
Lemma&nbsp;4 shows that every fine triplet is counted once and only once.
Summation over all `B` therefore yields the total number of fine
triplets, which the algorithm outputs. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

*`MAX = max(S) ≤ 10⁶`*

* FFT size `L` is the smallest power of two with `L > 2·MAX`  
  (`L ≤ 2²¹ = 2 097 152`).
* FFT and inverse FFT: `O(L log L)` time, `O(L)` memory.
* Building the binary array and the final summation: `O(N)` time,
  `O(N)` extra memory (the input list).

Overall  

```
Time   :  O( MAX log MAX )   ≤ 2·10⁶·21  ≈ 4·10⁷ elementary operations
Memory :  O( MAX )           ≤ 2·10⁶  numbers  (≈ 16 MiB)
```

Both easily satisfy the limits.

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys
import numpy as np

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    S = [int(next(it)) for _ in range(n)]

    max_val = max(S)

    # length of FFT (power of two > 2*max_val)
    size = 1
    while size <= max_val * 2:
        size <<= 1

    # binary characteristic array
    arr = np.zeros(size, dtype=np.float64)
    for v in S:
        arr[v] = 1.0

    # convolution via FFT
    spectrum = np.fft.rfft(arr)                 # forward FFT (real)
    conv = np.fft.irfft(spectrum * spectrum, n=size)  # inverse FFT
    conv = np.rint(conv).astype(np.int64)       # round to nearest integer

    # count fine triplets
    ans = 0
    for v in S:
        s = v * 2
        # ordered pairs for sum s : conv[s]
        # self pair (v, v) exists exactly once, so subtract 1 and halve
        unordered = (int(conv[s]) - 1) // 2
        ans += unordered

    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input / output format.