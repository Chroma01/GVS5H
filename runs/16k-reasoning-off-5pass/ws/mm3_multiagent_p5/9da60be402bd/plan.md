We need shortest length of a (possibly non-simple) directed walk from i to j whose edge-label string is a palindrome. Paths may repeat vertices, and length 0 (empty string) is allowed when i=j.

Key observation: If we reverse the entire graph and treat the labels as read backwards, a palindrome walk from i to j corresponds to two walks that meet in the middle. More concretely, a palindrome of length L has a center: either a single edge (odd L) or a vertex (even L). For an odd-length palindrome walk i → v → j, the first half and reversed second half must match: there is a walk from i to v and a walk from j to v (in the reversed graph) that produce the same label string.

We can think of this as a meet-in-the-middle on label strings. Since N ≤ 100, alphabet size ≤ 26, we can build, for each vertex pair (a,b), a map from label string to shortest walk length, but strings can be arbitrarily long → too large.

Better: BFS over pairs of vertices (a,b) tracking the difference in label sequences. This is similar to the "shortest palindrome path" classic problem. State: (u, v) meaning we are building a walk from i to u (forward) and a walk from j to v (in reversed graph). At each step we extend by one edge on both sides with the same label. When the two sides meet (i.e., u == v after one more step, for odd length, or directly equal, for even length), we obtain a palindrome path.

Algorithm per source i and target j (run separately for each i,j, or run a BFS per (i,j) pair):
- Preprocess reversed adjacency list: RevAdj[v] = list of (u, label) such that C_{u,v} = label.
- For each (i,j), do a BFS over state (u, v) where u is reachable from i and v is reachable from j in the reverse graph. Distance d of state (u,v) means we have built label string s of length d, with a walk of length d from i to u and a walk of length d from j to v (in reverse graph) both labeled s.
- Transitions: from state (u,v), for each label L, consider all forward edges u → u' with label L, and all reverse edges v → v' (i.e., original edges v' → v with label L). For each pair (u', v') with matching label L, push state (u', v') with distance d+1.
- Answer for (i,j):
   - If i == j: 0 is a palindrome (empty string).
   - Otherwise, the shortest palindrome has either:
        * even length: the two halves meet exactly, i.e., there exists u such that a walk of length k from i to u and a walk of length k from j to u in reverse graph exist. That corresponds to a state (u, u) reached in BFS at distance 2k? Wait, careful: In our BFS, state (u,v) at distance d means we have matched label strings of length d from i→u and j→v (reverse). For even palindrome, the two halves are exactly the same and meet at some middle vertex m: i →...→ m and j →...→ m in reverse. The total length is 2k where k = d. So we check when we first reach a state (u, u) at distance d, then total length = 2d.
        * odd length: the palindrome has a center edge e from p to q with label L. The first half goes from i to p (length k), then edge p→q, then the second half reversed goes from j to q. In our BFS framework, we need to consider transitions where we take one more edge on only one side? Let's think: State (u,v) after d steps has label string s. The current walk is i →...→ u (forward) and j →...→ v (reverse). The palindrome we are building is s concatenated with the reverse of s, possibly with a center edge. If we stop here (i.e., s is the first half, and reverse(s) is the second half), then we need u == v to merge? Actually, if we have i →...→ u and j →...→ u in reverse (meaning j →...→ u in original?), let's re-derive.

Standard known solution: For each pair (i,j), run a BFS on the product graph of the original and reversed graph, matching edges with the same label. Distance d to state (u,v) corresponds to the length of the first half. The total palindrome length is:
- 2d if u == v (even length palindrome meeting at vertex u).
- 2d+1 if there exists an edge u → v with some label L (odd length palindrome with center edge u→v). But careful: In the BFS state (u,v), we have consumed d labels on each side. The remaining unmatched center is an edge from u to v. If such an edge exists, total length = 2d+1.

Thus, the BFS explores states (u,v). The distance is the length of the matched prefix. Start state: (i, j) with distance 0. But wait: We need to handle the case i==j: answer 0. For i != j, we BFS.

Transitions: From state (u, v) at distance d, for each label L, we can take a forward edge u → u' labeled L, and a reverse edge v → v' labeled L. (Reverse edge v → v' means original edge v' → v with label L.) Then new state (u', v') at distance d+1.

When we visit a state (u, v):
- If u == v, we can form an even-length palindrome of length 2d.
- If there is an edge from u to v (in the original graph) with any label, we can form an odd-length palindrome of length 2d+1.

The BFS continues. We need the minimum over all reachable states. Since edge labels are from 'a' to 'z', we can group outgoing edges by label for efficiency.

But N=100, BFS per (i,j) would be O(N^2 * (N^2 + E)) which might be too high if we do it naively. Number of states is N^2 = 10000. BFS per pair is 10000 states. There are N^2 = 10000 pairs. So total states explored could be 10^8, which might be borderline but likely okay in Python with careful optimization? 10^8 is too high (10 seconds+). We need to optimize.

Alternative: Run BFS for all (i,j) simultaneously? Not obvious.

Better: Since N=100, we can run BFS for each i (source) and compute answers to all j. We fix i, and for each j we want the answer. Can we reuse computations? Possibly, but maybe per (i,j) BFS is acceptable with pruning? Let's estimate: For each i, we could do a BFS from i in the product graph? Not exactly.

Actually, the state is (u, v) where u is from i's forward reachable and v is from any j's reverse reachable. If we fix i, the BFS over (u, v) where u is reachable from i and v is any vertex. That's N^2 states. For each i, one BFS over the product graph of size N^2. That's N BFS, each O(N^2 + something). Total O(N^3) ≈ 10^6, which is fine! Wait, is that correct?

Let's see: For a fixed i, we want to compute for all j the answer. The BFS state (u, v) means we have matched a string s of length d, with a walk from i to u, and a walk from j to v in the reverse graph? No, the second component v depends on j. If we want to compute for all j simultaneously, the state would need to remember j. That's not fixed.

Alternative: For each i, we can run a multi-source BFS? No, j varies.

Let's reconsider: The BFS per (i,j) explores the product graph of the forward graph from i and the reverse graph from j. The number of states is N^2. If we do this for all N^2 pairs, we have N^4 = 10^8 states. That's a lot but maybe with optimization (like early termination, using deque) it could pass? 10^8 operations in Python is about 10-20 seconds, likely too slow.

We need a smarter approach.

Observation: The BFS for (i,j) only cares about the forward reachable set from i and reverse reachable set from j. We can precompute all-pairs shortest paths? Not directly.

Another approach: Since N=100, we can run a BFS for each i on the product graph where the "state" is (u, v) but the second component is not a fixed j; rather, we want to know for which j this state is useful. Actually, the transition only requires matching labels. The BFS from (i, j) is essentially finding the shortest path in the product graph from (i, j) to any state (u, u) or (u, v) with edge u→v. This is like a standard BFS on the product graph. But the product graph has N^2 vertices and edges determined by matching labels. If we do a BFS from all (i, j) simultaneously? That would be a BFS on a graph of size N^3? No.

Wait, maybe we can do a BFS on the graph where vertices are (i, j) and edges are formed by? Not exactly.

Let's think about the structure: For each i, we can compute the BFS on the product graph starting from all (i, j) for all j? That would be a multi-source BFS on the product graph? The product graph vertices are (u, v). The sources would be (i, 1), (i, 2), ..., (i, N). Then for each target (u, v) that is a "meeting" state (u=u or edge u→v), we can update answers for all j that correspond to the v? This seems messy.

Actually, the answer for (i, j) is the shortest distance in the product graph from (i, j) to the set of "accepting" states S = { (u, u) } ∪ { (u, v) | edge u→v exists }. This is exactly the shortest path from a single source (i, j) in an unweighted graph (the product graph). The product graph has N^2 vertices. So for each (i, j) we need a single-source shortest path. Doing this N^2 times is N^4.

But maybe we can compute all-pairs shortest paths on the product graph? The product graph has N^2 vertices, so all-pairs BFS would be N^2 * (N^2 + edges) = N^4, same.

Is there a way to reduce? Note that the product graph edges are only between states where the forward edge from u and the reverse edge from v have the same label. This is a kind of "synchronized" BFS.

We can run a BFS for each i, but with a twist: For fixed i, we want distances from (i, j) for all j. That is a multi-source BFS on the product graph where the sources are all (i, j) for j=1..N. However, the BFS explores (u, v) states. When we reach a state (u, v), the distance from source (i, j) is not the same for all j because the second component v is tied to j. Wait, the BFS from (i, j) explores states (u, v) where the second component v is reached from j via the reverse graph. If we start from all (i, j) simultaneously, we are effectively doing a BFS on the product graph where the first component is fixed at i, and the second component starts at all vertices. But the BFS transition from (i, v) to (u, v') requires a forward edge from i to u and a reverse edge from v to v' with same label. The first component i is fixed only at the start; as we explore, the first component moves away from i. So the BFS tree is rooted at the set of sources (i, *). The distance from source (i, j) to a state (u, v) is the BFS distance in this multi-source BFS only if the path from (i, j) to (u, v) does not mix different j's. But BFS from multiple sources on an unweighted graph computes, for each vertex, the distance to the nearest source. That doesn't give us per-j distances.

So multi-source BFS doesn't help for per-j answers.

We need a faster method. Let's think about the constraints: N ≤ 100. N^2 = 10000. If we do BFS per (i,j) with early termination, maybe it's okay? Let's estimate time: For each (i,j), BFS on a graph of 10000 vertices. Each state expansion: we need to consider matching labels. We can precompute for each vertex u, a dict mapping label to list of outgoing edges. Similarly for reverse. Then for a state (u, v), the number of outgoing edges is sum over labels of (out_deg_label(u) * rev_in_deg_label(v)). This could be large in the worst case (complete graph, out_deg up to 100, in_deg up to 100, 26 labels, so up to 100*100 = 10000 per state). That's too much.

But maybe we can optimize by precomputing, for each pair (u, v), the set of labels that appear on both outgoing from u and incoming to v in reverse (i.e., outgoing from v in original). Let's define: For each (u, v), we want to know which labels L have at least one edge u→u' labeled L and at least one edge v'→v labeled L. If there are multiple edges with the same label, we still just need to know that L is available. When we expand state (u, v), we go to (u', v') for all u' adjacent to u with label L and v' adjacent to v with label L (in reverse). The number of resulting (u', v') states is the product of the sizes of these adjacency lists. To minimize, we can iterate over the label that has smaller degree.

But still, worst-case expansion could be large.

Alternative perspective: The problem is equivalent to finding the shortest palindrome path. This is a known problem. There is a solution using BFS on the product graph, but with N=100, N^2=10000, and for each pair we do a BFS, that's 10^8 BFS steps. If each step is O(1) on average, it might be okay. But 10^8 in Python is tight (maybe 2-3 seconds if very optimized, but likely 5-10). We need to be careful.

Maybe we can use bitsets or something? Not sure.

Let's look for a better algorithm. Since the graph is directed and N is small, we can use Floyd-Warshall-like dynamic programming? No, because paths can be arbitrarily long (non-simple), so we can't bound the length. The BFS is necessary because we are looking for shortest walks in an unweighted graph (the product graph). The product graph has N^2 vertices. The BFS from (i, j) will visit at most N^2 states. So for each (i,j), BFS visits at most 10000 states. There are 10000 pairs, so 10^8 state visits. Each state visit involves looking at outgoing edges. If we can make the expansion of a state O(1) or O(deg), maybe it's okay.

But we can also observe that for many (i,j), the BFS will terminate early because the graph is sparse? Not necessarily; worst-case dense graph has many edges. But N=100, so max edges is 10000 (if all C_{i,j} are letters, but letters are 26, so max edges is 2600). Actually, since each C_{i,j} is a single character, there is at most one edge from i to j. So total edges E ≤ N^2 = 10000. So the graph is at most dense. The product graph edges: For each label L, and for each edge u→u' labeled L, and each edge v'→v labeled L, we have an edge from (u, v) to (u', v'). The number of such edges is sum_{L} (out_L * in_L), where out_L is the number of edges with label L, and in_L is the number of edges with label L (in the original graph, which is the same as reverse). Since each label L has at most N edges (actually at most N^2, but at most one per (i,j) so at most N per label? No, for a fixed label, there can be multiple edges from different sources, so out_L is the number of edges labeled L. Total edges is ≤ 10000, distributed over 26 labels. So on average, out_L ≈ 400. The product edges per label could be out_L * out_L (since in_L = out_L for reverse). So total product edges could be sum out_L^2. By Cauchy, sum out_L^2 ≥ (sum out_L)^2 / 26 = E^2/26. For E=2600, E^2/26 ≈ 260,000. So product graph edges around 260k. That's small! The product graph has at most 260k edges. Wait, is that correct? Let's check: For each label L, we have a set of edges E_L. The product graph edges for label L are all pairs ( (u, v), (u', v') ) such that u→u' ∈ E_L and v'→v ∈ E_L (i.e., v→v' in reverse). That's exactly the Cartesian product of E_L with itself. The number of such pairs is |E_L|^2. So total product edges = sum_{L} |E_L|^2. This can be up to 26 * (10000/26)^2 = 10000^2 / 26 ≈ 3.8 million. That's still okay.

But when we do BFS from (i, j), we only traverse edges that are reachable. However, the BFS still needs to consider outgoing edges from each state. If we can precompute the adjacency list for the product graph (i.e., for each state (u, v), a list of (u', v') with the label condition), we can do a standard BFS. The product graph has at most ~3.8 million edges, which is a bit high to store explicitly as a list for all 10000 states (average 380 edges per state). Actually, storing all product edges might be memory intensive: 3.8M edges, each as a pair of ints, maybe 16 bytes = 60MB. That's borderline but possible in Python? 3.8M * (2*2 + overhead) might be 100MB+. Could be tight.

But we don't need to store the full product graph. We can compute outgoing edges on the fly. For a state (u, v), we need to find all (u', v') such that there is a label L with u→u' labeled L and v→v' labeled L (in reverse, meaning v'→v labeled L in original). We can do this by iterating over labels L that appear in the outgoing edges of u, and for each such L, iterating over outgoing edges of v with label L (in reverse). To speed up, we can precompute for each vertex, a list of outgoing edges by label: out[u][L] = list of v such that u→v labeled L. Also, for reverse: rev_in[v][L] = list of u such that u→v labeled L (i.e., incoming to v). Then for state (u, v), the expansion is: for each label L in intersection of out[u] labels and rev_in[v] labels, for each u' in out[u][L] and each v' in rev_in[v][L], add (u', v').

The number of such pairs is the product of the sizes. The sum over all states of the product sizes is exactly the number of product edges, which we estimated up to 3.8M. So total work over all BFS visits could be up to 3.8M * (number of BFS runs that visit those states). But in the worst case, if we do BFS for all (i,j), we might traverse the entire product graph many times. Actually, each BFS from (i,j) explores a subset of the product graph. The union of all BFS explorations could be the entire product graph, but each edge might be traversed multiple times across different BFS runs. In the worst case, we might traverse each edge up to N^2 times, leading to 3.8M * 10000 = 3.8e10, impossible.

So we need to be smarter. We need to compute distances in the product graph from all sources (i, j) efficiently. That is, we want all-pairs shortest paths in the product graph. The product graph has N^2 vertices. We can run BFS from every vertex in the product graph. There are N^2 sources. BFS from each source visits all reachable vertices. In the worst case, the product graph is connected, so each BFS visits all 10000 vertices. That's 10000 * 10000 = 10^8 vertex visits. For each vertex visit, we expand its outgoing edges. The total work is the sum over all BFS of the sum of out-degrees of visited vertices. If the product graph is dense, out-degree could be up to 10000. So worst-case 10^8 * 10000 = 10^12, no.

But we can use the fact that the product graph is unweighted and we want all-pairs shortest paths. We can run BFS from each vertex, but we can also use the fact that the graph is a product of two graphs with a label matching condition. Maybe we can use a different approach.

Wait, maybe the constraints are such that a BFS per (i,j) is acceptable because N=100, and typical graphs are sparse. But we must guarantee it passes worst-case. Let's think about the worst-case input. The worst-case for edges is when every C_{i,j} is a letter. There are 26 letters, so we can assign letters to maximize the product edges. To maximize sum |E_L|^2, we should distribute edges as evenly as possible among the 26 labels. With N=100, the maximum number of edges is 10000. If we put 385 edges per label (10000/26 ≈ 384.6). Then sum |E_L|^2 ≈ 26 * 385^2 ≈ 3.85 million. So the product graph has about 3.85 million edges. The product graph has 10000 vertices. Average out-degree is 385. So BFS from a single source visits at most 10000 vertices, and processes at most 3.85M edges in total if the BFS visits all vertices? No, BFS from a single source visits each vertex once, and processes all outgoing edges of that vertex. So total edges processed in one BFS is the sum of out-degrees of all vertices in the product graph, which is exactly the number of edges in the product graph, ~3.85M. If we do this for all 10000 sources, total edges processed is 3.85M * 10000 = 38.5 billion. That's way too much.

But wait, do we need to process all edges for each BFS? We can early-terminate the BFS when we have found the answer for that (i,j). However, the BFS explores level by level. The distance in the product graph from (i,j) to an accepting state (u,u) or (u,v with edge) could be up to 2N? Actually, the BFS distance corresponds to half the palindrome length. The maximum palindrome length is not bounded a priori because paths can be non-simple. However, since the product graph has 10000 vertices, the shortest path in an unweighted graph cannot exceed 10000-1 edges. So BFS depth is at most 9999. But in practice, it's much smaller? Not necessarily; there could be a long simple path in the product graph. But the product graph is directed? Wait, the product graph edges: from (u,v) to (u',v') requires a forward edge u→u' and a reverse edge v'→v (i.e., original edge v'→v). This is not symmetric. The product graph is directed. So BFS from (i,j) explores forward in the product graph. The accepting states are specific. The BFS might need to explore a large portion of the product graph.

But is the product graph strongly connected? Not necessarily. The out-degree can be up to 385, but in-degree also similar. The diameter could be up to 10000.

So per (i,j) BFS might process a large number of edges. With 10000 BFS, it's too slow.

We need a different algorithm. Let's think about the nature of the problem. The palindrome path length is the shortest walk such that the label string is a palindrome. This is similar to the "shortest palindrome" problem in a graph. There is a known solution using BFS on the product graph, but with the observation that we only need to consider states (u, v) where the shortest path from i to u and from j to v (in reverse) are known? No.

Another approach: Since the labels are only 26, we can use a meet-in-the-middle with bitsets? Not sure.

Wait, maybe we can use the fact that the palindrome condition means that the walk from i to j is symmetric around its center. We can think of it as two walks: one from i to the center, and one from j to the center, that are reverses of each other. This is exactly the BFS on the product graph. But we can compute the BFS from all vertices in the original graph simultaneously? For example, we can run a BFS on the graph where states are (u, v) and we want to know the distance to the nearest accepting state. But we need distances from all (i, j) to that set. That's the reverse: we want distances from sources to a target set. We can do a multi-source BFS from the accepting states backward in the product graph! That would give us, for every state (i, j), the shortest distance to any accepting state. Since the product graph is directed, we can reverse it and do BFS from the accepting states. The number of accepting states: (u, u) for all u, and (u, v) for all edges u→v. There are at most N + E such states. So the set of accepting states is at most about 10000. Doing a multi-source BFS on the reverse product graph from these accepting states would compute the shortest distance from every (i, j) to the nearest accepting state. That's exactly what we want! The distance from (i, j) to an accepting state in the product graph is the same as the distance from the accepting state to (i, j) in the reverse product graph.

So the algorithm:
1. Build the product graph: vertices are pairs (u, v) for u,v in 1..N.
2. Build the reverse product graph: edges reversed. That is, for each edge (u,v) -> (u',v') in the product graph (meaning there is label L with u→u' and v'→v in original), we add an edge from (u',v') to (u,v) in the reverse product graph.
3. The accepting states are S = { (u, u) | u=1..N } ∪ { (u, v) | there is an edge u→v in original }.
4. Run a multi-source BFS on the reverse product graph starting from all states in S, with distance 0 for all? Wait, we need to be careful: The BFS distance from an accepting state to (i, j) in the reverse product graph gives the shortest path length from (i, j) to an accepting state in the original product graph. But the accepting states have different "base lengths": 
   - For (u, u), the palindrome length is 2 * d, where d is the distance in the original product graph from (i, j) to (u, u). In the reverse BFS, if we start from (u, u) with distance 0, then the BFS distance to (i, j) is d. So the palindrome length for (i, j) via this accepting state is 2 * d.
   - For (u, v) with edge u→v, the palindrome length is 2 * d + 1, where d is the distance from (i, j) to (u, v) in the original product graph. In the reverse BFS, if we start from (u, v) with distance 0, then the BFS distance to (i, j) is d. So the palindrome length is 2 * d + 1.
5. So we need to run a multi-source BFS where different sources have different "initial" values for the palindrome length. We can handle this by initializing the distance array for the BFS on the product graph states with infinity, and then for each accepting state, we set its distance to 0, but we need to track whether the answer is even or odd. Alternatively, we can compute the shortest distance in the product graph (in terms of number of edges) from each (i, j) to the set S, but with two different cost functions: one for even, one for odd. Actually, we can do two BFS: one from the even accepting states (u,u) and one from the odd accepting states (u,v) with edge. But the odd accepting states require a specific transition: the edge u→v must be the center. Wait, the odd accepting state (u, v) is not just any state with an edge; it's a state (u, v) such that there is an edge from u to v. In the BFS on the product graph, we can check when we are at state (u, v) if there is an edge u→v; if so, we can form an odd palindrome. So the set of states from which an odd palindrome can be formed is exactly the set of (u, v) with an edge. So we can treat these as "target" states with a cost of 1 (for the center edge) in addition to the BFS distance.

So the BFS on the product graph from a source (i, j) to the set S is what we need. The multi-source BFS from S on the reverse product graph will give us the shortest distance d from each (i, j) to S. But we need to know if the shortest path ends at an even or odd accepting state to compute the final answer. We can do the following: Run a BFS on the product graph (not reverse) from all sources (i, j)? No, that's what we want to avoid.

Instead, we can run a BFS on the reverse product graph starting from all accepting states, but we need to track the "parity" of the accepting state. Actually, the distance in the product graph from (i, j) to an accepting state s is the same as the distance from s to (i, j) in the reverse product graph. So we can run a BFS on the reverse product graph from all accepting states, and for each state (i, j) we record the distance d to the nearest accepting state and whether that accepting state was even or odd. Then the answer for (i, j) is:
- If the nearest accepting state is even (i.e., (u, u)), then answer = 2 * d.
- If the nearest accepting state is odd (i.e., (u, v) with edge), then answer = 2 * d + 1.
- However, we also have the case i == j, where the empty string (length 0) is a palindrome. In our framework, (i, i) is an even accepting state, and the distance from (i, i) to itself is 0, so answer = 0. That works.

But wait: The BFS distance d is the number of edges in the product graph from the accepting state to (i, j) in the reverse graph. That equals the number of edges in the product graph from (i, j) to the accepting state. So d is exactly the half-length. So answer = 2d or 2d+1.

So the problem reduces to: Given a directed graph (the product graph) with N^2 vertices, we want to compute, for every vertex (i, j), the shortest distance to a set of "target" vertices T, where T consists of:
- "even" targets: all (u, u) for u=1..N.
- "odd" targets: all (u, v) such that there is an edge u→v in the original graph.
We also need to know, for the shortest path, whether the target is even or odd (to compute the final length). If there are multiple shortest paths reaching different targets, we take the minimum final answer. So we need to find, for each (i, j), min( 2 * d_even, 2 * d_odd + 1 ), where d_even is the shortest distance to any (u, u), and d_odd is the shortest distance to any (u, v) with an edge.

But note: The BFS on the reverse product graph starting from all targets will naturally compute the shortest distance to the nearest target. However, the BFS doesn't distinguish between even and odd targets; it just finds the nearest target. If the nearest target is even, we get d_even. If the nearest is odd, we get d_odd. But we need the minimum of 2*d_even and 2*d_odd+1. It could be that the nearest target is odd, but there is a slightly farther even target that gives a smaller final answer (e.g., 2*3=6 vs 2*2+1=5, so odd is better; but what if 2*4=8 vs 2*3+1=7, odd is better; in general, 2d_odd+1 < 2d_even if d_odd < d_even. If d_odd >= d_even, then 2d_even <= 2d_odd+1, so even is better. Actually, if d_odd = d_even, then 2d_odd+1 = 2d_even+1 > 2d_even. So even is better when d_even <= d_odd. So the minimum is always achieved by the target type that has the smaller d, except when d_odd < d_even, odd is better by exactly 1? Wait: if d_odd = d_even - 1, then 2d_odd+1 = 2(d_even-1)+1 = 2d_even -1 < 2d_even. So odd is better. If d_odd = d_even, even is better. If d_odd = d_even - 2, 2d_odd+1 = 2d_even -3 < 2d_even. So odd is better. So the condition for odd to be better is d_odd < d_even. So we just need to find, for each (i, j), the shortest distance to any even target, and the shortest distance to any odd target. Then answer = min(2*d_even, 2*d_odd+1). If no path to either, answer is -1.

So we can run two BFS (or one BFS with two layers of targets) on the reverse product graph. But wait, the reverse product graph is huge? The product graph has N^2 = 10000 vertices. The reverse product graph also has 10000 vertices. The number of edges in the reverse product graph is the same as the product graph, up to ~3.85M. We can build the reverse product graph explicitly? 3.85M edges might be a lot to store in Python lists. Each edge as a pair of ints (2 bytes each? Python int is 28 bytes). 3.85M * 2 * 28 = 215MB, too much.

We need to avoid storing the full product graph. We can do the BFS on the reverse product graph without explicitly building it, by generating edges on the fly. But BFS on the reverse product graph means we are at a state (u, v) and we want to go to (u_prev, v_prev) such that there is a label L with u_prev → u and v → v_prev in reverse (i.e., v_prev → v in original). So from (u, v), the reverse transitions are: for each label L, consider all incoming edges to u with label L (i.e., edges x → u labeled L) and all outgoing edges from v with label L in reverse? Wait, careful.

Original product edge: (u, v) → (u', v') if there is label L with u → u' (forward) and v' → v (in original, i.e., v → v' in reverse). So in the reverse product graph, an edge from (u', v') to (u, v) exists if there is label L with u' → u (forward) and v → v' (in original? No, the condition for the edge (u,v) → (u',v') is: forward edge u→u' and reverse edge v→v' (meaning original edge v'→v). So in reverse, from (u', v') we go to (u, v) if there is label L such that u→u' (forward) and v→v' (reverse). But u→u' is an outgoing edge from u. So to go backwards from (u', v') to (u, v), we need to know: given u' and v', find all u such that there is an edge u→u' with some label L, and all v such that there is a reverse edge v'→v (i.e., original edge v→v') with the SAME label L. So we need to match labels between incoming edges to u' (in forward) and outgoing edges from v' in reverse (i.e., incoming edges to v' in original? Wait, v→v' in reverse means original edge v'→v. So v' has an incoming edge from v. So it's the set of v such that there is an edge v'→v in original. So both sides are incoming edges: to u' and to v'. So the reverse transition from (u, v) is: for each label L, for each u' such that u'→u is an edge with label L, and for each v' such that v'→v is an edge with label L, we can go to (u', v').

So in the reverse BFS, from a state (u, v), we look at incoming edges to u and incoming edges to v (in the original graph), and match by label. This is symmetric to the forward case but with incoming instead of outgoing. So the number of transitions is similar: sum over L of (in_deg_L(u) * in_deg_L(v)). The total number of reverse edges in the product graph is the same as forward, ~3.85M.

If we do a BFS on the reverse product graph starting from all target states, we will process each reverse edge at most once (when the BFS visits the source of that edge). So total time is proportional to the number of reverse edges processed. If we can process all reverse edges in a single BFS, that's about 3.85M edge traversals. That's perfectly fine! 3.85M operations in Python is very fast (under 0.1 seconds). So the plan is:

1. Build adjacency lists for the original graph: out[u] = dict of label -> list of v. Also build incoming lists: inc[u] = dict of label -> list of v (where v→u is an edge with that label).
2. We want to run a BFS on the product graph in reverse. The state is (u, v). The BFS will visit all states reachable from the target set. But wait, the BFS on the reverse product graph starting from the targets will visit exactly the states that can reach the targets in the forward product graph. But we need the distance from every state (i, j) to the targets. The BFS from targets in the reverse graph will compute the shortest distance from each state to the targets (i.e., the shortest path from the state to a target in the forward graph). So we need to start the BFS from all target states, and explore the reverse product graph. The BFS will eventually visit all states that can reach a target. What about states that cannot reach any target? Their distance will remain infinity, so answer is -1.

But wait: The BFS on the reverse product graph starting from all targets will compute the distance from each state to the nearest target. However, we need two separate distances: one to even targets and one to odd targets. We can do this by having two BFS, or one BFS with a state that includes the "type" of target? Actually, we can run a single BFS that simultaneously computes the shortest distance to an even target and the shortest distance to an odd target. How? We can initialize the BFS queue with all even targets with distance 0, and all odd targets with distance 0. But we need to distinguish the type. We can have two distance arrays: dist_even and dist_odd. Or we can do a BFS that tracks the "cost" in terms of the final palindrome length. Since the final answer is 2*d_even or 2*d_odd+1, we can define a weighted graph where each state has a base cost depending on the target. But the BFS is unweighted in terms of the number of product graph edges. We can do two separate BFS: one starting from even targets, one starting from odd targets. Each BFS computes the shortest distance in the product graph from each state to that set of targets. Since the graph is the same, we can run both BFS simultaneously? Or just run one BFS with a state that includes a bit for even/odd? No, the two BFS are independent; we can just run them sequentially. Each BFS will process all reverse edges that are reachable from the respective targets. But note: The reverse BFS from even targets might not visit all states; it only visits states that can reach an even target. Similarly for odd. But the union of visited states in both BFS will cover all states that can reach any target. However, we can just run a single BFS that computes both distances by storing in the BFS queue the state and the type? That doesn't work because the distance is the same for both types (the BFS distance in the product graph is the number of edges). The only difference is the final addition of 1. So we can run a BFS that computes, for each state (u, v), the shortest distance to ANY target. Then we can recover: if the nearest target is even, answer = 2*d; if odd, answer = 2*d+1. But as discussed earlier, the nearest target might not give the minimum final answer if the nearest is odd but there is an even target at the same distance or closer? Actually, we proved that the minimum final answer is min(2*d_even, 2*d_odd+1). This is not necessarily equal to 2*min(d_even, d_odd) or 2*min(d_even, d_odd)+1. For example, if d_even = 3 and d_odd = 3, then 2*d_even = 6, 2*d_odd+1 = 7, so answer is 6. The nearest target is at distance 3 (could be even or odd). If the BFS finds the nearest target and it's odd, we might incorrectly output 7. So we cannot just take the nearest target type; we need both d_even and d_odd.

Therefore, we need to compute d_even and d_odd separately. We can do this by running two BFS: one from even targets, one from odd targets. Each BFS is on the reverse product graph. Each BFS will process the reverse edges. The total work is twice the number of reverse edges, which is about 7.7M. That's still very fast. So we can just do two BFS.

But wait: Do we need to process all reverse edges in each BFS? The BFS only traverses edges that are on a path to a target. In the worst case, the BFS might visit all states and process all reverse edges. So total work is O(E_product) for each BFS. Since E_product is up to ~3.85M, total 7.7M, which is trivial.

Let's double-check the product graph size. The product graph has N^2 vertices. Each vertex (u, v) has outgoing edges defined by: for each label L, for each u' in out[u][L] and v' in rev_out[v][L] (where rev_out[v][L] is the set of v' such that v'→v in original, i.e., v' in inc[v][L]). So the number of edges is sum_{L} (|E_L| * |E_L|) = sum |E_L|^2. With N=100, E ≤ 10000. Max sum of squares when edges are evenly distributed: 26 * ceil(10000/26)^2 ≈ 26 * 385^2 = 3,853,850. So about 3.85 million edges. In Python, if we store the reverse product graph as a list of lists for each state, each edge is a tuple of two ints. That's memory heavy. But we don't need to store the graph. We can generate neighbors on the fly during the BFS. For BFS, we need to pop a state (u, v) from the queue, and then generate all its reverse neighbors: for each label L, for each u' in inc[u][L] and v' in inc[v][L], add (u', v'). To avoid generating the same neighbor multiple times, we use a visited array of size N x N. The BFS will visit each state at most once. For each visited state, we generate all its reverse neighbors. The total number of neighbor generations is the sum over visited states of the product of in-degrees by label. This sum is exactly the number of reverse edges in the product graph that are reachable from the targets. In the worst case, the BFS visits all states, and we generate all reverse edges, which is ~3.85M. So the total work is generating 3.85M pairs. Each pair generation involves a few operations. This is very fast.

However, we must be careful: For each state (u, v), the number of reverse neighbors is sum_L (in_deg_L(u) * in_deg_L(v)). If both in-degrees are large, this could be up to 100*100=10000 per state. With 10000 states, that's 100M generations, which might be a bit high but still okay? Wait, 3.85M is the total over the whole graph. The sum over all states of sum_L in_deg_L(u)*in_deg_L(v) is sum_L (sum_u in_deg_L(u)) * (sum_v in_deg_L(v)) = sum_L |E_L|^2. So the total number of reverse edges is exactly sum_L |E_L|^2 ≈ 3.85M. So the total number of neighbor generations across the entire BFS (over all states) is 3.85M. That's small. But wait, for a single state, the number of reverse neighbors can be large. For example, if there is a vertex u with in-degree 100 for label 'a', and a vertex v with in-degree 100 for label 'a', then that state has 10000 reverse neighbors. When we process that state, we generate 10000 neighbors. But since we only process it once, the total work is just that 10000. The sum over all states is still 3.85M. So the BFS will be fast.

So the algorithm is:
- Precompute for each vertex and each label, the list of outgoing edges and incoming edges. Since labels are 'a' to 'z', we can use arrays of size 26. But storing a list for each (vertex, label) pair. N=100, 26 labels, so 2600 lists. The total number of edges stored is 2*E (outgoing and incoming). E ≤ 10000, so at most 20000 edges stored. That's trivial.
- Create two distance arrays: dist_even and dist_odd, each of size N x N, initialized to -1 (or infinity).
- BFS 1 (even targets): Initialize queue with all (u, u) for u=1..N. Set dist_even[u][u] = 0. BFS on reverse product graph: when at state (u, v), for each label L, for each u_prev in inc[u][L] and v_prev in inc[v][L], if dist_even[u_prev][v_prev] is -1, set it to dist_even[u][v] + 1 and push to queue.
- BFS 2 (odd targets): Initialize queue with all (u, v) such that there is an edge u→v. Set dist_odd[u][v] = 0. BFS on reverse product graph similarly.
- For each pair (i, j), compute the answer:
   - If i == j, answer is 0 (already covered by even target, but we can just check).
   - Let d_even = dist_even[i][j], d_odd = dist_odd[i][j].
   - ans = infinity.
   - If d_even != -1: ans = min(ans, 2 * d_even)
   - If d_odd != -1: ans = min(ans, 2 * d_odd + 1)
   - If ans is infinity, output -1, else output ans.

Wait, is that correct? Let's test with the sample.

Sample 1:
N=4
C:
1: ab--
2: --b-
3: ---a
4: c---

Edges:
1->2: a
1->3: b
2->3: b
3->4: a
4->1: c

Let's compute manually some answers:
(1,4): expected 4.
In our BFS:
Even targets: (1,1), (2,2), (3,3), (4,4).
Odd targets: edges: (1,2), (1,3), (2,3), (3,4), (4,1).
We need distance from (1,4) to these targets in the forward product graph.
Let's find d_even: path from (1,4) to (u,u). (1,4) in forward product: from (1,4), we can take label 'a' on forward from 1 (1->2) and reverse from 4 (4->1? Wait, reverse from 4: we need a reverse edge from 4, i.e., original edge to 4. Original edges to 4: 3->4 with 'a'. So reverse from 4: we can go to 3. So state (1,4) with label 'a': forward 1->2, reverse 4->3 (since original 3->4 'a'). So new state (2,3). That's distance 1.
From (2,3): forward from 2: 2->3 'b'. Reverse from 3: original edges to 3: 1->3 'b', 2->3 'b'. So we can go to (3,1) and (3,2). Distance 2.
From (3,1): forward from 3: 3->4 'a'. Reverse from 1: original edges to 1: 4->1 'c'. No match for 'a' on reverse. So only 'c' on reverse? Forward has 'a', reverse has 'c' (incoming to 1: 4->1 'c'). So no match for 'a'. For label 'c': forward from 3 has no 'c' (only 'a'). So no outgoing from (3,1) with matching label? Wait, we need a label L that appears in both forward from 3 and incoming to 1. Forward from 3: only 'a'. Incoming to 1: 'c'. No match. So (3,1) is dead end.
From (3,2): forward from 3: 'a'. Incoming to 2: from 1->2 'a'. So match 'a': forward 3->4, reverse incoming to 2: 1->2, so reverse goes to 1. New state (4,1). Distance 3.
From (4,1): forward from 4: 'c' to 1. Incoming to 1: 'c' from 4. So match 'c': forward 4->1, reverse incoming to 1: 4->1, so reverse goes to 4. New state (1,4). Distance 4. We are back to (1,4) at distance 4. Not a target.
From (1,4) at distance 4, we can again go to (2,3) at distance 5, etc. This is a cycle. So we might not reach an even target. What about odd targets? We need to reach a state (u,v) with edge u->v. Let's see if we can reach (1,2) or (1,3) etc. From (2,3) at distance 2, we had (3,1) and (3,2). (3,1) not target. (3,2): is there an edge 3->2? No. From (3,2) we go to (4,1) at distance 3. (4,1): edge 4->1 exists! Yes, 4->1 is an edge. So (4,1) is an odd target. The distance from (1,4) to (4,1) is 3. So d_odd = 3. Then answer = 2*3+1 = 7. But expected answer is 4! So something is wrong.

Let's re-examine the expected answer for (1,4): they said length 4 path: 1->1->2->3->4. Wait, the path is 1 to 1 (length 0? No, path is 1 -> 1 -> 2 -> 3 -> 4. That's 4 edges. Labels: 1->1 has no edge? Wait, in the graph, is there a self-loop? The input: C_{1,1} is 'a'? Let's check sample input 1:
4
ab--
--b-
---a
c---
C_{1,1} = 'a', C_{1,2} = 'b', C_{1,3} = '-', C_{1,4} = '-'
C_{2,1} = '-', C_{2,2} = '-', C_{2,3} = 'b', C_{2,4} = '-'
C_{3,1} = '-', C_{3,2} = '-', C_{3,3} = '-', C_{3,4} = 'a'
C_{4,1} = 'c', C_{4,2} = '-', C_{4,3} = '-', C_{4,4} = '-'

So edges:
1->1: a
1->2: b
2->3: b
3->4: a
4->1: c

Path: 1 -> 1 (label a) -> 2 (label b) -> 3 (label b) -> 4 (label a). Labels: a b b a. That's a palindrome of length 4. So the path has edges: (1,1), (1,2), (2,3), (3,4). That's 4 edges. In our product graph BFS, we need to find a path from (1,4) to a target. Let's trace the product graph path corresponding to this palindrome.
The palindrome is: first half: 1 -> 1 (a), 1 -> 2 (b). Second half: 2 -> 3 (b), 3 -> 4 (a). The center is between the two b's? Actually, length 4 is even. So the first half is length 2: 1 to 2 (labels a, b). The second half reversed is 4 to 2 (labels a, b). So the middle vertex is 2. So the state should be (2,2) at distance 2? Let's see: from (1,4) we want to reach (2,2) at distance 2. Let's try to find a path of length 2 in the product graph from (1,4) to (2,2).
Step 1: from (1,4), match label? We need to go to some state (u,v) with distance 1. The palindrome first half starts with edge 1->1 (label a). The second half reversed starts with edge 4->3 (label a, since 3->4 is a, so reverse is 4->3). So we need a label 'a' that appears on outgoing from 1 and incoming to 4. Outgoing from 1: 'a' (to 1), 'b' (to 2). Incoming to 4: 'a' (from 3). So match 'a': forward 1->1, reverse 4->3. New state (1,3). Distance 1.
Step 2: from (1,3), we need next label 'b'. Outgoing from 1: 'b' to 2. Incoming to 3: 'b' from 1, 'b' from 2. So match 'b': forward 1->2, reverse: incoming to 3: 1->3 or 2->3. If we take 1->3, reverse goes to 1? Wait, reverse from v means original edge to v. Incoming to 3: 1->3 and 2->3. So reverse from 3 can go to 1 or 2. We want to go to state (2,2). So we need reverse to go to 2. That means original edge 2->3. So we take v' = 2. Then new state (2,2). Distance 2.
So from (1,4) to (2,2) in 2 steps. (2,2) is an even target! So d_even = 2. Then answer = 2*2 = 4. That matches expected.

In my earlier manual BFS, I missed the self-loop at 1. I said forward from 1: only 'a' and 'b'? Actually, forward from 1: 'a' to 1, 'b' to 2. I missed the self-loop when considering the first step. I considered forward 1->2 and reverse 4->3, but I didn't consider forward 1->1. So my manual trace was incomplete. The BFS algorithm will correctly find the self-loop.

So the BFS on the reverse product graph from even targets should compute d_even for (1,4) as 2. Let's verify with the reverse BFS idea: We start BFS from even targets (1,1), (2,2), (3,3), (4,4) in the reverse product graph. The reverse BFS will explore states (u,v) that can reach an even target. We want the distance from (1,4) to the nearest even target. In the forward product graph, the distance from (1,4) to (2,2) is 2. In the reverse product graph, the distance from (2,2) to (1,4) is also 2. So the BFS from (2,2) will reach (1,4) at distance 2. So dist_even[1][4] = 2. Then answer = 2*2 = 4. Good.

Now, for odd targets, we start BFS from all (u,v) with edge u->v. For (1,4), the nearest odd target in the forward product graph might be (4,1) at distance 3 as I found. But the answer is min(4, 7) = 4. So we need both distances. The BFS from odd targets will give dist_odd[1][4] = 3. Then we take min(2*2, 2*3+1) = min(4,7) = 4. Perfect.

So the algorithm is:
- Compute dist_even and dist_odd using BFS on the reverse product graph.
- For each (i,j), answer = min(2*dist_even[i][j] if not -1, 2*dist_odd[i][j]+1 if not -1). Also, if i==j, answer should be 0. But note that (i,i) is an even target, so dist_even[i][i] = 0, and 2*0 = 0. So it works.

Wait: Is it always true that if i==j, the empty path is considered? The problem says: "Among all (not necessarily simple) paths from vertex i to vertex j whose concatenation of labels on the edges forms a palindrome, what is the length of the shortest such path? If there is no such path, the answer is -1." And "Note that the empty string is also a palindrome." The empty string corresponds to a path of length 0, which is valid only if i == j. So for i == j, the answer is 0. Our BFS from even targets includes (i,i) with distance 0, so we get answer 0. So that's correct.

Now, we must ensure that the BFS on the reverse product graph correctly computes the shortest distance. The product graph is defined as:
- Vertices: (u,v) for u,v in 1..N.
- Directed edges: (u,v) -> (u',v') if there exists a label L such that there is an edge u -> u' with label L, and there is an edge v' -> v with label L (i.e., in the original graph, v' -> v).
We run BFS on the reverse of this graph. The reverse graph has edges (u',v') -> (u,v) if there is a label L with u -> u' and v' -> v.

In the BFS, we start with a set of sources. For even BFS, sources are (u,u) for all u. For odd BFS, sources are (u,v) for all edges u->v. We use a standard BFS with a queue. We maintain a visited array (dist). For each state (u,v) popped from the queue, we generate all reverse neighbors: for each label L, for each u_prev in inc[u][L] (i.e., edges x -> u with label L), and for each v_prev in inc[v][L] (edges y -> v with label L), we add (u_prev, v_prev) if not visited. The distance is dist[u][v] + 1.

This is exactly BFS on the reverse product graph. The number of states is N^2 = 10000. The BFS will visit each state at most once. The total work is sum over visited states of (number of reverse neighbors). As discussed, this is at most sum_L |E_L|^2 ≈ 3.85M. So it's very fast.

Let's verify with the second sample to be sure. Sample 2:
5
us---
-st--
--s--
u--s-
---ts

Edges:
1->1: u
1->2: s
2->2: s
2->3: t
3->3: s
4->1: u
4->4: s
5->4: t
5->5: s

We need to compute answers. The BFS will handle it.

One edge case: What if there is a path that uses the same vertex multiple times? The BFS on the product graph handles non-simple paths because the product graph states can repeat (u,v) only if the same pair of vertices is reached, but since we use a visited array, we only process each state once. This is correct because the BFS finds the shortest path in the product graph, which corresponds to the shortest palindrome walk. Even if the walk revisits vertices, the product graph state might be visited with a shorter distance. Since we only care about the shortest distance, BFS is correct.

Another edge case: The odd target is (u,v) with edge u->v. The distance d_odd is the number of product graph edges from (i,j) to (u,v). The palindrome length is 2*d_odd + 1. But what if the edge u->v is the first edge? Then d_odd = 0, and answer = 1. That corresponds to a palindrome of length 1: just the edge label itself. Since a single letter is a palindrome, the answer should be 1 if there is a direct edge. Our BFS: odd target (u,v) with edge u->v. dist_odd[u][v] = 0. For (i,j) = (u,v), dist_odd[u][v] = 0, so answer = 1. Also, could there be an even shorter palindrome? The empty string is length 0, but that's only for i==j. For i != j, length 0 is not possible. So 1 is correct.

What about a palindrome of length 2? That would be two edges with same label: i -> k -> j with label L on both edges. The center is the vertex k. In our framework, that's an even target (k,k) at distance 1? Let's see: from (i,j) to (k,k) in 1 step: we need a label L such that i->k and j'->j? Wait, for even length 2, the palindrome is L L. The first half is L, second half is L. The state after 1 step: we have matched one L. The forward walk goes i->k, the reverse walk goes j->? We need the reverse walk to go from j to k as well, because the second half reversed is the first half. So the state after 1 step should be (k, k). And the transition requires a label L on i->k and on j->k? But reverse from j: we need original edge k->j with label L. So we need edge i->k with label L, and edge k->j with label L. So from (i,j), we need a label L that is on outgoing from i to k, and on incoming to j from k (i.e., outgoing from k to j in original). So the condition is: there exists k and L such that i->k labeled L and k->j labeled L. In the product graph, this is exactly one step from (i,j) to (k,k) with label L. The reverse BFS from even target (k,k) will have dist_even[i][j] = 1. Then answer = 2*1 = 2. Correct.

What about palindrome of length 3? Labels L M L. The center is the edge with label M. The first half is L, second half reversed is L. The state after matching the first L: forward i->k, reverse j->m? Actually, let's derive: palindrome of length 3: i -> a -> b -> j, with labels L, M, L. The center is the edge a->b. The first half is L (i->a). The second half is M, L. Reversed, it's L, M. So the first part of the second half is L (j->b? Wait, the second half is from b to j: labels M, L. Reversed, it's L, M. So the first edge of the reversed second half is the last edge of the original second half, which is the edge b->j with label L. So the reverse walk starts at j and takes an edge j->? Actually, reverse walk in the product graph corresponds to walking backwards in the original graph? Let's be systematic.

In the product graph forward: from (i,j) we want to reach an odd target (a,b) where there is an edge a->b with label M. The path corresponds to: forward walk from i to a, and reverse walk from j to b. The reverse walk from j means walking along edges in the original graph in reverse? No, the reverse walk in the product graph uses reverse edges of the original graph. Specifically, a step in the product graph from (u,v) to (u',v') uses forward edge u->u' and reverse edge v'->v (original). So if we start at (i,j), after d steps we are at (u,v). The forward walk is i -> ... -> u. The reverse walk is j -> ... -> v? Wait, the reverse walk uses reverse edges: a reverse edge v'->v means original edge v'->v. So if we take a step from (u,v) to (u',v'), the reverse walk moves from v to v'? Let's trace: start (i,j). Step 1: use forward i->i' and reverse j'->j (original). So the reverse walk moves from j to j' (since original edge is j'->j, reverse is j->j'). So the reverse walk goes j -> j' (using the reverse of original edge j'->j). So the reverse walk is actually a walk in the original graph following edges backwards. So the reverse walk from j reaches v after d steps, meaning there is a path in the original graph from v to j of length d (the reverse of the walk we took). But the labels on the reverse walk are the same as the labels on the forward walk. So the string of labels on the reverse walk (which is a walk from v to j in the original graph) is the same as the string on the forward walk from i to u. So the palindrome is formed by the forward walk from i to u, then the edge u->v (center), then the reverse of the reverse walk from v to j. That is, the full palindrome is: labels on i->...->u, then label of u->v, then labels on v->...->j reversed. Since the labels on the reverse walk (v->...->j) are the same as on the forward walk (i->...->u), the concatenation is symmetric. The length is 2d + 1. So that matches.

Thus, the BFS on the reverse product graph starting from odd targets (u,v) with edge u->v will correctly compute the distance d_odd such that there is a walk from i to u and a walk from j to v (in the reverse sense) of length d with matching labels. The palindrome length is 2d+1.

So the algorithm is correct.

Now, we need to implement it efficiently in Python.

Implementation details:
- N up to 100.
- Read N, then N strings of length N.
- Build outgoing and incoming adjacency lists. Since labels are lowercase letters, we can map 'a'-'z' to 0-25.
- For each vertex u, we have out[u] as a list of 26 lists, or a dict. Since N=100 and alphabet=26, we can use a list of 26 lists. Each list contains the target vertices.
- Similarly, inc[u] for incoming edges.
- BFS:
   - Use collections.deque.
   - For even BFS: initialize dist_even = [[-1]*N for _ in range(N)]. For u in 0..N-1: dist_even[u][u] = 0, push (u,u) to queue.
   - While queue: pop (u,v). For L in 0..25: for u_prev in inc[u][L]: for v_prev in inc[v][L]: if dist_even[u_prev][v_prev] == -1: set to dist[u][v]+1, push.
   - For odd BFS: similarly, but sources are all (u,v) such that there is an edge u->v. We can precompute a list of such pairs. For each edge u->v with label L, we add (u,v) to sources. Note that there could be multiple edges with the same (u,v)? No, at most one edge between two vertices. So the set of odd targets is exactly the set of edges in the original graph. So we can iterate over all edges and add (u,v) to the source list. We should be careful: if there are multiple edges with different labels, (u,v) is still one target. We only need to add it once. So we can maintain a boolean array odd_target[u][v] and set it to True if there is any edge u->v. Then