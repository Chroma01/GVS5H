**Solution Explanation**

For a positive integer `N`

* `N` has exactly two different prime factors
* every prime factor occurs with an even exponent  

```
N = p^(2a) · q^(2b)      ( p , q are different primes , a , b ≥ 1 )
```

Therefore `N` is a perfect square and its square root has exactly two
different prime factors.

```
N is a 400 number   ⇔   N = m²  with  ω(m) = 2               (1)
```

`ω(m)` – number of distinct prime factors of `m`.

The maximal value of `A` is `10¹²`, consequently `m ≤ √10¹² = 10⁶`.
So we only have to know all `m ( 2 ≤ m ≤ 10⁶ )` with `ω(m) = 2`.

--------------------------------------------------------------------

#### 1.   Counting distinct prime factors for all numbers ≤ 10⁶  

A linear sieve (also called “Euler sieve”) gives the smallest prime
factor of every number and, at the same time, the number of distinct
prime factors.

```
cnt[i]  – number of distinct prime factors of i
primes  – list of primes in increasing order
```

```
cnt = array[0…MAX] filled with 0
primes = empty

for i = 2 … MAX
        if cnt[i] == 0               # i is prime
                cnt[i] = 1
                primes.append(i)

        for p in primes
                if i*p > MAX: break
                if i % p == 0:                # p already divides i
                        cnt[i*p] = cnt[i]     # same set of primes
                        break
                else:
                        cnt[i*p] = cnt[i] + 1 # new prime p appears
```

* each composite is generated exactly once,
* the inner loop stops after the first prime that divides `i`,
  therefore the total work is `O(MAX)`.

`MAX = 1 000 000`.  
After the sieve `cnt[m]` is known for every `m`.

--------------------------------------------------------------------

#### 2.   Build the list of all 400 numbers

```
ans = []
for m = 2 … MAX
        if cnt[m] == 2:                # exactly two distinct primes
                ans.append( m * m )     # N = m²
```

`ans` is automatically sorted because `m` grows.
The size of `ans` is about `2·10⁵` (≈ 19 % of the numbers up to `10⁶`).

--------------------------------------------------------------------

#### 3.   Answer a query  

For a given `A` we need the largest element of `ans` not larger than `A`.

```
idx = bisect_right(ans, A) - 1
print( ans[idx] )
```

`bisect_right` works in `O(log |ans|)` (`|ans| ≈ 2·10⁵`).

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm prints the required answer for every query.

---

##### Lemma 1  
A positive integer `N` is a 400 number **iff** `N = m²` with `ω(m)=2`.

**Proof.**  
*If* `N` is a 400 number, each prime exponent in `N` is even,
hence `N` is a perfect square: `N = m²`.  
`N` has exactly two different primes, therefore `m` also has exactly
those two primes, i.e. `ω(m)=2`.

*Only‑if* part: let `N = m²` and `ω(m)=2`.  
All prime exponents of `N` are twice the exponents of `m`, therefore
even. The two different primes of `m` are the only primes of `N`. ∎



##### Lemma 2  
After the linear sieve finishes, for every integer `x (1 ≤ x ≤ MAX)`
`cnt[x] = ω(x)` (the number of distinct prime factors of `x`).

**Proof.**  
Induction over `x`.

*Base* `x = 2` : `cnt[2]` is set to `1`, and `ω(2)=1`.

*Induction step.*  
Assume the statement true for all numbers `< x`.  
If `x` is prime, the outer `if` makes `cnt[x]=1`, which equals `ω(x)`.  
Otherwise `x` is composite and is written as `x = i·p` where `p` is the
smallest prime factor of `x`. The inner loop reaches this `p` while
processing `i` (because all smaller primes have already been tried).
Two cases:

* `i % p == 0` – `p` already divides `i`, thus the set of prime factors
  of `x` equals the set of prime factors of `i`.  
  The algorithm stores `cnt[x] = cnt[i] = ω(i) = ω(x)`.

* `i % p != 0` – `p` is a new prime, therefore `ω(x) = ω(i)+1`.  
  The algorithm stores `cnt[x] = cnt[i] + 1 = ω(i)+1 = ω(x)`.

Thus the invariant holds for all `x`. ∎



##### Lemma 3  
`ans` contains **all** 400 numbers not larger than `10¹²` and only them.

**Proof.**  
By Lemma&nbsp;1 a 400 number `N ≤ 10¹²` is `N = m²` with `ω(m)=2` and
`m ≤ √10¹² = 10⁶`.  
The construction of `ans` iterates over all `m` in this range,
checks `cnt[m]==2`. By Lemma&nbsp;2 this condition is equivalent to
`ω(m)=2`. For each such `m` the value `m²` is appended.
Hence every 400 number appears in `ans`, and nothing else is added. ∎



##### Lemma 4  
For any query value `A` the algorithm outputs the largest element of
`ans` that does not exceed `A`.

**Proof.**  
`bisect_right(ans, A)` returns the first index `k` such that
`ans[k] > A`. Therefore `k-1` is the last index with `ans[k-1] ≤ A`.
The algorithm prints `ans[k-1]`, which is exactly the largest element
≤ `A`. ∎



##### Theorem  
For every query the program prints the largest 400 number not exceeding
the given `A`.

**Proof.**  
By Lemma&nbsp;3 the set `ans` equals the set of all 400 numbers ≤ `10¹²`.  
By Lemma&nbsp;4 the program returns the greatest element of this set
that is ≤ `A`. Consequently the printed number is precisely the required
largest 400 number not exceeding `A`. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

*Precomputation*  

* linear sieve up to `10⁶` : `O(10⁶)` time, `O(10⁶)` memory  
* building `ans`          : `O(10⁶)` time, `≈ 2·10⁵` integers stored  

*Answering queries*  

* one binary search per query: `O(log |ans|) ≤ O(log 2·10⁵) ≤ 18`  
  total `O(Q log |ans|)`  

Overall  

```
Time   :  O(10⁶ + Q·log 2·10⁵)   ≤  about 4·10⁶ operations
Memory :  O(10⁶)  (≈ 20 MiB)
```

Both easily satisfy the limits (`Q ≤ 2·10⁵`).

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys
import bisect

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    Q = int(data[0])
    A_list = list(map(int, data[1:]))

    MAX_M = 10 ** 6                     # because (10^6)^2 = 10^12

    # ---------- 1. linear sieve, count distinct prime factors ----------
    cnt = [0] * (MAX_M + 1)            # cnt[x] = ω(x)
    primes = []

    for i in range(2, MAX_M + 1):
        if cnt[i] == 0:                # i is prime
            cnt[i] = 1
            primes.append(i)

        for p in primes:
            ip = i * p
            if ip > MAX_M:
                break
            if i % p == 0:              # p already present in i
                cnt[ip] = cnt[i]
                break                   # smallest prime factor reached
            else:
                cnt[ip] = cnt[i] + 1    # new prime p appears

    # ---------- 2. build list of all 400 numbers ----------
    ans = []
    for m in range(2, MAX_M + 1):
        if cnt[m] == 2:                 # exactly two distinct primes
            ans.append(m * m)          # N = m²

    # ---------- 3. answer the queries ----------
    out_lines = []
    for A in A_list:
        idx = bisect.bisect_right(ans, A) - 1
        out_lines.append(str(ans[idx]))

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input and output format.