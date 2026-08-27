
## ideation
The problem asks whether smoke exists at position (R, C) at time t+0.5 for each t from 1 to N.
The key insight is to model the movement of smoke particles.
1. At t=0, smoke is at (0,0).
2. At each integer time t (1 to N), wind blows. Then, if (0,0) is empty, new smoke is generated at (0,0).
3. We need to check if (R,C) has smoke at time t+0.5.

Let's track the position of the "original" smoke particle starting at t=0. Let $P_t$ be the position of this particle at time $t$ (after $t$ wind blows).
$P_0 = (0,0)$.
$P_t = P_{t-1} + \text{wind}_t$.

When new smoke is generated at time $k$ (at position (0,0)), it starts moving with the winds from step $k+1$ onwards.
The position of the smoke particle generated at time $k$ at time $t$ (where $t \ge k$) is determined by applying winds $S[k], S[k+1], \dots, S[t-1]$ to (0,0).
Let $P_t$ be the cumulative displacement from (0,0) after $t$ steps.
The displacement of the particle generated at time $k$ at time $t$ is $P_t - P_k$.
Why? Because the wind effects are additive and translation-invariant. The path from $k$ to $t$ is the same relative displacement as from 0 to $t-k$, but shifted. Specifically, if we define $P_t$ as the position of the particle starting at 0 after $t$ steps, then the position of a particle starting at 0 at time $k$ (which is effectively starting its journey at time $k$) at time $t$ is $P_t - P_k$.

So, at time $t+0.5$, the smoke particle generated at time $k$ (for $0 \le k \le t$) is at position $P_t - P_k$.
Smoke exists at (R,C) at time $t+0.5$ if there exists some $k \in [0, t]$ such that:
$P_t - P_k = (R, C)$
$\iff P_k = P_t - (R, C)$

Therefore, for each $t$, we:
1. Calculate $P_t$ (current position of the original particle).
2. Calculate the target position $T_t = P_t - (R, C)$.
3. Check if $T_t$ has been visited by the trajectory $P_k$ for any $k \in [0, t-1]$. Note: $k=t$ corresponds to new smoke generated at time $t$, which is at (0,0) at time $t+0.5$. So if $T_t = (0,0)$, i.e., $P_t = (R,C)$, then the new smoke at (0,0) is not at (R,C) unless (R,C)=(0,0) which is excluded. Wait, the new smoke is generated at (0,0) at time $t$. At time $t+0.5$, it hasn't moved yet, so it's at (0,0). So if (R,C) == (0,0), it would be 1. But constraints say (R,C) != (0,0). So $k=t$ never contributes to smoke at (R,C) unless (R,C)=(0,0). Thus we only need to check $k < t$. Actually, the set of visited positions should include $P_0, \dots, P_{t-1}$. Then we check if $P_t - (R,C)$ is in that set. Then we add $P_t$ to the set for future steps.

Algorithm:
- Initialize `curr_r = 0`, `curr_c = 0`.
- Initialize a set `visited` containing `(0,0)`.
- For $t$ from 1 to $N$:
  - Update `curr_r`, `curr_c` based on $S[t-1]$. This gives $P_t$.
  - Calculate `target_r = curr_r - R`, `target_c = curr_c - C`.
  - If `(target_r, target_c)` is in `visited`, output '1'. Else '0'.
  - Add `(curr_r, curr_c)` to `visited`.

This is O(N) time and space.

## worker: (None)
The solution uses the key insight that the position of a smoke particle generated at time $k$ (at position $(0,0)$) at time $t$ (where $t \ge k$) is given by $P_t - P_k$, where $P_t$ is the cumulative displacement of the original particle starting at time 0 after $t$ steps. This works because wind movements are translation-invariant and additive.

For each time $t$ from 1 to $N$, we:
1. Compute $P_t$ by applying the $t$-th wind direction to the previous position.
2. Check if there exists any $k \in [0, t-1]$ such that $P_k = P_t - (R, C)$. This is equivalent to checking if the point $(P_t.r - R, P_t.c - C)$ is in the set of previously visited positions $\{P_0, P_1, \dots, P_{t-1}\}$.
3. If such a $k$ exists, smoke is present at $(R, C)$ at time $t+0.5$, so we output '1'. Otherwise, '0'.
4. Add $P_t$ to the set of visited positions for future checks.

The algorithm runs in $O(N)$ time and space, using a hash set for $O(1)$ average-time lookups. This efficiently handles the constraint $N \le 200,000$.
