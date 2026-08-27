
## ideation
The problem requires simulating insertions into an array, but a direct simulation is too slow ($O(N^2)$) for $N \le 5 \times 10^5$. The key insight is to reverse the process: determine the final position of each number by working backwards from $N$ to $1$. 

At step $i$ (going backwards), the number $i$ was inserted at position $P_i$ in an array of size $i$. This means that in the final array of size $N$, the number $i$ occupies the $P_i$-th "available" slot among the remaining empty positions. 

We can use a Fenwick tree (Binary Indexed Tree) to efficiently find the $k$-th available position and mark it as occupied. Specifically:
1. Initialize a BIT with 1s at all positions 1 to $N$.
2. For $i$ from $N$ down to $1$, find the $P_i$-th position that still has a 1 in the BIT (using binary search on the BIT prefix sums).
3. Place $i$ at that position and update that position to 0 in the BIT.

This approach runs in $O(N \log N)$, which is efficient enough for the given constraints.

## worker: finalize
The solution uses a Fenwick Tree (BIT) to efficiently determine the final position of each number by reversing the insertion process. 

**Key Insight:** Instead of simulating insertions forward (which requires O(N) shifts per insertion, leading to O(N²) total), we work backwards from N to 1. When we process number i, it was inserted at position P_i in an array of size i. In the final array of size N, this corresponds to the P_i-th "available" (unoccupied) slot.

**Algorithm:**
1. Initialize a BIT with 1s at all positions 1 to N, representing all slots as available.
2. For i from N down to 1:
   - Find the P_i-th position that still has a 1 in the BIT using binary lifting on the BIT (O(log N)).
   - Place i at that position in the result array.
   - Update the BIT to mark that position as occupied (set to 0).
3. Output the result array.

**Complexity:** O(N log N) time and O(N) space, which is efficient for N ≤ 5×10⁵.
