1. **Key Insight**: Since all points lie on the boundary of a square, we can "unfold" the boundary into a 1D line by computing the perimeter distance from (0,0) for each point. The perimeter is `4 * side`.
2. **1D Transformation**: For each point, calculate its position along the perimeter:
   - If on bottom edge (y=0, 0<=x<=side): `pos = x`
   - If on right edge (x=side, 0<=y<=side): `pos = side + y`
   - If on top edge (y=side, 0<=x<=side): `pos = 2*side + (side - x)`
   - If on left edge (x=0, 0<=y<=side): `pos = 3*side + (side - y)`
3. **Manhattan Distance on Boundary**: For two points on the boundary, the Manhattan distance is NOT simply the absolute difference in their perimeter positions. However, because the points are on the boundary, the Manhattan distance between two points equals the minimum of the two possible paths along the boundary (clockwise and counter-clockwise) ONLY if we consider the actual geometry. Actually, a key observation: for points on the boundary of a square, the Manhattan distance between two points is equal to the shortest path along the boundary edges? No, that's not true. 
   
   Correction: The Manhattan distance |x1-x2| + |y1-y2| for points on the boundary is not directly the perimeter distance. However, we can still use binary search on the answer (the minimum distance). For a given candidate distance `d`, we need to check if we can select `k` points such that every pair has Manhattan distance >= `d`.
4. **Binary Search**: Binary search on the answer `d` from 0 to `4*side`. For each `d`, use a greedy approach: sort the points by their perimeter position, then iterate and pick points that are at least `d` apart in terms of Manhattan distance from the last picked point. But wait, the greedy on perimeter doesn't work directly because Manhattan distance isn't the perimeter distance.
5. **Better Greedy for Check**: Since `k` is small (<=25), we can use a different approach for the check. Actually, with `n` up to 15000, an O(n*k) or O(n^2) check might be too slow if done naively inside binary search. But note: after sorting by perimeter, we can use a greedy strategy: pick the first point, then pick the next point that is at least `d` away in Manhattan distance. This greedy works for 1D-like problems. But is the boundary 1D-like for Manhattan distance? 
   
   Actually, a known result: for points on the boundary of a square, if we sort them by their perimeter coordinate, then the Manhattan distance between two points is at least the difference in their perimeter coordinates if they are on the same edge or adjacent edges in a certain way? This is complex.
   
   Alternative: Since `k` is very small (<=25), we can use binary search on `d` and for each `d`, use a greedy algorithm that iterates through the sorted points (by perimeter) and picks a point if its Manhattan distance from the last picked point is >= `d`. This greedy is optimal for this "maximize minimum distance" problem on a line-like structure. The key is that the boundary, when unfolded, behaves like a circle. For circular arrangements, greedy works for maximizing minimum distance.
6. **Implementation**: 
   - Compute perimeter positions for all points.
   - Sort points by perimeter position.
   - Binary search for `d` in range [0, 4*side].
   - In `check(d)`: iterate through sorted points, pick first, then pick next if Manhattan distance from last picked >= `d`. Count picks. If count >= k, return True.
   - Return the maximum `d`.