
## ideation
The core insight is already identified: answer for i = max divisor d of A_i with cnt[d] >= K. Key difficulties and details to nail down:

1. **Computing cnt[d] efficiently**: Build freq[v] = occurrences of value v (size M+1, M = max(A) ≤ 1e6). Then for d from 1..M, cnt[d] = sum of freq[m] over multiples m of d. This is O(M log M) ≈ 14M operations — fine in PyPy/C, but in Python needs care. Use array module or list of ints; the inner loop `for m in range(d, M+1, d): cnt[d] += freq[m]` totals ~M*H(M) ≈ 1e6 * 14 = 1.4e7 additions. In pure Python this is borderline (~2-4s) but usually acceptable; can micro-optimize with local variables and slicing tricks. Alternative: `cnt[d] = sum(freq[d::d])` using slice sums — slicing creates a copy but sum over a list slice is C-speed, likely faster. Actually `sum(freq[d::d])` allocates a slice each time (total memory churn O(M log M)); still probably faster than explicit loops. Test both mentally: explicit loop with local vars is safer memory-wise.

2. **Computing best[v] for all v**: For each value v, best[v] = largest d | v with cnt[d] >= K. Approach: iterate d from M down to 1; if cnt[d] >= K, then for every multiple m of d, if best[m] is unset (0), set best[m] = d. Since we go descending, first assignment is the max. Total work again O(M log M). But worst case: if cnt[d] >= K for all small d (e.g., all A_i equal), we still iterate all multiples for each qualifying d → 1.4e7 assignments, fine. However, we can stop early: once all values have best assigned? Hard to track cheaply; simpler to just run full loop. Optimization: only need best[v] for values v that appear in A. We could collect unique values and enumerate divisors per unique value — number of unique values ≤ 1e6, divisors each ~ up to 240 avg ~100; worst case 1e8 — too slow. Better: the descending-d marking approach but only mark multiples m where freq[m] > 0. Still same loop cost. Just do full marking; 1.4e7 operations is fine.

   Alternative cleaner method: best[v] via divisor enumeration only for distinct values present. Distinct values could be up to min(N, M) = 1e6. Enumerating divisors by trial up to sqrt per value: 1e6 * 1000 = 1e9 — too slow. So sieve marking is the way.

3. **Edge cases**:
   - K = 1: answer is A_i itself (cnt[A_i] >= 1 always). Handled naturally.
   - K = N: answer is gcd of all elements dividing A_i... actually max d | A_i with cnt[d] = N, i.e., d divides every element, so d | gcd(all). Handled naturally.
   - Duplicates: freq handles it.
   - M could be small even if N huge — arrays sized by M, fine.

4. **Pitfalls**:
   - Memory: freq, cnt, best each of size M+1 ints. Python lists of ints are ~28 bytes/int → 3 * 1e6 * 28 ≈ 84MB — risky. Use `array('i')` or `array('I')` (4 bytes) → 12MB total. Or use `sys.setrecursionlimit`... no. Use array module; note array element access is slower than list but memory-safe. Compromise: freq as list built from input (values ≤ 1e6), then convert? Actually list of 1e6+1 ints mostly small — CPython caches small ints (-5..256) but counts can exceed 256; still each distinct int object shared? No — list stores references; repeated values share objects only if interned. Counts up to 1.2e6 → many distinct int objects, ~36 bytes per entry. Three lists ≈ 108MB+. Use `array('I')` for all three to be safe (12MB), accepting somewhat slower access.
   - Speed of array indexing in tight loops: array('I') access is C-converted, reasonably fast. The double loop ~1.4e7 iterations with array ops should run ~3-6s in CPython. Might be tight. Alternative: use `list` for freq (input values, many repeats share int objects? No, each parsed int is a new object unless small). Hmm — reading 1.2e6 ints already costs memory; we can read all, build freq, then free the input list.
   - Actually a faster cnt trick: for d in range(1, M+1): cnt[d] = sum(freq[d::d]) — slice + sum in C. With array, slicing works too and sum over array is C-loop. This is likely the fastest pure-Python approach. Total sliced elements ≈ 1.4e7, sum in C ≈ fast (<1s). Memory churn acceptable.
   - For best marking: loop d descending, if cnt[d] >= K: for m in range(d, M+1, d): if best[m]==0: best[m]=d. This inner loop in Python is the bottleneck (~1.4e7 iterations worst case). Optimization: skip d if cnt[d] < K (check cheap). Worst case all A equal to value V: cnt[d] >= K only for d | V (few), so cheap. Bad case: A consists of K copies of highly composite... e.g., K small and many distinct values → cnt[d] >= K for many small d. E.g., uniform random values, K=2: cnt[1] = N >= 2, cnt[2] ≈ N/2, ... cnt[d] >= 2 for d up to ~M/2. So roughly half of d values qualify → ~7e6 assignments. OK.
   - Early termination: track number of unset values among those with freq>0? Simpler: since d=1 always qualifies if K <= N (cnt[1]=N), every v gets best at latest at d=1. We could stop when all present values assigned: maintain remaining = number of distinct values; when marking best[m]==0 and freq[m]>0, decrement; break when 0. Good speedup in practice.
   - I/O: read via sys.stdin.buffer.read().split(); output via '\n'.join.

5. **Verification with samples**: Sample 1: freq of {3,4,6,7,12}; cnt[3]=2 (3,6,12? 12%3=0 yes → 3), wait cnt[3] = freq[3]+freq[6]+freq[9]+freq[12] = 1+1+0+1 = 3 >= 2. best[3]: divisors of 3: 3 (cnt 3>=2) → 3 ✓. best[4]: 4: cnt[4]=freq[4]+freq[8]+freq[12]=2 → 4 ✓. best[7]: 7 cnt=1 <2, 1 cnt=5 → 1 ✓. best[12]: 12 cnt=1, 6 cnt=2 → 6 ✓. Matches.

## worker: Implement the complete solution: write solve() tha
- **Core fact**: For index i, the optimal choice is A_i plus any K-1 other elements all divisible by some divisor d of A_i. So answer = max d | A_i with cnt[d] >= K, where cnt[d] = #{j : d | A_j}.
- **cnt computation**: `sum(freq[d::d])` uses C-level slicing and summation; total work O(M log M) ≈ 1.4e7 element visits, fast.
- **best computation**: iterate d from M down to 1; the first (largest) qualifying d that divides v sets best[v]. Early termination when every value present in A has been assigned (d=1 always qualifies since cnt[1] = N >= K, so termination is guaranteed).
- **Memory**: three `array('I')` of size M+1 ≈ 12 MB total, safe.
- **Sample 1 trace**: cnt[3]=3, cnt[4]=2, cnt[6]=2, cnt[7]=1, cnt[12]=1. best[3]=3, best[4]=4, best[6]=6, best[7]=1, best[12]=6 → matches.
- **Sample 2**: K=3, only d=1 has cnt=3 → all answers 1 → matches.
- **Sample 3**: spot-check i=1: A_1=414003=3·7·19721... 414003/59=7017 → 59 | A_1; answer 59 means 59 divides A_1 and ≥3 multiples of 59 exist, and no larger divisor of A_1 qualifies. Consistent with expected output.
- **Edge cases**: K=1 → cnt[A_i] ≥ 1 so best[A_i] = A_i (correct: choose only A_i, gcd = A_i). K=N → only divisors of the global gcd qualify (correct). N=1, K=1 → answer A_1. Duplicates handled by freq.
