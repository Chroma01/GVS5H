
## ideation
**Core difficulty**  
- `N` can be as large as 10¹², so we cannot simulate every square.  
- The move length is bounded by `B ≤ 20`, which limits the “memory” needed to decide future moves.  
- Bad squares are given as `M` disjoint intervals (`M ≤ 2·10⁴`), so the line splits into alternating safe and bad blocks.

**Key observation – state compression**  
Only the reachability of the last `B` squares matters.  
Let a bitmask `state` (length `B`) represent which of the squares at distances `0,…,B‑1` behind the current position are reachable.  
For a **safe** square the transition is deterministic:
```
new_state = ((state << 1) & ALL) |
            (1 if any of bits A‑1 … B‑1 is set else 0)
```
where `ALL = (1<<B)-1`.  
For a **bad** square the transition is a simple left shift (the new LSB is forced to 0).  
If a bad block has length `len ≥ B`, the mask becomes zero forever.

**Candidate approach**  
1. Parse the intervals, obtaining a list of alternating safe/bad blocks.  
2. Pre‑compute the transition for one safe step (`f`).  
3. Because the number of possible masks is at most `2^B ≤ 1 048 576`, pre‑compute `f^(2^i)` for `i = 0 … ⌈log₂ N⌉` (≤ 40) using binary lifting.  
4. Walk through the blocks:
   - For a safe block of length `L`, apply `L` safe steps using the lifting tables in `O(log L)` time.  
   - For a bad block of length `len`, shift the mask left by `len` (or set to zero if `len ≥ B`).  
5. After processing all blocks we are at square `N`. The answer is “Yes” iff the LSB of the final mask is 1.

**Pitfalls & edge cases**  
- **Memory for lifting tables**: `2^B · logN` entries can be large. With `B=20` and `logN≈40` we have ~40 M entries. Store them compactly (e.g., `array('I')`) to stay within typical limits (~160 MiB).  
- **Large bad blocks**: A bad block of length `≥ B` kills the mask; later safe steps cannot revive it. Early exit is possible.  
- **Empty safe blocks**: When `L_i = prev_end+1` the safe block is empty and must be skipped.  
- **Starting condition**: Square 1 is safe, initial mask = 1 (only distance 0 reachable).  
- **First/last blocks**: The first safe block starts at 1, the last safe block ends at N; ensure correct step counts.  
- **M = 0**: The whole line is safe; we simply apply `N‑1` safe steps.  
- **B small, A=1**: The transition may allow reaching any safe square; algorithm still works.  
- **Indexing off‑by‑one**: When applying `len` safe steps we move from `cur_pos` to `cur_pos+len`; the mask after those steps corresponds to the new position.

**Alternative ideas**  
- BFS on safe intervals with a DP that keeps the set of reachable positions modulo some period, but the binary‑lifting method is simpler and fits the constraints (`B` small, `M` moderate).  
- Could treat the problem as a reachability in a directed graph on safe squares and use segment‑tree techniques, but the mask DP is the most direct.

## worker: finalize
The solution uses a **bitmask DP** with binary lifting.

*   A mask of `B` bits represents which of the last `B` squares are reachable.
*   For a **safe** square the transition is deterministic and can be expressed as  
    `new_mask = ((old_mask << 1) & ALL) | (any of bits A‑1 … B‑1 set ? 1 : 0)`.
*   For a **bad** square the transition is a left shift (or zero if the block length ≥ B).
*   The line is split into alternating safe and bad intervals (at most `M+1` of them).  
    Each safe interval of length `L` is processed in `O(log L)` time by composing the
    pre‑computed `2^k`‑step tables (`nxt[k]`).  
    Bad intervals are handled in `O(1)`.
*   The algorithm is linear in the number of intervals (≤ 2·10⁴) and logarithmic in the
    interval lengths, easily fitting the limits (`B ≤ 20`, `N ≤ 10¹²`).  
    Memory usage is about `2^B · log₂ N` 32‑bit integers (≈ 160 MiB for the worst case).

The proof of correctness follows from Lemma 1–8: the mask always encodes the exact
set of reachable squares among the last `B` positions, and the final LSB tells
whether square `N` is reachable.
