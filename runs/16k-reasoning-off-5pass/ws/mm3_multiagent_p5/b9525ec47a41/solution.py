import sys
sys.setrecursionlimit(1 << 25)
MOD = 998244353

def solve():
    input_data = sys.stdin.read().split()
    N = int(input_data[0])
    s = input_data[1].strip()
    k = s.count('1')
    
    # Each vertex i (0 <= i < N) has degree in the tree part (excluding cycle edges) as s_i (the spoke)
    # The cycle edges contribute 1 to each vertex's degree (two cycle edges per vertex, but for tree DP after breaking cycle)
    # Actually, we break the cycle by removing one cycle edge, say (0,1). Then we have a tree T.
    # In T, each vertex i has degree: (if s_i=1) then 1 for spoke, plus cycle edges: 2 for all vertices except endpoints 0 and 1 have 1 cycle edge.
    # Let's carefully define the tree.
    # Graph: cycle C_N on vertices 0..N-1, plus vertex N connected to i iff s_i=1.
    # Remove edge (0,1) from the cycle. The resulting graph is a tree T.
    # Degrees in T:
    # - Vertex 0: originally deg=2 (cycle) + s_0. Remove edge (0,1), so cycle edges left: (N-1,0). So deg_T(0) = 1 + s_0.
    # - Vertex 1: originally deg=2 + s_1. Remove edge (0,1), so cycle edges left: (1,2). So deg_T(1) = 1 + s_1.
    # - Vertex i (2 <= i <= N-1): originally deg=2 + s_i, both cycle edges present. So deg_T(i) = 2 + s_i.
    # - Vertex N: deg_T(N) = k.
    # The tree T has N+1 vertices and E_T = N + k edges (since original E = N + k, removed one cycle edge).
    # For a tree, the number of distinct in-degree sequences is the number of vectors d with 0 <= d_v <= deg_T(v) and sum d_v = E_T.
    # This is the coefficient of x^{E_T} in product_{v} (1 + x + ... + x^{deg_T(v)}).
    # We can compute this via DP: dp[j] = number of ways to achieve sum j.
    # But N up to 10^6, E_T up to 2*10^6, DP O(N * E_T) is too slow.
    # However, we can use generating functions and the fact that many vertices have small degree.
    # Actually, for a tree, the number of score sequences is exactly the product of (deg_T(v)+1) minus something? No.
    # Wait, for a tree, the number of in-degree sequences is not simply the product; the sum constraint matters.
    # But we can compute it efficiently using the fact that the tree is a path with some pendant edges.
    # Specifically, T is a path 0 - 1 - 2 - ... - (N-1), with vertex N connected to some of the path vertices.
    # This is a "caterpillar" graph. We can process it sequentially.
    # For each vertex i (0..N-1), we have:
    #   - if i=0: one cycle edge to i-1 (which is N-1) and possibly spoke to N.
    #   - if i=1..N-2: two cycle edges (to i-1 and i+1) and possibly spoke.
    #   - if i=N-1: one cycle edge to N-2 and possibly spoke.
    # But after removing (0,1), the path is 0 - 1 - 2 - ... - N-1, with edges (i, i+1) for i=0..N-2, plus spokes.
    # Vertex N is connected to some path vertices.
    # This is a tree. We can compute the number of in-degree sequences by DP from leaves.
    # Since it's a tree, we can root it at, say, vertex N. Then each path vertex is a child of N if it has a spoke, otherwise its parent is the previous path vertex.
    # Actually, the tree structure: N is connected to some i in B (where s_i=1). The rest of the tree is the path 0-1-...-N-1.
    # If we root at N, then the children of N are the vertices in B. The path vertices are connected in a line.
    # We can do a DP on the tree using the fact that the number of score sequences of a tree can be computed by a simple recurrence if we know the degree sequence? Not simple.
    # However, there is a known formula: for a tree, the number of in-degree sequences is the number of ways to assign each edge to one endpoint such that the in-degree of v is the number of edges assigned to v. This is equivalent to: for each edge, choose a direction. The in-degree sequence is determined by the choices. The number of distinct in-degree sequences is the size of the image of the map from {orientations} to {in-degree vectors}.
    # For a tree, this image is exactly the set of vectors d with 0 <= d_v <= deg(v) and sum d_v = E. This is a polytope. The number of integer points in this polytope is the coefficient in the product.
    # We can compute this coefficient using a linear time algorithm if we can do convolution. But the degrees are up to 2, so the polynomials are (1+x) or (1+x+x^2) or (1+x+x^2+x^3) etc.
    # Actually, for a path of length N, the number of in-degree sequences is something. But here we have the extra vertex N.
    # Let's compute the generating function for the tree T.
    # We can do a DP that maintains the number of ways to achieve a given sum, but we can compress because the maximum sum is E_T = N + k.
    # Since N <= 10^6, E_T <= 2*10^6, a DP with O(N * E_T) is too slow (10^12). We need O(N) or O(N log N).
    # But wait! For a tree, the number of in-degree sequences might be computed by a simple product? No, the sum constraint is global.
    # However, note that the tree T is a path with some pendant edges. We can process it by splitting into components.
    # Actually, we can use the fact that the number of in-degree sequences of a tree is equal to the number of ways to choose a subset of edges for each vertex? No.
    # Let's think about the structure: T is a tree. The number of in-degree sequences is the number of vectors d such that there exists an orientation with in-degree d. By a theorem of Hakimi, for a tree, this is exactly the set of vectors with 0 <= d_v <= deg(v) and sum d_v = E. The number of such vectors is the permanent of a certain matrix? No.
    # We can compute it by a greedy algorithm: for a tree, we can assign the in-degrees from leaves inward. At each step, we choose the in-degree of the leaf (0 or 1) and then remove the leaf, adjusting the degree of its neighbor. This is similar to counting the number of ways to prune the tree. This can be done in linear time using a stack, but we need to count the number of valid assignments.
    # Actually, the number of valid d vectors is equal to the number of ways to choose, for each vertex, the number of incident edges oriented toward it, such that the sum is E. This is exactly the number of ways to assign each edge to one of its endpoints, with the constraint that the total assigned to v is between 0 and deg(v). This is the number of "edge covers" of the tree? No.
    # We can model it as: for each edge e=(u,v), we choose a direction u->v or v->u. This is equivalent to choosing, for each vertex, a subset of its incident edges to be incoming. The global constraint is that each edge is incoming to exactly one endpoint. So we are choosing a subset of edges to be "incoming to v" for each v, such that for each edge, exactly one of its endpoints chooses it as incoming. This is exactly a "cut" or "orientation". The in-degree sequence is the vector of sizes of these subsets.
    # So the number of distinct in-degree sequences is the number of vectors (S_v) such that there exists a partition of the edges into sets S_v (with 0 <= |S_v| <= deg(v)) such that each edge is in exactly one S_v. This is the number of "degree sequences of orientations".
    # For a tree, there is a known result: the number of orientations with a given in-degree sequence d is 1 if the sequence is valid (i.e., satisfies the leaf condition), and 0 otherwise. Actually, for a tree, an orientation is uniquely determined by its in-degree sequence? Let's check: path 0-1-2. d=(0,1,1). Is the orientation unique? We need d_0=0, so edge (0,1) must be 1->0. d_2=1, so edge (1,2) must be 1->2. Then d_1 gets 1 from (0,1)? 1->0 gives d_0=1, d_1=0. And 1->2 gives d_2=1, d_1=0. So d_1=0, but we need 1. Contradiction. So (0,1,1) is not realizable? But earlier I said (0,1,1) is realizable for the path 0-1-2. Let's re-check: For path 0-1-2, edges (0,1) and (1,2). To get d=(0,1,1): d_0=0 means (0,1) is 1->0. d_2=1 means (1,2) is 1->2. Then d_1 gets from 0? 1->0 gives d_1=0. 1->2 gives d_1=0. So d_1=0. So (0,1,1) is NOT realizable. My earlier claim that (0,1,1) is realizable was wrong! Let's correct: For path 0-1-2, the possible in-degree sequences are those with sum=2, and d_0,d_2 ∈ {0,1}, d_1 ∈ {0,1,2}. But are all such vectors realizable? Let's list: (0,2,0): 0->1, 2->1. (0,1,1): impossible as shown. (0,0,2): d_2=2 impossible since deg(2)=1. (1,1,0): 1->0 and 2->1? If 1->0, d_0=1, d_1=0. Then need d_1=1, so 2->1 gives d_1=1, d_2=0. So d=(1,1,0). (1,0,1): 0->1 and 2->1 gives d_0=0? Wait, 0->1 gives d_0=0, d_1=1. 2->1 gives d_2=0, d_1=2. So d=(0,2,0). That's (0,2,0). So (1,0,1) means d_0=1, d_1=0, d_2=1. Can we get that? 1->0 gives d_0=1, d_1=0. Then need d_2=1, so 1->2 gives d_1=0, d_2=1. Then d_1=0. So d=(1,0,1) is realizable: 1->0 and 1->2. (0,1,1) is not. (1,1,0) is realizable: 1->0 and 2->1. (0,0,2) invalid. (2,0,0) invalid. So the realizable sequences are (0,2,0), (1,0,1), (1,1,0). That's only 3 out of the 4 with sum=2 and degree bounds. So the condition is not just degree bounds! For a tree, there is a parity condition or something? Actually, for a tree, an orientation is determined by the in-degrees if we also know the out-degrees. The condition is that the in-degree sequence must satisfy that for every subtree, the sum of in-degrees is at most the number of edges in the subtree? More precisely, for any subset of vertices, the number of edges with both endpoints in the subset that are oriented toward the subset must be at least the sum of in-degrees in the subset minus the number of edges from the subset to the outside? This is complicated.
    # However, for our specific tree T, which is a path with pendant edges to N, we can use the fact that it's a "caterpillar" and we can compute the number of in-degree sequences by a linear DP using the fact that the path has small degree.
    # Actually, the number of in-degree sequences of a path of length N is known: for a path, the in-degree sequence is determined by the sequence of "turns". For a path, the orientations correspond to choices of direction for each edge, and the in-degree sequence is a sequence where each internal vertex has in-degree 0,1,2, and the sum is N-1? Wait, a path of N vertices has N-1 edges. The in-degree sequence of a path orientation: endpoints have in-degree 0 or 1, internal have 0,1,2. The number of distinct in-degree sequences of a path of length N is 2N? For N=3, we had 3. For N=4, path 0-1-2-3: edges (0,1),(1,2),(2,3). Possible in-degrees: sum=3. Let's compute number of distinct in-degree sequences. It might be N+1 choose 2? Not sure.
    # But our tree T is not a simple path; it has vertex N attached to some vertices.
    # Maybe we can use the fact that the graph G (the original cycle with spokes) is a partial 2-tree. The number of score sequences can be computed by dynamic programming on a tree decomposition. Since the graph has a cycle, we can do DP on the cycle by fixing the in-degree of one cycle edge's endpoint.
    # Let's go back to the original graph G. We want the number of distinct in-degree sequences of G. We already derived that the cycle orientations are given by a binary string a, and d_i = 1 + a_{i-1} - a_i + y_i. The y_i are independent choices for s_i=1. So the set of d sequences is the union over a of the boxes S(a) = { d : d_i = 1 + a_{i-1} - a_i + y_i, y_i ∈ {0,1} for s_i=1, else 0 }.
    # Now, note that 1 + a_{i-1} - a_i depends only on the edge (i-1,i) in the cycle. Specifically, if we define e_i = 1 + a_{i-1} - a_i, then e_i is the in-degree of i from the cycle. As a varies, e varies over all valid cycle in-degree sequences.
    # The key observation: for a fixed e, the set of d is the product over i of intervals. The union over e of these boxes.
    # Since the boxes are aligned (they are products of intervals), the union is a set of integer points that can be described by constraints. The number of points in the union is the number of d such that there exists e with d_i ∈ {e_i, e_i+1} (if s_i=1) or d_i = e_i (if s_i=0), and e is a valid cycle in-degree sequence.
    # This is exactly: d is valid if we can choose e_i ∈ {0,1,2} such that for s_i=0, e_i = d_i; for s_i=1, e_i ∈ {d_i, d_i-1}; and the sequence e is a valid cycle in-degree sequence (i.e., comes from some a).
    # The condition for e to be valid is that the partial sums of e_i - 1 are bounded. As we saw, this is equivalent to: for any cyclic interval, the number of 2's is at least the number of 0's (or vice versa). More precisely, there exists a starting point such that the partial sums of d_i = e_i - 1 stay in {0,1} (or {0,-1}). This is a global condition.
    # However, we can use the transfer matrix method with a variable z that tracks the partial sum. Since the state space is small (the current value of a_i, or the current partial sum), we can do a DP that computes the generating function for the number of d sequences.
    # Let's define a state for each position i that captures the necessary boundary information. The condition for e to be valid is that the sequence e_i - 1 has partial sums (in some direction) bounded. This is equivalent to saying that the walk e_i - 1 on integers with steps -1,0,1 never goes below 0 or above 1, after a cyclic shift. This is exactly the condition for a Dyck path but with a band of width 2.
    # We can eliminate the cyclic shift by fixing the starting value. Suppose we fix a_0. Then the condition is that the partial sums of e_i - 1 starting from i=1 (with a_0 given) are in {0,1} or {0,-1} depending on a_0. Actually, if a_0=0, then a_i = -S_i, so S_i ∈ {0,-1}. If a_0=1, S_i ∈ {0,1}. So for a fixed a_0, the condition is that the partial sums of e_i - 1 (with S_0=0) stay in {0, -a_0}? Let's derive: a_i = a_0 - S_i, where S_i = sum_{j=1}^i (e_j - 1). We need a_i ∈ {0,1}. So S_i must be a_0 or a_0 - 1. So S_i ∈ {a_0, a_0-1}. Since S_0=0, if a_0=0, S_i ∈ {0,-1}; if a_0=1, S_i ∈ {1,0}. So the partial sums are either in {0,1} (if a_0=1) or in {0,-1} (if a_0=0). So the condition is that the walk S_i stays within a band of two values.
    # Now, for a fixed a_0, the number of e sequences (and thus d sequences) can be computed by a DP that tracks the current S value (which can be one of two values). For each i, given the current S, we can choose e_i (which determines the next S) and also choose y_i (if s_i=1) to get d_i. The transition depends on s_i.
    # Since the state space is constant (S can be one of two values, and a_0 is fixed), we can do this DP in O(N) time! And then we sum over the two choices of a_0, and also we need to account for the fact that different a_0 might generate the same d sequence. But wait: for a fixed a_0, the DP computes the number of (e, y) pairs, but we want the number of distinct d sequences. However, the mapping from (e, y) to d is: for s_i=0, d_i = e_i; for s_i=1, d_i = e_i + y_i, with y_i ∈ {0,1}. So given d, e is determined if we know y_i. But for a fixed a_0, the DP computes the number of (e, y) sequences that produce a given d sequence. As we noted earlier, for a given d, there may be multiple (e, y) pairs. But in the DP for a fixed a_0, the e sequence is determined by a_0 and the choices of e_i. Actually, a is determined by a_0 and the e_i. So for a fixed a_0, each valid e sequence gives a unique a, and then each choice of y gives a unique d. So the number of (a, y) pairs with a_0 fixed is exactly the number of walks in the DP. The number of distinct d sequences generated by a_0 is at most the number of such pairs. But we need the number of distinct d sequences across both a_0. Since the mapping from (a, y) to d is not injective, we cannot simply sum the counts of pairs.
    # However, we can compute the generating function for the number of d sequences by using the fact that the DP state includes the current d_i? No.
    # Alternative: we can compute the number of distinct d sequences by building a DFA for the set of d sequences. Since the state space for the partial sum is small, and the output d_i is determined by e_i and y_i, we can create a new automaton whose states are the possible pairs (a_{i-1}, a_i) or the possible S values. Actually, the transition from a_{i-1} to a_i determines e_i = 1 + a_{i-1} - a_i. So if we know a_{i-1} and a_i, we know e_i. Then d_i is either e_i or e_i+1. So the output d_i is a function of the transition a_{i-1} -> a_i and the choice of y. So we have a finite state machine with states a ∈ {0,1}. The transitions are labeled by the possible d values. The set of d sequences generated by this machine (with the cycle condition a_N = a_0) is a regular language. The number of distinct strings of length N in this language can be computed by the number of paths in the machine, but we need to count distinct strings, not paths.
    # There is a standard method: the number of distinct strings of length N generated by an NFA is equal to the number of states in the minimal DFA, or we can compute it by taking the product of the NFA with itself? Actually, the number of distinct strings accepted by an NFA M of size S over alphabet Σ of length N is at most S * |Σ|^N, but we can compute it by the following: the set of strings is the image of the map from paths to strings. We can compute the number of distinct strings by dynamic programming on the NFA states, but tracking the set of possible strings. Since the NFA has only 2 states, the set of possible strings can be represented as a regular language with at most 2^2 = 4 states (the subset construction). So we can build a DFA with 4 states that accepts exactly the set of possible d sequences. Then the number of distinct d sequences of length N is the number of paths of length N in this DFA that start at the initial state and end in a state that corresponds to a valid cycle? But we also have the cycle condition on a. The DFA for the linear chain (ignoring the cycle) will have 4 states. The cycle condition means we only accept strings that can be generated by a cycle, i.e., the walk on a must be a cycle. In the DFA, the state is a subset of {0,1}. The initial state is the singleton {a_0} (for each a_0). After processing the string, we are in some subset S. The string is valid if S is nonempty and there exists a way to close the cycle? Actually, the cycle condition is that the walk on a is a cycle, which means the final state of a must equal the initial state. In the DFA, the state is a set of possible a states. For the string to be generated by a cycle with a_0 fixed, we need that starting from a_0, we end up in a set of states that includes a_0. But more precisely, the string is valid if there exists a path in the original NFA that is a cycle. This is equivalent to: in the subset construction, starting from {a_0}, after reading the string, we are in a subset S, and there is an edge in the original NFA from some state in S back to a_0 that is consistent with the cycle? No, the cycle condition is already built into the fact that we are considering a cycle of length N. If we break the cycle at some point, we have a linear chain of N transitions that start at a_0 and end at a_N, with a_N = a_0. So the final state must be a_0. In the DFA, the state is a subset of {0,1}. If we start at {a_0}, after N steps we are at some subset S. The string is valid if a_0 ∈ S. But actually, the DFA state is the set of possible current a states. For a fixed string, the set of possible a states after reading the string is exactly the set of a such that there is a path labeled by the string from a_0 to a. So the string is realizable as a cycle if and only if a_0 is in the final set. So for a fixed a_0, the set of valid d strings is the set of strings of length N that are accepted by the DFA starting at {a_0} and ending at a state that contains a_0.
    # So we can build a DFA with 4 states (the subsets of {0,1}) for each position i, but the transitions depend on i because s_i varies. Actually, the NFA transitions depend on i (since the allowed y depend on s_i). So the DFA for the whole cycle is time-varying: the transition matrix T_i for position i is a 4x4 matrix where T_i[S, S'] is 1 if there is a symbol d that causes transition from S to S'. But we need to count the number of distinct strings, not the number of paths. In a DFA, the number of distinct strings of length N is exactly the number of paths of length N in the DFA, but since it's deterministic, each path gives a unique string. Wait, in a DFA, for a given start state, each path gives a unique string. So the number of distinct strings is exactly the number of paths! But our DFA is nondeterministic in the sense that from a state S, on a given symbol d, there might be multiple next states? No, in a DFA, the transition is deterministic: for each state and each symbol, there is exactly one next state. In our subset construction, the transition on symbol d from subset S is the set of states that can be reached by some a in S via a transition labeled d. This is a deterministic function of S and d. So the resulting automaton is a DFA. However, the alphabet is the set of possible d values. For each position i, the set of possible d values is a subset of {0,1,2,3} (or smaller). The transition function δ_i(S, d) = { a' : ∃ a ∈ S, ∃ y allowed such that d = 1 + a - a' + y and a' ∈ {0,1} }.
    # This is a deterministic function from (S, d) to S'. So we have a DFA with 4 states. The number of distinct d strings of length N that are accepted starting from initial state S0 and ending in a state that contains a_0 is exactly the number of paths of length N in this DFA from S0 to a state S with a_0 ∈ S, where the path is labeled by the d symbols. But wait: in a DFA, a path is a sequence of states and symbols. The number of distinct strings is the number of paths, because each path gives a unique string. But is that true? Yes, in a DFA, the string is exactly the sequence of input symbols. So two different paths must differ in either states or symbols, but if they have the same sequence of symbols, they might have different states? Actually, in a DFA, the next state is uniquely determined by the current state and the input symbol. So a sequence of input symbols determines a unique sequence of states. Therefore, there is a bijection between strings and paths! So the number of distinct strings is exactly the number of paths. But this is only true if the DFA is complete and deterministic. Our DFA is deterministic: from each state S and each symbol d that is allowed at that step (the allowed symbols depend on i and S), the next state is uniquely determined. So for a fixed sequence of positions, the number of distinct d strings is the number of paths in this time-varying DFA from the initial state to an accepting state. But wait: the initial state is S0 = {a_0} for a_0=0 or 1. So we have two starting states. The accepting condition is that after N steps, the current state S contains a_0. So the number of distinct d strings is the number of paths of length N in the DFA (with time-varying transitions) that start at {0} and end at a state containing 0, plus those that start at {1} and end at a state containing 1. But note: a string might be generated by both a_0=0 and a_0=1. So we would be double-counting! So we need to count the union of the two sets of strings. This is not simply the sum of the number of paths from the two starts, because a string could be accepted from both starts. We need the number of distinct strings accepted by the NFA (which is the union of the languages from the two starts). Since the DFA is the subset construction of the NFA, the language of the NFA is exactly the language of the DFA starting from the initial states {0} and {1} (with accepting condition that the final state contains the start state). But note: the NFA has two possible cycles: one starting with a_0=0 and one with a_0=1. A string d is in the language if there exists some a_0 such that the string can be generated by a cycle starting and ending at a_0. In the DFA, the initial state is the set of possible start states? Actually, if we start with the set {0,1} as the initial state, then a string is accepted if after reading it, there is some a_0 in the initial set and some a in the final set such that a = a_0 and there is a path from a_0 to a. But the initial set is {0,1}. The DFA state after reading the string is the set of all a such that there is a path from some a_0 in the initial set to a. So if we start with {0,1}, the final set S has the property that a ∈ S iff there exists a_0 ∈ {0,1} with a path from a_0 to a labeled by the string. For the string to correspond to a cycle, we need a_0 = a. So we need that there exists a such that a ∈ S and there is a path from a to a? That is, a is in S and the path starts and ends at a. This is equivalent to: the set of start states that can reach their own value. This is not simply S containing a.
    # Let's be precise. Let the NFA have states 0 and 1. For a fixed a_0, the set of strings generated by cycles starting at a_0 is the set of strings for which there is a path from a_0 to a_0 of length N. The subset construction from a_0 gives a DFA with start state {a_0}. After N steps, the state is S. The string is accepted if a_0 ∈ S. So the language L_{a_0} is the set of strings such that the DFA starting at {a_0} ends in a state containing a_0. The overall language is L_0 ∪ L_1. We want |L_0 ∪ L_1|. The number of paths in the DFA from {a_0} to a state containing a_0 is exactly the number of strings in L_{a_0} (since the DFA is deterministic, each path gives a unique string, and all strings in L_{a_0} correspond to a path). So |L_{a_0}| is the number of paths from {a_0} to any state S with a_0 ∈ S. But |L_0 ∪ L_1| is not simply the sum because a string could be in both L_0 and L_1. However, note that if a string is in both L_0 and L_1, it must be that there is a path from 0 to 0 and from 1 to 1 labeled by the same string. This means the string can be generated by a cycle in both ways. We need to count distinct strings, so we need the size of the union.
    # We can compute the size of the union by inclusion-exclusion: |L_0 ∪ L_1| = |L_0| + |L_1| - |L_0 ∩ L_1|. So we need to compute |L_0|, |L_1|, and |L_0 ∩ L_1|. The intersection L_0 ∩ L_1 is the set of strings that have a path from 0 to 0 and from 1 to 1. This is equivalent to: the DFA starting from {0,1} ends in a state S such that 0 ∈ S and 1 ∈ S? Not exactly. If we start the DFA from {0,1}, then after reading the string, the state S is the set of a such that there is a path from some start state to a. For the string to be in L_0, we need a path from 0 to 0. For it to be in L_1, we need a path from 1 to 1. So if we start from {0,1}, the string is in L_0 ∩ L_1 iff there is a path from 0 to 0 and from 1 to 1. This means that in the DFA starting from {0,1}, the final state S must contain 0 (for the 0->0 path) and 1 (for the 1->1 path). So S must be {0,1}. But wait: it's possible that 0 ∈ S and 1 ∈ S, but the paths might be different? In the DFA, S is exactly the set of states reachable from some start state via the string. So 0 ∈ S means there is a path from some start state to 0. For it to be from 0, we need that the path starts at 0. But if we started from {0,1}, the path could start at 0 or 1. If 0 ∈ S, it could be reachable from 1. So the condition for a path from 0 to 0 is not simply 0 ∈ S; it requires that the path specifically starts at 0. So the DFA from {0,1} does not directly give the intersection. We need a more refined approach.
    # We can compute the number of distinct strings by building a DFA whose states are the possible pairs of paths? Actually, the number of distinct strings is the number of states in the minimal DFA. We can compute the minimal DFA by merging states that are equivalent. Since the NFA has only 2 states, the subset construction gives at most 4 states. We can then minimize this DFA (which may have fewer states). The number of distinct strings of length N is then the number of paths of length N from the initial state to the accepting state in this minimal DFA? But the DFA is time-varying, so we cannot minimize globally. However, we can consider the product of the NFA with itself? The standard way to count the number of distinct strings generated by an NFA M is to consider the NFA M x M (the product) and count the number of accepting paths that are "different" in some sense. Actually, the number of distinct strings is the number of paths in the NFA that are "unique" up to the string. This is equal to the number of states in the deterministic automaton obtained by the "powerset construction" on the NFA, but with the accepting condition that the state is "coaccessible" etc. For a time-varying NFA, the number of distinct strings of length N is the number of sequences of symbols d_0...d_{N-1} such that there exists a path in the NFA. This is exactly the number of sequences of symbols that are accepted by the NFA. We can compute this by a DP that tracks the set of possible NFA states after reading the prefix, but we also need to know the start state? Actually, for a fixed start state, the set of strings is the set of strings accepted by the NFA from that start state. The union over start states is the set of strings accepted from any start state. This is exactly the set of strings accepted by the NFA with initial state set {0,1} and accepting condition that the final state is "compatible" with a cycle? No, the cycle condition requires that the final state equals the start state. So for a string to be valid, there must exist a start state a_0 such that the string takes a_0 to a_0. This is equivalent to: the string is accepted by the NFA if we consider the NFA as having a transition from a back to a_0 at the end? No.
    # Let's think of the whole cycle as a single NFA that reads a string of length N and checks if it can be a cycle. We can model the cycle as follows: the state is the current a value. The string is read, and we transition. At the end, we require that the final a equals the initial a. This is a standard "cycle" condition. The number of distinct strings of length N that are accepted by this cyclic NFA is the number of strings d such that the product of the transition matrices (for each symbol) has a non-zero entry on the diagonal? Not exactly.
    # Since the NFA is small, we can do the following: for each possible string d, we can determine if it is valid by checking if there exists a_0 such that the transitions are possible. But we cannot enumerate strings.
    # However, we can use the fact that the output d_i is determined by the transition a_{i-1} -> a_i and the choice of y_i. So the set of possible transitions from a to a' is a set of d values. For each pair (a, a'), let D_i(a, a') be the set of d values that can be produced at position i when going from a to a'. This set depends on s_i. Specifically:
    # If s_i=0: D_i(a, a') = {1 + a - a'}.
    # If s_i=1: D_i(a, a') = {1 + a - a', 2 + a - a'}.
    # So D_i(a, a') is either a singleton or a set of size 2.
    # Now, a string d is valid if there exists a sequence a_0,...,a_N (with a_N = a_0) such that for each i, d_i ∈ D_i(a_{i-1}, a_i).
    # This is exactly the condition that the sequence of d_i can be "parsed" as a path in this graph.
    # We can think of the d_i as being generated by a walk on the directed graph with vertices {0,1} and edges labeled by sets D_i. The string is valid if there is a closed walk of length N that respects the edge labels.
    # The number of distinct strings of length N generated by a closed walk is what we want.
    # This is a classic problem: counting the number of distinct strings of length N accepted by a finite automaton with a cycle condition. Since the automaton is tiny, we can use matrix exponentiation or DP with state being the pair (a, a')? No.
    # We can use the following trick: the number of distinct strings is the number of paths in a certain graph. For each i, we can define a 4x4 matrix M_i where the rows and columns are the possible "boundaries". Since the condition is on a closed walk, we can fix the starting a_0. For a fixed a_0, the number of strings generated by closed walks starting at a_0 is the number of strings d such that there is a path from a_0 to a_0 labeled by d. This is the set of strings accepted by the NFA from state a_0. The number of such strings is the number of paths in the DFA obtained by subset construction from a_0. But as we saw, we need the union over a_0.
    # Since there are only 2 states, the subset construction from a_0 yields a DFA with at most 2 states (the reachable subsets of {0,1} from a_0). From a_0, the possible subsets after some steps are: {a_0} (if we haven't moved? Actually, from a_0, after one step, we can be at a' which is either 0 or 1, so the subset is {a'}. So the state in the DFA is just the current a value? Not exactly, because the DFA state is the set of possible a values. Since we start with a_0, the possible a values are always a single state? Let's check: if we start at a_0=0, can we reach both 0 and 1? Yes, if the string allows both. For example, if s_i=1, there might be transitions that can go to either 0 or 1. So the subset can be {0} or {1} or {0,1}. So the DFA has up to 3 states: {0}, {1}, {0,1}. The transitions are deterministic on symbols. So we can build this DFA for each a_0, and the number of strings from a_0 is the number of paths of length N from {a_0} to {a_0} (since we need to end at a_0 to close the cycle). But wait: the DFA state is the set of possible a. For a string to be accepted from a_0, we need that after reading the string, the DFA is in a state that contains a_0, and there is a path from a_0 to a_0. But in the DFA, the state is the set of a that can be reached from a_0. If the state contains a_0, that means there is a path from a_0 to a_0. So the accepting condition is that the DFA state contains a_0. So the number of strings from a_0 is the number of paths of length N in the DFA from start state {a_0} to any state S that contains a_0. But note: the DFA is time-varying, so the transition matrix depends on i.
    # We can compute the number of such paths for a fixed a_0 by a DP that tracks the current DFA state. The DFA state is a subset of {0,1}. The start state is {a_0}. The transitions: from a subset S, on symbol d, the next subset is T(S, d) = { a' : ∃ a ∈ S, d ∈ D_i(a, a') }. This is a deterministic function. So for a fixed a_0, we can define a DP where the state is the DFA state (one of 3 possibilities). For each i, we know the transition for each possible d. But to count the number of paths, we need to know the number of ways to reach each DFA state. However, different d can lead to the same next state, but they are different strings. So we need to count the number of distinct strings, which is the number of paths. Since the DFA is deterministic, each path corresponds to a unique string. So the number of strings from a_0 is exactly the number of paths of length N in this DFA from {a_0} to any state containing a_0. But wait: the DFA transition is defined for each symbol d. The number of paths is the sum over all d of the number of paths to the next state. So if we let dp[i][S] be the number of strings of length i that lead to DFA state S, then dp[0][{a_0}] = 1. For each i, we update dp[i+1][T] += sum_{d: T(S,d)=T} dp[i][S]. But this is just the number of paths in a graph where the edges are labeled by d. The number of distinct strings is the number of paths. So we can compute it by a simple DP over the 3 states! Because the transition for a given d is deterministic, the number of paths from S to T via d is 1 if d is a valid symbol, else 0. So dp[i+1][T] = sum_{S} (number of d such that T(S,d)=T) * dp[i][S]. But the number of d such that T(S,d)=T is the number of d that cause the transition. This depends on S and i. So we can precompute for each S and each possible T, the number of d that map S to T at position i. Since the set of possible d is small (at most 4 values), we can compute this number easily. Then the DP is O(N * 3 * 3) = O(N). This gives the number of strings from a_0 that end in a state containing a_0. But we need the union over a_0. So we would compute the number of paths from {0} to states containing 0, and from {1} to states containing 1. However, a string could be generated from both a_0=0 and a_0=1. We need to avoid double-counting. How can we compute the union? We can use inclusion-exclusion by also computing the number of strings generated from both. A string is generated from both if it can be generated by a cycle starting at 0 and by a cycle starting at 1. This means there is a path from 0 to 0 and from 1 to 1. In the DFA from the set {0,1} as the start state, the state after reading the string is the set of all a reachable from {0,1}. For the string to be in the intersection, we need that 0 is reachable from 0 and 1 is reachable from 1. This means that in the DFA starting from {0,1}, the final state S must have the property that 0 is reachable from 0 and 1 is reachable from 1. But if we start from {0,1}, the reachable set S is the set of a such that there is a path from some start state to a. For 0 to be reachable from 0, we need that the path from 0 to 0 exists. This is not equivalent to 0 ∈ S; it could be that 0 is reached from 1. So we need to track more information. We can track the set of possible (start, current) pairs. Since there are 2 start states and 2 current states, there are 4 possible pairs. The subset construction on the NFA with a distinguished start state gives a DFA with 4 states (the possible subsets of {0,1} but with the start state fixed? Actually, the standard subset construction for an NFA with multiple start states gives a DFA whose state is the set of NFA states reachable. The start state is the set of start states. The accepting condition is that the intersection of the current state with the set of start states is nonempty? No, for the NFA, a string is accepted if there is a path from some start state to some accepting state. Here, we want strings that have a path from 0 to 0 or from 1 to 1. So the accepting states are those that contain 0 (for the 0->0 path) or contain 1 (for the 1->1 path). But we want the union of the two languages. We can compute the number of distinct strings by building a DFA for the union. Since the NFA has 2 states, the subset construction gives a DFA with at most 4 states. The start state is {0,1}. The accepting states are those that contain 0 or 1. But wait, the condition for a string to be in L_0 is that there is a path from 0 to 0. In the DFA from {0,1}, the state S is the set of states reachable from some start state. If 0 ∈ S, it means there is a path from some start state to 0. It could be from 1. So 0 ∈ S does not guarantee a path from 0 to 0. So the accepting condition is not simply S containing 0. We need to know if the path specifically starts at 0. To capture this, we need to track for each state, which start states can reach it. This is exactly the "reachable pairs" approach. The state in the DFA is the set of pairs (a_0, a) such that there is a path from a_0 to a. There are 2 choices for a_0 and 2 for a, so 4 possible pairs. So the DFA has at most 4 states. The start state is {(0,0), (1,1)}? Actually, initially, a_0 is the start, and we are at a_0, so the reachable pairs are (0,0) and (1,1). So the start state is {(0,0), (1,1)}. The accepting condition for a cycle is that the pair (0,0) is in the final state (for a cycle starting at 0) or (1,1) is in the final state. So the accepting states are those containing (0,0) or (1,1). This DFA has 4 states. The transitions: from a set of pairs P, on symbol d, the next set P' is the set of (a_0, a') such that there exists (a_0, a) ∈ P and d ∈ D_i(a, a'). This is deterministic given d. So we can do a DP on the 4 states! This will give the exact number of distinct strings of length N that are accepted (i.e., have a cycle). And the number of distinct strings is exactly the number of paths in this DFA from the start state to an accepting state, because the DFA is deterministic. So we can compute it in O(N * 4 * 4) = O(16N) time! This is perfect.
    # Let's formalize this. The NFA has states 0 and 1. For each position i, the transition from a to a' produces a set of d values D_i(a, a'). We want to count the number of distinct strings d_0...d_{N-1} such that there exists a_0 with a_N = a_0 and d_i ∈ D_i(a_{i-1}, a_i). 
    # We can model this as a DFA whose states are subsets of {(a_0, a) | a_0, a ∈ {0,1}}. There are 4 possible pairs: (0,0), (0,1), (1,0), (1,1). Let's denote them as 0=(0,0), 1=(0,1), 2=(1,0), 3=(1,1). The start state is {0, 3} (since initially a = a_0, so pairs are (0,0) and (1,1)). The accepting states are those that contain 0 (for cycle at 0) or 3 (for cycle at 1). So accepting states are any state that contains 0 or 3.
    # The transition: from a set of pairs P, on symbol d, the next set P' is computed as follows: for each pair (a_0, a) in P, and for each a' such that d ∈ D_i(a, a'), we add (a_0, a') to P'. This is a deterministic transition for a given d. So the number of distinct strings is the number of paths of length N in this DFA from start state to an accepting state. Since the DFA is deterministic, each path corresponds to a unique string, and every valid string corresponds to a path. So the number of valid strings is exactly the number of paths.
    # To count the number of paths, we can do a DP: let dp[i][P] be the number of strings of length i that lead to state P. dp[0][{0,3}] = 1. For each i, we update dp[i+1][P'] += sum_{d} dp[i][P] for all P and d such that δ(P, d) = P'. But we don't need to sum over d individually; we can precompute for each P and each possible P' the number of d that cause the transition. Since the number of possible d is small (at most 4), we can compute this number. Then the update is dp[i+1][P'] += count(P, P', i) * dp[i][P], where count(P, P', i) is the number of d such that δ_i(P, d) = P'. This count depends on i because D_i depends on s_i.
    # This DP runs in O(N * 4 * 4) = O(16N) time, which is O(N) for N up to 10^6. Perfect!
    # Let's compute D_i(a, a') for each i and each (a, a').
    # s_i = 0: D_i(a, a') = {1 + a - a'}.
        # a=0, a'=0: d=1
        # a=0, a'=1: d=0
        # a=1, a'=0: d=2
        # a=1, a'=1: d=1
    # s_i = 1: D_i(a, a') = {1 + a - a', 2 + a - a'}.
        # a=0, a'=0: d=1,2
        # a=0, a'=1: d=0,1
        # a=1, a'=0: d=2,3
        # a=1, a'=1: d=1,2
    # Now, for a given state P (a set of pairs), we want to compute for each d what the next state is. Since d can be 0,1,2,3, we can precompute the transition matrix for each i.
    # However, the state space is 2^4 = 16 possible subsets of pairs. But many subsets may be unreachable. We can just iterate over all 16 states, or we can use a dictionary. Since 16 is small, we can just use an array of size 16.
    # We can encode each state P as a bitmask of 4 bits. The pairs are: 0:(0,0), 1:(0,1), 2:(1,0), 3:(1,1). Start state: bit 0 and bit 3 set -> mask 0b1001 = 9.
    # Accepting: any state with bit 0 or bit 3 set.
    # Transition: for a given mask, and a given d, the next mask is computed by: for each pair (a0, a) in the mask, and for each a' in {0,1} such that d ∈ D_i(a, a'), set the bit for (a0, a') in the next mask.
    # Since the number of d is small, we can for each i and each mask precompute the next mask for each d. Then for each d, we have a transition. The number of paths is the number of sequences of d's. But to do the DP, we need to sum over d. So we can precompute for each mask and each next mask, the number of d that lead to that next mask. Let's call this count trans[i][mask][next_mask]. Then the DP is: new_dp[next_mask] += trans[i][mask][next_mask] * dp[mask].
    # Since the masks are 16, we can do this with nested loops.
    # Complexity: for each i (up to 10^6), we compute trans for 16 masks. For each mask, we iterate over the 4 possible d, compute the next mask, and increment a counter. So per i, we do 16*4 = 64 operations. Total O(64N) = O(N). This is very fast.
    # We need to be careful with the modulo. The answer is the sum of dp[N][mask] for all accepting masks.
    # Let's verify with the sample. N=3, s=010. k=1. Let's compute manually? We'll trust the algorithm.
    # Let's test with small N to ensure correctness.
    
    # First, define the pairs and bitmasks.
    # pairs: idx 0: (0,0), 1: (0,1), 2: (1,0), 3: (1,1)
    # start_mask = 1<<0 | 1<<3 = 1 + 8 = 9
    # accept: mask & (1<<0) or mask & (1<<3) != 0
    
    # For each i, we have s_i. We precompute trans[i] as a 16x16 integer matrix (mod MOD). But storing 16x16 per i for N=10^6 is 256M integers, too much. Instead, we can compute the transitions on the fly: for each i, given s_i, we compute the transition for each d. But we can precompute the transition for s_i=0 and s_i=1, and then apply them. Since the transition only depends on s_i, we can have two 16x16 matrices: T0 and T1, where T_s[mask][next_mask] is the number of d that lead from mask to next_mask. Then the DP is: new_dp = T_{s_i} * dp (matrix multiplication). Since the matrices are 16x16, we can do this in O(16^2) per step, which is 256 per step, still O(N). But we can do better: since the transition is deterministic for each d, and there are only 4 d's, the matrix is very sparse. We can just for each mask, iterate over the 4 d's, compute next mask, and add to a temporary array. That's 16*4 = 64 operations per step, which is even better.
    
    # Let's write the code.
    
    # Precompute for each s (0 or 1) and each (a, a') the set of d's.
    # D[a][a'] for s=0: [1,0,2,1] for (0,0),(0,1),(1,0),(1,1)
    # For s=1: [1,2,0,1,2,3,1,2] etc.
    
    # We'll compute for each mask (0..15) and each d (0..3) the next mask.
    # But the next mask depends on s_i. So we can precompute next_mask0[mask][d] and next_mask1[mask][d].
    # Then for each i, we do: for each mask, for each d, next = next_mask_{s_i}[mask][d], and then trans[next] += dp[mask]. But we can combine d's: for each mask, we want to add dp[mask] to the counts of the next masks, weighted by the number of d that lead to them. Since d is just a way to produce a string, each d is a distinct string. So we should count each d separately. So we can do: for each mask, for each d, next = next_mask_{s_i}[mask][d], new_dp[next] += dp[mask]. This is O(16*4) = 64 per step.
    
    # Let's implement this.
    
    # Precompute next_mask for s=0 and s=1.
    # For each mask in 0..15:
    #   For each d in 0..3:
    #     next_mask = 0
    #     For each bit b in 0..3:
    #       if mask & (1<<b):
    #         a0 = b // 2? Actually, we need to map b to (a0, a).
    #         Let's define: b=0: a0=0, a=0
    #         b=1: a0=0, a=1
    #         b=2: a0=1, a=0
    #         b=3: a0=1, a=1
    #         Then for each a' in {0,1}:
    #           if d in D_i(a, a'):
    #             find b' for (a0, a')
    #             set bit b' in next_mask.
    #     Store next_mask.
    
    # Note: D_i(a, a') is a set. We can represent it as a boolean array or check membership.
    # For s=0: D0 = {0: {0:1}, 1: {0:0,1:1}, 2: {0:1,1:2}, 3: {0:1,1:1}}? Let's make a table.
    # a=0, a'=0: d=1
    # a=0, a'=1: d=0
    # a=1, a'=0: d=2
    # a=1, a'=1: d=1
    # For s=1:
    # a=0, a'=0: d=1,2
    # a=0, a'=1: d=0,1
    # a=1, a'=0: d=2,3
    # a=1, a'=1: d=1,2
    
    # We can precompute for each (a, a') the list of d's.
    # Then for each mask and d, compute next_mask.
    
    # Since N up to 10^6, we need to be efficient. The precomputation is done once.
    
    # Let's code it.
    
    # Mapping from (a0, a) to bit: 
    # a0=0,a=0 -> 0
    # a0=0,a=1 -> 1
    # a0=1,a=0 -> 2
    # a0=1,a=1 -> 3
    # So bit = a0*2 + a? Actually: 0*2+0=0, 0*2+1=1, 1*2+0=2, 1*2+1=3. Yes.
    
    # Precompute D0 and D1 as a 2x2 list of sets.
    D0 = [[set(), set()], [set(), set()]]
    D0[0][0] = {1}
    D0[0][1] = {0}
    D0[1][0] = {2}
    D0[1][1] = {1}
    D1 = [[set(), set()], [set(), set()]]
    D1[0][0] = {1,2}
    D1[0][1] = {0,1}
    D1[1][0] = {2,3}
    D1[1][1] = {1,2}
    
    # Precompute next_mask0[mask][d] and next_mask1[mask][d]
    # masks: 0..15
    # d: 0..3
    next_mask0 = [[0]*4 for _ in range(16)]
    next_mask1 = [[0]*4 for _ in range(16)]
    
    for mask in range(16):
        for d in range(4):
            # s=0
            nm = 0
            for b in range(4):
                if mask & (1 << b):
                    a0 = b >> 1
                    a = b & 1
                    for a_prime in (0,1):
                        if d in D0[a][a_prime]:
                            b_prime = a0*2 + a_prime
                            nm |= 1 << b_prime
            next_mask0[mask][d] = nm
            # s=1
            nm = 0
            for b in range(4):
                if mask & (1 << b):
                    a0 = b >> 1
                    a = b & 1
                    for a_prime in (0,1):
                        if d in D1[a][a_prime]:
                            b_prime = a0*2 + a_prime
                            nm |= 1 << b_prime
            next_mask1[mask][d] = nm
    
    # Now DP
    dp = [0]*16
    start_mask = 1<<0 | 1<<3  # (0,0) and (1,1)
    dp[start_mask] = 1
    
    for i in range(N):
        s_i = int(s[i])
        new_dp = [0]*16
        if s_i == 0:
            nxt = next_mask0
        else:
            nxt = next_mask1
        for mask in range(16):
            if dp[mask] == 0:
                continue
            val = dp[mask]
            for d in range(4):
                nm = nxt[mask][d]
                new_dp[nm] = (new_dp[nm] + val) % MOD
        dp = new_dp
    
    # Sum over accepting masks: those with bit 0 or bit 3 set.
    ans = 0
    for mask in range(16):
        if (mask & (1<<0)) or (mask & (1<<3)):
            ans = (ans + dp[mask]) % MOD
    
    print(ans)

solve()