We need to simulate Santa's movement on an axis-aligned Manhattan path, counting how many distinct house coordinates lie on any segment of his trajectory. Since houses are unique points, the total number of points that can ever be visited is ≤ N (2e5). For each house we can precompute the time (move index and parameter) when Santa would pass it, if any. Because moves are axis-aligned and houses have integer coordinates, a house (hx, hy) is visited during a move i iff one coordinate equals Santa's coordinate at the start of that move and the other lies within the segment range. We can binary search Santa's coordinate after each move prefix: for each house, find the first move where its x-coordinate is "skipped" (i.e., never revisited after the start). Actually a more direct method: simulate all moves while maintaining Santa's current x,y and the move index. For each house, we need to know if it lies on some segment. Since N and M are up to 2e5, O((N+M) log(N+M)) is fine.

We process moves one by one. For each move we want to know which houses have a coordinate equal to the moving axis and lie within the range. We can maintain two maps: for each x-coordinate, the set of y-values of houses with that x; for each y-coordinate, the set of x-values of houses with that y. When Santa moves vertically (U/D), let cx = current x, range [y1, y2]. We need all y such that (cx, y) is a house and y in range. So we look up the set of y's for x=cx, and count how many are in the interval. Similarly for horizontal moves. This can be done efficiently with balanced BSTs (sorted lists) and binary search to find the first element ≥ lo, then iterate while ≤ hi. However, iterating could be O(k) where k is houses matched in that move, but overall each house is processed at most once (when found) so total O(N log N + M log N). Use `bisect` on sorted lists stored in dicts.

When we find a house (hx, hy) during a move, we need to mark it as counted and also delete it from both maps to avoid future counting. So after counting, remove hy from xmap[hx] and remove hx from ymap[hy].

Implementation steps:
1. Read N, M, Sx, Sy.
2. Read houses into list.
3. Build `xmap = defaultdict(list)`: for each house, append hy to xmap[hx] then sort each list.
4. Build `ymap = defaultdict(list)`: similarly for y.
5. Initialize (cx, cy) = (Sx, Sy).
6. For each of M moves:
   - Read dir, step.
   - Determine new position (nx, ny) accordingly.
   - If dir in U/D (vertical):
        lo, hi = min(cy, ny), max(cy, ny).
        lst = xmap.get(cx, []).
        Find idx = bisect_left(lst, lo).
        Iterate j from idx while j < len(lst) and lst[j] <= hi:
            hy = lst[j]
            count += 1
            Remove from ymap[hy]: ymap[hy].remove(cx) – need O(1) removal? Use set for ymap? But we need sorted order for binary search on ymap too. For ymap, we only need to delete a single element when we count a house. We can store ymap as dict of sorted lists and when removing, do `ymap[hy].pop(bisect_left(ymap[hy], cx))` – O(log N) per removal, fine.
            Also remove hy from xmap[cx] similarly: `xmap[cx].pop(idx+j offset?)` but we are iterating, so easier: after collecting all y's to remove, we can delete them. To keep it simple, we can iterate with while loop, each time get idx = bisect_left(lst, lo), if idx < len(lst) and lst[idx] <= hi, then pop that element (using `pop(idx)`) which is O(N) per pop? That would be O(k^2) worst-case. Better: collect all matching y's into a list, then after loop, remove them from the sorted list by building a new list (filter). Since each house is removed at most once, total cost of rebuilding lists is O(N) across all moves. So: for each vertical move:
            - Get lst = xmap[cx] (sorted list).
            - i = bisect_left(lst, lo)
            - j = bisect_right(lst, hi)
            - matched = lst[i:j]
            - count += len(matched)
            - new_lst = lst[:i] + lst[j:]
            - xmap[cx] = new_lst
            - For each hy in matched: remove cx from ymap[hy] similarly.
        Similarly for horizontal moves.
   - Update cx, cy to nx, ny.
7. At the end, print cx, cy, count.

Edge cases: houses can have coordinates outside any movement, not counted. Houses at start point are guaranteed none.

Complexities: O((N+M) log N) time, O(N) memory.