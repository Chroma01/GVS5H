
## ideation
**Solution Explanation**

For every food we know

* its vitamin `V` (`1,2` or `3`)
* how many units `A` of this vitamin it contains
* how many calories `C` it costs

We may choose any subset of the foods, the total calories may not exceed `X`.
For a chosen subset let  

```
total1 = sum of A of the chosen foods with V = 1
total2 = sum of A of the chosen foods with V = 2
total3 = sum of A of the chosen foods with V = 3
```

The value of the subset is `min(total1,total2,total3)`.  
We have to make this value as large as possible.



--------------------------------------------------------------------

#### 1.   Independence of the three vitamins  

A food never gives two different vitamins, therefore the three groups are
*independent* – a food belonging to vitamin 1 never influences the amount of
vitamin 2 or 3.  
Consequently, for a fixed number `t`

```
t is attainable  ⇔  we can obtain at least t units of vitamin 1
                     and at least t units of vitamin 2
                     and at least t units of vitamin 3,
                     using together at most X calories
```

If for a vitamin we know the **minimum calories** needed to obtain at least
`t` units, then `t` is attainable iff the sum of the three minima does not
exceed `X`.

--------------------------------------------------------------------

#### 2.   Minimum calories for one vitamin – 0/1 knapsack  

For a single vitamin we have a classic 0/1 knapsack:

* weight   = calories `C`
* value    = vitamin amount `A`
* capacity = `X`

`dp[c]` – the maximum amount of this vitamin that can be taken with exactly
`c` calories (`c = 0 … X`).  
Initialisation: `dp[0]=0`, all other entries = “unreachable”.
Transition (process each food once, iterate `c` backwards)

```
for each food (a , c):
        for weight from X down to c:
                if dp[weight-c] reachable:
                        dp[weight] = max(dp[weight] , dp[weight-c] + a)
```

After processing all foods we turn the table into a *prefix* maximum:
`best[c] = max value reachable with at most c calories`.

Now for any required amount `t`

```
min_calories(t) = the smallest c (0 ≤ c ≤ X) with best[c] ≥ t
```

If no such `c` exists the needed amount is impossible.

The table size is only `X+1 ≤ 5001`, therefore the whole DP for one
vitamin needs `O(N·X)` operations, at most `5·10³·5·10³ = 2.5·10⁷`.  
The three vitamins together also need at most `2.5·10⁷` updates – easily fast
enough in Python.

--------------------------------------------------------------------

#### 3.   Searching the answer  

`answer` is the largest feasible `t`.  
The obvious upper bound is the total amount of each vitamin:

```
upper = min( sum of A for V=1 , sum of A for V=2 , sum of A for V=3 )
```

`answer` lies in `[0 , upper]`.  
We binary‑search this interval.  
For a middle value `mid` we compute the three minima
`c1, c2, c3` with the tables described above and test

```
c1 + c2 + c3 ≤ X   ?
```

If yes, `mid` is feasible and we try larger values,
otherwise we try smaller ones.
Each test needs only a linear scan over at most `X+1` entries,
so the binary search adds at most `log₂(upper) ≤ 31` such scans –
negligible compared to the DP.

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm outputs the maximum possible value of the
minimum vitamin intake.

---

##### Lemma 1  
For a fixed vitamin `v` and any non‑negative integer `t`,
`min_calories_v(t)` computed by the DP equals the minimum total calories
required to obtain at least `t` units of vitamin `v`.

**Proof.**  
The DP is the standard 0/1 knapsack DP for *maximum* value with a given
weight limit.  
`best_v[c]` after the prefix step is the maximum amount of vitamin `v`
obtainable with **at most** `c` calories.  
Therefore the smallest `c` with `best_v[c] ≥ t` is exactly the minimum
calories sufficient to reach `t`. ∎



##### Lemma 2  
For any integer `t` the following are equivalent  

* (a) there exists a subset of foods with total calories ≤ `X`
      and each vitamin amount ≥ `t`;
* (b) `min_calories_1(t) + min_calories_2(t) + min_calories_3(t) ≤ X`.

**Proof.**  

* (a) ⇒ (b):  
  Take the subset from (a). For each vitamin `v` the calories spent on
  foods of type `v` is at least the minimum needed to reach `t`,
  i.e. at least `min_calories_v(t)`. Summing over the three vitamins gives
  a total ≤ `X`, therefore the sum of the three minima is ≤ `X`.

* (b) ⇒ (a):  
  For each vitamin `v` choose a concrete subset of its foods that uses
  exactly `min_calories_v(t)` calories and gives at least `t` units
  (the existence follows from Lemma&nbsp;1).  
  The three subsets are disjoint, their total calories are the sum of the
  three minima, which by assumption does not exceed `X`.  
  Hence the union of the three subsets satisfies (a). ∎



##### Lemma 3  
For any integer `t` the procedure `feasible(t)` used in the binary search
returns *True* exactly when condition (b) of Lemma&nbsp;2 holds.

**Proof.**  
`feasible(t)` computes, for each vitamin `v`, the smallest weight `c`
with `best_v[c] ≥ t`. By Lemma&nbsp;1 this `c` equals
`min_calories_v(t)`. The procedure then checks whether the sum of the three
found weights does not exceed `X`. This is precisely condition (b). ∎



##### Lemma 4  
Let `T` be the value printed by the algorithm. Then `T` is feasible,
and no integer `t > T` is feasible.

**Proof.**  
The binary search maintains the invariant  

```
all values ≤ lo are feasible,
all values > hi are infeasible.
```

Initially `lo = 0` (feasible) and `hi = upper` (infeasible if any larger
value existed).  
In each iteration the middle `mid` is tested by `feasible(mid)`.
By Lemma&nbsp;3 the test is correct, therefore the invariant is preserved.
When the loop ends `lo = hi = T`. By the invariant, `T` is feasible and
every larger integer is infeasible. ∎



##### Lemma 5  
The value `T` printed by the algorithm equals the optimum value of the
original problem.

**Proof.**  
*Feasibility* of `T` follows from Lemma&nbsp;4, therefore the optimum is at
least `T`.  
If the optimum were larger, say `opt > T`, then `opt` would be feasible,
contradicting Lemma&nbsp;4 which states that no integer larger than `T` is
feasible. Hence `opt ≤ T`. Together we have `opt = T`. ∎



##### Theorem  
The algorithm always outputs the maximum possible value of the minimum
intake among vitamins 1, 2 and 3 under the calorie limit `X`.

**Proof.**  
Directly from Lemma&nbsp;5. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

*DP for the three vitamins*  

```
time   :  O(N · X)   ≤ 5·10³·5·10³ = 2.5·10⁷
memory :  O(X)       ≤ 5·10³  integers per vitamin (≈ 15 KB total)
```

*Binary search*  

```
iterations ≤ log₂( upper ) ≤ 31
each iteration scans at most 3·(X+1) ≤ 15003 entries
time   :  O( X log upper )  ≤ 5·10³·31  ≈ 1.5·10⁵
memory :  O(1)   (uses the tables already built)
```

Overall  

```
Time   :  O(N·X)   (dominant part)
Memory :  O(X)
```

Both satisfy the limits easily.

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys

def solve() -> None:
    input = sys.stdin.readline
    first = input().split()
    if not first:
        return
    N, X = map(int, first)

    # foods separated by their vitamin type (0,1,2 correspond to 1,2,3)
    foods = [[] for _ in range(3)]
    total_amount = [0, 0, 0]

    for _ in range(N):
        V, A, C = map(int, input().split())
        foods[V - 1].append((A, C))
        total_amount[V - 1] += A

    # ---------- 0/1 knapsack for each vitamin ----------
    # best[v][c] = maximum amount of vitamin v obtainable with at most c calories
    best = []
    for v in range(3):
        dp = [-1] * (X + 1)
        dp[0] = 0
        for a, c in foods[v]:
            # iterate backwards to enforce 0/1 usage
            for w in range(X, c - 1, -1):
                if dp[w - c] != -1:
                    val = dp[w - c] + a
                    if val > dp[w]:
                        dp[w] = val
        # make it monotone: max value for any weight ≤ w
        for w in range(1, X + 1):
            if dp[w] < dp[w - 1]:
                dp[w] = dp[w - 1]
        best.append(dp)

    # ---------- helper: is t attainable ? ----------
    def feasible(t: int) -> bool:
        used = 0
        for v in range(3):
            # smallest weight w with best[v][w] >= t
            w = 0
            while w <= X and best[v][w] < t:
                w += 1
            if w > X:          # impossible for this vitamin
                return False
            used += w
            if used > X:       # early stop
                return False
        return used <= X

    # ---------- binary search on the answer ----------
    lo = 0
    hi = min(total_amount)          # obvious upper bound

    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(lo)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.
