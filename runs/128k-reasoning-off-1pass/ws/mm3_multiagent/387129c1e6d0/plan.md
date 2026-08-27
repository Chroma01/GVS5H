We must simulate Santa's path segment by segment, efficiently counting how many distinct houses he visits. Each segment is axis-aligned (horizontal or vertical). For a horizontal move, houses that lie exactly on that segment have y = current y and x between min and max of the segment. Similarly for vertical moves. Since N and M are up to 2e5, we need O((N+M) log N) per segment. We can preprocess house points grouped by x-coordinate and y-coordinate using dictionaries mapping coordinate to sorted list of y values (for vertical) or x values (for horizontal), plus a set to deduplicate counted houses.

Processing each segment:
- Compute new position (x', y') from current (x, y) and direction/distance.
- If horizontal: let y0 = y (constant), x_low = min(x, x'), x_high = max(x, x'). Look up houses with y == y0: if the dictionary for y0 exists, binary search for the first index >= x_low and the first index > x_high; for each house in that range, if not yet counted, add to global set and increment counter. Also, check if the house at the start or end position exists and is on this segment (we can just include endpoints in the range; the binary search range includes them).
- If vertical: similar using x-coordinate mapping to sorted y lists.
- Update current position.

Time per segment: O(log N) for binary search. Overall O((N+M) log N). Use 64-bit integers (Python int is arbitrary).