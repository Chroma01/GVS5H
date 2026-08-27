We need for each k in [0, M-1] the inversion count of B_i = (A_i + k) mod M. As k increases by 1, every element increases by 1 mod M. We can compute the answer for k=0 using a BIT (Fenwick tree) over values 0..M-1 in O((N+M) log M). Then we update for k → k+1 efficiently: the relative order between two values changes only when one of them wraps from M-1 to 0. For each value v, let cnt[v] be its frequency in A. When k increments, the elements equal to M-1 become 0, and all other values v become v+1. This reduces inversions where the left element was > right element because of M-1>0, etc. A standard O(M) transition per k would be too slow, but we can precompute contributions for each k in O(M) total using prefix sums of frequencies and the number of pairs (i<j) where A_i > A_j, etc. Actually, the known solution is: answer[k+1] = answer[k] - (number of pairs (i<j) with A_i > A_j and A_i != M-1 and A_j != M-1? Wait, need to derive carefully. Simpler: For each k, define B_i^k = (A_i + k) mod M. The inversion count at k is: total pairs (i,j) i<j where B_i^k > B_j^k. As k increases by 1, for any pair not involving a wrap (i.e., neither A_i nor A_j is M-1), their order stays same. For pairs where exactly one is M-1, the order flips. For pairs where both are M-1, they remain equal (no inversion). More precisely, when k increases, elements with A_i = M-1 become smaller (0) relative to others. So inversions where A_i = M-1 > A_j (with A_j != M-1) are lost, and inversions where A_i != M-1 > A_j = M-1 are gained. The change is: delta = (number of pairs i<j with A_i != M-1 and A_j = M-1) - (number of pairs i<j with A_i = M-1 and A_j != M-1). This can be computed using prefix counts. Doing this per k requires recomputation; but the values of A_i are fixed, so the delta is the same for all k! Wait, is that true? Let's check sample 1: A=(2,1,0), M=3. For k=0, inv=3. For k=1, inv=1, delta=-2. For k=2, inv=1, delta=0. So delta changed. Why? Because the condition depends on the "current values" after adding k mod M, not the original A. The pairs where exactly one is M-1 after adding k correspond to A_i = (M-1 - k) mod M, not just M-1. So the delta is a function of k. Specifically, for each k, the wrapped value is w = (M-1 - k) mod M. Elements equal to w become 0 after addition, others become v+1. So the delta at step k depends on the position of w in the sorted order. We can precompute for each possible value x (0..M-1) the contribution of "when w = x" i.e., when (M-1 - k) mod M = x, meaning k = (M-1 - x) mod M. So we can compute an array add[x] = change in inversion count when w=x. Then ans[k] for k from 0 to M-1 is ans[0] + cumulative sum of add[wrapped values] in order of increasing k. Since k increments, w = (M-1 - k) mod M goes M-1, M-2, ..., 0. So we can iterate k from 0 to M-1, compute w, add precomputed delta[w] to running answer, and output. We just need to compute delta[x] for all x.

Computing delta[x]: When w = x, the elements A_i = x become 0, others become (A_i+1) mod M? Wait, B_i = (A_i + k) mod M. With k such that x = (M-1 - k) mod M, i.e., k = (M-1 - x) mod M. Then for elements with A_i = x, B_i = (x + k) mod M = 0. For other elements, B_i = (A_i + k) mod M which is (A_i + (M-1-x)) mod M = (A_i - x - 1) mod M? Actually A_i + k = A_i + M-1-x. Mod M, that's A_i - x - 1 (if A_i >= x+1) or A_i + M - 1 - x (if A_i <= x). But perhaps easier: The relative order between two values a,b (after adding k) is (a+k)%M > (b+k)%M. This is equivalent to a > b unless one of them wraps. More systematically, we can use the known technique: For each k, inv(k) = total pairs i<j - (number of pairs where B_i <= B_j). But the standard solution for this problem (often called "Inversion Sum" or AtCoder ABC 107 D? No, this is AtCoder ABC 154 F? Wait, actually this is AtCoder ABC 107 D? No, it's AtCoder ABC 154 F? Let me recall: There's a known problem "Inversion Sum" from AtCoder ABC 154 F? No, that's different. This is "Inversion Sum" from AtCoder Beginner Contest 107 D? Let me think: Actually this is AtCoder ABC 107 D? No, I remember a problem "Inversion Sum" from AtCoder ABC 154? Wait, I recall a problem: "Inversion Sum" from AtCoder Regular Contest 088? No. Actually this is AtCoder Beginner Contest 154 F? No, F is "Many Many Paths". This problem is AtCoder ABC 154? Wait, I know: It's AtCoder Beginner Contest 154? No. Let me search memory: The problem "Inversion Sum" is from AtCoder Beginner Contest 107 D? No. Actually, it's from AtCoder Beginner Contest 154? No, that's "I hate Shortest Path Problem". Wait, I know the problem: It's "Inversion Sum" from AtCoder Beginner Contest 107? No. Let me recall: AtCoder ABC 107 D is "Median of Medians". Not that. There's a problem "Inversion Sum" which is exactly this. It's from AtCoder Beginner Contest 154? No. Wait, I think it's from AtCoder Beginner Contest 107? No. Let me just recall the solution: The known solution computes answer[0] with BIT, then for each k from 1 to M-1, answer[k] = answer[k-1] + (something). The something is precomputed as: For each x from 0 to M-2, we compute the number of pairs (i,j) with A_i = x and A_j > x? Actually, the known recurrence: Let C be the frequency array. For each k, let t = (k) mod M. The change from k-1 to k is: we add 1 to all elements except those that become 0. Wait, the known approach: When we increase k by 1, elements with value v become v+1, except those that were M-1 become 0. The inversion count changes by: - (number of elements with value M-1) * (number of elements with value less than M-1 that appear after them) + (number of elements with value not M-1) * (number of elements with value M-1 that appear after them). But these counts depend on positions. However, we can compute for each value v, the number of pairs (i<j) where A_i = v and A_j > v, and where A_i > v and A_j = v. Actually, the known solution uses a different perspective: The answer for k is sum over all pairs (i,j) of indicator( (A_i+k)%M > (A_j+k)%M ). This can be expressed in terms of original A. For a fixed pair (i,j), as k varies, the indicator changes only when k crosses M - A_i or M - A_j. Specifically, (A_i+k)%M > (A_j+k)%M is equivalent to (A_i - A_j) mod M < something? Let's analyze: For two values a,b, we want to know for how many k in [0, M-1] is (a+k)%M > (b+k)%M. This is a known combinatorial fact: It's exactly floor((M - (a-b) mod M - 1) / ... )? Actually, consider the sequence of k. The condition (a+k) mod M > (b+k) mod M is equivalent to k mod M in some interval. Since both increase by 1, they stay in same relative order except when one wraps. The difference (a+k)%M - (b+k)%M = (a-b) mod M. Wait, that's constant! Because (a+k) mod M - (b+k) mod M is not constant; it's either a-b or a-b+M depending on wrap. Actually, (a+k) mod M = a+k if a+k < M, else a+k-M. So the relative order flips when exactly one wraps. For a fixed pair (a,b) with a != b, there is exactly one k in [0, M-1] where a+k >= M and b+k < M (if a > b), or vice versa. Specifically, if a > b, then for k from 0 to M-1-a, both are < M, order is a+k > b+k, so 1. For k from M-a to M-1-b, a wraps but b doesn't, so a+k-M < b+k, so 0. For k from M-b to M-1, both wrap, order is a+k-M > b+k-M, so 1. So the indicator is 1 for all k except the interval where exactly one wraps. That interval length is (M-1-b) - (M-a) + 1 = a - b. Wait, if a > b, then a - b > 0. So for a > b, the indicator is 0 for k in [M-a, M-b-1], which has length a - b. So the sum over k of indicator is M - (a - b) = M - (a - b). But we need the sum over k of the indicator for each k, not the sum over k. Wait, we need the value for each k, not the sum. But we can compute the answer for k=0 and then update. The update from k to k+1: the only pairs that change are those where one of the values is M-1 - k (mod M) and the other is not. As derived earlier, the delta is precomputable for each possible wrapped value. Since the wrapped value cycles through all M values exactly once as k goes 0..M-1, we can precompute delta[x] for all x, and then ans[k] = ans[0] + sum_{i=0}^{k-1} delta[(M-1 - i) mod M]. Since (M-1 - i) mod M as i increases goes M-1, M-2, ..., 0, we can just compute ans[0], then for k from 1 to M-1, ans[k] = ans[k-1] + delta[(M-1 - (k-1)) mod M] = ans[k-1] + delta[(M - k) mod M]. So we need delta for all values v from 0 to M-1. How to compute delta[v]? delta[v] is the change in inversion count when the wrapped value is v, i.e., when k is such that v = (M-1 - k) mod M. At that k, elements equal to v become 0, others become (A_i+1) mod M. So the change in inversion count is: (number of inversions lost) - (number of inversions gained). Inversions lost: pairs (i<j) where A_i = v and A_j > v (since v becomes 0, which is smaller than any positive value; but careful: other values become (A_j+1) mod M. If A_j = v, it also becomes 0, so order between two v's stays equal. If A_j != v, it becomes (A_j+1) mod M, which is in 1..M-1. So v (0) is less than all these, so all pairs with i<j, A_i = v, A_j != v are no longer inversions if they were before. But they were inversions only if v > A_j in the original? Wait, at step k, the values are B_i = (A_i + k) mod M. At the step where v wraps, we are comparing answer for k and k+1? Actually, the transition from k to k+1: at k, wrapped value is w = (M-1 - k) mod M. At k+1, wrapped value is w' = (M-1 - (k+1)) mod M = (w - 1) mod M. But the problem asks for each k independently. So we can think of the sequence of answers for k=0,1,...,M-1. The recurrence is ans[k+1] = ans[k] + delta[(M-1 - k) mod M]. So delta[v] is the change in answer when moving from the state where the wrapped value is v+1? Let's define carefully. Let f(k) be answer for k. We want f(0), then f(1) = f(0) + change, etc. The change from k to k+1: at k, the values are (A_i + k) mod M. At k+1, they are (A_i + k + 1) mod M. For a given k, let w = (M - 1 - k) mod M? Actually, at k, the elements that are M-1 are those with A_i + k ≡ M-1 mod M, i.e., A_i ≡ M-1 - k mod M. Let x = (M-1 - k) mod M. Then elements with A_i = x are M-1 at step k. When we go to k+1, those elements become 0, and all others become v+1. So the change in inversion count from step k to step k+1 is determined by x. So delta[x] = f(k+1) - f(k) where x = (M-1 - k) mod M. So we need to compute delta[x] for all x. Now, how to compute delta[x] efficiently for all x? The change is: f(k+1) - f(k) = (number of pairs (i,j) with i<j such that at step k+1, B_i > B_j but at step k, B_i <= B_j) minus (number of pairs where at step k, B_i > B_j but at step k+1, B_i <= B_j). Since only elements with A_i = x change their relative position drastically: they go from M-1 to 0. All other elements increase by 1, preserving their relative order. So the only pairs whose order can change are those involving at least one element with A_i = x. Pairs where both have A_i = x: they both go from M-1 to 0, so they remain equal, no change. Pairs where exactly one has A_i = x: the one with A_i = x was M-1, the other was v != M-1. At step k, the order was: if v < M-1, then M-1 > v, so inversion exists if the x-element is before the v-element. At step k+1, the x-element becomes 0, and the v-element becomes v+1 (mod M). Since v != M-1, v+1 is in 1..M-1. So 0 < v+1, so the x-element is smaller. Thus the inversion is lost if the x-element was before the v-element, and gained if the x-element was after the v-element. So the net change is: (number of pairs i<j with A_i = x, A_j != x) - (number of pairs i<j with A_i != x, A_j = x). Wait: If x-element is before, it was an inversion (M-1 > v), now it's not, so we lose an inversion: change -1. If x-element is after, it was not an inversion (v > M-1? No, v < M-1, so v < M-1, so not inversion), now it is: 0 < v+1, so it becomes an inversion, so we gain an inversion: change +1. So net change = (number of x-elements after non-x elements) - (number of x-elements before non-x elements). But that is exactly: (number of pairs (i,j) with A_i != x, A_j = x) - (number of pairs (i,j) with A_i = x, A_j != x). Let S = total number of elements with A_i = x. Let L be the number of non-x elements before each x-element. The number of pairs with A_i = x, A_j != x, i<j is sum over x-elements of (number of non-x elements after them). Actually, for each x-element, count non-x elements after it. Summing over all x-elements gives total pairs (i<j) with i=x, j!=x. And pairs with i!=x, j=x is sum over x-elements of (number of non-x elements before it). So delta[x] = (sum over x-elements of (# non-x before)) - (sum over x-elements of (# non-x after)). Since total non-x elements = N - S, the sum of non-x before and non-x after for each x-element sums to N - S. So delta[x] = (total non-x before all x-elements) - (total non-x after all x-elements) = 2*(total non-x before all x-elements) - S*(N - S). So we need for each x, the number of non-x elements that appear before the x-elements. This is a function of the positions. But we can precompute for each x: the number of pairs (i<j) with A_i != x and A_j = x. Let's denote P[x] = number of pairs (i,j) with i<j, A_i != x, A_j = x. And Q[x] = number of pairs (i<j) with A_i = x, A_j != x. Then delta[x] = P[x] - Q[x]. But note that P[x] + Q[x] = S * (N - S) because for each pair of one x and one non-x, exactly one ordering exists. So delta[x] = 2*P[x] - S*(N - S). So if we can compute P[x] for all x, we can compute delta[x]. How to compute P[x] efficiently? P[x] is the number of pairs (i<j) where A_i != x and A_j = x. This is equivalent to: for each position j where A_j = x, count the number of i < j with A_i != x. That is: (j-1) - (number of i < j with A_i = x). Summing over j with A_j = x: P[x] = sum_{j: A_j=x} [ (j-1) - count_x_before(j) ]. This can be computed if we know for each x, the sum of positions of x and the number of x before each. But we can also compute it using a BIT over the array: traverse from left to right, maintain a BIT of counts of values seen. For each x, we want total pairs where left is not x and right is x. That is: for each j with A_j=x, we want (j-1) - (number of x before j). This is: total pairs with i<j and A_i anything, minus pairs with i<j and A_i=x. Total pairs with i<j is just j-1. So P[x] = sum_{j: A_j=x} (j-1) - sum_{j: A_j=x} (number of x before j). The second sum is the number of pairs (i<j) with A_i=x and A_j=x. That is C(S,2) for each x, but careful: the sum over j of (number of x before j) counts for each pair of x's, the second one counts the first, so it's exactly C(S,2). So sum_{j: A_j=x} (number of x before j) = S*(S-1)/2. Therefore P[x] = sum_{j: A_j=x} (j-1) - S*(S-1)/2. So if we know for each x the sum of indices (1-based) of positions where A_i = x, we can compute P[x]. Let pos_sum[x] = sum of indices i where A_i = x. Then P[x] = pos_sum[x] - S - S*(S-1)/2? Wait: sum_{j: A_j=x} (j-1) = pos_sum[x] - S. So P[x] = pos_sum[x] - S - S*(S-1)/2. That is easy! So we can compute pos_sum and S in one pass. Then for each x, we have P[x]. Then Q[x] = S*(N-S) - P[x]. So delta[x] = P[x] - Q[x] = 2*P[x] - S*(N-S). We can precompute delta for all x. Then we compute ans[0] using a BIT over values (not positions) because inversion count at k=0 is based on values A_i. We can compute ans[0] = number of pairs i<j with A_i > A_j. This is standard: sort values, use BIT or just frequency array. Since M <= 2e5, we can use a BIT over frequencies. Then we iterate k from 0 to M-1: we have ans[0]. For k from 1 to M-1: the wrapped value at previous step was x = (M - k) mod M? Wait, we need to map: delta[x] is the change from step k-1 to step k, where x = (M-1 - (k-1)) mod M = (M - k) mod M. So for k >= 1, ans[k] = ans[k-1] + delta[(M - k) mod M]. We can precompute an array D[0..M-1] where D[x] = delta[x]. Then we just do: cur = ans0; for k in range(1, M): cur += D[(M - k) % M]; ans[k] = cur. Or we can just compute the list of wrapped values in order: w_0 = (M-1 - 0) mod M = M-1? Wait, for k=0 to 1, the wrapped value is x = (M-1 - 0) mod M = M-1. So the first delta to add is D[M-1]. For k=1 to 2, x = (M-1 - 1) mod M = M-2, so add D[M-2]. So the order of indices added is M-1, M-2, ..., 0. So we can iterate k from 0 to M-1, output ans[k], and for next k, add D[(M-1 - k) mod M]. Let's test with sample 1: N=3, M=3, A=(2,1,0). Compute S[0]=1, S[1]=1, S[2]=1. pos_sum[0]=3 (index 3), pos_sum[1]=2, pos_sum[2]=1. For x=0: S=1, P = pos_sum - S - S*(S-1)/2 = 3 - 1 - 0 = 2. Then Q = S*(N-S) - P = 1*2 - 2 = 0. delta = P - Q = 2. For x=1: S=1, P = 2 - 1 = 1. Q = 2 - 1 = 1. delta = 0. For x=2: S=1, P = 1 - 1 = 0. Q = 2 - 0 = 2. delta = -2. Now ans0: inversions in (2,1,0): 2>1, 2>0, 1>0 => 3. Now iterate k: start with ans0=3. For k=1: wrapped value from k=0 to 1 is x = (M-1 - 0) mod 3 = 2. So add D[2] = -2 => ans1 = 1. For k=2: wrapped value from k=1 to 2 is x = (M-1 - 1) mod 3 = 1. So add D[1] = 0 => ans2 = 1. Matches sample output! Good.

Test sample 2: N=5, M=6, A=(5,3,5,0,1). Compute S: 0:1, 1:1, 3:1, 5:2. pos_sum: 0:4, 1:5, 3:2, 5:1+3=4. For x=0: S=1, P = 4 - 1 - 0 = 3. Q = 1*4 - 3 = 1. delta = 2. x=1: S=1, P = 5-1=4. Q = 4-4=0. delta=4. x=3: S=1, P=2-1=1. Q=4-1=3. delta=-2. x=5: S=2, P=4 - 2 - 1 = 1. (S*(S-1)/2 = 1). Q = 2*3 - 1 = 5. delta = 1 - 5 = -4. Now ans0: inversions in A. A = (5,3,5,0,1). Pairs: (5,3): inv, (5,5): no, (5,0): inv, (5,1): inv, (3,5): no (3<5), (3,5): no, (3,0): inv, (3,1): inv, (5,0): inv, (5,1): inv. Total: 1+0+1+1+0+0+1+1+1+1 = 7. Matches sample. Now D[0]=2, D[1]=4, D[2]=0, D[3]=-2, D[4]=0, D[5]=-4. Iterate: start 7. k=1: add D[5] = -4 => 3. k=2: add D[4] = 0 => 3. k=3: add D[3] = -2 => 1. k=4: add D[2] = 0 => 1. k=5: add D[1] = 4 => 5. Matches sample! Good.

Test sample 3: N=7, M=7, A=(0,1,2,3,4,5,6). S: all 1. pos_sum[i] = i+1. For each x: S=1, P = (x+1) - 1 - 0 = x. Q = 6 - x. delta = 2x - 6. So D[0]=-6, D[1]=-4, D[2]=-2, D[3]=0, D[4]=2, D[5]=4, D[6]=6. ans0: inversions in (0,1,2,3,4,5,6) = 0. k=1: add D[6]=6 => 6. k=2: add D[5]=4 => 10. k=3: add D[4]=2 => 12. k=4: add D[3]=0 => 12. k=5: add D[2]=-2 => 10. k=6: add D[1]=-4 => 6. Matches sample.

So the algorithm is:
1. Read N, M, array A.
2. Compute frequency S[x] for x in 0..M-1, and pos_sum[x] (sum of 1-based indices).
3. For each x, compute P[x] = pos_sum[x] - S[x] - S[x]*(S[x]-1)//2. (If S[x]=0, P[x]=0).
4. Compute Q[x] = S[x]*(N - S[x]) - P[x].
5. Compute D[x] = P[x] - Q[x] = 2*P[x] - S[x]*(N - S[x]).
6. Compute ans0: number of inversions in A. Use a BIT of size M. Iterate i from 0 to N-1: query sum of values < A[i] (i.e., number of previous elements > A[i]? Actually inversion: i<j and A_i > A_j. We can iterate left to right: for each A[i], count how many previous elements are > A[i]. Using BIT, we can add A[i] to BIT, and query sum of (A[i]+1 to M-1). Or we can query sum of all - sum of <= A[i]. So ans0 = sum_{i} (i - prefix_sum(A[i])). After adding, we update BIT at A[i] with +1.
7. Now we have ans[0] = ans0.
8. For k from 1 to M-1:
   idx = (M - k) % M   (since we want x = (M-1 - (k-1)) mod M = (M - k) mod M)
   ans0 += D[idx]
   store ans0 as ans[k]
9. Print all ans.

Wait, careful with the order of indices. In the loop, for k=1, we want x = (M-1 - 0) = M-1. So idx = M-1. For k=2, x = (M-1 - 1) = M-2. So idx = M-2. In general, for k from 1 to M-1, idx = M-1 - (k-1) = M - k. So we can precompute an array of indices in that order: [M-1, M-2, ..., 0]. Then for k in range(1, M): ans.append(ans[-1] + D[order[k-1]]). Or we can just do: for k in range(1, M): ans.append(ans[-1] + D[(M - k) % M]).

Let's verify with M=3, k=1: (3-1)%3=2, D[2] correct. k=2: (3-2)%3=1, D[1] correct. For M=6, k=1: (6-1)%6=5, D[5] correct. k=2: (6-2)%6=4, D[4] correct. k=3: (6-3)%6=3, D[3] correct. k=4: (6-4)%6=2, D[2] correct. k=5: (6-5)%6=1, D[1] correct. Perfect.

Edge cases: S[x]=0. Then P[x]=0 (pos_sum=0, so P=0-0-0=0). Q[x]=0. D[x]=0. Works.

Complexities: O(N + M log M). N, M up to 2e5, fine.

We need to implement this in Python. The BIT can be a list of size M+1. The sum of positions can be up to N * M? N up to 2e5, M up to 2e5, product up to 4e10, fits in 64-bit integer (Python int is arbitrary, so fine). Answer can be up to N*(N-1)/2 ~ 2e5^2/2 = 2e10, fits.

Now, the problem asks to enclose code within delimiters. The user instruction: "Enclose your code within delimiters as follows. Ensure that when the python program runs, it reads the inputs, runs the algorithm and writes output to STDOUT." The sample format in the problem statement shows no specific delimiters, but the user says "Enclose your code within delimiters as follows." and "Ensure that when the python program runs...". Probably they want a code block. I'll provide a standard Python solution.

Let's write the code.

```python
import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = list(map(int, input().split()))
    
    # Frequency and position sum
    S = [0] * M
    pos_sum = [0] * M
    for idx, val in enumerate(A, 1):  # 1-based index
        S[val] += 1
        pos_sum[val] += idx
    
    # Precompute D[x] = delta[x]
    D = [0] * M
    for x in range(M):
        sx = S[x]
        if sx == 0:
            continue
        # P[x] = pos_sum[x] - sx - sx*(sx-1)//2
        P = pos_sum[x] - sx - sx * (sx - 1) // 2
        total_pairs = sx * (N - sx)
        Q = total_pairs - P
        D[x] = P - Q  # = 2*P - total_pairs
    
    # Compute ans0 using BIT
    size = M + 2
    bit = [0] * size
    def bit_add(i, v):
        i += 1  # 0-indexed to 1-indexed
        while i < size:
            bit[i] += v
            i += i & -i
    def bit_sum(i):
        # sum of [0, i]
        i += 1
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s
    
    inv0 = 0
    for val in A:
        # number of previous elements > val
        # total seen - number of previous elements <= val
        seen = bit_sum(M - 1)
        le = bit_sum(val)
        inv0 += seen - le
        bit_add(val, 1)
    
    ans = [inv0]
    cur = inv0
    for k in range(1, M):
        idx = (M - k) % M
        cur += D[idx]
        ans.append(cur)
    
    sys.stdout.write('\n'.join(map(str, ans)) + '\n')

if __name__ == "__main__":
    solve()
```

Check with sample 1: N=3, M=3, A=[2,1,0].
S: [1,1,1]
pos_sum: [3,2,1]
x=0: sx=1, P=3-1-0=2, total=2, Q=0, D=2.
x=1: sx=1, P=2-1=1, total=2, Q=1, D=0.
x=2: sx=1, P=1-1=0, total=2, Q=2, D=-2.
inv0: process 2: seen=0, le=0, inv+=0; add 2. seen=1, le=1? Actually bit_sum(M-1) returns total seen. For 2: seen=0? Wait, we process sequentially. Let's trace:
A=[2,1,0]
val=2: seen = bit_sum(2) = 0 (bit is empty). le = bit_sum(2) = 0. inv0 += 0. bit_add(2).
val=1: seen = bit_sum(2) = 1. le = bit_sum(1) = 0. inv0 += 1. bit_add(1).
val=0: seen = bit_sum(2) = 2. le = bit_sum(0) = 0. inv0 += 2. bit_add(0).
Total inv0=3. Correct.
ans[0]=3.
k=1: idx=(3-1)%3=2, D[2]=-2 => cur=1.
k=2: idx=(3-2)%3=1, D[1]=0 => cur=1.
Output: 3,1,1. Correct.

Sample 2: N=5, M=6, A=[5,3,5,0,1].
S: 0:1,1:1,2:0,3:1,4:0,5:2.
pos_sum: 0:4,1:5,3:2,5:1+3=4.
x=0: sx=1, P=4-1-0=3, total=1*4=4, Q=1, D=2.
x=1: sx=1, P=5-1=4, total=4, Q=0, D=4.
x=3: sx=1, P=2-1=1, total=4, Q=3, D=-2.
x=5: sx=2, P=4-2-1=1, total=2*3=6, Q=5, D=-4.
inv0: compute using BIT.
val=5: seen=0, le=0, inv+=0; add 5.
val=3: seen=1, le=1? bit_sum(3): bit has 5 at index 5. bit_sum(3) sums up to 3: 0. So le=0, seen=1, inv+=1. add 3.
val=5: seen=2, le=bit_sum(5)=2? bit has 5,3. bit_sum(5) counts both? Actually bit_sum(5) = 1 (at 5) + 1 (at 3) = 2. Wait, bit_sum(5) should return sum of counts for indices <=5. But 3 <=5, so it includes 3. So le=2. seen=2. inv+=0. add 5.
val=0: seen=3, le=bit_sum(0)=0. inv+=3. add 0.
val=1: seen=4, le=bit_sum(1)=1 (only 0). inv+=3. add 1.
Total inv0 = 0+1+0+3+3 = 7. Correct.
ans: [7]
k=1: idx=5, D[5]=-4 => 3.
k=2: idx=4, D[4]=0 => 3.
k=3: idx=3, D[3]=-2 => 1.
k=4: idx=2, D[2]=0 => 1.
k=5: idx=1, D[1]=4 => 5.
Output: 7,3,3,1,1,5. Correct.

Sample 3: N=7, M=7, A=[0,1,2,3,4,5,6].
S: all 1.
pos_sum: 1,2,3,4,5,6,7.
x=0: P=1-1=0, total=6, D=-6.
x=1: P=2-1=1, total=6, D=2*1-6=-4.
x=2: P=3-1=2, D=4-6=-2.
x=3: P=4-1=3, D=6-6=0.
x=4: P=5-1=4, D=8-6=2.
x=5: P=6-1=5, D=10-6=4.
x=6: P=7-1=6, D=12-6=6.
inv0: 0.
k=1: idx=6, D[6]=6 => 6.
k=2: idx=5, D[5]=4 => 10.
k=3: idx=4, D[4]=2 => 12.
k=4: idx=3, D[3]=0 => 12.
k=5: idx=2, D[2]=-2 => 10.
k=6: idx=1, D[1]=-4 => 6.
Output: 0,6,10,12,12,10,6. Correct.

The code seems correct.

One thing: In the BIT, bit_sum(M-1) is total seen. But we don't actually need seen, we can just query the number of elements strictly greater than val: total_seen - bit_sum(val). But we can also just use bit_sum(val) and subtract from something. Since we need total seen, we can maintain a variable 'seen' incremented each iteration. That's simpler and avoids extra BIT query. Let's do that for efficiency.

Modify inv0 calculation:
seen = 0
for val in A:
    le = bit_sum(val)
    inv0 += seen - le
    bit_add(val, 1)
    seen += 1

That's cleaner.

Also, note that M can be up to 2e5, BIT size M+2 is fine.

Potential overflow? Python int handles big numbers, so no issue.

Time complexity: O(N log M + M). N, M up to 2e5, log M ~ 18, so about 3.6 million operations, very fast.

Thus the plan is solid. I will now write the final response.</mm:think>### PLAN
We need the inversion count of B_i = (A_i + k) mod M for each k = 0..M-1. For k=0, compute the standard inversion count with a Fenwick tree (BIT) in O(N log M). For k → k+1, only elements equal to x = (M-1 - k) mod M wrap from M-1 to 0; all other values increase by 1, preserving their relative order. The change in inversion count is delta[x] = (pairs with non-x before x) - (pairs with x before non-x). This can be precomputed for every x in O(N + M) using frequency S[x] and the sum of positions pos_sum[x] of each value. Then we build D[x] = delta[x] and accumulate answers: ans[0] from BIT, and for k≥1, ans[k] = ans[k-1] + D[(M - k) mod M]. Overall complexity O((N+M) log M).