
## ideation
The core difficulty is that the set of absorbable cells is dynamic: absorbing one slime both increases Takahashi’s strength and exposes new boundary cells. The order of absorption must be handled carefully, especially because the condition is strict. Comparisons should avoid floating point and use the equivalent integer inequality \(X \cdot S_{\text{candidate}} < \text{current strength}\). Strength sums can reach roughly \(2.5\times 10^{17}\), so 64-bit arithmetic is required.

A useful invariant is that only slimes adjacent to the already absorbed region can be considered. If the smallest-strength boundary slime is not eligible, then no other boundary slime is eligible either. Consequently, repeatedly processing the minimum boundary value reaches the maximal closure. Every grid cell should be inserted into the frontier at most once, and stale entries or already absorbed cells must be ignored.

## worker: Implement the min-heap frontier expansion: parse i
The absorbed cells always form a connected region, and the heap stores exactly its unabsorbed neighboring cells. Processing the smallest boundary slime is optimal: if it is not absorbable, every other boundary slime is at least as large and is also not absorbable. Therefore the process can stop immediately.

The strict condition is checked with integer arithmetic as `value * X < current`, avoiding floating-point errors. Each cell is inserted into the heap at most once, giving `O(HW log(HW))` time and `O(HW)` memory.
