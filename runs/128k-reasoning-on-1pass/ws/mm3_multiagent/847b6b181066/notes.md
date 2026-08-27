
## ideation
**Core difficulty**  
The smoke spreads by a uniform translation at each time step (the wind direction), and new smoke is added at the origin only when it is empty. We need to know, after each translation, whether the query cell (R, C) contains any smoke. Direct simulation of positions would require tracking up to N+1 particles and would be O(N²) in the worst case, so we need a way to represent the whole set of smoke cells implicitly.

**Key observation – relative coordinates**  
If we keep a global offset **O(t)** = total displacement caused by winds up to time t, then every smoke particle that was generated at some earlier time `k` (0 ≤ k ≤ t) has absolute position  
`abs = O(t) – O(k)`.  
If we store all generated particles as *relative* coordinates with respect to the current offset, i.e. the pair `s = –O(k)`, then the absolute position at time t is simply `O(t) + s`.  
Thus we can maintain a set `rel` of these relative coordinates, updating the offset each step, and answer membership queries for (R, C) by checking whether `(R‑O.r, C‑O.c) ∈ rel`.

**Stepwise process**  
For each `t = 1 … N`:
1. Update the global offset according to the wind character `S[t]`.
2. Query: does `(R‑O.r, C‑O.c)` belong to `rel`? → output `1` or `0`.
3. Generation rule: a new particle is created at the origin iff the origin (0, 0) is empty, i.e. iff `(-O.r, -O.c) ∉ rel`. If so, insert this relative coordinate into `rel`.

All set operations are O(1) average time using a Python `set`, so the whole algorithm runs in O(N) time and O(N) memory.

**Pitfalls to watch for**
- Off‑by‑one timing: smoke is present at time `t+0.5` **after** the wind has moved all existing particles but **before** the possible generation at the origin. The order in the plan (update offset → query → maybe generate) correctly matches this.
- The query cell (R, C) is guaranteed to be different from (0, 0), but the generation condition must still check the origin correctly.
- Coordinates can become as large as ±N (or a bit more because of cumulative offsets), which fits comfortably in Python integers.
- Input size up to 200 000 – the set may hold up to N+1 elements, which is fine.
- Use fast I/O (`sys.stdin.readline`) to avoid timeouts.
- Output must be a single string of length N, no extra spaces or newlines beyond the final newline.

**Alternative approaches considered**
- *Direct simulation of each particle*: would be O(N²) and infeasible.
- *Using a grid (2‑D array) of size (2N+1)²*: also O(N²) memory/time, too large.
- *Binary indexed tree / interval tree*: not needed because the transformation is a simple translation; the relative‑coordinate trick already yields O(1) per step.

## worker: Parse the three integers `N, R, C` and the wind st
The wind moves **all** smoke uniformly, which is equivalent to keeping a global offset `O` that records the cumulative displacement.  
Each smoke particle generated at time `k` has absolute position `O(t) - O(k)`.  
If we store the constant part `s = -O(k)` for every generated particle, the absolute position at time `t` becomes `O(t) + s`.  

Thus we maintain:
* `off_r, off_c` – the current offset `O(t)`.
* a set `rel` of the stored constants `s = -O(k)` for all generations.

At each step:
1. Update the offset with the current wind direction.
2. Check whether `(R, C)` is occupied: it is present iff `(R - off_r, C - off_c) ∈ rel`.
3. Generate a new particle at the origin only if the origin is empty, i.e. iff `(-off_r, -off_c) ∉ rel`.

All operations are O(1) average, giving an overall O(N) algorithm with O(N) memory.  
The solution was verified against the provided samples.
