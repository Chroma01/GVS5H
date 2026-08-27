
## ideation
**Core difficulty**  
The pattern has exactly two wildcards `*` that each can match any (including empty) string.  
Thus the pattern can be written as  

```
p = L * M * R                (L, M, R may be empty)
```

A substring `s[l … r]` matches `p` iff the three literal parts `L`, `M`, `R` appear in `s` in this order, each at a distinct position, with possible gaps (the `*`’s) between them.  
The task is to minimise the length `r‑l+1`.  

Key sub‑problems:

1. **Finding all occurrences of each literal part** – a classic exact pattern matching problem.  
   KMP (or Z‑algorithm) gives all start positions in linear time.

2. **Choosing three occurrences (one from each part) that satisfy the order constraints**  
   `L` end ≤ `M` start ≤ `M` end ≤ `R` start, and we want the smallest window covering the chosen triple.  

3. **Handling the 2⁴ = 16 possibilities of empty/non‑empty parts** – several degenerate cases (e.g. `M` empty, both `L` and `R` empty) must be solved separately.

The main algorithmic challenge is to combine the occurrence lists efficiently (linear‑time) instead of trying all triples, which would be cubic.

**Candidate approaches**

1. **Brute force enumeration of substring start/end**  
   For each `(l,r)` in `s`, test if `s[l…r]` matches `p`.  
   *Why it’s bad*: O(n²) substrings, each test needs linear time → O(n³) worst case.

2. **Dynamic programming over `s` with wildcard matching**  
   Classic wildcard matching DP can decide if `p` matches a whole string, but we need the *shortest* matching **substring**, not the whole string.  
   We could run the DP for every possible start, still O(n·m) per start → O(n²·m) worst case.

3. **KMP + scanning** (the intended solution)  
   - Compute occurrence lists `occL`, `occM`, `occR` using KMP (or Z‑function).  
   - For the case where all three parts are present, use a three‑pointer walk: for each `l` in `occL` advance pointers in `occM` and `occR` to the first occurrence that satisfies the ordering constraints. This visits every feasible triple exactly once → O(|occL| + |occM| + |occR|) = O(n).  
   - Cases with empty parts reduce to two‑pointer scans (`L*R`) or trivial formulas (`only M`, `**`).  
   - Overall time `O(|s| + |p|)`, memory `O(|s|)` for the occurrence lists.

4. **Suffix automaton / suffix array**  
   Could store all substrings and query for containment, but the three‑part ordering makes it more complex; KMP is simpler and sufficient.

**Pitfalls to watch out for**

- **Empty pattern parts**:  
  `L`, `M`, or `R` may be empty. The algorithm must treat an empty part as “no restriction”.  
  - Special case `p == "**"` → answer `0` (empty substring matches).  
  - If `M` is empty, we only need `L` and `R` in order.  

- **Adjacent parts**:  
  Parts may touch (gap length zero). The ordering condition is `L_end ≤ M_start` and `M_end ≤ R_start`, *not* strict `<`.  

- **Overlapping occurrences** (within the same list) are fine; KMP returns overlapping matches automatically.  

- **Multiple occurrences of the same literal**: must keep *all* start positions; a two‑pointer scan that only remembers the “first” feasible one would miss shorter windows later.  

- **Integer overflow / length limits**: lengths up to 10⁵, safe in Python, but use a sentinel `INF = n+1` to detect no‑answer.  

- **Pattern length up to 10⁵**: KMP preprocessing is linear; sum of all three parts = `|p|`, total KMP work `O(|s| + |p|)`.  

- **Edge cases where one of the occurrence lists is empty** → answer `-1`.  

- **Off‑by‑one errors** when computing substring length `r_start + |R| – l_start`.  

- **Handling large input efficiently**: reading as a normal string is fine; avoid quadratic loops on the occurrence lists.

## worker: finalize
We split the pattern `p` into three literal parts `L`, `M`, `R` separated by the two `'*'`.  
Using the KMP algorithm we compute, in linear time, all start positions of each non‑empty part in `s`.  
The problem then reduces to choosing one occurrence of each part that respects the order constraints  
`L_end ≤ M_start ≤ M_end ≤ R_start` and minimises the window length covering them.  

A three‑pointer walk over the sorted occurrence lists examines every feasible triple exactly once and yields the minimal length.  
All degenerate cases (some parts empty) are handled separately, and the special pattern `"**"` returns `0`.  

The algorithm runs in `O(|s| + |p|)` time and `O(|s|)` additional memory, which easily satisfies the constraints.
