
## ideation
We have squares 1..N; some intervals are "bad" (cannot land on). From a current safe square x, we can jump to any safe square in [x+A, x+B] (provided x+i ≤ N). Starting at 1 (assumed safe because constraints say 1 < L_i), we want to know if we can eventually land exactly on N.

Key insight: Because A and B are small (≤20) and M is only up to 2·10⁴, but N is huge (≤10¹²), we can't DP over N. However, bad intervals are disjoint and sorted. The reachable set from a starting region is a contiguous interval of safe squares (because from any safe square within the reachable set, we can reach the same "frontier"). This is a classic "frog jump over bad zones" problem.

Greedy: maintain `right` = farthest safe index currently reachable, and `next_right` = farthest index we could possibly reach next step = `right + B`. But we need at least `A` distance per step, so if the current reachable front is at `right`, the next hop lands somewhere in `[max(right, prev_right)+A, right+B]`… Actually simpler: we simulate hop by hop but only when forced (i.e., at bad intervals).

Standard approach (used in AtCoder ABC-like problems):
- Let `ans` = current rightmost reachable safe square.
- For each bad interval [L, R]:
  - If `ans < L - 1`: we cannot even reach just before the bad interval → answer is No (stuck).
  - If `ans + B < L`: we need to make more jumps before the bad zone. Each additional jump extends reach by at most B, but we need to be able to step by at least A. We can greedily extend `ans` up to `min(ans + B, L-1)`… but careful: we can only land on safe squares. Since [L, R] is the next bad block, all squares in [ans+1, L-1] are safe. From `ans`, one hop reaches up to `ans+B`. If `ans+B ≥ L`, we can jump over. If not, we hop again: new rightmost = `ans+B`, from there next hop reaches up to `ans+2B`, but we must ensure each step ≥ A. As long as `ans + B ≥ L` is achievable by repeated hops of size in [A,B] over safe ground, we can do it. Because safe gaps are contiguous, we can just bump `ans` to `min(ans + B, L-1)` and check if we can now cross.
  - If `ans + B < L`: stuck → No.
  - Else (`ans + B ≥ L`): we can jump over the bad interval. After crossing, the farthest we can be is `ans + B`, but we cannot land on [L, R]. So we land at some point in [max(L, ans + A), R+1 ... actually min(ans+B, ...)]. The new `ans` becomes the max reachable safe index after the bad block. Since from any position ≤ ans we can reach, after crossing we can be at most `ans + B` (if safe). But we might be able to reach further with a subsequent hop. However, the key is: after crossing, the new reachable rightmost is `min(ans + B, next_safe_region_end)` but we can always later extend with more hops. Actually we set `ans = min(ans + B, N)` and then ensure `ans` is not inside a bad zone by jumping it to `max(ans, R)` (i.e., to just past the bad block). Because if `ans + B` lands inside [L,R], we can't be there; we must land at some safe square ≤ ans+B but ≥ max(ans+A, R+1)... Hmm, careful.

Better formulation (well-known):
- `ans` = rightmost reachable safe square so far.
- For each bad interval [L, R]:
  - If `ans < L - 1`: unreachable → No.
  - If `ans + B < L`: not enough range to cross → No.
  - Otherwise we can cross. Update `ans = max(ans, R)` (meaning we are now at least past R, because we jumped over). Then set `ans = min(ans + B, N)` to account for the next hop's reach from the new position. But actually after crossing, the farthest we can be on the next step is `R + B` (if we land just after R) or more generally from any position in the crossed zone. Since we can choose the landing point optimally, the new `ans` should be `min(R + B, N)`. Wait—but we jumped from somewhere ≤ ans (which is ≥ L-1? No, ans < L). Actually ans is in [L-1]? Let me redo.

Clean approach (standard greedy for frog with bad zones):
```
ans = 1
for each [L, R]:
    if ans < L - 1: return No
    # we can potentially land anywhere in [ans+A, ans+B], all must be safe or beyond R
    # max landing from current ans is ans+B
    if ans + B < L: return No
    # we can jump over. The best we can do: land at min(ans+B, ?) but skipping bad zone.
    # After jump, our new rightmost reachable becomes max(ans, R) + B? No.
```

Let me reconsider with the wave idea. The reachable set is always a contiguous interval [1, ans] of safe squares (where ans is the rightmost reachable safe square). Initially ans = 1. From ans, one hop extends the reachable safe interval to [1, ans+B] minus any bad squares inside. But if there are no bad squares between current ans+1 and ans+B, then ans becomes ans+B. If there is a bad interval [L,R] with L ≤ ans+B, then we can only reach safe squares up to L-1 via direct hop, but we might need multiple hops to get past.

Because the bad intervals are disjoint and sorted, the standard O(M) greedy works:
```
right = 1  # rightmost reachable safe index
for each [L, R]:
    if right < L - 1:
        # cannot even reach the square just before the bad interval
        # but maybe we can still jump over from earlier? No, we already extended as far as possible.
        print("No"); return
    # From 'right', the farthest we can reach in one hop is right + B.
    # If right + B < L, we cannot cross the bad interval at all.
    if right + B < L:
        print("No"); return
    # We can cross. Now the new rightmost reachable safe index is:
    # We can land anywhere in [max(right+A, L), right+B] that is safe.
    # The bad interval is [L,R], so safe landing zone is [max(right+A, R+1), right+B].
    # The new right becomes right+B (the farthest), but we must ensure it's safe (i.e., > R).
    # So new_right = max(right, R)  ... no.
    # Actually after the jump, we're at some safe square y in [R+1, right+B] (if right+B > R).
    # But we could also still be at positions up to right (we didn't move). The reachable safe set becomes [1, right] union [R+1, right+B].
    # Since we want the rightmost reachable, new_right = max(right, right+B) but right+B might be in bad zone, so we cap at min(right+B, N) and ensure > R.
    # If right+B > R, new_right = right+B.
    # If right+B <= R, we jumped but landed inside bad zone? Impossible because we required right+B >= L and we jump to safe square, so we must land at >= R+1 if right+B > R, or exactly at some safe spot. Actually if right+B is within [L,R], we can't land there. So the farthest safe landing is min(right+B, next_safe - 1)... 
```

Hmm, the cleanest way: the new reachable rightmost is `right + B` as long as `right + B > R` (i.e., we can land past the bad zone). If `right + B ≤ R`, that means our jump range doesn't even reach the end of the bad zone, so we can't cross → No. But wait, we might not jump from `right`; we might have an intermediate position. However, since the reachable set is contiguous [1, right], from any point in it we can hop. The farthest any hop can reach is `right + B` (from position `right`). So if `right + B < R+1`, i.e., `right + B ≤ R`, we can't get past the bad zone in one hop. Can multiple hops help? No, because we can't land inside [L,R], and we start at ≤ right < L. One hop from anywhere ≤ right lands in [x+A, x+B] ⊆ [A, right+B]. If right+B < R, then every possible landing is < R, but the bad zone extends to R. We can't land between L and R. So the only safe landing is in [A, L-1] ∪ [R+1, right+B]. If right+B ≤ R, [R+1, right+B] is empty. So we can only land in [A, L-1], which is ≤ right (since right ≥ L-1? Actually right could be < L-1). This means we can't make progress past the bad zone. So condition is `right + B ≥ R + 1`, i.e., we can land past R.

Wait, but the earlier check was `right + B < L` → can't reach bad zone. What about `L ≤ right + B ≤ R`? Then we can land in the bad zone (not allowed) or before L. The safe landings from `right` are [right+A, L-1] (if right+A ≤ L-1) and [R+1, right+B] (if R+1 ≤ right+B). If right+A > L-1, the first part is empty. So we need either to land before L (extending right to L-1) or jump over to R+1..right+B. But landing before L doesn't help cross. So we need R+1 ≤ right+B, i.e., right+B ≥ R+1. If that holds, new_right = right+B (farthest safe landing). Otherwise, we might try landing at L-1 (if reachable) and then from there... but L-1 < L, and from L-1, max reach is (L-1)+B. If (L-1)+B < R+1, still stuck. So we need to check iteratively? No, because if right+B < R+1, we can try to extend right first.

So the algorithm:
```
right = 1
for [L, R] in bad_intervals:
    if right + B < L:
        # can't reach the bad zone at all, but we might still need to? No, we just keep going.
        # Actually we just continue? No, we need to check if we can get past it eventually.
        # If right + B < L, we can hop and reach min(right+B, L-1) safely.
        # So update right = min(right + B, L - 1) and continue? But the loop processes bad zones in order.
        pass
```

I think the correct greedy is:
- `right` = rightmost reachable safe square.
- For each bad zone [L, R]:
  - If `right < L - 1`: we need to extend right. We can hop: new_right = min(right + B, L - 1). But we must ensure we can step by at least A. From `right`, one hop reaches up to `right+B`. If `right+B < L`, we can do multiple hops: each hop extends by up to B (from new right). Actually from `right`, the max reachable in k hops is `right + k*B` (landing at safe spots). As long as `right + B >= L - 1`? No, we need to check if we can reach L-1. The condition to reach L-1 is that there's a sequence of hops of size in [A,B] landing on safe squares (between current right and L-1). Since the gap is all safe, we can greedily hop: from right, go to right+B (safe, since < L). Then from there, go to (right+B)+B, etc. We can reach any point in [right + A, right + B] in one hop, [right + 2A, right + 2B] in two hops, etc. So we can reach L-1 iff there exists k such that right + k*A ≤ L-1 ≤ right + k*B. The max reachable is unbounded (with hops), so as long as L-1 ≥ right + A (i.e., we can make at least one hop forward), we can eventually reach L-1 by hopping in steps of B. Actually if A ≤ B, from right we can go to right+A..right+B. If L-1 is beyond right+B, we go to right+B, then to right+2B, etc. So we can reach L-1 iff L-1 ≥ right + A? No, we need to be able to step. From right, we must land at ≥ right+A. So if L-1 < right+A, we can't even move forward? But right < L-1, so L-1 ≥ right+1. And A ≥ 1, so L-1 could be < right+A. Then we can't reach L-1 directly. But we could overshoot? No, overshooting lands > L-1, which is in [L, R] (bad) or beyond. If beyond R, that's fine, but we want to cross. Actually if L-1 < right+A, that means L is very close to right. Specifically, right+A > L-1, so right ≥ L-A. Since right < L (because right < L-1 means right ≤ L-2... wait, right < L-1 means right ≤ L-2). So right ≤ L-2 < L-A+1, so A could be > 2. Anyway.

This is getting complicated. Let me look up the standard solution for this type of problem (AtCoder ABC 146 F? or similar). Actually this looks like AtCoder ABC 176 D? No.

Wait, the problem: squares 1..N, bad intervals, jump A..B. This is exactly AtCoder ABC 146 F? Let me think. Actually it's "Frog Jump" or similar. The constraints N up to 10^12, M up to 2e4, A,B ≤ 20. This is from AtCoder ABC 146 F? No, ABC 146 F is different. Maybe ABC 176? Let me recall: There's a problem "Frog Jump" with A,B ranges and bad squares, N up to 10^9, M up to 2e5. The solution is O(M) greedy.

The algorithm:
- Let `ans` = 1 (current rightmost reachable).
- For each bad interval [L, R]:
  - If `ans < L - 1`: We cannot reach the square just before L. But we might be able to jump over from before? No, if ans < L-1, the gap between ans and L-1 is safe. We need to check if we can reach L-1. Since we can hop in [A,B], and the gap is safe, we can extend ans to min(ans + B, L-1) in one hop if ans + B ≥ L-1? Actually we can do multiple hops. The farthest we can reach from ans with unlimited hops over safe ground is infinity (by hopping B each time). So we can always reach L-1 as long as L-1 ≥ ans + A? No, we can chain hops. From ans, we go to ans + d1 where A ≤ d1 ≤ B. Then to ans + d1 + d2, etc. We can reach any integer ≥ ans + A (by taking d1=A, then d2=B, d3=B...). So we can reach L-1 iff L-1 ≥ ans + A. If L-1 < ans + A, we can't step forward to L-1 because even the smallest hop is too big? Wait, if L-1 < ans + A, then ans + A > L-1, so even the smallest hop overshoots L-1. The only valid landing is ≥ ans + A. If L-1 < ans + A, then we cannot land on L-1. The next safe landing would be in [ans+A, ans+B] (all safe since < L). So we land at some y ≥ ans+A, and y could be ≥ L? If y ≥ L, we land in bad zone (if y ≤ R) or beyond. If we land beyond R, great. So we might not need to land on L-1.

So the condition to be stuck before a bad zone is: ans + B < L. Because if ans + B < L, then every possible landing from any position ≤ ans is < L (since max is ans+B < L). So the reachable set is bounded by ans+B < L, and we can't ever reach L or beyond. But wait, ans could be extended by hopping? From ans, we can hop to ans+B (if safe). But ans+B < L, so the new position is still < L. Then from there, max reach is ans+2B, etc. But we can never reach L if ans + k*B < L for all k. Since B > 0, ans + k*B → ∞, so eventually ans + k*B ≥ L. So we can reach L or beyond. But when we reach L, we land on a bad square. So we need to land past R. So the condition is that we can land at some y ≥ R+1, and y ≤ ans + k*B for some k, and each step is in [A,B]. The first landing at ≥ R+1 must be reachable. The max reachable after k hops is ans + k*B. The min reachable after k hops is ans + k*A. So we can land at y ≥ R+1 in k hops if ans + k*A ≤ y ≤ ans + k*B. So we need to find k such that ans + k*B ≥ R+1 and ans + (k-1)*B < L (to ensure we didn't overshoot into bad zone earlier)? Actually the path must avoid [L,R]. So we can have hops that land in safe zones, and the hop that crosses the bad zone must land at ≥ R+1. The simplest: take one big hop from some position x ≤ ans. x must be ≤ L-1 (safe before). The hop goes to y = x + d, A ≤ d ≤ B, y ≥ R+1. Also x ≥ ans_prev... this is the same as: exists x ∈ [1, ans] ∩ safe, and d ∈ [A,B] such that x + d ≥ R+1 and x + d ∉ [L,R]. Since x ≤ L-1 (safe before bad zone), x+d ≥ R+1 means d ≥ R+1 - x. We need A ≤ d ≤ B and d such that x+d ∉ [L,R]. Since x ≤ L-1 and x+d ≥ R+1 > R, x+d is automatically > R, so safe. So condition: exists x ≤ min(ans, L-1) such that R+1 - x ≤ B, i.e., x ≥ R+1 - B. Also we need A ≤ d, but d = x+d - x, and we just need some d ∈ [A,B] with d ≥ R+1-x. This is possible iff R+1 - x ≤ B and also R+1 - x ≥ A (so that d can be chosen in [A,B]... wait, d = (x+d) - x. We can choose the landing y = x+d as any value in [x+A, x+B]. We need y ≥ R+1. So we need x+B ≥ R+1 and also the interval [x+A, x+B] contains some y ≥ R+1. That means x+A could be > R+1, but then we overshoot, which is fine as long as y ≤ N. But we also need to not land in [L,R]. If x+A > R, then y > R, safe. If x+A ≤ R, we need y ≥ R+1, so we need x+B ≥ R+1. So condition: exists x ≤ min(ans, L-1) with x ≤ L-1, and [x+A, x+B] intersects [R+1, ∞). That is, x+B ≥ R+1 and (x+A > R or x+B ≥ R+1). Actually simpler: x+B ≥ R+1. And we can always pick y = max(x+A, R+1) if that ≤ x+B, i.e., max(x+A, R+1) ≤ x+B. Since x ≤ L-1 ≤ R, we have x+A ≤ L-1+A. This could be > R+1. If x+A > R+1, then y = x+A works. If x+A ≤ R+1, then we need x+B ≥ R+1. So condition is just x+B ≥ R+1 (since if x+A ≤ R+1 ≤ x+B, we can land at R+1; if x+A > R+1, we land at x+A > R+1). Wait, if x+A > R+1, that's fine (we land past R). So the only condition is x+B ≥ R+1. And we need x to be reachable (x ≤ ans) and x safe (x ≤ L-1, which is implied if x ≤ ans and ans < L? Not necessarily, but if ans ≥ L, we've already crossed. So when processing [L,R], we have ans < R+1 typically). Actually ans could be > R if we already passed, but then we're done with this interval.

So when processing [L,R], the condition to cross is: ans ≥ L-1? No, we need some x ≤ min(ans, L-1) with x+B ≥ R+1. The best x is the largest possible, i.e., min(ans, L-1). So we need min(ans, L-1) + B ≥ R+1.
- If ans ≥ L-1, then min is L-1, need L-1+B ≥ R+1, i.e., B ≥ R-L+2.
- If ans < L-1, then min is ans, need ans+B ≥ R+1.

But wait, we can also increase ans before crossing by hopping in the safe zone before L. If ans < L-1, we can hop to increase ans. As discussed, we can reach any position in the safe zone [ans+1, L-1] (if it's large enough). Specifically, we can reach L-1 iff L-1 ≥ ans+A (by hopping A then B's, or directly if in range). But we can also overshoot L-1. The max reachable from ans with multiple hops is unbounded (ans + k*B). So we can reach any y ≥ ans + A. So if ans + A ≤ L-1, we can reach L-1. If ans + A > L-1, we can't land on L-1, but we can land on some y ≥ ans+A. If ans+A > L-1, then y ≥ ans+A > L-1, so y ≥ L. If y > R, we cross. If y ∈ [L,R], we land in bad zone, invalid. So we need to land at y ≥ R+1. This requires ans + B ≥ R+1 (one hop from ans) or multiple hops. With multiple hops, we can reach any y ≥ ans + A. So we need some y ∈ [ans+A, ∞) that is safe and we can land there. The safe spots are [1, L-1] ∪ [R+1, N]. So we need [ans+A, ∞) to intersect [R+1, N]. That is, ans + A ≤ N (always true if ans < N) and ans + A ≤ some safe spot ≥ R+1. The first safe spot ≥ ans+A is max(ans+A, R+1) if ans+A > L-1, or ans+A if ans+A ≤ L-1. Actually if ans+A ≤ L-1, we land in safe zone before L, and then we can continue. So the crossing is possible iff we can eventually land at ≥ R+1. The condition for that is that the reachable set (which grows by B each hop, starting from ans) can reach R+1 without landing in [L,R]. Since the only bad zone is [L,R], and we start at ans < L (assuming we haven't crossed), the path must jump from some x ≤ L-1 to y ≥ R+1 in one step of size in [A,B]. The best x is the largest reachable x ≤ L-1. The reachable x grows. The set of reachable safe positions is all integers ≥ ans+1 that can be formed by sums of A..B. This is all integers ≥ ans + A (since B ≥ A, and we can add A then B's... actually with A..B, the reachable set from ans is all integers ≥ ans + A that satisfy some modulo condition? No, because we can choose any d ∈ [A,B] each step. The set of reachable positions is all integers ≥ ans + A? Let's check: can we reach ans + A + 1? From ans, hop A to ans+A. From ans+A, hop A to ans+2A, or B to ans+A+B. We can get ans+2A, ans+A+B, ans+2B, etc. With A ≤ B, the set of reachable positions from ans is all integers ≥ ans + A except possibly some small gaps? Actually with steps in [A,B], the reachable set is all integers ≥ ans + A. Proof: by induction, base: ans+A reachable. Suppose we can reach all integers in [ans+A, ans+k]. To reach ans+k+1, if k+1 - (k-1) = 2, but we need a step from some x. From ans+k, we can go to ans+k+A..ans+k+B. If ans+k+1 ≤ ans+k+B (i.e., 1 ≤ B, true), we can reach it. But we need ans+k+1 to be reachable from some already reachable x. If we have reached ans+m for all m ∈ [ans+A, ans+k], then from ans+k, we reach up to ans+k+B ≥ ans+k+A ≥ ans+A+A = ans+2A. This covers all. Actually the reachable set is exactly all integers ≥ ans + A. Wait, is ans + A + 1 reachable? From ans, we go to ans + d1, A≤d1≤B. From ans+d1, we go to ans+d1+d2, etc. The minimum after 2 hops is ans+2A. The set of reachable positions after 2 hops is [ans+2A, ans+2B] ∪ [ans+A+B, ans+B+A] (same). So it's all integers in [ans+2A, ans+2B] that are ≥ ans+A+B? No, [ans+2A, ans+2B] is a range of length B-A. Not all integers ≥ ans+2A are reachable in 2 hops; only those in [ans+2A, ans+2B]. But in 3 hops, we can fill gaps. In fact, with enough hops, the reachable set is all integers ≥ ans + A. Is that true? Let's test A=2, B=3. From ans=0: hop 2 or 3. After 1 hop: 2,3. After 2 hops: from 2: 4,5; from 3: 5,6. So {4,5,6}. After 3 hops: from 4:6,7; from 5:7,8; from 6:8,9. So {6,7,8,9}. The union is all integers ≥ 2. Yes! So indeed, with A ≤ B, the reachable set from ans is all integers ≥ ans + A. (This is because the gcd of A..B is 1? Actually even if gcd > 1, the reachable set modulo gcd is fixed, but since A..B are consecutive integers? No, A and B are arbitrary. But the problem doesn't require gcd=1. However, with steps in [A,B], we can reach all sufficiently large integers? Not all, only those congruent to ans + k*A mod (B-A)? Wait, no. The set of sums of k numbers from [A,B] is an interval [kA, kB] (since the set of sums of intervals is an interval). So after k hops, reachable positions are [ans + kA, ans + kB] (intersected with safe zones). As k increases, these intervals overlap and cover all integers ≥ ans + A. Specifically, for any y ≥ ans + A, choose k such that kA ≤ y - ans ≤ kB. This is possible because the intervals [kA, kB] for k=1,2,... cover all integers ≥ A. Proof: [A,B] covers [A,B]. [2A,2B] overlaps with [A,B] if 2A ≤ B+1, i.e., A ≤ B, which is true. So by induction, the union is [A, ∞). So yes, reachable set is all integers ≥ ans + A.

Therefore, if ans + A ≤ L-1, we can reach L-1. If ans + A > L-1, we can reach any y ≥ ans + A. To cross [L,R], we need to reach some y ≥ R+1. Since we can reach any y ≥ ans + A, the condition to cross is that there exists y ≥ max(ans+A, R+1) that is reachable and safe, and the path to y doesn't require landing in [L,R]. But we can jump directly to y from some x ≤ L-1. As long as x+B ≥ y, we can jump. The best x is the largest reachable x ≤ L-1. Since we can reach any x in [max(ans+1, A), L-1] (if L-1 ≥ ans+A), we can pick x = min(ans + something, L-1). Actually we can reach any x in [ans+A, L-1] (if this interval is non-empty). From such x, we can jump to y ∈ [x+A, x+B]. We need y ≥ R+1. So we need x+B ≥ R+1. The maximum x is L-1. So condition is (L-1) + B ≥ R+1, i.e., B ≥ R - L + 2. But wait, we might not have reached L-1 yet. We can reach any x in [ans+A, L-1]. The largest such x is L-1. So we can choose x = L-1 (if L-1 ≥ ans+A). If L-1 < ans+A, we cannot reach L-1, but we can reach any y ≥ ans+A. In that case, we need ans+A > L-1. Then we are jumping from some x < L-1? Actually if ans+A > L-1, then even the smallest hop from ans goes to ≥ L. We cannot land in [L,R] (unless we land exactly at R+1 or beyond). We can land at y ∈ [ans+A, ans+B]. We need some y ≥ R+1. So condition is ans+B ≥ R+1 and the interval [ans+A, ans+B] contains some point ≥ R+1. This is true iff ans+B ≥ R+1 (since ans+A ≤ ans+B). And we need that point to be safe, i.e., not in [L,R]. Since ans+A > L-1 (by assumption), ans+A ≥ L. So y ≥ L. We need y > R. So we need ans+B ≥ R+1. Also we need that there is a valid y in [ans+A, ans+B] that is ≥ R+1. The valid y are those ≥ R+1. So we need [ans+A, ans+B] ∩ [R+1, ∞) ≠ ∅, i.e., ans+B ≥ R+1. And we also need that we can actually make the hop from ans to y with y ∈ [ans+A, ans+B] and y ≥ R+1. This requires y ≥ ans+A (always) and y ≤ ans+B. So we need some y with max(ans+A, R+1) ≤ y ≤ ans+B. This is possible iff max(ans+A, R+1) ≤ ans+B. If ans+A ≥ R+1, then ans+A ≤ ans+B is true, so we can pick y=ans+A. If ans+A < R+1, we need R+1 ≤ ans+B, i.e., ans+B ≥ R+1. So in both cases, condition is ans+B ≥ R+1. But wait, if ans+A < R+1 and ans+B ≥ R+1, we pick y = R+1 (which is in [ans+A, ans+B] if ans+A ≤ R+1 ≤ ans+B). Yes. So condition is simply ans+B ≥ R+1.

But is that sufficient? We also need to ensure that from the new position y (or later positions), we can continue. But the greedy just updates the rightmost reachable. After crossing, the new rightmost reachable is y (or later). Since we can reach any y ≥ ans+A, and we can reach y ≥ R+1, the new rightmost reachable after this hop is some y ∈ [max(ans+A, R+1), min(ans+B, N)]. The farthest we can be is min(ans+B, N). But we also have the constraint that we might need to cross more bad zones. However, if we just update right = min(ans+B, N) and then for the next bad zone, we check if we can cross, is that correct?

Wait, the above analysis assumed we are at ans and we take one hop. But ans is the rightmost reachable. After taking a hop, the new rightmost is at most ans+B. However, we might have multiple hops before the next bad zone. The key is: the reachable set is always a contiguous interval [1, right] of safe squares, where right is the maximum reachable safe square. Initially right=1. When we encounter a bad zone [L,R]:
- If right < L: the safe zone before L extends to L-1. We can extend right by hopping. Since we can reach any safe square ≥ right+A (as argued, the reachable set is all safe squares ≥ right+A up to some limit? No, the reachable set is all safe squares that can be reached. But with no bad squares in between, the reachable set is all integers ≥ right+1 that are ≥ right+A. So we can reach any integer ≥ right+A. So we can extend right to min(right+B, L-1)? No, we can extend right to L-1 if L-1 ≥ right+A, or we can jump over to ≥ R+1. But to maximize right, we should consider what happens after the bad zone. Actually, after the bad zone, the new right becomes max(right, something). The standard algorithm is:
  - If right + B < L: cannot reach the bad zone. We can extend right to right + B (since all squares in [right+1, right+B] are safe and reachable). But wait, we can also do multiple hops and reach further. The set of reachable safe squares before L is all integers in [right+A, L-1] (since beyond L is bad). So we can extend right to L-1 if L-1 ≥ right+A. If L-1 < right+A, we cannot reach L-1; the next reachable safe square is ≥ right+A, which is ≥ L (since L-1 < right+A implies right+A ≥ L). So we are already at or past L. But L is bad. So we need to jump to ≥ R+1. This is possible if right+B ≥ R+1. If so, we land at some y ≥ R+1, and right becomes y (or later). The maximum possible right after crossing is right+B.
  - So the condition to cross is: right + B ≥ R + 1. (Since we can always take one hop from the rightmost position right, as long as right < L or right ≥ L? If right ≥ L, we are already in or past the bad zone. If right ∈ [L,R], impossible. If right > R, we've already crossed, so this bad zone is behind us. So when processing, we can assume right < R+1, i.e., right ≤ R.)
  - Actually, if right ≥ L, we are in trouble (in bad zone) unless right > R. So we should process bad zones in order and ensure we never land in them.

The standard solution is O(M) with this logic:
```
right = 1
for L, R in bad:
    if right < L - 1:
        # we are before the bad zone. Can we reach L-1?
        # We can reach any position in [right+A, L-1] (if non-empty).
        # So we update right = L-1.
        # But is that always reachable? Only if right+A ≤ L-1.
        # If right+A > L-1, we cannot reach L-1.
        if right + A > L - 1:
            # we cannot step to L-1. We must overshoot.
            # Then we need to jump directly to ≥ R+1 from some x ≤ right.
            # The best x is right. So we need right+B ≥ R+1.
            if right + B < R + 1:
                return No
            # we can jump. New right is right+B (but we might not land there if it's > N or in next bad zone, but for now update)
            right = min(right + B, N)
            # But wait, we might land in [L,R] if right+B ∈ [L,R]? No, right+B ≥ R+1 by condition, so safe.
        else:
            # we can reach L-1. Update right to L-1.
            right = L - 1
    else:
        # right ≥ L-1, so we are at or past the safe zone before bad.
        # We are at right ≤ R (since if right > R, we'd have passed).
        # Actually if right > R, this bad zone is already passed? But the loop goes in order, so right should be ≤ R.
        # We need to jump over the bad zone.
        # From right, we can jump to [right+A, right+B]. We need to land at ≥ R+1.
        if right + B < R + 1:
            return No
        right = min(right + B, N)
```

But this is not quite right because after updating right = L-1, we might not be able to cross in the next step if right+B < R+1. We need to check crossing from L-1. So the condition to cross from the new right (which is at most L-1) is that (new_right) + B ≥ R+1. If new_right = L-1, we need L-1+B ≥ R+1. If that's false, we are stuck. But wait, we could have not gone all the way to L-1; we could stop earlier to get a better launch? No, farther right is better for crossing because B is fixed. So maximizing right is best. So if L-1+B < R+1, we cannot cross from L-1. Could we cross from an earlier position? No, because earlier + B < L-1 + B < R+1. So impossible. So the condition L-1+B ≥ R+1 is necessary and sufficient (assuming we can reach L-1).

But what if we cannot reach L-1? Then we must overshoot from current right. The condition is right+B ≥ R+1. And we can overshoot to right+B. But right+B might be > R+1, which is fine. So the unified condition is: we can cross the bad zone [L,R] iff the maximum reachable right before crossing (call it pre_right) satisfies pre_right + B ≥ R+1, where pre_right is the rightmost safe square we can reach before the bad zone. The pre_right is the maximum of right and L-1 (whichever is smaller and reachable). Actually, if right < L, we can extend right to at most L-1 (if reachable) or we are stuck. If right + A > L-1, we cannot reach L-1, so pre_right = right (the current right, which is < L). Then condition is right + B ≥ R+1. If right + A ≤ L-1, we can reach L-1, so pre_right = L-1. Condition is L-1 + B ≥ R+1. After crossing, the new right is min(pre_right + B, N) but we must also ensure we don't land in the next bad zone? No, we just set right = min(pre_right + B, N) and then the next iteration will handle the next bad zone.

Wait, is it always optimal to go to L-1 if we can? Yes, because farther right gives more reach. So the algorithm is:
```
right = 1
for [L, R] in bad:
    if right < L:
        # we are before the bad zone
        # try to extend right to L-1
        if right + A <= L - 1:
            right = L - 1
        # else: we cannot reach L-1; right remains as is
    # now check if we can cross
    if right + B < R + 1:
        return No
    # we can cross. new right is right + B
    right = min(right + B, N)
```
But is this correct? Let's test with sample 1:
N=24, M=2, A=3, B=5. Bad: [7,8], [17,20].
right=1.
[7,8]: right=1 < 7. right+A=4 ≤ 6, so right=6. Now right=6. Check cross: 6+5=11 ≥ 9? R+1=9. 11≥9, ok. right = min(11, 24) = 11.
[17,20]: right=11 < 17. right+A=14 ≤ 16, so right=16. Check: 16+5=21 ≥ 21 (R+1=21). ok. right = min(21,24)=21.
After loop, right=21. We need to reach N=24. Now we are at right=21. There are no more bad zones. We need to check if we can reach 24. Since no more bad zones, we can extend right by hopping. We can reach any position ≥ 21+3=24. So yes. But the loop only updates right when crossing bad zones. After the last bad zone, we have right=21, but we need to reach 24. We must continue hopping. The final check: can we reach N? We need to simulate hopping after the last bad zone. Since there are no more bad squares, we can just check if right + A ≤ N (or right < N and we can reach N). Actually after the last bad zone, the remaining squares are all safe. So we can reach N iff right < N and we can step to N. Since we can chain hops, we can reach N iff N ≥ right + A (i.e., we can make at least one hop forward) and then we can reach N by hopping B repeatedly. More precisely, we can reach N iff there exists k such that right + k*A ≤ N ≤ right + k*B. Since A ≤ B and we can adjust, this is equivalent to N ≥ right + A and the distance N - right is reachable. But with no bad squares, we can always reach any target ≥ right + A by hopping A then B's. So condition is simply N ≥ right + A. But wait, what if N is between right+A and right+B? We can reach it in one hop. If N > right+B, we hop to right+B, then right+2B, etc. Since right+B - right = B ≥ A, we can always step by at least A. So yes, we can reach N iff N ≥ right + A. But we also need to not overshoot? No, we stop at N exactly. Since we can choose step size, we can land exactly on N as long as N - current ≥ A and N - current ≤ (some number of hops)*B. Actually we need to be able to hit N exactly. With steps in [A,B], we can reach any integer ≥ right + A that is congruent to right + something modulo gcd(A,B)? No, we can choose step sizes freely, not fixed. We can choose any integer d ∈ [A,B] each step. So the set of reachable positions from right (with no bad squares) is all integers ≥ right + A. Because we can go right+A, right+A+B, right+A+2B, etc., and also right+2A, etc. The union of [kA, kB] for k≥1 is [A, ∞). So yes, all integers ≥ right+A are reachable. So final check: if right + A ≤ N, return Yes, else No.

But wait, what if right is already N? Then Yes.

Let's test sample 2:
N=30, M=1, A=5, B=8. Bad: [4,24].
right=1.
[4,24]: right=1 < 4. right+A=6 > 3 (L-1=3). So we cannot reach L-1. right remains 1. Check cross: 1+8=9 < 25 (R+1=25). So No. Correct.

Sample 3:
N=100, M=4, A=10, B=11. Bad: [16,18], [39,42], [50,55], [93,99].
right=1.
[16,18]: right=1 < 16. right+A=11 ≤ 15. So right=15. Check: 15+11=26 ≥ 19. ok. right=min(26,100)=26.
[39,42]: right=26 < 39. right+A=36 ≤ 38. So right=38. Check: 38+11=49 ≥ 43. ok. right=49.
[50,55]: right=49 < 50. right+A=59 > 49. So cannot reach L-1=49? Wait, L-1=49. right=49. So right is already 49! right < L is false (49 < 50 true). So we are at right=49, which is L-1. So we don't need to extend. Then check cross: right+B = 49+11=60 ≥ 56 (R+1=56). ok. right=60.
[93,99]: right=60 < 93. right+A=70 ≤ 92. So right=92. Check: 92+11=103 ≥ 100 (R+1=100). ok. right=min(103,100)=100.
After loop, right=100 = N. Return Yes. Correct.

But wait, in the first step of sample 3, right=26 after first bad zone. Then second bad zone [39,42]: right=26 < 39. right+A=36 ≤ 38 (L-1=38). So right=38. Good.

Edge case: what if right + A > L - 1 but right + B ≥ R+1? We handled that (right remains, cross directly).
What if right ≥ L? Then we are at or past L. If right > R, we are already past; but the loop processes in order, so right should be ≤ R. If right ∈ [L,R], impossible (we landed in bad zone). So we must ensure that after crossing, right is not in [L,R]. Our update right = min(pre_right + B, N). If pre_right + B > R, we land past R. If pre_right + B ≤ R, we land inside bad zone, which is invalid. But our condition right + B < R+1 ensures pre_right + B ≥ R+1. If pre_right + B = R+1, we land exactly at R+1, safe. If > R+1, safe. So new right is safe.

One more check: after updating right = pre_right + B, this new right might be in the next bad zone. That's fine; the next iteration will handle it (it will try to cross from there, but if right ∈ [L_next, R_next], we are stuck? Actually if right is in the next bad zone, that means we landed in it, which is invalid. So we need to ensure that when we cross one bad zone, we don't land in the next one. The update right = pre_right + B could land in the next bad zone if the bad zones are close. But wait, we are processing bad zones in order. After crossing [L,R], the next bad zone is [L',R'] with L' > R. Our new right is pre_right + B. If this is ≥ L' and ≤ R', we are in the next bad zone. But the next iteration will see right ∈ [L', R'] and right < L' is false, and right + B < R'+1 might be true or false. However, we are already in a bad zone! That's invalid. So we must ensure that after crossing, we land at a safe square. That means pre_right + B must not be in any bad zone. Since the next bad zone starts at L', we need pre_right + B < L' or pre_right + B > R'. But pre_right ≤ R < L'. So pre_right + B could be ≥ L'. If it's in [L', R'], we land in bad zone. But the problem says we choose the move; we can choose a smaller i to land before L'. So we are not forced to land at pre_right + B; we can land anywhere in [pre_right + A, pre_right + B] that is safe. So when updating right, we should set it to the maximum safe landing, i.e., the maximum y ∈ [pre_right + A, pre_right + B] that is not in any bad zone. Since we are crossing the current bad zone, y must be ≥ R+1. But y could be in the next bad zone. So we should set right = max safe y. However, the next iteration will handle the next bad zone. If we set right to pre_right + B, and it falls in the next bad zone, that's a problem. But we can choose y < pre_right + B to avoid the next bad zone. The algorithm should be: after crossing, right = min(pre_right + B, L_next - 1) or something? Actually, we want the rightmost reachable safe square after the hop. We can hop to any y ∈ [pre_right + A, pre_right + B] that is safe. The rightmost safe y is the largest integer ≤ pre_right + B that is not in any bad zone. Since bad zones are disjoint, this is either pre_right + B (if safe) or the end of the current bad zone R (but we can't land there) or the start of the next bad zone minus 1. So right = min(pre_right + B, L_next - 1) where L_next is the start of the next bad zone, or N if no next.

But wait, the next iteration will process the next bad zone. If we set right = L_next - 1, then the next iteration sees right < L' and extends/crosses. If we set right = pre_right + B and it happens to be ≥ L', we are in trouble. So we should clamp right to the safe region.

However, the standard approach is to process bad zones one by one and after crossing, the new right is the maximum index we can reach that is not in the current bad zone and not beyond the next bad zone? Actually, we can just update right = min(pre_right + B, L_next - 1) if there is a next bad zone, else N. But the loop already handles the next bad zone. If we set right = pre_right + B and it's in the next bad zone, the next iteration's check `if right < L` will be false, and it will try to cross from inside the bad zone, which is invalid. So we need to ensure that after crossing, right is safe.

Let's refine: When we cross [L,R], we choose a landing y ∈ [pre_right + A, pre_right + B] such that y is safe (not in [L,R] and not in any future bad zone? Actually future bad zones are handled later, but we must not land in them now). The set of safe squares is [1, L-1] ∪ [R+1, N] minus the future bad zones. The farthest safe landing ≤ pre_right + B is the min of pre_right + B and (L_next - 1) if L_next exists and L_next ≤ pre_right + B. If pre_right + B < L_next, then pre_right + B is safe (assuming it's not in [L,R], which is true by crossing condition). So we can set right = min(pre_right + B, L_next - 1). Then the next iteration starts with this right.

But does this affect the ability to cross future bad zones? If we clamp to L_next - 1, we might be closer than necessary. But we could have landed at a larger safe square by choosing a different y? No, because L_next - 1 is the largest safe square before the next bad zone. If pre_right + B > L_next - 1, we cannot land at any square ≥ L_next because they are bad (until R_next). So the maximum safe landing is indeed L_next - 1. So we must set right = min(pre_right + B, L_next - 1). This is crucial.

Let's test with an example: A=2, B=3. Bad: [5,5], [8,8]. Start right=1.
[5,5]: pre_right: right=1 < 5. right+A=3 ≤ 4, so right=4. pre_right=4. Cross: 4+3=7 ≥ 6. L_next=8. min(7, 7)=7. So right=7.
[8,8]: right=7 < 8. right+A=9 > 7. So we cannot reach L-1=7? Wait L-1=7. right=7. So right is already 7. right < L is false. So we are at right=7. pre_right=7. Cross: 7+3=10 ≥ 9. L_next doesn't exist (or N). right = min(10, N). So we jump to 10. Works.

Another example: A=3, B=5. Bad: [10,10], [12,12]. Start right=1.
[10,10]: right=1 < 10. right+A=4 ≤ 9, so right=9. pre_right=9. Cross: 9+5=14 ≥ 11. L_next=12. min(14, 11)=11. So right=11.
[12,12]: right=11 < 12. right+A=14 > 11. So right remains 11. pre_right=11. Cross: 11+5=16 ≥ 13. L_next none. right=16. Works.

What if after crossing, we land exactly at L_next? That's bad, so we clamp to L_next - 1.

What if we cannot reach L-1 and right+B is huge, but next bad zone is soon? E.g., A=10, B=20. Bad: [5,5], [6,6]. Start right=1.
[5,5]: right=1 < 5. right+A=11 > 4, so cannot reach L-1. pre_right=1. Cross: 1+20=21 ≥ 6. L_next=6. min(21, 5)=5. So right=5.
[6,6]: right=5 < 6. right+A=15 > 5. pre_right=5. Cross: 5+20=25 ≥ 7. L_next none. right=25. Works.

What if we cannot reach L-1 and right+B is not enough to reach R+1? Then No.

So the algorithm is:
```
right = 1
bad_intervals = list of (L, R)
for i, (L, R) in enumerate(bad_intervals):
    # Extend right to L-1 if possible
    if right < L:
        if right + A <= L - 1:
            right = L - 1
        # else: right remains (cannot reach L-1)
    # Now try to cross
    # Determine the maximum safe landing after crossing
    # We need to jump to some y >= R+1, y <= right + B, and y not in any bad zone.
    # The next bad zone starts at L_next (or N+1 if none)
    if i + 1 < len(bad_intervals):
        L_next = bad_intervals[i+1][0]
    else:
        L_next = N + 1
    # Check if we can cross: need right + B >= R+1
    if right + B < R + 1:
        print("No"); return
    # The new right is the max safe y in [R+1, min(right+B, L_next-1)]
    new_right_candidate = min(right + B, L_next - 1)
    if new_right_candidate < R + 1:
        # cannot land past R without entering next bad zone? But we can also land before next bad zone? Wait, we need y >= R+1. If L_next <= R+1, that means the next bad zone starts at or before R+1. But the bad zones are disjoint and sorted, so L_next > R. If L_next = R+1, then new_right_candidate = min(right+B, R). But we need y >= R+1. So we cannot land safely? Actually if L_next = R+1, then the next bad zone is immediately after the current one. The safe region between them is empty. So we must land past R+1, i.e., in the next bad zone or beyond. We cannot land in the next bad zone. So we must land at >= R_next + 1? But we are processing the current one. The only safe landing is >= L_next? No, L_next is bad. So we must land past the next bad zone? That's impossible in one hop if right+B < L_next. But we can chain hops. This suggests we need to consider the next bad zone as well.
```

Ah! This is the key complication. The bad zones can be close together. We might not be able to land between them. We need to jump over multiple bad zones in one hop? No, we land on a safe square. If two bad zones are adjacent (R+1 = L_next), there is no safe square between them. We must jump from before the first to after the second. That requires crossing both in one trajectory. The standard approach handles this by considering that the "safe" intervals are the gaps between bad zones. The reachable set is always within the current safe gap or after crossing.

Actually, the correct way is: the reachable set is always contained in a single "safe component" of the safe squares? No, after crossing, we are in the next safe component. But we might not be able to reach the next safe component if we can't jump far enough.

I think the standard greedy is: the rightmost reachable safe square `ans` is always at the right end of the current safe interval (or the start of a bad interval? No, it's a safe square). We maintain `ans` as the rightmost reachable safe square. When we encounter a bad interval [L,R], if `ans < L`, we are in the safe interval before it. We can try to extend `ans` to `L-1` if possible. Then we need to jump over [L,R]. The farthest we can land is `ans + B`. But we might land in the next bad zone. However, we can always choose to land at `min(ans + B, next_L - 1)` if that is ≥ R+1. If not, we need to consider that we might not be able to cross this bad zone at all, or we might need to not jump to the maximum.

Wait, if `ans + B` lands in the next bad zone, we can simply choose a smaller jump to land at `L_next - 1` (if `L_next - 1 ≥ R+1`). If `L_next - 1 < R+1`, that means the safe gap between the two bad zones is empty or negative. So we must jump from before the first bad zone to after the second bad zone. That requires `ans + B ≥ R_next + 1` (or at least `> R_next`). But we are only considering the current bad zone. The next iteration will see we are still before it? Actually, if we jump over both, we land past the second bad zone. But we must ensure we don't land in any bad zone. So we need to jump from some `x ≤ ans` to `y ≥ R_next + 1` (if we want to cross both). But we might also land in the safe gap if it exists.

This suggests that we should process the bad zones in a way that considers the safe gaps. The reachable set is always a contiguous interval of safe squares. The safe squares are partitioned into maximal contiguous safe intervals: (0, L1-1), (R1+1, L2-1), ..., (RM+1, N). We start in the first safe interval. We can move right within a safe interval by hopping. When we are at the right end of a safe interval (or anywhere in it), we can jump to the next safe interval if we can clear the bad zone. The jump distance must be in [A,B]. We are at some position x in the current safe interval [s, e] (where s is the start of the safe interval, e is the end, e = L-1 for the first gap, etc.). We want to jump to some y in the next safe interval [s', e'] (s' = R+1, e' = L_next - 1). The condition is: there exists x ∈ [s, e] ∩ reachable, and d ∈ [A,B] such that x + d = y ∈ [s', e']. Since we want to maximize progress, we should take x as large as possible (rightmost reachable). The rightmost reachable in the current safe interval is min(e, right) where right is the global rightmost reachable? Actually, we can reach any position in the current safe interval that is ≥ s + A? Not exactly. The reachable set within the safe interval is all positions ≥ max(s, previous_right+1) that are reachable by hops. This is complicated.

Given the constraints (M up to 2e4), an O(M) or O(M log M) solution is needed. The known solution for this problem (AtCoder ABC 146 F? Actually it's "Frog Jump" from AtCoder ABC 211 D? No, D is tree. Maybe ABC 215 D? No. Let me search my memory. There is a problem "Frog 1" and "Frog 2" but those are DP. This is "Frog Jump" with bad squares. I recall a problem from AtCoder Beginner Contest 176? No. Actually, it's "AtCoder Grand Contest" or "Regular Contest"? The constraints N up to 1e12, M up to 2e4, A,B <= 20. This is "AtCoder Beginner Contest 146 F"? No, that's "Sugoroku". Sugoroku! ABC 146 F is "Sugoroku". The problem: There are N squares, M pairs (L_i, R_i) of bad squares. Move from 1 to N with step A..B. Yes! That's exactly it. ABC 146 F - Sugoroku.

The solution for Sugoroku: O(M) greedy with "ans" as the rightmost reachable. The algorithm is:
- ans = 1
- For i from M down to 1? Or forward?
Actually, the known solution processes from the end? No, forward.
Wait, I remember: We maintain the rightmost reachable square `ans`. For each bad interval from left to right:
- If `ans < L_i - 1`: We need to see if we can reach `L_i - 1`. The distance is `L_i - 1 - ans`. We need to check if we can cover this distance with steps in [A,B]. Since we can stop anywhere, we can reach `L_i - 1` iff `L_i - 1 - ans >= A` (because we can just step by B repeatedly after the first step? Actually, the condition to be able to reach a point y from x with steps in [A,B] is that y - x >= A and y - x is not too large? With no bad squares in between, we can reach any y >= x + A. So we can reach L-1 iff L-1 >= ans + A. But in Sugoroku, the rule is: if ans < L-1, we set ans = L-1, but we must also ensure we can actually make the moves. The solution sets ans = L-1 if ans < L-1, but then adjusts by looking back? Hmm.

Let me recall the editorial of ABC 146 F. The greedy: maintain the rightmost reachable index `ans`. For each bad interval [L, R] from left to right:
- If `ans < L`: We are before the bad interval. We can move to `min(ans + B, L-1)` in one step? No, we can only move to safe squares. Actually, the editorial says: we try to move to the rightmost possible square. So we set `ans = min(ans + B, L-1)`. But if `ans + B < L`, we are stuck? No, we can take multiple steps. The editorial handles this by noting that we can always reach `L-1` as long as `L-1 >= ans` and we can step. Actually, the editorial solution is:
```
ans = 1
for L, R in bad:
    if ans < L - 1:
        ans = L - 1
    if ans + B < L:
        # cannot even reach the bad zone? But we are already at L-1? No.
        # Actually if ans < L-1, we set ans to L-1. Then ans >= L-1.
        # So we don't have ans < L-1.
        pass
    if ans + B < R + 1:
        print("No"); return
    ans = min(ans + B, N)
```
Wait, this is exactly what I had earlier! But does it handle the clamping to next bad zone? No. In Sugoroku, the bad zones are "bad squares" and we can land on any non-bad square. The greedy `ans = min(ans + B, N)` might land in the next bad zone, but the next iteration will see `ans` is in the next bad zone and handle it. But if we land in the next bad zone, that's invalid! However, in the loop, when we process the next bad zone, we will check `if ans < L - 1` etc. If `ans` is inside the next bad zone, say `L <= ans <= R`, then `ans < L - 1` is false. Then we check `if ans + B < R + 1`. If `ans` is already inside, we might think we can cross it. But we shouldn't be there. So the condition should ensure we never land in a bad zone. The standard greedy must ensure that after the update `ans = min(ans + B, N)`, `ans` is not in any bad zone. How? By setting `ans = min(ans + B, L_next - 1)` as I thought. But I haven't seen that in the editorial.

Let me check the sample 1: N=24, A=3, B=5. Bad: [7,8], [17,20].
ans=1.
[7,8]: ans=1 < 6. ans = 6. ans+B=11 >= 9. ans = min(11,24)=11.
[17,20]: ans=11 < 16. ans = 16. ans+B=21 >= 21. ans = min(21,24)=21.
End. ans=21 < 24. But we need to reach 24. The editorial would then check if we can reach N from ans. Since no more bad zones, we need to see if we can reach 24. With ans=21, A=3, we can reach 24 (21+3=24). So Yes.
But what if we had set ans=11 after first bad zone, and the second bad zone was [12,12]? Then:
[7,8]: ans=6. ans+B=11. ans=11.
[12,12]: ans=11. ans < 11? No, L-1=11. So ans is not < L-1. Check: ans+B=16 >= 13. ans = min(16,24)=16.
This works. But what if the second bad zone was [11,11]? Then:
[7,8]: ans=6. ans+B=11 >= 9. ans=11.
[11,11]: L=11. ans=11. ans < L-1 (10) is false. Check: ans+B=16 >= 12. ans=16.
But ans=11 is in [11,11]! That's a bad square. The update ans = min(ans+B, N) = 11 is invalid. But the code would set ans=11, then see L=11, R=11, and ans < L-1 is false, so it tries to cross. But we are already in the bad zone. However, the crossing condition ans+B >= R+1 = 12 is true, so it sets ans=16. This effectively jumps from the bad square? No, the state "ans" represents a reachable safe square. If ans becomes 11, which is bad, it's an error. But in the logic, we never checked that ans is safe. We just updated ans to 11. Then the next iteration sees ans=11, L=11, so ans is exactly at the start of the bad zone. Is that considered safe? The problem says square j is bad if L_i <= j <= R_i. So 11 is bad. We cannot be at 11. So the algorithm is flawed if it allows ans to be in a bad zone.

But wait, in the step for [7,8], we had ans=6 before. We set ans = min(6+5, 24) = 11. But 11 is after the bad zone (8+? 11 is safe because next bad zone is [11,11] in my hypothetical). In my hypothetical, the next bad zone is [11,11]. So 11 is bad. But the algorithm set ans=11. This is a bug. The correct update should be ans = min(ans+B, L_next - 1) = min(11, 10) = 10. Then for [11,11], ans=10 < 10? L-1=10, so ans is not < 10. Actually ans=10 is safe. Then we try to cross: ans+B=15 >= 12, so ans=15. This works.

So the clamping is necessary. The editorial for ABC 146 F must include this. Let me recall: the editorial says we process from right to left? No, forward. The editorial solution:
```
ans = 1
for L, R in bad:
    if ans < L - 1:
        ans = L - 1
    if ans + B < R + 1:
        print("No")
        return
    ans = min(ans + B, N)
```
But this doesn't clamp to next L. However, note that `ans` is updated to `ans + B`, and then the next iteration will see if `ans < L_next - 1`. If `ans` is in the next bad zone, then `ans < L_next - 1` is false, but `ans` is bad. The code doesn't check if `ans` is safe. But maybe the condition `ans < L - 1` is true only if we are before the bad zone. If we are inside, it's false. Then we check `ans + B < R + 1`. If we are inside, we might still be able to jump out. But we shouldn't be inside. The issue is that the update `ans = min(ans + B, N)` might put us inside. The editorial might rely on the fact that `ans + B` is always ≥ `R+1`, so we jump

## worker: Implement the solution in Python: read inputs, sto
The solution implements the greedy wave-propagation approach. `right` tracks the rightmost safe square currently reachable. For each bad interval `[L, R]`, we first try to advance `right` to `L-1` if the gap is large enough (`right + A <= L-1`). Then we verify we can jump over the bad zone (`right + B >= R+1`). The new landing position is clamped to `L_next - 1` to avoid landing inside the next bad zone. After processing all bad intervals, we check if `N` is reachable from the final `right` by testing `right + A <= N` (since with no further bad squares we can reach any position ≥ `right + A`).
