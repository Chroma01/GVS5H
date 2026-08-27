
## ideation
**Restating the reduction (the plan's math checks out, verified below).**

Entry $(i,j)$ of $B^p$ = sum over walks $i=v_0\to v_1\to\dots\to v_p=j$ of $\prod_t B_{v_t,v_{t+1}}$. Summing over all $B$: each zero-cell $e$ becomes a free variable $x_e\in\{1,\dots,p-1\}$ appearing with multiplicity $m_e$ (the number of times the walk traverses that cell), and
$$\sum_{x=1}^{p-1}x^{m}\equiv \begin{cases}-1 & (p-1)\mid m\ \text{(including }m=0)\\ 0&\text{otherwise}\end{cases}\pmod p .$$
So the whole sum $=(-1)^K\sum_{\text{"valid" walks}}\prod(\text{fixed }A\text{ entries})$, where valid means every zero cell is used a multiple of $(p-1)$ times (0 allowed). **Key point: the unused zero cells each give a factor $-1$, which is exactly what produces the global $(-1)^K$.**

Walk length is exactly $p$, so for $p\ge 3$ the multiset of zero-cell usages is either:
1. all zero → walk uses only nonzero cells → total contribution $= (A^p)_{i,j}$ (with zeros literally 0, since those terms vanish anyway);
2. exactly one zero cell used $p-1$ times, plus one step on some other cell (2(p−1) ≤ p only if p ≤ 2; m = p needs (p−1)|p, impossible for p ≥ 3).

Enumerating case 2 geometrically:
- **Zero self-loop $(a,a)$**: the $p-1$ loop steps are all at vertex $a$; the single extra step cannot sit strictly between two loops (it would have to start and end at $a$, i.e. be the loop itself). Hence it is first or last:
  - first: walk $i\to a$ then loops, so $j=a$: add $A_{i,a}$ to entry $(i,a)$ for every $i$ (rows contribution: column $a$ of answer $+=$ column $a$ of $A$);
  - last: $i=a$, loops, then $a\to j$: add $A_{a,j}$ to entry $(a,j)$ (row $a$ of answer $+=$ row $a$ of $A$).
  (Entries of $A$ that are 0 contribute 0, which is exactly right because such an extra step would be a second zero cell used once → invalid.)
- **Zero cell $(a,b)$, $a\neq b$**: using it $p-1$ times forces $\ge p-2$ returning steps $b\to a$, but only 1 extra step is available, so $p\le 3$. For $p=3$ the unique walk is $a\to b\to a\to b$ with the extra step $(b,a)$: add $A_{b,a}$ to entry $(a,b)$.

Final answer $=(-1)^K\bigl(A^p+\text{corrections}\bigr)\bmod p$.

**Verification on sample 1** ($N=2,p=3,A=[[0,1],[0,2]]$, $K=2$ so sign $+1$): $A^2=[[0,2],[0,1]]$, $A^3=[[0,1],[0,2]]$. Zero self-loop $(1,1)$: column-1 contribution $A_{i,1}=0$; row-1 contribution adds $A_{1,2}=1$ to $(1,2)$. Zero cell $(2,1)$, $a\ne b$, $p=3$: adds $A_{1,2}=1$ to $(2,1)$. Total $[[0,2],[1,2]]$ = expected output. ✔

**Sample 2** is $p=2$: only one $B$ (all zeros→1), answer $=M^2 \bmod 2$. ✔ (The general derivation degenerates at $p=2$ since $p-1=1$ makes every walk valid — just special-case it.)

**Main implementation difficulty: computing $A^p \bmod p$ with $N=100$, $p\le 10^9$.**
- ~30 squarings + up to 30 multiplies of $100\times100$ matrices → must use numpy (pure Python $6\times10^7$ inner ops is too slow).
- Overflow: entries $<p<2^{30}$, product $<2^{60}$, summing 100 of them overflows int64. Use the 15-bit split: `A = Ah*2^15 + Al` with `Ah = A>>15 < 2^15`, `Al = A & 0x7fff`. Then `Ah@B < 2^15·2^30·100 < 2^52` (safe); reduce mod p **before** shifting left by 15 (otherwise `<<15` overflows), then add `(Al@B)%p` and reduce.
- Make sure dtype is int64 (`np.int64`), and that `p` is a Python int used carefully (numpy `%` with int64 is fine).

**Pitfalls list**
- Don't forget the $(-1)^K$ factor (parity of number of zeros); apply as `(-1)**(K&1)` mod p.
- $p=2$ must be a separate branch.
- $p=3$ needs BOTH the self-loop corrections and the off-diagonal $(a,b)\mapsto A_{b,a}$ corrections.
- For $p\ge5$ only self-loop corrections.
- Corrections must be added to $A^p$ *before* multiplying by the sign, and everything reduced mod p.
- $N=1$ edge case works (check: $A_{1,1}=0$, odd $p$ → answer 0 since $\sum_{x} x^p = \sum x \equiv 0$).
- Input parsing: read all tokens at once (`sys.stdin.buffer.read().split()`).
- Output: N lines, space-separated, values in $[0,p)$.

## worker: Write the complete Python program end-to-end: read
Implemented the plan exactly:

- **Math**: Sum over all B of $(B^p)_{i,j}$ equals $(-1)^K\sum_{\text{valid walks}}\prod A$-entries, where a walk of length $p$ is valid iff each zero cell is traversed a multiple of $(p-1)$ times. For $p\ge3$ only two families exist: walks avoiding zero cells entirely (giving $A^p$ with zeros left as 0), and walks using exactly one zero cell $p-1$ times plus one non-zero-cell step. The latter is only realizable for a zero self-loop $(a,a)$ (extra step first: adds $A_{i,a}$ to entry $(i,a)$; extra step last: adds $A_{a,j}$ to entry $(a,j)$), and additionally, when $p=3$, for a zero off-diagonal cell $(a,b)$ via walk $a\to b\to a\to b$ adding $A_{b,a}$ to entry $(a,b)$.
- **p=2** special branch: unique B (all zeros→1), answer $M^2 \bmod 2$.
- **Matrix power** with numpy int64 and the 15-bit hi/lo split; `(Xh@Y)` is reduced mod p *before* the `<<15` shift so no int64 overflow ($2^{15}\cdot2^{30}\cdot100<2^{52}$, and after reduction the shift gives $<2^{45}$).
- Corrections are accumulated in a separate matrix `C` from the *original* $A$ (mod p), added to $A^p$, then the global sign $(-1)^K$ is applied and everything reduced into $[0,p)$.
- Pure-Python fallback included if numpy is unavailable.
- Hand-verified against sample 1 ($[[0,2],[1,2]]$) and sample 2 as described in the plan; $N=1$ and $p=3$ off-diagonal cases handled.
