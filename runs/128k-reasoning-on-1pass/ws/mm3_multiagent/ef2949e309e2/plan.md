The middle element of a size‑5 subsequence is at the third chosen index `i`.  
For each possible middle position `i` we count how many ways to choose the two
indices on the left and the two on the right so that the value `v = nums[i]`
is a **unique mode**.  
Let  

* `L[x]` – occurrences of value `x` in the left part (`< i`)  
* `R[x]` – occurrences of value `x` in the right part (`> i`)  

`L[v]` and `R[v]` are the numbers of `v` on left/right.  
The total number of `v` in the subsequence is `c = L[v] + R[v] + 1`.  
The only feasible values are `c = 2,3,4,5` ( `c = 1` can never win).  

For a fixed `i` we enumerate the possible distributions of the `c‑1` extra
`v`’s between left and right:

| c | distribution (a,b) = (#v on left, #v on right) | condition on other picks |
|---|----------------------------------------------|--------------------------|
| 5 | (2,2)                                         | none                      |
| 4 | (1,2) or (2,1)                               | one non‑v on the side with the single `v` |
| 3 | (0,2) , (1,1) , (2,0)                        | the other picks may repeat values |
| 2 | (0,1) or (1,0)                               | the three other picks must be **all different** |

All counts are expressed only through  

```
L[v], R[v], Lnv = i - L[v], Rnv = (n-1-i) - R[v]
Σ L[w]^2 , Σ R[w]^2 , Σ L[w]·R[w]   (over w ≠ v)
```

and the auxiliary sums

```
A = (Lnv^2 - Σ L[w]^2) / 2               # unordered pairs of left non‑v
Ap = (Rnv^2 - Σ R[w]^2) / 2
B = Σ L[w]·R[w]·(Lnv - L[w])
Bp = Σ L[w]·R[w]·(Rnv - R[w])
```

These give the required number of ways for the `c = 2` case, while the
other cases are simple binomial products.

The whole algorithm scans the array once, maintaining a prefix count
`left_cnt`. For each `i` we compute the above aggregates by iterating over
all distinct values (`O(K)` per `i`, `K ≤ n ≤ 1000`). The total work is
`O(n·K) ≤ 10⁶`, easily fast enough.

All answers are taken modulo `10⁹+7`.