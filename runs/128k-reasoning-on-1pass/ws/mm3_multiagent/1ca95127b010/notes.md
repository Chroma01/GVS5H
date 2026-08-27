
## ideation
**Problem understanding**  
We have two binary strings `S` and `T` of length `N`. Two operations are allowed:

- **Operation A**: replace a pattern `00…0 11…1` (exactly `X` zeros followed by `Y` ones) with `11…1 00…0` (the same `X` zeros and `Y` ones swapped).
- **Operation B**: replace a pattern `11…1 00…0` (exactly `Y` ones followed by `X` zeros) with `00…0 11…1` (the same `Y` ones and `X` zeros swapped).

Both operations keep the total number of `0`s and `1`s unchanged. The question is whether `S` can be turned into `T` using any sequence of these operations.

**Core difficulty**  
The operations only **swap adjacent blocks** of opposite type: a block of `X` zeros can be swapped with a neighboring block of `Y` ones, and a block of `Y` ones can be swapped with a neighboring block of `X` zeros. However, a block must have **full length** (`X` for zeros, `Y` for ones) to be movable. Shorter blocks are *fixed* and can never participate in an operation.

Thus the problem reduces to understanding which parts of the string are movable and which are fixed, and then checking if the two strings have the same “canonical” structure.

**Key observations**

1. **Decomposition of a run**  
   - For a maximal run of zeros of length `L`:  
     `L = q·X + r` with `0 ≤ r < X`.  
     The leftmost `r` zeros are **fixed** (they are too short to be part of an operation). The remaining `q` blocks of exactly `X` zeros are **movable**.  
   - For a maximal run of ones of length `M`:  
     `M = p·Y + s` with `0 ≤ s < Y`.  
     The rightmost `s` ones are **fixed**. The preceding `p` blocks of exactly `Y` ones are **movable**.

2. **Canonical representation**  
   By scanning the string from left to right, we obtain an alternating list of:
   - **Fixed parts**: pairs `(type, length)` where `type` is `0` or `1`.
   - **Intervals**: segments between two consecutive fixed parts (or the ends of the string) that contain only movable blocks. An interval is described by the number of `X`‑blocks and `Y`‑blocks it contains, i.e., a pair `(cntX, cntY)`.

3. **Effect of operations**  
   Inside a single interval, any two adjacent blocks of opposite type can be swapped (Operation A or B). This is exactly the ability to perform bubble‑sort on the sequence of blocks, so **any permutation of the blocks within an interval is reachable**.  
   Fixed parts never move because they are too short to be part of any operation.

4. **Transformability condition**  
   `S` can be transformed into `T` **iff** their canonical representations are identical:
   - The sequences of fixed parts are exactly the same (same order, same type, same length).
   - The sequences of intervals are exactly the same (same number of intervals, and for each interval the counts of `X`‑blocks and `Y`‑blocks are equal).

   This condition is necessary (operations cannot change fixed parts or the total number of blocks in an interval) and sufficient (within each interval we can reorder the blocks arbitrarily to match the order in `T`).

5. **Algorithm outline**  
   - Parse `S` to obtain `(fixed_S, intervals_S)`.  
   - Parse `T` to obtain `(fixed_T, intervals_T)`.  
   - Compare the two fixed lists element by element.  
   - Compare the two interval lists element by element.  
   - If all comparisons match, output `Yes`; otherwise `No`.

**Pitfalls and edge cases**

- **Direction of fixed remainder**: zeros remainder is **leftmost**, ones remainder is **rightmost**. Incorrect handling will break the comparison.
- **Interval boundaries**: a new interval must be started **after** every fixed part (including the first fixed part, so the interval before it is stored even if empty).
- **Runs with no fixed part**: the whole run is movable blocks, and they are added to the current interval.
- **When `X` or `Y` is larger than `N` (or `X+Y > N`)**: the operation may be impossible, but the canonical representation remains injective; the condition still correctly reduces to `S == T`.
- **First and last intervals**: the initial interval (before the first fixed part) and the final interval (after the last fixed part) must be considered.
- **Off-by-one errors** in the decomposition (`%` and `//` operations) and in the scanning loop.
- **Large `N` (5·10⁵)**: linear time `O(N)` and linear memory `O(N)` are required; Python’s recursion is not needed.
- **Input format**: read all data at once with `sys.stdin.read()` for speed.

**Candidate approaches**

1. **Brute‑force simulation** – impossible due to exponential state space.
2. **BFS/DFS on all possible strings** – infeasible for `N` up to 5·10⁵.
3. **Block decomposition and canonical comparison** – the intended efficient solution; runs in `O(N)`.
4. **Greedy matching** – trying to apply operations on the fly to transform `S` into `T` might work but is more complex and error‑prone.
5. **String hashing / automata** – not suitable because the operations are not local enough.

The block‑decomposition method is the natural, optimal approach.

---

## worker: finalize
The solution decomposes each string into fixed parts (remainders of runs that are shorter than the required block size) and intervals (segments containing only full blocks of length X or Y). The operations allow swapping adjacent full blocks of opposite type, so within each interval the multiset of blocks is invariant, and the fixed parts never move. Therefore, two strings are transformable if and only if their sequences of fixed parts and the counts of X‑blocks and Y‑blocks in each corresponding interval are identical. The parsing is linear in the string length, and the comparison is straightforward.
