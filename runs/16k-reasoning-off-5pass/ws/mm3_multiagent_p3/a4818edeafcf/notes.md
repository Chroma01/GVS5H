
## ideation
The problem asks to split the array into three non-empty contiguous parts and maximize the sum of distinct counts. Standard trick: precompute `left[i]` = distinct in prefix 1..i, and `right[k]` = distinct in suffix k..N. Then iterate over the right end of the middle subarray `r` from 2 to N-1. Maintain `best_left = max(left[1..r-1])` (since middle starts after some i < r). Also maintain a running count of distinct elements in the current middle subarray A[start..r] where start is fixed at 2 initially and we can expand leftwards? Wait, to consider all middle subarrays ending at r, we need all possible starts s where 1 < s ≤ r. That would be O(N^2). The standard approach instead iterates over the *left end* of the middle subarray? Let's rethink.

Actually, the known approach for this problem (AtCoder ABC 217 E? No, this is similar to "Three Subarrays" or "ABC 098 D"? It's exactly the problem "Split into Three Subarrays" from a recent contest). The standard solution is: for each index `r` (the end of the middle subarray), we want to maximize `left[i] + distinct(A[i+1..r]) + right[r+1]` over `i < r`. This is O(N^2) if done naively. But we can do it in O(N) using the fact that as we increase `r` by 1, the set of valid `i` for the middle subarray is `1..r-1`. However, the distinct count for A[i+1..r] depends on `i`. This seems hard.

Wait, the classic solution uses a two-pointer technique: as we move the left end of the middle subarray, we maintain a set for the middle. Actually, the problem is: for each split (i, j), middle is A[i+1..j]. We can iterate `i` from 1 to N-2, and for each `i`, we expand `j` from i+1 to N-1, but we need to maintain distinct count and also `right[j+1]`. But `right[j+1]` is non-increasing? No, `right[k]` is distinct count in suffix, which can vary.

Let me recall the known solution: 
- Compute `left[i]` for all i.
- Compute `right[i]` for all i.
- Then for each `i` from 1 to N-2, we can use a set for the middle, and we expand `j` from i+1 to N-1. As we expand, we add elements to a set, and for each `j`, candidate = `left[i] + size(set) + right[j+1]`. The maximum over `j` for this `i`. But this is O(N^2).

The actual trick: We can iterate over the *start* of the middle subarray (or the *end*). There's a known solution: For each `j` (end of middle), we want to find the best `i < j` that maximizes `left[i] + distinct(i+1..j)`. This is not easily separable.

Alternative view: The problem is equivalent to finding max over i<j of left[i] + right[j+1] + distinct(i+1..j). We can process from left to right, maintaining a multiset of elements in the middle as we move the left boundary. Actually, we can iterate over the left boundary `i` of the middle subarray? No.

Another approach: The problem can be solved in O(N) using a "two pointers" or "sliding window" on the middle subarray, but with careful data structures. Wait, I recall a problem: "Split into three subarrays, maximize sum of distinct counts" from AtCoder. The solution: 
- Precompute `right[k]`.
- For each `i` (the end of the first part, i.e., the split point after the first subarray), we want to find the best second split `j > i`. For a fixed `i`, as `j` increases, the distinct count in the middle (A[i+1..j]) increases by 1 for each new element, but never decreases. Also, `right[j+1]` is a known array. So for fixed `i`, the function `f(j) = left[i] + distinct(i+1..j) + right[j+1]` is the sum of a non-decreasing function and `right[j+1]`. We need the max over `j` from i+1 to N-1. But doing this for each `i` is O(N^2).

The actual known solution: iterate over `i` (the end of the first subarray) from 1 to N-2, and use a set for the middle. But we need to bound the total work. The trick is that the middle subarray's distinct count can be updated efficiently if we use two pointers? No.

Let me search memory: This is "ABC 217 E" or similar? Actually it's "ABC 098 D"? No. It's "AtCoder Regular Contest 108 C"? No.

I remember a problem: "Three Subarrays" (hard version) from Codeforces? Or AtCoder "Three Subarrays" (ARC something). The constraints: N up to 3e5, A_i up to N. The solution: 
- Compute `right[]`.
- Then iterate `i` from 1 to N-2, and for each `i`, we consider `j` from i+1 to N-1. But we maintain a sliding window? Actually, we can iterate `i` from N-2 down to 1, and maintain a set for the middle subarray that expands to the right as we decrease `i`? Let's think.

Let `i` be the split point after the first subarray. The middle subarray starts at i+1. We want to find the best `j` (i < j < N). For a fixed start s = i+1, we expand j to the right. As j increases, the middle distinct count increases, and `right[j+1]` is known. The max over j for this start s is `max_{e >= s} (distinct(s..e) + right[e+1])`. Then the answer is `max_s (left[s-1] + max_{e >= s} (distinct(s..e) + right[e+1]))`. 

Now, we can compute `M[s] = max_{e >= s} (distinct(s..e) + right[e+1])` for all s. How to compute M efficiently? We can process s from N down to 1. When we move s one step left (i.e., s decreases by 1), we add a new element A[s] to the middle. The set for the middle now contains A[s..e] for varying e. But we need to consider all e >= s. This seems like we need to maintain a data structure over e. 

Alternatively, process from left to right: maintain a pointer `j` that moves right, and a set for the middle. But we need to consider all splits (i, j). There's a known solution: 
- For each i (end of first subarray), we consider j from i+1 to N-1, but we can use a "freq" array and maintain the distinct count. The total number of operations if we use a freq array and for each i we iterate j from i+1 to N-1? That's O(N^2).

Wait, the problem is exactly the same as the one in AtCoder "ABC 217 G" or similar? No. It's from a recent contest: "ABC 277 F?" No.

Let me derive the O(N) solution:
- Precompute `right[k]` = distinct in A[k..N].
- We want to compute for each possible middle subarray (L, R) with L ≤ R, the value `left[L-1] + distinct(L..R) + right[R+1]`. We need the maximum over all L, R with 1 < L ≤ R < N? Actually L = i+1, R = j, with i < j, so 1 ≤ L-1 < R < N, so L ≥ 2, R ≤ N-1, and L ≤ R.
- We can iterate over L from 2 to N-1. For each L, we want to find the best R ≥ L. We can maintain a sliding window? But R can go up to N-1. If we fix L, we can expand R and track distinct count, and we need `right[R+1]`. As R increases, distinct count is non-decreasing. `right[R+1]` is known. So for fixed L, the maximum of `distinct(L..R) + right[R+1]` can be found by scanning R from L to N-1. That's O(N) per L, total O(N^2). Not good.

But maybe we can do it in O(N) by noting that the distinct count for the middle subarray changes only when we encounter new elements. However, the number of distinct elements in the whole array is at most N, but the number of times the distinct count for (L..R) increases as R moves is at most the number of distinct elements. If we process L from N-1 down to 2, we can maintain a freq array and a set for the current middle subarray (which starts at L and ends at R where R is the maximum we have considered). But we need to consider all R. Actually, we can process L from N-1 down to 2, and for each L, we want to find the best R ≥ L. If we process L in decreasing order, we can add A[L] to a "middle" set, and also we can maintain a set of candidates for R. But we need to consider all R.

Wait, there is a known solution: 
- For each i (the end of the first part), we can find the best j (end of the middle) by considering that as j increases, the middle distinct count increases, but `right[j+1]` can be anything. We can use a segment tree or something? No.

Let me think differently. The problem is from AtCoder "ABC 098 D"? No, that's different. It's "ABC 217 E"? No. It's "AtCoder Beginner Contest 277 F"? No.

Actually, I recall a problem: "Three Subarrays" (Hard) from Codeforces Round. But the constraints and problem statement match AtCoder "ABC 217 G"? No, ABC 217 G is "I hate Shortest Path Problem". 

Let me search memory: The problem is "ABC 138 E"? No. It's "ARC 097 C"? No.

Wait, the problem statement says: "This problem is a harder version of Problem C." This is typical for AtCoder problems where the easy version is for two subarrays, and the hard version is for three. The easy version is: split into two non-empty subarrays, maximize sum of distinct counts. The hard version is three subarrays. The easy version can be solved in O(N) by precomputing left and right and finding max left[i] + right[i+1]. The hard version is O(N) as well? But with a sliding window?

Actually, the hard version can be solved in O(N log N) or O(N) using a two-pointer approach where we maintain a window for the middle subarray. Let's try to design it.

We want to maximize `left[i] + mid_distinct + right[j+1]`. 
We can iterate over the left split i from 1 to N-2. For each i, we want to find the best j > i. We can use a set for the middle, starting with j = i+1, and then we can expand j. But as we expand j, the middle distinct count only increases when we see a new element. However, we need to consider all j. But note that `right[j+1]` is fixed for each j. We can just iterate j from i+1 to N-1 for each i? That's O(N^2).

But maybe we can do it in O(N) by noting that the middle subarray's distinct count is monotonic in j, and we can use a data structure to find the best j efficiently. Actually, the function `f(j) = mid_distinct(i+1..j) + right[j+1]` for a fixed i: as j increases, `mid_distinct` is non-decreasing, and `right[j+1]` is arbitrary. We need the max of f(j). This is like we have an array B[j] = right[j+1], and we have a function g(j) = mid_distinct(i+1..j) which is non-decreasing. We want max (g(j) + B[j]). This can be found by scanning j, but doing it for each i is O(N^2). However, if we can update the middle set as we move i, we might be able to reuse computations.

Another approach: The problem is symmetric. We can precompute for each position the number of distinct elements in the prefix and suffix. Then we can iterate over the middle subarray's *start* index L from 2 to N-1. For a fixed L, we want to find the best R ≥ L. We can maintain a set for the middle as we increase R. But we also need to consider that L changes. If we fix R and vary L? 

Wait, there is a known solution: 
- Precompute `left[i]` and `right[i]`.
- Then we iterate over the middle subarray's *right end* R from 2 to N-1. For each R, we want to find the best L ≤ R (with L ≥ 2). The middle is A[L..R]. As L decreases (moving left), the distinct count for the middle can only increase or stay the same (since we are adding elements to the left). So for a fixed R, the function `h(L) = distinct(L..R) + left[L-1]` is non-decreasing as L decreases? Actually, as L decreases, we are including more elements on the left of the middle, so distinct count can increase. left[L-1] is the distinct count in A[1..L-1]. As L decreases, left[L-1] includes more elements, so it is non-decreasing. So h(L) is non-decreasing as L decreases? Not necessarily: distinct(L..R) increases (or stays same), left[L-1] increases (or stays same). So h(L) is non-decreasing as L goes from R down to 2. But we also have `right[R+1]` which is constant for fixed R. So for fixed R, the maximum of `left[L-1] + distinct(L..R)` over L=2..R is simply the value at L=2? Wait, if both components are non-decreasing as L decreases, then the sum is also non-decreasing. So the maximum is achieved at the smallest L, i.e., L=2. But that would mean the best middle subarray ending at R is always the one starting at 2. That's not true, because left[L-1] and distinct(L..R) are not independent: an element that appears in both the left part and the middle part would be counted twice, but in the split, it's counted once in left and once in middle. The distinct count in left[L-1] is the number of distinct elements in A[1..L-1]. The distinct count in A[L..R] is the number of distinct elements in A[L..R]. There is no overlap. So the total distinct in left and middle is exactly the number of distinct elements in A[1..R] minus the number of distinct elements in A[1..L-1]? No. The distinct count in left + middle is not simply the distinct count in the union because the same element could appear in both, but in the sum we count it twice if it appears in both. Actually, the sum of distinct counts for two disjoint subarrays is exactly the number of distinct elements in the first subarray plus the number in the second. If an element appears in both, it is counted twice. So the sum is not the size of the union; it's the sum of sizes. So as we decrease L, we are adding more elements to the left, which might increase left[L-1] by 1 for each new distinct element, and we are also adding elements to the middle (by moving the start left), which might increase distinct(L..R) by 1 for each new distinct element that was not already in A[L+1..R]. However, the element we add to the left is the same element we add to the middle? No, when L decreases, the element A[L] is added to the left part (so left becomes A[1..L]) and the middle becomes A[L..R]. So the element A[L] is in both the left and the middle. So if A[L] is a new distinct element for the left (i.e., it didn't appear in A[1..L-1]), then left[L-1] increases by 1. Also, if A[L] didn't appear in A[L+1..R], then distinct(L..R) increases by 1. So the sum increases by 2 if A[L] is new to both, by 1 if new to one, by 0 if new to neither. So the sum is non-decreasing as L decreases? Not necessarily: if A[L] is already in the middle (so distinct(L..R) doesn't increase) but is new to the left (left increases), then sum increases. If A[L] is already in the left (so left doesn't increase) but new to the middle, sum increases. If A[L] is in both already, sum doesn't change. So indeed, as L decreases, the sum left + middle distinct is non-decreasing! Because we are adding an element to both sets; it can only increase or stay the same for each set independently. Therefore, for a fixed R, the maximum of left[L-1] + distinct(L..R) over L=2..R is achieved at L=2. That means the best middle subarray ending at R is the one that starts as early as possible (L=2). But that would mean the first part is A[1..1] (since L-1 = 1). That is not necessarily true. Wait, is that correct? Let's test with an example: A = [1, 2, 1, 3]. N=4. left[1] = 1 (A[1]=1). left[2] = 2 (1,2). left[3] = 2 (1,2). Suppose R=3 (middle ends at 3). L can be 2 or 3.
- L=3: middle = A[3] = [1]. distinct = 1. left[L-1] = left[2] = 2. Sum = 3.
- L=2: middle = A[2..3] = [2,1]. distinct = 2. left[L-1] = left[1] = 1. Sum = 3.
So both give 3. 
Suppose R=4? But middle must end before N, so R ≤ N-1. For N=4, R can be 2 or 3. R=3 is the max. 
Now consider A = [1, 1, 2, 2]. N=4. left[1]=1, left[2]=1, left[3]=2.
R=3: L=3: middle=[2], distinct=1, left[2]=1, sum=2. L=2: middle=[1,2], distinct=2, left[1]=1, sum=3. So L=2 is better.
R=2: L=2: middle=[1], distinct=1, left[1]=1, sum=2.
So indeed, L=2 (smallest L) seems to give the maximum for fixed R? But wait, what about the constraint that the three subarrays are non-empty? The first subarray is A[1..L-1]. If L=2, first subarray is just A[1]. That's non-empty. So it's allowed. But is it always optimal to take L=2 for a fixed R? That would mean the first split is always at i=1. But that's not true in general. For example, in the sample: A = [3,1,4,1,5]. left: i=1:1, i=2:2, i=3:3, i=4:4. right: k=5:1, k=4:2, k=3:3, k=2:4, k=1:5. 
Consider R=4 (middle ends at 4). Then right[5]=1. L can be 2,3,4.
- L=4: middle=[1], distinct=1, left[3]=3, sum=4 + right[5]=5? Wait, total = left[L-1] + distinct(L..R) + right[R+1]. For R=4, right[5]=1.
  - L=2: left[1]=1, middle=[1,4,1] distinct=2, sum=1+2+1=4.
  - L=3: left[2]=2, middle=[4,1] distinct=2, sum=2+2+1=5.
  - L=4: left[3]=3, middle=[1] distinct=1, sum=3+1+1=5.
So L=3 and L=4 both give 5, which is larger than L=2. So my claim that L=2 is best is false. Why? Because left[L-1] increased from 1 to 2 to 3, and distinct(L..R) decreased from 2 to 2 to 1. The sum increased because left increased more than middle decreased. So as L decreases, left increases and middle distinct may increase or decrease? Wait, when L decreases, the middle subarray becomes longer on the left. It includes more elements. So its distinct count can only increase or stay the same! It cannot decrease. Because we are adding an element to the middle. In the example: 
- L=4: middle = A[4] = [1], distinct=1.
- L=3: middle = A[3..4] = [4,1], distinct=2. Increased.
- L=2: middle = A[2..4] = [1,4,1], distinct=2. Same as L=3.
So distinct(L..R) is non-decreasing as L decreases. left[L-1] is also non-decreasing as L decreases. So the sum is non-decreasing as L decreases. That means the maximum for fixed R is at the smallest L, i.e., L=2. But in the example, for R=4, the sum at L=2 is 1+2+1=4, at L=3 is 2+2+1=5, at L=4 is 3+1+1=5. So the sum is not non-decreasing as L decreases! It went from 4 to 5 to 5. That's non-decreasing (4 ≤ 5 ≤ 5). So it is non-decreasing. The maximum is at L=3 or L=4, which is smaller L? Wait, L=2 is the smallest L. But the sum at L=2 is 4, which is less than at L=3 and L=4. That contradicts the non-decreasing property. Let's check:
- At L=4: left[3]=3, distinct=1, right[5]=1 => 5.
- At L=3: left[2]=2, distinct=2, right[5]=1 => 5.
- At L=2: left[1]=1, distinct=2, right[5]=1 => 4.
So as L decreases from 4 to 2, the sum goes: L=4:5, L=3:5, L=2:4. It decreased! So it is not non-decreasing. Why? Because when L decreases, we add A[L] to the left and to the middle. left increases by 1 if A[L] is new to the left. distinct(L..R) increases by 1 if A[L] is new to the middle. But the increase in left is 1, the increase in distinct is 0 or 1. So the sum increases by 1 or 2 or 0. It should never decrease. But in the example, from L=3 to L=2: we add A[2]=1. left[1] becomes left[2]? Wait, left[L-1] at L=3 is left[2] (A[1..2]) = 2. At L=2, left[1] (A[1..1]) = 1. That's a decrease! Because as L decreases, L-1 decreases, so left[L-1] is the distinct count in a smaller prefix. Ah! I made a mistake. L-1 is the end of the first subarray. As L decreases, the first subarray becomes shorter? No, L is the start of the middle. The first subarray is A[1..L-1]. If L decreases, L-1 decreases, so the first subarray becomes shorter (since L-1 is the end index). For example, L=4: first subarray is A[1..3] (end at 3). L=3: first subarray is A[1..2] (end at 2). L=2: first subarray is A[1..1] (end at 1). So as L decreases, the first subarray gets shorter! Therefore, left[L-1] is a non-increasing function of L? Let's see: left[3]=3, left[2]=2, left[1]=1. So as L decreases, L-1 decreases, and left[L-1] decreases. So left[L-1] is non-increasing as L decreases (i.e., it increases as L increases). And distinct(L..R) is non-decreasing as L decreases (i.e., it decreases as L increases). So the two terms move in opposite directions. So the sum is not monotonic. That makes sense.

So for a fixed R, we want to maximize f(L) = left[L-1] + distinct(L..R) + right[R+1], with L from 2 to R. We can do this by iterating L from R down to 2, maintaining a set for the middle. As we decrease L, we add A[L] to the middle set. We also need to know left[L-1]. We can compute f(L) for each L. But doing this for each R is O(N^2) if we reset the set each time. However, we can process R from 1 to N-1, and for each R, we want to find the best L ≤ R. If we process R from left to right, the set for the middle (L..R) would change as R increases and L changes. This is similar to a 2D problem.

The standard solution for this problem (split into three subarrays) is O(N) or O(N log N). I recall that it uses a sliding window on the middle subarray: we fix the right end of the middle, and then we find the best left end. But we need to do it efficiently.

Let's search my memory: The problem is "ABC 217 G" no. "ARC 108 C" no. Actually, it is "AtCoder Regular Contest 097 C" - "Three Subarrays" maybe? No, ARC 097 C is "K-th Substring". 

Wait, I remember a problem: "Three Subarrays" from Codeforces Round 849 Div 4? No.

Let me think of the constraints: N up to 3e5. A_i up to N. This is a typical AtCoder problem. I think it's from "AtCoder Beginner Contest 217" maybe? Let me check: ABC 217 F is "Make Pair". No. ABC 216 F? No. 

Actually, the problem statement says "This problem is a harder version of Problem C." So the contest has a Problem C that is the easy version (split into two subarrays). This is common in AtCoder. The easy version: given N, split into two non-empty subarrays, maximize sum of distinct counts. That easy version is solved by precomputing left and right and taking max left[i] + right[i+1]. The hard version is split into three. I think this is from "AtCoder Regular Contest 108" or "AtCoder Beginner Contest 222"? Let's check: ABC 222 E is "Red and Blue Tree". No.

Maybe it's from "AtCoder Grand Contest 044"? No.

I recall a problem: "Three Subarrays" (Hard) from AtCoder, and the solution is to precompute left and right, and then for each i (the split between first and second), we can use a set for the second subarray and expand it. But we need to bound the total operations. The trick is that the second subarray can be expanded using a two-pointer technique because the distinct count in the second subarray is monotonic, and we can maintain a "best" value. Actually, we can do the following:
- Iterate over the first split i from 1 to N-2.
- For each i, we want to find the best j > i.
- We can maintain a pointer j that starts at i+1 and moves right. As we move j, we add A[j] to a set. The distinct count of the middle is the size of the set. We also know left[i] and right[j+1]. So for this i, the best j gives left[i] + size(set) + right[j+1]. But as we increase i for the next iteration, the middle subarray changes completely, so we have to reset the set. That would be O(N^2) if we do it naively.

However, we can iterate over the *second* split j from 2 to N-1, and for each j, we want to find the best i < j. For a fixed j, we can maintain a set for the middle as we decrease i. But again, resetting for each j is O(N^2).

The known solution: 
- Precompute left and right.
- For each possible middle subarray, we can compute its distinct count. But we need to find the max over all.
- We can use a segment tree or a sparse table to answer distinct count queries? No, the distinct count for a range can be answered with Mo's algorithm or sqrt decomposition, but we need to do it for many ranges.

Wait, there is a known O(N) solution: 
- For each index k, we want to know the number of distinct elements in the subarray from k to some point. 
- The key observation: The middle subarray can be represented by its left end L and right end R. We want to maximize left[L-1] + distinct(L,R) + right[R+1].
- We can iterate L from 2 to N-1. For each L, we want to find the best R ≥ L. As we increase L, we can maintain a set for the current R? But R can be anything.
- Actually, we can fix R and vary L. As R increases, we can add A[R] to some data structure. For a fixed R, the function f(L) = left[L-1] + distinct(L,R) is what we need to maximize. We can precompute for each R the maximum of f(L) over L ≤ R. Then the answer is max over R of (max_{L} f(L) + right[R+1]).
- So we need to compute for each R: M[R] = max_{2 ≤ L ≤ R} (left[L-1] + distinct(L,R)). Then answer = max_R (M[R] + right[R+1]).
- How to compute M[R] efficiently? As R increases, we can update M[R] from M[R-1]. When we move from R-1 to R, the new element A[R] is added to the right end of the middle subarray. For any L, distinct(L,R) = distinct(L,R-1) + (1 if A[R] is not in A[L..R-1] else 0). So it's not a simple update.
- Alternatively, we can process from right to left. Fix L, and find best R. As we increase R, distinct(L,R) increases when A[R] is new to the window. This is like we have a window and we are adding elements to the right. We can maintain a set for the window. But we need to do this for all L.

Wait, there is a known solution: 
- We can compute the distinct count for all subarrays in O(N) if we use the fact that A_i ≤ N? No, the number of subarrays is O(N^2), but we only need a specific measure.

Let's think of a different approach. The problem is to maximize f(i,j) = left[i] + mid(i+1,j) + right[j+1]. This is like we have an array B where B[k] = something. Not directly.

I recall that for the "hard version" of splitting into three subarrays, the solution uses a "two-pointer" or "sliding window" on the middle subarray, but with a twist: we maintain the middle subarray's distinct count and also a separate set for the right part? No.

Let's search for "AtCoder three subarrays distinct" in my memory. I think it's from "AtCoder Beginner Contest 217 G" no. Actually, it's "AtCoder Regular Contest 097 C" no. Let's think of recent contests: "ABC 277" is "Triangle". "ABC 278" is "Xor and Sum". "ABC 279" is "Zero Subarray". Not that.

Maybe it's from "Codeforces Round 849 Div 2"? No.

Wait, the problem is exactly "ABC 098 D" no. It's "ABC 138 E" no.

Let me try to solve it from scratch with a different perspective. The constraints are N up to 3e5. We need an O(N log N) or O(N) solution. The naive O(N^2) is too slow.

We can precompute for each index the number of distinct elements in the prefix and suffix. That's O(N). Now we need to maximize left[i] + mid(i+1,j) + right[j+1]. This is equivalent to: for each j, find the best i < j that maximizes left[i] + mid(i+1,j). So we can iterate j from 2 to N-1, and for each j, we need to compute max_{i < j} (left[i] + mid(i+1,j)). Then add right[j+1] and take the max over j.

So the problem reduces to: as we sweep j from left to right, maintain a set of possible i's, and for each j, we need to know for each i, the distinct count of A[i+1..j]. That is, we need to maintain a data structure that can answer: given a set of left endpoints i, and we extend the right endpoint to j, what is the distinct count of A[i+1..j]? And we need to maximize left[i] + that distinct count.

This is a classic problem that can be solved with a "frequency of frequencies" or by maintaining a bitset? But we need to do it for all i. The number of i's is O(N). For each j, we would need to update the distinct count for all i. That's O(N^2).

But note that the distinct count of A[i+1..j] only increases when we encounter a new element. For a fixed i, the distinct count is the number of distinct elements in the subarray. As j increases, the distinct count for that i only changes when we see an element that hasn't appeared in A[i+1..j-1]. So for each i, the distinct count changes at most the number of distinct elements in the whole array times? Actually, it can change O(N) times per i in the worst case (if all elements are distinct). So that's still O(N^2).

We need a more clever data structure. Perhaps we can reverse the roles: instead of fixing i and varying j, we can fix the set of elements in the middle and consider the possible i and j. 

Another idea: The problem is equivalent to choosing three disjoint contiguous subarrays that cover the whole array? No, they partition the array. So the array is split at i and j. The middle is A[i+1..j]. We can think of the middle subarray as a window. For each possible window (L, R), the value is left[L-1] + distinct(L,R) + right[R+1]. We want the maximum over all L, R with 2 ≤ L ≤ R ≤ N-1. 

We can iterate over R from 2 to N-1. For each R, we want to find L that maximizes left[L-1] + distinct(L,R). We can maintain a data structure for L. As R increases, we add A[R] to the right. The distinct(L,R) for a given L increases by 1 if A[R] is not in A[L..R-1]. So for each L, we need to know if A[R] is already in the current window. This is like we have a window (L, R) and we are adding an element at R. We can maintain a frequency array for the whole window? But the window changes with L.

Wait, we can process L from 2 to N-1. For each L, we can expand R to the right until the end. As we expand R, we maintain a set. For a fixed L, the function f(R) = left[L-1] + distinct(L,R) + right[R+1] is left[L-1] + (distinct(L,R) + right[R+1]). We want the max over R. Since left[L-1] is constant for fixed L, we need to maximize g(R) = distinct(L,R) + right[R+1] for R ≥ L. Now, as L increases, the set for the middle changes (we remove A[L] from the left of the window). So we can process L from N-1 down to 2. When we decrease L (i.e., move L to the left), we add A[L] to the window. But we also need to consider all R. This is like we have a window that starts at L and ends at some R. We want to find the best R. If we fix L, we can just scan R from L to N-1 and compute distinct(L,R) and right[R+1]. That is O(N) per L, total O(N^2). But maybe we can do it faster if we note that distinct(L,R) is the number of distinct elements in the window. As we move L left, the window gains A[L] and we lose the leftmost element? No, the window is L..R, so as L decreases, the window expands to the left. So the window is [L, R]. We can choose R freely. So for each L, we want to find the best R. We can think of this as: for each L, we have an array of values for R: distinct(L,R) + right[R+1]. We need the max over R. If we can precompute for each R the value right[R+1], and we can quickly compute distinct(L,R) for any L, R, then we could use a segment tree. But distinct(L,R) is not easily computable in O(1) without preprocessing. However, we can use a "sparse table" or "offline queries" to answer distinct count queries in O(1) or O(log N). But there are O(N^2) queries.

Wait, we only need the maximum over R for each L, not the value for each R. So we can do the following: for each L, we can expand R from L to N-1, and we only care about the maximum. But as we expand R, distinct(L,R) increases. It increases by 1 exactly when A[R] is a new element in the window. So the number of times distinct(L,R) increases is at most the number of distinct elements in A[L..N-1]. If we do this for all L, the total work might be O(N sqrt N) or O(N log N) if we use a two-pointer approach where we move L and R together.

Consider the following two-pointer approach: We maintain a window [L, R] and a set of elements in the window. We also have the value for the current window: left[L-1] + distinct(L,R) + right[R+1]. We want to maximize this over all windows. We can start with L=2, R=2. Then we can try to expand R to the right, updating the set and the distinct count. For each R, we have a candidate. Then we can increment L, and adjust R? But R cannot decrease because the window must be contiguous? Actually, as L increases, the window's left boundary moves right. We can then expand R further to the right to consider larger windows. But we might miss some windows where R is smaller than the current R. So we need to be careful.

This is similar to the problem of finding a subarray with maximum distinct count plus something. But here the function is not just the size of the window; it also includes left and right.

Another perspective: The answer is max_{i < j} (left[i] + right[j+1] + distinct(i+1, j)). This is like a convolution. We can precompute left[i] and right[j+1]. The challenge is the middle term. Notice that distinct(i+1, j) is the number of distinct elements in the subarray. This is equivalent to: sum over elements x of (1 if x appears in (i+1, j) else 0). So distinct(i+1, j) = sum_{x} I(x in (i+1, j)). Therefore, the total sum = left[i] + right[j+1] + sum_x I(x in (i+1, j)). This is not separable.

But we can think of it as: for each element x, it contributes 1 to the middle distinct count if it appears in the middle subarray. It also might contribute to left and right. But left and right are precomputed, so they already account for the distinct counts in the first and third parts. So the total is exactly the sum of distinct counts in the three parts. There is no overlap in counting: each part's distinct count is computed independently. So the total is just the sum.

Maybe we can use a "divide and conquer" approach? Or a "D&C on the split point"? There is a known technique for splitting into two subarrays: we can use a set and expand from the middle. For three subarrays, maybe we can use a "two pointers" where we maintain a window for the middle, and we consider the best left and right for that window.

Specifically, for each possible middle subarray (L, R), the total is left[L-1] + distinct(L,R) + right[R+1]. We can think of this as: for each R, we want to find the best L. We can precompute an array `best_left_for_R` that gives the maximum of left[L-1] + distinct(L,R) over L ≤ R. How to compute that? We can process R from left to right. When we increase R, we add A[R] to the right. For each L, distinct(L,R) increases by 1 if A[R] is not in the current window for that L. So we need to update the value for all L. That's O(N) per R.

But wait! The distinct count for a given L is exactly the number of distinct elements in the window. As we add A[R], the distinct count for a window (L, R) increases if A[R] is a new element in that window. So for all L such that A[R] is not in (L, R-1), the distinct count increases. How many such L are there? It's the set of L such that the first occurrence of A[R] in (L, R) is at R. In other words, L must be greater than the previous occurrence of A[R] before R. So if the previous occurrence of A[R] is at index p, then for any L > p, the window (L, R) does not contain A[R] in (L, R-1), so the distinct count increases. For L ≤ p, the window already contains A[R] (from the previous occurrence), so the distinct count does not increase. Therefore, when we add A[R], the distinct count for all windows (L, R) with L > p increases by 1. This is a key observation!

So we can maintain an array `val[L]` for L = 2..N-1, which represents the value left[L-1] + distinct(L, R) for the current R. Initially, for R=1, we can't have middle. But we can start with R=2? Actually, the middle must be non-empty, so L ≤ R. So we can initialize for R=1, but there is no valid L. We can process R from 2 to N-1. At step R, we want to update val[L] for L from 2 to R. Initially, for R=2, the only possible L is 2. So val[2] = left[1] + distinct(2,2). Then for R=3, we have L=2 and L=3. We can update from the previous R. 

Let's formalize:
We have an array `val[L]` for L = 2..N-1, which we want to be `left[L-1] + distinct(L, R)` for the current R (we process R increasing). Initially, for R = 1, we can set val[L] = left[L-1] (since distinct(L,1) = 0 if L=1? But L starts at 2, so for R=1, no valid L. So we can start with R=2: val[2] = left[1] + 1 (if A[2] is distinct, which it is for the single element). Actually, we can initialize for R=1: for L=2, val[2] = left[1] (distinct(L,1) is 0 because L=2 > 1, so empty middle? No, if R=1, the middle subarray would be (L..R) = (2..1) which is empty. So we don't consider R=1. So start at R=2.

We want to maintain val[L] as we increase R. When we increase R to R+1, we need to update val[L] for all L ≤ R+1. The change: distinct(L, R+1) = distinct(L, R) + (1 if A[R+1] not in A[L..R] else 0). So val[L] increases by 1 if A[R+1] is not in A[L..R], else 0. As observed, if the previous occurrence of A[R+1] in the array is at index p (with p < R+1), then for any L > p, A[R+1] is not in A[L..R] (because the only occurrence in L..R would be at p, but L > p means p is not in L..R). For L ≤ p, A[R+1] is in A[L..R] (at p), so no increase. So the update is: for all L in (p+1 .. R+1], val[L] += 1. Note that L must be ≥ 2, and L ≤ R+1. So we can do a range add on the array val[L] for L in [max(2, p+1), R+1]. This is a range add query. We can maintain val as a difference array or a Fenwick tree or a segment tree. But we also need to be able to query the maximum of val[L] over L=2..R+1 at each step R+1 to compute the candidate answer: max_val + right[R+2] (since the third part starts at R+2). Actually, the candidate for split (L-1, R) is val[L] + right[R+1]. So for each R from 2 to N-1, we need max_{L=2..R} (val[L]) + right[R+1].

So the algorithm:
1. Precompute left[i] for i=1..N.
2. Precompute right[i] for i=1..N+1 (right[N+1]=0).
3. Initialize an array `add` of size N+2 with zeros. We will use a Fenwick tree or segment tree to support range add and range max query on the indices 2..N-1. But we only need to add on ranges [max(2, p+1), R] as we process R.
4. We will process R from 2 to N-1. We maintain a data structure over indices L=2..R. Initially, for R=2, we need to set val[2] = left[1] + 1. But we can also start with R=1 and have val[L] = left[L-1] for L=2..N-1, and then as we add elements, we do range adds. Let's see:
   - Initially, for L=2..N-1, let val[L] = left[L-1]. This corresponds to distinct(L, R) with R=1? But for R=1, the middle (L..1) is empty, so distinct=0. So val[L] should be left[L-1] for R=1. But we only care about R ≥ 2. So we can start with this base, and then for each R from 2 to N-1, we add the new element A[R] to the middle. The effect of adding A[R] to the middle is: for all L such that L ≤ R, the distinct count for window (L, R) includes A[R] if it's new. But we can think of it as: we are building the window from left to right. So for R=2, we want val[2] = left[1] + 1. In our base, val[2] = left[1]. So we need to add 1 to val[2]. For R=3, we have windows (2,3) and (3,3). The new element is A[3]. For L=3, window (3,3) gets A[3] as a new distinct, so val[3] increases by 1. For L=2, window (2,3) gets A[3] if it's new. So we need to add 1 to val[2] if A[3] is not in A[2..2]. This matches the range add idea: when adding A[R], we find its previous occurrence p. Then for all L in [max(2, p+1), R], we add 1 to val[L] (because for those L, the window (L, R) does not contain A[R] before, so it's a new distinct element). But wait, we also need to consider that for L=R, the window is just A[R], so it's always a new distinct element. So the range is L from max(2, p+1) to R. This works.

So algorithm:
- Compute left[1..N], right[1..N+1] (right[N+1]=0).
- Initialize a segment tree or Fenwick tree with all values = left[L-1] for L=2..N-1. (We only care about L=2..N-1 because the first subarray must be non-empty, so L-1 ≥ 1 => L ≥ 2; and the middle must be non-empty and not the last element, so R ≤ N-1, and L ≤ R, so L can be up to N-1.)
- Maintain an array `prev` to store the last occurrence of each value. `prev` size N+1 (since A_i ≤ N).
- ans = 0.
- For R from 2 to N-1:
  - p = prev[A[R]] (0 if not seen before).
  - L_start = max(2, p+1).
  - L_end = R.
  - If L_start <= L_end, do a range add of 1 to indices L_start..L_end in the segment tree.
  - Update prev[A[R]] = R.
  - Now, the current max val over L=2..R is the maximum in the segment tree for indices 1..R (or 2..R). We can query the maximum on the range [2, R].
  - candidate = max_val + right[R+1].
  - ans = max(ans, candidate).
- Print ans.

We need a data structure that supports range add and range max query. A segment tree with lazy propagation can do this in O(log N) per operation. Since we do N operations, total O(N log N). N=3e5, so O(N log N) is fine.

But we can do even better: we can use a Fenwick tree for range add and point query? No, we need range max query. Fenwick tree can do range add and point query, or point add and range sum, but not range add and range max. So we need a segment tree with lazy propagation. That's O(N log N). With 3e5, it's fast enough.

However, we can optimize: we only need the maximum over a prefix [2, R]. So we can maintain the maximum in a segment tree that supports range add and range max. That's standard.

Let's verify the logic with the sample.
Sample 1: A = [3,1,4,1,5]. N=5.
left: 
1:1, 2:2 (3,1), 3:3 (3,1,4), 4:3 (3,1,4,1), 5:4 (3,1,4,1,5).
right (1-indexed, right[k] = distinct in A[k..N]):
1:4 (3,1,4,1,5) -> wait: A[1..5] = 3,1,4,1,5 distinct: 3,1,4,5 -> 4. So right[1]=4.
2:4 (1,4,1,5) -> 1,4,5 -> 4. right[2]=4.
3:3 (4,1,5) -> 4,1,5 -> 3. right[3]=3.
4:2 (1,5) -> 1,5 -> 2. right[4]=2.
5:1 (5) -> 1. right[5]=1.
right[6]=0.

Initialize val[L] for L=2..4 (since N-1=4):
L=2: val[2] = left[1] = 1.
L=3: val[3] = left[2] = 2.
L=4: val[4] = left[3] = 3.

prev array: all 0.

R=2:
p = prev[A[2]] = prev[1] = 0.
L_start = max(2, 1) = 2.
L_end = 2.
Add 1 to val[2] -> val[2] becomes 2.
prev[1] = 2.
Now max val over L=2..2: val[2]=2.
candidate = 2 + right[3] = 2 + 3 = 5.
ans = 5.

R=3:
p = prev[A[3]] = prev[4] = 0.
L_start = max(2, 1) = 2.
L_end = 3.
Add 1 to val[2] and val[3].
val[2] was 2 -> 3.
val[3] was 2 -> 3.
prev[4] = 3.
max val over L=2..3: max(3,3) = 3.
candidate = 3 + right[4] = 3 + 2 = 5.
ans = 5.

R=4:
p = prev[A[4]] = prev[1] = 2.
L_start = max(2, 3) = 3.
L_end = 4.
Add 1 to val[3] and val[4].
val[3] was 3 -> 4.
val[4] was 3 -> 4.
prev[1] = 4.
max val over L=2..4: max(3,4,4) = 4.
candidate = 4 + right[5] = 4 + 1 = 5.
ans = 5.

So ans=5. Correct.

Sample 2: N=10, A= [2,5,6,4,4,1,1,3,1,4].
Let's compute left and right quickly? Not needed, but the algorithm should give 9.

So the O(N log N) solution with segment tree works.

But can we do it in O(N)? Since we only need the max over a prefix, and we are doing range adds on suffixes, we might be able to use a simpler data structure. Actually, the range we add to is always of the form [L_start, R], which is a suffix of the current valid L's (from 2 to R). So we are adding to a suffix of the prefix. We need to maintain the maximum of a prefix of an array that supports suffix additions. We can do this with a Fenwick tree if we reverse the order? Let's see: indices L=2..N-1. We need to add to a range [a, b] and query max on [2, R]. If we map L to N-1 - L + 2 or something? Actually, we can maintain the array in reverse order: let index i = R - L + 1? Not exactly. The query is max over L=2..R. That's a prefix of the array (from the start). The updates are on suffixes of the current prefix? When we add to [L_start, R], that's exactly a suffix of the prefix [2, R]. So we are adding to a suffix of the prefix. If we maintain a segment tree over the whole array [2, N-1], we can do it. But maybe we can use a "max suffix" or something? Since we only need the max over the whole prefix [2, R] at the end, and we are adding to suffixes, we can maintain the array and keep track of the maximum. However, the additions are to suffixes, and we need the max of the entire prefix. We can maintain a multiset of values, but the range add makes it hard because all values in the range change. So a segment tree is the natural choice.

But wait, we can do it in O(N) with a different approach: we can precompute for each position the "next occurrence" and use a two-pointer? Let's think if we can do it in O(N) using the fact that the range add is on a contiguous range that is a suffix. We can maintain an array `val` and an array `lazy` for suffix additions. Actually, we can maintain a difference array `diff` such that the value at L is the sum of diff[2..L]. Since we are adding 1 to a suffix [a, R], we can just increment diff[a] and decrement diff[R+1]. Then to get the max over [2, R], we need the maximum of the prefix sums. That is not easily maintained in O(1) per update. We could use a segment tree, which is O(N log N). With N=3e5, O(N log N) is perfectly fine. The time limit is usually 2-3 seconds, and segment tree in Python might be a bit tight but should pass with careful implementation (e.g., using iterative segment tree). Or we can use PyPy and it's fine.

But wait, we can do it in O(N) if we use a "max of prefix sums" with a data structure like a "max segment tree" that supports range add and range max. That's O(N log N). There is also an O(N) solution using a "deque" or "monotonic queue" if we can express it differently? Let's see: the problem is equivalent to max_{i<j} (left[i] + right[j+1] + distinct(i+1,j)). This is like a convolution. We can also use a "divide and conquer" approach on the value? No.

Another known solution: 
- For each i, we can find the best j using a two-pointer technique. Actually, we can fix the right end of the middle j, and then we want to find i. We can use a set for the middle and expand it. But we need to consider all i. The two-pointer approach: we maintain a window [L, R] for the middle. We start with L=2, R=2. Then we can try to expand R to the right. But as we expand R, the distinct count increases. We can also move L to the right. But we need to consider all splits (L, R). We can iterate over L and R simultaneously? Not exactly.

Given the time constraints, the O(N log N) segment tree solution is standard and reliable. I'll implement that.

But let's double-check the segment tree operations:
- We have an array `val` of size N (for indices 1..N, but we only use 2..N-1). We can use 1-indexed segment tree.
- Initially, for i=2..N-1, val[i] = left[i-1].
- We need to support:
  1. Range add: add v to val[l..r].
  2. Range max query: max on [2, R] (or [L, R] but we always query from 2 to current R).
- Since we always query the max on [2, R], we can maintain a pointer R and query the prefix max. We can just query the max on [2, R] each time. That's O(log N) per query.
- The updates are on [L_start, R] where R is the current R. So we update a range that ends at the current R. So we can do: for R from 2 to N-1:
    p = prev[A[R]]
    L_start = max(2, p+1)
    if L_start <= R:
        segtree.range_add(L_start, R, 1)
    prev[A[R]] = R
    max_val = segtree.range_max(2, R)
    ans = max(ans, max_val + right[R+1])

This is O(N log N). N=3e5, log N ~ 19, so about 6 million operations. In Python, with an iterative segment tree, it should be fast. But we need to be careful with recursion depth; iterative is better.

We can also use a Fenwick tree if we only need to query the max on a prefix? No, Fenwick can't do range add and range max. But we can do range add and point query, then we could maintain a priority queue of values, but the values change, so we need a lazy propagation. So segment tree is the way.

Let's think if we can avoid the segment tree. We have an array, we add 1 to suffixes, and we want the max of the prefix. We can maintain the array in a "difference" style and also maintain a "max of prefix" using a stack or something? Since we are adding to suffixes, the order of values might be preserved? Not necessarily. For example, if we have values [3, 1, 2] and we add to a suffix, the max might change in a non-trivial way. So segment tree is simplest.

But wait, there is a known O(N) solution for this problem using "next occurrence" and a "sparse table" or "offline queries"? Actually, I recall that the problem can be solved in O(N) by iterating over the middle subarray's right end and maintaining a "best left" using a map of the last occurrence. Let's try to derive an O(N) solution.

We want to maximize left[i] + right[j+1] + distinct(i+1, j). 
We can process j from 2 to N-1. We need to maintain a set of candidates for i. For each i, the value is left[i] + distinct(i+1, j). As j increases, the distinct count for a given i increases by 1 if A[j] is not in A[i+1..j-1]. As before, this is equivalent to: for the current j, for each i, if the next occurrence of A[j] before j is p, then for i > p, distinct(i+1, j) increases. So we can think of it as: we have an array of values for i, and when we add A[j], we add 1 to all i in (p, j-1]? Actually, i goes from 1 to j-1. The condition for i is: A[j] is not in A[i+1..j-1]. The previous occurrence of A[j] is at p < j. If p < i+1, then A[j] is not in A[i+1..j-1]? Wait: if p < i+1, then the previous occurrence is before the start of the middle subarray, so it is not included. So A[j] is a new distinct element for the middle subarray. If p ≥ i+1, then the previous occurrence is inside the middle subarray, so A[j] is not new. So the condition is: i+1 > p, i.e., i ≥ p. So for i in [p, j-1], the distinct count increases. But note that i must be at least 1, and the first subarray is A[1..i], so i ≥ 1. Also, the middle is A[i+1..j], so we need i+1 ≤ j, so i ≤ j-1. So i ranges from 1 to j-1. For i in [p, j-1], the distinct count for middle (i+1..j) increases by 1. So we can maintain an array `add` of length N, and for each j, we add 1 to add[p..j-1] (where p is the previous occurrence of A[j]). Then the distinct count for middle (i+1..j) is the sum of adds for that i over the steps? Actually, if we initialize distinct(i+1,1) = 0, and for each j from 2 to N-1, we add to the range, then distinct(i+1,j) = sum of additions for i from the steps up to j. But we can maintain a running array `val[i]` that is left[i] + distinct(i+1, current j). Initially, for j=1, val[i] = left[i]. Then for each j, we add 1 to val[i] for i in [p, j-1] (if p ≤ j-1). Then the candidate is max_{i=1..j-1} val[i] + right[j+1]. This is exactly the segment tree approach but with a different range: [p, j-1] instead of [max(2, p+1), R]? Let's check: In the previous notation, L = i+1, so i = L-1. The range for L was [max(2, p+1), R] where R is the current R (which is j). So L from p+1 to j. That corresponds to i from p to j-1. And the first subarray is A[1..i], so i ≥ 1. Also, the middle must be non-empty, so i+1 ≤ j => i ≤ j-1. So i from 1 to j-1. So the range is i in [max(1, p), j-1]. In the earlier, I had L_start = max(2, p+1), so i_start = L_start - 1 = max(1, p). So it matches. So we are adding to i in [p, j-1] (if p ≤ j-1). So we can maintain an array `val[i]` for i=1..N-2 (since i < j ≤ N-1). Initially, val[i] = left[i] for i=1..N-2. Then for j=2 to N-1:
    p = previous occurrence of A[j] (0 if none).
    if p <= j-1: (if p=0, then p <= j-1 always true, so we add to [0, j-1]? But i starts at 1, so we need to handle p=0. If p=0, then we add to all i from 1 to j-1. So we can set L = max(1, p).)
    Actually, if p=0, then we add to i in [1, j-1] (since max(1,0)=1). So the range is [max(1, p), j-1].
    So we do: for i in [max(1, p), j-1], val[i] += 1.
    Then candidate = max(val[1..j-1]) + right[j+1].
This is exactly the same as the segment tree approach, but with i instead of L. So we can use a segment tree over i=1..N-2. The update is range add on [max(1, p), j-1], and query is max on [1, j-1]. This is still O(N log N) with segment tree.

Can we do it in O(N)? We need to support range add and prefix max. There is a data structure called "segment tree with lazy propagation" which is O(log N). But there is also a trick: since we are always adding to a suffix of the prefix? Actually, the range we add to is [p, j-1], which is a suffix of the valid i's (from 1 to j-1). So we are adding to a suffix of the current prefix. We want the max of the prefix. This is exactly the same as before. We can maintain a "max of prefix" by keeping track of the array and a "lazy" value for the suffix? If we maintain the array in reverse order, then adding to a suffix becomes adding to a prefix in the reversed array. Then we need the max of the prefix in the reversed array? Let's see: if we reverse the indices, let k = N - i. Then the prefix [1, j-1] becomes [N-(j-1), N-1] which is a suffix. The update [p, j-1] becomes [N-(j-1), N-p]. That's not a simple prefix. So it doesn't simplify.

However, there is a known O(N) solution for this problem using a "map of last occurrence" and a "multiset" where we update values by adding 1 to a range, but we can do it by maintaining a difference array and a "max prefix" using a segment tree that supports range add and range max. The O(N log N) is fine. But maybe we can do it in O(N) if we use a "deque" or "monotonic queue" because the values have a special property? Let's check if the array `val[i]` has any monotonicity. As we move j, we add 1 to a suffix. The values in the suffix increase by 1. The relative order of the values might change, but only by 1. We can maintain the max easily with a segment tree. I think O(N log N) is the intended solution for the hard version, and the easy version is O(N). The problem says "harder version", so O(N log N) is acceptable.

But wait, there is an O(N) solution using a "two-pointer" on the middle subarray. Let's think: we want to maximize left[i] + distinct(i+1,j) + right[j+1]. We can fix the middle subarray's length or something. Another approach: we can precompute for each position the number of distinct elements in the subarray ending at that position. But that doesn't help.

I recall a solution that uses "sparse table" to answer distinct queries in O(1), and then uses a "two-pointer" to find the best j for each i. But the two-pointer would be O(N) if the distinct count is monotonic. For a fixed i, as j increases, distinct(i+1,j) is non-decreasing, and right[j+1] is arbitrary. We want to maximize the sum. This is like for each i, we have an array of values: f_i(j) = distinct(i+1,j) + right[j+1]. We want the max over j. We can compute f_i(j) for all j? That's O(N^2).

Wait, there is a known solution: 
- For each i, we can find the "best" j by considering that distinct(i+1,j) only changes at certain points. But we still need to consider all j.

Maybe we can do it by iterating over the middle subarray's distinct elements? No.

Given the time, I'll implement the O(N log N) segment tree solution. It's clean and correct.

Let's implement the segment tree with range add and range max.
We can use an iterative segment tree with lazy propagation. Since we have up to 3e5 elements,

## worker: Read N and array A (1-indexed).
We solved the problem using a segment tree with lazy propagation to support range add and range max queries. The key idea is to precompute `left[i]` (distinct in prefix) and `right[k]` (distinct in suffix). We then iterate over the end of the middle subarray `j` from 2 to N-1. For each `j`, we maintain an array `val[i] = left[i] + distinct(i+1, j)` for all `i < j`. When we add a new element A[j] to the middle subarray, the distinct count for windows (i+1..j) increases by 1 for all `i` such that A[j] is not already in the window. This happens exactly when `i` is at least the previous occurrence `p` of A[j]. So we add 1 to the range `[max(1, p), j-1]`. Then the best split for this `j` is `max(val[1..j-1]) + right[j+1]`. We take the maximum over all `j`. The segment tree allows us to do range adds and range max queries in O(log N) per operation, total O(N log N) which is efficient for N up to 3e5.

## worker: Refine the Python solution to ensure correctness a
The solution uses a segment tree with lazy propagation to efficiently support range additions and range maximum queries. The key insight is to iterate over the end of the middle subarray `j`. For each `j`, we maintain an array `val[i] = left[i] + distinct(i+1, j)` for all possible `i < j`. When adding a new element `A[j]`, the distinct count for windows `(i+1..j)` increases by 1 for all `i` such that the previous occurrence `p` of `A[j]` satisfies `i ≥ p`. This translates to a range add on `[max(1, p), j-1]`. After the update, the best split for this `j` is `max(val[1..j-1]) + right[j+1]`. Taking the maximum over all `j` yields the answer. The algorithm runs in O(N log N) time, which is efficient for N up to 3×10⁵. Tested on the provided samples and matches expected outputs.

## worker: Implement the final solution in Python: read N and
The solution uses a segment tree with lazy propagation to efficiently handle range additions and range maximum queries. The key insight is to iterate over the end of the middle subarray `j`. For each `j`, we maintain an implicit array `val[i] = left[i] + distinct(i+1, j)` for all `i < j`. When adding a new element `A[j]`, the distinct count for windows `(i+1..j)` increases by 1 for all `i` such that the previous occurrence `p` of `A[j]` satisfies `i ≥ p`. This corresponds to a range add on `[max(1, p), j-1]`. The best split for this `j` is `max(val[1..j-1]) + right[j+1]`. Taking the maximum over all `j` yields the answer. The algorithm runs in O(N log N) time, which is efficient for N up to 3×10⁵. The segment tree is implemented iteratively to avoid recursion overhead and match the required format.
