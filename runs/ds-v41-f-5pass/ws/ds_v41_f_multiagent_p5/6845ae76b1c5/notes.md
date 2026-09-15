- **Problem:** For K prefix queries (X,Y) output sum_{i<X, j<Y} |A_i - B_j|. N up to 1e5, K up to 1e4. Need sublinear-per-query; must use numpy to fit Python time.
- **Chosen approach (works, verified):** split indices into blocks of size S. Let bi=X//S, bj=Y//S, a0=bi*S, b0=bj*S. Then
  answer = P[bi][bj] + (i in [a0,X) vs j<b0) + (i<b0... i.e. i<a0 vs j in [b0,Y)) + corner.
  Precompute Uc and Vc as cumulative arrays so the two middle terms are O(1) lookups.
- **Definitions:** Uc[bj,t] = sum_{i<t} sum_{j<b0(j)}|A_i-B_j| with b0(j)=bounds[bj]; Vc[bi,t] = sum_{j<t} sum_{i<bounds[bi]}|A_i-B_j|. Both are (nblk+1) x (N+1) int64 with column 0 = 0.
- **Incremental build:** Uc[bj] = Uc[bj-1] + cumsum over i of contrib, where contrib[i] = sum over B-block of |A_i - b|. For a sorted block sb with prefix sums pb (len L+1) and idx=searchsorted(sb,A,side='right') = count of b <= A_i: contrib = A_i*(2*idx-L) + pb[L] - 2*pb[idx]. Vc symmetric with roles of A and B swapped.
- **Precompute P:** P[bi][bj] = Uc[bj, bounds[bi]] (full-block prefix). nblk^2 is tiny.
- **Per query:** ans = P[bi][bj] + (Uc[bj,X]-Uc[bj,a0]) + (Vc[bi,Y]-Vc[bi,b0]) + corner; corner = sum|a-b| over remA=A[a0:X], remB=B[b0:Y], computed by sorting remB, prefix sums, and the same searchsorted formula, vectorized over remA. Skip corner if either remainder empty.
- **Block size S:** nblk_target = min(64, int(sqrt(K))+1); S = ceil(N/nblk_target). Balances build cost O(N^2/S) against per-query O(S log S); keeps two int64 arrays under ~105 MB for N=1e5.
- **Numeric safety:** all sums stay in int64. Max answer 1e5*1e5*2e8 = 2e18 < 9.22e18. contrib terms <= ~4e13; Uc/Vc entries <= 2e18. Use int64 everywhere (int32 overflows).
- **Input parsing:** tokens from buffer.split() are bytes; int(bytes) works in Python. Convert A,B via np.array(list(map(int,...)),dtype=int64). Per-query tokens converted with int() in the loop.
- **Complexity:** build O(nblk*N*log S); per query O(log S) for O(1) parts plus O(S log S) corner. For N=1e5,K=1e4 this is ~1-2 s in numpy.
- **Pitfalls avoided:** no 4e7/1e9-sized dense structures; no per-element persistent-segment-tree queries (would be ~4e7 slow steps); O(1) middle terms via cumulative arrays instead of slice sums.
- **Superseded ideas:** Mo's algorithm, offline CDQ/Fenwick, and per-element PST remainder were dropped in favour of this blocking + cumulative-array scheme; direct persistent segment tree per rest element is too slow in Python.
