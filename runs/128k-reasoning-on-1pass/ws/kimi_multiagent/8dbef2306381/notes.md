
## ideation
Core difficulty is `N` up to `1e12`, so any per-square DP is impossible; but `M <= 2e4`, bad intervals are sorted/disjoint, and step lengths are tiny (`1 <= A <= B <= 20`). The problem should reduce to local reachability over compressed good/bad regions.

Key structural observations to verify:
- If `A == B`, movement is fixed-step `d`: reachable squares are exactly `1 + kd`. Need `(N-1) % d == 0` and no bad square `j` with `j ≡ 1 mod d`.
- If `A < B`, the allowed step lengths include consecutive integers, so gcd is `1`; long good regions should eventually become “saturated.”
- A contiguous bad interval `[L,R]` of length `len = R-L+1` can be crossed only if some jump from `<L` to `>R` has length at most `B`. The shortest possible crossing jump is `(R+1)-(L-1) = len+1`, so `len >= B` is immediately impossible. This matches the plan’s early rejection, but the off-by-one must be proved carefully.
- Because `B <= 20`, a sliding-window DP over a compressed coordinate array is attractive: `f[x]` depends only on `f[x-B .. x-A]`, so maintain a count of reachable predecessors in that window.
- The main subtlety is choosing a safe cap `C` for long good gaps. The plan’s `k0 = ceil((A-1)/(B-A))`, `T = A*k0`, `C = T + 2B` is plausible but needs a rigorous invariant: after enough consecutive good squares, reachability becomes periodic/all-ones sufficiently far ahead, so truncating a long good gap cannot change whether the final side is reachable.
- Final gap needs special handling: if the tail good region before `N` is longer than the cap, reaching `N` should be equivalent to having any reachable state in the represented prefix/saturated region; otherwise check exact `f[N]`.

Pitfalls:
- Off-by-one errors in 1-based indexing, dummy index 0, and window `[x-B, x-A]`.
- Mishandling `M=0`: one long good gap from `1` to `N`.
- Forgetting that squares `1` and `N` are guaranteed good by constraints, but moves still cannot land inside bad intervals.
- Assuming `len > B` instead of `len >= B` for uncrossable bad intervals.
- Compressing too aggressively without proving saturation; too conservatively may still be fine because `B <= 20`, but proof is needed.
- Fixed-step case must be separated before using consecutive-step/gcd arguments.

## worker: Implement the complete solution (A==B modular chec
- For `A == B`, every reachable square has the form `1 + kA`. The answer is `Yes` exactly when `N` has this form and no bad square does.
- For `A < B`, touching bad intervals are merged because the input permits adjacency. A contiguous bad block of length at least `B` requires a jump of at least `length + 1`, so it is impossible to cross.
- Sums of `k` allowed jumps cover every integer in `[kA, kB]`. Once `k(B-A) >= A-1`, consecutive such intervals touch. Thus every offset at least `T = A * ceil((A-1)/(B-A))` is representable.
- In any good gap, the first reachable square after a bad block must occur within the first `B` squares. After at most `T` further good squares, reachability becomes saturated. Therefore a good gap longer than `C = T + 2B` can be replaced by its length-`C` prefix while preserving the reachable states relevant to the next bad block.
- For a long final gap, any reachable square in the retained prefix implies an early reachable entry into the original final gap; since `N` is more than `T` away from that entry, `N` is reachable.
- The sliding-window DP maintains the number of reachable squares in `[x-B, x-A]` in `O(1)` per compressed square.
- Validated against an exhaustive per-square DP oracle on small exhaustive bad-square subsets and randomized cases including `A == B`, adjacent bad intervals, empty interval lists, and gaps around the compression threshold.
- Complexity is `O(M + compressed_length)`, with `compressed_length <= (M+1)C + M(B-1) <= about 8.1e6`, and `O(compressed_length)` memory.
