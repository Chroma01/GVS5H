**Solution Explanation**

For a positive integer `x`

* `s(x)` – sum of its decimal digits  
* `p(x)` – product of its decimal digits  

`x` is *beautiful* iff `p(x) % s(x) == 0`.

`0 < l ≤ r < 10⁹`, therefore at most 9 decimal digits.



--------------------------------------------------------------------

#### 1.  Observations  

*If a digit `0` occurs, the product becomes `0`.  
`0` is divisible by any positive sum, therefore every number that contains
a zero digit is automatically beautiful.*

Only numbers **without** a zero digit need a real test.

* The product of a number without zeros consists only of the primes
  `2, 3, 5, 7` :

```
digit 1 : –            digit 2 : 2
digit 3 : 3            digit 4 : 2²
digit 5 : 5            digit 6 : 2·3
digit 7 : 7            digit 8 : 2³
digit 9 : 3²
```

For a digit we only have to add the corresponding prime exponents.
The maximal exponents for a 9‑digit number are  

```
e2 ≤ 3·9 = 27 ,   e3 ≤ 2·9 = 18 ,   e5 ≤ 9 ,   e7 ≤ 9
```

* For a fixed sum `s` ( `1 ≤ s ≤ 81` ) the condition  

```
p(x) divisible by s
```

means that for every prime `p ∈ {2,3,5,7}` the exponent of `p` in `p(x)`
is at least the exponent of `p` in `s`.  
If `s` contains any other prime factor (`11,13,…`) the condition can never
hold (the product has no such prime).  
So for each `s` we pre‑compute the needed exponents
`(need2, need3, need5, need7)` or mark the sum as *impossible*.



--------------------------------------------------------------------

#### 2.  Digit DP  

We count beautiful numbers `≤ X`.  
The answer for the interval `[l,r]` is  

```
count(r) – count(l‑1)
```

`count(X)` is obtained by a classic digit DP (most significant digit first).

State of the DP

```
pos            – current digit index (0 … n-1)
tight          – all already chosen digits are equal to the prefix of X
started        – have we already placed a non‑leading digit?
sum            – sum of the already placed digits   (0 … 81)
e2 , e3 , e5 , e7 – prime exponents of the product of placed digits
```

`started = False` forces `sum = 0` and all exponents `0`.

Transition for the current digit `d` ( `0 … limit` )  

```
if not started and d == 0:
        still not started, state unchanged
else:
        number has started
        if d == 0:
                product becomes 0 → the whole number is beautiful
                → we only have to count all completions of the suffix
        else:
                add d to the sum
                increase the appropriate exponents
                recurse
```

When a zero digit is placed we **do not** continue the ordinary DP.
The remaining suffix is always beautiful, therefore we count it with a
tiny auxiliary DP that knows only the position and the `tight` flag
(`zeroSeen` is irrelevant any more).

**Leaf** (`pos == n`)

```
if not started:   no number → 0
if started and zeroSeen: 1                (product = 0)
otherwise:
        look at the needed exponents for the current sum
        the number is beautiful iff all four exponents are large enough
        → 1 or 0
```

The ordinary DP has at most  

```
10 (positions) * 2 (tight) * 2 (started) *
82 (sum) * 28 * 19 * 10 * 10  < 9·10⁶
```

states, but because the sum and the exponents are tightly coupled,
the real number of reachable states is only about `10⁵`.  
The auxiliary zero‑DP has only `2·10` states.

Both DPs use memoisation (`functools.lru_cache`).  
The whole computation for a bound `X` needs far below a millisecond.

--------------------------------------------------------------------

#### 3.  Correctness Proof  

We prove that the algorithm returns the exact number of beautiful
integers in `[l,r]`.

---

##### Lemma 1  
If a positive integer contains a decimal digit `0` then it is beautiful.

**Proof.**  
The product of its digits is `0`.  
For any positive sum of digits `s` we have `0 % s = 0`. ∎



##### Lemma 2  
For a positive integer without a zero digit  
`p(x) % s(x) = 0`  **iff**  for every prime `p ∈ {2,3,5,7}` the exponent of
`p` in `p(x)` is at least the exponent of `p` in `s(x)`.

**Proof.**  
`p(x)` contains only the primes `2,3,5,7`.  
If a prime `q` different from these occurs in `s(x)`, `q` cannot divide
`p(x)` – the condition is impossible.  
Otherwise `s(x) = 2^{a₂}·3^{a₃}·5^{a₅}·7^{a₇}`.
`p(x)` is divisible by `s(x)` exactly when for each of the four primes the
exponent in `p(x)` is not smaller than the corresponding `aᵢ`. ∎



##### Lemma 3  
For a fixed sum `s (1 ≤ s ≤ 81)` the table `need[s]` built by the program
contains the correct tuple `(a₂,a₃,a₅,a₇)` or marks the sum as impossible.

**Proof.**  
The program factorises `s` by the primes `2,3,5,7`.  
If a remainder larger than `1` remains, a prime `>7` divides `s`; by Lemma 2
the condition can never hold, therefore `need[s] = None`.  
Otherwise the counted multiplicities are exactly the exponents of the
primes in the factorisation, which is the definition of the tuple. ∎



##### Lemma 4  
`dfs(pos, tight, started, sum, e2,e3,e5,e7)` (the main DP) returns the
number of beautiful integers that can be formed by filling the remaining
positions `pos … n‑1` respecting the `tight` bound and the already fixed
prefix state.

**Proof by induction on `pos` (reverse order).**

*Base (`pos = n`).*  
All digits are fixed.

* if `started` is false we have built no positive number → return `0`;
* if a zero digit has already appeared (`zeroSeen`) the product is `0`,
  the number is beautiful by Lemma 1 → return `1`;
* otherwise the number has no zero digit.
  By Lemma 2 it is beautiful exactly when the four exponents satisfy the
  condition of `need[sum]`. The program checks exactly this and returns
  `1` or `0`.  

Thus the value is correct.

*Induction step.*  
Assume the lemma true for `pos+1`.  
For the current position the program iterates over all admissible digits
`d`.  
For each digit it builds the new state exactly as the real number would do
(update `started`, possibly set a zero flag, update `sum` and the four
exponents).  
If a zero is placed the program adds the result of `zero_dp`,
which (Lemma 5) equals the number of possible suffixes that keep the whole
number beautiful.  
If no zero is placed the recursive call returns the correct number for
the suffix by the induction hypothesis.  
Summation over all possible `d` gives precisely the number of beautiful
integers that can be created from the current state. ∎



##### Lemma 5  
`zero_dp(pos, tight)` (the auxiliary DP) returns the number of ways to
fill the remaining positions `pos … n‑1` with any digits (0‑9) respecting
the `tight` bound, **given that the already built prefix already contains a
zero digit** (hence the whole number will be beautiful).

**Proof.**  
If `tight` is false we are free to choose any of the ten digits at each
remaining position, i.e. `10^{n-pos}` possibilities – the program returns
exactly this value.  
If `tight` is true the recursion enumerates the digit `d` from `0` to the
current bound, sets the new `tight` flag and adds the result for the next
position, which is exactly the definition of counting numbers ≤ the bound.
The base case `pos = n` returns `1` (one completed number). ∎



##### Lemma 6  
`count(X)` (the top‑level call of the DP) equals the number of beautiful
positive integers `≤ X`.

**Proof.**  
The call is `dfs(0, True, False, 0,0,0,0,0)`.  
All digits are still to choose, the prefix is empty, therefore `started` is
false, the sum and the exponents are `0`.  
By Lemma 4 the returned value is exactly the number of beautiful numbers
that can be built from the empty prefix under the bound `X`, i.e. the
beautiful numbers not larger than `X`. ∎



##### Lemma 7  
For any interval `[l,r] (1 ≤ l ≤ r)` the algorithm outputs the number of
beautiful integers in this interval.

**Proof.**  
`count(r)` counts all beautiful numbers `≤ r`.  
`count(l‑1)` counts all beautiful numbers `< l`.  
Their difference is precisely the number of beautiful numbers `l ≤ x ≤ r`. ∎



##### Theorem  
`beautifulNumbers(l, r)` returned by the program equals the required
answer.

**Proof.**  
By Lemma 6 `count(r)` and `count(l‑1)` are the exact counts of beautiful
numbers not larger than `r` and `l‑1`.  
Lemma 7 shows that their difference is exactly the amount of beautiful
integers in `[l,r]`. ∎



--------------------------------------------------------------------

#### 4.  Complexity Analysis  

`n = number of decimal digits of X ≤ 9`

*Number of different states of the main DP*  

```
positions : n
tight     : 2
started   : 2
sum       : 0 … 81          (82 values)
e2        : 0 … 27
e3        : 0 … 18
e5 , e7   : 0 … 9
```

The reachable states are far fewer – only about `10⁵`.  
For each state we try at most `10` digits.

```
Time   :  O(number of reachable states)  < 2·10⁶ operations
Memory :  O(number of reachable states)  < 1 MB
```

Both limits are easily satisfied for the given constraints.



--------------------------------------------------------------------

#### 5.  Reference Implementation  (Python 3)

```python
import sys
from functools import lru_cache

# ------------------------------------------------------------
# pre‑compute the exponent requirements for every possible sum
MAX_SUM = 81                     # 9 * 9
need = [None] * (MAX_SUM + 1)   # need[s] = (a2,a3,a5,a7)  or  None
for s in range(1, MAX_SUM + 1):
    a2 = a3 = a5 = a7 = 0
    t = s
    possible = True
    for p in (2, 3, 5, 7):
        while t % p == 0:
            if p == 2:
                a2 += 1
            elif p == 3:
                a3 += 1
            elif p == 5:
                a5 += 1
            else:               # p == 7
                a7 += 1
            t //= p
    if t != 1:                 # a prime > 7 divides s
        possible = False
    if possible:
        need[s] = (a2, a3, a5, a7)
    # else need[s] stays None  → sum can never be reached
# ------------------------------------------------------------

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        """return count of beautiful numbers in [l, r] (inclusive)"""

        # ------------------------------------------------
        # count of beautiful numbers in [1, X]
        # ------------------------------------------------
        def count_upto(X: int) -> int:
            if X <= 0:
                return 0
            digits = list(map(int, str(X)))
            n = len(digits)

            # ---------- DP for the case "already contains a zero" ----------
            @lru_cache(maxsize=None)
            def zero_dp(pos: int, tight: bool) -> int:
                """count of completions of the suffix when a zero already appeared"""
                if pos == n:
                    return 1                     # one finished number
                if not tight:
                    # any digit 0..9 for each remaining position
                    return pow(10, n - pos)
                limit = digits[pos]
                total = 0
                for d in range(limit + 1):
                    ntight = tight and (d == limit)
                    total += zero_dp(pos + 1, ntight)
                return total

            # ---------- main DP ----------
            @lru_cache(maxsize=None)
            def dfs(pos: int, tight: bool, started: bool,
                    s: int, e2: int, e3: int, e5: int, e7: int) -> int:
                """count of beautiful numbers that can be built from the current state"""
                if pos == n:
                    if not started:
                        return 0                # no positive number
                    # product is zero → automatically beautiful
                    if s == 0:                  # actually s > 0 here
                        return 0
                    req = need[s]
                    if req is None:
                        return 0
                    a2, a3, a5, a7 = req
                    return 1 if (e2 >= a2 and e3 >= a3 and
                                 e5 >= a5 and e7 >= a7) else 0

                limit = digits[pos] if tight else 9
                total = 0
                for d in range(limit + 1):
                    ntight = tight and (d == limit)
                    if not started and d == 0:
                        # still only leading zeros
                        total += dfs(pos + 1, ntight, False,
                                     0, 0, 0, 0, 0)
                    else:
                        # number has started (or starts now)
                        if d == 0:
                            # a zero digit → product becomes 0 → beautiful for sure
                            total += zero_dp(pos + 1, ntight)
                        else:
                            ns = s + d
                            ne2, ne3, ne5, ne7 = e2, e3, e5, e7
                            if d == 2:
                                ne2 += 1
                            elif d == 3:
                                ne3 += 1
                            elif d == 4:
                                ne2 += 2
                            elif d == 5:
                                ne5 += 1
                            elif d == 6:
                                ne2 += 1
                                ne3 += 1
                            elif d == 7:
                                ne7 += 1
                            elif d == 8:
                                ne2 += 3
                            elif d == 9:
                                ne3 += 2
                            # digit 1 changes nothing
                            total += dfs(pos + 1, ntight, True,
                                         ns, ne2, ne3, ne5, ne7)
                return total

            # start with empty prefix
            return dfs(0, True, False, 0, 0, 0, 0, 0)

        # ---------------------------------------------------------
        return count_upto(r) - count_upto(l - 1)
```

The program follows exactly the algorithm proven correct above
and conforms to the required function signature.