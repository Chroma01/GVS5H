1. The problem involves huge N (up to 10^12) but small jump range (A,B ≤ 20) and M ≤ 20000 bad intervals, with sorted non-overlapping intervals.
2. We can perform a BFS/DFS over the positions modulo some cycle. Since jumps are bounded, the only relevant information is the "state" within a window of size B behind a bad interval's right edge. This is a classic AtCoder problem solved using BFS on the "distance" modulo some base.
3. We'll use the standard approach: BFS from position 1, maintaining a set of visited positions (compressed). For each reachable position x, try jumps in [A,B] to find x+i that is not in any bad interval. We need an efficient way to check if x+i is "good".
4. Since M is small enough, we can store bad intervals in a list, and for each candidate y, binary search the interval list to see if y falls in any. We also need to cap the BFS to avoid infinite loops: we only need to explore up to the start of the last bad interval + B (or similar), because after the last bad interval, we can just greedily jump if there's a gap.
5. Algorithm: BFS using a queue. Start with position 1. Track visited positions. For each position x popped:
   - For each i in [A,B]:
     - y = x + i
     - If y > N: break (since jumps are positive, we can break for i beyond limit, but we should check y<=N)
     - If y == N: print "Yes" and return.
     - If y is bad: skip
     - If y not visited: mark visited, push to queue.
   - To detect y being bad: binary search the intervals. Since intervals are sorted and non-overlapping, we can find the interval where L_i <= y <= R_i.
   - Cap the maximum x we push: Actually we need to ensure BFS terminates. We can keep a maximum "limit" based on the next bad interval: once we reach a point past the last bad interval, we can just check if the gap to N is reachable. But a simpler cap: we only care about positions up to the end of the last bad interval + B? Actually if we can reach a position > last bad interval's R, then we just need to check if (N - pos) is reachable by jumps. Since jumps are [A,B], we can reach N if there's some k such that k*A <= (N-pos) <= k*B? Not exactly, because we can accumulate steps. But the problem is a standard one: AtCoder ABC 175 E? No, this is similar to AtCoder ABC 174 F or a specific problem. Actually it's from AtCoder ABC 195? No. I recall a problem "Good Jumper" or similar. Wait, it's AtCoder ABC 196 D? No.
6. Let me recall: This is AtCoder ABC 174? Actually there's a problem "Jumping Takahashi" or similar. The known solution: BFS on positions, but the positions can be large. However, because B ≤ 20, we can represent the state by the "minimum position" we can reach relative to the end of bad intervals. The standard solution: BFS from 1. For each reachable x, try all jumps. To avoid infinite BFS, we only need to explore x up to the end of the last bad interval + B. Because once you are past all bad squares, if N is within [x + A, x + B] or you can continue jumping (but there are no bad squares), you can check directly. Actually, if there are no bad squares from some point onward, you can just check if the remaining distance is reachable. More precisely, the BFS only needs to explore positions up to min(N, last_bad_R + B). Beyond that, we can determine reachability to N using a simple modulo argument.
7. Wait, the known solution for this exact problem (AtCoder ABC 195 F? No, it's ABC 200 D? No.) Let me think: The problem is "Jumping Takahashi" or "Bad Squares". Actually it's AtCoder ABC 174 F? No. Let me search my memory: There's an AtCoder problem "ABC 196 D" is about tatami. Not this.
8. Actually this is AtCoder ABC 161? No.
9. I remember a problem: "Given N, M, A, B and bad intervals, can you reach N from 1 with jumps in [A,B] avoiding bad squares?" The solution is BFS where we maintain a set of "distances" modulo something. Wait, there's a known trick: Since A,B are small, we can BFS over positions, but to keep the BFS finite, we only need to consider positions up to the rightmost bad square + B, because if we can reach a position x > last_bad_R, then we can reach N if and only if (N - x) is reachable by unrestricted jumps? Not exactly, because there might be bad squares, but we assumed x is past all bad squares. So from x, all squares are good. Then we can just check if N - x is in the reachable set from 0 using jumps in [A,B]. But the reachable set from 0 using jumps in [A,B] is all integers >= some Frobenius number? Since A and B are not coprime necessarily, but A <= B <= 20. Actually if gcd(A,B) = g, we can only reach multiples of g. But we can also check if there's a path. However, the BFS approach typically used: we BFS until we either reach N or exhaust positions up to some limit. The limit is the position of the last bad square + B, or N if no bad squares.
10. The exact solution: BFS from 1. Maintain a set of visited positions. For each x popped, try y = x + i for i in [A,B]. If y == N, success. If y is bad, skip. If y > limit (where limit = min(N, last_bad_R + B)), skip. Else if not visited, add. After BFS, if we haven't reached N, then we check: if we can reach a position x > last_bad_R (i.e., past all bad squares) and x < N, can we reach N? Actually, we also need to consider that from x we can continue jumping with the same rule (no bad squares). So we can check: is there a path from x to N with jumps in [A,B]? That is equivalent to: can we write N - x as a sum of numbers in [A,B]? This is a known problem: given A, B, can we represent D as sum of numbers in [A,B]? Since A,B are small, we can precompute the set of reachable distances up to some bound, or use DP. But the BFS already explores positions up to limit, so any x > last_bad_R that is visited is <= limit = last_bad_R + B. So x is at most B past the last bad square. From there, if we can jump again, we can reach up to x + B, but there are no bad squares, so we could just continue. However, the BFS limit is last_bad_R + B, so if we don't reach N, we fail. But is that correct? Let's test with a simple case: N=10, A=2, B=3, no bad squares. BFS limit = min(10, 0+3) = 3? Actually last_bad_R is 0 (none). limit = N = 10? The rule is: if there are no bad squares, we can just check if N-1 is reachable. The BFS from 1 with jumps [2,3] can reach: 1->3,4,5, then from 3->5,6,7, etc. The BFS will explore up to N-1? Actually with no bad squares, the BFS would explore all positions up to N-1, because there are no bad squares to prune. But that's O(N) which is too large for N=10^12. So we cannot just BFS up to N.
11. So the BFS limit must be something like: the farthest point we need to consider is the end of the last bad interval + B, or the start of the last bad interval + something. Actually the standard solution for this problem (I recall it's AtCoder ABC 174 F? No, ABC 195? Let me think: The problem is "Bad Squares" or "Jumping Takahashi 2"? Actually it's "AtCoder Beginner Contest 161 - F"? No.
12. Let me derive the correct limit. The key observation: Once we are past all bad squares, the problem becomes "can we reach N from current position using jumps of [A,B] with no obstacles". This is equivalent to: is N - x in the set of numbers that can be formed as sum of numbers in [A,B]? Since A,B are small, the set of representable numbers has bounded gaps after some point. Specifically, by the Chicken McNugget theorem, for coprime A,B, all numbers >= (A-1)*(B-1) are representable. For non-coprime, multiples of gcd. But more generally, the set of representable numbers eventually becomes periodic with period gcd(A,B)? Actually the set of sums of [A,B] is a semigroup. Its complement (gaps) is finite. The maximum gap is bounded by something like A*B. So we can precompute the reachable distances from 0 using BFS up to some bound (e.g., A*B), and then for any larger D, we can check if D is reachable by seeing if D is in the set, or if D - k*g is in the set for some k? Actually, we can just precompute the set of all representable numbers up to, say, 2*A*B. Then for any D, we can check if there exists some t such that D - t is in that set? Not exactly.
13. But in this problem, the known solution uses a BFS over positions modulo something, or BFS on a graph where nodes are positions, but we limit the BFS to positions up to the end of the last bad interval + B. Let me check: If we BFS only up to last_bad_R + B, then we only consider positions that are at most B past the last bad square. From there, we can try to jump further. But since there are no bad squares, we can just check if N is within a few jumps. However, the BFS might not reach a position close enough to N if the gap is large. For example, N=100, last bad square at 80, A=10, B=20. BFS limit = 80+20=100. So we consider positions up to 100. That's fine. But what if N=1000, last bad at 80, A=10, B=20. BFS limit = 100. We might reach 95, but not 100. From 95, we can jump to 105, but 105 > limit, so we wouldn't explore. But we need to check if we can reach N=1000 from 95. Since there are no bad squares, we can just check if 1000-95 is reachable by jumps. But we didn't explore that because we stopped at 100. So the BFS limit cannot be just last_bad_R + B. We need a different approach.
14. Let me recall the actual known solution. This problem is AtCoder ABC 195 D? No. Searching memory: "There are N squares arranged in a row... bad if exists i... L_i <= j <= R_i... jump A <= i <= B... reach N". This is AtCoder ABC 161? No, ABC 161 is "Lunlun Number". ABC 174 is "Repsept". ABC 195 is "Shipping Center". 
15. Wait, I think this is AtCoder ABC 196 F? No. Let me think of the constraints: N up to 10^12, M up to 2e4, A,B up to 20. This is AtCoder ABC 200 D? No, that's about subset sums. 
16. Actually, this is "AtCoder Beginner Contest 174 - F"? No. 
17. I recall a problem: "Jumping Takahashi" with bad squares. It's from AtCoder Regular Contest? Or maybe it's "ABC 196 - D"? No.
18. Let me search my internal database: The problem is "AtCoder ABC 161 - F"? No. 
19. Actually, I think it's "AtCoder Beginner Contest 195 - F"? No. 
20. Wait, I remember a solution: We use BFS/DFS but we only need to explore positions up to the end of the last bad interval + B, BUT we also consider the "state" of being past the last bad interval. More precisely, the BFS explores positions, but to avoid infinite loops, we only keep positions that are less than or equal to the left endpoint of the next bad interval? No.
21. Let me think differently. Since the bad intervals are sorted and non-overlapping, we can process them one by one. For each bad interval, we can determine the set of positions from which we can jump over it. The standard approach is to consider the "gaps" between bad intervals. The problem reduces to: can we traverse from 1 to N by jumping over gaps. But the jumps are of length at most B, so we need to cross each gap. Actually, the path can go through the gaps, but we cannot step on bad squares. So we need to jump from a good square to another good square. This is like a graph where good squares are nodes, and edges exist if the distance is in [A,B]. We want to know if 1 and N are connected.
22. Since M is up to 20000 and B is small, we can compress the good intervals. The good intervals are: [1, L_1-1], [R_1+1, L_2-1], ..., [R_M+1, N]. Note that R_M < N, so there is a last good interval. We can perform BFS on these intervals. For each good interval, we need to know which positions in it are reachable. But positions within a good interval of length L can be reached if there is some position in the previous good interval that can jump to it. However, the number of positions is large.
23. The key insight: Since B is small, we only need to keep track of positions modulo some value? Actually, the classic solution for this problem (I am now recalling) uses a BFS on the "distance" from the left, but with a trick: we only keep positions that are less than the start of the next bad interval plus B. More specifically, we maintain a set of reachable positions, but we limit the BFS to positions up to the current "frontier". The algorithm is:
   - Let bad intervals be I_1, ..., I_M.
   - We process from left to right.
   - Maintain a set of reachable positions that are less than or equal to the current "maximum" we care about.
   - The maximum is the right endpoint of the current bad interval + B.
   - For each bad interval [L,R], we consider the reachable positions up to R+B.
   - We try to jump from those positions to land on or past L, but before or on R+B.
   - Actually, the BFS explores all reachable positions, but we only keep those that are at most R_i + B for the i-th bad interval? Or something like that.
24. Let me search for the exact algorithm. I remember a problem "AtCoder ABC 195 F" is about BFS with obstacles. No.
25. Actually, I think this problem is "AtCoder Beginner Contest 174 F" is "Range Set Query". Not this.
26. Wait, I recall a problem "Jumping Takahashi 2" or "Bad Squares" from AtCoder. The constraints N up to 10^12, M up to 2e4, A,B <= 20. The solution: BFS from 1, but using a set of "positions modulo (A+B)"? No.
27. Let's reason from scratch. We have a line of squares. Bad squares are blocked. We start at 1 (which is good because L_i > 1). We want to reach N (which is good because R_i < N). At each step, from a good square x, we can jump to x+i for i in [A,B] provided x+i is good and <= N. This is a standard BFS on an implicit graph. The graph has up to N nodes, but N is huge. However, the bad squares only block M intervals. The good squares form M+1 intervals. Let's denote them:
   - G_0 = [1, L_1 - 1]
   - G_1 = [R_1 + 1, L_2 - 1]
   - ...
   - G_M = [R_M + 1, N]
   Note that G_0 and G_M are non-empty because L_1 > 1 and R_M < N.
   We need to traverse from 1 to N through these good intervals using jumps of length in [A,B].
   A jump from a good interval G_i to G_j (j > i) lands in G_j if the distance d from the start of G_i to the end point is such that the landing point is in G_j. Actually, it's easier to think: we are at some position x in G_i. We can jump to x+i for i in [A,B]. We want x+i to be in some good interval. If x+i lands in a bad interval, it's invalid.
   The graph is essentially: each good interval is a set of positions. From a position in G_i, we can reach positions in G_{i+1}, G_{i+2}, etc., as long as the jump length is in [A,B].
   Since B is small, the number of good intervals we can "skip" in one jump is bounded. Actually, a jump of length at most B cannot skip a bad interval that is longer than B? No, a bad interval can be long, but we cannot land inside it. So if we are in G_i, and the next bad interval is long, we might not be able to jump over it if the required jump length is larger than B? But we can also use multiple jumps. So we can traverse a bad interval by jumping from a position in G_i to a position in G_{i+1}? Wait, G_i and G_{i+1} are separated by a bad interval. So to get from G_i to G_{i+1}, we must make a jump that lands in G_{i+1}. The distance from a position in G_i to a position in G_{i+1} is at least (R_i+1) - (L_{i+1}-1) = R_i - L_{i+1} + 2, which is the gap between the bad intervals. Actually, the bad intervals are separated by at least 1 (since R_i < L_{i+1}), so the gap between G_i and G_{i+1} is just 1? Wait: G_i ends at L_{i+1}-1, and G_{i+1} starts at R_i+1. The distance from the end of G_i to the start of G_{i+1} is (R_i+1) - (L_{i+1}-1) = R_i - L_{i+1} + 2. Since R_i < L_{i+1}, this is at most 1? Actually, if R_i = 5, L_{i+1} = 6, then distance = 5+1 - (6-1) = 1. So the bad intervals are adjacent? The condition is R_i < L_{i+1}, so they are strictly separated. The gap between G_i and G_{i+1} is actually 0? Let's define: bad intervals are [L_1,R_1], [L_2,R_2], ... with R_1 < L_2. So between R_1 and L_2, there is a gap. The good squares are squares not in any bad interval. So G_0 = [1, L_1-1]. G_1 = [R_1+1, L_2-1]. G_2 = [R_2+1, L_3-1], etc. So G_1 is the gap between bad interval 1 and 2. G_0 is from 1 to L_1-1. So G_0 and G_1 are separated by bad interval 1. To get from G_0 to G_1, you must jump from a position in G_0 to a position in G_1. The distance from a position x in G_0 to a position y in G_1 is y - x. Since x <= L_1-1 and y >= R_1+1, the minimum distance is (R_1+1) - (L_1-1) = R_1 - L_1 + 2. This could be large if the bad interval is long? No, R_1 - L_1 is the length of the bad interval minus 1. So the minimum distance to cross a bad interval is (R_1 - L_1) + 2. If the bad interval is long, this minimum distance is large. But we can only jump up to B. So if a bad interval is longer than B-1, we might not be able to cross it in one jump? Wait, we don't need to cross the bad interval in one jump. We are in G_0, we jump to somewhere. If we jump to a position in G_0 (i.e., still before the bad interval), that's fine. But to eventually get to G_1, we need to land in G_1. We can make multiple jumps within G_0, then eventually jump to G_1. But the jump that lands in G_1 must have length in [A,B]. So we need a position x in G_0 such that x + i is in G_1 for some i in [A,B]. That is, there exists x in G_0 and i in [A,B] such that R_1+1 <= x+i <= L_2-1. This is possible if the intervals [x+A, x+B] intersect G_1. Since we can choose x in G_0, we need that the union of [x+A, x+B] for x in G_0 intersects G_1. This is a condition on the gap between G_0 and G_1.
   More generally, from a good interval G, we can reach a set of positions in the next good intervals. Since B is small, we can do a BFS over the "good intervals" and track reachable positions at the boundaries.
   But there is a more efficient way: because B is small, we can track the set of reachable positions modulo some value? Actually, the standard solution for this problem is to use a BFS/DFS where we only consider positions up to the right endpoint of the current bad interval + B. The idea is that once we are past a bad interval, we don't need to keep positions that are too far behind. Specifically, we process the bad intervals in order, and for each bad interval, we determine which positions in the next good interval are reachable. But we cap the positions we keep to be within a window of size B from the left end of the next good interval? No.
28. Let me recall the exact solution from memory. I remember reading an editorial for a problem like this. The trick is: BFS on positions, but we only need to explore positions up to the end of the last bad interval + B. Because if we can reach a position x that is greater than the end of the last bad interval, we can just check if N is reachable from x by a simple greedy or DP since there are no obstacles. But as I thought earlier, if N is far, we might not be able to tell. However, the editorial says: we only need to explore positions up to the end of the last bad interval + B. Wait, but that would mean if N is very large, we only explore up to R_M + B, and if we don't reach N, we output No. But is that correct? Let's test: N=100, A=1, B=2, no bad squares. R_M = 0, so limit = 2. BFS from 1: reach 2,3. From 2 reach 3,4. But we only explore up to 2? So we would output No, but actually we can reach 100. So the limit cannot be just R_M + B. There must be something else.
29. Actually, if there are no bad squares, the problem is trivial: can we reach N from 1 with jumps in [A,B]? That's possible if and only if N-1 can be expressed as a sum of numbers in [A,B]. Since A,B <= 20, we can precompute the reachable distances. But the BFS approach for the general case must handle the no-bad-squares case.
30. The correct limit for BFS is: the maximum position we need to consider is the right endpoint of the last bad interval, but we also need to consider the possibility of jumping from the last good interval to N. Actually, the BFS should explore all positions that could be the "landing" point after crossing a bad interval. The known solution: BFS on the graph where nodes are positions, but we only keep positions that are less than the left endpoint of the next bad interval plus B? No.
31. Let me think about the state. Since the bad intervals are sorted, we can process them one by one. For each bad interval, we want to know which positions in the next good interval are reachable. To compute that, we need to know which positions in the current good interval are reachable, and then for each such position, we can jump to positions in the next good interval. The next good interval might be far, but the jump length is bounded by B. So from a position x, we can only reach positions in [x+A, x+B]. So if we are in good interval G_i, we can only reach positions in G_{i+1} that are within B of some reachable x in G_i. But G_i might be long, so there could be many reachable x. However, we don't need to keep all of them. We only need to keep the "frontier" of reachable positions that are close to the next bad interval. Specifically, to cross a bad interval of length L, we need to jump from a position x in G_i to a position y in G_{i+1} such that y - x in [A,B]. The set of such x is those with y - B <= x <= y - A. Since we want to know if there exists any y in G_{i+1} reachable, we can just keep the reachable positions in G_i that are within B of the end of G_i? Actually, if we keep all reachable positions in G_i, the number could be large. But we can compress: since B is small, the pattern of reachable positions in a long good interval might be periodic or we can just keep a set of "gaps" from the end.
32. There is a known solution: BFS on the "distance" from the start of the current good interval, but we only need to keep positions that are less than the left endpoint of the next bad interval plus something. Let me search my memory for "AtCoder Bad Squares" or "Jumping Takahashi". I think it's "AtCoder Beginner Contest 195 F"? No.
33. Wait, I think it's "AtCoder ABC 161 F" is about division. 
34. Let's consider the problem as: we have a set of bad intervals. We start at 1. We can jump [A,B]. We want to reach N. This is exactly the problem "AtCoder ABC 174 F"? No, that's about ranges.
35. I recall a problem: "Squares" or "Bad Squares" from AtCoder. The constraints match: N up to 10^12, M up to 2e4, A,B <= 20. It's from AtCoder Regular Contest? Actually, I think it's "AtCoder Beginner Contest 196 D"? No.
36. Let me try to reconstruct the solution logically. We have bad intervals. We can think of the line as having "good segments". The last good segment is [R_M+1, N]. We need to determine if we can reach N from the start. We can do a BFS from 1, but we cap the maximum position we push into the queue. What is the cap? The cap should be: the rightmost point we need to consider is the right endpoint of the last bad interval plus B, but only if we are not past it. Actually, if we can reach a position x that is <= R_M + B, we can then try to jump from x to some y in the last good segment. But if the last good segment is very long, we might need to make multiple jumps within it. However, since there are no bad squares in the last good segment, we can just check if we can reach N from any reachable x in the last good segment. But we might not have explored all reachable x in the last good segment because we capped at R_M + B. So we need a different approach for the last good segment.
37. Perhaps the BFS should explore up to the end of the last good segment? But that's N, which is huge. So we cannot.
38. The key is: once we are in the last good segment (or any good segment with no bad squares ahead), the problem becomes a simple reachability with no obstacles. For a line with no obstacles, we can reach N from x if and only if the remaining distance D = N - x can be expressed as a sum of numbers in [A,B]. Since A,B <= 20, we can precompute the set of all representable numbers up to some bound, and then for any D, we can check if D is representable by seeing if D mod gcd(A,B) is 0 and D is large enough? But A,B are not necessarily coprime. However, we can just do a BFS on the distances modulo some number. Actually, for a given A,B, the set of representable numbers is eventually periodic with period g = gcd(A,B). The maximum gap is bounded by something like A*B/g. So we can precompute the set of all representable numbers up to, say, A*B. Then for any D, we can check if there exists some t in [0, A*B] such that D - t is representable? Not exactly.
39. A standard method: We can BFS on the state (position) but we only keep positions that are within B of the end of the current "block". Actually, the problem can be solved by considering the "gaps" between bad intervals. We can jump from one good interval to another. The graph of good intervals is small (M+1). For each pair of good intervals, we can determine if there is a jump from some position in the first to some position in the second. Since the good intervals can be long, we need to know if there is a position in the first such that a jump of length in [A,B] lands in the second. This is a condition on the intervals. But we also need to consider that we can make multiple jumps within a good interval. So the reachable set in a good interval might be everything, or it might be constrained.
40. Because B is small, we can do a BFS on the "positions modulo some value" but that seems complicated.
41. Let me look for the actual problem. I'm almost certain this is "AtCoder Beginner Contest 195 F"? No. 
42. Wait, I remember: "AtCoder Beginner Contest 200 D" is about subset sums. 
43. I think it's "AtCoder Beginner Contest 174 F" is "Range Set Query". 
44. Let me try to search my memory for the exact problem statement: "There are N squares arranged in a row, labeled 1, 2, ..., N from left to right. You are given M pairs of integers (L_1, R_1), ..., (L_M, R_M). A square j is defined to be bad if and only if there exists some i such that L_i <= j <= R_i. Determine whether you can move from square 1 to square N by repeatedly performing the following action: Let your current square be x. Choose an integer i that satisfies all of the following conditions, and move to square x + i: A <= i <= B, x + i <= N, Square x + i is not bad." This is exactly "AtCoder Beginner Contest 195 F"? No, F is usually a hard problem. 
45. Actually, I think it's "AtCoder Beginner Contest 196 D" is "Hanjo". 
46. I recall a problem "Bad Squares" from AtCoder. It might be "AtCoder Regular Contest 108" or something. 
47. Let me think of the solution. I remember reading an editorial that said: We can BFS from 1, but we only need to keep positions that are less than the left endpoint of the next bad interval plus B. More precisely, we maintain a set of "frontier" positions. We process the bad intervals from left to right. For each bad interval [L,R], we consider the positions in the good interval before it. We want to know which positions in the good interval after it are reachable. To do this, we can BFS within the good interval, but we only need to keep positions that are at most R + B? No.
48. Another approach: Since the jumps are small, we can model the problem as a graph where the vertices are the "good intervals" and the edges represent possible jumps. But we also need to know the exact positions. However, because B is small, the exact positions only matter up to a window of size B. So we can compress the state by keeping the set of reachable positions modulo some number, but the number might be the lcm of something.
49. Let's consider the infinite line version. If there were no bad squares, the reachable set from 1 is 1 + S, where S is the set of sums of [A,B]. S is a semigroup. The complement of S is finite. So for large enough D, D is in S iff D mod g is 0 (or something). But here we have obstacles.
50. The known solution for this problem uses a BFS on the "distance" from the start, but with a limit of B past each bad interval. Actually, I found a recollection: The solution is to BFS on the positions, but we only push positions that are less than the right endpoint of the current bad interval + B. We also process the "gaps" between bad intervals. Specifically, we maintain a set of reachable positions. We iterate through the bad intervals. For each bad interval, we take the reachable positions that are before it, and we try to jump over it. The positions we can land on are within B of the bad interval's right endpoint. So we only need to keep those positions. After processing all bad intervals, we have a set of reachable positions in the last good interval. Then we check if N is reachable from any of them using a simple BFS/DP on the remaining distance without obstacles.
51. Let's formalize: We have bad intervals I_1, I_2, ..., I_M. Let the good intervals be G_0 = [1, L_1-1], G_1 = [R_1+1, L_2-1], ..., G_M = [R_M+1, N]. Note that G_M is the last.
   We start with reachable set S_0 = {1} (which is in G_0, since L_1 > 1).
   For k = 1 to M:
     We want to find the reachable positions in G_k (and maybe beyond) after crossing the first k bad intervals.
     To do this, we can BFS within G_k starting from positions that can be reached by jumping from S_{k-1}? But S_{k-1} contains positions in G_{k-1}. We need to jump from G_{k-1} to G_k. A jump from x in G_{k-1} to y in G_k is valid if y - x in [A,B] and y in G_k.
     So for each x in S_{k-1}, the reachable y in G_k are those in [x+A, x+B] intersect G_k.
     Then from those y, we can also make jumps within G_k. So we can BFS within G_k. But G_k could be long. However, we only need to keep track of positions in G_k that are "useful" for the next step. The next bad interval is I_{k+1} (if k < M) or the end is N. To cross I_{k+1}, we need to jump from G_k to G_{k+1}. The jump must land in G_{k+1}. So we need positions in G_k that are close enough to G_{k+1} such that a jump of length in [A,B] can reach G_{k+1}. The maximum distance from a position in G_k to G_{k+1} is if we are at the left end of G_k. The minimum distance to G_{k+1} is (R_k+1) - (left of G_k). But we can only jump up to B. So only positions in G_k that are within B of G_{k+1} can jump to G_{k+1}. Specifically, we need x in G_k such that x + B >= R_k+1 (the start of G_{k+1}). So x >= R_k+1 - B. So we only need to keep reachable positions in G_k that are in the rightmost part: [max(L_{k+1} - B, R_k+1), L_{k+1}-1]? Wait, G_k is [R_{k-1}+1, L_k-1] for k>=1. For k=0, G_0 is [1, L_1-1]. The next good interval is G_1 = [R_1+1, L_2-1]. To jump from G_0 to G_1, we need x in G_0 such that x+i in G_1. The smallest i is A, largest is B. So x must be at most L_2-1 - A. Also x must be at least (R_1+1) - B. So the useful x in G_0 are in [max(1, R_1+1-B), min(L_1-1, L_2-1-A)]. So we only need to keep reachable positions in that subrange.
   In general, to jump from G_k to G_{k+1}, we need x in G_k such that x+A <= L_{k+1}-1 and x+B >= R_k+1. So x in [R_k+1 - B, L_{k+1} - 1 - A] intersect G_k. So the "useful" part of G_k is the intersection of G_k with that interval. The length of this useful part is at most B - A + something? Actually, it could be up to B - A + 1? Not exactly, but it's bounded by B - A + (L_{k+1} - R_k - 1). But L_{k+1} - R_k - 1 is the length of G_{k+1}? No, L_{k+1} - 1 is the end of G_k, and R_k+1 is the start of G_{k+1}. So the gap between G_k and G_{k+1} is 0? They are adjacent in terms of the line, but there is a bad interval between them. The distance from the end of G_k (L_{k+1}-1) to the start of G_{k+1} (R_k+1) is (R_k+1) - (L_{k+1}-1) = R_k - L_{k+1} + 2. Since R_k < L_{k+1}, this distance is at least 2? Actually, if R_k = L_{k+1} - 1, then the bad intervals are adjacent, so there is no good square between them. But the problem says R_i < L_{i+1}, so there is at least one integer between them? No, if R_i = 5 and L_{i+1} = 6, then the integer 6 is L_{i+1}, so there is no good square between them? Actually, bad squares are [5,5] and [6,6]? But then square 6 is bad. So the good squares are ...4, then 7... So the gap between G_k and G_{k+1} is not necessarily non-empty. The good intervals are defined as the sets of squares not in any bad interval. Since the bad intervals are disjoint and sorted, the good intervals are the complement. So between R_k and L_{k+1}, there might be good squares. Specifically, G_k ends at L_{k+1}-1, and G_{k+1} starts at R_k+1. Since R_k < L_{k+1}, we have R_k+1 <= L_{k+1}. So the intervals [R_k+1, L_{k+1}-1] are the good squares between the bad intervals. That is exactly G_k? Wait, careful: G_0 = [1, L_1-1]. G_1 = [R_1+1, L_2-1]. So the good squares between bad interval 1 and 2 are G_1. The bad intervals are [L_1,R_1] and [L_2,R_2]. So G_1 is the gap between them. So G_0 is before the first bad interval. G_1 is between first and second. So for k>=1, G_k is between bad interval k and k+1. G_0 is before the first. G_M is after the last.
   So to jump from G_k to G_{k+1}, we are jumping over bad interval k+1? Actually, from G_0 to G_1, we jump over bad interval 1. From G_1 to G_2, we jump over bad interval 2. In general, from G_{k-1} to G_k, we jump over bad interval k. So when we are at G_k, we have already crossed bad intervals 1..k. The next bad interval to cross is k+1 (if k < M). To cross bad interval k+1, we need to jump from G_k to G_{k+1}. The distance from a position x in G_k to a position y in G_{k+1} is y - x. We need y - x in [A,B]. So x must be in [y - B, y - A]. The smallest y is the start of G_{k+1} = R_k+1. The largest y is the end of G_{k+1} = L_{k+2}-1 (for k < M-1) or N (for k=M-1). So the useful x in G_k are those that can reach some y in G_{k+1}. That is, x in G_k such that there exists y in G_{k+1} with y - x in [A,B]. This is equivalent to x in G_k intersect [ (R_k+1) - B, (L_{k+2}-1) - A ] (for k < M-1). For the last step, it's [ (R_M+1) - B, N - A ].
   So the "frontier" of G_k that can reach the next good interval is the set of x in G_k that are close enough to the next bad interval. Specifically, we only need to keep reachable positions in G_k that are at most B away from the start of G_{k+1} (i.e., x >= R_k+1 - B) and at most A away from the end of G_{k+1}? Not exactly. But the key is that the number of such x is small because the length of the interval [R_k+1 - B, L_{k+1}-1 - A] is at most B - A + 1? Let's compute: The interval is [R_k+1-B, L_{k+1}-1-A]. The length is (L_{k+1}-1-A) - (R_k+1-B) + 1 = L_{k+1} - R_k - 2 - A + B. Since L_{k+1} - R_k - 1 is the length of the good interval G_{k+1} minus 1? Actually, G_{k+1} is [R_k+1, L_{k+1}-1]? Wait, for k+1, the good interval is G_{k+1} = [R_k+1, L_{k+2}-1]? No, careful: G_1 = [R_1+1, L_2-1]. So for general i, G_i = [R_{i-1}+1, L_i-1] for i=1..M, and G_0 = [1, L_1-1], G_M = [R_M+1, N]. So G_{k+1} = [R_k+1, L_{k+2}-1] (for k=0..M-2). The useful x in G_k are those that can reach G_{k+1}. They must satisfy: there exists y in [R_k+1, L_{k+2}-1] such that y - x in [A,B]. This means x in [ (R_k+1) - B, (L_{k+2}-1) - A ] intersect G_k. Since G_k = [R_{k-1}+1, L_k-1] (for k>=1), the intersection is [max(R_{k-1}+1, R_k+1-B), min(L_k-1, L_{k+2}-1-A)]. The length of this intersection is at most B - A + 1? Not necessarily, because L_{k+2}-1-A could be much larger than L_k-1. But we are intersecting with G_k, so the upper bound is L_k-1. So the upper bound is min(L_k-1, L_{k+2}-1-A). The lower bound is max(R_{k-1}+1, R_k+1-B). So the length is at most (L_k-1) - (R_k+1-B) + 1 = L_k - R_k - 2 + B. This could be large if L_k - R_k is large. But L_k - R_k is the length of bad interval k? Actually, bad interval k is [L_k, R_k]. So L_k - R_k is negative or zero? L_k <= R_k, so L_k - R_k <= 0. So L_k - R_k - 2 is negative. So the length is at most B - (R_k - L_k) - 2? Wait: L_k - R_k is <= 0, so L_k - R_k - 2 is <= -2. So the length is at most B - 2? That seems too small. Let's plug numbers: Suppose bad intervals are short. Then L_k and R_k are close. For example, bad interval k is [10,10]. Then L_k=10, R_k=10. Then L_k - R_k - 2 = -2. So length <= B - 2. If B=5, length <= 3. That seems plausible. If bad interval k is long, say [10,20], then L_k=10, R_k=20. Then L_k - R_k = -10. So L_k - R_k - 2 = -12. Length <= B - 12, which is negative. So in that case, there are no x in G_k that can reach G_{k+1} in one jump. But we can still cross by making multiple jumps within G_k? No, G_k is before the bad interval. To cross a long bad interval, we need to jump from G_k to G_{k+1} in one jump? Not necessarily. We can jump from G_k to somewhere in G_k? But G_k is before the bad interval. The bad interval is [L_k, R_k]. G_k ends at L_k-1. So to get to G_{k+1}, which starts at R_k+1, we must cross the bad interval. We can only cross it by jumping from a position in G_k to a position in G_{k+1}. There are no other good squares in between. So we must make a jump that lands in G_{k+1}. So the distance must be in [A,B]. So if the gap between G_k and G_{k+1} is too large, we cannot cross in one jump. But wait, the gap is (R_k+1) - (L_k-1) = R_k - L_k + 2. If this gap is > B, then we cannot cross because the minimum jump is A, but A could be small? Actually, if the gap is > B, then any jump from G_k will fall into the bad interval or before G_{k+1}. So we cannot cross. So for a long bad interval, it might be impossible to cross. So the useful x in G_k are those that can jump to G_{k+1}. The distance from x to G_{k+1} is y - x. The minimum distance is (R_k+1) - x. So we need (R_k+1) - x <= B, i.e., x >= R_k+1 - B. Also the maximum distance to G_{k+1} is (L_{k+2}-1) - x. We need that to be >= A, i.e., x <= L_{k+2}-1 - A. So the useful x are in [R_k+1-B, L_{k+2}-1-A] intersect G_k. The length of this interval is (L_{k+2}-1-A) - (R_k+1-B) + 1 = L_{k+2} - R_k - 2 - A + B. This can be large if L_{k+2} is large. But we also intersect with G_k, so the upper bound is L_k-1. So the length is at most (L_k-1) - (R_k+1-B) + 1 = L_k - R_k - 1 + B. Since L_k <= R_k, L_k - R_k - 1 <= -1. So the length is at most B - 1. Actually, L_k - R_k - 1 is negative (or zero if L_k = R_k+1, but L_k <= R_k, so L_k - R_k - 1 <= -1). So the length is at most B - 1. So the number of useful positions in G_k is at most B. That's the key! Because we only need to consider positions in G_k that are within B of the start of G_{k+1} (i.e., x >= R_k+1-B) and also within G_k (x <= L_k-1). Since R_k+1-B might be less than the start of G_k, the number of such x is at most B. So we can represent the reachable set in the "frontier" of G_k as a set of offsets from the right end of G_k or something.
   So the algorithm is: We process the good intervals from left to right. For each good interval G_k, we maintain a set of reachable positions within G_k that are "useful" for crossing the next bad interval. But we also need to know the reachable positions within G_k to compute the useful ones. However, since we only care about positions that can lead to a jump to the next good interval, we can just keep a sliding window of reachable positions at the right end of G_k. Actually, we can do a BFS within G_k, but we only need to keep positions that are within B of the right end of G_k? Not exactly.
   Let's think: We start at 1 in G_0. We want to cross bad interval 1 to get to G_1. To do that, we need to reach a position in G_0 that is within B of G_1. So we need to know which positions in G_0 are reachable. But G_0 can be long. However, we only need to know the reachable positions in the rightmost part of G_0: specifically, in [L_1 - B, L_1 - 1]? Wait, G_0 is [1, L_1-1]. The next good interval G_1 starts at R_1+1. To jump from G_0 to G_1, we need x in G_0 such that x+B >= R_1+1, i.e., x >= R_1+1-B. Also we need x+A <= L_2-1 (the end of G_1). So x <= L_2-1-A. But since we are only considering x in G_0, x <= L_1-1. So the useful x are in [max(1, R_1+1-B), min(L_1-1, L_2-1-A)]. The number of such x is at most B. So we only need to determine which of these x are reachable from 1 using jumps in [A,B] within G_0. But G_0 is just a line with no bad squares. So we can reach x from 1 if and only if x-1 is in S, the set of sums of [A,B]. So we can precompute S up to some bound, but here x is small (within B of something). Actually, the length of G_0 could be huge, but we only care about the reachable positions in that specific window of size at most B. So we can just simulate the BFS within that window. Since the window is small, we can just try all possible x in that window and check if they are reachable from 1 by a BFS that only explores positions in G_0. But G_0 can be long, so a BFS from 1 to x might be long. However, since there are no bad squares in G_0, the reachable set from 1 in G_0 is exactly 1 + S intersect G_0. So we can just check if x-1 is in S. But S is the set of all numbers representable as sum of [A,B]. Since A,B <= 20, we can precompute S up to a certain bound, say 400. Then for any x, if x-1 > 400, we can determine if it's in S by checking periodicity. But actually, the maximum gap in S is bounded by A*B. So if we precompute S up to A*B, we can determine for any D if D is in S by checking if D mod g is in some set? Not exactly. But we can just do a BFS on the set of distances modulo something. However, since we only need to check for x in a small window, we can just iterate from the start of the window backwards and see if we can land there.
   Actually, a simpler approach: Since the window is small, we can just BFS from 1, but we stop when we either reach the window or determine we can't. But 1 might be far from the window. However, we can jump in [A,B]. So we can reach positions in the window if the distance from 1 to the window is representable. But we also have bad squares? No, G_0 has no bad squares. So it's just a matter of whether we can reach that position. But we can also overshoot? No, we want to land exactly on a position in the window. So we need to check if there is a path of jumps in [A,B] from 1 to x. This is equivalent to: is x-1 in the semigroup generated by [A,B]? Since A,B are small, we can precompute the set of all possible distances up to some large number, or use a BFS modulo g. But we have multiple such checks (one for each good interval). So we need an efficient way to check if a given D is representable.
   However, note that the window size is at most B. And the distance from the start of G_k to the window might be large. But we can do a BFS on the "state" of the reachable positions in the current good interval, but we only keep positions that are within B of the right end? Actually, the standard solution for this problem is to BFS on the positions, but we only push positions that are at most the right endpoint of the current bad interval + B. And we process the bad intervals in order. Let's try to reconstruct that.
   We have bad intervals. We want to know if we can reach N. We can do a BFS from 1, but we maintain a set of reachable positions. However, we cannot keep all positions because N is huge. The trick is that we only need to keep positions that are "close" to the end of the next bad interval. Specifically, we can process the bad intervals one by one. For each bad interval, we consider the reachable positions that are before it. We try to jump over it. The positions we can land on are within B of the bad interval's right endpoint. So we only need to keep those positions. Then we move to the next bad interval. After processing all bad intervals, we have a set of reachable positions in the last good interval. Then we check if we can reach N from any of them using a simple BFS/DP without obstacles.
   Let's define: For each bad interval I_i = [L_i, R_i], we want to compute the set of reachable positions in the good interval after it, but only those that are useful for the next bad interval. Actually, we can compute the set of reachable positions in the entire good interval G_i, but we only need to keep the ones that are within B of the right end of G_i? No.
   Let me look for the exact algorithm. I remember a solution: BFS on the graph where nodes are the "good intervals" and we keep a set of "reachable offsets" from the right end of each good interval. Since the jumps are small, the reachable set in a good interval can be described by a set of distances from the right end. Specifically, if we know which positions in the last B positions of a good interval are reachable, we can compute which positions in the next good interval are reachable. Because from a position x in the current good interval, we can jump to x+i. The landing position y in the next good interval will satisfy y - x in [A,B]. So y = x + i. The set of y we can reach is the union over x in reachable set of [x+A, x+B] intersect next good interval. Since the next good interval starts at some point, we can just compute the new reachable set as a set of positions. But we need to bound the size of this set. The new reachable set might be up to the size of the next good interval, which could be large. However, we only need to keep positions that are close to the right end of the next good interval, because those are the ones that can reach further. Actually, to cross the next bad interval, we need to be within B of its start. So we only need to keep positions in the next good interval that are at least (start of next good interval) - B. So the size of the set we keep is at most B. So we can represent the state as a bitmask of length B (or less) indicating which of the last B positions of the current good interval are reachable.
   Let's formalize: We process the good intervals in order. For G_0, we start with position 1. We need to determine which positions in the rightmost part of G_0 (within B of L_1-1) are reachable. But we can compute the reachable set in G_0 by doing a BFS from 1, but we only care about positions in [L_1-B, L_1-1]? Actually, to jump to G_1, we need x in G_0 such that x >= R_1+1-B. Since R_1+1 is the start of G_1, and R_1 < L_1? Not necessarily. R_1 can be greater than L_1. But G_0 ends at L_1-1. So R_1+1-B could be less than L_1-1. So the useful x are in [max(1, R_1+1-B), L_1-1]. The length of this interval is at most B. So we only need to know which of these x are reachable. We can compute this by BFS from 1, but we can stop when we either reach these positions or determine they are unreachable. However, BFS from 1 might be long. But we can use the fact that G_0 has no bad squares, so we can just check if each such x is reachable by checking if x-1 is in the semigroup. But we can also do a BFS on the "distance" modulo something. Since A,B are small, we can precompute the reachable distances up to a certain bound. But maybe it's easier: since the window is small, we can just iterate from the rightmost useful position leftwards and see if we can reach it by a jump from somewhere in the window? That seems messy.
   Actually, the BFS can be done on the fly: we start from 1, and we do a BFS, but we only push positions that are <= some limit. The limit is the right endpoint of the current bad interval + B. We process the bad intervals in order. For each bad interval, we run a BFS from the current set of reachable positions, but we only explore positions up to R_i + B. Then we take the reachable positions that are in the good interval after the bad interval, and we set them as the new starting points for the next bad interval. And we continue. This way, the BFS never explores too far. At the end, we have reachable positions in the last good interval, and we check if N is reachable.
   Let's test this idea with an example. Suppose N=100, bad interval [20,30], A=1, B=2. Start: reachable {1}. Bad interval 1: R_1=30. Limit = 30+2=32. BFS from 1 with limit 32. We can reach all positions up to 32 (since no bad squares yet). So reachable up to 32. Now, the next bad interval? There is only one. So after processing all bad intervals, we have reachable positions in the last good interval. The last good interval is [31, 100]. We have reachable positions up to 32. So in the last good interval, we have reachable positions: 31, 32. Then we need to check if we can reach 100 from 31 or 32 with jumps [1,2] and no obstacles. From 32, we can reach any number >= 32? Actually, with jumps 1,2, we can reach any number >= 32+1=33? But we need to check if 100 is reachable. Since we can jump 1 or 2, we can reach any number >= 32 + some threshold. Actually, from 32, we can reach 100 if 100-32 is representable. 68 is representable? Yes, 68 is even, so we can use 34 jumps of 2. So we should output Yes. And indeed, we can go 1->...->32->100.
   Another example: N=100, bad interval [20,80], A=1, B=2. R_1=80. Limit = 82. BFS from 1 up to 82. We can reach all up to 82. But note: the bad interval is [20,80]. So from 1, we can go up to 19 (since 20 is bad). Then from 19, we can jump to 20 or 21, but 20 is bad, so we can only jump to 21. But 21 is still in the bad interval? 21 is between 20 and 80, so it's bad. So actually, we cannot land on 21. So from 19, jumps: 1->20 (bad), 1->21 (bad). So we are stuck at 19. So BFS from 1 with limit 82 would only reach positions that are good. So it would reach 1, then from 1 we can jump to 2,3,... up to 19. From 19, we cannot jump anywhere because 20 and 21 are bad. So reachable set in the limit is {1..19}. Now, the last good interval is [81, 100]. Do we have any reachable positions in it? No, because we didn't reach 81..82. So we output No. And indeed, we cannot cross the long bad interval.
   So the algorithm: We have a global limit. We do a BFS from 1. We only push positions that are <= the right endpoint of the current "processing" bad interval + B. But we need to process the bad intervals in order. Actually, we can just set the limit to the right endpoint of the last bad interval + B? But as we saw, if the last good interval is long, we might not be able to tell if we can reach N. Wait, in the first example, the last good interval was [31,100], and we had reachable positions at 31,32. We then needed to check if N=100 is reachable from them without obstacles. So after the BFS up to the limit, we have a set of reachable positions in the last good interval (specifically, those within the limit). Then we need to check if any of these positions can reach N. Since there are no obstacles from that point on, we can just check if N is reachable from any of those positions using jumps in [A,B]. This is a simple reachability problem on a line without obstacles. We can solve it by checking if the distance D = N - x is representable as a sum of numbers in [A,B]. Since A,B are small, we can precompute the set of representable numbers up to a certain bound, and then for larger D, use periodicity.
   So the steps:
   1. Read N, M, A, B.
   2. Read the M bad intervals. They are sorted and non-overlapping.
   3. If M=0, then we just need to check if N-1 is representable as sum of [A,B]. We can do that separately.
   4. Otherwise, let the bad intervals be [L_1,R_1], ..., [L_M,R_M]. The last good interval is [R_M+1, N]. We will perform a BFS from 1, but we only explore positions up to R_M + B. (We might need to explore a bit more to account for jumps that land exactly on R_M+1? Actually, R_M+1 is the first good square after the last bad interval. To land on it, we need a jump from a position <= R_M+1-B. So the maximum position we need to consider to potentially land on R_M+1 is R_M+1-B + B = R_M+1. So the limit R_M+B is sufficient.)
   5. BFS: Start with a queue containing 1. Maintain a set of visited positions (since positions can be up to 10^12, we cannot use a boolean array, but the number of positions we visit will be small, so we can use a set or a dict). Actually, since the limit is R_M+B, and M is up to 20000, R_M can be up to 10^12. So the limit could be up to 10^12+20. We cannot allocate an array of that size. But we only visit a small number of positions because the graph is sparse. However, the BFS might visit many positions if the good intervals are long. But we are limiting the BFS to positions up to R_M+B. But R_M+B could be huge (up to 10^12). If there are no bad squares, M=0, we skip this and use the no-obstacle method. If there are bad squares, but the good intervals are long, say G_0 is [1, 10^12 - 1], and there is a bad interval at the end? Actually, if M>=1, then R_M < N. The limit is R_M+B. But R_M could be close to N. If the bad intervals are at the end, R_M might be N-1, so limit is N-1+B, which is > N. But we can cap at N. So the limit is min(N, R_M+B). If R_M is close to N, the limit is close to N, so the BFS might explore a lot. But wait, if the bad intervals are at the end, then the good intervals are long. For example, N=10^12, one bad interval [10^12-20, 10^12-1]. Then R_M = 10^12-1, limit = 10^12-1+20 = 10^12+19, capped at N=10^12. So we would BFS from 1 up to 10^12. That's 10^12 operations, impossible. So the BFS cannot simply go up to N. There must be a different limit.
   The key is: we don't need to BFS through the entire long good interval. We only need to know the reachable positions near the end of the good interval. So the BFS should be done in a way that only explores positions that are "close" to the bad intervals. Specifically, we process the good intervals one by one. For each good interval, we only explore the part that is within B of the next bad interval. So the total number of positions explored across all good intervals is O(M*B), which is manageable.
   Let's design the algorithm properly:
   - We have good intervals: G_0, G_1, ..., G_M. (G_0 = [1, L_1-1], G_i = [R_i+1, L_{i+1}-1] for i=1..M-1, G_M = [R_M+1, N].)
   - We start with reachable set S_0 = {1}. Note that 1 is in G_0.
   - For i = 0 to M-1:
       We are in good interval G_i. We want to find the reachable positions in G_{i+1} (or beyond) that can be reached by crossing the bad interval after G_i (which is bad interval i+1? Actually, G_i is followed by bad interval i+1? Wait: G_0 is before bad interval 1. So to go from G_0 to G_1, we cross bad interval 1. So for i=0, we cross bad interval 1. For i=1, we are in G_1, and we cross bad interval 2 to get to G_2. So in general, for i=0..M-1, we cross bad interval i+1.
       We have a set of reachable positions in G_i. We need to expand this to reachable positions in G_{i+1} (and maybe further, but we only need the ones that are useful for the next crossing). Actually, we can just BFS within G_i from the current reachable positions, but we only need to keep positions that are within B of the end of G_i? Or we need to keep positions that can reach G_{i+1}.
       To cross to G_{i+1}, we need to be at a position x in G_i such that x + i in G_{i+1} for some i in [A,B]. So x must be in [ (start of G_{i+1}) - B, (end of G_{i+1}) - A ] intersect G_i. Since we only care about the resulting positions in G_{i+1}, we can just compute the set of reachable positions in G_{i+1} by considering all jumps from the current reachable positions in G_i that land in G_{i+1}. Then, from those new positions, we can also make jumps within G_{i+1} to reach other positions in G_{i+1}. But we only need to keep those new positions that are useful for the next crossing (i.e., within B of the end of G_{i+1}? Actually, to cross the next bad interval, we need to be within B of its start. The next bad interval is i+2 (if i+1 < M). Its start is L_{i+2}? Wait, the bad interval after G_{i+1} is i+2, with start L_{i+2}. So we need to keep positions in G_{i+1} that are >= R_{i+1}+1 - B? Actually, to cross bad interval i+2, we need to jump from G_{i+1} to G_{i+2}. So we need x in G_{i+1} such that x+B >= start of G_{i+2} = R_{i+1}+1? No, G_{i+2} starts at R_{i+1}+1. So we need x >= R_{i+1}+1 - B. So we only need to keep positions in G_{i+1} that are in the rightmost part: [R_{i+1}+1-B, L_{i+2}-1] (intersect G_{i+1}). The length of this interval is at most B. So we can maintain for each good interval a set of reachable positions in that rightmost window.
       So the algorithm:
         For each good interval G_i, we maintain a set of reachable positions in the window W_i = [max(start of G_i, start of G_i? Actually, we need to define the window that is useful for the next crossing. For G_0, the next bad interval is 1. To cross to G_1, we need x in G_0 such that x+B >= start of G_1 = R_1+1. So x >= R_1+1-B. So the window for G_0 is W_0 = [max(1, R_1+1-B), L_1-1] (since G_0 ends at L_1-1). The size of W_0 is at most B.
         For G_i (i=1..M-1), the next bad interval is i+1. To cross to G_{i+1}, we need x in G_i such that x+B >= start of G_{i+1} = R_{i+1}+1. So x >= R_{i+1}+1-B. So the window for G_i is W_i = [max(start of G_i, R_{i+1}+1-B), end of G_i]. The size of W_i is at most B.
         For G_M, there is no next bad interval. So we need to determine if we can reach N from some position in G_M. We can compute the reachable set in G_M, but G_M could be long. However, since there are no bad squares in G_M, we can just check if N is reachable from the reachable positions in the window of G_{M-1} after crossing the last bad interval. Actually, we need to consider the reachable positions in G_M that are "close enough" to the start of G_M? No, we just need to know if there is any reachable position in G_M from which we can reach N. Since G_M is just a line, we can compute the set of reachable positions in G_M that are at most B away from N? Actually, to reach N, we need a position x in G_M such that N - x is representable. We can just check that for the reachable positions in the "entry" to G_M. But the reachable positions in G_M are those that we can reach by jumping from the window of G_{M-1} across the last bad interval, and then possibly making additional jumps within G_M. But since G_M has no bad squares, if we can reach any position in G_M, we can reach N if and only if the distance from that position to N is representable. So we can just compute the set of reachable positions in G_M that are at most something? Actually, we can just BFS within G_M, but we only need to explore up to N. But N is huge. However, we can use the no-obstacle reachability check for any position. So we don't need to BFS within G_M. We just need to know the set of positions in G_M that are reachable from the previous step. But how do we compute that set without BFS through the whole G_M? We can compute it as: from the reachable positions in W_{M-1}, we can jump to G_M. The jump will land at some y in G_M. Then from y, we can make additional jumps within G_M. But since there are no obstacles, the set of reachable positions in G_M is exactly the set of positions that are representable from some initial y. So we can just check for each y that is reachable in one jump from W_{M-1} to G_M, whether N is reachable from y. But wait, we might also be able to make multiple jumps within G_M to get closer to N. So we need to consider all positions in G_M that are reachable from the set of initial landing positions. However, since there are no obstacles, if we can reach any position in G_M, we can reach N if and only if the distance from that position to N is representable. So we can just compute the set of reachable positions in G_M that are "close" to the start? No, we need to consider all reachable positions in G_M, but they might be many. However, we can use the fact that the reachable set in G_M is a union of arithmetic progressions? Actually, if we have a set of starting positions S in G_M, the reachable set is S + S, where S is the semigroup generated by [A,B]. This set can be described as all positions x in G_M such that x - s is in the semigroup for some s in S. Since S is finite (size at most B), and the semigroup is known, we can check for each s in S if there exists x = s + d in G_M such that d is in the semigroup and s+d = N? Actually, we want to know if N is reachable. That is, does there exist s in S and d in the semigroup such that s + d = N? This is equivalent to: does there exist s in S such that N - s is in the semigroup? So we just need to know the set S of positions in G_M that are reachable in one jump from the previous window. But S might not be the only reachable positions in G_M, because we could also make jumps within G_M from those positions. But if we can make additional jumps, that just means we can reach further positions. However, if N is reachable, then there is some path. The last jump before reaching N is from some position y in G_M (y < N). So N - y must be in [A,B]. So y is in [N-B, N-1]. So we only need to know if there is any reachable position in [N-B, N-1] that is in G_M. So we don't need to know the entire reachable set in G_M; we only need to know if any position in the last B positions of G_M is reachable. And we can compute that by doing a BFS from the start of G_M, but we can stop when we either reach the last B positions or determine they are unreachable. But the start of G_M is R_M+1. The distance from R_M+1 to N-B could be huge. So we cannot BFS through the whole G_M. However, we can use the no-obstacle reachability from the entry point. Actually, we can compute the set of reachable positions in G_M that are in the window [N-B, N-1] by using the semigroup property. But maybe it's easier: we can just BFS from the start of G_M, but we only explore positions that are within B of the end? No, that doesn't work.
   Let me rethink: The standard solution for this problem is to BFS on the "positions modulo some number" or to use a BFS with a limit of R_M + B, but then after that, we do a greedy check. I recall a solution: BFS from 1, but we only push positions that are <= the right endpoint of the current bad interval + B. We process the bad intervals in order. For each bad interval, we run a BFS from the current frontier, but we only explore positions up to the right endpoint of that bad interval + B. Then we take the reachable positions that are in the good interval after the bad interval, and we set them as the new frontier. We continue. At the end, we have a frontier in the last good interval. Then we check if N is reachable from that frontier using a simple BFS/DP without obstacles, but we can cap that BFS to some limit as well? Actually, after the last bad interval, we can just do a BFS without obstacles, but we can stop when we reach N or when the distance from the current position to N is less than something? Since there are no obstacles, we can just check if the distance from any frontier position to N is representable. So we don't need to BFS through the last good interval. We just need the frontier positions. And the frontier positions are those we can reach by jumping from the previous window. So we can compute them directly.
   Let's try to write a precise algorithm:
   - Maintain a set of reachable positions `cur` that are in the current "window" of interest.
   - Initially, `cur` = {1}. But 1 might not be in the window for G_0. We need to bring 1 into the window. Actually, we can just BFS from 1 until we reach the window W_0. But since G_0 has no bad squares, we can just check if 1 can reach any position in W_0. But W_0 is at the end of G_0. The distance from 1 to W_0 might be large. However, we can use the fact that the reachable set from 1 in G_0 is 1 + S. So we can just compute which positions in W_0 are in 1 + S. That is, for each x in W_0, check if x-1 is in S. Since W_0 is small (size <= B), we can just iterate over x in W_0 and check if x-1 is representable. How to check if a number D is representable as sum of [A,B]? We can precompute the set of representable numbers up to some bound, say 400. Then for D > 400, we can use the fact that the set is eventually periodic with period g = gcd(A,B). Actually, the semigroup generated by [A,B] has Frobenius number. But we can just do a BFS on the distances modulo g. Since A,B <= 20, g is at most 20. We can precompute the set of all representable numbers up to, say, 400. Then for any D, we can check if D is representable by finding if there is some multiple of g that we can add? Not exactly. A simple way: since A,B are small, we can precompute the set of all representable numbers up to 400, and then for any D, we can just do a BFS on the state (D mod something) but that's not deterministic. Actually, we can just do a greedy: since we can use jumps of A and B, we can think of it as a coin change problem. The set of representable numbers is all integers >= some bound that are multiples of g. The bound is the Frobenius number. But we don't need the exact bound; we can just precompute the representable numbers up to, say, A*B. Then for any D, if D > A*B and D is a multiple of g, it is representable. But is that true? For A=4, B=6, g=2. The representable numbers are 0,4,6,8,10,12,... The largest non-representable is 2? Actually, 2 is not representable, 10 is, 12 is. The Frobenius number is not defined for non-coprime. The condition for representability is that D is a multiple of g and D >= some minimum. For [A,B] with A<=B, the set of representable numbers is exactly the set of multiples of g that are >= (A/g) * (B/g) - 1? Not exactly. Actually, the set of representable numbers is the semigroup generated by A and B. Its complement in the multiples of g is finite. The maximum non-representable multiple is at most A*B/g - A - B? Not sure. But since A,B <= 20, we can just precompute all representable numbers up to 400. Then for D > 400, we can check if D is representable by seeing if D - k*g is representable for some k? That's not a simple check. However, we can do a BFS on the graph of distances modulo g. Since g is small, we can compute the set of representable residues modulo g and the minimum representable number for each residue. Then for a given D, we can check if D >= min_rep[res] and D is a multiple of g? But the condition is that D - min_rep[res] is a multiple of g. So we can just compute for each residue r mod g, the minimum representable number with that residue, and then check if D >= min_rep[r] and (D - min_rep[r]) % g == 0. But wait, the set of representable numbers might not include all sufficiently large multiples of g. Actually, for a numerical semigroup generated by A and B, the set of gaps is finite. The condition is that D is representable if and only if D is a multiple of g and D >= some threshold. But is that threshold the same for all residues? No, each residue class mod g that is representable has its own minimum. And all sufficiently large numbers in that residue class are representable. So we can precompute for each residue r (0 <= r < g) the minimum representable number m[r] with that residue. Then for a given D, if D % g == r, and D >= m[r], then D is representable. But we need to ensure that m[r] is finite (i.e., there is at least one representable number with that residue). So we can precompute m[r] by BFS up to some bound. Since A,B <= 20, the bound can be 400. So we can precompute an array `rep` of size 400 (or 4000) indicating which numbers are representable. Then for D > 400, we check D % g and compare with m[r]. But we need to be careful: is it true that all numbers >= m[r] with the same residue are representable? Yes, for numerical semigroups generated by two numbers, the set of representable numbers is eventually periodic with period g. Actually, the set of representable numbers is a semigroup, and its complement is finite. So there exists a bound B such that for all n >= B, n is representable iff n % g is in some set. So we can precompute the minimum representable number for each residue mod g. So we can implement a function `is_representable(D)` that returns True if D can be expressed as sum of numbers in [A,B].
   So back to the algorithm: We have a set of reachable positions in the current window. To compute the reachable positions in the next window, we do the following:
   - For each x in the current window (which is in G_i), we can jump to y = x + j for j in [A,B]. We want y to be in the next good interval G_{i+1}. We collect all such y. This gives a set of "entry" positions into G_{i+1}.
   - Then, from these entry positions, we can make additional jumps within G_{i+1} to reach other positions in G_{i+1}. But we only need the positions that are in the next window W_{i+1} (which is the rightmost part of G_{i+1}). So we need to compute the reachable set in G_{i+1} restricted to W_{i+1}. Since G_{i+1} has no bad squares, the reachable set in G_{i+1} from a set of starting positions S is the set of positions that are representable as s + d where s in S and d is a sum of [A,B]. But we only care about the intersection with W_{i+1}. Since W_{i+1} is small (size <= B), we can just iterate over all possible positions in W_{i+1} and check if they are reachable from S. How to check if a position y in W_{i+1} is reachable from S? It is reachable if there exists s in S such that y - s is representable (i.e., in the semigroup). So we can just check for each y in W_{i+1} and each s in S, if y - s is representable. If yes, then y is reachable. This is O(|W| * |S| * check_time). Since |W| <= B, |S| <= B, and check_time is O(1) (if we have a good representation function), this is fast.
   - So we can compute the new set `cur` for the next window as: for each y in W_{i+1}, if there exists s in the previous `cur` (which are in G_i) such that y - s is in [A,B] and y - s is representable? Wait, careful: The jump from s to y must be a single jump? No, we can make multiple jumps. So from s in G_i, we can jump to some intermediate positions, and eventually reach y. So the condition is that y - s is a sum of numbers in [A,B] (with each summand in [A,B]), and all intermediate positions are in good squares. But since we are in G_{i+1} which is a good interval, there are no bad squares. So as long as we don't jump out of G_{i+1}? Actually, if we start in G_i, we can jump to G_{i+1} in one jump, or we can jump within G_i and then to G_{i+1}. So the path from s to y might go through other good intervals? But we are only considering jumps that land in G_{i+1}. If we make a jump that lands in a bad interval, it's invalid. So the path must avoid bad intervals. Since G_i and G_{i+1} are separated by a bad interval, any jump from G_i to G_{i+1} must be a single jump that crosses the bad interval. Because if we try to make multiple jumps, we would have to land somewhere in between, but the only squares between G_i and G_{i+1} are the bad interval. So we cannot land on them. Therefore, the only way to go from G_i to G_{i+1} is a single jump that lands in G_{i+1}. So from s in G_i, we can only reach y in G_{i+1} if y - s is a single jump, i.e., y - s in [A,B]. So there are no multi-jump paths that cross the bad interval. So the condition is simply: y is reachable from s if y - s in [A,B] and y in G_{i+1}. And then from y, we can make additional jumps within G_{i+1}. So to compute the reachable set in G_{i+1}, we can start with the set S of all y that can be reached in one jump from the previous `cur` (which is in G_i). Then from S, we can BFS within G_{i+1} to find all reachable positions in G_{i+1}. But we only need the ones in W_{i+1}. So we can just BFS from S within G_{i+1}, but we stop when we reach W_{i+1} or when we can't go further. However, BFS within G_{i+1} might be long if G_{i+1} is long. But since we only need the positions in W_{i+1}, and W_{i+1} is at the right end of G_{i+1}, we can just compute the reachable set in W_{i+1} by checking for each y in W_{i+1} if there exists s in S such that y - s is representable (as a sum of [A,B]) AND the path from s to y stays within G_{i+1}. But does it stay within G_{i+1}? If we start at s in G_{i+1} and make jumps, we might jump out of G_{i+1}? Actually, G_{i+1} is followed by another bad interval (unless it's the last). If we jump from s in G_{i+1} and land in the next bad interval, that's invalid. So we must ensure that all intermediate positions are in G_{i+1}. So the representability condition is not enough; we also need that the path doesn't cross into the next bad interval. But since we are only interested in reaching y in W_{i+1}, and y is near the end of G_{i+1}, we can just do a BFS from S within G_{i+1} and only explore positions that are in G_{i+1} and <= y. But we can do this efficiently by noting that from a position in G_{i+1}, we can jump up to B forward. So if we want to reach y, we need to ensure that we don't overshoot y or land in the next bad interval. Actually, we can just BFS from S, but we only keep positions that are in G_{i+1} and <= y. Since y is in W_{i+1} and W_{i+1} is at the end, the number of positions we explore is bounded by the length of G_{i+1} from S to y, which could be large. But wait, we can optimize: since we only need to know if y is reachable, and the jumps are in [A,B], we can use a DP/BFS on the positions modulo something. But maybe we can avoid BFS by using the fact that the reachable set in a long interval without obstacles is eventually all positions that are congruent to something modulo g. Actually, if we have a set of starting positions S in G_{i+1}, the reachable set in G_{i+1} is S + Semigroup, but restricted to G_{i+1}. This set might not be all positions in G_{i+1} that are in the semigroup; it depends on S. But since we are only interested in the rightmost window W_{i+1}, and W_{i+1} is small, we can just simulate the BFS from S, but we can stop when we reach a position in W_{i+1} or when the distance from the current position to the start of W_{i+1} is too large? Actually, we can do a BFS from S, but we only push positions that are <= the maximum position we care about. The maximum position we care about is the end of W_{i+1}. So we do a BFS from S, but we only explore positions up to the end of W_{i+1}. Since S is a set of positions in G_{i+1}, and G_{i+1} is before W_{i+1}, the BFS might have to explore a lot of positions if G_{i+1} is long. But we can use the fact that the BFS without obstacles can be simulated by just checking distances. Actually, from a position s in S, we can reach y if and only if y - s is a sum of numbers in [A,B] AND all intermediate positions are in G_{i+1}. Since G_{i+1} is an interval, the condition that intermediate positions are in G_{i+1} is equivalent to: the path never goes below the start of G_{i+1} or above the end of G_{i+1}. But since we are moving forward, we only need to ensure that we don't jump over the end. But if we are just trying to reach a specific y, we can just check if there is a path. This is equivalent to checking if y is in the reachable set from S. We can compute the reachable set from S in the interval [start, end] by BFS. Since the interval can be long, we need a faster way. Notice that the jumps are small. So we can use a BFS with a set of visited positions, but we only visit positions that are reachable. The number of reachable positions in a long interval can be large, but we only need to know if the end window is reachable. There is a known technique: since A,B are small, we can use a BFS on the "state" which is the position modulo some number, but that's for the whole problem. Here, we have a specific interval.
   Alternatively, we can avoid the BFS within G_{i+1} by noting that from S, we can reach any position in G_{i+1} that is sufficiently far and has the right residue, provided that the distance from S to that position is representable. But we need a concrete way.
   Let me look for the standard solution. I am now recalling that the solution is to BFS on the graph, but we maintain a set of reachable positions that are "close" to the end of the current good interval. The BFS is done on the fly as we process the good intervals. The key is that the number of positions we keep is small. Specifically, we keep a set of reachable positions in the current good interval, but we only keep those that are at most B positions away from the end of the good interval. Then, when we move to the next good interval, we compute the new set by considering jumps from these positions. Since the jumps are at most B, the new set will be a set of positions in the next good interval that are also within B of its end. So the size of the set remains bounded by B (or maybe 2B). So the total time is O(M * B^2) or something.
   Let's try to design it that way:
   - For each good interval G_i, we maintain a set of reachable positions `S_i` that are in the "tail" of G_i, specifically in the last B positions of G_i. But wait, the tail of G_i is the part that is useful for crossing the next bad interval. The next bad interval starts at L_{i+1} (for i=0, L_1; for i>=1, L_{i+1}? Actually, bad interval i+1 is [L_{i+1}, R_{i+1}]. G_i ends at L_{i+1}-1. So the last B positions of G_i are [L_{i+1}-B, L_{i+1}-1]. To jump from G_i to G_{i+1}, we need x in G_i such that x+B >= start of G_{i+1} = R_{i+1}+1. So we need x >= R_{i+1}+1-B. So the useful x are in [R_{i+1}+1-B, L_{i+1}-1]. The length of this interval is (L_{i+1}-1) - (R_{i+1}+1-B) + 1 = L_{i+1} - R_{i+1} - 2 + B. Since L_{i+1} <= R_{i+1}, L_{i+1} - R_{i+1} is negative, so the length is at most B-1. So indeed, the useful x are in a set of size at most B-1. So we can maintain a set of reachable positions in that set.
   - Initially, for G_0, the useful set is W_0 = [max(1, R_1+1-B), L_1-1]. We need to know which positions in W_0 are reachable from 1. We can compute this by BFS from 1 within G_0, but we only care about W_0. Since G_0 is just a line, we can just check for each x in W_0 if x-1 is representable (as sum of [A,B]). But we also need to ensure that the path stays within G_0. Since there are no bad squares in G_0, any path of jumps in [A,B] from 1 to x is valid as long as it doesn't go below 1 or above L_1-1? But we can always choose a path that stays within bounds if x is in G_0. Actually, if x is in G_0, we can just use the greedy algorithm: jump B until close, then adjust. But we need to be sure that we don't need to go through bad squares. Since G_0 is good, any path is fine. So we can just use the representability check. However, we also need to consider that we might not be able to reach x if we are forced to land on a bad square? But there are no bad squares in G_0. So the only obstacle is the boundary. So we need to check if there is a path from 1 to x using jumps in [A,B] that stays within [1, L_1-1]. This is a bounded reachability problem. But since the interval is large, we can solve it by checking if x-1 is representable and x-1 <= some maximum? Actually, if x-1 is representable, we can always find a path that stays within [1, L_1-1] as long as the path doesn't overshoot? But we can always go backwards? No, we can only move forward. So we need a path that starts at 1 and ends at x, with all intermediate positions in [1, L_1-1]. This is equivalent to: can we express x-1 as a sum of numbers in [A,B] such that the partial sums never exceed L_1-1? But since we can always choose the jumps to avoid overshooting? Actually, if we are going from 1 to x, and x is not too far, we can just use a combination of A and B. The condition for existence of a path that stays within bounds is that x-1 is representable and x-1 is not too large? Actually, if x-1 is representable, we can always find a representation that doesn't overshoot the upper bound, as long as the upper bound is at least x. But we also need to not go below 1, which is automatic. So the only issue is if the path forces us to go above L_1-1 before coming back? But we can't come back. So we need a path that is monotonic increasing. So we need to find a sequence of jumps that sums to x-1, and each partial sum + 1 is <= L_1-1. This is possible if and only if x-1 is representable and we can do it without exceeding the bound. But since the jumps are positive, the partial sums are increasing. So the condition is that the sum of the first k jumps is <= L_1-1 - 1 for all k. This is equivalent to saying that we can represent x-1 in a way that no partial sum exceeds L_1-2. But since we can always use the largest jump B, we might overshoot. However, we can use a greedy approach: from 1, we want to reach x. We can always jump B until we are within B of x, then jump the exact difference. This will work as long as we never land above L_1-1. So we need that the positions we land on are <= L_1-1. This is true if we start at 1 and jump B repeatedly, we get positions 1+B, 1+2B, etc. As long as 1+kB <= L_1-1 for all k until we are close to x, we are fine. But if L_1-1 is small, we might be restricted. However, since we only care about x in W_0, and W_0 is near L_1-1, the distance from 1 to W_0 might be large. But we can also use smaller jumps to avoid overshooting. In fact, if x-1 is representable, there exists a representation that doesn't overshoot the upper bound, as long as the upper bound is at least the maximum jump? Not necessarily. For example, A=2, B=3, L_1-1=5. Can we reach 5 from 1? 5-1=4, which is 2+2. Path: 1->3->5. That works. Can we reach 4? 4-1=3, which is 3. Path: 1->4. Works. So it seems fine. The only potential issue is if the target is so close to the start that we can't reach it with a single jump? But A>=1, so we can always reach nearby. So I think for an interval with no bad squares, we can reach x from 1 if and only if x-1 is representable. But we also need to ensure that we don't step on bad squares, but there are none. So we can just use the representability check.
   - So for G_0, we can compute S_0 = { x in W_0 | x-1 is representable }.
   - Then for i=0 to M-2 (i.e., for all but the last transition), we do:
       We have a set S_i of reachable positions in W_i (which is in G_i).
       We want to compute S_{i+1}, the set of reachable positions in W_{i+1} (which is in G_{i+1}).
       To do this, we consider all possible jumps from positions in S_i. For each x in S_i, and for each jump length j in [A,B], we get a landing position y = x+j. We only care if y is in G_{i+1}. If y is in G_{i+1}, then we have an entry into G_{i+1}. We collect all such y into a set E.
       Then, from E, we can make additional jumps within G_{i+1}. We want to know which positions in W_{i+1} are reachable from E. This is a BFS within G_{i+1} from the set E. But as argued, G_{i+1} is a good interval. So the reachable set in G_{i+1} from E is the set of positions that can be reached by jumping within G_{i+1}. We can compute the intersection of this reachable set with W_{i+1}. How to compute it efficiently? We can just BFS from E within G_{i+1}, but we only explore positions up to the end of W_{i+1}. Since W_{i+1} is at the end of G_{i+1}, and E is somewhere in G_{i+1}, the BFS might have to explore a lot of positions. However, we can use the fact that the BFS without obstacles can be simulated by a DP on the positions. Since the jumps are small, we can maintain a set of reachable positions as a sliding window. But maybe we can just BFS from E, but we stop when we reach a position in W_{i+1} or when we can't go further. The maximum position we need to consider is the end of W_{i+1}. So we can do a BFS from E, but we only push positions that are <= end of W_{i+1}. The number of positions we push could be large if G_{i+1} is long. But we can use a trick: since the jumps are in [A,B], the reachable set in a long interval from a set of starting positions is eventually periodic. Actually, if we start from a set of positions, the set of reachable positions in an interval without obstacles is exactly the set of positions that are congruent to some residue modulo g and are >= some threshold. But we need a concrete algorithm.
   - There is a known solution that uses a BFS on the "state" of the current position, but it only keeps positions that are at most B away from the end of the current good interval. The BFS is done by iterating through the good intervals and using a set of offsets. I think the standard solution is: We maintain a set of reachable positions that are in the range [current_end - B, current_end]. When we move to the next good interval, we update this set by adding A..B to each position and taking those that fall in the new good interval, and then we do a kind of closure. Actually, the closure is just the fact that if we have a reachable position at x, then we can also reach x+1 if we can jump B from somewhere? Not exactly.
   Let me search my memory for the exact code. I recall a solution that looks like:
   ```
   from collections import deque
   visited = set()
   q = deque([1])
   visited.add(1)
   while q:
       x = q.popleft()
       for d in range(A, B+1):
           y = x + d
           if y > N: break
           if y == N: print("Yes"); return
           if is_bad(y): continue
           if y not in visited:
               visited.add(y)
               q.append(y)
   ```
   But this is too slow if N is large and there are no bad squares. So there must be a pruning condition: we only push y if y <= some limit. The limit is updated as we process the bad intervals. Specifically, we process the bad intervals in order. We maintain a "current right limit" which is the right endpoint of the current bad interval + B. We only push y if y <= current_limit. When we have processed a bad interval, we update the current_limit to the right endpoint of the next bad interval + B. And we also only consider positions that are in the good interval after the current bad interval. This is similar to the BFS limit idea.
   Let's try to implement that: We have bad intervals sorted. We will perform a BFS, but we only explore positions up to a dynamic limit. We process the bad intervals from left to right. Initially, the limit is R_1 + B. We BFS from 1, but we only push positions that are <= R_1 + B. During BFS, we might reach positions in the good interval after the first bad interval. Those positions are in [R_1+1, L_2-1] (for the first gap). We continue BFS within that limit. Once we have explored all positions <= R_1 + B, we then increase the limit to R_2 + B, and we continue BFS from the frontier (the positions in the good interval after the first bad interval). We then explore positions up to the new limit. This way, the BFS never explores beyond R_i + B for the i-th bad interval. At the end, we have explored up to R_M + B. Then we check if N is reachable. But as we saw, if N is far, we might not have explored enough. So after the BFS, we need to check if N is reachable from the positions we have in the last good interval. We can do that by using the no-obstacle reachability check.
   So the algorithm:
   - Read bad intervals.
   - Create a list of bad intervals for binary search.
   - If M == 0: just check if N-1 is representable.
   - Otherwise, let bad intervals be [L_1,R_1], ..., [L_M,R_M].
   - We will do a BFS with a queue. We maintain a set of visited positions.
   - We start with position 1 in the queue.
   - We maintain a variable `current_limit` which is the maximum position we are allowed to push into the queue. Initially, `current_limit` = min(N, R_1 + B). But wait, we might need to push positions that are > R_1? Actually, the first bad interval is [L_1,R_1]. The good interval before it is G_0 = [1, L_1-1]. The good interval after it is G_1 = [R_1+1, L_2-1]. We want to cross it. To cross it, we need to reach a position in G_1. The maximum position we might need to consider in G_1 is R_1+1 + B? Actually, to land in G_1, we need a jump from G_0. The landing position y in G_1 is at most (L_1-1) + B. But also y >= R_1+1. So the maximum y is min(L_1-1+B, L_2-1). So the limit for the first phase should be the maximum position we might land on in G_1. That is: the maximum y in G_1 that can be reached from G_0. The maximum possible y is (L_1-1) + B, but we also have to be in G_1, so y <= L_2-1. So the limit is min(L_2-1, L_1-1+B). But since L_2-1 might be larger than L_1-1+B, the limit is L_1-1+B. So we can set `current_limit` = R_1 + B? Wait, R_1 is the end of the first bad interval. The start of G_1 is R_1+1. The maximum y we can reach in G_1 is (L_1-1)+B. But (L_1-1)+B could be greater than R_1+B? Since L_1 <= R_1+1? Not necessarily. L_1 could be much smaller than R_1. So (L_1-1)+B could be less than R_1+B. Actually, since L_1 <= R_1+1, L_1-1 <= R_1. So (L_1-1)+B <= R_1+B. So the maximum y we can reach in G_1 is at most R_1+B. So setting `current_limit` = R_1+B is safe. But it might be larger than necessary, but that's fine.
   - So we do a BFS from 1, but we only push positions y if y <= current_limit. We also need to check if y is bad. We stop when the queue is empty.
   - After that, we have visited all positions up to current_limit that are reachable. Now, we need to move to the next bad interval. The next bad interval is [L_2,R_2]. The good interval after it is G_2 = [R_2+1, L_3-1]. We need to continue BFS from the positions we have that are in G_1 (i.e., positions in [R_1+1, L_2-1]). But we also have positions in G_0 that are <= current_limit. However, positions in G_0 cannot help us cross the next bad interval because they are too far left. To cross the next bad interval, we need to start from a position in G_1 that is within B of G_2. So we need to filter the visited set to only those in G_1 that are "useful". Actually, we can just take all visited positions in G_1, and then for each such position, we can try to jump to G_2. But we need to ensure that we don't lose any positions. The BFS we did up to current_limit already explored all positions reachable up to that limit. So any position in G_1 that is reachable and <= current_limit is already in the visited set. Now, we want to continue BFS from those positions, but we increase the limit to the next one: `current_limit` = min(N, R_2 + B). We then take the visited positions that are in G_1 and <= R_1+B (which they all are), and we push them into a new queue? But we need to be careful: we have already explored from them up to current_limit. So we should only explore new positions that are > current_limit and <= new_limit. So we can just do: for each visited position x in G_1 (i.e., x in [R_1+1, L_2-1]), for each jump j in [A,B], y = x+j. If y > new_limit, break? Actually, we need to push y if y > current_limit and y <= new_limit and y is not bad and not visited. But we also need to consider that we might need to explore multiple steps within G_1 to reach the useful positions. However, since we already did a BFS up to current_limit, we have already explored all reachable positions up to current_limit. So any position in G_1 that is reachable and could lead to a jump to G_2 is either <= current_limit or > current_limit. But if it's > current_limit, it would be in the range (current_limit, L_2-1]. So we need to continue BFS within G_1 to reach those positions. So we can just do a BFS starting from all visited positions in G_1, but we only explore positions y that are > current_limit and <= new_limit. And we also need to include positions that are in G_1 but > current_limit. So we can set up a new queue with all visited positions in G_1 that are <= current_limit, but we only process jumps that land > current_limit. However, we might also need to process jumps that land <= current_limit? No, those are already visited. So we can just do: new_queue = all visited positions in G_1. Then while new_queue not empty: pop x, for each j in [A,B], y = x+j. If y > new_limit, break. If y <= current_limit, continue (already visited). If y is bad, continue. If y not visited, mark visited and push to new_queue. This way, we only explore new positions. This is efficient.
   - We repeat this for each bad interval. At the end, we have visited positions up to R_M + B. Then we need to check if N is reachable. N is in G_M. We have visited positions in G_M that are <= R_M + B. We need to check if we can reach N from any of those positions using jumps in [A,B] without obstacles. This is the no-obstacle reachability check. We can do this by taking the set of visited positions in G_M, and for each such position x, check if N - x is representable. If yes, print "Yes". If no, print "No".
   - But wait: what if N is <= R_M + B? Then we might have already visited N during the BFS. So we should check during BFS if we reach N.
   - Also, we need to handle the case where the last good interval is very long, and we have visited positions near its start. We need to check if N is reachable from those positions. Since there are no obstacles, we can just check representability.
   - What about the first good interval G_0? We started BFS from 1. We need to ensure that we can reach the window in G_0 that is useful for crossing the first bad interval. But our BFS up to current_limit will explore all reachable positions up to current_limit. So that will include the useful positions in G_0 if they are reachable. So we don't need a special step for G_0.
   - So the algorithm is:
        1. Read N, M, A, B. Read bad intervals into lists L and R.
        2. If M == 0: check if N-1 is representable. Print Yes/No.
        3. Else, create a list of bad intervals for binary search (or just use the L and R arrays since they are sorted).
        4. Initialize visited = set(), queue = deque([1]). visited.add(1). current_limit = min(N, R[0] + B). Note: R is 0-indexed.
        5. While queue not empty:
            x = queue.popleft()
            for d in range(A, B+1):
                y = x + d
                if y > N: break
                if y == N: print("Yes"); return
                if y > current_limit: continue  # don't push beyond current limit
                if is_bad(y): continue
                if y not in visited:
                    visited.add(y)
                    queue.append(y)
        6. After the loop, we have processed up to current_limit. Now, for each bad interval i from 0 to M-2 (i.e., for the first M-1 bad intervals), we do:
            - The current bad interval is i. The good interval after it is G_{i+1} = [R[i]+1, L[i+1]-1] (for i < M-1). For i = M-1, the good interval is G_M = [R[M-1]+1, N].
            - We want to continue BFS from the visited positions in G_{i+1}. So we collect all visited positions x such that R[i]+1 <= x <= L[i+1]-1. Actually, we also need to include positions that are in G_{i+1} but might have been visited? Yes, we take all visited positions in that range. But we also need to include positions that are in G_{i+1} but we haven't visited because they are > current_limit? No, we are about to increase the limit, so we will explore new positions. So we need to push the visited positions in G_{i+1} into a new queue, and then explore positions up to the new limit.
            - But careful: the visited positions in G_{i+1} might be empty. If empty, we can skip.
            - New limit: for i from 0 to M-2, new_limit = min(N, R[i+1] + B). For i = M-1, we don't have a next bad interval, so we don't need to increase the limit? Actually, after the last bad interval, we have no more limits. We just need to check reachability to N. So we can just take the visited positions in G_M and check representability.
            - So for i = 0 to M-2:
                new_limit = min(N, R[i+1] + B)
                new_queue = deque()
                for x in visited:
                    if R[i]+1 <= x <= L[i+1]-1:
                        new_queue.append(x)
                current_limit = new_limit
                while new_queue not empty:
                    x = new_queue.popleft()
                    for d in range(A, B+1):
                        y = x + d
                        if y > N: break
                        if y == N: print("Yes"); return
                        if y > current_limit: continue
                        if is_bad(y): continue
                        if y not in visited:
                            visited.add(y)
                            new_queue.append(y)
            - After processing all bad intervals, we have visited positions up to R[M-1] + B. Now we need to check the last good interval G_M = [R[M-1]+1, N]. We have visited positions in G_M that are <= R[M-1] + B. We need to check if we can reach N from any of them. So we collect all visited positions x in G_M (i.e., x >= R[M-1]+1). For each such x, check if N - x is representable. If yes, print "Yes". Otherwise, print "No".
        7. We also need to handle the case where during the BFS we might have already reached N. So we check that at every step.
   - This algorithm should work. But we need to be careful with the `is_bad` function. Since M is up to 20000, we can store the bad intervals in a list and use binary search to check if a point is in any bad interval. Since the intervals are sorted and non-overlapping, we can do: find the interval i such that L[i] <= y <= R[i]. We can use bisect to find the index i such that L[i] <= y, then check if y <= R[i]. If yes, it's bad.
   - Also, the `is_representable` function: we need to check if a number D can be expressed as a sum of numbers in [A,B]. Since A,B <= 20, we can precompute a set `rep` of all representable numbers up to, say, 400. Then for D > 400, we can use the fact that the set is eventually periodic with period g = gcd(A,B). We can precompute for each residue r mod g the minimum representable number m[r] with that residue. Then for D, if D >= m[D % g], then D is representable. But we need to ensure that m[r] is defined for the residue. Actually, not all residues may be representable. So we can precompute an array `min_rep` of size g, initialized to infinity. For each number in `rep` up to 400, if it's a multiple of g, update min_rep[num % g] = min(min_rep[num % g], num). Then for a given D, if min_rep[D % g] is not infinity and D >= min_rep[D % g], then D is representable. But is that sufficient? For numerical semigroups generated by two numbers, the set of representable numbers is eventually periodic with period g. The preperiod is bounded. So if we precompute up to 400, we should have found the minimum for each residue that is representable. And for any D >= that minimum, D is representable. So this should work. But we need to be careful: if A and B are not coprime, the set of representable numbers is not all multiples of g; it's a subset. But the condition is still that D is in the semigroup. The semigroup is the set of all numbers that can be written as a nonnegative combination of A and B. The set of gaps is finite. So for each residue class mod g that is representable, there is a minimum representable number, and all larger numbers with that residue are representable. So the condition D >= m[r] is necessary and sufficient. So we can precompute m[r] by BFS up to some bound. Since A,B <= 20, the Frobenius number for coprime A,B is A*B - A - B. For non-coprime, the maximum gap is at most A*B/g. So precomputing up to 400 should be safe. Actually, we can just precompute up to A*B*2 or something. But 400 is fine since max A*B is 400.
   - One more thing: during the BFS, we might have a lot of visited positions. The number of visited positions is bounded by the number of positions we explore, which is at most the total length of the windows we explore. Since we only explore up to R_M + B, and we only explore positions in good intervals, the number of positions could be up to R_M + B, which is huge if R_M is huge. But wait, we only explore positions that are reachable. In a long good interval with no bad squares, we might explore a lot of positions. For example, if G_0 is [1, 10^12], and we BFS from 1 with jumps [1,2], we will visit almost all positions up to 10^12. That's too many. So the BFS as described above would still be too slow if we allow it to explore all positions in a long good interval. We need to limit the BFS to only the positions that are "close" to the end of the good interval. In the algorithm above, we set `current_limit` = R_1 + B. But R_1 could be huge, and the good interval G_0 could be huge. So we would be exploring positions in G_0 up to R_1 + B, which could be 10^12. So we need a different limit.
   The key is: we don't need to explore the entire good interval G_0. We only need to explore the part of G_0 that is within B of the end of G_0. Because only those positions can be used to cross the first bad interval. So we should set the limit for the first phase to be the maximum position in G_0 that is useful for crossing. That is, we only need to explore positions in G_0 that are >= L_1 - B? Actually, to cross the first bad interval, we need x in G_0 such that x+B >= R_1+1. So x >= R_1+1-B. Since G_0 ends at L_1-1, the useful x are in [max(1, R_1+1-B), L_1-1]. So we only need to explore positions in that range. But we also need to reach those positions from 1. So we need to BFS from 1, but we can stop once we have explored all positions in that range, or we can BFS up to L_1-1. But L_1-1 could be huge. However, we can BFS from 1, but we only push positions that are <= L_1-1. That is still huge if L_1-1 is huge. So we need to avoid BFS through the whole G_0.
   The solution is to not BFS through the whole good interval, but instead, for each good interval, we only keep track of the reachable positions in the "tail" of the good interval. And to compute the reachable positions in the tail, we can use a BFS that only explores the tail, but we need to know which positions in the tail are reachable from the start of the good interval. Since the good interval has no bad squares, the reachable set in the tail is determined by the representability of distances. So we can just check for each position in the tail if it is reachable from the start of the good interval (or from the previous tail). But the start of the good interval might be far from the tail. However, we can use the fact that the reachable set in a long interval is eventually all positions that are in the semigroup. But we need a concrete way.
   I recall the standard solution: We process the good intervals from left to right. For each good interval, we maintain a set of reachable positions that are in the last B positions of the good interval. To compute this set for the current good interval, we take the set from the previous good interval, and for each position in that set, we consider jumps of length A..B that land in the current good interval. Those landing positions are in the current good interval. Then, from those landing positions, we can make additional jumps within the current good interval to reach other positions in the last B positions. But since the current good interval has no bad squares, we can just do a BFS from the landing positions, but we only explore positions up to the end of the good interval. However, the current good interval could be long, so we need to limit the BFS. The trick is that we only care about the last B positions. So we can do a BFS from the landing positions, but we stop when we reach the last B positions or when we have explored enough. Since the jumps are small, we can use a DP to compute which positions in the last B positions are reachable. Specifically, we can maintain a set of reachable positions as a sliding window of size B. We start with the landing positions. Then we iterate from the left end of the good interval to the right, and we keep a set of reachable positions in the last B positions. But this might be O(length of good interval) which is too long.
   There is a known technique: Since A,B are small, we can represent the reachable set in a good interval as a set of residues modulo g = gcd(A,B). Actually, in a long good interval, the reachable set from a set of starting positions is periodic with period g. So we can just compute the reachable set in a window of size g (or something) and then repeat. But we need to account for the boundary.
   Let me think about the problem differently. This is a known problem from AtCoder. I am sure the solution is to BFS on the "distance" from the start, but with a limit. Actually, I remember a solution that uses a BFS where the queue contains positions, and we only push positions that are less than or equal to the right endpoint of the current bad interval + B. But we also need to handle the fact that the good intervals can be long. The solution might be to compress the positions by considering only positions that are within B of the end of each good interval. And we can compute the reachable positions in that window by doing a BFS from the previous window, but we limit the BFS to that window. How to do that? We can just do a BFS from the previous window, but we only push positions that are within the current window. But the current window is at the end of the good interval. So we start from the previous window (which is in the previous good interval), and we try to jump to the current good interval. The landing positions are in the current good interval. Then from those landing positions, we can make additional jumps within the current good interval to reach the current window. Since the current window is small, we can just do a BFS from the landing positions, but we only explore positions up to the end of the current window. This BFS might have to go through the current good interval, which could be long. But we can optimize by noting that from a landing position, we can only make jumps forward. So we can just simulate the BFS by iterating from the landing positions to the right, and keeping track of reachable positions. But if the good interval is long, we might have to iterate over many positions. However, we can use the fact that the reachable set in a long interval without obstacles is easy to compute: if we have a set of starting positions, the set of positions that are reachable within the interval is exactly the set of positions that are in the semigroup generated by [A,B] added to the starting positions, and also within the interval. So we can just check for each position in the target window if it is reachable from the starting positions. This check is: for each y in target window, and for each s in starting positions, if y - s is representable and y - s >= 0, then y is reachable. This is O(|target| * |start| * check_time). Since |target| <= B, |start| <= B, this is O(B^2) per good interval. So the total time is O(M * B^2), which is fine since M <= 20000, B <= 20. So B^2 = 400, M=20000 gives 8e6 operations, which is fast.
   So the algorithm is:
   - We have a list of good intervals. We will process them from left to right.
   - For each good interval G, we maintain a set of reachable positions that are in the "tail" of G, specifically in the set T = [end - B + 1, end]? Actually, we need the positions that are useful for the next crossing. The next crossing requires positions in G that are >= start of next good interval - B. So the tail is [max(start of G, start of next good interval - B), end of G]. The size of this tail is at most B. So we can maintain a set of reachable positions in this tail.
   - Initially, for G_0, the tail is W_0 = [max(1, R_1+1-B), L_1-1] (assuming M>=1). We need to compute which positions in W_0 are reachable from 1. Since G_0 has no bad squares, we can just check for each x in W_0 if x-1 is representable. But we also need to ensure that we don't overshoot the end of G_0? Actually, if x-1 is representable, we can find a path from 1 to x that stays within G_0. But is that always true? We need to ensure that the path doesn't require landing on positions > L_1-1. Since we are only using jumps in [A,B], and the maximum jump is B, we might need to avoid jumping over the end. But if x-1 is representable, we can always choose a representation that doesn't exceed the bound, as long as the bound is at least the target? Not necessarily. For example, A=2, B=3, G_0 = [1,4] (so L_1-1=4). Can we reach 4 from 1? 4-1=3, which is a jump of 3. That's valid. So yes. What about reaching 3? 3-1=2, valid. So it seems fine. But consider a case where the target is close to the start, but the only representations require large jumps that overshoot? For example, A=3, B=5, target=4, distance=3. 3 is in [A,B], so we can jump 3 directly. So it's fine. The only potential issue is if the target is not representable. So I think the condition is simply that x-1 is representable. However, we also need to consider that we might need to make multiple jumps, and each jump must land in G_0. So the partial sums must be <= L_1-1. This is a stronger condition. But since we can always use a greedy approach: jump B until we are within B of x, then jump the exact difference. This will work as long as the positions we land on are <= L_1-1. But if G_0 is very short, we might not be able to do that. For example, A=5, B=6, G_0 = [1,3] (so L_1-1=3). Can we reach 3 from 1? 3-1=2, but we can only jump 5 or 6. So we cannot reach 3. So x-1=2 is not representable. So it's fine. What if G_0 = [1,6]? Then we can reach 6 by jumping 5. So it's fine. So I think the representability condition is sufficient. But let's test a case: A=2, B=4, G_0 = [1,5], target=5. 5-1=4, which is a jump of 4. So we can jump 4 directly. So it's fine. What if target=3? 3-1=2, valid. So it seems that if the distance is representable, we can always find a path that stays within the interval, as long as the interval contains the start and the target. Because we can always use the representation that doesn't use jumps that are too large. But there might be a case where the only representation uses a jump that is larger than the remaining distance? For example, A=3, B=4, target=5, distance=4. 4 is in [A,B], so we can jump 4. So it's fine. What if target=4, distance=3, jump 3. So it seems that if the distance is representable, there is a representation that doesn't exceed the target, because we can always break down the jumps to be exactly the difference. But wait, the jumps must be integers in [A,B]. So if the distance is representable, there exists a sequence of jumps that sum to the distance. Each jump is at least A, so the first jump is at least A. If A is large, we might overshoot? For example, A=10, B=20, target=15, distance=14. 14 is not representable. So no problem. What if target=25, distance=24. 24 is representable? 10+10+4? But 4 is less than A. So 24 is not representable with jumps >=10. So it must be that the distance is a combination of numbers >=10. So if the distance is representable, all jumps are >= A. So if the start is 1, and we jump A, we land at 1+A. If 1+A > L_1-1, then we cannot land in G_0. But if the target is in G_0, then 1+A <= target <= L_1-1. So 1+A <= L_1-1. So the first jump is at least A, so we land at 1+A which is <= L_1-1. So that's fine. Similarly, by induction, all partial sums will be <= L_1-1 because the target is <= L_1-1 and we are moving towards it. So as long as the target is in G_0, any representation of the distance will keep the partial sums within [1, L_1-1]? Not necessarily: consider a representation that goes above the target and then comes back? But we can't come back. So if a representation has a partial sum > L_1-1, then it overshoots the target, which is impossible because the final sum is exactly the distance. So the partial sums are increasing. So if the final sum is <= L_1-1, then all partial sums are <= L_1-1. So the condition is simply that the distance is representable. So for G_0, we can just check representability.
   - So the algorithm for the general step:
        We have a set `prev` of reachable positions in the tail of the previous good interval G_prev. The tail of G_prev is W_prev = [max(start of G_prev, start of next good interval - B), end of G_prev]. (For the first step, G_prev is G_0, and start of next good interval is R_1+1.)
        We want to compute the set `cur` of reachable positions in the tail of the current good interval G_cur. The tail of G_cur is W_cur = [max(start of G_cur, start of next good interval - B), end of G_cur]. (If G_cur is the last good interval, then there is no next good interval, so we don't need a tail; we just need to check reachability to N.)
        To compute `cur`:
            - First, find the set of positions in G_cur that can be reached in one jump from `prev`. That is, for each x in `prev`, and for each j in [A,B], y = x+j. If y is in G_cur, add y to a set `entry`.
            - Then, from `entry`, we can make additional jumps within G_cur. We want to know which positions in W_cur are reachable from `entry`. This is equivalent to: for each y in W_cur, check if there exists s in `entry` such that y - s is representable (and y - s >= 0). But we also need to ensure that the path from s to y stays within G_cur. Since s and y are in G_cur, and we are moving forward, the condition is that s <= y and y <= end of G_cur. Also, we need that all intermediate positions are in G_cur. This is automatically satisfied if we only consider paths that don't overshoot the end. But if we use the representability check, we are essentially allowing any path of jumps in [A,B] from s to y. Will such a path ever land outside G_cur? It could land below start of G_cur if we jump backwards, but we only move forward. So it can only land above end of G_cur if we overshoot. So we need to ensure that the path doesn't overshoot the end of G_cur. But if y is in G_cur, and we are moving from s to y, the path will not overshoot y if we use a representation that doesn't exceed y. But the representability check doesn't guarantee that the path doesn't overshoot the end of G_cur. However, if y is in G_cur, then y <= end of G_cur. So if the path doesn't overshoot y, it won't overshoot the end. So we need to check if there is a path from s to y that doesn't overshoot y. This is equivalent to: can we represent y - s as a sum of numbers in [A,B] such that all partial sums are <= y - s? Actually, the partial sums of the jumps are the distances traveled. The positions visited are s + (partial sum). So we need s + (partial sum) <= end of G_cur for all partial sums. Since s >= start of G_cur, and partial sum >= 0, the condition s + partial sum <= end of G_cur is automatically satisfied if s + (final sum) <= end of G_cur, i.e., y <= end of G_cur. But what about intermediate partial sums? They could be greater than y - s? No, they are increasing. So the maximum partial sum is the final sum, which is y - s. So s + (partial sum) <= s + (y - s) = y <= end of G_cur. So the condition is automatically satisfied. The only issue is if the path requires landing on positions that are below start of G_cur. But since s >= start of G_cur, and we only move forward, we will never go below start. So the only condition is that the path is valid (i.e., y - s is representable) and s <= y. So we can just check: for each y in W_cur, if there exists s in `entry` such that y >= s and y - s is representable, then y is reachable. But wait, we also need to consider that we might make multiple jumps from s, and the first jump might land outside G_cur? But s is in G_cur, and the first jump is at most B. If s + B > end of G_cur, we might land outside G_cur. But that would be invalid. However, if we are using the representability check, we are assuming we can make jumps in [A,B] that sum to y - s. But the first jump might be B, and s+B might be > end of G_cur. But then we would be landing in the next bad interval, which is invalid. So we need to ensure that all intermediate positions are in G_cur. So the representability check is not sufficient; we need to ensure that the path stays within G_cur. This is a bounded reachability problem. However, we can avoid this issue by noting that we only care about reaching y in W_cur, and W_cur is at the end of G_cur. So if s is in G_cur, and we want to reach y which is near the end, the path will likely be near the end. But to be safe, we can just do a BFS from `entry` within G_cur, but we only explore positions up to the end of W_cur. Since W_cur is small, we can just BFS from `entry` and only push positions that are in G_cur and <= end of W_cur. The number of positions we push is bounded by the length of G_cur from the smallest entry to the end of W_cur. This could be large if G_cur is long and `entry` is near the start. So we need a better way.
   - The standard solution avoids this by not doing a BFS within the good interval. Instead, it uses a DP on the "positions modulo something" or it uses a greedy approach. I recall that the solution is to BFS on the "state" which is the set of reachable positions in the last B positions of the current good interval. And to compute the next set, we do: for each position in the current set, we add A..B, and if the result is in the next good interval, we add it. Then we also add positions that are reachable by multiple jumps within the next good interval. But we can compute the closure by noting that if we have a reachable position at x, then we can also reach x+1 if we can jump B from somewhere? Not exactly.
   Let me search for the exact algorithm. I think the key is that we can represent the state as a bitmask of which of the last B positions are reachable. And we can update the bitmask by shifting and adding new positions. Specifically, let the good interval be [l, r]. We maintain a set of reachable positions in [r-B+1, r]. We can represent this as a boolean array of size B. When we move to the next good interval, we need to update this array. The rule is: from a reachable position x in the previous good interval, we can jump to x+j. The new reachable positions in the next good interval are those. Then, from those new positions, we can make additional jumps. But we can simulate the BFS within the next good interval by using a BFS on the positions, but we only care about the last B positions. So we can just do a BFS from the new positions, but we only push positions that are <= r (the end of the good interval). Since the good interval could be long, we need to limit the BFS. The trick is to stop the BFS when the distance from the current position to the end is less than A? Not sure.
   - Another approach: Since the jumps are small, we can use a BFS on the "distance" from the start of the good interval, but we cap the distance at something. Actually, the problem is known to be solvable by BFS with a queue, and the number of visited nodes is at most M * B. The reason is that we only visit positions that are within B of the end of each good interval. So we can implement the BFS as follows:
        We have a global queue. We start with position 1.
        We also have a "current maximum" which is the right endpoint of the current bad interval + B. We update this maximum as we process the bad intervals.
        We do a BFS, but we only push positions y if y <= current_maximum. We also need to ensure that we don't push positions that are in the current good interval but too far left? Actually, the BFS will naturally explore positions in order. We can stop pushing when we exceed the current maximum.
        But we also need to ensure that we don't miss positions that are > current_maximum but could be reached later? No, because we increase the maximum as we process bad intervals.
        So the algorithm: 
            cur_max = min(N, R_1 + B)
            q = [1]
            visited = {1}
            while q:
                x = q.pop(0)
                for d in range(A, B+1):
                    y = x + d
                    if y > N: break
                    if y == N: print("Yes"); return
                    if y > cur_max: continue
                    if is_bad(y): continue
                    if y not in visited:
                        visited.add(y)
                        q.append(y)
            # after this, we have visited all positions <= cur_max that are reachable.
            # now process the next bad interval
            for i in range(1, M):
                # the next good interval is [R_i+1, L_{i+1}-1] (for i < M-1) or [R_M+1, N] (for i = M-1)
                # we need to continue BFS from visited positions in this good interval
                # but we also need to include positions that are in this good interval but we haven't visited because they are > cur_max
                # so we set new_cur_max = min(N, R_{i+1} + B) (for i < M-1) or N (for i = M-1)
                # and we start a new BFS from the visited positions in the good interval
                new_q = []
                for x in visited:
                    if R_i+1 <= x <= L_{i+1}-1:  # for i < M-1
                        new_q.append(x)
                    elif i == M-1 and x >= R_M+1:
                        new_q.append(x)
                cur_max = min(N, R_{i+1} + B) if i < M-1 else N
                q = new_q
                while q:
                    x = q.pop(0)
                    for d in range(A, B+1):
                        y = x + d
                        if y > N: break
                        if y == N: print("Yes"); return
                        if y > cur_max: continue
                        if is_bad(y): continue
                        if y not in visited:
                            visited.add(y)
                            q.append(y)
            # after processing all bad intervals, we have visited all positions <= R_M + B that are reachable.
            # now check if we can reach N from the visited positions in the last good interval
            for x in visited:
                if x >= R_M+1:
                    if is_representable(N - x):
                        print("Yes"); return
            print("No")
   - This algorithm has a problem: when we do the BFS in the i-th phase, we only push positions y that are <= cur_max. But what if there are positions in the good interval that are > cur_max but we need to reach them to eventually reach N? For example, if the last good interval is long, and we have a reachable position at the start of it, we might not be able to reach N because we didn't explore the middle. But we have the final check with is_representable, which handles that. So the only issue is if we need to reach a position in the last good interval that is > R_M+B? But we set cur_max to N for the last phase, so we explore all positions up to N. But that could be huge. So we need to set cur_max appropriately for the last phase. Actually, for the last phase, we don't need to explore all positions up to N. We just need to know which positions in the last good interval are reachable. We can compute that by checking from the entry points. So we can set cur_max = R_M + B for the last phase as well, and then do the final check. That is, we don't need to do a BFS for the last good interval. We just need to know the reachable positions in the last good interval that are <= R_M + B. So we can process the bad intervals up to M-1, and for the last one, we just do the final check. So we can modify the loop to process i=1 to M-1, and after the loop, do the final check. So the last BFS phase is for i = M-1, but we set cur_max = R_M + B, and we only push positions y that are <= R_M + B. Then we don't need to do a BFS for the last good interval; we just check the visited positions in the last good interval.
   - But wait: in the BFS for i = M-1, we are exploring positions in the good interval G_{M-1} and maybe the last good interval G_M? Actually, for i = M-1, the bad interval is [L_M, R_M]. The good interval before it is G_{M-1} = [R_{M-1}+1, L_M-1]. The good interval after it is G_M = [R_M+1, N]. When we do the BFS for i = M-1, we start from visited positions in G_{M-1} (and maybe earlier). We set cur_max = R_M + B. So we will explore positions in G_{M-1} and also positions in G_M that are <= R_M + B. That is, we will explore the part of G_M that is within B of its start. So we will have visited positions in G_M that are in [R_M+1, R_M+B]. Then we do the final check: for each visited x in G_M (i.e., x >= R_M+1), check if N - x is representable. This is correct because from those x, we can make additional jumps within G_M to reach N if the distance is representable. So we don't need to explore further in G_M.
   - So the algorithm works if we set the cur_max for each phase to be R_i + B, where R_i is the right endpoint of the i-th bad interval. And we start the BFS for phase i from the visited positions in the good interval before the i-th bad interval. But we need to ensure that we don't lose visited positions that are in earlier good intervals but could be used to jump to the current good interval? Actually, once we have processed a bad interval, we no longer need positions that are before that bad interval, because they cannot help us cross the next bad interval (since the next bad interval is further to the right, and jumps are forward). So we can discard them. So we can just keep the visited positions that are in the current good interval.
   - However, there is a subtlety: when we do the BFS for phase i, we might have visited positions in the good interval G_{i-1} that are useful. But we also might have visited positions in G_{i-2} that are not in G_{i-1}. Those cannot jump to G_i because they are separated by two bad intervals. So we only need to keep visited positions in G_{i-1}. So in the loop, we only push visited positions that are in G_{i-1} into the new queue.
   - So the algorithm is:
        1. Read inputs.
        2. If M == 0: check representability of N-1. Print Yes/No.
        3. Else:
            - bad = list of (L_i, R_i)
            - function is_bad(y): binary search in bad to check if y is in any interval.
            - function is_representable(D): precompute rep up to 400, then use min_rep array.
            - visited = set()
            - q = deque([1])
            - visited.add(1)
            - cur_max = min(N, bad[0][1] + B)  # R_0 + B
            - While q not empty:
                pop x
                for d in range(A, B+1):
                    y = x + d
                    if y > N: break
                    if y == N: print("Yes"); return
                    if y > cur_max: continue
                    if is_bad(y): continue
                    if y not in visited:
                        visited.add(y)
                        q.append(y)
            - For i from 1 to M-1:
                # good interval before this bad interval: [R_{i-1}+1, L_i-1]
                # good interval after: [R_i+1, L_{i+1}-1] for i < M-1
                # we need to continue BFS from visited positions in the good interval before
                new_q = deque()
                l_good = bad[i-1][1] + 1
                r_good = bad[i][0] - 1
                for x in visited:
                    if l_good <= x <= r_good:
                        new_q.append(x)
                cur_max = min(N, bad[i][1] + B) if i < M-1 else N  # actually for i=M-1, we don't need to BFS, we can just set cur_max = bad[M-1][1] + B
                # but careful: for i=M-1, the next good interval is the last one, so we don't have a next bad interval. So we don't need to increase cur_max beyond bad[M-1][1]+B.
                # So for i from 1 to M-1:
                #    cur_max = min(N, bad[i][1] + B)
                #    new_q = positions in visited that are in [bad[i-1][1]+1, bad[i][0]-1]
                #    BFS with cur_max
                # After the loop, we have visited positions up to bad[M-1][1]+B.
                # Then check last good interval: [bad[M-1][1]+1, N]
                # For each x in visited with x >= bad[M-1][1]+1, check if N - x is representable.
            - But wait: in the BFS for phase i, we are using cur_max = R_i + B. But we also need to include positions that are in the good interval after the i-th bad interval? Actually, for phase i, we are crossing the i-th bad interval. The positions we can land on are in the good interval after it, which is [R_i+1, L_{i+1}-1] (for i < M-1). The maximum position we can land on is R_i + B? Actually, from a position in the good interval before, we can jump up to B. So the maximum landing position is (L_i - 1) + B. But L_i - 1 <= R_i, so (L_i - 1) + B <= R_i + B. So the maximum landing position is at most R_i + B. So setting cur_max = R_i + B is safe. It might be larger than L_{i+1}-1, but we will check is_bad for positions > L_{i+1}-1? Actually, positions between L_{i+1}-1 and R_i+B might be in the next bad interval or after it. But we are only interested in positions in the good interval after the i-th bad interval. So we can just set cur_max = min(N, R_i + B) and then in the BFS, we check is_bad. So if a position is in the next bad interval, it will be marked as bad and skipped. So it's fine.
            - However, we also need to consider that we might need to explore positions in the good interval after the i-th bad interval that are > R_i + B? No, because to land in the good interval after, we need to jump from the good interval before. The maximum jump is B, so we can't land beyond R_i + B. So we don't need to explore beyond R_i + B for that phase.
            - So the algorithm is correct.
   - But we still have the problem that the BFS might explore a lot of positions in a long good interval before the first bad interval. For example, if the first bad interval is at L_1 = 10^12 - 10, and N = 10^12, then G_0 is [1, 10^12 - 11]. The BFS from 1 with cur_max = R_1 + B = (10^12 - 10) + 20 = 10^12 + 10, capped at N = 10^12. So cur_max = 10^12. The BFS will explore all reachable positions in G_0 up to 10^12. That's 10^12 operations. So we need to avoid that. The solution is to not BFS through the entire G_0. Instead, we should only BFS through the "tail" of G_0. So we need to set cur_max to something much smaller. The correct cur_max for the first phase should be the maximum position in G_0 that is useful for crossing the first bad interval. That is, we only need to explore positions in G_0 that are >= R_1+1 - B. So we can set cur_max = R_1 + B, but we also need to ensure that we don't explore positions in G_0 that are < R_1+1 - B. How to do that? We can start the BFS from 1, but we only push positions that are <= R_1 + B. But we still might have to explore many positions to reach the tail. For example, if the tail is at 10^12 - 100, and we start at 1, we might have to explore many positions to reach there. But we can use the fact that in G_0, there are no bad squares. So we can just check directly which positions in the tail are reachable. So we can do: for the first phase, instead of BFS, we can just compute the set of reachable positions in the tail W_0 = [max(1, R_1+1-B), L_1-1] by checking representability. So we don't need to BFS from 1 through the whole G_0. We can just set `cur` = { x in W_0 | x-1 is representable }. Then we proceed to the next phase.
   - For the subsequent phases, we have a set `cur` of reachable positions in the tail of the current good interval. To compute the next set, we do:
        - entry = set()
        - for x in cur:
            for j in range(A, B+1):
                y = x + j
                if y in next_good_interval:  # i.e., y >= R_i+1 and y <= L_{i+1}-1
                    entry.add(y)
        - Then, from entry, we want to compute the set of reachable positions in the next tail W_next. This is a BFS within the next good interval. But since the next good interval has no bad squares, we can do: for each y in W_next, check if there exists s in entry such that y - s is representable. So we can compute the next set as: for y in W_next, if any(s in entry, y >= s and is_representable(y-s)), then add y to next set.
   - This is O(B^2) per phase, and we have M phases, so total O(M * B^2). This is efficient.
   - We also need to handle the last good interval. For the last good interval, we don't have a next tail. Instead, we need to check if N is reachable. We can do: for each x in the last set (which are in the tail of the last good interval before the last bad interval, or maybe we have a set in the last good interval? Actually, after processing the last bad interval, we have a set `cur` that is in the tail of the last good interval before the last bad interval? No, after processing the last bad interval, we have a set of reachable positions in the good interval after the last bad interval, which is the last good interval G_M. But we only computed the set in the tail of G_M? Actually, in the step for the last bad interval, we compute the set for the next good interval's tail. So after that, we have a set of reachable positions in the tail of G_M. Then we can check if N is reachable from any of those positions. So we can just do: for x in cur (which are in G_M's tail), check if is_representable(N - x). If yes, print Yes.
   - But what if the last good interval is so long that the tail is not enough? Actually, the tail of G_M is defined as [max(start of G_M, N - B + 1?), wait, for the last good interval, there is no next bad interval. So we don't have a "useful tail" for crossing. Instead, we just need to know if we can reach N. So we can just compute the reachable set in the entire last good interval? But that could be long. However, we can use the same trick: we only need to check if N is reachable from the entry points. So we can just take the entry points into G_M (which we computed as `entry` in the last step), and then check if N is reachable from any of them. But we might also have made multiple jumps within G_M. So we need to check if N is reachable from the set of all reachable positions in G_M. That is exactly: for each x in the reachable set in G_M, check if N - x is representable. But we don't have the full reachable set. However, we can compute the reachable set in the tail of G_M that is relevant for reaching N. Since to reach N, we need a position x in G_M such that N - x is representable. That means x must be in [N - B, N-1] (since the last jump must be in [A,B], so x must be at least N-B). So we only need to know which positions in [N-B, N-1] are reachable. And we can compute that by doing a BFS from the entry points, but we only explore positions in that range. Since the entry points are in G_M, and G_M is [R_M+1, N], the distance from the entry points to N-B could be large. But we can use the representability check: a position y in [N-B, N-1] is reachable from an entry point s if y - s is representable. So we can just check that. So we don't need to BFS through the whole G_M. We can just check for each y in [N-B, N-1] that is in G_M, and for each s in entry, if y - s is representable, then y is reachable. And then we can check if y == N? Actually, if y is in [N-B, N-1], then we can jump from y to N if the jump is exactly N-y, which is in [A,B] because y >= N-B. So if y is reachable, then N is reachable. So we can just check if there exists y in [max(R_M+1, N-B), N-1] such that y is reachable from entry. So we can compute the reachable set in that window.
   - So the algorithm for the last step: we have a set `entry` of positions in G_M that are reachable in one jump from the previous tail. We want to know if we can reach N. We can do: for y in [max(R_M+1, N-B), N-1], check if there exists s in entry such that y >= s and is_representable(y - s). If yes, print Yes. If no, print No.
   - So the full algorithm:
        1. Read inputs.
        2. If M == 0: check if is_representable(N-1). Print Yes/No.
        3. Else:
            - bad = [(L_i, R_i) for i in 1..M]
            - good intervals:
                G0 = [1, L1-1]
                for i=1 to M-1: G_i = [R_i+1, L_{i+1}-1]
                G_M = [R_M+1, N]
            - We will process from G0 to G_{M-1}. For each, we maintain a set `cur` of reachable positions in the tail W_i of G_i.
            - The tail W_i is defined as the set of positions in G_i that are within B of the start of the next good interval. That is:
                For i=0: W0 = [max(1, R1+1-B), L1-1]
                For i=1 to M-1: W_i = [max(R_{i-1}+1, R_i+1-B), L_{i+1}-1]? Wait, careful: The next good interval after G_i is G_{i+1} (for i < M-1). So the start of G_{i+1} is R_{i+1}+1. So the tail of G_i is [max(start of G_i, R_{i+1}+1-B), end of G_i]. For i=0, start of G_0 is 1, end is L1-1, next good interval is G1, start of G1 is R1+1. So W0 = [max(1, R1+1-B), L1-1].
                For i=1, G1 start is R1+1, end is L2-1, next good interval is G2, start of G2 is R2+1. So W1 = [max(R1+1, R2+1-B), L2-1].
                In general, for i from 0 to M-2: W_i = [max(start of G_i, R_{i+1}+1-B), end of G_i].
                For i = M-1, G_{M-1} is before the last bad interval. The next good interval is G_M. So W_{M-1} = [max(start of G_{M-1}, R_M+1-B), end of G_{M-1}]. But note that end of G_{M-1} is L_M-1. So W_{M-1} = [max(R_{M-1}+1, R_M+1-B), L_M-1].
            - The size of each W_i is at most B.
            - Step 0: Compute `cur` for G0.
                cur = set()
                for x in W0:
                    if is_representable(x-1):  # x-1 >= 0
                        cur.add(x)
                If cur is empty, then we cannot cross the first bad interval. So we can print No? But wait, maybe we can still reach N by some other path? No, because to get to any other good interval, we must cross the first bad interval. So if cur is empty, we cannot reach N. But careful: what if the first bad interval is not the only obstacle? Actually, if we cannot reach any position in W0, then we cannot cross the first bad interval. But could we reach N without crossing the first bad interval? N is to the right of all bad intervals, so we must cross all bad intervals. So if we can't cross the first, we can't reach N. So we can immediately print No if cur is empty. But there is an edge case: what if the first bad interval is before 1? No, L_i > 1. So 1 is in G0. So we start in G0. So we need to reach W0. So if cur is empty, print No.
            - For i from 1 to M-1:
                - We have `cur` for G_{i-1}. We want to compute `next_cur` for W_i.
                - First, compute the set of positions in G_i that can be reached in one jump from `cur`. That is:
                    entry = set()
                    for x in cur:
                        for j in range(A, B+1):
                            y = x + j
                            if y in G_i:  # i.e., R_{i-1}+1 <= y <= L_i-1? Wait, G_i is [R_{i-1}+1, L_i-1] for i=1..M-1? Actually, G1 = [R1+1, L2-1], G2 = [R2+1, L3-1], etc. So for i, G_i = [R_{i-1}+1, L_i-1]? Check: i=1: R0+1? There is no R0. So better to use the bad intervals: G0 = [1, L1-1], G1 = [R1+1, L2-1], G2 = [R2+1, L3-1], ..., G_{M-1} = [R_{M-1}+1, L_M-1], G_M = [R_M+1, N].
                    So for i from 1 to M-1, G_i = [R_{i-1}+1, L_i-1]? Actually, for i=1, G1 = [R1+1, L2-1]. So it should be [R_i+1, L_{i+1}-1]? Let's index properly:
                        Bad intervals: 1 to M.
                        G0: before bad 1.
                        G1: between bad 1 and 2: [R1+1, L2-1]
                        G2: between bad 2 and 3: [R2+1, L3-1]
                        ...
                        G_{M-1}: between bad M-1 and M: [R_{M-1}+1, L_M-1]
                        G_M: after bad M: [R_M+1, N]
                    So for i=1..M-1, G_i = [R_i+1, L_{i+1}-1]. (Note: R_i is the right endpoint of bad interval i.)
                    So entry should be positions in G_i. So condition: R_i+1 <= y <= L_{i+1}-1.
                    So:
                        for x in cur:
                            for j in range(A, B+1):
                                y = x + j
                                if y >= R_i+1 and y <= L_{i+1}-1:
                                    entry.add(y)
                - Then, from entry, we want to compute the reachable positions in W_i. W_i is the tail of G_i: [max(R_i+1, R_{i+1}+1-B), L_{i+1}-1]? Wait, the next good interval after G_i is G_{i+1} (for i < M-1). So the start of G_{i+1} is R_{i+1}+1. So the tail of G_i is [max(R_i+1, R_{i+1}+1-B), L_{i+1}-1]. So W_i = [max(R_i+1, R_{i+1}+1-B), L_{i+1}-1]. For i = M-1, the next good interval is G_M, start of G_M is R_M+1. So W_{M-1} = [max(R_{M-1}+1, R_M+1-B), L_M-1].
                - So for i from 1 to M-1, we compute next_cur as:
                    next_cur = set()
                    for y in W_i:
                        # check if y is reachable from entry
                        for s in entry:
                            if y >= s and is_representable(y - s):
                                next_cur.add(y)
                                break
                - If next_cur is empty, then we cannot cross the next bad interval. So we can print No and return.
                - Set cur = next_cur.
            - After processing i=1 to M-1, we have `cur` for W_{M-1} (which is in G_{M-1}). Now we need to cross the last bad interval to get to G_M. So we compute entry for G_M:
                entry = set()
                for x in cur:
                    for j in range(A, B+1):
                        y = x + j
                        if y >= R_M+1 and y <= N:  # G_M = [R_M+1, N]
                            entry.add(y)
            - Now, we want to check if N is reachable from entry. We can check for y in [max(R_M+1, N-B), N-1]:
                for y in [max(R_M+1, N-B), N-1]:
                    for s in entry:
                        if y >= s and is_representable(y - s):
                            print("Yes"); return
            - Also, we should check if N is in entry? Actually, if we can jump directly to N, that would have been caught in the loop? But the loop only goes up to N-1. So we should also check if N is in entry. But if y = N, then N - s is representable? Actually, if we can jump from s to N in one jump, then N - s is in [A,B], which is representable. So we can include N in the range. So we can set the range to [max(R_M+1, N-B), N]. But careful: if N is in the range, and we find a s such that N - s is representable, then N is reachable. So we can set the range to [max(R_M+1, N-B), N]. But if N is in the range, we need to ensure that the path doesn't require landing on N-B? Actually, if N - s is representable, it could be a multi-step path. But the last step must be a jump in [A,B]. So if N - s is representable, there is a path. So it's fine. So we can check the range [max(R_M+1, N-B), N].
            - If no such y, print No.
   - This algorithm is O(M * B^2) and should be fast.
   - We need to implement is_representable(D) efficiently. We can precompute a set `rep` of representable numbers up to, say, 400. And also an array `min_rep` of size g (g = gcd(A,B)). For each number in `rep` that is a multiple of g, update min_rep[number % g] = min(min_rep[number % g], number). Then for a given D, if D < 0, return False. If D is in `rep`, return True. If D > 400, then if min_rep[D % g] is not infinity and D >= min_rep[D % g], return True. Else False.
   - But we need to be careful: the semigroup generated by [A,B] might not include all sufficiently large multiples of g. For example, A=4, B=6, g=2. The representable numbers are 0,4,6,8,10,12,... The non-representable even numbers are 2. So for residue 0 mod 2, the minimum representable is 0. For residue 1 mod 2, there is no representable number. So min_rep[0]=0, min_rep[1]=infinity. So for D=10, D%2=0, D>=0, so representable. For D=2, D%2=0, D>=0, but 2 is not representable. So our condition would incorrectly say representable because 2 >= 0. So we need to ensure that we only use the condition for D that are large enough. The condition should be: D is representable if D >= min_rep[D % g] and D > some threshold? Actually, the semigroup has a Frobenius number for the coprime case. For non-coprime, the set of representable numbers is exactly the set of numbers that are multiples of g and are >= some minimum for each residue. But the minimum might be 0 for some residues. For residue 0, 0 is representable, but 2 is not. So the condition D >= min_rep[r] is not sufficient. We need to ensure that D is actually in the semigroup. The semigroup is the set of all nonnegative integer combinations of A and B. This set is periodic with period g after some point. Specifically, there exists an integer N0 such that for all n >= N0, n is in the semigroup iff n is a multiple of g and n/g is in the semigroup generated by A/g and B/g. So we can just precompute the representable numbers up to N0, and then for larger n, check if n is a multiple of g and n/g is representable by the scaled semigroup. But since A/g and B/g are coprime, the scaled semigroup is a numerical semigroup. Its Frobenius number is (A/g)*(B/g) - (A/g) - (B/g). So we can precompute up to that Frobenius number + something. But A/g and B/g are at most 20, so their product is at most 400. So we can just precompute all representable numbers up to 400 * 2 = 800 or so. Then for any D, if D is in that set, return True. Else, if D is a multiple of g, then D/g is a number. We can check if D/g is in the scaled representable set. But we don't have that precomputed. Alternatively, we can just precompute the representable numbers up to 4000, and then for D > 4000, we can use a greedy algorithm? Actually, since A,B <= 20, we can just do a BFS on the state (D mod something) to check if D is representable. But the simplest is: since A,B are small, we can precompute a boolean array `is_rep` of size, say, 4000. Then for D > 4000, we can use the fact that if D is representable, then D - A and D - B are representable. But we need to check for large D efficiently. We can use a BFS on the residues modulo A? Not sure.
   - Actually, we can just precompute the representable numbers up to 4000, and then for D > 4000, we can do: if D % g == 0, then we can check if D/g is in the scaled semigroup. The scaled semigroup is generated by A/g and B/g. Since these are coprime, the Frobenius number is (A/g)*(B/g) - (A/g) - (B/g). So the largest non-representable number in the scaled semigroup is that. So we can precompute the scaled representable numbers up to that Frobenius number. Then for D, if D/g > that Frobenius number, then D/g is representable. So D is representable. If D/g <= that, we can check in the precomputed set. So we can do that.
   - But maybe we don't need to be that fancy. Since we are only checking representability for D up to something like 10^12, and we have to do it many times, we need an O(1) or O(log) check. We can precompute the representable numbers up to 4000, and then for D > 4000, we can check: if D % g == 0, then D/g is an integer. We can check if D/g is in the set {k * (A/g) + l * (B/g) | k,l >= 0}. This is equivalent to checking if D/g is in the semigroup generated by A/g and B/g. Since A/g and B/g are coprime, the semigroup contains all integers >= (A/g)*(B/g). So we can just check if D/g >= (A/g)*(B/g) - (A/g) - (B/g) + 1? Actually, the Frobenius number is the largest non-representable. So if D/g > Frobenius, then it is representable. So we can just compute the Frobenius number for the coprime pair (A/g, B/g) and use that. So the condition for D > 4000 is: if D % g == 0 and D/g > (A/g)*(B/g) - (A/g) - (B/g), then D is representable. But wait, the Frobenius number is for two coprime numbers. So we need to compute g = gcd(A,B). Then a = A/g, b = B/g. They are coprime. The Frobenius number is a*b - a - b. Then for D, if D is a multiple of g, let D' = D/g. If D' > a*b - a - b, then D' is representable by a and b. So D is representable. If D' <= a*b - a - b, we can check by precomputing a set for D' up to a*b. So we can precompute a set `rep_scaled` of representable numbers for the scaled semigroup up to a*b. Then for D, we compute D' = D/g. If D' is in `rep_scaled`, return True. If D' > a*b - a - b, return True. Else return False.
   - This is exact and efficient.
   - So we can implement is_representable(D) as:
        if D < 0: return False
        g = gcd(A,B)
        if D % g != 0: return False
        D_prime = D // g
        a = A // g
        b = B // g
        # Frobenius number for a,b
        frob = a*b - a - b
        if D_prime > frob: return True
        # precompute rep_scaled for numbers up to frob
        return D_prime in rep_scaled_set
   - We can precompute rep_scaled by BFS up to frob.
   - This should work.
   - Now, we also need to handle the case where the first bad interval is not present? That's M=0, handled separately.
   - Let's test the algorithm on the samples.
   Sample 1: N=24, M=2, A=3, B=5, bad: [7,8], [17,20]
        G0 = [1,6]
        G1 = [9,16]  (since R1=8, L2=17, so R1+1=9, L2-1=16)
        G2 = [21,24] (R2=20, so R2+1=21, N=24)
        W0 = [max(1, R1+1-B), L1-1] = [max(1, 8+1-5=4), 6] = [4,6]
        cur for G0: check x in [4,6] if x-1 is representable.
            x=4: 3 is representable? 3 is in [A,B]? A=3, so yes.
            x=5: 4 is representable? 4 is not in [3,5]? 4 is in [3,5], so yes.
            x=6: 5 is in [3,5], so yes.
        So cur = {4,5,6}
        i=1: G1 = [9,16], W1 = tail of G1: next good interval is G2, start of G2 = 21. So W1 = [max(9, 21-5=16), 16] = [16,16]. So W1 = {16}.
        entry for G1: from cur={4,5,6}, jumps 3,4,5:
            from 4: 7,8,9 -> 9 is in G1? 9>=9 and 9<=16, so add 9.
            from 5: 8,9,10 -> add 9,10
            from 6: 9,10,11 -> add 9,10,11
        So entry = {9,10,11}
        Now, compute next_cur for W1={16}:
            check if 16 is reachable from entry:
                for s in entry: 16-9=7, representable? 7 = 3+4, yes. So 16 is reachable.
        So cur = {16}
        i=2: G2 = [21,24], this is the last good interval. We don't compute W2. We compute entry for G2:
            from cur={16}, jumps 3,4,5:
                16+3=19, 16+4=20, 16+5=21. 21 is in G2? 21>=21 and 21<=24, so add 21.
        So entry = {21}
        Now check if N=24 is reachable: range [max(21, 24-5=19), 24] = [21,24].
            y=21: 21 is in entry, but we need to check if we can reach 24 from 21. 24-21=3, which is representable. So we can check: for y=24, check if 24 is reachable from entry? Actually, we check for y in [21,24]:
                y=21: check if 21 is reachable from entry? 21 is in entry, so we can consider 21 as a starting point. But we want to know if 24 is reachable. So we should check for y such that from y we can jump to 24. So we need y in [24-5, 23] = [19,23]. But 21 is in that range. So we can do: for y in [21,23] (since 24-5=19, but 19 is not in G2), check if y is reachable from entry. Then if y is reachable, we can jump to 24. So we need to check if any y in [21,23] is reachable from entry. For y=21, 21 is in entry, so it's reachable. Then from 21, we can jump 3 to 24. So we should print Yes.
        So algorithm: for the last step, we have entry. We want to check if N is reachable. We can do: for y in [max(R_M+1, N-B), N-1] (since from y we can jump to N if N-y in [A,B]), check if y is reachable from entry. If yes, print Yes. Also, if N is in entry, we can also check that. But if N is in entry, that means we can jump directly to N, so we should print Yes. So we can include N in the range? Actually, if N is in entry, then we can reach N directly. So we can just check if N is in entry. So the final check: 
            if N in entry: print Yes
            else:
                for y in [max(R_M+1, N-B), N-1]:
                    for s in entry:
                        if y >= s and is_representable(y - s):
                            print Yes; return
        In our example, entry={21}. N=24, not in entry. Range: [max(21, 24-5=19), 23] = [21,23]. For y=21, s=21, y-s=0, representable? 0 is representable (empty sum). So we can say 21 is reachable from 21. So y=21 is reachable. Then from 21, we can jump 3 to 24. So we should print Yes.
        But wait, is 0 representable? Usually, a sum of zero numbers is 0. So we can consider 0 representable. So we should have is_representable(0) = True. So that works.
        So the algorithm prints Yes.
   Sample 2: N=30, M=1, A=5, B=8, bad: [4,24]
        G0 = [1,3]
        G1 = [25,30]  (R1=24, so R1+1=25, N=30)
        W0 = [max(1, R1+1-B), L1-1] = [max(1, 25-8=17), 3] = [17,3] which is empty. So W0 is empty.
        cur for G0: no positions to check. So cur is empty. So we cannot cross the first bad interval. Print No.
        Correct.
   Sample 3: N=100, M=4, A=10, B=11, bad: [16,18], [39,42], [50,55], [93,99]
        Let's compute:
        G0 = [1,15]
        G1 = [19,38] (R1=18, L2=39 -> R1+1=19, L2-1=38)
        G2 = [43,49] (R2=42, L3=50 -> R2+1=43, L3-1=49)
        G3 = [56,92] (R3=55, L4=93 -> R3+1=56, L4-1=92)
        G4 = [100,100] (R4=99, so R4+1=100, N=100)
        W0 = [max(1, R1+1-B), L1-1] = [max(1, 19-11=8), 15] = [8,15]
        cur for G0: check x in [8,15] if x-1 is representable.
            A=10, B=11. Representable numbers: 0,10,11,20,21,22,30,... 
            x-1: for x=8, 7 not representable. x=9,8 no. x=10,9 no. x=11,10 yes. x=12,11 yes. x=13,12 no. x=14,13 no. x=15,14 no.
            So cur = {11,12}
        i=1: G1 = [19,38], W1 = tail of G1: next good G2 start=43, so W1 = [max(19, 43-11=32), 38] = [32,38]
        entry for G1: from cur={11,12}, jumps 10,11:
            from 11: 21,22 -> 21,22 in G1? 19<=21,22<=38, so add 21,22.
            from 12: 22,23 -> add 22,23.
        entry = {21,22,23}
        Compute next_cur for W1=[32,38]:
            for y in [32,38]:
                check if reachable from entry:
                    y=32: from 21, 32-21=11 representable? 11 is in [10,11], yes. So 32 reachable.
                    y=33: 33-22=11, yes.
                    y=34: 34-23=11, yes.
                    y=35: 35-24? but 24 not in entry. Actually, we need to check each s. For y=35, s=21: 14 not rep. s=22:13 no. s=23:12 no. So 35 not reachable.
                    y=36: 36-21=15 no, 36-22=14 no, 36-23=13 no.
                    y=37: 37-21=16 no, 37-22=15 no, 37-23=14 no.
                    y=38: 38-21=17 no, 38-22=16 no, 38-23=15 no.
            So next_cur = {32,33,34}
        i=2: G2 = [43,49], W2 = tail of G2: next good G3 start=56, so W2 = [max(43, 56-11=45), 49] = [45,49]
        entry for G2: from cur={32,33,34}, jumps 10,11:
            from 32: 42,43 -> 43 in G2? 43<=49, so add 43.
            from 33: 43,44 -> add 43,44.
            from 34: 44,45 -> add 44,45.
        entry = {43,44,45}
        Compute next_cur for W2=[45,49]:
            y=45: from 43, 45-43=2 no; from 44, 1 no; from 45, 0 yes. So 45 reachable.
            y=46: 46-43=3 no, 46-44=2 no, 46-45=1 no.
            y=47: 47-43=4 no, 47-44=3 no, 47-45=2 no.
            y=48: 48-43=5 no, 48-44=4 no, 48-45=3 no.
            y=49: 49-43=6 no, 49-44=5 no, 49-45=4 no.
        So next_cur = {45}
        i=3: G3 = [56,92], W3 = tail of G3: next good G4 start=100, so W3 = [max(56, 100-11=89), 92] = [89,92]
        entry for G3: from cur={45}, jumps 10,11:
            45+10=55, 45+11=56 -> 56 in G3? 56<=92, so add 56.
        entry = {56}
        Compute next_cur for W3=[89,92]:
            y=89: 89-56=33, representable? 33=11+11+11, yes. So 89 reachable.
            y=90: 90-56=34= ? 10+10+14? 14 not rep. 11+11+12? 12 not. 10+10+10+4? 4 not. Actually, 34 is not representable with 10 and 11? 10+10+10+4 no, 11+11+12 no. So 34 not rep. But maybe 10+11+13 no. So 34 not rep. So 90 not reachable.
            y=91: 91-56=35, not rep.
            y=92: 92-56=36, not rep.
        So next_cur = {89}
        i=4: G4 = [100,100], last good interval. entry for G4: from cur={89}, jumps 10,11:
            89+10=99, 89+11=100 -> 100 in G4? 100<=100, so add 100.
        entry = {100}
        Now check N=100: N is in entry, so print Yes.
        Correct.
   - So the algorithm works on the samples.
   - Now, we need to implement it efficiently in Python.
   - Steps:
        1. Read N, M, A, B.
        2. Read bad intervals into lists L, R.
        3. Precompute is_representable(D) function.
        4. If M == 0: if is_representable(N-1): Yes else No.
        5. Else:
            - Define good intervals:
                G0: [1, L[0]-1]
                For i in range(M-1): G_{i+1} = [R[i]+1, L[i+1]-1]
                G_M: [R[M-1]+1, N]
            - But we don't need to store all; we can process on the fly.
            - We will maintain a set `cur` for the current tail.
            - For the first step:
                W0_start = max(1, R[0]+1-B)
                W0_end = L[0]-1
                cur = set()
                for x in range(W0_start, W0_end+1):
                    if is_representable(x-1):
                        cur.add(x)
                if not cur: print No; return
            - For i from 1 to M-1:
                # G_i = [R[i-1]+1, L[i]-1]  (since i is 1-indexed in the loop, but careful)
                # Actually, for the i-th step (i=1..M-1), we are processing G_i.
                # G_i: start = R[i-1]+1, end = L[i]-1.
                # W_i: start = max(start, R[i]+1-B)  (since next good interval is G_{i+1} = [R[i]+1, L[i+1]-1], so start of next is R[i]+1)
                # W_i: end = L[i]-1
                # So:
                gi_start = R[i-1] + 1
                gi_end = L[i] - 1
                wi_start = max(gi_start, R[i] + 1 - B) if i < M-1 else max(gi_start, R[M-1] + 1 - B)  # actually for i=M-1, the next is G_M, so use R[M-1]+1-B
                wi_end = gi_end
                # Compute entry
                entry = set()
                for x in cur:
                    for d in range(A, B+1):
                        y = x + d
                        if gi_start <= y <= gi_end:
                            entry.add(y)
                if not entry: print No; return
                # Compute next_cur
                next_cur = set()
                for y in range(wi_start, wi_end+1):
                    found = False
                    for s in entry:
                        if y >= s and is_representable(y - s):
                            found = True
                            break
                    if found:
                        next_cur.add(y)
                if not next_cur: print No; return
                cur = next_cur
            - Now, for the last good interval G_M = [R[M-1]+1, N]:
                # Compute entry for G_M
                entry = set()
                for x in cur:
                    for d in range(A, B+1):
                        y = x + d
                        if y >= R[M-1]+1 and y <= N:
                            entry.add(y)
                if not entry: print No; return
                # Check if N is reachable
                if N in entry: print Yes; return
                # Check range
                check_start = max(R[M-1]+1, N - B)
                for y in range(check_start, N):
                    for s in entry:
                        if y >= s and is_representable(y - s):
                            print Yes; return
                print No
   - We need to be careful with indices: in the loop for i from 1 to M-1, i is the index of the good interval G_i. The bad intervals are 0-indexed in our list. So when i=1, we are processing G_1 = [R[0]+1, L[1]-1]. The next good interval is G_2 = [R[1]+1, L[2]-1]. So the start of the next good interval is R[1]+1. So the tail W_1 should use R[1]+1-B. So in the loop, for i (1-indexed), we need to use R[i] for the next bad interval? Actually, for G_i, the next bad interval is i (since G_i is between bad i and i+1? Wait, careful: G_0 is before bad 1. G_1 is between bad 1 and 2. So for G_i, the next bad interval is i+1? Actually, G_i is followed by bad interval i+1? No: G_0 is followed by bad 1. G_1 is followed by bad 2. So in general, G_i is followed by bad interval i+1. So to cross from G_i to G_{i+1}, we need to jump over bad interval i+1. So the start of G_{i+1} is R[i+1]+1? Wait, G_{i+1} is between bad i+1 and i+2. So G_{i+1} = [R[i+1]+1, L[i+2]-1]. So the start of G_{i+1} is R[i+1]+1. So for G_i, the useful tail is determined by the start of G_{i+1}, which is R[i+1]+1. So in the loop for i from 1 to M-1, we are processing G_i. The next good interval is G_{i+1}, and its start is R[i+1]+1. So we need to use R[i+1] (if i+1 < M). For i = M-1, the next good interval is G_M, start of G_M is R[M-1]+1. So we can unify by using an index for the "next" start. Let's define:
        For i from 0 to M-1:
            G_i: start_i, end_i.
            next_start_i: the start of the next good interval. For i=0, next_start = R[0]+1. For i=1..M-2, next_start = R[i]+1? Actually, for G_i, the next good interval is G_{i+1}. For i=0, G_1 start = R[0]+1. For i=1, G_2 start = R[1]+1. So in general, for G_i, next_start = R[i]+1. Because G_i is between bad i and i+1? Wait, G_0 is before bad 1, so the next bad is 1, and G_1 starts at R[1]+1? No, G_1 is between bad 1 and 2, so it starts at R[1]+1. So for G_0, the next good interval is G_1, which starts at R[1]+1. So next_start for G_0 is R[1]+1. For G_1, next good is G_2, start R[2]+1. So next_start for G_i is R[i+1]+1. For G_{M-1}, next good is G_M, start R[M-1]+1. So we can write:
            For i in range(M):
                if i == 0: G0 = [1, L[0]-1], next_start = R[0]+1
                elif i < M-1: G_i = [R[i-1]+1, L[i]-1], next_start = R[i]+1
                else: G_{M-1} = [R[M-2]+1, L[M-1]-1], next_start = R[M-1]+1
            This is messy. Better to process the good intervals in order, and for each, we know the start and end, and the start of the next good interval.
   - We can restructure the code to be clearer.
   - Let's define the good intervals as a list of tuples (start, end). We can compute them once:
        goods = []
        goods.append((1, L[0]-1))
        for i in range(M-1):
            goods.append((R[i]+1, L[i+1]-1))
        goods.append((R[M-1]+1, N))
   - So goods[0] is G0, goods[1] is G1, ..., goods[M] is G_M. There are M+1 good intervals.
   - For each good interval except the last, we need to compute the tail W_i = [max(goods[i][0], start of next good interval - B), goods[i][1]].
   - The start of the next good interval is goods[i+1][0].
   - So W_i_start = max(goods[i][0], goods[i+1][0] - B)
   - W_i_end = goods[i][1]
   - For the last good interval, we don't need a tail; we just check reachability to N.
   - So the algorithm:
        goods = [(1, L[0]-1)]
        for i in range(M-1):
            goods.append((R[i]+1, L[i+1]-1))
        goods.append((R[M-1]+1, N))
        # Now goods has M+1 intervals.
        # Step 0: compute cur for goods[0]
        W0_start = max(goods[0][0], goods[1][0] - B)
        W0_end = goods[0][1]
        cur = set()
        for x in range(W0_start, W0_end+1):
            if is_representable(x-1):
                cur.add(x)
        if not cur: print No; return
        # For i from 1 to M-1 (i.e., for goods[1] to goods[M-1])
        for i in range(1, M):
            # goods[i] is the current good interval
            gi_start, gi_end = goods[i]
            # next good interval is goods[i+1]
            wi_start = max(gi_start, goods[i+1][0] - B)
            wi_end = gi_end
            # compute entry
            entry = set()
            for x in cur:
                for d in range(A, B+1):
                    y = x + d
                    if gi_start <= y <= gi_end:
                        entry.add(y)
            if not entry: print No; return
            # compute next_cur
            next_cur = set()
            for y in range(wi_start, wi_end+1):
                found = False
                for s in entry:
                    if y >= s and is_representable(y - s):
                        found = True
                        break
                if found:
                    next_cur.add(y)
            if not next_cur: print No; return
            cur = next_cur
        # Now, for the last good interval goods[M]
        gm_start, gm_end = goods[M]
        # compute entry for goods[M]
        entry = set()
        for x in cur:
            for d in range(A, B+1):
                y = x + d
                if gm_start <= y <= gm_end:
                    entry.add(y)
        if not entry: print No; return
        # check if N is reachable
        if N in entry: print Yes; return
        check_start = max(gm_start, N - B)
        for y in range(check_start, N):
            for s in entry:
                if y >= s and is_representable(y - s):
                    print Yes; return
        print No
   - This should work. We need to ensure that the ranges are correct. Note that W0_start could be > W0_end, in which case cur is empty.
   - Also, we need to handle the case where M=0 separately because goods would be just [(1, N)]? Actually, if M=0, we don't have bad intervals. So we handle that at the beginning.
   - Now, we need to implement is_representable(D) efficiently. We'll precompute a set `rep` for numbers up to some bound. Since A,B <= 20, the maximum representable number we might need to check is the maximum distance in the good intervals. But the good intervals can be long, so D could be up to 10^12. So we need an O(1) check for large D.
   - As discussed, we can use the gcd trick.
   - Let's implement is_representable(D):
        from math import gcd
        g = gcd(A, B)
        if D < 0: return False
        if D % g != 0: return False
        D_prime = D // g
        a = A // g
        b = B // g
        # Frobenius number for a,b
        frob = a*b - a - b
        if D_prime > frob: return True
        # Precompute rep_scaled for numbers up to frob
        return D_prime in rep_scaled_set
   - We need to precompute rep_scaled_set. We can do a BFS up to frob. Since frob <= 400, we can just compute it.
   - But we also need to handle D=0. For D=0, we want True (empty sum). So we should have 0 in rep_scaled_set.
   - So precompute:
        rep_scaled = set()
        rep_scaled.add(0)
        queue = [0]
        while queue:
            x = queue.pop(0)
            for step in [a, b]:
                y = x + step
                if y <= frob and y not in rep_scaled:
                    rep_scaled.add(y)
                    queue.append(y)
   - This will generate all representable numbers up to frob.
   - Then is_representable(D) is as above.
   - We also need to handle the case where A and B are such that a or b is 1. If a=1, then all numbers are representable. If b=1, same. Then frob = 1*b - 1 - b = -1? Actually, if a=1, then every number is representable. So we can just return True if D%g==0. But our formula frob = a*b - a - b gives -1 if a=1? For a=1, b=20, frob = 20 - 1 - 20 = -1. So we can just say if a==1 or b==1, return True. So we can handle that.
   - So the implementation of is_representable:
        from math import gcd
        g = gcd(A, B)
        if D < 0: return False
        if D % g != 0: return False
        D_prime = D // g
        a = A // g
        b = B // g
        if a == 1 or b == 1: return True
        frob = a*b - a - b
        if D_prime > frob: return True
        # precompute rep_scaled up to frob
        return D_prime in rep_scaled_set
   - We'll precompute rep_scaled_set at the beginning.
   - One more thing: in the loops, we iterate over y in range(wi_start, wi_end+1). The range could be large if wi_start and wi_end are large. But we argued that wi_end - wi_start + 1 <= B. Let's verify: wi_start = max(gi_start, next_start - B). wi_end = gi_end. The length is gi_end - max(gi_start, next_start - B) + 1. Since gi_end = next_start - 1? Actually, gi_end is the end of G_i, and next_start is the start of G_{i+1}. They are separated by a bad interval. Specifically, G_i = [R_{i-1}+1, L_i-1]? Wait, careful: For G_i (i>=1), it is between bad i and i+1. So gi_start = R[i-1]+1, gi_end = L[i]-1. The next good interval G_{i+1} has start = R[i]+1. So next_start = R[i]+1. The length of the tail is gi_end - max(gi_start, next_start - B) + 1. Since next_start - B could be less than gi_start, the max is gi_start. So the length is gi_end - gi_start + 1 = length of G_i. But that could be large. Wait, we said the useful part is the intersection of G_i with [next_start - B, gi_end]. So the length is min(gi_end, gi_end) - max(gi_start, next_start - B) + 1. This is not necessarily bounded by B. For example, if G_i is very long, and next_start - B is very small, then the tail is the whole G_i, which could be long. But is that correct? Let's re-examine: The useful positions in G_i for crossing the next bad interval are those that can reach G_{i+1}. That requires x in G_i such that x+B >= next_start. So x >= next_start - B. So the useful x are in [max(gi_start, next_start - B), gi_end]. This interval could be as long as gi_end - gi_start + 1, which is the length of G_i. So it is not bounded by B. However, we don't need to keep all reachable positions in this interval. We only need to keep the reachable positions in this interval that are "close" to the end? Actually, to cross the next bad interval, we need to jump from x to G_{i+1}. The jump length is in [A,B]. So if x is in [max(gi_start, next_start - B), gi_end], we can jump to G_{i+1}. But if x is very left, we might need a large jump to reach G_{i+1}, but the maximum jump is B. So if x < next_start - B, we cannot reach G_{i+1} in one jump. So the condition x >= next_start - B is correct. So the useful x are in that interval. So the tail is indeed that interval, and it could be long. But then our algorithm of iterating over all y in that interval and checking representability would be slow if the interval is long. However, we argued earlier that the number of reachable positions in that interval is small. But we are iterating over all y in the interval, not just the reachable ones. If the interval is long, say length L, then we are doing O(L) iterations per phase, which could be too slow if L is large. So we need to limit the size of the tail. The key is that we don't need to consider all y in the tail. We only need to consider the reachable positions in the tail. And the reachable positions in the tail are determined by the entry points and the representability. But we don't know which are reachable without checking. So we need a way to compute the reachable set in the tail without iterating over the whole tail.
   The standard solution: We only keep positions in the tail that are at most B away from the end of the tail? Actually, to cross the next bad interval, we need to be within B of the start of the next good interval. So the useful positions are in [next_start - B, gi_end]. The length of this is at most B + (gi_end - next_start + B) = B + (gi_end - next_start) + B. But gi_end = L_i-1, and next_start = R_i+1. So gi_end - next_start = L_i-1 - (R_i+1) = L_i - R_i - 2. Since L_i <= R_i+1, L_i - R_i - 2 <= -1. So gi_end - next_start <= -1. So the length is at most B - 1 + B = 2B - 1? Actually, if L_i = R_i+1, then gi_end - next_start = -1, so the length is B - 1 + B = 2B-1. If L_i is much smaller than R_i, then gi_end - next_start is very negative, so the length is smaller. So the length of the tail is at most 2B-1. Let's check: The tail is [max(gi_start, next_start - B), gi_end]. The maximum possible length occurs when gi_start <= next_start - B, and gi_end is as large as possible. gi_end = L_i-1. next_start = R_i+1. The condition gi_start <= next_start - B means R_{i-1}+1 <= R_i+1 - B => R_{i-1} <= R_i - B. So the bad intervals are separated by at least B. In that case, the tail starts at next_start - B, and ends at gi_end. The length is gi_end - (next_start - B) + 1 = (L_i-1) - (R_i+1 - B) + 1 = L_i - R_i - 2 + B. Since L_i <= R_i+1, L_i - R_i - 2 <= -1. So the length is at most B - 1. So actually, the length is at most B-1. Wait, that's different. Let's compute properly:
        tail_start = max(gi_start, next_start - B)
        tail_end = gi_end
        length = tail_end - tail_start + 1
        Case 1: gi_start >= next_start - B. Then tail_start = gi_start. length = gi_end - gi_start + 1 = length of G_i. But in this case, gi_start >= next_start - B implies R_{i-1}+1 >= R_i+1 - B => R_{i-1} >= R_i - B. So the bad intervals are close. In this case, the length of G_i is (L_i-1) - (R_{i-1}+1) + 1 = L_i - R_{i-1} - 1. This could be large? But note that G_i is between bad intervals. The bad intervals are [L_i, R_i] and [L_{i+1}, R_{i+1}]? Actually, G_i is between bad i and i+1. So the bad intervals are i and i+1. So the condition for G_i to be long is that the gap between R_i and L_{i+1} is large. But L_{i+1} is the start of the next bad interval. So if the gap is large, then the bad intervals are far apart. In that case, the tail is the whole G_i, which could be long. So the length of the tail can be as large as the length of G_i, which could be up to 10^12. So we cannot iterate over the whole tail.
   - So we need a different approach. The standard solution is to not iterate over the whole tail, but to only keep the positions in the tail that are reachable. And to compute the reachable positions in the tail, we can use a BFS from the entry points, but we only explore positions that are in the tail. Since the tail could be long, we need to limit the BFS. The trick is that from an entry point, we can only make jumps forward. So to reach a position y in the tail, we need to be able to jump from some entry point to y. But y is in the tail, which is at the end of G_i. The entry points are in the middle of G_i. So the distance from the entry points to y could be large. However, we can use the representability check. So we can just check for each y in the tail if it is reachable from the entry points. But if the tail is long, we cannot check all y. But we don't need to check all y; we only need to know which y in the tail are reachable, and we only need the reachable ones for the next step. But to know which y are reachable, we might have to check many. However, we can use the fact that the reachable set in the tail is determined by the entry points and the semigroup. Specifically, a position y in the tail is reachable from entry point s if y - s is representable. So the set of reachable y in the tail is the union over s in entry of (s + representable numbers) intersect tail. This set can be computed by iterating over s and over representable numbers. But the number of representable numbers is infinite. However, for a given s and a given tail, we only care about y up to the end of the tail. So we can iterate over k such that s + k is in the tail and k is representable. But k can be up to 10^12. So we need a way to generate the representable numbers up to a bound. Since the tail length could be up to 10^12, we cannot iterate over all k. But we can use the fact that the representable numbers are periodic. So we can just check for each residue class mod g, what is the minimum k, and then add multiples of g. But we need to do this for each s. This could still be O(tail_length) if we are not careful.
   - Actually, the known solution for this problem uses a BFS that is limited to positions that are within B of the end of the current good interval. And they use a BFS from the entry points, but they only explore positions that are within B of the end. How? They maintain a set of reachable positions in the "window" of size B at the end of the good interval. And to compute this window, they do a BFS from the entry points, but they only push positions that are <= the end of the good interval. However, the BFS might still be long if the good interval is long. But they use a trick: they only keep positions that are in the last B positions of the good interval. And they update this set by considering jumps from the previous set. This is like a sliding window BFS. Since the jumps are at most B, the BFS only needs to keep the last B positions. So they don't need to BFS through the whole good interval. They just need to know which of the last B positions are reachable. And to compute that, they can do a BFS from the entry points, but they only push positions that are in the last B positions. However, the entry points might be far from the last B positions. So they need to simulate the BFS across the good interval efficiently. They do this by using a queue and only pushing positions that are within the good interval. But if the good interval is long, the queue could have many elements. So they need a way to avoid pushing all positions. The trick is that they only need to know the reachable positions in the last B positions. So they can do a BFS from the entry points, but they stop when they reach the last B positions. However, to reach the last B positions, they might have to traverse the entire good interval. So they need a way to jump over the middle. They do this by using the fact that from any position, you can jump B forward. So if you have a reachable position, you can reach positions up to that + B. So the set of reachable positions expands by B each step. So if the distance from the entry point to the last B positions is D, you can reach the last B positions in about D/B steps. But D could be up to 10^12, so that's too many steps. So they need a better way.
   - I recall that the standard solution uses a BFS on the "state" which is the set of reachable positions modulo some number, but that seems complex.
   - Let me think again. The problem is from AtCoder, and I remember the solution is to BFS with a limit. Actually, the BFS with a limit (R_i + B) works if we do it correctly. The key is that we don't need to BFS through the entire good interval because we only need to know the reachable positions in the tail. And the BFS with a limit will automatically limit the number of positions we visit. In the BFS with a limit, we start from 1, and we only push positions y if y <= current_limit. So if current_limit is R_1 + B, we only visit positions up to that limit. But as we saw, if the good interval G_0 is long, we might have to visit many positions to reach the tail. For example, if G_0 is [1, 10^12], and the first bad interval is at [10^12-10, 10^12-1], then R_1 = 10^12-1, so current_limit = 10^12-1+20 = 10^12+19, capped at N=10^12. So we would visit positions from 1 to 10^12. That's 10^12 visits. So that's not efficient.
   - So the BFS with a limit doesn't work if the good intervals are long. We need a different limit. The correct limit for the first phase should be the maximum position in G_0 that is useful for crossing. That is, we only need to visit positions in G_0 that are >= R_1+1-B. So we should set current_limit = R_1+1-B + B? Actually, we need to visit those positions. But to reach them from 1, we might need to visit positions before them. However, we can just check directly if those positions are reachable from 1 using the representability check, as we did in the tail-based algorithm. So we don't need to BFS from 1 to reach them; we can just check representability. So the tail-based algorithm is correct.
   - So the tail-based algorithm with the representability check for the first step is the way to go. And for subsequent steps, we have a set of reachable positions in the previous tail. To compute the next tail, we need to know the reachable positions in the next tail. The next tail is an interval of length at most 2B? Actually, we saw that the length could be up to the length of G_i. But is that true? Let's re-derive carefully.
        For G_i (i>=1), it is between bad i and i+1. So G_i = [R[i-1]+1, L[i]-1]? Wait, indexing: Let's index bad intervals from 0 to M-1.
        Then:
        G0: [1, L[0]-1]
        G1: [R[0]+1, L[1]-1]
        G2: [R[1]+1, L[2]-1]
        ...
        G_{M-1}: [R[M-2]+1, L[M-1]-1]
        G_M: [R[M-1]+1, N]
        So for i from 1 to M-1, G_i = [R[i-1]+1, L[i]-1]. (Because G1 uses R[0], G2 uses R[1], etc.)
        The next good interval is G_{i+1} = [R[i]+1, L[i+1]-1] (for i < M-1). So the start of the next good interval is R[i]+1.
        The useful positions in G_i are those that can jump to G_{i+1}. That requires x in G_i such that x+B >= R[i]+1, so x >= R[i]+1-B. Also, we need to be able to reach G_{i+1}, so we need x+A <= L[i+1]-1. So x <= L[i+1]-1-A. But since x is in G_i, x <= L[i]-1. So the useful x are in [max(R[i-1]+1, R[i]+1-B), min(L[i]-1, L[i+1]-1-A)]. This is the intersection. The length of this interval is at most (L[i]-1) - (R[i]+1-B) + 1 = L[i] - R[i] - 2 + B. Since L[i] <= R[i]+1, L[i] - R[i] - 2 <= -1. So the length is at most B-1. So the useful part of G_i is at most B-1 in length. So the tail W_i is actually that interval, and its length is at most B-1. So we can iterate over it.
        What about the condition x <= L[i+1]-1-A? That gives an upper bound. If L[i+1]-1-A < L[i]-1, then the upper bound is L[i+1]-1-A. So the length is (L[i+1]-1-A) - (R[i]+1-B) + 1 = L[i+1] - R[i] - 2 - A + B. This could be larger than B-1. But note that L[i+1] is the start of the next bad interval. So L[i+1] - R[i] - 1 is the gap between the bad intervals. If the gap is large, this length could be large. For example, if the bad intervals are far apart, L[i+1] could be much larger than R[i]. So the useful part could be long. But wait, the condition x <= L[i+1]-1-A comes from the requirement that the jump lands in G_{i+1}. If the gap is large, then G_{i+1} is long, so we can land anywhere in it. So x can be anywhere as long as x+B >= R[i]+1. So the upper bound is actually only limited by G_i's end. So the useful x are in [max(R[i-1]+1, R[i]+1-B), L[i]-1]. The length of this is (L[i]-1) - max(R[i-1]+1, R[i]+1-B) + 1. If R[i-1]+1 >= R[i]+1-B, then the lower bound is R[i-1]+1, and the length is L[i] - R[i-1] - 1. This could be large if the gap between R[i-1] and L[i] is large. But that gap is exactly the length of G_i. So the useful part could be the whole G_i, which could be long. So my earlier reasoning that the length is at most B-1 is wrong. It is only at most B-1 if R[i-1]+1 <= R[i]+1-B, i.e., the bad intervals are separated by at least B. If the bad intervals are closer, the useful part could be longer. So the tail can be long.
   - So we need a way to handle a long tail. The solution is to not iterate over the whole tail, but to only keep the reachable positions in the tail. And to compute the reachable positions in the tail, we can use a BFS from the entry points, but we only explore positions that are in the tail. Since the tail could be long, we need to limit the BFS. The trick is to use a BFS that only keeps positions that are within B of the end of the tail. Because to cross the next bad interval, we need to be within B of the start of the next good interval. So we only need to know the reachable positions in [R[i]+1-B, L[i]-1] (if R[i]+1-B > R[i-1]+1). So we can set a sub-tail of size at most B. And we can compute the reachable positions in that sub-tail by doing a BFS from the entry points, but we only push positions that are in that sub-tail. However, the entry points might be far from that sub-tail. So we need to simulate the BFS across the gap. We can do this by using a DP: for each position in the gap, we can determine if it is reachable. But the gap could be long. However, we can use the fact that the reachable set in the gap is determined by the entry points and the semigroup. So we can just check for each position in the sub-tail if it is reachable from the entry points. And we can do that by checking if the distance from some entry point is representable. So we don't need to BFS through the gap. We can just check the sub-tail directly. But the sub-tail is of size at most B. So we only need to check B positions. So the algorithm is: for each good interval, we compute the sub-tail of size at most B that is useful for the next crossing. Then we compute the reachable positions in that sub-tail by checking representability from the entry points. This is O(B^2) per good interval. And we don't need to iterate over the whole good interval. So the tail-based algorithm is actually correct if we define the tail as the sub-tail of size at most B. But we need to define the sub-tail correctly.
   - The sub-tail for G_i should be the set of positions in G_i that are within B of the start of G_{i+1}. That is, [max(R[i]+1-B, R[i-1]+1), L[i]-1]? Actually, we need x >= R[i]+1-B. But we also need x to be in G_i, so x >= R[i-1]+1. So the sub-tail is [max(R[i-1]+1, R[i]+1-B), L[i]-1]. The length of this is (L[i]-1) - max(R[i-1]+1, R[i]+1-B) + 1. If R[i-1]+1 >= R[i]+1-B, then the lower bound is R[i-1]+1, and the length is L[i] - R[i-1] - 1. This could be large. So the sub-tail could be large. But wait, if R[i-1]+1 >= R[i]+1-B, that means R[i-1] >= R[i] - B. So the bad intervals are close. In that case, the gap between them is small, so the sub-tail is essentially the whole G_i, which could be large. But is that correct? Let's think: If the bad intervals are close, then the gap between them is small. So G_i is the gap between bad i-1 and i? Actually, G_i is between bad i and i+1. So if R[i-1] and R[i] are close, that means the end of bad i-1 and the start of bad i+1 are close? Not necessarily. Let's use concrete numbers: A=1, B=2. Bad intervals: [10,10] and [11,11]. Then R[0]=10, R[1]=11. So R[0] >= R[1]-2? 10 >= 9, yes. So condition holds. Then G1 = [R[0]+1, L[1]-1] = [11, 10]? That's empty. So G1 is empty. So the sub-tail is empty. So the condition R[i-1]+1 >= R[i]+1-B might be true, but if G_i is empty, then the sub-tail is empty. So the length is 0. In general, if the bad intervals are close, the good interval G_i might be small. So the sub-tail could be small. But what if the bad intervals are far apart? For example, bad intervals: [10,10] and [100,100]. Then R[0]=10, R[1]=100. R[0] >= R[1]-B? 10 >= 100-2=98, false. So condition false. Then the sub-tail lower bound is R[1]+1-B = 100+1-2=99. So the sub-tail is [99, L[1]-1]. L[1] is the start of bad 2, which is 100. So L[1]-1=99. So sub-tail is [99,99], size 1. So indeed, the sub-tail is small. So it seems that the sub-tail is always of size at most B. Let's prove it: The sub-tail is [max(R[i-1]+1, R[i]+1-B), L[i]-1]. The length is (L[i]-1) - max(R[i-1]+1, R[i]+1-B) + 1. We want to show this is <= B. Consider two cases:
        Case 1: R[i-1]+1 >= R[i]+1-B. Then max = R[i-1]+1. Length = L[i] - R[i-1] - 1. But note that L[i] is the start of bad i, and R[i-1] is the end of bad i-1. Since the bad intervals are disjoint, L[i] > R[i-1]. So L[i] >= R[i-1]+1. So L[i] - R[i-1] - 1 >= 0. But we need to bound it by B. Is it always <= B? Not necessarily. For example, if A=1, B=100, and the gap between R[i-1] and L[i] is 200, then L[i] - R[i-1] - 1 = 200-1=199, which is > B=100. So the sub-tail could be large. So my claim is false.
   - So we need to handle the case where the sub-tail is large. In that case, we cannot iterate over the sub-tail. We need a different approach. The standard solution is to use a BFS that is limited to positions that are within B of the end of the good interval. And they use a BFS that only explores positions that are in the good interval and within the current limit. But they also use a trick: they only keep positions that are in the last B positions of the good interval. And to compute the reachable set in the last B positions, they do a BFS from the entry points, but they only push positions that are in the last B positions. However, the entry points might be far from the last B positions. So they need to simulate the BFS across the good interval. They do this by using a queue and only pushing positions that are reachable. But if the good interval is long, the queue could have many elements. So they need a way to compress the state. The trick is that the reachable set in a long good interval without obstacles is eventually all positions that are in the semigroup. So they can just compute the reachable set in a window of size B at the end by using a DP that iterates over the good interval. But the good interval could be long, so iterating over it is not feasible. So they need a way to jump over the good interval. They do this by using the fact that from any reachable position, you can jump B forward. So the set of reachable positions expands by B each step. So if you have a set of reachable positions, you can compute the set of positions that are reachable in the next B steps by adding B to each. This is like a flood fill. So you can simulate the BFS by repeatedly adding B to the set. Since the good interval is a line, this will fill it quickly. So you can compute the reachable set in the last B positions by starting from the entry points and repeatedly adding B until you cover the interval. But you need to do this efficiently. You can do it by just taking the maximum reachable position in the entry set, and then adding B repeatedly. But you also need to consider the exact positions, not just the maximum. Because the last B positions might require specific positions. So you need to know the exact set of reachable positions in the last B positions. This can be done by doing a BFS from the entry points, but only keeping the last B positions. Since the BFS from the entry points will visit positions in increasing order, you can just do a BFS until you reach the end. But if the good interval is long, you will visit many positions. So you need to skip. You can skip by using the fact that if you have a reachable position, then all positions that are congruent to it modulo g and are >= some threshold are reachable. So you can just compute the threshold. This is getting complicated.
   - Given the time, I should implement the simpler BFS with a limit, but with a smarter limit. Actually, the BFS with a limit works if we set the limit to the right endpoint of the current bad interval + B, and we process the bad intervals in order, but we also need to ensure that we don't BFS through a long good interval. The way to do that is to not BFS from the very beginning each time, but to start the BFS from the positions that are in the current good interval. And to get those positions, we need to have computed them in the previous step. So we can do a BFS that only explores the current good interval and the next bad interval. Specifically, for each bad interval, we do a BFS from the positions in the good interval before it, but we only explore positions up to the end of that good interval plus B. And we only push positions that are in the good interval. This way, the BFS is limited to the length of the good interval plus B. If the good interval is long, the BFS might still be long. But we can use the fact that the good interval has no bad squares, so we can use the representability check to skip the BFS. So the tail-based algorithm is actually the correct one. We need to implement it efficiently.
   - Let's look at the constraints: M <= 2e4, A,B <= 20. So we can afford O(M * B^2) time. But we cannot afford O(M * length of good interval). So we need to ensure that the operations per good interval are O(B) or O(B^2). The tail-based algorithm, if we iterate over the sub-tail, could be O(length of sub-tail) which could be O(length of good interval) in the worst case. So we need to modify it to only iterate over B positions.
   - The key is that we don't need to consider all positions in the sub-tail. We only need to consider the positions in the sub-tail that are reachable. And to find the reachable positions, we can use the entry points and the representability check. But the sub-tail could be long, so we cannot iterate over all of it. However, we can iterate over the entry points and the representable numbers. But the representable numbers up to the length of the sub-tail could be many. But we can use the fact that the representable numbers are periodic. So we can just check for each residue class mod g whether there is a representable number in the appropriate range. But we need to do this for each entry point. This could still be O(B * (sub-tail length / g)) which is not good if the sub-tail is long.
   - Actually, the sub-tail is defined as the set of positions that are within B of the start of the next good interval. So the sub-tail is at most B in length. Wait, I'm confused. Let's re-define the sub-tail properly. We want to know which positions in G_i can reach G_{i+1}. That requires x in G_i such that x+B >= start of G_{i+1}. So x >= start of G_{i+1} - B. So the set of such x is [max(start of G_i, start of G_{i+1} - B), end of G_i]. The length of this interval is (end of G_i) - (start of G_{i+1} - B) + 1 = (end of G_i) - (start of G_{i+1}) + B + 1. But end of G_i = L[i]-1, start of G_{i+1} = R[i]+1. So length = (L[i]-1) - (R[i]+1) + B + 1 = L[i] - R[i] - 2 + B. Since L[i] <= R[i]+1, L[i] - R[i] - 2 <= -1. So length <= B-1. So the sub-tail is at most B-1 in length. So it is small! My earlier counterexample was wrong because I considered the gap between R[i-1] and L[i], but that's the length of G_i, not the sub-tail. The sub-tail is only the part of G_i that is close to the next bad interval. So indeed, the sub-tail is small. So we can iterate over it.
   - Let's verify with the counterexample: A=1, B=100, bad intervals: [10,10] and [200,200]. Then L[0]=10, R[0]=10, L[1]=200, R[1]=200. So G1 = [R[0]+1, L[1]-1] = [11, 199]. The next good interval G2 is after bad 2, so not relevant. But for i=0, we are crossing bad 1. The sub-tail for G0 is [max(1, R[0]+1-B), L[0]-1] = [max(1, 10+1-100=-89), 9] = [1,9]. So length 9, which is <= B=100. For i=1, we are crossing bad 2. The sub-tail for G1 is [max(R[0]+1, R[1]+1-B), L[1]-1] = [max(11, 200+1-100=101), 199] = [101,199]. The length is 199-101+1=99, which is <= B=100. So indeed, the sub-tail length is at most B. So we can iterate over it.
   - Therefore, the tail-based algorithm is correct and efficient. We just need to make sure we define the sub-tail correctly.
   - So the algorithm is as described before. We will implement it.
   - Let's write the code step by step.
   - First, read inputs.
   - Precompute is_representable.
   - Handle M=0.
   - Compute goods list.
   - Compute cur for goods[0] using the sub-tail.
   - Loop over i=1 to M-1 (goods[1] to goods[M-1]), compute entry and next_cur using the sub-tail of goods[i].
   - For the last goods[M], compute entry and check N.
   - We need to be careful with the sub-tail definition for each step.
   - For goods[0], the sub-tail is W0 = [max(goods[0][0], goods[1][0] - B), goods[0][1]].
   - For goods[i] (1 <= i <= M-1), the sub-tail is Wi = [max(goods[i][0], goods[i+1][0] - B), goods[i][1]].
   - For the last goods[M], we don't need a sub-tail; we just check N.
   - So the code can be written as described.
   - Let's test the algorithm on the samples again to be sure.
   - Sample 1: works.
   - Sample 2: works.
   - Sample 3: works.
   - Edge cases: M=0, A=B=1, N=2, no bad squares: N-1=1, representable? 1 is in [1,1], so yes.
   - Edge case: A=10, B=10, N=100, bad interval [50,60]. Then we need to jump exactly 10. G0=[1,49], G1=[61,100]. Sub-tail for G0: [max(1, 61-10=51), 49] = [51,49] empty. So cur empty, print No. But is it actually impossible? From 1, we can only jump 10. So we can reach 11,21,31,41. From 41, we can jump to 51, but 51 is in the bad interval? 51 is between 50 and 60, so bad. So we cannot land on 51. So we are stuck. So No. Correct.
   - Edge case: A=10, B=10, N=100, bad interval [50,59]. Then G0=[1,49], G1=[60,100]. Sub-tail for G0: [max(1, 60-10=50), 49] = [50,49] empty. So No. But can we reach 60? From 41, we can jump to 51, but 51 is bad. From 31, jump to 41. So we can only reach 1,11,21,31,41. From 41, jump to 51 (bad) or 61 (too far, jump is 20). So we cannot reach 60. So No. Correct.
   - Edge case: A=10, B=10, N=100, bad interval [40,49]. Then G0=[1,39], G1=[50,100]. Sub-tail for G0: [max(1, 50-10=40), 39] = [40,39] empty. So No. But from 1, we can reach 11,21,31. From 31, we can jump to 41, but 41 is bad. So we cannot reach 50. So No. Correct.
   - Edge case: A=10, B=10, N=100, bad interval [30,39]. Then G0=[1,29], G1=[40,100]. Sub-tail for G0: [max(1, 40-10=30), 29] = [30,29] empty. So No. But from 1, we can reach 11,21. From 21, jump to 31, but 31 is bad. So No. Correct.
   - Edge case: A=10, B=10, N=100, bad interval [20,29]. Then G0=[1,19], G1=[30,100]. Sub-tail for G0: [max(1, 30-10=20), 19] = [20,19] empty. So No. From 1, reach 11. From 11, jump to 21, bad. So No. Correct.
   - Edge case: A=10, B=10, N=100, bad interval [10,19]. Then G0=[1,9], G1=[20,100]. Sub-tail for G0: [max(1, 20-10=10), 9] = [10,9] empty. So No. From 1, we can only reach 1. Cannot jump to 11 because bad. So No. Correct.
   - Edge case: A=10, B=10, N=100, bad interval [1,9]? But L_i > 1, so not allowed.
   - So the algorithm seems correct.
   - Now, we need to implement the representability check.
   - We'll precompute a set `rep_scaled` for the scaled semigroup.
   - Code structure:
        from math import gcd
        import sys
        input = sys.stdin.readline

        N, M, A, B = map(int, input().split())
        L = []
        R = []
        for _ in range(M):
            l, r = map(int, input().split())
            L.append(l)
            R.append(r)

        # Precompute representability
        g = gcd(A, B)
        a = A // g
        b = B // g
        if a == 1 or b == 1:
            # All multiples of g are representable
            def is_representable(D):
                if D < 0: return False
                return D % g == 0
        else:
            frob = a*b - a - b
            rep_scaled = set()
            rep_scaled.add(0)
            # BFS to generate all representable numbers up to frob
            from collections import deque
            q = deque([0])
            while q:
                x = q.popleft()
                for step in (a, b):
                    y = x + step
                    if y <= frob and y not in rep_scaled:
                        rep_scaled.add(y)
                        q.append(y)
            def is_representable(D):
                if D < 0: return False
                if D % g != 0: return False
                D_prime = D // g
                if D_prime > frob: return True
                return D_prime in rep_scaled

        if M == 0:
            if is_representable(N-1):
                print("Yes")
            else:
                print("No")
            return

        # Build good intervals
        goods = []
        goods.append((1, L[0]-1))
        for i in range(M-1):
            goods.append((R[i]+1, L[i+1]-1))
        goods.append((R[M-1]+1, N))

        # Step 0: compute cur for goods[0]
        wi_start = max(goods[0][0], goods[1][0] - B)
        wi_end = goods[0][1]
        cur = set()
        for x in range(wi_start, wi_end+1):
            if is_representable(x-1):
                cur.add(x)
        if not cur:
            print("No")
            return

        # Process goods[1] to goods[M-1]
        for i in range(1, M):
            gi_start, gi_end = goods[i]
            # sub-tail of goods[i]
            wi_start = max(gi_start, goods[i+1][0] - B)
            wi_end = gi_end
            # compute entry
            entry = set()
            for x in cur:
                for d in range(A, B+1):
                    y = x + d
                    if gi_start <= y <= gi_end:
                        entry.add(y)
            if not entry:
                print("No")
                return
            # compute next_cur
            next_cur = set()
            for y in range(wi_start, wi_end+1):
                found = False
                for s in entry:
                    if y >= s and is_representable(y - s):
                        found = True
                        break
                if found:
                    next_cur.add(y)
            if not next_cur:
                print("No")
                return
            cur = next_cur

        # Last good interval goods[M]
        gm_start, gm_end = goods[M]
        entry = set()
        for x in cur:
            for d in range(A, B+1):
                y = x + d
                if gm_start <= y <= gm_end:
                    entry.add(y)
        if not entry:
            print("No")
            return
        if N in entry:
            print("Yes")
            return
        check_start = max(gm_start, N - B)
        for y in range(check_start, N):
            for s in entry:
                if y >= s and is_representable(y - s):
                    print("Yes")
                    return
        print("No")
   - This should work.
   - Let's test with the samples manually by running through the code.
   - Sample 1: N=24, M=2, A=3, B=5, bad: [7,8], [17,20]
        goods: [(1,6), (9,16), (21,24)]
        g = gcd(3,5)=1, a=3, b=5, frob=3*5-3-5=7, rep_scaled up to 7.
        is_representable: for D, if D>7, true; else check in rep_scaled.
        M>0.
        Step 0: wi_start = max(1, 9-5=4) =4, wi_end=6. cur: x=4: 3 in rep? 3 in rep_scaled? 3=3, yes. x=5: 4=4? 4 not in rep_scaled? Actually, 4 is not in rep_scaled because 3+? 4 is not representable with 3 and 5? 3+? 4-3=1 not. So 4 not representable. But wait, 4 is in [A,B]? A=3, B=5, so 4 is a valid jump. So D=4 should be representable. But in our scaled semigroup, a=3, b=5, so 4 is not a multiple of g=1? Actually, D=4, D%g=0, D_prime=4. 4 > frob=7? No, 4 <=7. So we check if 4 in rep_scaled. But rep_scaled only contains numbers representable as sum of 3 and 5. 4 is not representable. So is_representable(4) would return False. That's a problem! Because we can jump 4 directly. So D=4 is representable as a single jump. But in the scaled semigroup, we only consider nonnegative combinations of 3 and 5. But 4 is not a combination of 3 and 5. However, in the original problem, we can choose a jump of exactly 4. So 4 is representable. Our is_representable function only checks if D is a sum of numbers in [A,B], but it doesn't consider that a single jump can be any number in [A,B]. So the semigroup generated by [A,B] is actually the set of all numbers that can be written as a sum of numbers in [A,B], where each summand is in [A,B]. But note that a single jump is a sum of one number, so any number in [A,B] is representable. So the semigroup is generated by the set [A,B], not just by A and B. So our gcd trick only works for the set {A, B}. But the set is all integers from A to B. So the semigroup generated by [A,B] is different. In fact, the set of representable numbers using jumps in [A,B] is the set of all integers that can be written as a sum of numbers in [A,B]. This is a numerical semigroup generated by all integers from A to B. This semigroup is actually all integers >= A*(B-A+1)? Not exactly. But we can precompute it similarly by BFS. But the number of generators is B-A+1, which is at most 20. So we can just BFS up to some bound. The bound for this semigroup is something like A*B. So we can precompute all representable numbers up to, say, 400. Then for larger D, we can use the fact that the semigroup is eventually periodic with period g = gcd(A, A+1, ..., B) = gcd(A, A+1, ..., B). Actually, the set of representable numbers is a numerical semigroup if A and B are coprime? Not necessarily, because the generators are consecutive integers. The semigroup generated by consecutive integers is actually all integers >= A*(B-A+1)? I recall that the semigroup generated by {A, A+1, ..., B} is all integers >= A*(B-A+1). But is that true? For example, A=3, B=5, generators: 3,4,5. The semigroup contains 3,4,5,6,7,8,9,... Actually, 6=3+3, 7=3+4, 8=4+4, 9=3+3+3, 10=5+5, 11=3+4+4, etc. So the largest non-representable is? 1,2 are not. 3,4,5,6,7,8,9,10,11,... So all integers >= 3 are representable. So the Frobenius number is 2. So it's not A*(B-A+1). So we need a general way to check representability.
   - Since the generators are consecutive integers from A to B, the semigroup is actually all integers >= A*(B-A+1) - (B-A+1) + 1? Not sure. But we can just precompute the representable numbers up to some bound using BFS, and then for larger D, use the fact that the set is eventually all integers. Actually, if A and B are consecutive, the semigroup is all integers >= A. If they are not consecutive, there might be gaps. For example, A=3, B=6, generators: 3,4,5,6. The representable numbers: 3,4,5,6,7,8,9,... So all integers >= 3. So it seems that if the set includes consecutive integers, the semigroup is all integers >= A. In general, the semigroup generated by {A, A+1, ..., B} is all integers >= A. Because you can always add 1 if you have consecutive numbers. So the only non-representable numbers are those less than A. So the semigroup is actually all integers >= A. Wait, is that true? If you have A and A+1, then you can make any integer >= A. So if B >= A+1, then the semigroup is all integers >= A. So the only gaps are numbers less than A. So the representability check is trivial: D is representable if and only if D >= 0 and D >= A? But what if D is less than A? Then it's not representable. So is_representable(D) = (D >= A). But wait, what about D=0? We can have a sum of zero jumps, so 0 is representable. So is_representable(D) = (D == 0 or D >= A). But is that always true? Consider A=3, B=5. D=1,2: not representable. D=3,4,5: representable. D=6: representable. So yes. Consider A=4, B=6. D=4,5,6: representable. D=7: 4+? 7-4=3 not in [4,6]. But 7 can be 4+? Actually, 7 is not representable? 4+4=8, 4+5=9, 4+6=10, 5+5=10, 5+6=11, 6+6=12. So 7 is not representable. But 7 >= A=4, so our rule fails. So the rule is not simply D >= A. So we need a proper check.
   - Since the generators are consecutive integers, the semigroup is a numerical semigroup. Its Frobenius number can be computed. For the set {A, A+1, ..., B}, the semigroup is all integers >= (A-1)*(B-A+1) - (B-A+1) + 1? I'm not sure. But since A,B <= 20, we can just precompute the representable numbers up to, say, 400. And for D > 400, we can use the fact that the semigroup is periodic with period g = gcd(A, A+1, ..., B) = 1. So the period is 1. So all sufficiently large integers are representable. So we can just find the largest non-representable number, and then for D > that, return True. So we can precompute the representable numbers up to, say, 400, and then for D > 400, we can check if D is in the set? But the set might have gaps beyond 400. However, since the period is 1, the set will eventually be all integers. So we can just find the maximum gap. We can precompute the representable numbers up to 400, and then for D > 400, we can check if D - 400 is in the set? Not exactly. But we can just BFS up to 400, and then for D > 400, we can use a greedy algorithm: if D >= A, we can always represent it. But we saw a counterexample: A=4, B=6, D=7. 7 is not representable. But 7 is > 400? No, 7 is small. So if we precompute up to 400, we would have 7 in the set? Let's compute: for A=4, B=6, the representable numbers are: 4,5,6,8,9,10,11,12,... So 7 is not representable. So if we precompute up to 400, we will find that 7 is not in the set. So we can just check if D is in the precomputed set. If D <= 400, we check directly. If D > 400, we need a rule. But since the semigroup is eventually all integers, there exists some bound B0 such that for all D >= B0, D is representable. We can find B0 by precomputing up to, say, 4000. But we can do better: since the generators are consecutive, the semigroup is all integers >= A*(B-A+1)? Actually, for A=4, B=6, A*(B-A+1)=4*3=12. But 7,8,9,10,11 are representable? 8,9,10,11 are representable, but 7 is not. So the largest non-representable is 7. And 7 < 12. So the bound is not that. Actually, the semigroup generated by consecutive integers has a Frobenius number of A-1 if the set includes A and A+1. But if the set is {4,6}, then it's not consecutive. In our problem, the set is [A,B], which is consecutive. So it includes all integers from A to B. So the semigroup is generated by consecutive integers. In that case, the semigroup is actually all integers >= A. Wait, but for A=4, B=6, the set is {4,5,6}. That's consecutive. And we saw that 7 is not representable. So that's a counterexample. Why? Because to get 7, we need 4+3, but 3 is not in the set. So we cannot make 7. So the semigroup generated by {4,5,6} is not all integers >= 4. So my claim is false. So we need a proper way to check representability.
   - Since the number of generators is at most 20, we can precompute the representable numbers up to a certain bound. What bound? We can use the fact that the semigroup is eventually periodic. The period is g = gcd(A, A+1, ..., B) = 1. So the period is 1. So there exists a bound such that all integers >= that bound are representable. We can find that bound by BFS. Since the generators are small, we can BFS up to, say, 4000. That should be enough. We can BFS on the state of the distance modulo 1? Not helpful. We can just BFS all representable numbers up to 4000. Since the maximum jump is 20, the BFS will generate numbers quickly. We can store them in a set. Then for a given D, if D is in the set, return True. If D > 4000, we can use a simple check: since the period is 1, and the set is eventually all integers, we can just check if D is in the set by seeing if D - k is in the set for some k? Not straightforward. But we can use the fact that if D is large enough, it is representable. We can find the largest non-representable number. We can do that by BFS until we see a number that is not reachable and then check if all larger numbers are reachable. Since the period is 1, once we have a block of consecutive representable numbers of length equal to the maximum jump, all larger numbers are representable. So we can BFS until we have found a sequence of B consecutive representable numbers. Then we can stop. So we can precompute the representable numbers up to, say, 400, and then check if we have B consecutive numbers. If yes, then for any D greater than the last number in that block, D is representable. So we can set a threshold.
   - In our algorithm, we only need to check representability for D that are differences between positions in the sub-tails. The sub-tails are of size at most B, so the differences are at most the length of the good interval, which could be up to 10^12. So we need a check for large D. So we need an O(1) check for large D.
   - We can do the following: precompute the representable numbers up to some bound, say 4000. Also, find the smallest number such that all numbers from that number to that number + B are representable. Call that threshold T. Then for any D >= T, D is representable. So our is_representable(D) can be: if D < 0: False; if D in precomputed set: True; if D >= T: True; else: False.
   - How to find T? We can BFS until we have found B consecutive representable numbers. Since the maximum jump is B, if we have B consecutive representable numbers, then any number >= the first number in that block is representable. So we can just BFS and keep track of the largest consecutive block. We can do this until we have found a block of length B. Since the semigroup is generated by numbers up to 20, the threshold T will be at most 400. So we can just BFS up to 400.
   - So the plan: precompute a boolean array `rep` of size, say, 4000. Do a BFS from 0, using jumps in [A,B]. Mark all reachable numbers up to 4000. Then find the smallest T such that all numbers from T to T+B-1 are representable. Actually, we need the smallest T such that for all D >= T, D is representable. That is equivalent to finding the Frobenius number + 1. So we can just find the largest number less than T that is not representable. So we can BFS until we have a consecutive block of B representable numbers. The start of that block is T. Then any D >= T is representable. So we can set T to that start.
   - Let's implement that.
   - So is_representable(D):
        if D < 0: return False
        if D <= max_precomputed: return rep[D]
        if D >= T: return True
        return False
   - We need to choose max_precomputed large enough. We can set it to 4000. BFS up to 4000. Then find T.
   - In the BFS, we start from 0, and for each x, we try x+d for d in [A,B]. If x+d <= 4000 and not visited, mark and push.
   - Then we find T: for i from 0 to 4000-B+1, if all rep[i:i+B] are True, then T = i, break. We can also just take the smallest i such that rep[i] is False? Actually, we want the threshold such that for all D >= T, D is representable. That means the largest non-representable number is less than T. So we can find the largest non-representable number and set T = that + 1. So we can iterate from 4000 downwards to find the largest number that is not representable. But that might be slow if 4000 is large. We can just BFS until we have a consecutive block of B representable numbers. Since the semigroup is generated by numbers up to 20, the Frobenius number is at most 400. So T will be at most 400. So we can just BFS up to 400, and then find T by checking from 0 to 400-B+1.
   - So we can do:
        max_check = 400
        rep = [False] * (max_check + B + 1)  # extra space
        rep[0] = True
        queue = deque([0])
        while queue:
            x = queue.popleft()
            for d in range(A, B+1):
                y = x + d
                if y <= max_check and not rep[y]:
                    rep[y] = True
                    queue.append(y)
        # Now find T: smallest such that all rep[T:T+B] are True
        T = None
        for i in range(max_check + 1):
            if all(rep[i:i+B]):
                T = i
                break
        # If T is None, we can set T = max_check + 1
        if T is None:
            T = max_check + 1
   - Then is_representable(D):
        if D < 0: return False
        if D <= max_check: return rep[D]
        return D >= T
   - But wait, if D > max_check, we need to ensure that D >= T. But what if T is None? Then we just return False for D > max_check? But that would be wrong. So we need to ensure that T is set. Actually, if we can't find a block of B consecutive representable numbers up to max_check, we can increase max_check. Since the semigroup is generated by numbers up to 20, the Frobenius number is at most A*B. So we can set max_check to A*B + B. That should be enough. For A=3, B=5, A*B=15, so max_check=15+5=20. But we saw that 7 is not representable for A=4, B=6. A*B=24, so max_check=24+6=30. We can compute up to 400 to be safe.
   - Let's test with A=4, B=6. max_check=400. BFS from 0: we get rep[0]=True, then 4,5,6. Then 4+4=8, 4+5=9, 4+6=10, 5+5=10, 5+6=11, 6+6=12. Then 8+4=12, 8+5=13, 8+6=14, 9+4=13, 9+5=14, 9+6=15, 10+4=14, 10+5=15, 10+6=16, etc. We will eventually get all numbers >= 8 except 7. So the largest non-representable is 7. So T should be 8. And 8 is in rep. And rep[8:8+6] = rep[8:14] = [True, True, True, True, True, True]? Actually, 8,9,10,11,12,13 are all True. So T=8. So is_representable(7) returns False because 7 <= 400 and rep[7] is False. is_representable(8) returns True. is_representable(100) returns True because 100 >= T=8. So that works.
   - So we can implement the representability check this way.
   - Now, we need to integrate this into the algorithm.
   - The algorithm is O(M * B^2) which is fine.
   - Let's write the final code.
   - We need to be careful with the ranges and indices.
   - We'll use the goods list as described.
   - For the representability check, we'll precompute rep up to 4000 (or 5000) to be safe.
   - Code:
        from collections import deque
        import sys
        from math import gcd

        input = sys.stdin.readline

        N, M, A, B = map(int, input().split())
        L = []
        R = []
        for _ in range(M):
            l, r = map(int, input().split())
            L.append(l)
            R.append(r)

        # Precompute representability
        max_check = 5000
        rep = [False] * (max_check + B + 1)
        rep[0] = True
        q = deque([0])
        while q:
            x = q.popleft()
            for d in range(A, B+1):
                y = x + d
                if y <= max_check and not rep[y]:
                    rep[y] = True
                    q.append(y)
        # Find T: smallest such that all rep[T:T+B] are True
        T = None
        for i in range(max_check + 1):
            if i + B <= len(rep) and all(rep[i:i+B]):
                T = i
                break
        if T is None:
            T = max_check + 1  # fallback

        def is_representable(D):
            if D < 0: return False
            if D <= max_check: return rep[D]
            return D >= T

        if M == 0:
            if is_representable(N-1):
                print("Yes")
            else:
                print("No")
            return

        # Build good intervals
        goods = []
        goods.append((1, L[0]-1))
        for i in range(M-1):
            goods.append((R[i]+1, L[i+1]-1))
        goods.append((R[M-1]+1, N))

        # Step 0: compute cur for goods[0]
        wi_start = max(goods[0][0], goods[1][0] - B)
        wi_end = goods[0][1]
        cur = set()
        for x in range(wi_start, wi_end+1):
            if is_representable(x-1):
                cur.add(x)
        if not cur:
            print("No")
            return

        # Process goods[1] to goods[M-1]
        for i in range(1, M):
            gi_start, gi_end = goods[i]
            wi_start = max(gi_start, goods[i+1][0] - B)
            wi_end = gi_end
            entry = set()
            for x in cur:
                for d in range(A, B+1):
                    y = x + d
                    if gi_start <= y <= gi_end:
                        entry.add(y)
            if not entry:
                print("No")
                return
            next_cur = set()
            for y in range(wi_start, wi_end+1):
                found = False
                for s in entry:
                    if y >= s and is_representable(y - s):
                        found = True
                        break
                if found:
                    next_cur.add(y)
            if not next_cur:
                print("No")
                return
            cur = next_cur

        # Last good interval goods[M]
        gm_start, gm_end = goods[M]
        entry = set()
        for x in cur:
            for d in range(A, B+1):
                y = x + d
                if gm_start <= y <= gm_end:
                    entry.add(y)
        if not entry:
            print("No")
            return
        if N in entry:
            print("Yes")
            return
        check_start = max(gm_start, N - B)
        for y in range(check_start, N):
            for s in entry:
                if y >= s and is_representable(y - s):
                    print("Yes")
                    return
        print("No")
   - This should be correct and efficient.
   - Let's test with the samples in our head.
   - Sample 1: works.
   - Sample 2: works.
   - Sample 3: works.
   - Edge case: M=0, A=1, B=1, N=2: is_representable(1): 1<=5000, rep[1] should be True because 1 is in [1,1]. So Yes.
   - Edge case: M=0, A=3, B=5, N=4: is_representable(3): 3 in rep? 3 is in [3,5], so Yes. So should print Yes if we can reach N=4 from 1 with jumps 3,4,5? 1+3=4, so Yes.
   - Edge case: M=0, A=3, B=5, N=5: 1+4=5, so Yes.
   - Edge case: M=0, A=3, B=5, N=6: 1+5=6, so Yes.
   - Edge case: M=0, A=3, B=5, N=7: 1+3+3=7, so Yes. is_representable(6): 6 in rep? 3+3=6, so Yes.
   - So the representability check is correct.
   - One more thing: in the representability check, we consider 0 as representable. That is correct because we can have a sum of zero jumps. So is_representable(0) should be True. In our BFS, we start with 0, so rep[0]=True. So that's fine.
   - Now, we need to ensure that the algorithm handles the case where the sub-tail is empty. In that case, the for loop over y range will not execute, so next_cur will be empty, and we print No. That's correct.
   - Also, we need to ensure that the entry set is not empty. If entry is empty, we print No.
   - The algorithm seems complete.
   - Let's write the final code with proper input parsing and output.</mm:think>### PLAN
The problem involves determining reachability on a line of N squares (up to 10^12) with M bad intervals (sorted, non-overlapping) and jumps of length in [A, B] (A,B ≤ 20). We can move only to good squares. The key insight is that we only need to consider "useful" positions at the right end of each good interval (the tail within B of the next bad interval), which has size at most B. We process good intervals from left to right, maintaining a set of reachable positions in the current tail. For each step, we compute positions reachable in one jump from the previous tail into the current good interval, then determine which positions in the new tail are reachable using a representability check (can a distance be expressed as a sum of numbers in [A,B]?). This yields an O(M·B²) algorithm. We precompute a table of representable distances up to 5000 to handle large distances efficiently.