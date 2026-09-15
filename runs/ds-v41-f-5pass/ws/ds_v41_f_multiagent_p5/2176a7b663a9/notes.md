- **Problem model:** vertices are closed intervals [L_i,R_i]; edge iff intervals are disjoint (R_i<L_j or R_j<L_i). Path weight = sum of vertex weights (all >=1). Answer = min-weight s-t path or -1.
- **Core theorem (proved, airtight):** For overlapping s,t, if any path exists then one of length <=3 exists. Given a path s=v0,...,vk=t (k>=3), look at v1 (adj s) and v_{k-1} (adj t):
  - v1 adj s => R1<Ls (A) or L1>Rs (B). v_{k-1} adj t => R2<Lt (C) or L2>Rt (D).
  - (A)&(C): one of R1<min(Ls,Lt) or R2<min(Ls,Lt) must hold, so a single left-of-both intermediate beats it.
  - (B)&(D): symmetric, a right-of-both intermediate beats it.
  - (A)&(D): v1 is left-of-s and v2 right-of-t; overlap guarantees R1<Ls<=Rt<L2, so they are disjoint => valid s-v1-v2-t.
  - (B)&(C): symmetric, valid s-v1-v2-t.
  Hence path weight >= W_s+W_t+(one of the three candidate structures), and each candidate is a realizable path, so the minimum is attained among them. Same-side length-3 pairs (A,C)/(B,D) are always dominated by a length-2 candidate.
- **Disjoint case:** if Rs<Lt or Rt<Ls, direct edge is optimal since weights are positive (any longer path adds positive weights).
- **Enumerated candidates m (extra weight):**
  1. single intermediate left of both: bestR[min(Ls,Lt)]; right of both: bestL[max(Rs,Rt)].
  2. left of s + right of t: bestR[Ls] + bestL[Rt].
  3. right of s + left of t: bestL[Rs] + bestR[Lt].
  Answer = W_s+W_t+m, or -1 if m stays INF.
- **Candidate validity in overlap:** bestR[Ls] excludes s,t (their R>=Ls since Ls<=Rt); bestL[Rt] excludes s,t similarly; bestR[min] and bestL[max] also exclude both. Candidate-2 pair is disjoint since R1<Ls<=Rt<L2; candidate-3 pair since R<Lt<=Rs<L. So counts use only genuine extra vertices.
- **Precompute:** M=2N. bestR[c]=min W with R_u<c via forward sweep (min of bestR[c-1], minAtR[c-1]); bestL[c]=min W with L_u>c via backward sweep (min of bestL[c+1], minAtL[c+1]). Arrays sized M+2, sweep covers 0..M+1 so all query indices (<=M) are valid. O(N) build, O(1) per query.
- **Pitfalls:** sentinel INF=1<<60; TH=INF>>1 to detect "nonexistent" (<1e18 threshold, real weights <=1e9). Use integer compare for min (no min() overhead needed but fine). Self-contained stdin/stdout.
- **Verification:** both samples reproduced exactly: sample1 -> 11,6,-1; sample2 -> 157,124,-1,114,114. Manual case analysis (above) confirms the <=3-edge reduction and that no 4+ edge path can beat the candidates; brute-force-style reasoning on constructed small examples (overlap/no-path, large coordinate gaps, both sides) matches the four-branch logic.
