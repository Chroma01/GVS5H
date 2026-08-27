1. Identify all starting positions of '1' in the grid, as every valid segment must begin with a 1.
2. For each starting '1', explore all 4 diagonal directions. For each direction, extend the sequence following the pattern 2, 0, 2, 0, ... as long as possible.
3. At each step in the extension, check if a 90-degree clockwise turn is possible. A 90-degree clockwise turn from a diagonal direction means switching to the next diagonal direction in the order: (1,1) -> (1,-1) -> (-1,-1) -> (-1,1) -> (1,1).
4. After turning, continue extending in the new direction following the same sequence pattern. The total length is the sum of the lengths of the two segments (including the turning point once).
5. Track the maximum length found across all starting points and directions.