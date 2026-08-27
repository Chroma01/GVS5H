
## ideation
The problem asks whether smoke exists at a specific target cell $(R, C)$ at half-integer times $t + 0.5$ for $t = 1, \dots, N$.

Let's trace the movement of smoke:
1.  At $t=0$, smoke is at $(0,0)$.
2.  For each step $k=1, \dots, N$:
    *   First, all existing smoke moves according to the $k$-th character of $S$.
    *   Then, if there is no smoke at $(0,0)$, new smoke is generated at $(0,0)$.

We need to determine if smoke is at $(R, C)$ at time $t + 0.5$. This is the state *after* the wind has blown at step $t$ but *before* any new smoke generation at step $t+1$ (which happens at integer time $t+1$). Actually, the problem says "at time $t+0.5$", which is after the wind blow at step $t$ and before the potential new smoke generation at step $t+1$ (which would happen at integer time $t+1$). Wait, let's re-read carefully.
"At times $t=1,2,\dots,N$, the following happen in order: Wind blows... If there is no smoke in cell (0,0), new smoke is generated at cell (0,0)."
The state at $t+0.5$ is after the wind blow of step $t$ and before the wind blow of step $t+1$. The new smoke generation happens immediately after the wind blow of step $t$. So, at $t+0.5$, the smoke present consists of:
*   Smoke that was present before step $t$'s wind, moved by the wind.
*   Smoke that was just generated at $(0,0)$ at the end of step $t$ (if generated).

Let $P_k$ be the position of a particle that started at $(0,0)$ at time $k$ (meaning it was generated at the end of step $k$, or initially at $t=0$).
Actually, it's easier to think about the cumulative displacement.
Let $D_t$ be the net displacement vector from $(0,0)$ after applying the first $t$ wind blows.
$D_0 = (0,0)$.
$D_t = D_{t-1} + \text{direction}(S[t-1])$ for $t \ge 1$.

Consider a "batch" of smoke generated at the end of step $k$ (where $k=0$ corresponds to the initial smoke at $t=0$).
This batch starts at $(0,0)$ at time $k$.
At time $t$ (after wind blow $t$), this batch has been subjected to wind blows $k+1, \dots, t$.
The net displacement from time $k$ to time $t$ is $D_t - D_k$.
So, the position of this batch at time $t$ (after wind blow $t$) is $(0,0) + (D_t - D_k) = D_t - D_k$.

The problem asks if smoke exists at $(R, C)$ at time $t+0.5$.
At this moment, the smoke present is the union of all batches generated at steps $k < t$ (including $k=0$) that have moved to $(R, C)$.
Specifically, a batch generated at step $k$ (end of step $k$) is at $(R, C)$ at time $t+0.5$ if:
$D_t - D_k = (R, C)$
$\implies D_k = D_t - (R, C)$

Note: The smoke generated at step $t$ (if any) is at $(0,0)$ at time $t+0.5$. It will only be at $(R, C)$ if $(R, C) = (0,0)$, but the constraints say $(R, C) \neq (0,0)$. So we only care about batches generated at $k < t$.
Also, smoke generated at step $k$ exists at time $t+0.5$ only if it hasn't been "reset" or something? No, smoke persists. The only condition for new smoke is "if there is no smoke in cell (0,0)". This affects *whether* new smoke is generated, but it doesn't remove existing smoke. So all previously generated smoke batches continue to exist and move.

So, for each $t \in \{1, \dots, N\}$, we need to check if there exists any $k \in \{0, \dots, t-1\}$ such that $D_k = D_t - (R, C)$.

Algorithm:
1.  Initialize current position $D = (0,0)$.
2.  Store seen positions in a set `seen`. Initially `seen = {(0,0)}`.
3.  For $t = 1$ to $N$:
    a. Update $D$ by adding the direction corresponding to $S[t-1]$.
    b. Target position for a previous start point is $Target = D - (R, C)$.
    c. Check if $Target$ is in `seen`.
    d. If yes, output '1'; else '0'.
    e. Add current $D$ to `seen`. (This $D$ corresponds to $D_t$, which will be a candidate $D_k$ for future $t' > t$).

Wait, let's verify the timing.
At $t=1$:
Wind blows. $D_1$ is calculated.
We check if any $k < 1$ (i.e., $k=0$) satisfies $D_0 = D_1 - (R, C)$.
$D_0 = (0,0)$. So check if $(0,0) = D_1 - (R, C) \implies D_1 = (R, C)$.
If smoke generated at $t=0$ is at $(R, C)$ after wind 1, then yes.
Then we add $D_1$ to `seen`.

At $t=2$:
Wind blows. $D_2$ is calculated.
We check if any $k \in \{0, 1\}$ satisfies $D_k = D_2 - (R, C)$.
This covers smoke from initial batch ($k=0$) and smoke generated at end of step 1 ($k=1$).
Then add $D_2$ to `seen`.

This logic holds. The constraint $(R, C) \neq (0,0)$ ensures we don't have to worry about the newly generated smoke at step $t$ being at $(R, C)$ immediately, because it's at $(0,0)$.

Complexity: $O(N)$ time and space. $N \le 200,000$, so this is efficient.

Pitfalls:
- Coordinate system: N is $r-1$, S is $r+1$, W is $c-1$, E is $c+1$.
- Using a set of tuples for $(r, c)$ in Python is fine.
- Input parsing.

## worker: none
The problem asks whether smoke exists at $(R, C)$ at time $t+0.5$ for each $t=1 \dots N$.
Smoke is generated at $(0,0)$ at $t=0$ and potentially at the end of each step $k$ if no smoke is at $(0,0)$ after the wind blow. However, the condition "if there is no smoke in cell (0,0)" only determines *if* new smoke is generated; it does not remove existing smoke. All smoke batches persist and move according to the wind.

Let $D_t$ be the net displacement vector from $(0,0)$ after the first $t$ wind blows. $D_0 = (0,0)$.
A batch of smoke generated at the end of step $k$ (where $k=0$ is the initial smoke) starts at $(0,0)$ at time $k$. After the wind blows at steps $k+1, \dots, t$, this batch will be at position $D_t - D_k$.
We want to know if any batch is at $(R, C)$ at time $t+0.5$. This happens if there exists some $k < t$ such that $D_t - D_k = (R, C)$, or equivalently $D_k = D_t - (R, C)$.
Note that smoke generated at step $t$ (if any) is at $(0,0)$ at time $t+0.5$. Since $(R, C) \neq (0,0)$, this new smoke cannot be at $(R, C)$ at time $t+0.5$. Thus, we only need to check $k < t$.

Algorithm:
1. Maintain a set `seen` of all cumulative displacements $D_k$ for $k < t$. Initially, `seen = {(0,0)}`.
2. Iterate $t$ from 1 to $N$:
   a. Update current displacement $D_t$ based on $S[t-1]$.
   b. Check if $D_t - (R, C)$ is in `seen`. If yes, smoke exists at $(R, C)$ at $t+0.5$.
   c. Add $D_t$ to `seen` for future checks.
3. Output the results.

Time Complexity: $O(N)$ because each step involves constant-time set operations.
Space Complexity: $O(N)$ to store the set of seen displacements.
