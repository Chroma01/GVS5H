
## ideation
**Restating.** Operations only set bits to 1, so order is irrelevant and the problem is pure set cover: choose a sub‑multiset of the M available sets (set of op *i* is either `[L_i,R_i]` (op1) or its complement (op2)) whose union is `[1,N]`, minimizing the number of chosen operations. Each index may be used at most once (with one of the two "paying" modes).

**Core insight (why it's easy).** The optimal cost is only ever 1, 2, 3, or −1; no covering DP/greedy is needed.

- Cost 0: impossible (N ≥ 1).
- **Cost 1**: only op1 with `[L_i,R_i] = [1,N]` (op2 can never cover everything since intervals are nonempty).
- **Cost 2**, exactly three shapes:
  - op1+op1: `[L_i,R_i] ∪ [L_j,R_j] = [1,N]` ⟹ need i with L=1 (take max R among these), j with R=N (take min L among these), and `R_i + 1 ≥ L_j`. After the cost‑1 check no interval is `[1,N]`, so i ≠ j automatically.
  - op1(i)+op2(j), i ≠ j: complement(I_j) ∪ I_i = full ⟺ `I_j ⊆ I_i` (containment pair, duplicates count).
  - op2+op2: complement(I_i) ∪ complement(I_j) = complement(I_i ∩ I_j) = full ⟺ the two intervals are **disjoint**.
- **Cost 3 (M ≥ 3, none of the above)**: let a = argmin R, b = argmax L. Then a ≠ b (if the same index held both min R and max L, every other interval would contain it → containment case already fired; M ≥ 3 ⟹ another exists). Since no disjoint pair, `L_b ≤ R_a`, so `I_a ∩ I_b = [L_b, R_a]`. For **any** third index c, `L_c ≤ L_b` and `R_c ≥ R_a`, hence `I_a ∩ I_b ⊆ I_c`. So op2 on a, op2 on b, op1 on any c ≠ a,b always works. Note this argument doesn't even need the antichain reasoning — it only needs a≠b and non‑disjointness.
- **−1**: M ≤ 2 and no cost‑1/cost‑2 certificate (with M ≤ 2 the total budget is ≤ 2 ops, so if no 1‑ or 2‑op solution exists it's impossible).

**Verification on samples (mental):** S1 → containment `[2,4]⊆[1,4]` gives `2 0 1 0` (cost 2 ✓). S2 → `[1,5]` gives cost 1 ✓. S3 → L=1 max R = 3, R=5 min L = 2, 3 ≥ 1 ⟹ `1 1` ✓. S4 → nothing, M=2 ⟹ −1 ✓.

**Implementation details / pitfalls.**
- Containment detection in O(M log M): sort indices by (L asc, R desc); scan keeping the best (max R, index); if current R ≤ bestR then bestIdx's interval contains current → answer. Ties in L must be sorted R desc so the earlier one is the container; equal intervals also correctly detected.
- Disjoint pair: use argmin R and argmax L; they are disjoint iff `L_max > R_min`. Only trust this after the containment check (so the two indices differ); or explicitly check index inequality.
- Order of cost‑2 checks doesn't matter — any valid witness is accepted.
- Watch N = 1 (every interval is `[1,N]` → cost 1), and M = 1, M = 2 edge cases.
- Output: `K` on one line, then M values separated by spaces on the next line; build with `' '.join`, single `sys.stdout.write`.
- I/O: `sys.stdin.buffer.read().split()`; 200k pairs — build L, R arrays via slicing of the token list mapped to int for speed; avoid per‑line reads.
- Don't allocate anything of size N (N up to 10^6, fine, but unnecessary) — algorithm is O(M log M) or even O(M) if containment is found via sorting-free tricks (sorting is fine).

**Possible traps to double check.** (1) Using the same operation index twice (e.g. op1 and op2 on the same i) is illegal — enforce i ≠ j everywhere. (2) The "two op1" case must also allow adjacency (`R_i + 1 = L_j`), not just overlap. (3) Make sure containment check considers i ≠ j but identical intervals are allowed. (4) Cost 3 construction must pick c distinct from a and b.

## worker: *Implement the complete solution in one file:** fa
Implemented exactly the planned case analysis:

1. **Cost 1**: some interval equals `[1,N]` → op1 there.
2. **Cost 2, op1+op1**: take the interval starting at 1 with maximum R (`best_i`) and the interval ending at N with minimum L (`best_j`). Since step 1 failed, no interval is `[1,N]`, so `best_i != best_j` automatically (checked anyway). Union is full iff `R[best_i]+1 >= L[best_j]`; choosing extremes is optimal among such pairs.
3. **Cost 2, op1+op2**: complement(I_j) ∪ I_i = full ⟺ `I_j ⊆ I_i`. Detected by sorting indices by `(L asc, R desc)` and sweeping with running max R: the first index whose R ≤ running max is contained in the recorded container (its L is ≤ current L because of the sort, ties broken so the larger-R interval comes first). Equal intervals are detected too, and container index ≠ contained index.
4. **Cost 2, op2+op2**: complement(I_i)∪complement(I_j) = complement(I_i∩I_j) = full ⟺ intervals disjoint ⟺ argmax L's L > argmin R's R (with distinct indices).
5. **Cost 3**: if none of the above and M ≥ 3, then `a = argmin R`, `b = argmax L` are distinct (if the same index carried both, it would be contained in every other interval and case 3 would have fired for M ≥ 2), and they intersect (case 4 failed), so `I_a ∩ I_b = [L_b, R_a]`. Any third interval c satisfies `L_c ≤ L_b` and `R_c ≥ R_a`, hence contains `[L_b, R_a]`. So op2 on a, op2 on b, op1 on c covers everything.
6. Otherwise M ≤ 2, and with at most 2 operations no 1- or 2-op solution exists → `-1`.

Complexity O(M log M) time, O(M) memory (nothing proportional to N is allocated). Fast I/O with a single `read().split()` and a single `stdout.write`.

Mental sample checks: S1 → containment `[2,4] ⊆ [1,4]` → `2 / 2 0 1 0`-equivalent valid witness; S2 → `[1,5]` cost 1; S3 → `R=3, L=2`, 3+1≥2 → cost 2 with both op1; S4 → no case fires, M=2 → −1.
