We need to count subsequences of length 5 where the element at position 2 (the middle) is the unique mode. For a middle element value v at index i, we must choose 2 elements before i and 2 after i (preserving order) such that in the resulting 5-tuple, v appears more times than any other value. Since the middle is v, v appears at least once; we must prevent any other value from tying or exceeding its count.

Key idea: For each index i as the middle, count pairs (L, R) of 2-element subsequences from left and right where the combined multiset has v as unique mode. This is equivalent to: no other value appears 2+ times, and no value appears 1 time in a way that ties v (i.e., v must appear 2 or 3 times if other singletons exist, or appear 2+ times and be strictly greater than any other count).

Simpler reduction: For middle value v at index i, among the 4 other chosen elements, the max count of any non-v value must be ≤ count of v minus 1, where count of v is between 1 and 3. So we need:
- If v appears once in the 5-tuple: impossible (other values can appear at most 1, but they could tie). So count_v must be ≥ 2.
- If count_v = 2: other values can appear at most 1 each.
- If count_v = 3: other values can appear at most 2, but since only 2 remaining slots, at most 1 other element with any count, which is fine as long as that count ≤ 2 (i.e., ≤ count_v - 1 = 2). Actually if count_v=3, the other 2 slots can be anything since max other count ≤ 2 ≤ 2 = count_v - 1. So any selection works.

Wait, let me reconsider. If v appears 3 times, remaining 2 slots could both be the same value x ≠ v, giving x count 2. Then v count 3 > 2, so v is unique mode. Allowed.

If v appears 2 times, remaining 2 slots: if they are both x ≠ v, then x count 2 ties v → not allowed. They must be two different non-v values, or one equals v (but that would make v count 3, already covered). So the 2 other elements must not both equal the same non-v value.

Approach:
- For each i (middle position), split array into left = nums[:i] and right = nums[i+1:].
- We need to choose 2 from left (ordered) and 2 from right (ordered) such that the middle mode condition holds.
- Since n ≤ 1000, we can do O(n^2) overall. For each i, we can iterate over pairs from left (i-1 choose 2) and pairs from right (n-i-1 choose 2), but that's O(n^4) worst case.

Better: For each i, iterate over pairs from the smaller side and use a hash map on the other side.

Let left size = L, right size = R. We choose 2 from left and 2 from right.

Fix a pair from left: (a, b) at positions p1 < p2 in left. We need to count pairs from right (c, d) at positions q1 < q2 such that the condition holds.

The condition depends on:
- count of v (which is 1 from middle + how many of {a,b,c,d} equal v)
- For each other value x ≠ v, count of x in {a,b,c,d}

We need v to have strictly maximum count.

Let me define: among the 4 chosen elements {a,b,c,d}, let f(x) = count of x. Condition: f(v) + 1 > max over x≠v of f(x), i.e., f(v) ≥ max_{x≠v} f(x).

So f(v) ≥ max_other, where max_other = max over x≠v of f(x). Since total is 4, f(v) ∈ {0,1,2,3,4}.

If f(v) = 0: max_other ≤ 0, so all 4 are non-v, but max_other ≥ 1 if any element exists. So impossible.
If f(v) = 1: max_other ≤ 1, so no non-v value appears twice. So at most one repeat among {a,b,c,d} of any non-v value.
If f(v) = 2: max_other ≤ 2, and the two non-v elements must not both be same value (else max_other = 2 ties).
If f(v) = 3: max_other ≤ 3, the one non-v element can be anything.
If f(v) = 4: max_other = 0, all 4 are v.

Case f(v) = 4: all 4 chosen are v. Count = C(L_v, 2) * C(R_v, 2) where L_v, R_v are counts of v in left/right.

Case f(v) = 3: exactly 3 of the 4 are v, 1 is non-v. Choose which 3 slots are v: 4 ways. Actually, let me count: number of ways to pick (a,b) from left and (c,d) from right such that exactly 3 of {a,b,c,d} equal v.

Sub-case: a=v, b=v, c≠v, d=v → 1 v in right. Or a=v, b=v, c=v, d≠v. Or a=v, b≠v, c=v, d=v. Or a≠v, b=v, c=v, d=v. So 4 sub-cases, each with 1 non-v in one specific position.

Hmm, this case analysis is getting complex. Let me think of inclusion-exclusion.

Total pairs (2 from left, 2 from right) = C(L,2)*C(R,2). Subtract those where condition fails.

Condition fails iff there exists x ≠ v with f(x) ≥ f(v) + 1 (impossible since f(v)+1 ≤ 5 but total is 4, so f(x) ≥ f(v)+1). Actually condition fails iff max_other ≥ f(v) + 1, or there's a tie at the top: max_other = f(v) and v is not the unique max (i.e., some x≠v has count = f(v)).

Equivalent: unique mode v iff f(v) > max_{x≠v} f(x), i.e., f(v) ≥ max_other + 1.

Hmm wait, "unique mode" means v appears strictly more than any other. So f(v) > f(x) for all x ≠ v. This means f(v) ≥ max_other + 1.

So:
- f(v) = 1: need max_other = 0, impossible.
- f(v) = 2: need max_other ≤ 1. So no two non-v elements are equal, and not two v's in the 4 (else f(v)≥2 counted differently). Wait, f(v) here is total count of v in the 4 chosen. So f(v)=2 means exactly 2 of the 4 are v. Then we need max_other ≤ 1, meaning the 2 non-v elements are distinct.
- f(v) = 3: max_other ≤ 2. The 1 non-v element is alone, so max_other ≤ 1 ≤ 2. Always satisfied. So any selection with exactly 3 v's works.
- f(v) = 4: max_other = 0. Always satisfied.

So valid configurations:
(A) Exactly 2 v's in {a,b,c,d}, and the other 2 are distinct non-v values.
(B) Exactly 3 v's in {a,b,c,d}, 1 is any non-v.
(C) All 4 are v.

Let me count each.

Let L_v = count of v in left, L_nv = L - L_v (non-v).
R_v = count of v in right, R_nv = R - R_v.

(C) All 4 v: C(L_v, 2) * C(R_v, 2).

(B) Exactly 3 v: choose 3 positions for v out of 4 slots, but slots are 2 in left + 2 in right.
- 2 v in left, 1 v in right, 1 non-v in right: C(L_v,2) * R_v * R_nv
- 2 v in right, 1 v in left, 1 non-v in left: L_v * L_nv * C(R_v, 2)
- 1 v in left, 2 v in right, ... wait that's same as above? Let me redo.

Positions: L1, L2, R1, R2 (4 positions). Exactly 3 are v.
- L1=v, L2=v, R1=v, R2=nv: C(L_v,2)*C(R_v,1)*R_nv = C(L_v,2)*R_v*R_nv
- L1=v, L2=v, R1=nv, R2=v: same by symmetry in right, so *1 for ordering? No, R1 and R2 are ordered by index, so C(R_v,1)*R_nv counts ordered (R1=v, R2=nv) but we also need (R1=nv, R2=v). 

Hmm, I need to be careful. The 2 elements from right are chosen as an ordered pair (c at smaller index, d at larger). So "1 v and 1 non-v in right" means c=v,d=nv or c=nv,d=v.

So (B) breaks into:
- 2 v in left, 1 v in right, 1 non-v in right: number of ways = C(L_v,2) * [R_v * R_nv (c=v,d=nv) + R_nv * R_v (c=nv,d=v)] = C(L_v,2) * 2*R_v*R_nv
- 2 v in right, 1 v in left, 1 non-v in left: 2*L_v*L_nv * C(R_v,2)

Wait, but the left pair is also ordered by index. So "2 v in left" means we pick 2 indices from left both with value v, and they're automatically ordered. The count is C(L_v, 2) which equals number of unordered pairs, but since they're ordered by index, C(L_v,2) is the count of ordered pairs (p1<p2). 

Hmm, I had it as: left contributes an ordered pair (a,b) with a before b. The number of ordered pairs (a,b) with a,b ∈ left, a before b, both = v is C(L_v, 2). OK.

So for (B):
- 2 v in left (C(L_v,2) ways), 1 v + 1 nv in right (R_v * R_nv + R_nv * R_v = 2*R_v*R_nv ways... wait no).

If right has 1 v and 1 nv, the ordered pair is either (v, nv) or (nv, v). Number of (v,nv) pairs = R_v * R_nv (choose v at first position, nv at second, with first index < second index). But not all such pairs are valid since we need first index < second index.

OK I need to be more careful. Let me redefine.

Let's say left has indices 0..L-1 (in original order), and we pick 2 of them: p1 < p2. The pair is characterized by (nums[p1], nums[p2]). Number of pairs with both = v: C(L_v, 2).

Similarly for right.

For "1 v and 1 nv in right (ordered)": we need q1 < q2 with one of them = v and other = nv. Count = (number of (v,nv) pairs) + (number of (nv,v) pairs).

Number of (v,nv) pairs: choose q1 ∈ {positions with v}, q2 ∈ {positions with nv, q2 > q1}. This depends on relative ordering.

Hmm, this is getting complicated because v and nv elements are interleaved.

Let me think differently. For the right side, given the 2 chosen positions q1 < q2, the pair is (nums[q1], nums[q2]). The 4 possibilities:
- (v,v): C(R_v, 2)
- (nv,nv): C(R_nv, 2)
- (v,nv): number of pairs where q1 has v, q2 has nv
- (nv,v): number of pairs where q1 has nv, q2 has v

Let me define:
- A = # pairs (q1,q2) with q1<q2, nums[q1]=v, nums[q2]=v = C(R_v,2)
- B = # pairs with nums[q1]=v, nums[q2]=nv
- C = # pairs with nums[q1]=nv, nums[q2]=v
- D = # pairs with both nv = C(R_nv,2)

A+B+C+D = C(R,2).

Similarly for left.

Now, configurations (B): exactly 3 v's in {a,b,c,d}.
The 4 slots (a,b,c,d) with a,b from left (a before b), c,d from right (c before d).
3 v's means 1 non-v. The non-v can be in a, b, c, or d.

- a=nv, b=v, c=v, d=v: count = (B_left) * (A_right) where B_left = # left pairs with a=nv, b=v.
  Wait, B_left should be pairs with nums[p1]=nv, nums[p2]=v. Let me rename: 
  - left pairs: LL_vv, LL_nvv, LL_vnv, LL_nvnv where the subscripts denote (first, second).
  - Similarly right: RR_vv, RR_nvv, RR_vnv, RR_nvnv.

Then (B) configurations:
- (nv, v, v, v): LL_nvv * RR_vv
- (v, nv, v, v): LL_vnv * RR_vv
- (v, v, nv, v): LL_vv * RR_nvv
- (v, v, v, nv): LL_vv * RR_vnv

And (A): exactly 2 v's, 2 non-v's, the 2 non-v's are distinct.
- (nv, nv, v, v): LL_nvnv * RR_vv
- (nv, v, nv, v): LL_nvv * RR_nvv
- (nv, v, v, nv): LL_nvv * RR_vnv
- (v, nv, nv, v): LL_vnv * RR_nvv
- (v, nv, v, nv): LL_vnv * RR_vnv
- (v, v, nv, nv): LL_vv * RR_nvnv

And (C): all 4 v: LL_vv * RR_vv.

This is very complex. Let me think of a simpler approach.

Alternative: Total valid = (B) + (A) + (C) = total - (configurations where condition fails).

Condition fails iff: some non-v value appears ≥ 2 times, OR all elements are non-v (but we have f(v)≥1 from middle... wait f(v) here is count in {a,b,c,d}).

Hmm, the condition is f(v) > f(x) for all x ≠ v, where f counts in the 4 chosen elements.

Let me redefine based on the 4 chosen elements {a,b,c,d}:
Let f_v = count of v, f_other(x) for x ≠ v.
Valid iff f_v > max_x f_other(x).

Equivalently: max_x f_other(x) < f_v, i.e., max_x f_other(x) ≤ f_v - 1.

Since f_v + sum f_other = 4, and f_v ≤ 4.

Cases by f_v:
- f_v = 4: max_other = 0 < 4. ✓
- f_v = 3: max_other ≤ 1 < 3. ✓ (since 1 other element)
- f_v = 2: max_other ≤ 1 < 2. Need 2 other elements to be distinct.
- f_v = 1: max_other ≤ 0 < 1. Need 3 other elements all... wait, f_v=1 means 1 v and 3 non-v, max_other could be 2 or 3. Need max_other = 0, but 3 non-v means max_other ≥ 1. Impossible.
- f_v = 0: impossible since v is the middle (f_v ≥ 1 from middle? No, f_v counts only in {a,b,c,d}, not middle).

Wait, I need to include the middle! Let me restart.

Let me redefine. The 5-tuple is (a, b, v, c, d) where v = nums[i]. Total count of v in 5-tuple = 1 (from middle) + f_v where f_v = count of v in {a,b,c,d}. Total count of x ≠ v in 5-tuple = f_x = count of x in {a,b,c,d}.

Unique mode v means 1 + f_v > f_x for all x ≠ v, i.e., f_v ≥ f_x for all x ≠ v (and f_v ≥ 1, which is true since 1+f_v > f_x ≥ 0).

Wait, 1 + f_v > f_x iff f_v ≥ f_x (since both integers). And we need strict: 1 + f_v > f_x, i.e., f_v ≥ f_x. 

Hmm, 1 + f_v > f_x means f_x < 1 + f_v, i.e., f_x ≤ f_v (integers). So we need f_x ≤ f_v for all x ≠ v.

But we also need v to be the unique mode, meaning no other value ties. So f_x ≤ f_v for all x ≠ v, AND there exists no x with f_x = 1 + f_v... wait, that's the same as f_x ≤ f_v.

Actually, 1 + f_v > f_x for all x ≠ v means v's total count (1 + f_v) is strictly greater than any other x's count (f_x). This is equivalent to: max_{x≠v} f_x ≤ f_v.

So condition: max_{x≠v} f_x ≤ f_v.

Let me redo cases by f_v (count of v in {a,b,c,d}):
- f_v = 4: max_other ≤ 4. The 4 are all v, max_other = 0. ✓
- f_v = 3: max_other ≤ 3. The 4th is some non-v, so max_other = 1 ≤ 3. ✓
- f_v = 2: max_other ≤ 2. The 2 others: max_other ≤ 2 always. ✓
- f_v = 1: max_other ≤ 1. The 3 others must have max count ≤ 1, so all distinct.
- f_v = 0: max_other ≤ 0, but 4 non-v means max_other ≥ 1. Impossible.

Wait, this changes things! With the middle contributing 1 to v's count, the condition is much more lenient.

Let me re-examine the examples.

Example 2: nums = [1,2,2,3,3,4]. Answer = 4. The valid subsequences are [1,2,2,3,4] and [1,2,3,3,4].

[1,2,2,3,4]: v=2 (middle, position 2). Counts: 1→1, 2→2, 3→1, 4→1. v count = 2, others max = 1. 2 ≥ 1. ✓
[1,2,3,3,4]: v=3 (middle, position 3). Counts: 1→1, 2→1, 3→2, 4→1. v count = 2, others max = 1. ✓
[1,2,2,3,3]: v=2 (middle, position 2). Counts: 1→1, 2→2, 3→2. v=2, others max=2. 2 ≥ 2 but not strict. Invalid. ✓ (correctly excluded)

So condition is f_v ≥ max_{x≠v} f_x (where f_v, f_x count in {a,b,c,d} only).

Cases:
- f_v = 0: max_other ≤ 0, impossible (4 non-v elements).
- f_v = 1: 1 v in {a,b,c,d}, 3 non-v. Need max of non-v counts ≤ 1, so 3 non-v are all distinct.
- f_v = 2: 2 v's, 2 non-v. max_other ≤ 2 always true. ✓
- f_v = 3: 3 v's, 1 non-v. max_other = 1 ≤ 3. ✓
- f_v = 4: 4 v's. ✓

So valid configurations:
(A) f_v = 1: 3 non-v all distinct.
(B) f_v = 2: any 2 non-v.
(C) f_v = 3: any 1 non-v.
(D) f_v = 4: 0 non-v.

Now let's count. Let me use:
- L_v, L_nv = L - L_v (counts in left).
- R_v, R_nv = R - R_v (counts in right).

Also, I need the "cross" counts: pairs where first = v, second = nv, etc. This depends on interleaving.

Hmm, the problem is that for the 2 non-v elements (in case A with f_v=1, or in case B with f_v=2), I need to count configurations carefully.

Let me think about it by splitting left/right contributions.

For a configuration specified by (left pair type, right pair type), the count is product of left count and right count.

Left pair types (for the 2 elements from left):
- (v,v): L_vv = C(L_v, 2)
- (v,nv): L_vnv = # pairs (p1<p2) with nums[p1]=v, nums[p2]≠v
- (nv,v): L_nvv = # pairs with nums[p1]≠v, nums[p2]=v
- (nv,nv): L_nvnv = C(L,2) - L_vv - L_vnv - L_nvv

Similarly for right.

The four slot values (a,b,c,d) and their counts of v and non-v determine f_v and the multiset of non-v values.

Let me enumerate by (f_v in left, f_v in right):
- f_v in left = 0: left pair is (nv,nv). Count = L_nvnv.
- f_v in left = 1: left pair is (v,nv) or (nv,v). Count = L_vnv + L_nvv.
- f_v in left = 2: left pair is (v,v). Count = L_vv.

Similarly for right. Total f_v = f_v_left + f_v_right.

Valid (A): f_v = 1, 3 non-v distinct. Sub-cases:
- f_v_left=0, f_v_right=1: left is (nv,nv), right is (v,nv) or (nv,v). 2 non-v in left, 1 in right. Need all 3 distinct. So 2 non-v in left are distinct AND different from the 1 non-v in right. But left (nv,nv) means both non-v, and we need them distinct AND ≠ the right non-v.
  - # valid = sum over distinct non-v values x,y in left with x≠y, and right non-v z ≠ x, y. Complex.

This is getting very complex due to the "distinct" constraint.

Alternative approach: For each middle i, iterate over the smaller of left/right side, and for each pair from that side, use a hashmap on the other side to count valid completions.

Actually, let me think. For each i, let's iterate over pairs (p1, p2) from the smaller side (say left if L < R). For each such pair, we know the multiset of values. We need to count pairs (q1, q2) from the right such that the combined 4-tuple (with middle v) has v as unique mode.

For each left pair, the count of valid right pairs can be computed if we precompute, for the right side, statistics about the 2-element pairs.

Let me precompute for the right side:
- RR_vv = C(R_v, 2) (pairs both v)
- RR_total = C(R, 2)
- RR_with_dup = # pairs where both elements are the same (i.e., a pair (x,x) for some x). This = sum_x C(count_x, 2) over all values x in right.

For a left pair, let left_set = multiset of the 2 values. We want to count right pairs such that combined 4 (with v) has v as unique mode.

Condition on combined {a,b,c,d}: f_v ≥ max_{x≠v} f_x.

Let me denote the left pair's contribution: if left has (a,b), then f_v contribution = [a==v] + [b==v], and for each x≠v, the count from left is [a==x] + [b==x].

Let f_v_L = # v in left pair (0, 1, or 2).
For each x ≠ v, f_x_L = # x in left pair (0, 1, or 2; specifically 0, 1, or 2 but constrained: sum over x = 2 - f_v_L).

We need f_v_L + f_v_R ≥ max_x (f_x_L + f_x_R).

Case 1: f_v_L = 2 (left is (v,v)). Then f_v ≥ 2 + f_v_R ≥ 2. max_other = max_x f_x_R. Need 2 + f_v_R ≥ max_x f_x_R, always true since max_x f_x_R ≤ 2 and f_v_R ≥ 0, so 2 + f_v_R ≥ 2 ≥ max. ✓ All right pairs valid.

So if left = (v,v), all C(R,2) right pairs work.

Case 2: f_v_L = 1 (left has exactly 1 v). Then f_v = 1 + f_v_R. We need 1 + f_v_R ≥ max_x (f_x_L + f_x_R).

Sub-case 2a: left is (v, x) with x ≠ v. Then f_x_L = 1, f_y_L = 0 for y ≠ x, y ≠ v.
Need 1 + f_v_R ≥ max(1 + f_x_R, max_{y≠v,x} f_y_R) = 1 + max(f_x_R, max_{y≠v,x} f_y_R).
So f_v_R ≥ max(f_x_R, max_{y≠v,x} f_y_R) = max_{y≠v} f_y_R.
This means: count of v in right ≥ count of any non-v in right.

Sub-case 2b: left is (x, v) with x ≠ v. Same as 2a by symmetry (the multiset is the same: {v, x}).

So in case 2, left pair is {v, x} for some x ≠ v (or x = v, but that's case 1). The condition is: in the right pair, v appears ≥ every other value.

This is a strong condition! Let's count right pairs where v is the most frequent (or tied for most, but we need f_v_R ≥ f_y_R for all y).

Actually we need f_v_R ≥ f_y_R for all y ≠ v, which means v is a mode (or tied mode) of the right pair. But the right pair has only 2 elements.

Right pair (c,d):
- (v,v): f_v_R=2, others 0. ✓
- (v, y) with y≠v: f_v_R=1, f_y_R=1. ✓ (1≥1)
- (y, v) with y≠v: same. ✓
- (y, z) with y,z ≠ v (could be y=z or y≠z): f_v_R=0, f_y_R≥1. Need 0 ≥ f_y_R, impossible.

So in case 2, valid right pairs: those with at least 1 v. Count = C(R,2) - C(R_nv, 2) = total right pairs - pairs of 2 non-v.

Wait, but I also need to exclude cases where some y ≠ v appears 2 times in right, but that's already excluded since "at least 1 v" means at most 1 non-v.

Let me recount: right pairs with at least 1 v = total - pairs with 0 v = C(R,2) - C(R_nv, 2). ✓

But wait, we also need f_v_R ≥ f_y_R. If right is (v,y), f_v_R=1, f_y_R=1, OK. If right is (y,y), f_v_R=0, f_y_R=2, not OK. The condition "at least 1 v" correctly excludes (y,y) and (y,z) for y,z ≠ v.

Hmm, but what about (v, y) where y appears in left? We need f_v_R ≥ f_y_R, i.e., 1 ≥ 1. OK. So any right pair with at least 1 v works.

So case 2: left = {v, x} (x can be anything, including v, but we said x ≠ v). For each such left pair, valid right pairs = C(R,2) - C(R_nv, 2).

Wait, but the left pair (v,v) is case 1, not case 2. In case 2, left has exactly 1 v, so the other element is some x ≠ v. But we should consider: does x matter? From the analysis, the condition is "right has at least 1 v", regardless of x. So yes, for any left pair with exactly 1 v, valid right pairs = C(R,2) - C(R_nv,2).

But wait, I need to double check. Left = (v, x), right = (v, y). Then {a,b,c,d} = {v, x, v, y}. f_v = 2, f_x = 1, f_y = 1. max_other = 1 ≤ 2 = f_v. ✓

Left = (v, x), right = (v, v). f_v = 3, f_x = 1. max_other = 1 ≤ 3. ✓

Left = (v, x), right = (v, v). Wait I already did this.

Left = (v, x), right = (x, x). f_v = 1, f_x = 3. max_other = 3 > 1. ✗. And this is correctly excluded since right has 0 v.

So case 2 count = (number of left pairs with exactly 1 v) * (C(R,2) - C(R_nv, 2)).

Case 3: f_v_L = 0 (left has 0 v). Then f_v = f_v_R. Need f_v_R ≥ max_x f_x_L + f_x_R = (2 from left, distributed) + f_x_R.

Wait, f_x_L for the left pair. Left pair is (x1, x2) with x1, x2 ≠ v. So f_x_L ≥ 0 for all x, and sum = 2.

Need f_v_R ≥ f_x_L + f_x_R for all x ≠ v.

Since f_v_R ≤ 2 (right has only 2 elements), and f_x_L + f_x_R ≥ f_x_L.

If left = (x, x) (both same non-v), then f_x_L = 2, so need f_v_R ≥ 2 + f_x_R ≥ 2, so f_v_R = 2 and f_x_R = 0. So right must be (v,v).

If left = (x, y) with x ≠ y, both ≠ v, then f_x_L = 1, f_y_L = 1, others 0. Need:
- f_v_R ≥ 1 + f_x_R
- f_v_R ≥ 1 + f_y_R
- f_v_R ≥ f_z_R for z ≠ v,x,y

Since f_v_R ≤ 2, we need 1 + f_x_R ≤ 2, so f_x_R ≤ 1, similarly f_y_R ≤ 1.

Sub-sub-cases:
- f_v_R = 0: need 0 ≥ 1 + f_x_R, impossible.
- f_v_R = 1: need 1 ≥ 1 + f_x_R, so f_x_R = 0. Similarly f_y_R = 0. So right has 1 v and 1 non-v, and that non-v is not x or y. 
  - Right = (v, z) or (z, v) with z ≠ v, x, y.
- f_v_R = 2: need 2 ≥ 1 + f_x_R, so f_x_R ≤ 1 (always true). Similarly f_y_R ≤ 1. Right = (v,v). ✓

So for left = (x,y) distinct, x,y ≠ v:
- Right = (v,v): valid.
- Right = (v, z) or (z, v) with z ∉ {v, x, y}: valid.
- Right with 0 v or with z ∈ {x,y}: invalid.

Hmm, this depends on x, y specifically! So I can't just use a simple formula; I need to track which non-v values appear.

This makes the problem harder. Let me reconsider.

Given the complexity, maybe a different approach: for each i as middle, iterate over all 2-subsets from the smaller side, and for each, compute the valid count from the larger side using precomputed maps.

n ≤ 1000, so for each i, C(min(L,R), 2) iterations. Total over i: sum_i C(min(L_i, R_i), 2). In worst case, L = R = n/2, so each i contributes C(n/2, 2) ≈ n^2/8. Total ≈ n^3/8 ≈ 1.25 * 10^8. Might be tight but feasible in Python with optimization. Actually 1000^3 / 8 = 1.25e8, which is slow.

Alternative: for each i, iterate over 2-subsets of left (C(L,2)) and for each, look up in a precomputed right map. C(L,2) ≤ 5e5, and n=1000, so total = sum_i C(L_i, 2) = sum_i C(i, 2) ≈ n^3/6 ≈ 1.67e8. Still slow.

Better: for each i, iterate over 2-subsets of the smaller side, and for the larger side, precompute a map from "value multiset" to count. But the condition is complex.

Let me think more carefully. The "valid right pairs" for a given left pair (a,b):

Let me define for the right side, I want to query: given a left pair (a,b), how many right pairs (c,d) make the combined 4-tuple (a,b,c,d) valid (v is unique mode)?

Valid iff f_v ≥ max_{x≠v} f_x, where f counts in {a,b,c,d}.

This depends on the multiset {a,b} and the multiset {c,d}. Let me categorize by the "type" of left pair:

Left pair types:
1. (v,v): valid right pairs = C(R,2) (all).
2. (v, x) with x ≠ v: valid right pairs = C(R,2) - C(R_nv, 2) (right has ≥1 v).

Wait, I need to double check. If left = (v, x) and right = (y, z) with y,z ≠ v (both non-v), then combined {v, x, y, z}. f_v = 1, max_other = max(1, 1) = 1. Need f_v ≥ max_other, i.e., 1 ≥ 1. ✓.

Oh! I made an error before. Let me redo.

f_v = count of v in {a,b,c,d}. If left = (v,x), right = (y,z) with x,y,z ≠ v, then f_v = 1. max_other = max(f_x, f_y, f_z) = max(1, 1, 1) = 1 (assuming x,y,z distinct, or if some equal, larger).

If x = y, then f_x = f_y = 2 (wait, f_x counts in {a,b,c,d} = {v, x, x, z}, so f_x = 2, f_z = 1). max_other = 2 > 1 = f_v. ✗

If x, y, z all distinct and ≠ v, then max_other = 1 = f_v. ✓

So for left = (v, x), right = (y, z) with y,z ≠ v:
- Valid iff max(f_x in {a,b,c,d}, f_y, f_z) ≤ f_v = 1.
- f_x in {a,b,c,d} = 1 + f_x in right. So f_x = 1 + [y=x] + [z=x].
- If y = x or z = x, then f_x ≥ 2 > 1. ✗
- If y, z ≠ x, then f_x = 1, f_y = 1, f_z = 1. ✓

So valid right pairs (with both non-v): both ≠ x. Count = C(R_nv - count_x_in_right, 2) where count_x_in_right = # of x in right.

Hmm, but this is if right is both non-v. What if right has 1 v?

Let me redo case 2 (left = (v, x), x ≠ v) properly.

Right pair (c, d):
- (v, v): combined {v, x, v, v}. f_v = 3, f_x = 1. max_other = 1 ≤ 3. ✓
- (v, y) y ≠ v: combined {v, x, v, y}. f_v = 2, f_x = 1, f_y = 1. max_other = 1 ≤ 2. ✓ (regardless of whether y = x or not)
- (y, v) y ≠ v: same. ✓
- (y, z) y,z ≠ v: combined {v, x, y, z}. f_v = 1. f_x = 1 + [y=x]+[z=x]. f_y = 1+[z=y]. f_z = 1.
  - If y = z = x: f_x = 3, max = 3 > 1. ✗
  - If exactly one of y,z = x: f_x = 2 > 1. ✗
  - If y, z ≠ x: f_x = 1, f_y ≤ 1, f_z ≤ 1. max_other = max(1, 1, 1) = 1 = f_v. ✓
  - If y = z ≠ x: f_y = 2 > 1. ✗
  - If y = z = x: covered.
  - If y ≠ z, both ≠ x: ✓ (assuming y ≠ v, z ≠ v, which is given).

Wait, I need f_y ≤ f_v = 1. If y = x, f_y = f_x = 2 > 1. ✗. If y ≠ x and y ≠ v, f_y = 1 ≤ 1. ✓. If y = v, then this is the (v, y) case, not the both-non-v case.

OK so summarizing for left = (v, x), x ≠ v:
- Right (v,v): ✓
- Right (v, y) or (y, v), y ≠ v: ✓ (any y, including y = x)
- Right (y, z), y,z ≠ v: ✓ iff neither y nor z equals x.

So valid right pairs = C(R,2) - C(R_nv, 2) + (right both non-v, neither = x).

The right both non-v neither = x count = C(R_nv - cnt_x_right, 2) where cnt_x_right = count of x in right.

So total = [C(R,2) - C(R_nv,2)] + C(R_nv - cnt_x_right, 2).

Hmm, this depends on cnt_x_right, which depends on x.

Let me define: for the right side, let g(x) = count of x in right (for x ≠ v). Then:

Valid right pairs for left = (v, x) = C(R,2) - C(R_nv, 2) + C(R_nv - g(x), 2).

But C(R,2) - C(R_nv, 2) = total right pairs with at least 1 v = RR_vv + RR_vnv + RR_nvv.

And C(R_nv - g(x), 2) = pairs in right that are both non-v and both ≠ x.

So valid = (right pairs with ≥1 v) + (right pairs both non-v, both ≠ x).

= (right pairs) - (right pairs both non-v, at least one = x)
= C(R,2) - C(R_nv, 2) + C(R_nv - g(x), 2).

Hmm, or: = C(R,2) - [C(R_nv, 2) - C(R_nv - g(x), 2)] = C(R,2) - (pairs both non-v with at least one = x).

Pairs both non-v with at least one = x = C(R_nv, 2) - C(R_nv - g(x), 2) = g(x) * (R_nv - g(x)) + C(g(x), 2). Hmm, or more directly: # pairs (y, z) with y < z, y,z ∈ right, y,z ≠ v, and (y = x or z = x) = g(x) * (R_nv - 1) if we think of it as... no wait.

# unordered pairs {y, z} with y, z in right, y ≠ z, both ≠ v, and (y = x or z = x): 
- {x, w} where w ∈ right, w ≠ v, w ≠ x: g(x) * (R_nv - g(x)) pairs.
- Plus {x, x}: C(g(x), 2) pairs.

Wait, I want ordered or unordered? The right pair (c, d) is ordered (c < d in index). So (y, z) with y at smaller index, z at larger.

The count of ordered pairs (c, d) with c < d, c and d both ≠ v, and (c = x or d = x):

Hmm, this depends on the positions of x and other non-v values in right. It's not simply g(x) * (R_nv - g(x)) + C(g(x), 2) because the ordering matters.

Actually, for unordered pairs {y, z} (y and z are values, not positions), the count of position-pairs is not simply determined by value counts.

OK this is getting complicated. Let me think of a different approach.

For each middle i, I'll iterate over 2-subsets from the left side (L choose 2 ≤ 5e5 per i, but n=1000 so average is small), and for each left pair, I'll iterate over 2-subsets from the right side to check validity. But that's O(L^2 * R^2) per i.

Alternatively, for each i, precompute for the right side a map from (multiset of 2 values) to count. Then for each left pair, look up the valid right pairs.

A pair (c, d) with c at position q1, d at position q2 (q1 < q2) is characterized by the multiset {nums[q1], nums[q2]}. The multiset is one of: {v,v}, {v, x} for x ≠ v, {x, x} for x ≠ v, {x, y} for x ≠ y, x,y ≠ v.

The count of right pairs with multiset {v, v}: RR_vv = C(R_v, 2).
The count of right pairs with multiset {v, x} (x ≠ v): RR_vx. This depends on positions of v and x in right.
The count of right pairs with multiset {x, x} (x ≠ v): RR_xx = C(cnt_x_right, 2).
The count of right pairs with multiset {x, y} (x ≠ y, both ≠ v): RR_xy.

For each left pair (a, b) with multiset M_L, I need to count right pairs with multiset M_R such that combined {a,b,c,d} satisfies f_v ≥ max_other.

This is complex. Let me think of a cleaner formulation.

Let me define for the right side a function F(left_multiset) = # right pairs making combined valid.

Given the complexity, maybe iterate over 2-subsets from the smaller side and for each, enumerate valid right pairs. To enumerate valid right pairs, precompute for right: total pairs, pairs with ≥1 v, etc., and also for specific x, pairs involving x.

Actually, let me just do O(n^3) or O(n^4) carefully and see if it fits. n=1000, n^3 = 10^9, too slow. n^2 * log n = 10^6 * 10 = 10^7, fine.

Let me think O(n^2): for each i (middle), O(n) work. Total O(n^2).

For each i, can I compute the count in O(R) or O(L) time?

For each i, the count is sum over left pairs * (right pairs compatible). The right pairs compatible depends on the left pair.

If I fix a left pair and want to know valid right pairs, it depends on the left pair's values. So I need to group left pairs by some key and for each key, compute the right count.

Keys for left pair (based on what affects validity):
- (v, v): all right pairs valid.
- (v, x) for x ≠ v: valid right pairs = C(R,2) - (right pairs both non-v with at least one = x).
- (x, x) for x ≠ v: combined {x, x, c, d}. f_v = f_v_R. max_other = max(2 + f_x_R, f_y_R for y ≠ v,x).
  Need f_v_R ≥ 2 + f_x_R and f_v_R ≥ f_y_R.
  - f_v_R ≤ 2, so f_v_R ≥ 2 + f_x_R ≥ 2, so f_v_R = 2 and f_x_R = 0. So right = (v, v) only.
- (x, y) for x ≠ y, both ≠ v: combined {x, y, c, d}. f_v = f_v_R. max_other = max(1 + f_x_R, 1 + f_y_R, f_z_R for z ≠ v,x,y).
  Need f_v_R ≥ 1 + f_x_R, f_v_R ≥ 1 + f_y_R, f_v_R ≥ f_z_R.
  Since f_v_R ≤ 2:
  - f_v_R = 2: need 2 ≥ 1 + f_x_R → f_x_R ≤ 1 (always). Similarly f_y_R ≤ 1. ✓ So right = (v, v).
  - f_v_R = 1: need 1 ≥ 1 + f_x_R → f_x_R = 0. Similarly f_y_R = 0. And f_z_R ≤ 1. So right has 1 v, 1 non-v, and that non-v is not x or y.
  - f_v_R = 0: need 0 ≥ 1 + f_x_R, impossible.

So for left = (x, y) distinct, x, y ≠ v:
- Right = (v, v): valid. Count = C(R_v, 2).
- Right = (v, z) or (z, v) with z ≠ v, z ≠ x, z ≠ y: valid.
- Right with 0 v: invalid (unless... let me recheck).
  Right = (z, w) with z, w ≠ v. f_v = 0. f_x = 1 + [z=x]+[w=x]. f_y = 1 + [z=y]+[w=y]. Need 0 ≥ 1 + f_x_R, impossible. ✗
- Right = (v, x) or (x, v): f_v = 1, f_x = 1 + 1 = 2, f_y = 1. Need 1 ≥ 2. ✗
- Right = (v, y) or (y, v): f_x = 1 + 0 = 1, f_y = 2. Need 1 ≥ 2. ✗
- Right = (v, z), z ≠ x,y: f_v = 1, f_x = 1, f_y = 1, f_z = 1. ✓

So for left = (x, y) distinct, valid right pairs = C(R_v, 2) + [right has 1 v and 1 non-v ≠ x, ≠ y].

Right has 1 v and 1 non-v ≠ x, ≠ y: the non-v must be a value z ≠ v, x, y. The number of such ordered pairs (c, d) with one = v and other = z, z ∉ {v, x, y}.

This depends on positions. Let me define for right:
- h(x) = # positions in right with value x, for x ≠ v.
- pos_v = positions of v in right.
- For z ≠ v, pos_z = positions of z.

# ordered pairs (c, d), c < d, with {c, d} = {v, z}: = (# positions of v before positions of z) + (# positions of z before positions of v) - ... actually it's just # pairs with one = v, one = z = h(v) * h(z) ... no wait, it's # (c < d) with (c=v, d=z) + # (c < d) with (c=z, d=v) = h(v) * h(z) ... hmm no, because we need c < d, so not all v-z combinations work.

# (c < d) with c = v, d = z: for each v-position i and z-position j with i < j. This is (# v before # z) type, not simply h(v)*h(z).

OK so this depends on the relative ordering of v and z in right. This is annoying.

Let me think of yet another approach.

Precompute for the right side, for each value z, the number of right pairs (c, d) with c < d that are "compatible" in some sense.

Actually, the key insight: for right, I want to answer queries of the form "how many pairs (c, d) with c < d have a given property P that depends on a left pair".

The left pair determines constraints on (c, d). Let me categorize the constraints:

For left pair type:
T1: (v, v) → all (c, d). Count = C(R, 2).
T2: (v, x) with x ≠ v → (c, d) has at least one v, OR (c, d) both non-v and neither = x.
T3: (x, x) with x ≠ v → (c, d) = (v, v). Count = C(R_v, 2).
T4: (x, y) distinct, x, y ≠ v → (c, d) = (v, v), or (c, d) has one v and one non-v ≠ x, y.

For T2 and T4, the count depends on the specific value x (and y).

Let me precompute for right:
- RR_vv = C(R_v, 2)
- RR_nv_total = C(R_nv, 2) = # pairs both non-v.
- For each value x ≠ v, RR_xx = C(cnt_x_right, 2) = # pairs both = x in right.
- For each value z ≠ v, # right pairs with exactly one v and one = z. This = # (c < d) with c = v, d = z + # (c < d) with c = z, d = v. Let me call this RR_vz.

Then:
- T2 count for left = (v, x): C(R, 2) - [RR_nv_total - C(cnt_x_right, 2)] - [pairs both non-v, one = x, one ≠ x]
  Wait, valid = pairs with ≥1 v + pairs both non-v, both ≠ x.
  = C(R, 2) - RR_nv_total + C(cnt_x_right, 2) ... no.
  = [C(R, 2) - RR_nv_total] + C(R_nv - cnt_x_right, 2)
  = [pairs with ≥1 v] + C(R_nv - cnt_x_right, 2).

Hmm, C(R_nv - cnt_x_right, 2) = pairs both non-v, both ≠ x = RR_nv_total - [pairs both non-v with at least one = x] = RR_nv_total - [cnt_x_right * (R_nv - cnt_x_right) + C(cnt_x_right, 2) ... wait no, that's for unordered value pairs, but position pairs is different].

Ugh, position pairs vs value pairs. Let me redefine carefully.

Let right positions be indexed. Let f(x) = # positions in right with value x. For x ≠ v, let f(x) be the count.

# position pairs (c, d) with c < d, both in right, both non-v, both = x: C(f(x), 2).
# position pairs both non-v, both ≠ x: = C(R_nv - f(x), 2). This counts pairs of positions, both non-v, neither = x. This is correct because if we exclude positions with value x, the remaining non-v positions number R_nv - f(x), and pairs among them = C(R_nv - f(x), 2). 

But wait, the positions with value x are excluded, so the remaining positions are those with value ≠ v and ≠ x. Pairs among them (c < d) are counted. So C(R_nv - f(x), 2) is correct.

OK so T2 count = [pairs with ≥1 v] + C(R_nv - f(x), 2) = [C(R, 2) - C(R_nv, 2)] + C(R_nv - f(x), 2).

For T4 with left = (x, y), x ≠ y, x, y ≠ v:
Valid = C(R_v, 2) + [# pairs with exactly one v, one non-v, non-v ∉ {x, y}]
= C(R_v, 2) + sum_{z ∉ {v, x, y}} RR_vz.

RR_vz = # pairs (c < d) with {c, d} = {v, z}.

Now sum_{z ∉ {v, x, y}} RR_vz = [sum_{z ≠ v} RR_vz] - RR_vx - RR_vy.

And sum_{z ≠ v} RR_vz = # pairs (c < d) with exactly one v and one non-v = R_v * R_nv ... no wait, it's not R_v * R_nv because of the c < d constraint.

sum_{z ≠ v} RR_vz = total # pairs (c < d) with one = v, one = non-v = sum over v-positions of (# non-v after) + sum over v-positions of (# non-v before) ... = # (c < d) with c = v, d ≠ v + # (c < d) with c ≠ v, d = v.

Let me define for the right array:
- pref_vv[i] = # v in right before position i.
- suff_vv[i] = # v in right after position i.
- etc.

Actually, let me just precompute: for each position i in right, prefix counts and suffix counts of each value. But there can be up to n distinct values, so we need to compress.

Values are in [-10^9, 10^9], up to n=1000 distinct. We can compress them.

For each i (middle), and for the right subarray, I want:
- For each value z ≠ v, RR_vz = # pairs (c < d) in right with {nums[c], nums[d]} = {v, z}.

This is: for each v-position p in right, # z-positions q in right with q > p, plus # z-positions q in right with q < p. = (for each p with nums[p]=v) [(# z after p) + (# z before p)] = h(v) * h(z) ... no wait, that would be if we allowed c > d too, but we have c < d.

# (c < d, c = v, d = z) = sum_{p: nums[p]=v} (# z-positions q > p).
# (c < d, c = z, d = v) = sum_{p: nums[p]=v} (# z-positions q < p).
Total RR_vz = sum_{p: nums[p]=v} (# z-positions ≠ p) = h(v) * h(z). 

Wait, that's because for each v-position p, the z-positions q with q ≠ p (either q < p or q > p) all contribute, and c < d is automatic depending on which is smaller. Let me recount.

For fixed v-position p, the pairs (c, d) with c < d, c = v or d = v (specifically d = v or c = v at position p):
- If c = p (so nums[c] = v), d = q with q > p and nums[q] = z: count = # z after p.
- If d = p, c = q with q < p and nums[q] = z: count = # z before p.

Total for this p: # z after p + # z before p = h(z) - [p is z] = h(z) (since p is v, not z).

Summing over all v-positions p: h(v) * h(z).

So RR_vz = h(v) * h(z). 

Similarly, for left, we can define analogous quantities.

So the valid count for T4 left = (x, y):
C(R_v, 2) + sum_{z ≠ v, x, y} RR_vz = C(R_v, 2) + h(v) * sum_{z ≠ v, x, y} h(z) = C(R_v, 2) + h(v) * (R_nv - h(x) - h(y)).

So this depends on h(x) and h(y) in right.

Now, to compute the total for middle i, I need to sum over all left pairs:
- T1: (v, v) left pairs. Count = C(L_v, 2). Each contributes C(R, 2).
- T2: (v, x) left pairs for x ≠ v. For each x, # left pairs (v, x) or (x, v) = (depends on positions). Let me define LL_vx = # left pairs (a, b) with a < b, {nums[a], nums[b]} = {v, x}. This = h_left(v) * h_left(x) (by similar argument, since we need one = v, one = x, and a < b, total = h(v)*h(x)).

  Wait, is LL_vx = h_left(v) * h_left(x)? Let me verify. For each v-position p in left, # x-positions q ≠ p in left. Each such (p, q) with p < q or p > q gives a pair. Total = h(v) * h(x). And each pair is counted once. Yes, LL_vx = h_left(v) * h_left(x).

  Hmm, but this includes pairs where a = v, b = x (a < b) and a = x, b = v (a < b). Both are valid left pairs (a, b) with a < b. So total = h(v) * h(x). ✓

  So # left pairs with multiset {v, x} for x ≠ v is h_left(v) * h_left(x). Let me call this L_vx.

  For each such x, contribution = L_vx * T2_count(x) = L_vx * [C(R, 2) - C(R_nv, 2) + C(R_nv - h_right(x), 2)].

  Sum over x ≠ v.

- T3: (x, x) left pairs for x ≠ v. Count = C(h_left(x), 2). Each contributes C(R_v, 2).

- T4: (x, y) left pairs for x ≠ y, x, y ≠ v. Count = h_left(x) * h_left(y) (similar to T2). Each contributes C(R_v, 2) + h_right(v) * (R_nv - h_right(x) - h_right(y)).

So total for middle i = T1 + T2_sum + T3_sum + T4_sum.

Let me write this out.

T1 = C(L_v, 2) * C(R, 2)

T2_sum = sum_{x ≠ v} h_left(v) * h_left(x) * [C(R, 2) - C(R_nv, 2) + C(R_nv - h_right(x), 2)]
       = h_left(v) * sum_{x ≠ v} h_left(x) * [C(R, 2) - C(R_nv, 2) + C(R_nv - h_right(x), 2)]
       = h_left(v) * [L_nv * (C(R, 2) - C(R_nv, 2)) + sum_{x ≠ v} h_left(x) * C(R_nv - h_right(x), 2)]

where L_nv = sum_{x ≠ v} h_left(x) = L - L_v.

T3_sum = sum_{x ≠ v} C(h_left(x), 2) * C(R_v, 2)
       = C(R_v, 2) * sum_{x ≠ v} C(h_left(x), 2)

T4_sum = sum_{x ≠ y, x,y ≠ v} h_left(x) * h_left(y) * [C(R_v, 2) + h_right(v) * (R_nv - h_right(x) - h_right(y))]

Let me expand T4_sum:
= C(R_v, 2) * sum_{x ≠ y, x,y ≠ v} h_left(x) * h_left(y) + h_right(v) * sum_{x ≠ y, x,y ≠ v} h_left(x) * h_left(y) * (R_nv - h_right(x) - h_right(y))

sum_{x ≠ y, x,y ≠ v} h_left(x) * h_left(y) = [sum_{x ≠ v} h_left(x)]^2 - sum_{x ≠ v} h_left(x)^2 = L_nv^2 - S2_left, where S2_left = sum_{x ≠ v} h_left(x)^2.

The second sum:
sum_{x ≠ y, x,y ≠ v} h_left(x) * h_left(y) * (R_nv - h_right(x) - h_right(y))
= R_nv * sum_{x ≠ y} h_left(x) h_left(y) - sum_{x ≠ y} h_left(x) h_left(y) (h_right(x) + h_right(y))
= R_nv * (L_nv^2 - S2_left) - sum_{x ≠ y, x,y ≠ v} h_left(x) h_left(y) h_right(x) - sum_{x ≠ y, x,y ≠ v} h_left(x) h_left(y) h_right(y)

By symmetry (swap x and y), the last two sums are equal:
sum_{x ≠ y, x,y ≠ v} h_left(x) h_left(y) h_right(x) = sum_{x ≠ y, x,y ≠ v} h_left(y) h_left(x) h_right(y)
So they are equal, call it P = sum_{x ≠ y, x,y ≠ v} h_left(x) h_left(y) h_right(x).

Then the second sum = 2P.

So T4_sum = C(R_v, 2) * (L_nv^2 - S2_left) + h_right(v) * [R_nv * (L_nv^2 - S2_left) - 2P].

This is getting complex. Let me think if there's a simpler way.

Alternative: instead of grouping by value, just iterate over left pairs and for each, compute the right count.

For each i, iterate over left pairs (a, b) with a < b. For each, compute the number of valid right pairs.

To compute valid right pairs for a given left pair, I need to sum over right pairs (c, d) with c < d the indicator "valid".

# valid right pairs = total right pairs - # invalid right pairs.

Invalid: combined 4-tuple (a, b, c, d) has max_other > f_v.

Hmm, let me think of a direct formula.

For left = (a, b) (specific ordered pair, or multiset), the valid right pairs depend on {a, b}'s multiset.

Case left = {v, v}: valid = C(R, 2).
Case left = {v, x}, x ≠ v: valid = [pairs with ≥1 v] + [pairs both non-v, both ≠ x] = [C(R,2) - C(R_nv, 2)] + C(R_nv - h_right(x), 2).
Case left = {x, x}, x ≠ v: valid = C(R_v, 2).
Case left = {x, y}, x ≠ y, both ≠ v: valid = C(R_v, 2) + h_right(v) * (R_nv - h_right(x) - h_right(y)).

For the last two cases, the valid count depends on x and y (or just x in case 3).

So if I iterate over all left pairs, I can group them:
- Multiset {v, v}: count C(L_v, 2), each contributes C(R, 2).
- Multiset {v, x} for each x ≠ v: count h_left(v) * h_left(x), each contributes [C(R,2) - C(R_nv, 2)] + C(R_nv - h_right(x), 2).
- Multiset {x, x} for each x ≠ v: count C(h_left(x), 2), each contributes C(R_v, 2).
- Multiset {x, y} for each x < y, both ≠ v: count h_left(x) * h_left(y), each contributes C(R_v, 2) + h_right(v) * (R_nv - h_right(x) - h_right(y)).

Wait, for multiset {v, x}, the # left pairs is h_left(v) * h_left(x) (as computed, since one is v and one is x, a < b, total = h(v)*h(x)). But this counts both (a=v, b=x) and (a=x, b=v) as a < b, which is correct since a < b in index.

But the left pair as a multiset is {v, x} regardless of order. So in my formula, I should use the multiset, and the count is the # left pairs with that multiset.

For multiset {v, x}: # left pairs = h_left(v) * h_left(x). ✓
For multiset {x, x}: # left pairs = C(h_left(x), 2). ✓
For multiset {x, y}, x ≠ y: # left pairs = h_left(x) * h_left(y). ✓

OK so now the total for middle i is:

total = C(L_v, 2) * C(R, 2)  [T1]
      + sum_{x ≠ v} h_L(v) * h_L(x) * ([C(R,2) - C(R_nv, 2)] + C(R_nv - h_R(x), 2))  [T2]
      + sum_{x ≠ v} C(h_L(x), 2) * C(R_v, 2)  [T3]
      + sum_{x < y, x,y ≠ v} h_L(x) * h_L(y) * [C(R_v, 2) + h_R(v) * (R_nv - h_R(x) - h_R(y))]  [T4]

Let me simplify. Let me denote:
- a = h_L(v), b = R = |right|, c = h_R(v), d = R_nv = R - c, so b = L, etc. Let me just use L, R, L_v, R_v, L_nv = L - L_v, R_nv = R - R_v.
- For each value x ≠ v, let l_x = h_L(x), r_x = h_R(x).

T1 = C(L_v, 2) * C(R, 2).

T2 = h_L(v) * sum_{x ≠ v} h_L(x) * [C(R, 2) - C(R_nv, 2) + C(R_nv - r_x, 2)]
   = L_v * [L_nv * (C(R, 2) - C(R_nv, 2)) + sum_{x ≠ v} l_x * C(R_nv - r_x, 2)]

T3 = C(R_v, 2) * sum_{x ≠ v} C(l_x, 2)

T4 = sum_{x < y, x,y ≠ v} l_x * l_y * [C(R_v, 2) + R_v * (R_nv - r_x - r_y)]
   = C(R_v, 2) * sum_{x < y} l_x l_y + R_v * sum_{x < y} l_x l_y (R_nv - r_x - r_y)
   = C(R_v, 2) * [L_nv^2 - sum l_x^2] / 2 + R_v * sum_{x < y} l_x l_y (R_nv - r_x - r_y)

Wait, sum_{x < y} l_x l_y = (L_nv^2 - sum l_x^2) / 2.

For the second part: sum_{x < y} l_x l_y (R_nv - r_x - r_y) = R_nv * sum_{x<y} l_x l_y - sum_{x<y} l_x l_y (r_x + r_y).

sum_{x<y} l_x l_y r_x = ? Let S = sum_x l_x * r_x * (sum_{y ≠ x} l_y) = sum_x l_x r_x (L_nv - l_x) = L_nv * sum_x l_x r_x - sum_x l_x^2 r_x.

And sum_{x<y} l_x l_y (r_x + r_y) = sum_{x<y} l_x l_y r_x + sum_{x<y} l_x l_y r_y = 2 * sum_{x<y} l_x l_y r_x (by symmetry) = 2 * (1/2) * sum_{x ≠ y} l_x l_y r_x = sum_{x ≠ y} l_x l_y r_x.

Wait, sum_{x<y} l_x l_y r_x + sum_{x<y} l_x l_y r_y. In the second sum, swap x and y: = sum_{y<x} l_y l_x r_y = sum_{x<y} l_x l_y r_y... hmm let me just compute.

sum_{x<y} l_x l_y r_x = sum_x l_x r_x *