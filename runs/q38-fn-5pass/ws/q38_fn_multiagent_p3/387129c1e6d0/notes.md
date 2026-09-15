
## ideation
The core difficulty is that the path is a union of up to 200,000 axis-aligned continuous segments, while the houses are up to 200,000 integer points in a huge coordinate range. A direct simulation checking every house against every segment is impossible. The problem must be reduced to efficient geometric range queries or sweep-line processing.

There are several subtle issues:
- Segments are inclusive of their endpoints, so a house exactly at a segment endpoint counts.
- Horizontal and vertical segments can overlap, touch, or intersect, causing the same house to be counted multiple times unless deduplicated.
- Coordinates and the final position can exceed 32-bit integer range, so 64-bit arithmetic is required in languages with fixed-width integers.
- Houses are distinct, but segments may be repeated or overlapping, so counting must be based on the union of covered points, not raw segment traversals.
- A house may be covered by both horizontal and vertical segments, so if horizontal and vertical coverage are counted separately, double-counted houses must be removed.

The natural decomposition is to treat horizontal coverage and vertical coverage separately, because a house is on a horizontal segment if its y-coordinate matches the segment and its x-coordinate lies within the segment interval, and similarly for vertical segments. The main challenge is doing this efficiently and then combining the two counts without double-counting.
