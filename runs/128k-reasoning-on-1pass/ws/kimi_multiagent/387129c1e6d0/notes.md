
## ideation
Core difficulty: the path length can be astronomically large (`M * C_i` up to `2e14`), so step-by-step simulation is impossible. Each move is axis-aligned, so a house can only be encountered if it shares the current `y` for L/R moves or current `x` for U/D moves and lies between the inclusive endpoints. The count is over distinct houses on the union of all segments, so segment order matters only for the final coordinate, not for which houses are covered.

The proposed row/column sorted-list + DSU successor idea is viable, but a simpler and more robust approach is to build the union of horizontal intervals per `y` and vertical intervals per `x`, merge intervals, then test each house once against these merged interval maps. This avoids repeatedly scanning already-found houses and avoids DSU-per-line complexity. A house at an intersection of a horizontal and vertical segment could otherwise be double-counted, so either test each house globally as “covered by horizontal union OR covered by vertical union,” or maintain a global visited set.

Pitfalls: normalize segment endpoints with `min/max`; intervals are inclusive; do not enumerate by distance; repeated passes over the same house must not inflate count or runtime; use fast input/output; coordinate values are large but Python integers avoid overflow; merging must handle many distinct lines efficiently with dictionaries; be careful that a house is counted if it lies on any segment, even if only at an endpoint.

## worker: Implement the interval-union solution: parse input
- Each move is axis-aligned, so it can only cover houses on one horizontal line (`y = const`) or one vertical line (`x = const`).
- While simulating the moves, the program stores normalized inclusive intervals: horizontal intervals grouped by `y`, vertical intervals grouped by `x`.
- Intervals on the same line are merged; because all house coordinates are integers, merging intervals with `l <= prev_r + 1` is safe.
- Each house is tested once with binary search against the merged horizontal intervals on its row and, if not found there, against the merged vertical intervals on its column. This counts every distinct house at most once.
- Python integers avoid overflow even though coordinates can reach about `3e14`.
