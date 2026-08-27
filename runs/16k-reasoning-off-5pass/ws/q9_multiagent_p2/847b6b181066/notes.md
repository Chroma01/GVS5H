
## ideation
<your analysis>
The problem requires simulating smoke movement on a grid where smoke moves with the wind and regenerates at (0,0) if empty. A direct simulation of all smoke particles is too slow ($O(N^2)$) because the number of particles can grow linearly with $N$.
However, we can observe that any smoke particle present at time $t$ originated from $(0,0)$ at some time $k \le t-1$ (since regeneration happens after the check at $t+0.5$). The position of a particle generated at time $k$ at time $t$ is determined by the cumulative wind displacement from step $k+1$ to $t$.
Let $T_i$ be the cumulative displacement vector after step $i$. The position of the particle generated at time $k$ (available at start of $k+1$) at time $t$ is $T_t - T_k$.
A particle is generated at time $k$ if and only if the position $T_k$ has not been visited by any previous cumulative displacement $T_0, \dots, T_{k-1}$. If $T_k$ repeats a previous position, it means a particle from an earlier time $j$ ($T_j = T_k$) lands on $(0,0)$ at step $k$, preventing regeneration.
Thus, the set of occupied cells at check time $t+0.5$ corresponds to $\{ T_t - T_k \mid 0 \le k < t, T_k \text{ is a new position} \}$.
We need to check if $(R,C)$ is in this set, which is equivalent to checking if $T_k = T_t - (R,C)$ exists in the set of "new" $T_k$ values for $k < t$.
We can solve this in $O(N)$ time by maintaining a hash set of "new" $T_k$ values encountered so far. For each step $t$, we query the set, then update it with $T_t$ if it's a new position.

</analysis>

## worker: Implement the $O(N)$ algorithm using a hash set to
The problem asks us to simulate smoke movement on a grid. The key insight is that the set of occupied cells at time $t+0.5$ can be described mathematically based on the cumulative wind displacements.
Let $T_t$ be the cumulative displacement vector after $t$ wind blows. $T_0 = (0,0)$.
A smoke particle generated at time $k$ (meaning it appeared at $(0,0)$ at time $k+0.5$) will be at position $T_t - T_k$ at time $t+0.5$.
A new particle is generated at time $k$ if and only if no previous particle lands on $(0,0)$ at time $k+0.5$. This happens if $T_k$ has not appeared in the sequence $T_0, T_1, \dots, T_{k-1}$.
Thus, the set of occupied cells at time $t+0.5$ is $\{ T_t - T_k \mid 0 \le k < t, T_k \text{ is unique} \}$.
To check if $(R, C)$ is occupied, we need to verify if there exists a $k < t$ such that $T_k$ is unique and $T_t - T_k = (R, C)$, which simplifies to checking if $T_t - (R, C)$ is in the set of unique $T_k$ values encountered so far.
We can maintain a set of seen positions and a set of unique positions. For each step $t$, we update these sets and perform the check in $O(1)$ time on average. The total time complexity is $O(N)$.

## worker: finalize
The solution implements an $O(N)$ algorithm by leveraging the mathematical property of smoke movement on the grid.
1.  **State Representation**: Instead of simulating every smoke particle (which could be $O(N^2)$), we track the cumulative displacement vector $T_t$ of the "original" smoke from $(0,0)$ after $t$ wind blows.
2.  **Regeneration Logic**: A new smoke particle is generated at $(0,0)$ at time $t+0.5$ if and only if no existing smoke particle lands on $(0,0)$ at that moment. This happens if the current cumulative displacement $T_t$ has not been visited before in the sequence $T_0, T_1, \dots, T_{t-1}$. We maintain a set `unique_positions` containing all such $T_k$ values.
3.  **Query Logic**: At time $t+0.5$, a smoke particle exists at $(R, C)$ if there was a unique particle generated at some time $k < t$ such that its displacement relative to the current wind is exactly $(R, C)$. Mathematically, this means $T_t - T_k = (R, C)$, or $T_k = T_t - (R, C)$. We simply check if this required $T_k$ exists in our `unique_positions` set.
4.  **Complexity**: Each step involves constant time set operations (addition and lookup), leading to an overall time complexity of $O(N)$ and space complexity of $O(N)$, which fits well within the constraints ($N \le 200,000$).
