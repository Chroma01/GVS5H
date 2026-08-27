
## ideation
The problem asks for the maximum height `h` at coordinate 0 such that not all buildings are visible. If height 0 sees all buildings, output -1. Otherwise, output that maximum height.

A building `i` is visible from (0, h) if there exists a point on it such that the segment to (0, h) doesn't intersect any other building. Since buildings are vertical segments and only buildings with smaller X can block the view to a building, the condition for building `i` to be visible is that `h` must be strictly greater than the y-intercept of the line through `(X_i, H_i)` and any left building `(X_j, H_j)` (j < i). Specifically, for each `i`, define `L_i = max_{j < i} (H_j * X_i - H_i * X_j) / (X_i - X_j)`. Building `i` is visible iff `h > L_i`. Thus, all buildings are visible iff `h > L` where `L = max_i L_i`. The answer is `L` if `L > 0`; if `L <= 0`, height 0 sees all and we output -1.

`L` is exactly the maximum y-intercept of lines through any two buildings (with the right one having larger X). This is equivalent to finding the maximum over all pairs of `(H_a * X_b - H_b * X_a) / (X_b - X_a)`.

This can be computed in O(N) using a convex hull trick (monotonic queue) by sweeping from left to right. For each building `i`, we need to maximize `H_i * X_j - H_j * X_i` over `j < i`. This is a linear function in `(X_j, H_j)`. We can maintain the upper convex hull of the points seen so far. For a query point `(X_i, H_i)`, we need the point on the hull that maximizes the cross product `X_i * H_j - H_j * X_i` (or equivalently the y-intercept). Since `X_i` is increasing, we can use a deque and maintain the hull such that the optimal point moves monotonically.

Alternatively, we can maintain a set of lines and use pointer to the best. But the convex hull of points approach is standard: we keep points on the upper hull. For a new point `i`, we want to find which previous point gives the maximum y-intercept. The y-intercept of line through `j` and `i` is `(H_j * X_i - H_i * X_j) / (X_i - X_j)`. For fixed `i`, this is a function of `j`. As we sweep, we can maintain a convex hull of candidate points. Since the query `X_i` is increasing, the optimal `j` on the hull moves forward. We can use a deque and pop from front when the next point gives a better value.

Specifically, we maintain a deque of points representing the upper convex hull. For each new point `i`, we add it to the hull (removing previous points that are now below the line). Then we query the deque to find the point that gives the maximum y-intercept with `i`. Since the optimal point moves to the right as `i` increases, we can pop from the front while the next point gives a larger y-intercept. The condition to check: compare the y-intercept of line through `i` and the current best point vs the next point. If the next point gives a larger y-intercept, move the front.

We need to be careful with floating point precision. We can compare the y-intercepts without division by cross-multiplying. For two candidate points `a` and `b` (with `a` before `b` in the deque), the y-intercept of line through `i` and `a` is `(H_a X_i - H_i X_a)/(X_i - X_a)`. For `b`, it's `(H_b X_i - H_i X_b)/(X_i - X_b)`. We want to know which is larger. Cross-multiplying (since denominators are positive):
`(H_a X_i - H_i X_a) * (X_i - X_b) > (H_b X_i - H_i X_b) * (X_i - X_a)`.
This is a safe integer comparison since all values are up to 1e9 and N=2e5, products can be up to 1e18, which fits in 128-bit integer (Python int is arbitrary precision, so fine).

Algorithm:
1. Read N and points.
2. Initialize deque with first point.
3. For i from 2 to N:
   - While deque has at least 2 points and the y-intercept with the first point is <= y-intercept with the second point, pop left.
   - Let j be the leftmost point in deque. Compute f(j, i) = (H_j X_i - H_i X_j) / (X_i - X_j). Update L = max(L, f(j, i)).
   - Then add point i to deque: while deque has at least 2 points and the new point makes the last two points not part of the upper hull (i.e., cross product condition), pop right.
   - Push i.
4. If L <= 0, print -1. Else print L.

The condition for maintaining the upper hull: points (X1, H1), (X2, H2), (X3, H3) with X1 < X2 < X3. We want to keep X2 if the slope from X1 to X2 is less than the slope from X2 to X3? Actually, for the upper hull (concave from above), we want the cross product (X2-X1)*(H3-H2) - (H2-H1)*(X3-X2) < 0? Let's check: For upper hull, we want the points to be such that the line from X1 to X3 is below X2? Actually, if X2 is above the line from X1 to X3, then X2 is on the upper hull. The cross product condition for X2 to be redundant (below the upper hull) is that X2 is below the line from X1 to X3, which means (H2 - H1)/(X2 - X1) < (H3 - H2)/(X3 - X2)? Wait, if X2 is above the line, then the slope from X1 to X2 is greater than the slope from X1 to X3. But we need to check the standard condition. For the upper convex hull (the part visible from above), we want to remove points that cause a "right turn" (i.e., the new point is below the line from the second last to the last? Actually, the standard monotonic chain algorithm for upper hull: sort by x, then for each new point, while the last two points and the new point make a right turn (cross product > 0), pop the last point. But that's for the lower hull. For the upper hull, we pop when the cross product is negative? Let's derive: We want the upper hull to be the set of points that are extreme in the upper direction. The convex hull is the intersection of all half-planes. The upper hull is the chain from leftmost to rightmost along the top. For this chain, as we go from left to right, the slopes should be decreasing? Or increasing? Consider points (0,0), (1,10), (2,0). The upper hull is the two edges: (0,0)-(1,10) and (1,10)-(2,0). The slopes are 10 and -10. They are not monotonic. Actually, the upper hull can have slopes that decrease and then increase? No, the upper hull is a concave function? Let's plot: (0,0) to (1,10) to (2,0). This is a hill. The upper hull is the entire set of points. The slopes: 10 then -10. They decrease. So the slopes are decreasing. If we have a third point (3,5), the upper hull might be (0,0)-(1,10)-(3,5). The slopes: 10 and then (5-10)/(3-1) = -2.5. So decreasing. So for the upper hull, the slopes of the edges are decreasing. That means as we go right, the slope gets smaller. So when adding a new point, if the new slope (from new point to the last point) is greater than the previous slope (from second last to last), then the last point is below the line from second last to new point? Actually, if the new slope is greater than the previous slope, then the sequence of slopes is not decreasing, so the last point is not on the upper hull. So we should pop the last point if the new slope is greater than the previous slope. But careful: the slope from A to B is (H_B - H_A)/(X_B - X_A). For the upper hull, we want the slopes to be strictly decreasing. So if we have A, B, C in the hull, we want slope(A,B) > slope(B,C). If adding C makes slope(B,C) >= slope(A,B), then B is below the line from A to C, so B is not on the upper hull. So we pop B. This is equivalent to checking the cross product: (B-A) x (C-B) = (X_B - X_A)*(H_C - H_B) - (H_B - H_A)*(X_C - X_B). If this is >= 0, then the turn is left (counterclockwise), meaning the slope from A to B is less than the slope from B to C? Let's compute: slope(A,B) = (H_B - H_A)/(X_B - X_A). slope(B,C) = (H_C - H_B)/(X_C - X_B). If slope(A,B) < slope(B,C), then (H_B - H_A)/(X_B - X_A) < (H_C - H_B)/(X_C - X_B) => cross product < 0. So if cross product < 0, slope(A,B) < slope(B,C), which means slopes are increasing. But we want decreasing slopes for upper hull. So we should pop when cross product < 0? Wait, if slopes are increasing, that's a left turn (counterclockwise). For the lower hull, we want the hull to be convex (curving upward), so we want left turns (cross product > 0). For the upper hull, we want the hull to be concave (curving downward), so we want right turns (cross product < 0). So we should pop when the cross product is > 0? Let's test with (0,0), (1,10), (2,0). A=(0,0), B=(1,10), C=(2,0). cross = (1-0)*(0-10) - (10-0)*(2-1) = 1*(-10) - 10*1 = -20 < 0. So cross < 0. This is a right turn. We want to keep B. So we pop when cross > 0. So condition: while len(deque) >= 2 and cross(deque[-2], deque[-1], new_point) >= 0, pop right. Because if cross >= 0, it's a left turn, which means the new point is "above" the line from second last to last? Actually, cross >= 0 means (B-A) x (C-B) >= 0. In our example, cross was -20, so we don't pop. Good. If we had (0,0), (1,1), (2,10): A=(0,0), B=(1,1), C=(2,10). cross = (1-0)*(10-1) - (1-0)*(2-1) = 9 - 1 = 8 > 0. This is a left turn. Is B on the upper hull? The points are (0,0), (1,1), (2,10). The line from A to C is slope 5. At X=1, height is 5. B is at 1, which is below the line. So B is below the line from A to C, so B is not on the upper hull. The upper hull should be just A and C. So we should pop B. And indeed cross > 0, so we pop. So the condition is correct: pop while cross >= 0.

So the algorithm for adding point i to the hull:
while len(dq) >= 2 and cross(dq[-2], dq[-1], i) >= 0:
    dq.pop()
dq.append(i)

Now, for querying: we need to find the point in dq that maximizes the y-intercept with i. The y-intercept function for a fixed i as a function of the left point j is f(j) = (H_j X_i - H_i X_j) / (X_i - X_j). As X_i increases, the optimal j moves to the right. We can maintain a pointer or pop from the front. The condition to pop from front: if the y-intercept with the second point is greater than with the first point, then the first point is no longer optimal. So we check:
Let a = dq[0], b = dq[1]. Compute f(a, i) and f(b, i). If f(b, i) > f(a, i), then pop left.
We can compare them without division: 
(H_b X_i - H_i X_b) * (X_i - X_a) > (H_a X_i - H_i X_a) * (X_i - X_b).
This is safe with Python integers.

So the steps for each i:
- While len(dq) >= 2 and the y-intercept with dq[0] is <= y-intercept with dq[1], pop left.
- Let j = dq[0]. Compute L = max(L, (H_j * X_i - H_i * X_j) / (X_i - X_j)).
- Then add i to hull: while len(dq) >= 2 and cross(dq[-2], dq[-1], i) >= 0: pop right.
- Append i.

We need to handle the case where dq has only one point: then we just use that point.

After processing all, L is the answer. If L <= 0, print -1, else print L.

Let's test this algorithm on sample 1:
Points: (3,2), (5,4), (7,5)
i=1: dq = [(3,2)]
i=2 (5,4):
  dq has one point, so j=(3,2). f = (2*5 - 4*3)/(5-3) = (10-12)/2 = -1. L = -1.
  Add (5,4): dq has only one point, append. dq = [(3,2), (5,4)].
i=3 (7,5):
  Query: dq has two points. Check f(dq[0], i) vs f(dq[1], i).
    f((3,2), (7,5)) = (2*7 - 5*3)/4 = (14-15)/4 = -0.25.
    f((5,4), (7,5)) = (4*7 - 5*5)/2 = (28-25)/2 = 1.5.
  Since 1.5 > -0.25, pop left. dq = [(5,4)].
  Now j = (5,4). f = 1.5. L = 1.5.
  Add (7,5): dq has one point, append. dq = [(5,4), (7,5)].
End. L = 1.5. Output 1.5. Correct.

Sample 4: (10,10), (17,5), (20,100), (27,270)
i=1: dq=[(10,10)]
i=2 (17,5):
  j=(10,10): f = (10*17 - 5*10)/(17-10) = (170-50)/7 = 120/7 ≈ 17.14. L=17.14.
  Add (17,5): dq=[(10,10), (17,5)]
i=3 (20,100):
  Query: compare f((10,10), (20,100)) and f((17,5), (20,100)).
    f1 = (10*20 - 100*10)/10 = (200-1000)/10 = -80.
    f2 = (5*20 - 100*17)/3 = (100-1700)/3 = -1600/3 ≈ -533.33.
  f1 > f2, so don't pop. j=(10,10). f = -80. L stays 17.14.
  Add (20,100): check cross of (10,10), (17,5), (20,100):
    cross = (17-10)*(100-5) - (5-10)*(20-10) = 7*95 - (-5)*10 = 665 + 50 = 715 > 0. So pop right: pop (17,5). dq=[(10,10)]. Append (20,100). dq=[(10,10), (20,100)].
i=4 (27,270):
  Query: dq=[(10,10), (20,100)].
    f1 = (10*27 - 270*10)/17 = (270-2700)/17 = -2430/17 ≈ -142.94.
    f2 = (100*27 - 270*20)/7 = (2700-5400)/7 = -2700/7 ≈ -385.71.
  f1 > f2, so don't pop. j=(10,10). f = -142.94. L stays 17.14.
  Add (27,270): check cross of (10,10), (20,100), (27,270):
    cross = (20-10)*(270-100) - (100-10)*(27-10) = 10*170 - 90*17 = 1700 - 1530 = 170 > 0. So pop right: pop (20,100). dq=[(10,10)]. Append (27,270). dq=[(10,10), (27,270)].
End. L = 120/7 ≈ 17.142857. Correct.

So the algorithm works.

Now, we need to implement this carefully. The comparison for popping from front uses cross multiplication with large numbers. Python int is fine.

The cross product for hull maintenance: (x2-x1)*(y3-y2) - (y2-y1)*(x3-x2). This is also large but fine.

Finally, we need to output with high precision. Python's float is double, which has about 15-16 decimal digits. The error tolerance is 1e-9, so double is fine. But we can also use fractions for exactness? Not necessary, but we can output with enough digits.

One edge case: if L is negative, we output -1. But what if L is exactly 0? The problem says "if it is possible to see all buildings at height 0 at coordinate 0, report -1". At height 0, if L=0, then the condition for all visible is h > 0. So at h=0, not all are visible. So we should output 0.0. In sample 3, L=0, output 0.0. So we only output -1 if L < 0? Actually, if L = 0, then from height 0, we cannot see all (since need h > 0). So answer is 0. If L < 0, then h=0 satisfies h > L, so all visible, answer -1. So condition: if L <= 0? Wait, if L = 0, h=0 gives 0 > 0 false, so not all visible. So answer is 0. If L < 0, h=0 gives 0 > L true, so all visible, answer -1. So we output -1 if L < 0, and 0 if L = 0. So we can check: if L < 0, print -1. Else print L.

But careful: floating point precision. We should use a small epsilon? Actually, since L is computed as a double, we can compare with 0 with some tolerance. But the problem says answers with absolute or relative error at most 1e-9. So if L is very small negative due to floating point, we might output -1 incorrectly. Better to compute L exactly as a rational number? We can keep track of the maximum fraction, but comparisons for popping use cross multiplication which is exact. At the end, L is a double. We can just check if L < 0 with a small epsilon, say -1e-12. Or we can keep L as a float but compute it as a fraction with numerator and denominator. But the output requires a floating point number. We can output the float. Since we use exact integer comparisons for the algorithm, the float computed for the final L might have a small error, but it's fine. However, when we decide whether to output -1, we should be careful. If the true L is 0, due to floating point it might be slightly positive or negative. We can instead keep track of the exact maximum numerator/denominator? But we don't need to store all, we can just keep the float. Given the constraints, the numbers are up to 1e9, and N=2e5. The maximum y-intercept could be large, up to 1e9. The precision of double is enough. To be safe, we can use Python's Fraction for exact comparison? But that would be slow. We can just use float and when checking if L <= 0, we can use a tolerance: if L < 1e-12, treat as non-positive? Actually, the problem says if it is possible to see all buildings at height 0, report -1. So if the true L is 0, at height 0 we cannot see all. So we should output 0. If the true L is negative, we output -1. So we need to distinguish between 0 and negative. If the computed float is exactly 0, or very close to 0, we should output 0. If it's clearly negative, output -1. Since the algorithm uses exact integer comparisons, the value we compute for L is exactly the maximum of some fractions. We can store L as a float, but we can also keep a separate flag if we ever get a positive value. Actually, we can just maintain L as a float, and if at the end L <= 0 (with a small epsilon like 1e-12), we output -1? But if L is exactly 0, we want 0. If L is -1e-15, we want -1. So we can check: if L < 0 and L > -1e-12, it might be 0. But it's easier: since we only care about the sign for the final answer, and we only output the value if it's > 0, we can just check if the maximum numerator we encountered is positive? Actually, we can keep the maximum as a fraction (numerator, denominator) and at the end compare. But we can also just use float and print with enough precision, and if the printed value would be 0, we print 0. But the condition for -1 is strict: if L < 0, print -1. So if L is a very small negative number, we should print -1. If L is 0, print 0. In sample 3, the answer is 0.000000000000000000. So they expect exactly 0. So we can compute L as a double, and if L <= 0, we need to decide. Since the problem says "if it is possible to see all buildings at height 0", and if L=0, it's not possible. So we need to output 0. So we can check if L < 0 (with a small epsilon to avoid floating point issues). Actually, we can just check if the maximum value we computed is strictly less than 0. Since we use exact comparisons for popping, the only floating point operations are the division when computing the candidate value. We can instead keep the candidate as a fraction and compare fractions exactly. But the algorithm requires comparing f(a,i) and f(b,i) to decide popping. We already do that with cross multiplication, which is exact. So we never need the actual float value during the algorithm. At the end, we have the maximum L. We can store L as a tuple (num, den) for the maximum fraction. But we need to compare fractions to find the maximum. We can do that with cross multiplication as well. So we can keep L as a fraction (numerator, denominator) in reduced form? Not necessary; we can keep numerator and denominator as integers (not necessarily reduced) and compare by cross multiplication. When we update L, we check if new_num * L_den > L_num * new_den. Then we can convert to float for output. This avoids floating point errors entirely.

Let's do that: keep L_num = 0, L_den = 1 (representing 0). For each candidate f = (H_j * X_i - H_i * X_j) / (X_i - X_j), let num = H_j * X_i - H_i * X_j, den = X_i - X_j. Note that for left blockers, num could be negative. But we want the maximum. So we compare: if num * L_den > L_num * den, update. At the end, L_val = L_num / L_den. If L_num < 0, print -1. If L_num == 0, print 0.0. Else print L_num / L_den as float.

This is exact and safe.

Now, we need to ensure that the algorithm is O(N). The deque operations are O(1) amortized.

Let's write the code accordingly.

One more thing: the problem says "Height must be non-negative; if it is possible to see all buildings at height 0 at coordinate 0, report -1 instead." So we only consider h >= 0. If the maximum L is negative, that means from height 0 we can see all, so -1. If L is positive, answer is L. If L is exactly 0, answer is 0.

So the plan is solid.

## worker: Implement the sweep with a deque maintaining the u
The algorithm correctly identifies the threshold height `L` as the maximum y-intercept of any line through two buildings. By sweeping from left to right and maintaining the upper convex hull of previous points in a deque, we can query the optimal left blocker for each new building in amortized O(1) time. The convex hull maintenance uses exact integer cross products to avoid floating point errors during comparisons. The maximum fraction is stored as numerator/denominator and updated using exact cross multiplication, so the final answer is computed from exact integers and only converted to float for output, ensuring the required precision. The final check handles the case where the maximum is negative (output -1) versus zero/positive (output the value).
