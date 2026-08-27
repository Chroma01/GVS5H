**Solution Explanation**

For every cell we may apply two kinds of flips  

* flip a whole row   – toggles all `W` bits in that row  
* flip a whole column – toggles one bit in every row  

The order of the flips does not matter, only whether each row and each
column is flipped an odd number of times.
Let  

* `r_i ∈ {0,1}` – *1* means row `i` is flipped  
* `c_j ∈ {0,1}` – *1* means column `j` is flipped  

The final value in cell `(i , j)` is  

```
A[i][j] xor r_i xor c_j
```

For a fixed column mask `C = (c_1 … c_W)` (as a bit mask) the whole grid
looks like

```
(A_i xor C)       (row i, before possible row flip)
```

If we also flip row `i` we xor the whole row with the all‑ones mask
`FULL = (1<<W)-1`.  
The number of `1`s in a row `i` after column flips is

```
p_i(C) = popcount( A_i xor C )
```

Flipping the row changes this number to `W - p_i(C)`.  
For this row we can choose the better of the two, therefore its
contribution to the total sum is

```
f_i(C) = min( p_i(C) , W - p_i(C) )
```

The whole answer is

```
answer = min over all C ( Σ_i f_i(C) )
```

--------------------------------------------------------------------

#### 1.   Reformulation as a XOR‑convolution

Define a function on masks

```
f(mask) = min( popcount(mask) , W - popcount(mask) )
```

For a row whose original mask is `M`

```
f_i(C) = f( M xor C )
```

If we know for every possible mask `M` how many rows have exactly this
mask, i.e. a frequency array

```
freq[M] = #{ i | A_i = M }          (0 ≤ M < 2^W)
```

then

```
total(C) = Σ_M freq[M] * f( M xor C )
```

The right hand side is exactly the **XOR‑convolution** of the two
arrays `freq` and `f`.  
For a convolution of size `N = 2^W` the Fast Walsh–Hadamard Transform
(FWHT) evaluates it in `O(N log N)`.

--------------------------------------------------------------------

#### 2.   Algorithm
```
read H, W
N = 1 << W
freq[0…N-1] = 0
for each row:
        read string s
        mask = integer represented by s
        freq[mask] += 1

f[mask] = min( mask.bit_count() , W - mask.bit_count() )

# XOR‑convolution of freq and f
A = freq (copy)
B = f
FWHT(A)          # in‑place transform
FWHT(B)
for i = 0 … N-1:
        A[i] = A[i] * B[i]
FWHT(A)          # inverse transform (same routine)
for i = 0 … N-1:
        A[i] //= N          # divide by the size of the transform

answer = min_i A[i]
print answer
```

`FWHT` (forward transform) works on an array `a` of length `N` (a power
of two) :

```
step = 1
while step < N:
        for i in range(0, N, step*2):
                for j in range(i, i+step):
                        u = a[j]
                        v = a[j+step]
                        a[j]   = u + v
                        a[j+step] = u - v
        step <<= 1
```

The inverse transform is the same code; after it we divide every entry
by `N`.

--------------------------------------------------------------------

#### 3.   Correctness Proof  

We prove that the algorithm outputs the minimal possible sum.

---

##### Lemma 1  
For a fixed column mask `C` and a row with original mask `M`,
the minimal contribution of this row after arbitrary row flips equals  
`f(M xor C) = min(popcount(M xor C), W - popcount(M xor C))`.

**Proof.**  
After applying the column mask the row becomes `M xor C`.  
If we do not flip the row, the number of `1`s is `popcount(M xor C)`.  
If we flip the row, every bit toggles, turning the number of `1`s into
`W - popcount(M xor C)`.  
We may choose whichever is smaller, which is exactly `f(M xor C)`. ∎



##### Lemma 2  
For a fixed column mask `C` the total sum over all rows equals  

```
total(C) = Σ_M freq[M] * f(M xor C)
```

**Proof.**  
Group rows by their original mask `M`.  
All rows with the same `M` have the same contribution `f(M xor C)` by
Lemma&nbsp;1, and there are `freq[M]` of them. Summation over all `M`
gives the formula. ∎



##### Lemma 3  
Let `A` and `B` be two arrays of length `N = 2^W`.  
The XOR‑convolution `C` defined by  

```
C[t] = Σ_x A[x] * B[t xor x]   for all t
```

is computed by the FWHT procedure described above.

**Proof.**  
The FWHT is the matrix of the Walsh–Hadamard transform.
It diagonalises the XOR‑convolution: if `Â = FWHT(A)` and `B̂ = FWHT(B)`,
then `Ĉ = Â ∘ B̂` (pointwise product), and the inverse transform
recovers `C`. This is a standard property of the Walsh–Hadamard
transform. ∎



##### Lemma 4  
After the three FWHT steps and the final division by `N`,
the array `A` produced by the algorithm satisfies  

```
A[t] = total(C = t)   for every t ∈ [0, N)
```

**Proof.**  
Initially `A = freq`, `B = f`.  
The first two transforms give their Walsh–Hadamard representations.
Pointwise multiplication yields `Ĉ[t] = freq̂[t] * f̂[t]`.  
By Lemma&nbsp;3 the inverse transform of `Ĉ` equals the XOR‑convolution
of `freq` and `f`, i.e. the array `C` with  

```
C[t] = Σ_M freq[M] * f(M xor t)
```

which is exactly `total(t)` by Lemma&nbsp;2.  
Finally we divide by `N`, which is the normalisation required for the
inverse Walsh–Hadamard transform, obtaining integer values `A[t]`. ∎



##### Lemma 5  
`answer = min_{C} total(C) = min_i A[i]` where `A` is the array after the
algorithm.

**Proof.**  
By Lemma&nbsp;4 each `A[i]` equals `total(i)`. The minimum of the set
`{ total(i) | 0 ≤ i < N }` is therefore the minimum entry of `A`. ∎



##### Theorem  
The algorithm outputs the minimum possible value of  

```
 Σ_{i=1..H} Σ_{j=1..W} A_{i,j}
```

after any sequence of allowed operations.

**Proof.**  

* For any choice of column flips `C` the optimal choice of row flips
  yields a total sum `total(C)` (Lemma&nbsp;2).  
* The algorithm computes `total(C)` for **all** `C` (Lemma&nbsp;4).  
* The minimal achievable sum is `min_C total(C)`, which the algorithm
  returns as `min_i A[i]` (Lemma&nbsp;5).  

Thus the printed number equals the optimum. ∎



--------------------------------------------------------------------

#### 4.   Complexity Analysis  

*Reading input* : `O(H·W)` (just to convert strings to masks)  
*FWHT*          : `O(N log N)` where `N = 2^W ≤ 262 144`  
                 → at most `N·W ≤ 4.7·10⁶` elementary operations.  

Memory consumption: two integer arrays of length `N` → `O(N)`  
(≈ 2·262 144 integers, well below the limits).

Both time and memory easily satisfy the constraints (`H ≤ 2·10⁵`,
`W ≤ 18`).

--------------------------------------------------------------------

#### 5.   Reference Implementation  (Python 3)

```python
import sys

def fwht(a):
    """In‑place Fast Walsh–Hadamard Transform (XOR version)."""
    n = len(a)
    step = 1
    while step < n:
        for i in range(0, n, step * 2):
            for j in range(i, i + step):
                u = a[j]
                v = a[j + step]
                a[j] = u + v
                a[j + step] = u - v
        step <<= 1

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    N = 1 << W

    freq = [0] * N
    for _ in range(H):
        s = next(it)
        mask = 0
        # column j (0‑based) corresponds to bit (1 << j)
        for j, ch in enumerate(s):
            if ch == '1':
                mask |= 1 << j
        freq[mask] += 1

    # f[mask] = min(popcount(mask), W - popcount(mask))
    f = [0] * N
    for mask in range(N):
        p = mask.bit_count()
        f[mask] = p if p <= W - p else W - p

    # XOR‑convolution of freq and f via FWHT
    a = freq[:]          # copy
    b = f[:]
    fwht(a)
    fwht(b)
    for i in range(N):
        a[i] = a[i] * b[i]
    fwht(a)              # inverse transform (same routine)
    n_inv = N
    for i in range(N):
        a[i] //= n_inv    # normalisation

    ans = min(a)
    print(ans)

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.