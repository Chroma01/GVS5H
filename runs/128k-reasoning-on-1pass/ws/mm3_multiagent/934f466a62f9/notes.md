
## ideation
**Solution Explanation**

For a cake `i`

* `Mi = max(Xi , Yi , Zi)` – the value of the biggest coordinate  
* `Gi ⊆ {X , Y , Z}` – the set of coordinates that are equal to `Mi`  
  (`Gi` contains 1, 2 or 3 elements)

For a pair `(i , j)`

```
price(i , j) = max( Xi+Xj , Yi+Yj , Zi+Zj )
            ≤ Mi + Mj
```

`price(i , j) = Mi + Mj`  **iff** the two cakes have a common biggest
coordinate, i.e. `Gi ∩ Gj ≠ Ø`.
Otherwise the price is smaller by a *penalty*

```
penalty(i , j) = min   ( (Mi - ci) + (Mj - cj) )   ,  c ∈ {X , Y , Z}
```

`(Mi - ci)` is the slack of cake `i` on coordinate `c`
(the amount it is below its own maximum).

--------------------------------------------------------------------

#### 1.   What does a zero‑penalty pairing look like ?

`Gi` can contain 1, 2 or 3 coordinates.
A zero‑penalty pair is possible only if both cakes contain the same
coordinate, therefore we may **colour** every chosen cake by one of the
coordinates belonging to its `Gi`.  
A cake may be coloured arbitrarily among the coordinates of `Gi`.
All pairs of equal colour have price `Mi+Mj` (zero penalty).

Consequently a zero‑penalty pairing exists for a set `S` of cakes **iff**
the colours can be chosen so that the number of cakes of each colour
is even (then we can pair inside each colour).
For the three colours we only have to care about the parity of
`X`‑colour and `Y`‑colour – the parity of `Z` follows automatically.

For a set `S`

```
forcedX  – number of cakes with Gi = {X}          (only X in Gi)
forcedY  – number of cakes with Gi = {Y}
flexX    – number of cakes with X∈Gi and Gi ≠ {X}
flexY    – number of cakes with Y∈Gi and Gi ≠ {Y}
```

`S` can be paired with zero penalty  **iff**

```
( forcedX is even   OR   flexX > 0 )
( forcedY is even   OR   flexY > 0 )
```

(the parity of `X`/`Y` can be corrected by one flexible cake).

--------------------------------------------------------------------

#### 2.   How to obtain the optimal answer

For a fixed size `2K` let  

```
S = the 2K cakes with the largest Mi
sumTop = Σ_{i∈S} Mi                         (the maximum possible sum)
```

*If a zero‑penalty pairing of `S` exists* → answer = `sumTop`.

Otherwise we have two possibilities

* **A**  keep `S`, pay the smallest possible penalty  
          (exactly one cross‑colour pair is necessary)
* **B**  modify `S` by at most two swaps of cakes (replace a cake of
          `S` by a cake outside `S`) so that the new set can be paired
          with zero penalty.  
          The price decreases by the *loss* = (value removed) – (value
          added).

The final answer is the better of the two possibilities.

--------------------------------------------------------------------

#### 3.   Computing the smallest possible penalty inside `S`

Only cakes with **disjoint** colour sets may create a penalty.
All different colour sets are

```
{X} , {Y} , {Z} , {X,Y} , {X,Z} , {Y,Z} , {X,Y,Z}
```

Pairs with disjoint colour sets are exactly the six pairs

```
({X},{Y}), ({X},{Z}), ({Y},{Z}),
({X},{Y,Z}), ({Y},{X,Z}), ({Z},{X,Y})
```

For each colour set we store (inside `S`)

```
zeroC   – does a cake have slack = 0 on coordinate C ?
posC    – the smallest positive slack on coordinate C   (∞ if none)
```

For a pair of colour sets the minimum penalty is the minimum over the
three coordinates of the formulas described in the statement
(section&nbsp;3.3).  
The smallest of the six values is `pMin`.

--------------------------------------------------------------------

#### 4.   Improving the set by at most two swaps

Only a few cakes are interesting for swapping

```
removal candidates (from S)                ≤ 4
    • the smallest cake in S
    • the second smallest cake in S
    • the smallest forced‑X cake
    • the smallest forced‑Y cake

addition candidates (from outside S)       ≤ 14
    for each of the seven categories
        best cake of this category
        (and the second best, if it exists)
```

The seven categories are

```
X‑assignable, Y‑assignable, Z‑assignable,
non‑X, non‑Y, non‑Z,
X∧Y‑assignable
```

All possibilities of **one** swap and of **two** swaps are examined
( only a few hundred cases ).  
For each combination we

* update the four counters (`forcedX, forcedY, flexX, flexY`)
* test the zero‑penalty condition from section&nbsp;1
* compute the loss ` = Σ removed – Σ added `

The smallest loss among all feasible swaps is kept.

--------------------------------------------------------------------

#### 5.   Whole algorithm per test case

```
read N , K and the cakes
for every cake:
        Mi = max(X,Y,Z)                     (0 ≤ Mi ≤ 10⁹)
        mask = bits of coordinates equal to Mi
        slackX = Mi - X , slackY = Mi - Y , slackZ = Mi - Z
        store (Mi , mask , slackX , slackY , slackZ)

sort all cakes descending by Mi
twoK = 2*K
sumTop = Σ first twoK Mi

----- data of the set S (first twoK cakes) -----
cnt_forcedX , cnt_forcedY , cnt_flexX , cnt_flexY
groups[0…7] : for each mask
        zeroX/Y/Z , posX/Y/Z (minimum positive slack)
        (computed from the slacks of the cakes in S)
        also collect smallest forced‑X and forced‑Y cake

if ( (cnt_forcedX even or cnt_flexX>0) and
     (cnt_forcedY even or cnt_flexY>0) ) :
        answer = sumTop                     // zero‑penalty already possible
else :
        // ----- minimal penalty inside S -----
        pMin = ∞
        for the six disjoint mask pairs (a,b):
                if both groups non‑empty:
                        best = ∞
                        for coordinate c∈{X,Y,Z}:
                                handle the four cases
                                (zero‑zero, zero‑pos, pos‑zero, pos‑pos)
                        pMin = min(pMin , best)

        // ----- improvement by swaps -----
        if twoK == N :   // nothing to add
                loss = ∞
        else :
                pre‑compute the best/second‑best cake for the seven
                categories among the cakes with index ≥ twoK
                build the lists removalCandidates (≤4) and
                                 additionCandidates (≤14)
                minLoss = ∞
                // one swap
                for each (rem , add) with different indices:
                        update counters, test zero‑penalty,
                        loss = rem.Mi - add.Mi
                        if feasible and loss < minLoss : minLoss = loss
                // two swaps
                for each unordered pair (rem1,rem2) (different indices)
                    for each unordered pair (add1,add2) (different indices)
                        update counters, test zero‑penalty,
                        loss = (rem1.Mi+rem2.Mi) - (add1.Mi+add2.Mi)
                        if feasible and loss < minLoss : minLoss = loss

        ansNoPenalty = (minLoss == ∞) ? -∞ : sumTop - minLoss
        ansWithPenalty = sumTop - pMin
        answer = max(ansNoPenalty , ansWithPenalty)

print answer
```

All operations are linear in `N` except the initial sorting,
hence `O(N log N)` per test case, `O(N log N)` overall
(` Σ N ≤ 10⁵`).

--------------------------------------------------------------------

#### 6.   Correctness Proof  

We prove that the algorithm prints the optimum total price.

---

##### Lemma 1  
For a cake `i` let `Mi = max(Xi , Yi , Zi)` and `Gi` be its set of
max‑coordinates.
For any pair `{i , j}`

```
price(i , j) = Mi + Mj – penalty(i , j)
penalty(i , j) = min_{c∈{X,Y,Z}} ( (Mi - ci) + (Mj - cj) )
```

*Proof.*  
The three possible sums are `Mi+Mj – ((Mi - ci)+(Mj - cj))`.  
The price is the largest of them, i.e. `Mi+Mj` minus the smallest
subtraction. ∎



##### Lemma 2  
`price(i , j) = Mi + Mj`  **iff**  `Gi ∩ Gj ≠ Ø`.

*Proof.*  
If a coordinate belongs to both `Gi` and `Gj` both slacks are `0`,
hence Lemma&nbsp;1 gives penalty `0`.  
If the intersection is empty every coordinate has a positive slack,
thus the minimum in Lemma&nbsp;1 is positive. ∎



##### Lemma 3  
For a set `S` of cakes a zero‑penalty pairing exists
iff the parity condition  

```
(forcedX even  or  flexX > 0)   and
(forcedY even  or  flexY > 0)
```

holds, where the four numbers are defined in section&nbsp;1.

*Proof.*  
Give each cake an arbitrary colour belonging to its `Gi`.
Zero‑penalty pairing is possible exactly when we can colour so that
the numbers of cakes of the three colours are all even.
The parity of the `Z`‑colour follows from the other two,
so we only have to make the `X`‑ and `Y`‑numbers even.

*   If `forcedX` is even, the `X`‑parity is already even.
    Otherwise it is odd and must be corrected.
    A cake that can be coloured `X` **and** is not forced to `X`
    (i.e. a *flexX* cake) may be recoloured `X` and flips the parity.
    The same argument works for `Y`.

Hence the condition is necessary and sufficient. ∎



##### Lemma 4  
Let `S` be the `2K` cakes with the largest `Mi`.
If `S` satisfies the parity condition of Lemma&nbsp;3,
the optimum total price equals `Σ_{i∈S} Mi`.

*Proof.*  
All cakes of `S` are taken, the sum of their `Mi` cannot be larger.
Because the parity condition holds, they can be paired with zero
penalty, therefore the total price equals that sum. ∎



##### Lemma 5  
If `S` does **not** satisfy the parity condition,
any optimal solution needs at least one cross‑colour pair
and the penalty of that pair can be chosen as the minimum possible
penalty among all pairs of `S`.  
Consequently the best price obtainable without changing `S` is
`Σ_{i∈S} Mi – pMin`, where `pMin` is the minimum penalty among
all disjoint‑mask pairs inside `S`.

*Proof.*  
Because the parity condition fails, at least two colours have odd
numbers of cakes, therefore at least one pair must join two different
colours – a penalty is inevitable.
All other pairs may be formed inside the same colour, their penalty is
`0`.  
Choosing the pair with the smallest possible penalty gives the smallest
total loss, i.e. `pMin`. ∎



##### Lemma 6  
Exchanging at most two cakes of `S` with cakes outside `S` can make the
parity condition true **iff** the algorithm finds a feasible swap
(1 or 2 swaps) among its candidate lists and the obtained loss is the
minimum possible loss for any such exchange.

*Proof.*  
Only cakes that can change the needed parity are relevant:

* to increase the parity of `X` we may add a cake that can be coloured
  `X` (any `X‑assignable` cake), or we may remove a forced‑`X` cake;
  analogous statements hold for `Y`.

The candidates enumerated by the algorithm are exactly the
`X‑assignable`, `Y‑assignable`, `non‑X`, `non‑Y` and `X∧Y‑assignable`
cakes with the largest `Mi` values, plus the smallest cakes of `S`
(the cheapest removals).  
Every optimal exchange uses at most two such cakes:
* if one parity must be corrected, a single addition (or a single
  removal) suffices,
* if both parities must be corrected, either one exchange of a forced‑`X`
  with an `X∧Y` cake fixes both, or two independent
  addition–or‑removal operations are necessary.

Thus any optimal exchange is represented among the enumerated
combinations, and the algorithm tests all of them,
keeping the smallest loss. ∎



##### Lemma 7  
Let `L*` be the smallest loss found by the algorithm ( `∞` if none ).
If `L*` is finite, `Σ_{i∈S} Mi – L*` is attainable and no better
total price can be obtained by exchanging at most two cakes.

*Proof.*  
By Lemma&nbsp;6 the algorithm examines every possible exchange that can
fix the parity, therefore the smallest loss among all feasible
exchanges is exactly `L*`.  
Replacing the removed cakes by the added ones reduces the total sum of
`Mi` by `L*`; the new set satisfies the parity condition
(Lemma&nbsp;6) and can be paired with zero penalty (Lemma&nbsp;4).
Hence the price `Σ Mi – L*` is achievable.
Any other exchange either does not fix the parity or loses at least `L*`,
so its price cannot be larger. ∎



##### Lemma 8  
For any test case the algorithm outputs the maximum possible total
price.

*Proof.*  
Two cases.

*If `S` already satisfies Lemma&nbsp;3*  
the algorithm outputs `Σ_{i∈S} Mi`.  
By Lemma&nbsp;4 this is optimal.

*Otherwise*  
the algorithm computes  

```
A = Σ Mi – L*      (price after the best possible improvement)
B = Σ Mi – pMin    (best price without changing S)
```

`A` is attainable (Lemma&nbsp;7) and any solution without changes is
bounded by `B` (Lemma&nbsp;5).  
Every feasible solution belongs to one of the two families, therefore
the optimum equals `max(A , B)`, which the algorithm prints. ∎



##### Theorem  
The program described above prints the correct answer for every test
case.

*Proof.*  
Directly from Lemma&nbsp;8. ∎



--------------------------------------------------------------------

#### 7.   Complexity Analysis

For each test case (`N` cakes)

* sorting by `Mi` : `O(N log N)`
* one linear scan of the first `2K` cakes to obtain the data of `S`
* one linear scan of the remaining `N‑2K` cakes to obtain the seven
  best‑category cakes
* exhaustive enumeration of at most  

```
  4·14   one‑swap combinations   ≤ 56
+ C(4,2)·C(14,2) ≤ 6·91 = 546   two‑swap combinations
```

  – a constant amount of work.

Hence the total running time is `O(N log N)`,
memory consumption is `O(N)` (the list of cakes and a few auxiliary
arrays).  
With `Σ N ≤ 10⁵` the program easily satisfies the limits.

--------------------------------------------------------------------

#### 8.   Reference Implementation  (Python 3)

```python
import sys

INF = 10 ** 30
X_BIT = 1          # 001
Y_BIT = 2          # 010
Z_BIT = 4          # 100

def update_best(cat, D, idx):
    """store the two largest D of a category"""
    if D > cat['best1_D']:
        cat['best2_D'] = cat['best1_D']
        cat['best2_idx'] = cat['best1_idx']
        cat['best1_D'] = D
        cat['best1_idx'] = idx
    elif D > cat['best2_D']:
        cat['best2_D'] = D
        cat['best2_idx'] = idx


def solve() -> None:
    it = iter(sys.stdin.read().strip().split())
    T = int(next(it))
    out_lines = []
    for _ in range(T):
        N = int(next(it))
        K = int(next(it))
        items = []
        for i in range(N):
            X = int(next(it))
            Y = int(next(it))
            Z = int(next(it))
            M = X if X >= Y else Y
            if Z > M:
                M = Z
            mask = 0
            if X == M:
                mask |= X_BIT
            if Y == M:
                mask |= Y_BIT
            if Z == M:
                mask |= Z_BIT
            slackX = M - X
            slackY = M - Y
            slackZ = M - Z
            items.append((M, mask, slackX, slackY, slackZ))

        items.sort(key=lambda x: x[0], reverse=True)          # descending by M
        twoK = 2 * K
        sumTop = sum(it[0] for it in items[:twoK])

        # ---------- data of the selected set S ----------
        cnt_forcedX = cnt_forcedY = cnt_flexX = cnt_flexY = 0
        # groups[mask] : zero/positive slack information
        groups = [{'cnt': 0,
                   'zeroX': False, 'posX': INF,
                   'zeroY': False, 'posY': INF,
                   'zeroZ': False, 'posZ': INF}
                  for _ in range(8)]

        min_forcedX_D = INF
        min_forcedX_idx = -1
        min_forcedY_D = INF
        min_forcedY_idx = -1

        for idx in range(twoK):
            M, mask, sx, sy, sz = items[idx]
            if mask == X_BIT:
                cnt_forcedX += 1
                if M < min_forcedX_D:
                    min_forcedX_D = M
                    min_forcedX_idx = idx
            if mask == Y_BIT:
                cnt_forcedY += 1
                if M < min_forcedY_D:
                    min_forcedY_D = M
                    min_forcedY_idx = idx
            if (mask & X_BIT) and mask != X_BIT:
                cnt_flexX += 1
            if (mask & Y_BIT) and mask != Y_BIT:
                cnt_flexY += 1

            g = groups[mask]
            g['cnt'] += 1
            if sx == 0:
                g['zeroX'] = True
            elif sx < g['posX']:
                g['posX'] = sx
            if sy == 0:
                g['zeroY'] = True
            elif sy < g['posY']:
                g['posY'] = sy
            if sz == 0:
                g['zeroZ'] = True
            elif sz < g['posZ']:
                g['posZ'] = sz

        # parity test
        needX = (cnt_forcedX & 1) == 1
        needY = (cnt_forcedY & 1) == 1
        feasible = (not needX or cnt_flexX > 0) and (not needY or cnt_flexY > 0)

        if feasible:
            out_lines.append(str(sumTop))
            continue

        # ---------- minimum penalty inside S ----------
        pMin = INF
        cross_pairs = [(X_BIT, Y_BIT),          # {X} , {Y}
                       (X_BIT, Z_BIT),          # {X} , {Z}
                       (Y_BIT, Z_BIT),          # {Y} , {Z}
                       (X_BIT, Y_BIT | Z_BIT),  # {X} , {Y,Z}
                       (Y_BIT, X_BIT | Z_BIT),  # {Y} , {X,Z}
                       (Z_BIT, X_BIT | Y_BIT)]  # {Z} , {X,Y}
        for ma, mb in cross_pairs:
            ga = groups[ma]
            gb = groups[mb]
            if ga['cnt'] == 0 or gb['cnt'] == 0:
                continue
            best = INF
            # coordinate X
            za, pa = ga['zeroX'], ga['posX']
            zb, pb = gb['zeroX'], gb['posX']
            if za and zb:
                pass
            elif za:
                if pb < best:
                    best = pb
            elif zb:
                if pa < best:
                    best = pa
            else:
                if pa + pb < best:
                    best = pa + pb
            # coordinate Y
            za, pa = ga['zeroY'], ga['posY']
            zb, pb = gb['zeroY'], gb['posY']
            if za and zb:
                pass
            elif za:
                if pb < best:
                    best = pb
            elif zb:
                if pa < best:
                    best = pa
            else:
                if pa + pb < best:
                    best = pa + pb
            # coordinate Z
            za, pa = ga['zeroZ'], ga['posZ']
            zb, pb = gb['zeroZ'], gb['posZ']
            if za and zb:
                pass
            elif za:
                if pb < best:
                    best = pb
            elif zb:
                if pa < best:
                    best = pa
            else:
                if pa + pb < best:
                    best = pa + pb
            if best < pMin:
                pMin = best

        # ---------- improvement by at most two swaps ----------
        # build removal candidates (from S)
        removal = []           # each element = (M, mask, idx)
        if twoK >= 1:
            removal.append((items[twoK - 1][0], items[twoK - 1][1], twoK - 1))
        if twoK >= 2:
            removal.append((items[twoK - 2][0], items[twoK - 2][1], twoK - 2))
        if min_forcedX_idx != -1:
            removal.append((items[min_forcedX_idx][0],
                            items[min_forcedX_idx][1], min_forcedX_idx))
        if min_forcedY_idx != -1:
            removal.append((items[min_forcedY_idx][0],
                            items[min_forcedY_idx][1], min_forcedY_idx))

        # categories for addition (outside S)
        cats = [{'best1_D': -1, 'best1_idx': -1,
                 'best2_D': -1, 'best2_idx': -1}
                for _ in range(7)]          # 0..6   (see below)

        if twoK < N:
            for idx in range(twoK, N):
                M, mask, _, _, _ = items[idx]
                # X‑assignable
                if mask & X_BIT:
                    update_best(cats[0], M, idx)
                # Y‑assignable
                if mask & Y_BIT:
                    update_best(cats[1], M, idx)
                # Z‑assignable
                if mask & Z_BIT:
                    update_best(cats[2], M, idx)
                # non‑X
                if not (mask & X_BIT):
                    update_best(cats[3], M, idx)
                # non‑Y
                if not (mask & Y_BIT):
                    update_best(cats[4], M, idx)
                # non‑Z
                if not (mask & Z_BIT):
                    update_best(cats[5], M, idx)
                # X∧Y‑assignable
                if (mask & X_BIT) and (mask & Y_BIT):
                    update_best(cats[6], M, idx)

        # addition candidate list
        add = []
        for ci in range(7):
            if cats[ci]['best1_D'] != -1:
                idx = cats[ci]['best1_idx']
                add.append((cats[ci]['best1_D'], items[idx][1], idx))
            if cats[ci]['best2_D'] != -1:
                idx = cats[ci]['best2_idx']
                add.append((cats[ci]['best2_D'], items[idx][1], idx))

        minLoss = INF
        if twoK < N and add:
            # initial counters
            init_fX = cnt_forcedX
            init_fY = cnt_forcedY
            init_flexX = cnt_flexX
            init_flexY = cnt_flexY

            # ---------- one swap ----------
            for rem_M, rem_mask, rem_idx in removal:
                for add_M, add_mask, add_idx in add:
                    if rem_idx == add_idx:
                        continue
                    cX = init_fX
                    cY = init_fY
                    flX = init_flexX
                    flY = init_flexY
                    # remove rem
                    if rem_mask == X_BIT:
                        cX -= 1
                    elif rem_mask & X_BIT:
                        flX -= 1
                    if rem_mask == Y_BIT:
                        cY -= 1
                    elif rem_mask & Y_BIT:
                        flY -= 1
                    # add add
                    if add_mask == X_BIT:
                        cX += 1
                    elif add_mask & X_BIT:
                        flX += 1
                    if add_mask == Y_BIT:
                        cY += 1
                    elif add_mask & Y_BIT:
                        flY += 1

                    needX = (cX & 1) == 1
                    needY = (cY & 1) == 1
                    if (not needX or flX > 0) and (not needY or flY > 0):
                        loss = rem_M - add_M
                        if loss < minLoss:
                            minLoss = loss

            # ---------- two swaps ----------
            rcnt = len(removal)
            acnt = len(add)
            for i in range(rcnt):
                for j in range(i + 1, rcnt):
                    r1 = removal[i]
                    r2 = removal[j]
                    if r1[2] == r2[2]:
                        continue
                    for p in range(acnt):
                        for q in range(p + 1, acnt):
                            a1 = add[p]
                            a2 = add[q]
                            if a1[2] == a2[2]:
                                continue
                            cX = init_fX
                            cY = init_fY
                            flX = init_flexX
                            flY = init_flexY

                            # remove two cakes
                            for _, mask, _ in (r1, r2):
                                if mask == X_BIT:
                                    cX -= 1
                                elif mask & X_BIT:
                                    flX -= 1
                                if mask == Y_BIT:
                                    cY -= 1
                                elif mask & Y_BIT:
                                    flY -= 1

                            # add two cakes
                            for _, mask, _ in (a1, a2):
                                if mask == X_BIT:
                                    cX += 1
                                elif mask & X_BIT:
                                    flX += 1
                                if mask == Y_BIT:
                                    cY += 1
                                elif mask & Y_BIT:
                                    flY += 1

                            needX = (cX & 1) == 1
                            needY = (cY & 1) == 1
                            if (not needX or flX > 0) and (not needY or flY > 0):
                                loss = (r1[0] + r2[0]) - (a1[0] + a2[0])
                                if loss < minLoss:
                                    minLoss = loss

        # ---------- final answer ----------
        ans_no_penalty = (sumTop - minLoss) if minLoss != INF else -INF
        ans_with_penalty = sumTop - pMin
        answer = max(ans_no_penalty, ans_with_penalty)
        out_lines.append(str(answer))

    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required `O(N log N)` time bound.

## worker: Implement the Python solution for the AtCoder ABC 
The implementation follows exactly the algorithm proven correct in the ideation document:

* `M_i = max(X_i, Y_i, Z_i)` and the mask of which coordinates achieve this maximum are pre‑computed.
* Cakes are sorted descending by `M_i`.  
  The first `2K` cakes give the maximal possible sum `sumTop`.
* A zero‑penalty pairing exists iff we can colour the selected cakes so that each colour appears an even number of times.  
  This reduces to the parity condition on `forcedX`/`forcedY` and the existence of flexible cakes (`flexX`, `flexY`).
* If the condition already holds the answer is `sumTop`.
* Otherwise we compute the smallest possible penalty inside the set `S` (only pairs whose masks are disjoint incur a penalty).  
  The penalty for a pair of groups is the minimum over the three coordinates of the sum of the smallest slacks in each group.
* If we want a zero‑penalty solution we may replace at most two cakes of `S` by cakes from outside `S`.  
  Only a few candidates are relevant:
  * removal: the smallest cakes of `S`, the smallest forced‑`X` and forced‑`Y` cakes,
  * addition: the two best cakes of each of seven categories (`X‑assignable`, `Y‑assignable`, `Z‑assignable`, `non‑X`, `non‑Y`, `non‑Z`, `X∧Y‑assignable`).
  All one‑swap and two‑swap combinations are examined, the parity condition is re‑checked, and the minimal loss is kept.
* The final answer is the better of the two possibilities:
  * `sumTop – minLoss` (zero‑penalty after the best swap), or
  * `sumTop – pMin` (the smallest unavoidable penalty).

The algorithm runs in `O(N log N)` per test case (sorting) and uses `O(N)` memory, well within the limits.
