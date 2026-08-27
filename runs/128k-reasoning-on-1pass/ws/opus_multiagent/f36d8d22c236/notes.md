
## ideation
**Reduction.** Every operation acts on *letters*, never on positions, so all positions holding the same letter of `S` are forever tied together. Hence:
- For each `i`, letter `S[i]` must eventually become `T[i]`. If some letter `c` of `S` is required to become two different letters ⇒ `-1`.
- Otherwise we get a partial map `f` on the 26 letters, defined on `dom = set(S)`. `f` need **not** be injective (merging letters is allowed).

**Bucket model.** Think of 26 buckets; bucket `c` holds the set of positions currently labeled `c`. Operation `x→y` empties bucket `x` into bucket `y` (irreversible merge). Goal: bucket `v` must finally contain exactly the positions of `⋃{c : f(c)=v}`.

Group letters by target: `P_v = f⁻¹(v)`. Ideal cost:
- if `v ∈ P_v` (i.e. `f(v)=v`): `|P_v|-1` ops (merge everyone into `v`),
- else `|P_v|` ops (merge the group into one member — no emptiness needed since they share the same final target — then dump into `v`, which **requires bucket `v` to be empty**).

Summing: ideal total = `changed = #{c ∈ dom : f(c) ≠ c}`. This is also a lower bound (each non‑fixed letter needs ≥1 op with it as `x`).

**When is the ideal unattainable?** Choose for each nonempty group `P_v` with `v∉P_v` a *representative* `r` that does the final dump; all other members can be merged into `r` at time 0 (free, no constraint), so they become empty immediately. The only ordering constraint is: `dump(r_v)` must come after bucket `v` is emptied, and `v` is emptied by its own dump only if `v` is itself a representative. A deadlock = a cycle in the functional graph `c→f(c)` (length ≥2) in which **every node is forced to be the representative of the next group**, i.e. every cycle node has in‑degree exactly 1 (no tree edge entering the cycle). Such a cycle costs **+1** (break it with a temporarily free letter `z`: `a1→z, ak→a1, …, a2→a3, z→a2`; `z` is free again afterwards, so it can be reused for other cycles, but each cycle needs its own extra op because contents of different cycles have different targets and can never be merged).

⚠ **Major pitfall — the PLAN in the prompt is wrong**: it adds +1 for *every* cycle of length ≥2. Counterexample: `N=3, S="abc", T="baa"` (`f(a)=b, f(b)=a, f(c)=a`; cycle `a↔b`). Sequence `b→c` ("acc"), `a→b` ("bcc"), `c→a` ("baa") gives **3** ops, but `changed + allCycles = 4`. Because `indeg(a)=2` (both `b` and `c` map to `a`), the cycle is *not isolated* and costs nothing extra. Both given samples (1 and 4) fail to distinguish the two formulas (sample 4's 3‑cycle *is* isolated).

**So:** `answer = changed + (# cycles of length ≥ 2 in the functional graph all of whose nodes have in-degree exactly 1)`.

**Impossibility (besides inconsistency).** We need at least one bucket to become empty at some moment to break an isolated cycle. Initially free letters = letters not in `S`. If `|dom| = 26`, a letter can still be freed by an intra‑group merge, which exists iff `f` is **not** injective. If `|dom| = 26` and `f` is injective then `f` is a permutation of all 26 letters: any op would strictly decrease the number of distinct letters (impossible to restore, since `T` also needs 26 distinct letters) ⇒ `-1` (unless `changed = 0`, i.e. `S = T`, answer 0). Note: if `|dom|=26` and `f` injective then all in‑degrees are 1, so any non‑identity `f` has an isolated cycle — consistent.

Final decision procedure:
1. inconsistent map ⇒ `-1`;
2. `changed == 0` ⇒ `0`;
3. `|dom| == 26` and `f` injective ⇒ `-1`;
4. else `changed + #isolated_cycles`.

**Other pitfalls / details.**
- `f(c)` may be a letter **not** in `dom` (chain terminates there; that node has no outgoing edge) — cycle detection must handle nodes outside `dom`.
- In‑degree must count only preimages inside `dom` (i.e. `Counter(f.values())` over defined entries).
- Fixed points (`f(c)=c`) are length‑1 cycles — never charge extra.
- Order of checks: test `changed == 0` **before** the 26‑letter/-1 test.
- Performance: N ≤ 2·10⁵; use `sys.stdin.read()`; `set(zip(S,T))` has ≤676 elements and is O(N) — cheap. Everything else is O(26).

## worker: Write the final Python solution exactly as specifi
Implemented exactly the specified procedure.

Reasoning recap (matches the ideation notes, correcting the original PLAN):
- Operations act on letters, so `S[i] -> T[i]` induces a partial map `f` on the 26 letters; any conflict ⇒ `-1`.
- Lower bound: each letter `c` with `f(c) != c` must be the source `x` of at least one operation ⇒ `changed` ops.
- Grouping by target `v`, all members of `f^{-1}(v)` can be pre-merged into one representative for free (these merges are among the `changed` ops), and the representative's final dump into `v` requires bucket `v` to be empty. Deadlock arises exactly on a directed cycle of length ≥ 2 in which every node has in-degree 1 (no external letter merges into it and frees it early); each such isolated cycle costs exactly +1 (break via a temporarily free letter, which is released again and reusable across cycles).
- If `|dom| = 26` and `f` is injective (a permutation of all letters) and `f != id`, no letter can ever be freed while keeping 26 distinct letters ⇒ `-1`. Otherwise a free letter exists (unused letter, or freed by a non-injective merge).

Hand-verified outputs:
- Sample 1 `afbfda/bkckbb`: `f: a→b, b→c, d→b, f→k`, changed = 4, no cycle ⇒ 4 ✓
- Sample 2: changed = 0 ⇒ 0 ✓
- Sample 3: `a→a` and `a→r` conflict ⇒ -1 ✓
- Sample 4 `abac/bcba`: `a→b, b→c, c→a`, changed = 3, isolated 3-cycle ⇒ 4 ✓
- `("abc","baa")`: `a→b, b→a, c→a`, changed = 3, cycle `a↔b` has `indeg[a]=2` ⇒ not isolated ⇒ 3 (achievable: `b→c`, `a→b`, `c→a`) ✓
- `S == T` ⇒ 0 (checked before the -1 permutation test) ✓
- 26-letter non-identity permutation ⇒ -1 ✓
- 26 letters with a merge (image size < 26) plus an isolated 2-cycle ⇒ `changed + 1` ✓
- `N=1`, `"a"/"b"` ⇒ 1 ✓

Complexity: O(N + 26); `set(zip(S,T))` bounded by 676 pairs, cycle detection over ≤ 26 nodes.
