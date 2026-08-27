We need to simulate a sequence of axis-aligned moves and count how many distinct house points are visited or passed through. Since moves are up to 1e9 steps, we cannot enumerate intermediate points. We only care about houses that lie exactly on each segment.

Approach:
1. Group houses by their y-coordinate (for vertical moves) and by their x-coordinate (for horizontal moves) using dictionaries mapping coordinate value to list of (other coord, index).
2. Sort each list to allow binary search (bisect) to find houses within the inclusive range of a move.
3. Simulate moves in order. For each move, we compute the target endpoint using 64-bit arithmetic (Python ints handle it). Then, depending on direction, we query the appropriate dictionary: for L/R look up current y; for U/D look up current x. Binary search to collect houses whose other coordinate lies between start and end (inclusive), using a while loop that repeatedly pops the leftmost (or rightmost) qualifying house and marks them as seen. This avoids revisiting houses.
4. Keep a boolean array `seen` of length N, and an integer `count` of distinct houses encountered so far. When we find an unvisited house index, mark seen and increment count.
5. Output final (x, y) and count.

Complexities: O(N log N + M log N) time, O(N) memory.