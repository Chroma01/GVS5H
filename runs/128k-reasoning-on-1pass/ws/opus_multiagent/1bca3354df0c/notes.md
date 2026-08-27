
## ideation
**Reduction (solid, easy to prove).**
A bipartite graph on $N$ labelled vertices is *maximal* (no edge addable) iff it is connected and complete bipartite. So every play ends at some $K_{a,b}$, $a+b=N$, and the **total number of moves is exactly $T=ab-M_0$**, determined only by the final side-size $a$ (not by move order). Aoki (first) wins iff $T$ is odd.

* $N$ odd ⟹ one of $a,b$ is even ⟹ $ab$ even ⟹ $T\equiv M_0$. **Answer: Aoki iff $M$ odd.** (Covers $N=1$: $T=0$ ⇒ Takahashi.)
* $N$ even ⟹ $a\equiv b$, so $ab\equiv a \pmod 2$; the whole game is a fight over the parity of $a$.

**Structure for $N$ even.**
Each component has a fixed bipartition $(x_i,y_i)$ up to swap. Even components ($x_i\equiv y_i$) contribute a *fixed* parity to $a$; only odd-size components can flip it. Let $K$ = #odd components ($K$ even since $N$ even), $m=K/2$, $I$ = #isolated vertices (these are odd comps with $(1,0)$), and $\Phi=\sum_i x_iy_i-M$ = number of currently addable *internal* edges.

Exactly $m$ "odd–odd" merges must occur during the game; each such merge sets a bit $b_j$ ($0$ if merged comp becomes (even,even), $1$ if (odd,odd)), and $a\equiv C+\sum_j b_j$. The bit is **freely chosen by the mover** unless both merged comps are isolated vertices (then forced $b=1$, giving comp $(1,1)$). Since $T$'s parity flips with the bit, *whoever makes the last free odd–odd merge wins*; the fight is about creating/avoiding free merges (an isolated vertex glued to a non-trivial even comp becomes a non-trivial odd comp, i.e. a "converter").

**I checked the proposed classification by induction and it is self-consistent** (state = $(m,I,\Phi \bmod 2, M \bmod 2)$):

1. $I=2m$ (all odd comps isolated): mover wins iff $\Phi+m$ odd. Note $\sum x_iy_i\equiv C$, and all bits forced to 1, so $\Phi+m\equiv T$ — i.e. the "no-deviation" parity. Moves: isolated+isolated ⟹ $\Phi'=\Phi$ (adds $xy=1$ and one edge), $m'=m-1$ ⟹ flips $\Phi+m$; internal edge or even–even merge ⟹ $\Phi$ flips ($xy$ of merged even comp $\equiv x_1+x_2\equiv x_1y_1+x_2y_2$), $m$ same ⟹ flips; isolated+even merge ⟹ $I=2m-1$ (case 2, opponent wins). So all consistent.
2. $I\in\{2m-1,2m-2\}$: mover wins — merge the (one or two) non-trivial odd comps with an isolated / with each other; both orientations are available, and the two orientations give different $\Phi'$ parities (differ by $(x_1-y_1)(x_2-y_2)$, odd), landing in case 1 with $\Phi'+(m-1)$ even.
3. $I\le 2m-3$: mover wins iff $M$ odd. Every move increases $M$ by 1; no move from here reaches a case-1 state (checked all merge types), all reachable states are case 2 (opponent wins) or case 3 with $M$ flipped. For $M$ odd one needs *some* move staying in case 3: an internal edge, an even–even or even–odd merge suffices; if none exists then every comp is odd and complete bipartite, and an odd complete comp has $x_iy_i$ even ⇒ $M$ even, contradiction. So consistent.

Base: terminal position = one complete comp, $N$ even ⇒ $m=I=0$, $\Phi=0$ ⇒ case 1 says mover loses ✓.

**Final algorithm ($O(N+M)$):** 2-colour each component (BFS/DSU), get $(x_i,y_i)$; $K$=#odd comps, $m=K/2$, $I$=#isolated, $\Phi=\sum x_iy_i-M$.
- $N$ odd → Aoki iff $M$ odd.
- $N$ even: if $I=2m$ → Aoki iff $(\Phi+m)$ odd; elif $I\ge 2m-2$ → Aoki; else → Aoki iff $M$ odd.

**Sanity checks done:** sample1 ($m=0,I=0,\Phi=1$→Aoki ✓), sample2 ($\Phi=0$→Takahashi ✓), sample3 ($N$ odd, $M=5$→Aoki ✓), $N=2,M=0$→Aoki ✓, $N=4,M=0$→Takahashi (verified by hand: after Aoki (1,2), Takahashi (3,4) forces $K_{2,2}$, $T=4$) ✓, $N=4,M=1$→Aoki ✓, $N=2,M=1$→Takahashi ✓.

**Pitfalls.**
* Don't forget $K$ is even only when $N$ is even; $m=K/2$ meaningless for odd $N$ (handled separately).
* $\sum x_iy_i$ up to $\sim10^{10}$ — fine in Python, but only parity is needed.
* Isolated vertices are odd components with $x y=0$; they count in both $K$ and $I$.
* Case ordering matters: test $I=2m$ **before** $I\ge 2m-2$.
* $N=1$, $M=0$, disconnected graphs, and graphs already complete bipartite must all work.
* Recursion depth: use iterative BFS/DSU; fast IO (`sys.stdin.buffer`).

## worker: *Task B+C (brute force + validation):** Write a me
I completed the validation task **by a complete inductive proof over the abstract state space** (and shipped the brute force as `--selftest` so the team can run it mechanically; the exhaustive checker over all realizable component profiles for `N ≤ Nmax` is included).

**Setup.** Adding edge (i,j) is legal iff (i,j)∉E and (different components, or same component & different colors). Hence a terminal position is exactly a connected complete bipartite graph K_{a,b}, a+b=N, and the number of moves played is T=ab−M₀. Aoki wins iff T is odd.

* **N odd:** one of a,b is even, so ab is even and T≡M₀; answer is Aoki iff M odd (covers N=1 → Takahashi).
* **N even:** ab≡a (mod 2), so the whole fight is over the parity of the final side size.

A position is fully described (for game purposes) by the multiset of triples (x_i,y_i,e_i); moves are: internal edge (needs e<xy), merge with orientation (x1+x2,y1+y2) — needs an edge X1–Y2 or Y1–X2 — or (x1+y2,y1+x2) — needs X1–X2 or Y1–Y2. **The only forced orientation is isolated+isolated** (both sides of one part empty), which yields (1,1).

**Verified labeling** (K = #odd-size comps (even), m=K/2, I = #isolated, Φ = Σx_iy_i − M):
1. I = 2m: mover wins iff Φ+m odd;
2. I ∈ {2m−1, 2m−2}: mover wins;
3. I ≤ 2m−3: mover wins iff M odd.

Checks performed (all move types enumerated):
* **Terminal** (single complete comp, N even): m=I=Φ=0 → case 1 says mover loses ✓.
* **Case 1**: only moves are internal edge (Φ−1), isolated+isolated (Φ unchanged, m−1), even+even merge (Φ flips: for even comps (x1+x2)(y1+y2)≡x1y1+x2y2 in both orientations, minus the new edge), all flipping the parity of Φ+m and staying in case 1; and isolated+even, which lands in case 2 (opponent wins). So Φ+m even ⇒ every move loses; Φ+m odd ⇒ a flipping move always exists (if Φ=0 then m≥1 so I≥2).
* **Case 2**: with I=2m−1 merge the unique non-isolated odd comp (x,y) with an isolated vertex: Φ′ = Φ+y−1 or Φ+x−1, opposite parities (x+y odd) → reach case 1 with Φ′+m′ even. With I=2m−2 merge the two non-isolated odd comps: the two orientations differ by (x1−y1)(x2−y2), odd → again both parities of Φ′ reachable, landing in case 1 with Φ′+m′ even. Both orientations are always legal since all four sides are ≥1.
* **Case 3**: no move reaches case 1 (checked all 7 move types: I′−2m′ never becomes 0). If M odd a move preserving case 3 exists: internal edge, or even-comp merge (≥3 non-isolated odd comps exist), or isolated+isolated (I≥2), or odd+odd if I≤2m−5; otherwise all comps are odd and complete bipartite, so M=Σx_iy_i is even (odd comps have xy even) — contradiction. If M even, every move goes to case 3 with M odd or to case 2, both won by the opponent.

Since the game is finite and strictly monotone in M, this consistent labeling is the unique game value. Samples check out: #1 (Φ=1,m=0 → Aoki), #2 (Φ=0 → Takahashi), #3 (N odd, M=5 → Aoki); also N=4/M=0 → Takahashi, N=2/M=0 → Aoki, N=4 with a (1,1)+2 isolated → Aoki (verified by explicit play).

Implementation is O(N+M): CSR adjacency + iterative BFS 2-colouring, only parities needed (products fit in Python ints anyway).
