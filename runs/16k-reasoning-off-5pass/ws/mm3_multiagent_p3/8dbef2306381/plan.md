We have a line of squares 1..N with M disjoint "bad" intervals. From any position x, we may jump to x+i for any integer i∈[A,B] provided the destination ≤N and not bad. We must decide reachability of N from 1.

Because A,B ≤ 20 but N can be up to 1e12, we cannot BFS over all squares. However, the number of bad intervals M ≤ 2e4 is small. The key observation: along any path, whenever we land in a "good" region (segment between bad intervals or before/after all bad intervals), we can move within it using step sizes between A and B. Since A and B are small, reachability within a contiguous good region reduces to checking that its length is at least A and the gap can be bridged.

Algorithm:
1. Mark the "good" intervals on the number line: 
   - G0 = [1, L1-1] (if L1>1)
   - Gi = [Ri+1, L_{i+1}-1] for i=1..M-1
   - GM = [R_M+1, N]
2. Merge consecutive good intervals that are close enough: if the gap between end of Gi and start of Gi+1 can be crossed in a single jump (i.e., start_{i+1} - end_i ≤ B and ≥ A), they are effectively connected. We propagate connectivity using DSU/union over good intervals.
3. After merging, treat each connected component of good squares as a node. Within a component, we can always reach any square (because step sizes cover a range, and the component is "dense" enough). So we only need to check reachability between components using jumps that cross bad intervals.
4. BFS/DFS on components: from 1's component, try jumping to any other component whose squares are within distance [A,B]. If N is reached, output "Yes", else "No".