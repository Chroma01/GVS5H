To solve this problem, we need to determine the minimum weight path between two vertices in a graph where edges exist between intervals that do not intersect. The key insight is that the graph's connectivity can be analyzed by considering the complement: two intervals are connected if they are disjoint. This suggests that intervals which "overlap" form a cluster that is disconnected from other clusters if there's no disjoint interval bridging them.

However, a more direct approach leverages the structure of the intervals. Two intervals $[L_i, R_i]$ and $[L_j, R_j]$ are connected if $\max(L_i, L_j) > \min(R_i, R_j)$. This condition is equivalent to saying one interval is completely to the left of the other.

The graph can be decomposed into connected components. Within a connected component, the minimum weight path between any two nodes $s$ and $t$ will likely involve going through a "hub" node with a small weight. Specifically, if the graph is connected, the shortest path between $s$ and $t$ is often $\min(W_s + W_t + W_k)$ for some intermediate node $k$, or just $W_s + W_t$ if they are directly connected.

Actually, a stronger property holds: if the graph is connected, the minimum weight path between any two nodes $u$ and $v$ is $\min(W_u + W_v + \min_{k \neq u,v} W_k, \text{direct edge weight if exists})$. But checking all pairs is too slow.

Let's refine the component analysis. The intervals can be sorted. The connectivity of interval graphs (or their complements) can be determined by sweeping. The complement of an interval graph is a comparability graph? No.

Let's look at the structure again. Edges exist for disjoint intervals. This is the "disjointness graph".
Two intervals are disjoint if one is strictly to the left of the other.
This implies that if we have a set of intervals that all pairwise intersect, they form an independent set in G.
If we have a set of intervals that are pairwise disjoint, they form a clique in G.

The connected components of G can be found by considering the "overlap graph" of the intervals. If the overlap graph is connected, does that mean G is disconnected? Not necessarily.
Actually, it is known that the complement of an interval graph is a comparability graph? No.

Let's use the following property:
The graph G is connected if and only if the union of all intervals is not "broken" in a way that separates left from right?
Actually, we can find connected components of G efficiently.
Consider the intervals sorted by $L_i$.
Two intervals $i$ and $j$ are connected if $R_i < L_j$ or $R_j < L_i$.

We can compute connected components of G using a sweep-line algorithm or by building the complement graph's components? The complement graph has edges for intersecting intervals. The complement of G is the intersection graph of intervals, which is an interval graph. Interval graphs are chordal and their connected components can be found easily.
Let $G'$ be the intersection graph. The connected components of $G'$ correspond to clusters of mutually overlapping intervals.
If $G'$ has multiple connected components, say $C_1, C_2, \dots, C_k$, then there are no edges between any interval in $C_a$ and any interval in $C_b$ in $G'$, which means ALL pairs between $C_a$ and $C_b$ are edges in $G$. Thus, if $G'$ has $k$ connected components, $G$ consists of a complete $k$-partite graph (with parts $C_1, \dots, C_k$).
If $G'$ is connected, then $G$ might still be disconnected? No. If $G'$ is connected, it means the intervals form a single "cluster" of overlaps. In this case, $G$ is connected if and only if there exist at least two disjoint intervals?
Actually, if $G'$ is connected, $G$ is connected unless all intervals intersect at a common point? No.
If $G'$ is connected, then for any two intervals $u, v$, there is a chain of overlapping intervals. This doesn't directly imply connectivity in $G$.
However, if $G'$ has multiple connected components, then $G$ is a complete multipartite graph. The distance between any $u \in C_a$ and $v \in C_b$ ($a \neq b$) is 1. The distance between $u, v \in C_a$ is 2 (via any node in $C_b$) if $N \ge 2$ components.
So, if $G'$ has $\ge 2$ components, the answer for $u, v$ is:
- If $u, v$ in different components: $W_u + W_v$.
- If $u, v$ in same component: $W_u + W_v + \min_{k \notin C_u} W_k$.

If $G'$ is connected (1 component), then $G$ might be disconnected.
When is $G$ disconnected when $G'$ is connected?
$G$ is disconnected if the intervals can be partitioned into two sets $A, B$ such that no interval in $A$ is disjoint from any in $B$. This means every interval in $A$ intersects every interval in $B$. This implies that the union of intervals in $A$ and $B$ all share a common point? Not necessarily a single point, but they are "interleaved" such that no separation exists.
Actually, if $G'$ is connected, $G$ is connected if and only if there exist two disjoint intervals. If all intervals pairwise intersect, then $G$ has no edges, so it's disconnected (unless $N=1$).
If there is at least one pair of disjoint intervals, then $G$ is connected?
Yes, it is a known result that the complement of a connected interval graph is connected unless the interval graph is a complete graph (all pairwise intersect).
So:
1. Find connected components of the intersection graph $G'$.
2. If there are $>1$ components, $G$ is complete multipartite.
3. If there is 1 component:
   - If all intervals pairwise intersect (i.e., $G'$ is a complete graph), then $G$ has no edges. Output -1 for all pairs.
   - Otherwise, $G$ is connected. The shortest path between $u$ and $v$ is:
     - 1 if they are disjoint (edge exists).
     - 2 if they are not disjoint, via an intermediate node $k$ that is disjoint from both. We want to minimize $W_u + W_v + W_k$. So we need the minimum weight node $k$ that is disjoint from both $u$ and $v$.

To implement this:
1. Build the intersection graph components. This can be done by sorting intervals and sweeping.
2. Identify the global minimum weight node $W_{min}$ and its index.
3. For the case of multiple components in $G'$, the logic is straightforward.
4. For the single component case:
   - Check if $G'$ is complete. If so, output -1.
   - Else, for each query $(u, v)$:
     - If $u, v$ disjoint, ans = $W_u + W_v$.
     - Else, find min $W_k$ such that $k$ is disjoint from $u$ and $v$.
       - Note: $k$ must be disjoint from $[L_u, R_u]$ and $[L_v, R_v]$.
       - This means $k$ must be to the left of $\min(L_u, L_v)$ or to the right of $\max(R_u, R_v)$.
       - We can precompute the minimum weight interval ending before $X$ and starting after $Y$.

Let's refine the "single component, not complete" case.
We need $\min \{ W_k \mid [L_k, R_k] \cap [L_u, R_u] = \emptyset \text{ and } [L_k, R_k] \cap [L_v, R_v] = \emptyset \}$.
The condition is equivalent to:
$R_k < \min(L_u, L_v)$ OR $L_k > \max(R_u, R_v)$.
So we need $\min( \min \{ W_k \mid R_k < \min(L_u, L_v) \}, \min \{ W_k \mid L_k > \max(R_u, R_v) \} )$.
We can precompute:
- `min_W_left[x]`: minimum weight of an interval with $R_k < x$.
- `min_W_right[x]`: minimum weight of an interval with $L_k > x$.

Steps:
1. Read input.
2. Determine connected components of the intersection graph $G'$.
   - Sort intervals by $L_i$.
   - Use a sweep-line to find components. Two intervals are in the same component if they overlap or are connected via a chain of overlaps.
   - Actually, finding components of an interval graph is easy: sort by $L$, keep track of the maximum $R$ seen so far in the current component. If the next interval's $L$ is greater than the current max $R$, it starts a new component.
3. If number of components $> 1$:
   - For each query $(u, v)$:
     - If $comp[u] \neq comp[v]$, ans = $W_u + W_v$.
     - If $comp[u] == comp[v]$, ans = $W_u + W_v + \min_{k \notin comp[u]} W_k$.
4. If number of components == 1:
   - Check if $G'$ is complete. This is true if for all $i, j$, $[L_i, R_i]$ intersects $[L_j, R_j]$. This is equivalent to $\max(L_i) \le \min(R_i)$? No. It's equivalent to the intersection of all intervals is non-empty? No, pairwise intersection doesn't imply common intersection for general graphs, but for interval graphs, Helly's property says yes! So if $G'$ is connected and pairwise intersecting, then there is a common point.
   - So, check if $\max(L_i) \le \min(R_i)$. If yes, all pairwise intersect. Output -1.
   - Else, $G$ is connected.
   - Precompute `min_W_left` and `min_W_right` arrays.
     - Coordinate range is up to $2N$.
     - `min_W_left[x]` = min $W_k$ for all $k$ with $R_k < x$.
     - `min_W_right[x]` = min $W_k$ for all $k$ with $L_k > x$.
   - For each query $(u, v)$:
     - If disjoint ($R_u < L_v$ or $R_v < L_u$), ans = $W_u + W_v$.
     - Else, let $L_{min} = \min(L_u, L_v)$, $R_{max} = \max(R_u, R_v)$.
     - Ans = $W_u + W_v + \min(\text{min\_W\_left}[L_{min}], \text{min\_W\_right}[R_{max}])$.

Note: In the multi-component case, if $u, v$ are in the same component, we need the min weight of a node NOT in that component. We can precompute the global min weight, and if the global min is in the same component, we need the second min weight that is outside. Or simply, for each component, store the min weight outside.

Let's write the code.

```python
import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    N = int(next(iterator))
    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = int(next(iterator))
        
    L = [0] * (N + 1)
    R = [0] * (N + 1)
    for i in range(1, N + 1):
        L[i] = int(next(iterator))
        R[i] = int(next(iterator))
        
    Q = int(next(iterator))
    queries = []
    for _ in range(Q):
        s = int(next(iterator))
        t = int(next(iterator))
        queries.append((s, t))
        
    # Step 1: Find connected components of the intersection graph G'
    # Sort intervals by L, but keep track of original indices
    intervals = []
    for i in range(1, N + 1):
        intervals.append((L[i], R[i], i))
    
    intervals.sort(key=lambda x: x[0])
    
    comp = [0] * (N + 1)
    comp_id = 0
    current_max_r = -1
    
    # To handle components correctly:
    # Iterate through sorted intervals.
    # A new component starts if the current interval's L > current_max_r of the previous component.
    # But we need to update current_max_r as we go within a component.
    
    # Actually, standard algorithm for interval graph components:
    # Sort by L.
    # Maintain the max R of the current component.
    # If the next interval's L > max R of current component, it starts a new component.
    # Otherwise, it belongs to the current component, and we update max R.
    
    # However, we must process all intervals.
    
    comp_id = 1
    current_max_r = -1
    # We need to assign components.
    # Let's create a list of (L, R, original_index)
    
    # Re-sort just to be sure
    sorted_intervals = sorted([(L[i], R[i], i) for i in range(1, N+1)], key=lambda x: x[0])
    
    comp_id = 1
    current_max_r = sorted_intervals[0][1]
    comp[sorted_intervals[0][2]] = comp_id
    
    for i in range(1, N):
        l, r, idx = sorted_intervals[i]
        if l > current_max_r:
            comp_id += 1
            current_max_r = r
        else:
            current_max_r = max(current_max_r, r)
        comp[idx] = comp_id
        
    num_components = comp_id
    
    # Precompute min weight outside each component
    # If num_components > 1, we need min weight for each component's "outside"
    
    # Global min weight and its component
    global_min_w = float('inf')
    global_min_idx = -1
    for i in range(1, N+1):
        if W[i] < global_min_w:
            global_min_w = W[i]
            global_min_idx = i
            
    # For each component, find the minimum weight node NOT in that component
    # We can compute this by:
    # 1. Find the global min. If it's not in comp C, then min_out[C] = global_min_w.
    # 2. If it is in comp C, then min_out[C] = min weight in other components.
    
    # Let's find the two smallest weights globally and their components
    min1_w = float('inf')
    min1_comp = -1
    min2_w = float('inf')
    min2_comp = -1
    
    for i in range(1, N+1):
        w = W[i]
        c = comp[i]
        if w < min1_w:
            min2_w = min1_w
            min2_comp = min1_comp
            min1_w = w
            min1_comp = c
        elif w < min2_w:
            min2_w = w
            min2_comp = c
            
    min_out = [0] * (num_components + 1)
    for c in range(1, num_components + 1):
        if min1_comp != c:
            min_out[c] = min1_w
        else:
            min_out[c] = min2_w
            
    results = []
    
    if num_components > 1:
        for s, t in queries:
            if comp[s] != comp[t]:
                results.append(str(W[s] + W[t]))
            else:
                # Same component, need to go through a node in another component
                # Path: s -> k -> t, weight W[s] + W[k] + W[t]
                # Minimize W[k] for k not in comp[s]
                results.append(str(W[s] + W[t] + min_out[comp[s]]))
                
    else:
        # Single component
        # Check if all intervals pairwise intersect
        # By Helly's property for intervals, this is true iff intersection of all is non-empty
        # i.e., max(L) <= min(R)
        
        max_L = max(L[1:])
        min_R = min(R[1:])
        
        if max_L <= min_R:
            # All pairwise intersect, G has no edges
            for s, t in queries:
                results.append("-1")
        else:
            # G is connected
            # Precompute min_W_left and min_W_right
            # Coordinates up to 2N
            max_coord = 2 * N + 1
            min_W_left = [float('inf')] * (max_coord + 2)
            min_W_right = [float('inf')] * (max_coord + 2)
            
            # min_W_left[x] = min W[k] such that R[k] < x
            # min_W_right[x] = min W[k] such that L[k] > x
            
            # Initialize min_W_left
            # We can iterate x from 1 to max_coord
            # But easier: collect all (R[k], W[k]) and (L[k], W[k])
            
            # For min_W_left:
            # Sort intervals by R
            # Then for a given x, we want min W for R < x.
            # We can precompute prefix min on sorted R.
            
            # Let's create an array for min_W_left
            # min_W_left[x] should be min W[k] for all k with R[k] < x.
            # We can compute this by iterating x from 1 to max_coord.
            # Maintain a min heap or just a running min?
            # Since we want min W for R < x, we can add intervals with R = x-1 to a pool.
            
            # Actually, simpler:
            # Create an array 'min_w_for_r' where min_w_for_r[r] = min W[k] with R[k] == r.
            # Then min_W_left[x] = min(min_w_for_r[1], ..., min_w_for_r[x-1])
            
            min_w_for_r = [float('inf')] * (max_coord + 1)
            for i in range(1, N+1):
                r = R[i]
                if W[i] < min_w_for_r[r]:
                    min_w_for_r[r] = W[i]
                    
            running_min = float('inf')
            for x in range(1, max_coord + 2):
                # min_W_left[x] is min W for R < x, i.e., R <= x-1
                if x - 1 >= 1:
                    if min_w_for_r[x-1] < running_min:
                        running_min = min_w_for_r[x-1]
                min_W_left[x] = running_min
                
            # For min_W_right:
            # min_W_right[x] = min W[k] for L[k] > x, i.e., L >= x+1
            min_w_for_l = [float('inf')] * (max_coord + 1)
            for i in range(1, N+1):
                l = L[i]
                if W[i] < min_w_for_l[l]:
                    min_w_for_l[l] = W[i]
                    
            running_min = float('inf')
            for x in range(max_coord, -1, -1):
                # min_W_right[x] is min W for L > x, i.e., L >= x+1
                if x + 1 <= max_coord:
                    if min_w_for_l[x+1] < running_min:
                        running_min = min_w_for_l[x+1]
                min_W_right[x] = running_min
                
            for s, t in queries:
                # Check if disjoint
                if R[s] < L[t] or R[t] < L[s]:
                    results.append(str(W[s] + W[t]))
                else:
                    # Not disjoint, need intermediate k
                    # k must be disjoint from both s and t
                    # L_min = min(L[s], L[t]), R_max = max(R[s], R[t])
                    L_min = min(L[s], L[t])
                    R_max = max(R[s], R[t])
                    
                    # k must have R[k] < L_min OR L[k] > R_max
                    w_left = min_W_left[L_min]
                    w_right = min_W_right[R_max]
                    
                    min_w_k = min(w_left, w_right)
                    
                    if min_w_k == float('inf'):
                        # Should not happen if G is connected and not complete
                        results.append("-1")
                    else:
                        results.append(str(W[s] + W[t] + min_w_k))
                        
    print('\n'.join(results))

solve()
```