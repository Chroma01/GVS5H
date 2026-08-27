
## ideation
The problem asks whether we can color an N×N grid so that each row and each column consists of a prefix of black cells followed by white cells. This is equivalent to finding a Young diagram (order ideal) that contains all precolored black cells and excludes all precolored white cells. A key observation is that such a diagram exists if and only if no white cell lies southwest of any black cell (i.e., there is no pair (B, W) with B.x ≥ W.x and B.y ≥ W.y). If such a pair exists, the white cell would be forced to be black by the prefix conditions, causing a contradiction. Conversely, if no such pair exists, we can take the lower closure of the black cells as the diagram, which will contain all black cells and no white cells.

To check efficiently, we can sort black cells by column (y-coordinate) descending and white cells by column descending. While sweeping through the white cells, we maintain the maximum row (x-coordinate) among black cells with column ≥ current white cell's column. If this maximum row is ≥ the white cell's row, a conflict is found. This runs in O(M log M) time due to sorting.

Pitfalls: 
- Ensure we sort by the correct coordinate (column index y) and compare row indices x.
- Handle edge cases where there are no black or no white cells (always possible).
- N can be up to 1e9, but coordinates fit in integers.

## worker: Implement the sweep algorithm in Python: read N an
The algorithm checks for the existence of a conflict where a white cell is southwest of a black cell. By sorting black cells by column descending and sweeping through white cells, we efficiently maintain the maximum row among black cells with sufficient column index. If this maximum row is at least the white cell's row, a conflict exists and we output "No". Otherwise, a valid Young diagram exists (constructed as the lower closure of black cells), so we output "Yes". The time complexity is O(M log M) due to sorting, and M ≤ 2×10⁵ ensures this is fast. The constraints on N (up to 10⁹) do not affect the algorithm since we only process given cells.
