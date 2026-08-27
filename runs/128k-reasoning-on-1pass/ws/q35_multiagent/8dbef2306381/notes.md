
## ideation
The problem asks for reachability from square 1 to $N$ with step sizes in $[A, B]$, avoiding bad intervals.
Key observations:
1.  $N$ is very large ($10^{12}$), so we cannot simulate square by square.
2.  $M$ is moderate ($2 \times 10^4$), and $B$ is small ($\le 20$).
3.  Bad intervals are disjoint and sorted.
4.  If any bad interval has length $\ge B$, it acts as an impenetrable wall (cannot jump over), so output No.
5.  We can maintain the set of reachable squares as a collection of disjoint intervals.
6.  Since $B$ is small, the number of intervals likely remains small, or we can process them efficiently.
7.  We can fast-forward the expansion of intervals when there are no bad squares ahead, using arithmetic progression logic.
8.  After processing all bad intervals, we check if $N$ is reachable from the remaining intervals.

Algorithm:
1.  Read input. Check if any bad interval length $\ge B$. If so, print No.
2.  Initialize reachable intervals $R = [(1, 1)]$.
3.  Iterate through each bad interval $[L, R_{bad}]$:
    a.  For each interval $[u, v]$ in $R$:
        i.  If $v < L$, fast-forward the interval to reach at least $L$. This involves calculating the number of steps $k$ needed such that the right endpoint $v$ reaches $L$. Update $u, v$.
        ii. Clip the interval against $[L, R_{bad}]$. Remove any part overlapping with the bad interval.
    b.  Filter out intervals that are completely to the left of $R_{bad}$ (since they cannot reach $N$ which is to the right). Specifically, keep intervals with $u > R_{bad}$.
    c.  Merge overlapping or adjacent intervals in $R$.
4.  After processing all bad intervals, check if $N$ is reachable from any interval in $R$.
    a.  If an interval $[u, v]$ covers $N$ (i.e., $u \le N \le v$), then Yes.
    b.  If $v < N$, simulate expansion or check modulo arithmetic (if $A=B$) to see if $N$ can be reached. Since $B$ is small, simulation is fast (at most $A$ steps to grow interval length to $A$, after which everything to the right is reachable).

## worker: (none)
The algorithm maintains a set of reachable intervals. For each bad interval, it expands the reachable intervals and clips them against the bad interval. Fast-forwarding is used to efficiently handle large gaps between bad intervals. The key insight is that once an interval has length $\ge B$, it becomes "solid" and can reach any square to its right. The simulation step handles the case where intervals are not yet solid, but since $B$ is small, this simulation is fast.
