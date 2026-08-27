
## ideation
The problem asks us to simulate the movement of smoke on a 2D grid with a campfire at (0,0).
Smoke particles are born at (0,0) at certain time steps.
Specifically, a particle is born at time $t$ if and only if no smoke exists at (0,0) after the wind blows at time $t$.
We need to determine if smoke exists at a target cell $(R, C)$ at time $t+0.5$ for each $t=1, \dots, N$.
Time $t+0.5$ corresponds to the state after the wind blows at time $t$, but before the regeneration at time $t$ is considered for the next step (or effectively, the regeneration at time $t$ has happened, but since $(R, C) \neq (0,0)$, the newly generated smoke at (0,0) doesn't affect the check for $(R, C)$).
Actually, the check for smoke at $(R, C)$ at $t+0.5$ depends on particles born at times $b < t$.
The condition for a new particle to be born at time $t$ depends on whether any particle born at $b < t$ is at (0,0) after wind blows at time $t$.

Let $D_t$ be the position of the "original" particle (born at $t=0$) after $t$ wind steps.
$D_0 = (0,0)$.
$D_t = D_{t-1} + \text{move}(S[t-1])$.
A particle born at time $b$ ($0 \le b < t$) is at position $D_t - D_b$ at time $t$.
Smoke exists at $(R, C)$ at time $t+0.5$ if and only if there exists $b < t$ such that $D_t - D_b = (R, C)$, i.e., $D_b = D_t - (R, C)$.
Smoke exists at (0,0) at time $t$ (after wind) if and only if there exists $b < t$ such that $D_t - D_b = (0,0)$, i.e., $D_t = D_b$.
A new particle is generated at time $t$ if and only if no smoke exists at (0,0) at time $t$, i.e., $D_t \notin \{ D_b \mid b < t \}$.

Algorithm:
1. Maintain a set `visited` containing $D_b$ for all birth times $b$ encountered so far. Initially `visited = {(0,0)}`.
2. Maintain `curr` position, initially $(0,0)$.
3. For each time step $t=1$ to $N$:
   - Update `curr` according to $S[t-1]$. This is $D_t$.
   - Check if smoke exists at $(R, C)$: This is true if $D_t - (R, C) \in \text{`visited`}`.
   - Check if new smoke is generated: This is true if $D_t \notin \text{`visited`}`.
     - If new smoke is generated, add $D_t$ to `visited`.
4. Output the results.

Complexity: $O(N)$ time, $O(N)$ space.

## worker: Implement a function to update the current coordin
The problem asks us to determine if smoke exists at a target cell $(R, C)$ at specific time points.
Smoke particles are born at $(0,0)$ at time $t$ if and only if no smoke exists at $(0,0)$ after the wind blows at time $t$.
Let $D_t$ be the position of the "original" smoke particle (born at $t=0$) after $t$ wind steps.
A particle born at time $b$ ($0 \le b < t$) is at position $D_t - D_b$ at time $t$.
Smoke exists at $(R, C)$ at time $t$ if and only if there exists a birth time $b < t$ such that $D_t - D_b = (R, C)$, which simplifies to $D_b = D_t - (R, C)$.
A time $b$ is a birth time if and only if $D_b$ is a new position not visited by the original particle before time $b$.
Thus, we need to check if $D_t - (R, C)$ is in the set of unique positions visited by the original particle up to time $t-1$.
We can maintain a set `visited` of these unique positions. Initially, it contains $(0,0)$.
In each step $t$, we update the current position $D_t$ based on the wind direction.
We check if $(D_t[0] - R, D_t[1] - C)$ is in `visited`. If yes, smoke exists at $(R, C)$.
Then, if $D_t$ is not in `visited`, we add it, indicating that a new particle is born at $(0,0)$ at time $t$.
This approach runs in $O(N)$ time and uses $O(N)$ space.
