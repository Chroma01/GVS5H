1.  **Reverse Simulation**: Instead of simulating insertions forward (which is $O(N^2)$), we process the operations in reverse order, from $i=N$ down to $1$.
2.  **Empty Slot Tracking**: We maintain the final array positions as "empty slots". Initially, all $N$ positions are empty.
3.  **Binary Indexed Tree (BIT)**: We use a BIT to efficiently manage the empty slots. The BIT stores the count of empty slots in ranges. Initially, all positions have a count of 1.
4.  **Finding Positions**: For each number $i$ (processing backwards), its position in the final array corresponds to the $P_i$-th currently empty slot. We use binary lifting on the BIT to find the index of the $k$-th empty slot in $O(\log N)$ time.
5.  **Update**: Once the position is found, we place number $i$ there and mark that slot as occupied (update BIT by decrementing the count at that index).
6.  **Complexity**: This approach runs in $O(N \log N)$ time, which fits the constraints $N \le 5 \times 10^5$.