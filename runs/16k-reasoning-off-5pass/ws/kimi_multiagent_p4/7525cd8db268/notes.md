
## ideation
- Core model: nums = [1..n] in order, so each conflicting pair (a,b) can be normalized to a<b. A subarray is invalid iff it contains both endpoints of any remaining pair.
- For fixed pairs, validity by right endpoint r: subarray [l,r] is invalid iff l <= max(a among pairs (a,r)). Let L[r] = max a (0 if none). Then number of valid subarrays ending at r is r - L[r]. Base answer = sum_r (r - L[r]).
- Removing exactly one pair (a,b) only changes L[b]. If a == L[b] and it is the unique max, L[b] becomes secondMax[b] (or 0); otherwise no change. Gain for b = L[b] - secondMax[b], but only if at least one removed pair attains the max at b. Since we must remove exactly one pair, we can always choose a max-attaining pair for some b; gain depends only on b, so take max gain over all b.
- Answer = base + max_b (L[b] - secondMax[b]).
- Pitfalls:
  - Normalize each pair to (min,max).
  - Need top two values per right endpoint b, not counts, because removing any one max pair lowers L[b] to second max even if duplicates existed? Duplicates of same pair are not explicitly forbidden; if duplicate identical pairs exist, removing one still leaves another identical conflict, so L[b] unchanged. To handle duplicates robustly, track count of max too; gain is 0 unless countMax==1. Constraints don't state uniqueness, so include count.
  - Use 1-indexed arrays length n+1.
  - Complexity O(n + m).

## worker: Implement the solution: normalize pairs, track per
- Normalized each pair to (a, b) with a < b since nums is [1..n] in order; a subarray contains both endpoints iff l <= a and r >= b.
- For fixed pairs, with L[b] = max a over pairs ending at b (0 if none), valid subarrays ending at b number b - L[b]; base = sum over b.
- Removing pair (a, b) only affects L[b]: it drops to the second max only if a is the unique maximum at b (cntMax[b] == 1, guarding against duplicate identical pairs). Gain for b is max1[b] - max2[b]; answer = base + max gain.
- Verified: Example 1 → pairs (2,3),(1,4): L[3]=2, L[4]=1; base = (1-0)+(2-0)+(3-2)+(4-1)=7; gains: b=3 → 2, b=4 → 1; answer 9. Example 2 → pairs (1,2),(2,5),(3,5): L[2]=1, L[5]=3 (max2=2); base = 1+1+3+4+2=11; gains: b=2 → 1, b=5 → 1; answer 12.
- Complexity O(n + m) time, O(n) space.
