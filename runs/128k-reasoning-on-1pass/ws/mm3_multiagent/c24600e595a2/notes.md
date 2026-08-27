
## ideation
The operation flips a single bit of `A` and then charges the **new** weighted sum of ones.  
The total payment equals the sum of the weighted sums of all intermediate arrays
(the initial array does not contribute).  
Thus the problem reduces to: in which order should we flip the required bits to make
`A` equal to `B` so that the sum of the intermediate weighted sums is minimal?

Key observations:
* Every position that differs must be flipped exactly once (flipping twice cancels and
  only adds non‑negative cost).
* Flipping `1 → 0` (a *removal*) **decreases** the current weight,
  while flipping `0 → 1` (an *addition*) **increases** it.
* An optimal sequence can be transformed into one where **all removals happen first**
  and then **all additions** (exchange argument: swapping an addition that precedes a
  removal never raises the cost because `c + d > 0`).
* Within the removal phase, processing larger `C_i` first yields a smaller total cost
  (removing a larger weight reduces the current weight earlier, which benefits every
  later step). Hence removals should be ordered **descending** by `C_i`.
* Within the addition phase, processing smaller `C_i` first is optimal (adding a small
  weight increases the current weight only a little). Hence additions should be ordered
  **ascending** by `C_i`.

With this optimal order the total cost can be computed by a single linear simulation:

```
cur = initial_weight = Σ C_i for i with A_i = 1
ans = 0
for c in removals (sorted descending):
        ans += cur - c          # weight after the removal
        cur  -= c
for c in additions (sorted ascending):
        ans += cur + c          # weight after the addition
        cur  += c
```

The algorithm runs in `O(N log N)` time (for sorting) and `O(N)` memory, well within
the limits (`N ≤ 2·10⁵`). The answer can be as large as `≈ 10⁶·2·10⁵·2·10⁵` (≈ 8·10¹⁶),
which fits easily in Python’s arbitrary‑precision integers.

Pitfalls to watch for:
* Using the **new** weight after each flip (not before) when accumulating the answer.
* Not forgetting positions where `A_i = B_i = 1` – they stay `1` throughout and affect the
  current weight at every step.
* Handling the case where there are no removals or no additions (loops simply do nothing).
* Ensuring fast input reading for up to `2·10⁵` numbers.

## worker: Implement `solve()` in Python as described: read N
The operation flips a single bit of `A` and then charges the **new** weighted sum of ones.  
The total payment equals the sum of the weighted sums of all intermediate arrays (the initial one does not contribute).  
Thus we need to decide the order of flipping the required bits to turn `A` into `B` so that this sum is minimal.

Key observations:
* Every position that differs must be flipped exactly once (flipping twice cancels and only adds non‑negative cost).
* Flipping `1 → 0` (a *removal*) **decreases** the current weight, while flipping `0 → 1` (an *addition*) **increases** it.
* An optimal sequence can be transformed into one where **all removals happen first** and then **all additions** (exchange argument: swapping an addition that precedes a removal never raises the cost because `c + d > 0`).
* Within the removal phase, processing larger `C_i` first yields a smaller total cost (removing a larger weight reduces the current weight earlier, benefiting every later step). Hence removals should be ordered **descending** by `C_i`.
* Within the addition phase, processing smaller `C_i` first is optimal (adding a small weight increases the current weight only a little). Hence additions should be ordered **ascending** by `C_i`.

With this optimal order the total cost can be computed by a single linear simulation:
```
cur = Σ C_i for i with A_i = 1
ans = 0
for c in removals (sorted descending):
        ans += cur - c
        cur  -= c
for c in additions (sorted ascending):
        ans += cur + c
        cur  += c
```
The algorithm runs in `O(N log N)` time (for sorting) and `O(N)` memory, well within the limits (`N ≤ 2·10⁵`). Python’s arbitrary‑precision integers handle the potentially large result.

The implementation reads the entire input as tokens, builds the `remove` and `add` lists, sorts them as required, and performs the simulation to obtain the minimum total cost.

## worker: Implement `solve()` in Python with fast I/O, build
The algorithm follows the proven optimal strategy:
1. **Classify** each position: removal (1→0) or addition (0→1).
2. **Remove first, add later**: any addition before a removal can be swapped to reduce cost (since C_i > 0).
3. **Order removals descending** by C_i: removing larger weights first reduces the current weight earlier, benefiting all subsequent operations.
4. **Order additions ascending** by C_i: adding smaller weights first keeps the current weight low for longer.
5. **Simulate** the process: after each flip, the cost paid is the new weight, which we accumulate.

The code uses `sys.stdin.buffer.read()` for fast I/O and Python's arbitrary-precision integers handle the potentially large result (up to ~8×10¹⁶). Time complexity is O(N log N) due to sorting, and memory is O(N).
