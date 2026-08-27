**Solution Explanation**

For a binary vector `X = (X1 … XN)` let  

```
weight(X) = Σ ( Xi · Ci )
```

The operation described in the statement is

*choose an index i, flip Xi*  

and the paid amount is the weight **after** the flip.

If we write the sequence of vectors that appear while we are working

```
A = S0 , S1 , S2 , … , Sk = B
```

(`S0` is the initial array, `Sk` is the final one) then the total amount
we pay is

```
cost = weight(S1) + weight(S2) + … + weight(Sk)            (1)
```

The start state `S0` does **not** contribute to the cost.



--------------------------------------------------------------------

#### 1.   Which bits have to be flipped ?

```
S1 = { i | Ai = 1 , Bi = 0 }   ( 1 → 0 )
S0 = { i | Ai = 0 , Bi = 1 }   ( 0 → 1 )
```

Every optimal solution flips every index of `S1` and `S0` **once**
(flipping twice cancels, and any extra flip only adds a non‑negative
cost).

--------------------------------------------------------------------

#### 2.   Order of the flips

*Removing a 1* (`1 → 0`) **decreases** the weight,
*adding a 1* (`0 → 1`) **increases** the weight.

*Exchange argument*  

Assume an optimal sequence contains an addition before a removal.
Look at the two involved operations only, everything else unchanged.

```
…  (current weight = w)  →  add c  →  (weight w+c)  →  remove d  →  (weight w+c-d)
```

The paid amount for the two steps is  

```
(w + c) + (w + c – d) = 2w + 2c – d                (2)
```

If we swap them we get  

```
(w – d) + (w – d + c) = 2w – 2d + c                (3)
```

The difference (2) – (3) = `c + d  > 0`.  
So swapping **never increases** the total cost, it even makes it
strictly smaller because all `Ci` are positive.
Therefore an optimal sequence can be transformed into one where

```
all removals are performed first, afterwards all additions.
```

*Order inside the two groups*  

Consider only the removals.
During a removal the paid amount equals the weight **after** the removal,
i.e. the current weight minus the removed `Ci`.
Hence a larger `Ci` gives a larger reduction of the weight and
decreases the cost of all later operations more.
Consequently we should remove the **largest** `Ci` first,
the second largest next, … – i.e. `S1` in **descending** order.

For additions the situation is symmetric.
The cost of an addition is the current weight **plus** the added `Ci`.
Adding a small `Ci` early increases the weight only a little,
while a large `Ci` would increase it a lot and make all later
operations more expensive.
So we add the **smallest** `Ci` first, then the second smallest, … –
i.e. `S0` in **ascending** order.

--------------------------------------------------------------------

#### 3.   Computing the cost

```
w0 = Σ Ci for all i with Ai = 1                (initial weight)

cur = w0
answer = 0

for c in S1 sorted descending:
        answer += cur - c          # weight after the removal
        cur    -= c

# now cur = Σ Ci for positions where Ai = Bi = 1

for c in S0 sorted ascending:
        answer += cur + c          # weight after the addition
        cur    += c
```

`answer` is exactly the value of (1) for the optimal order,
hence the minimum possible total cost.

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm described above always outputs the minimum
total cost.

---

##### Lemma 1  
In an optimal sequence no index is flipped more than once.

**Proof.**  
Every flip toggles the bit, therefore flipping the same index twice
restores the original value and the two operations are independent of
the rest of the sequence.
Their total cost is the sum of two non‑negative weights, therefore
removing the second flip never increases the total cost. ∎



##### Lemma 2  
Let a sequence contain an addition (cost `c`) before a removal (cost `d`).
Swapping these two operations does not increase the total cost.

**Proof.**  
The situation before the two operations is identical, call the current
weight `w`.  
Cost of the original order (addition then removal) is given by (2) :

```
2w + 2c – d
```

Cost after swapping (removal then addition) is given by (3) :

```
2w – 2d + c
```

Their difference equals `c + d > 0`, so the swapped order is cheaper.
∎



##### Lemma 3  
There exists an optimal sequence in which **all** removals are performed
before any addition.

**Proof.**  
Take an optimal sequence (exists by finiteness).  
If it already has this property we are done.
Otherwise there is a first addition that appears before a later removal.
By Lemma&nbsp;2 swapping these two operations yields a sequence with
strictly smaller cost – contradicting optimality.
Therefore such a pair cannot exist and the sequence must have all
removals first. ∎



##### Lemma 4  
Among all removals, processing them in **descending** order of `Ci`
minimises the total cost of the removal phase.

**Proof.**  
Consider two removals with values `x ≥ y`.
Let the current weight before the first one be `w`.  
The cost of the order *x then y* is  

```
(w – x) + (w – x – y) = 2w – 2x – y
```

The cost of the order *y then x* is  

```
(w – y) + (w – y – x) = 2w – 2y – x
```

Since `x ≥ y`, `2w – 2x – y ≤ 2w – 2y – x`.  
Thus putting the larger `Ci` first is never worse.
By repeatedly applying this argument to adjacent pairs,
any order can be transformed into descending order without increasing
the cost. ∎



##### Lemma 5  
Among all additions, processing them in **ascending** order of `Ci`
minimises the total cost of the addition phase.

**Proof.**  
The argument is symmetric to Lemma&nbsp;4.
For two additions with values `x ≤ y` and current weight `w`,
the cost of *x then y* is `2w + 2x + y`,
the cost of *y then x* is `2w + 2y + x`,
and the former is not larger because `x ≤ y`. ∎



##### Lemma 6  
The algorithm computes the cost of the sequence  

*removals in descending order, followed by additions in ascending order*.

**Proof.**  
The algorithm starts with `cur = w0 = weight(A)`.  
For a removal of value `c` it adds `cur - c` (the weight after the
removal) to the answer and updates `cur ← cur - c`.  
Consequently after processing all removals, `cur` equals the weight of
the vector consisting of the positions where `Ai = Bi = 1`.

For an addition of value `c` it adds `cur + c` (the weight after the
addition) and updates `cur ← cur + c`.  
After all additions `cur` becomes the weight of the final vector `B`.
Thus the accumulated value equals the sum of the weights of all
intermediate states, i.e. the cost of that concrete sequence. ∎



##### Lemma 7  
The sequence used by the algorithm is optimal.

**Proof.**  
By Lemma&nbsp;3 there is an optimal sequence with all removals first.
By Lemma&nbsp;4 the removal part can be reordered into descending order
without increasing the cost.
By Lemma&nbsp;5 the addition part can be reordered into ascending order
without increasing the cost.
The resulting sequence is exactly the one simulated by the algorithm,
so its cost is optimal. ∎



##### Theorem  
The program prints the minimum possible total amount of money needed to
turn the array `A` into `B`.

**Proof.**  
The program implements the algorithm proved optimal in Lemma&nbsp;7,
and Lemma&nbsp;6 shows that the value it computes equals the cost of
that optimal sequence.  Therefore the printed number is the minimum
achievable cost. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

*Reading the input* – `O(N)`  
*Sorting* – at most `N` numbers in each of the two lists: `O(N log N)`  
*One linear scan* – `O(N)`  

Memory consumption: the three input arrays (`O(N)`) and the two
auxiliary lists `S0` and `S1` (at most `N` integers).  
Overall  

```
Time   :  O(N log N)      (N ≤ 2·10⁵)
Memory :  O(N)
```

Both easily satisfy the limits.



--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys

def solve() -> None:
    input = sys.stdin.readline
    N_line = input()
    while N_line.strip() == "":
        N_line = input()
    N = int(N_line)

    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    C = list(map(int, input().split()))

    # values to be removed (1 -> 0) and to be added (0 -> 1)
    remove = []   # S1
    add = []      # S0

    w0 = 0          # initial weight = sum Ci for Ai == 1
    w_fixed = 0     # weight of positions that are already 1 and stay 1

    for a, b, c in zip(A, B, C):
        if a == 1:
            w0 += c
            if b == 1:
                w_fixed += c
        if a == 0 and b == 1:
            add.append(c)          # 0 -> 1
        elif a == 1 and b == 0:
            remove.append(c)       # 1 -> 0

    # optimal orders
    remove.sort(reverse=True)   # descending
    add.sort()                  # ascending

    cur = w0
    total = 0

    # all removals first
    for c in remove:
        total += cur - c   # weight after the removal
        cur -= c

    # now cur == w_fixed

    # then all additions
    for c in add:
        total += cur + c   # weight after the addition
        cur += c

    print(total)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.