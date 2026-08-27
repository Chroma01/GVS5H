
## ideation
The problem allows global substitutions: pick x, y and replace all x in S with y. This is equivalent to building a function v from original letters to current letters, initially identity. Each operation (x→y) updates v: for all c with v(c)=x, set v(c)=y. The final string has character v(S[i]) at position i.

The reachable functions v are exactly the idempotent ones (v(v(c)) = v(c) for all c). This means the functional graph consists of stars: each component has a fixed point r (v(r)=r) and leaves L with v(l)=r. No cycles of length >1.

Given S and T, we need to find if there exists an idempotent v such that v(S[i]) = T[i]. For each letter c in S, if it appears with different targets in T, impossible. Otherwise, define t_c as the required target. We need v(c) = t_c. For idempotence, t_c must be a fixed point: if t_c appears in S, then t_{t_c} = t_c. This forbids cycles in the mapping from S letters to their T targets.

If feasible, the minimal number of operations equals the number of letters c with v(c) ≠ c, i.e., the number of leaves across all stars. Each leaf requires at least one operation, and we can achieve it with exactly that many by processing each star independently (e.g., merge each leaf directly into the root).

Sample 4 (S="abac", T="bcba") gives a 3-cycle a→b, b→c, c→a, which is not idempotent. According to the analysis, it should be impossible, yet the sample output is 4. There might be a misunderstanding: perhaps the operation is not “replace every occurrence of x in S with y” but “choose a character x in S and replace it with y” (individual replacement). But the problem statement clearly says “every occurrence”. Alternatively, sample 4 might have a different explanation. However, given the standard nature of this problem (AtCoder ABC 285 F? Actually, it's likely from AtCoder ABC 302 F or similar), the correct answer is indeed 4 for that sample. The cycle is achievable by using a temporary letter to break the cycle. For example, sequence: (a→d), (b→c), (c→a), (d→b) costs 4. Let's verify: Start "abac". 1. a→d: "dbdc". 2. b→c: "dcdc". 3. c→a: "dada". 4. d→b: "baba". That's "baba", not "bcba". Another sequence: (a→d), (b→a), (c→b), (d→c)? That gives something else. Actually, the known solution for this problem is: if there is a cycle, we can break it by introducing a new letter, but the number of operations is the number of edges in the cycle plus something. Wait, I recall the problem: the minimum number of operations is the number of connected components in a certain graph minus the number of cycles? No.

Let's re-evaluate with the possibility that we can choose any x,y, and we want to minimize operations. The standard solution for this problem (I think it's AtCoder ABC 285 F? No, 285 F is about substrings. Actually, it's AtCoder Beginner Contest 302 F? No, 302 F is "Find the Forest". Let's search memory: There's a problem called "Substitution" from AtCoder Regular Contest 108? Or maybe it's from a recent contest. The key insight: The operation allows us to redirect letters. The condition for possibility is that for each character, all occurrences in S must have the same target in T. If that holds, then the answer is N - (number of characters in S that are already correct?) No.

Wait, I remember a problem: "You are given two strings S and T. You can choose a character c and replace all occurrences of c in S with d. Find the minimum number of operations to make S equal to T." The solution: Build a graph where nodes are characters, and for each position i, if S[i] != T[i], add a directed edge from S[i] to T[i]. The condition for possibility is that this graph has no cycles of length >1 (i.e., is a forest where each tree has at most one outgoing edge per node, and roots have self-loops or no outgoing edge). If there is a cycle, we can still do it but we need to break the cycle by using an extra operation: the number of operations is the number of edges in the graph plus the number of cycles? Actually, the minimal number of operations is the number of edges in the graph that are not self-loops, plus the number of cycles? Let's test on sample 4: edges: a→b, b→c, c→a. That's 3 edges, one cycle. The answer is 4, which is 3+1. On sample 1: edges: a→b, f→k, b→c, d→b. That's 4 edges, no cycle (a→b, b→c; f→k; d→b). The answer is 4. So 4 edges, 0 cycles, total 4. On sample 2: no edges, 0. Sample 3: impossible because a has two targets. So the formula seems to be: answer = number of edges (S[i] != T[i]) + number of cycles in the directed graph. But we need to be careful: if there is a cycle, we need an extra operation to break it. For a cycle of length L, we can break it by redirecting one of the nodes to a temporary node, then redirecting the rest, then redirecting the temporary to the correct target. That adds 1 operation per cycle. So total operations = |E| + (number of cycles). But is that always minimal? What if there are multiple cycles? Each cycle needs one extra operation. But also, if a node has out-degree >1, that's impossible (since each S[i] has only one T[i], so each node has at most one outgoing edge). So the graph is a set of directed trees where each node has out-degree at most 1. The cycles are the strongly connected components of size >1. For each such cycle, we need one extra operation. However, what about a chain that leads into a cycle? That's impossible because if a node points to a node in a cycle, then the cycle is still there. But if a node points to a node in a cycle, the cycle must be broken, so that node's target is not in the cycle. Actually, if there is a cycle, any node that eventually reaches the cycle is part of the cycle's basin. But the condition for possibility: we must be able to break the cycle. The standard approach: count the number of edges (where S[i] != T[i]). If there is any cycle, we can still perform operations, but we need to use a temporary character to break the cycle. The minimum number of operations is the number of edges plus the number of cycles. But wait, in sample 4, there is one cycle of length 3, edges=3, answer=4. So that matches.

Let's test with a simple cycle of length 2: S="ab", T="ba". Edges: a→b, b→a. Cycle length 2. According to formula, answer = 2 + 1 = 3. Can we do it in 3 operations? S="ab". We need "ba". Try: 1. a→c (temp). S="cb". 2. b→a. S="ca". 3. c→b. S="ba". Yes! 3 operations. Can we do it in 2? We already argued no. So 3 is minimal. So formula holds.

What about a longer chain into a fixed point? S="ab", T="bc". Edges: a→b, b→c. No cycle. Edges=2. Answer should be 2. Can we do in 2? 1. a→b: S="bb". 2. b→c: S="cc". Yes, 2 ops. Could we do in 1? No. So 2 is minimal.

What about a chain a→b, b→c, c→c? That's 2 edges (a→b, b→c), c is fixed. Answer 2. Sequence: a→b, b→c. Works.

What about two separate components: S="ab", T="cd". Edges: a→c, b→d. No cycles. Answer 2. Sequence: a→c, b→d. 2 ops. Can we do in 1? No, because a and b are independent.

What about a node with self-loop? S="aa", T="aa". Edges=0. Answer 0.

So the minimal number of operations is exactly the number of indices i where S[i] != T[i], plus the number of cycles in the directed graph formed by edges S[i] → T[i] for S[i] != T[i]. But wait: what if there is a cycle that is not a simple cycle but part of a larger component? For example, a→b, b→a, and also c→a. That's a cycle a↔b, and c points to a. The graph has a cycle. The condition for possibility: we can break the cycle. The number of operations: edges=3 (a→b, b→a, c→a). Cycles=1. So answer=4. Can we do it in 4? Let's test: S="abc", T="bac". (a→b, b→a, c→a). S: a,b,c. T: b,a,a. Sequence: 1. a→d (temp). S="dbc". 2. b→a. S="dac". 3. d→b. S="bac". 4. c→a? Wait, we need c→a, but we already have a at position 2? Actually, after step3, S="bac": positions 0:b,1:a,2:c. We need position 2 to be a. So we need (c→a). That's a 4th operation. So total 4 operations: (a→d), (b→a), (d→b), (c→a). That's 4. Could we do better? Maybe (a→b) first? S="bbc". (b→a): "aac". (c→a): "aaa". No. (b→a): "aac". (a→b): "bbc". (c→a): "bba". No. (c→a): "aba". (a→b): "bbb". (b→a): "aaa". No. So 4 seems minimal. So formula holds.

Now, what about multiple cycles? For example, two disjoint 2-cycles: S="ab", T="ba", and also S="cd", T="dc". Combined: S="abcd", T="badc". Edges: a→b, b→a, c→d, d→c. Edges=4, cycles=2. Answer=6. Can we do in 6? We can break each cycle with one extra op. For first cycle: a→temp1, b→a, temp1→b (3 ops). For second: c→temp2, d→c, temp2→d (3 ops). Total 6. Could we share temporary? If we use the same temporary for both cycles, it might interfere. For example, use 'e' for both: 1. a→e, 2. b→a, 3. e→b, 4. c→e, 5. d→c, 6. e→d. That's 6. If we try to use the same 'e' but do it in a different order to save? Suppose we do: 1. a→e, 2. b→a, 3. c→e, 4. d→c, 5. e→b, 6. e→d? But after step5, e is b, so step6 does nothing. So we need to do e→d before e→b? Actually, we need to redirect e to both b and d? That's impossible because after redirecting e to one, it's that letter. So we need two different temporaries, or we can use one temporary but sequence it carefully: 1. a→e, 2. b→a, 3. e→b (now e is b, and a→b, b→a done). Then we need to do c→d, d→c. We could use a new temporary f, or we could reuse e? But e is now b, so we can't use e for c/d because that would turn c to b. So we need a separate temporary for the second cycle. So total 6. So formula seems correct.

But is it always exactly edges + cycles? Let's consider a cycle of length 1? That's a self-loop, no extra op. A cycle of length L requires L operations to do the cycle directly (a→b, b→c, ..., L→a) but that doesn't work because it collapses everything. Actually, to achieve a cycle, we need L+1 operations: we break the cycle by introducing a temporary, do L-1 operations to shift the others, and then redirect the temporary. More generally, for a cycle of length L, we can do it in L+1 operations. The edges in the cycle are L, so edges + 1 = L+1. So each cycle adds exactly 1 to the count.

What about a node that points to a node in a cycle? For example, a→b, b→a (cycle), and c→a. The edges are 3, cycles=1, total 4. As we saw, we can do it in 4. The edge c→a is not part of the cycle, but it points to a. In the operation sequence, after we break the cycle, we need to handle c→a. But since a is already involved, we can just do c→a at the end. So the extra op is only for the cycle itself.

Thus the problem reduces to:
- If there exists a letter c in S that has multiple distinct targets in T, output -1.
- Otherwise, construct a directed graph on the 26 letters (or only those appearing) with an edge from S[i] to T[i] whenever S[i] != T[i].
- The condition for possibility is that the graph has no node with out-degree > 1 (already guaranteed by the first check) and no node with in-degree > 1? Wait, can a node have in-degree > 1? Yes, multiple different letters can map to the same target. For example, a→b, c→b. That's fine. In-degree >1 is allowed. The only forbidden structure is a cycle of length >1. Actually, is that the only forbidden structure? What about a node that points to a node that points to another, and that other points back? That's a cycle. So any directed cycle of length >1 is forbidden. But is that sufficient? Consider a node that points to itself: fine. A chain a→b, b→c, c→c: fine. A node that points to a node that is in a cycle: that creates a cycle? If a points to b, and b is in a cycle, then the cycle exists regardless. So the condition is simply: the directed graph must be acyclic (except for self-loops). In other words, the graph is a DAG if we ignore self-loops. Since each node has out-degree at most 1, the graph is a set of trees pointing towards roots, where roots are either self-loops or nodes with no outgoing edge. But if a root has no outgoing edge, that means the letter does not appear in S? Actually, if a letter x appears in T but not in S, it has no outgoing edge. That's fine. So the condition is: there is no cycle of length >1.

If there is a cycle, we can still achieve the transformation, but we need to add one operation per cycle. The total operations = number of edges (S[i] != T[i]) + number of cycles.

But wait, is that always true? What if there are multiple cycles that share nodes? They are disjoint because each node has out-degree at most 1, so cycles are vertex-disjoint. So number of cycles is well-defined.

Let's test with a case where there is a cycle and also some trees feeding into the cycle. For example: a→b, b→a (cycle), c→a. Edges: 3, cycles: 1. Answer = 4. We already saw that works. What about a→b, b→c, c→b? That's a cycle of length 2 (b↔c) with a pointing to b. Edges: 3, cycles: 1. Answer 4. Can we do it in 4? S: a,b,c. T: b,c,b? Wait, T would be: a→b, b→c, c→b. So S="abc", T="bcb". Let's try: 1. a→d. S="dbc". 2. b→c. S="dcc". 3. d→b. S="bcc". 4. c→b. S="bbb"? No, we need "bcb". After step3: S="bcc": pos0:b,1:c,2:c. Target: b,c,b. So we need pos2: c→b. So step4: (c→b). S="bcb". Yes, 4 operations. So works.

What about a longer chain into a cycle: a→b, b→c, c→d, d→c (cycle of length 2). Edges: 4, cycles: 1. Answer 5. Likely works.

So the formula seems robust: answer = number of mismatches (edges) + number of cycles in the directed graph.

But we must be careful: what if there is a cycle but we can break it without an extra operation by using a node that is already part of the graph? For example, in a 2-cycle a↔b, can we do it in 2 operations? We already saw no. So extra op is needed.

What about a cycle of length 3: we need 4 operations. So the formula holds.

Now, is there any case where we need more than edges + cycles? Consider a node that has in-degree from many nodes, and we need to merge them. But each edge is an operation. However, we can sometimes merge multiple leaves into the root in fewer operations than the number of leaves? For example, a→c, b→c. Two edges. Can we do it in 1 operation? If we do (a→b), then a becomes b. Then (b→c) changes both a and b to c. That's 2 operations. So 2 is minimal. So each edge requires at least one operation. But could two edges be done in one operation? Only if they share the same source. But the source is S[i], which are distinct positions but could be the same letter. For example, if S has multiple a's all mapping to b, that's still one edge a→b. So the number of edges is the number of distinct pairs (S[i], T[i]) with S[i] != T[i]? Actually, the graph has at most one edge from a given letter because if S[i]=c and S[j]=c, then T[i] and T[j] must be the same (otherwise impossible). So each letter c in S has at most one outgoing edge. So the number of edges is exactly the number of letters c in S such that c != t_c. So edges = number of letters in S that need to change. Let's denote k = number of letters in S that have t_c != c. Then the minimal number of operations without cycles is exactly k. Because each such letter must be changed at least once, and we can change them independently. So answer = k + number of cycles.

But wait, is it always true that each edge requires a separate operation? What if two edges share the same target and we can do them together? For example, a→c and b→c. We need to change a to c and b to c. Can we do it in 1 operation? No, because an operation replaces all occurrences of a single source. To change both a and b to c, we need to either change a to b then b to c (2 ops), or a to c and b to c (2 ops). So 2 operations. So each edge requires at least one operation. So the number of operations is at least the number of edges. And we can achieve exactly the number of edges if there are no cycles. With cycles, we need one extra per cycle.

Thus the answer is: let E be the set of pairs (S[i], T[i]) with S[i] != T[i]. For each letter c, if it appears in S, let t_c be the unique T value. If c != t_c, we have an edge c → t_c. Let k be the number of such edges. Let c be the number of cycles in this directed graph (cycles of length > 1). Then answer = k + c? Wait, k is the number of edges, c is the number of cycles. So answer = k + c? But in sample 4, k=3, c=1, answer=4. So yes, answer = k + c. But k already includes the edges in the cycles. So answer = |E| + (# cycles).

But is it always |E| + (# cycles)? Let's test with a cycle of length 2: k=2, cycles=1, answer=3. Works. Cycle of length 1: not a cycle. So formula seems correct.

Now, we need to compute the number of cycles in the directed graph. The graph has at most 26 nodes, so we can easily find cycles. However, we must be careful: the graph may have multiple edges? No, each node has at most one outgoing edge. So we can just iterate over letters, follow edges, and detect cycles. Since N can be large, but the graph is small, we can process it.

Algorithm:
1. Read N, S, T.
2. For each letter c from 'a' to 'z', initialize a map target[c] = None.
3. For each i from 0 to N-1:
   if S[i] != T[i]:
      if target[S[i]] is None: set target[S[i]] = T[i].
      else if target[S[i]] != T[i]: conflict -> print -1.
4. If no conflict, build the graph. For each c with target[c] is not None and target[c] != c, add edge c -> target[c].
5. Count the number of edges k = number of such c.
6. Find the number of cycles in this graph. Since each node has out-degree at most 1, we can do a DFS or union-find to detect cycles. For each unvisited node, follow the edge until we either reach a node with no outgoing edge (to a letter not in S or self-loop) or a visited node. If we reach a node that is currently in the recursion stack, we found a cycle. Count it.
7. Answer = k + number_of_cycles.
8. Print answer.

Let's test with the samples:
Sample 1: S="afbfda", T="bkckbb". Pairs: a->b, f->k, b->c, d->b. All consistent. Edges: a->b, f->k, b->c, d->b. k=4. Cycles: follow a->b->c (c is not in S? c is not in S, so edge b->c points to c which has no outgoing edge. So no cycle. f->k, k no outgoing. d->b, b->c. So no cycles. Answer = 4+0=4. Correct.

Sample 2: no edges, k=0, cycles=0, answer=0.

Sample 3: a appears at pos0 and pos2, T[0]=a, T[2]=r. Conflict -> -1.

Sample 4: S="abac", T="bcba". Pairs: a->b, b->c, c->a. All consistent. Edges: a->b, b->c, c->a. k=3. Cycles: a->b->c->a is a cycle of length 3. Number of cycles = 1. Answer = 3+1=4. Correct!

So the formula works for all samples.

Now, we need to ensure that the graph detection is correct. Note that some letters may not appear in S, so they have no outgoing edge. Also, if a letter appears in S and maps to itself, it has a self-loop. We should treat self-loops as not a cycle (or as a cycle of length 1, but we don't add extra). Only cycles of length > 1 count.

Implementation details:
- Represent letters as integers 0..25.
- target array of size 26, initialized to -1.
- For each position i, let s = S[i]-'a', t = T[i]-'a'.
- If s != t:
   if target[s] == -1: target[s] = t.
   else if target[s] != t: print -1 and exit.
- After processing, for each c where target[c] != -1 and target[c] != c, we have an edge.
- Count edges k.
- Detect cycles: visited array, in_stack array (or recursion stack). For c in 0..25:
   if not visited[c]:
        start a walk. Use a map or array to track the path. Since 26 nodes, we can do a simple loop.
        current = c
        while True:
            visited[current] = True
            // we need to detect if we enter a cycle. Actually, we can use a separate array to mark nodes in the current path.
            Use a dictionary or list to store the path. When we move to next = target[current] (if target[current] != -1 and target[current] != current), check if next is in the path. If so, we found a cycle, increment cycle count. If next is already visited but not in path, then it's a tail leading to an already processed component, no new cycle.
            If next == -1 or target[next] == next or next not in the path, continue.
        Alternatively, we can use a standard DFS for cycle detection in a functional graph.

Since the graph is small (26 nodes), we can simply for each node, follow the chain and count cycles. But careful: a cycle can be entered from multiple nodes. We need to count each cycle once.

Simpler: Use an array state[26] with 0=unvisited, 1=visiting, 2=visited. For each node c, if state[c]==0, start DFS. In DFS, for node c, mark state[c]=1. Then if target[c] != -1 and target[c] != c, let d = target[c]. If state[d]==0, recurse. If state[d]==1, then we found a cycle. Increment cycle count. After processing, mark state[c]=2.

This works because each node has at most one outgoing edge, so the graph is a collection of directed trees and cycles. The DFS will find each cycle exactly once.

Let's test on sample 4: edges: a->b, b->c, c->a. Start DFS at a: state[a]=1, target[a]=b, state[b]=0 -> recurse: state[b]=1, target[b]=c, state[c]=0 -> recurse: state[c]=1, target[c]=a, state[a]=1 -> found cycle, count++. Then unwind, mark all 2. So count=1.

On a chain a->b, b->c, c has no outgoing: start a: state[a]=1, target[a]=b -> recurse: state[b]=1, target[b]=c -> recurse: state[c]=1, target[c] is -1 (or self), so no cycle. mark c=2, b=2, a=2. Count=0.

On two cycles: cycle1: a->b, b->a; cycle2: c->d, d->c. Start a: find cycle, count=1. Then start c: find cycle, count=2.

What about a node that points into a cycle: a->b, b->c, c->b. Edges: a->b, b->c, c->b. Start a: state[a]=1, target[a]=b -> recurse: state[b]=1, target[b]=c -> recurse: state[c]=1, target[c]=b, state[b]=1 -> found cycle, count=1. Mark c=2, b=2, a=2. So count=1. Good.

What about a self-loop: a->a. Start a: state[a]=1, target[a]=a. Since target[a]==a, we don't recurse. We don't count it as a cycle. That's correct.

Now, is it possible that a node has target[c] = c, but also another node points to it? That's fine.

So the algorithm is:
- Check conflicts.
- Count edges k.
- Count cycles c.
- Output k + c.

But wait, is it always k + c? Let's test with a case where there is a cycle and also a node that points to a node in the cycle, but the node in the cycle is not the root? Already covered. The extra operation is only for the cycle itself, not for the incoming edge. So k already counts the incoming edge. So total operations = k + c.

What about a case where a cycle is length 1? That is, a node with target[a] = a. That's not a cycle, it's a fixed point. We don't count it. And we don't need an extra operation for it.

What about a node that has target[c] = -1 (doesn't appear in S) and we treat it as no edge. That's fine.

Now, consider a case where there is a cycle but we can break it using a node that is not in the graph? For example, using a temporary letter that doesn't appear in S or T. That temporary letter is not part of the original graph. In our count, we don't have an edge for the temporary. The extra operation is to redirect a node to the temporary, then later redirect the temporary to the target. That adds one operation per cycle. So k + c accounts for that.

But is it always possible to achieve the transformation with k + c operations? The problem asks for the minimum number. We have a lower bound: at least k (each edge needs at least one change) and at least one per cycle (to break it). And we can achieve it with k + c. So it's minimal.

We should also consider if there are any other constraints. For example, what if a letter appears in S but we set its target to a letter that is not in S and not in T? That's fine. We can choose any letter.

One more thing: The graph might have a cycle that involves a letter that doesn't appear in S? No, if a letter doesn't appear in S, it has no outgoing edge in the graph (since we only add edges from S letters). So cycles can only consist of letters that appear in S.

Also, note that the graph is on 26 nodes, so we can easily run DFS.

Now, let's consider the case where there is a conflict. We already check that. But is there any other impossibility? For example, what if a letter in S maps to a letter that also appears in S, but that letter's target is different, creating an inconsistency? Actually, if c maps to d, and d maps to e, that's fine as long as there is no cycle. The condition is exactly that the directed graph is acyclic except for self-loops. Our cycle detection will find cycles. If there is a cycle, it's not impossible, we just need extra ops. Wait, the problem asks: "Determine whether it is possible to make S identical to T by repeating the operation below any number of times". So if there is a cycle, it is still possible! As we saw with sample 4, it is possible with 4 operations. So the only impossibility is when a letter in S has two different targets. That is the only conflict. So any other configuration is possible. The cycle detection is not for impossibility, but for counting extra operations.

Thus the algorithm is:
1. For each i, if S[i] != T[i], check that all positions with the same S[i] have the same T[i]. If not, print -1.
2. Build the mapping target for each letter that appears in S.
3. Count the number of edges k (target[c] != c and target[c] != -1).
4. Count the number of cycles in the directed graph defined by these edges.
5. Output k + number_of_cycles.

Let's test with a few custom cases.

Case: S="a", T="b". k=1, cycles=0. Answer=1. Sequence: (a→b). Works.

Case: S="ab", T="ba". k=2, cycles=1 (a→b→a). Answer=3. Sequence: (a→c), (b→a), (c→b). Works.

Case: S="abc", T="bca". k=3, cycles=1 (a→b→c→a). Answer=4. Works as in sample.

Case: S="abc", T="bcc". Edges: a→b, b→c. k=2, cycles=0. Answer=2. Sequence: (a→b), (b→c). Works.

Case: S="abc", T="abb". Edges: c→b. k=1, cycles=0. Answer=1. Sequence: (c→b). Works.

Case: S="ab", T="aa". Edges: b→a. k=1, cycles=0. Answer=1. Sequence: (b→a). Works.

Case: S="a", T="a". k=0, answer=0.

Case: S="abac", T="abac". k=0, answer=0.

Case: S="abac", T="abrc". Conflict because a maps to a and r. -1.

Case: S="ab", T="cd". Edges: a→c, b→d. k=2, cycles=0. Answer=2. Sequence: (a→c), (b→d). Works.

Case: S="a", T="b", but also S has another a mapping to b? That's fine.

Now, what about a case where a letter maps to itself but also appears as a target for another? E.g., S="ab", T="aa". b→a. a is fixed. k=1, cycles=0. Answer=1.

What about a case with a cycle of length 2 and a separate edge: S="abx", T="bay". Edges: a→b, b→a, x→y. k=3, cycles=1. Answer=4. Sequence: break cycle with temp, then x→y. Works.

Now, is there any case where we need more than k + c? Consider a cycle of length 2: a↔b. We need 3 operations. k=2, c=1, total 3. Good. What if the cycle is a→b, b→c, c→a. k=3, c=1, total 4. Good.

What about a cycle that is not a simple cycle? It's a set of cycles, each adds 1.

What about a node that points to a node in a cycle, but the cycle is length 2, and the node is also part of the cycle? That's the same.

So the formula seems solid.

Now, we need to implement the solution in Python, reading from stdin and writing to stdout.

Complexities: O(N + 26) time, O(26) space.

Let's write the code.

Steps:
- Read N (int).
- Read S (str).
- Read T (str).
- Initialize target = [-1]*26.
- For i in range(N):
   s = ord(S[i]) - ord('a')
   t = ord(T[i]) - ord('a')
   if s != t:
       if target[s] == -1:
           target[s] = t
       elif target[s] != t:
           print(-1)
           return
- Count edges: k = sum(1 for c in range(26) if target[c] != -1 and target[c] != c)
- Count cycles: Use a visited array, state array.
   state = [0]*26  # 0=unvisited, 1=visiting, 2=visited
   cycles = 0
   for c in range(26):
       if state[c] == 0:
           # iterative DFS
           stack = []
           current = c
           while True:
               if state[current] == 0:
                   state[current] = 1
                   stack.append(current)
               elif state[current] == 1:
                   # found a cycle. But careful: we need to count only cycles of length >1. If it's a self-loop, we didn't recurse, so current would be something else? Actually, in our DFS, we only follow edges if target[current] != current. So if target[current] == current, we don't recurse. So state[current] would be set to 1, but we don't go to next. So we need to handle the case where we are at a node and its target is itself. Let's structure the DFS properly.
               # Let's do a recursive function.
   Actually, recursive might hit recursion depth, but max 26, so it's fine. Let's write a recursive function.
   def dfs(c):
       if state[c] == 1:
           # found a cycle
           return 1
       if state[c] == 2:
           return 0
       state[c] = 1
       if target[c] != -1 and target[c] != c:
           d = target[c]
           if dfs(d):
               return 1
       state[c] = 2
       return 0
   But this counts every back edge as a cycle. In a functional graph, a back edge from a node to an ancestor in the recursion stack indicates a cycle. However, if we have a cycle, the first node that detects the cycle will count it, but we need to make sure we count each cycle only once. In a functional graph, when we do DFS from a node in a cycle, we will eventually hit a node whose target points back to a node in the current stack. That will return 1. We can just increment a global counter when that happens. But if we return 1 up the recursion, the ancestors will also return 1, causing multiple counts. We need to count the cycle only once. So better to use a separate visited array for cycle detection, or use the state array to mark nodes in the current path, and when we find a back edge, we find the cycle. But since each node has at most one outgoing edge, a cycle is a set of nodes that mutually point to each other. In DFS, when we are at a node and its target is in state 1, we have found a cycle. We can increment the cycle count, and then we need to mark all nodes in that cycle as state 2 to avoid recounting. But the recursion will unwind. Actually, we can just count cycles in a different way: since the graph is a set of components each containing at most one cycle, we can for each unvisited node, walk along the path until we hit a visited node or a node with no outgoing edge. Use a dictionary to track the order of nodes visited in the current walk. If we hit a node that is in the current walk, we have a cycle. Count it. Then mark all nodes in the walk as visited.

   Let's implement an iterative version to avoid recursion issues (though 26 is small, recursion is fine). But iterative is also simple.

   Approach: 
   visited = [False]*26
   cycles = 0
   for c in range(26):
       if not visited[c]:
           path = []  # list of nodes in current walk
           current = c
           while True:
               if visited[current]:
                   # already processed, no new cycle
                   break
               if current in path: (we can use a set for O(1) check)
                   # found a cycle. The cycle starts at the index where current appears in path.
                   cycles += 1
                   # mark all nodes in path as visited to avoid reprocessing
                   for node in path:
                       visited[node] = True
                   break
               # mark current as part of path
               path.append(current)
               # move to next
               nxt = target[current]
               if nxt == -1 or nxt == current:
                   # no outgoing edge or self-loop: end of path
                   for node in path:
                       visited[node] = True
                   break
               current = nxt
   This will count each cycle exactly once because once we find a cycle, we mark all nodes in the path as visited. But wait, in a cycle, when we start from any node in the cycle, the path will go around the cycle and eventually hit a node already in the path, so we detect the cycle. For example, start at a in a→b→c→a. path=[a], current=a, not visited, not in path. Append a, current=target[a]=b. path=[a,b], current=b, not in path. Append b, current=target[b]=c. path=[a,b,c], current=c, not in path. Append c, current=target[c]=a. Now current=a, which is in path. So we detect cycle, cycles+=1, mark a,b,c as visited. Then next time we encounter any of them, visited is True, so we skip.

   But what about a node that points to a node in a cycle? For example, d→a. When we start at d, path=[d], current=d, visited[d]=False, not in path. Append d, current=target[d]=a. Now current=a, not visited, not in path. Append a, current=target[a]=b. Append b, current=b... eventually we detect the cycle at a, and cycles+=1. Then we mark all nodes in path (d,a,b,c) as visited. So that's fine.

   However, we need to be careful: when we detect a cycle, we should mark all nodes in the current path as visited, including the ones that are part of the cycle and the ones that lead to it. That way, we don't process them again. In the example, path=[d,a,b,c], and we detect cycle when current=a (which is in path). So we mark d,a,b,c as visited. Good.

   But what if the path is longer? It's fine.

   So the iterative approach with a set for the path is simple. Since the graph is tiny, we can even use a list and search, but set is easier.

   Let's code:
   visited = [False]*26
   cycles = 0
   for c in range(26):
       if not visited[c]:
           path_set = set()
           path_list = [] # to keep order for marking
           cur = c
           while True:
               if visited[cur]:
                   break
               if cur in path_set:
                   cycles += 1
                   for node in path_list:
                       visited[node] = True
                   break
               path_set.add(cur)
               path_list.append(cur)
               nxt = target[cur]
               if nxt == -1 or nxt == cur:
                   for node in path_list:
                       visited[node] = True
                   break
               cur = nxt
   Note: We must be careful that when we break due to visited[cur], we don't mark the path as visited, but the path nodes are not yet marked. However, if we break because visited[cur] is True, it means we have already processed that node and its component, so the current path leads into a known component. We don't need to mark the current path nodes because they are part of a tree leading to a visited node. But wait, if we don't mark them, they will remain unvisited, and the outer loop will start a new walk from them. That would be incorrect because they are already reachable from a visited node, but they might not be visited themselves. For example, consider a chain d→a, where a is part of a cycle. When we start at d, we walk to a, then around the cycle, detect cycle, and mark d,a,b,c as visited. So they are marked. If we start at a first, we detect the cycle and mark a,b,c. Then later start at d, we walk d→a, but a is visited, so we break without marking d. Then d remains unvisited. That's a problem because d is part of the same component. So we need to ensure that when we break due to visited[cur], we still mark the nodes in the current path as visited. Because they are part of a tree feeding into a visited component. So we should mark them. Let's adjust:

   while True:
       if visited[cur]:
           for node in path_list:
               visited[node] = True
           break
       if cur in path_set:
           cycles += 1
           for node in path_list:
               visited[node] = True
           break
       path_set.add(cur)
       path_list.append(cur)
       nxt = target[cur]
       if nxt == -1 or nxt == cur:
           for node in path_list:
               visited[node] = True
           break
       cur = nxt

   This ensures that all nodes traversed are marked visited.

   Let's test with d→a, a→b, b→a.
   Start c=3 (d). visited[3]=False. path_list=[3], path_set={3}, cur=3. nxt=target[3]=0 (a). cur=0.
   Loop: visited[0]=False, not in path_set. path_list=[3,0], path_set={3,0}, cur=0. nxt=target[0]=1 (b). cur=1.
   Loop: visited[1]=False, not in path_set. path_list=[3,0,1], path_set={3,0,1}, cur=1. nxt=target[1]=0 (a). cur=0.
   Loop: visited[0]=False, but 0 is in path_set. So cycles+=1, mark all: visited[3]=True, visited[0]=True, visited[1]=True. Good.
   Then later, when c=0, visited[0]=True, skip.
   c=1, visited[1]=True, skip.
   c=3, visited[3]=True, skip.

   Works.

   Now, what about a node that points to itself? target[c]=c. When we start at c, path_list=[c], path_set={c}, cur=c. nxt=target[c]=c. Since nxt==cur, we break and mark c as visited. No cycle counted. Correct.

   What about a node that has no outgoing edge (target[c] = -1)? When we start at c, path_list=[c], path_set={c}, cur=c. nxt=-1. So we break and mark c. Correct.

   So this works.

   Finally, answer = k + cycles.

   Let's test with sample 4 using this code logic:
   target: a->b, b->c, c->a. k=3.
   visited all False.
   c=0 (a): path_list=[0], path_set={0}, cur=0. nxt=1. cur=1.
   c=1: visited[1]=False, not in path_set. path_list=[0,1], path_set={0,1}, cur=1. nxt=2. cur=2.
   c=2: visited[2]=False, not in path_set. path_list=[0,1,2], path_set={0,1,2}, cur=2. nxt=0. cur=0.
   c=0: visited[0]=False, 0 in path_set. cycles+=1, mark all visited[0,1,2]=True.
   Then other letters: no edges, so target=-1, they will be marked visited with no cycle.
   cycles=1, k=3, answer=4.

   Perfect.

   One more test: S="abac", T="abac". No edges, k=0. For each c, target=-1, so when we start, path_list=[c], nxt=-1, mark visited. No cycles. Answer=0.

   Another test: S="ab", T="aa". target[b]=a. k=1. b points to a. a has no edge. Start at a (index 0): path_list=[0], nxt=-1, mark visited. Start at b (index 1): path_list=[1], nxt=0, cur=0. visited[0]=True, so mark 1 visited. No cycle. cycles=0. Answer=1.

   Another test: S="ab", T="ba". target[a]=b, target[b]=a. k=2. Start at a: path_list=[0], nxt=1, cur=1. path_list=[0,1], nxt=0, cur=0. 0 in path_set, cycles+=1, mark both visited. Answer=2+1=3.

   So the algorithm is correct.

   Now, we need to write the code in the required format.

   Let's write the solve() function.

   Edge cases: N can be up to 2e5, but the graph is only 26 nodes. The strings are of length N. We need to ensure we process them efficiently.

   Potential pitfalls: 
   - We must handle the case where a letter appears in S but never with a different T (i.e., always S[i]=T[i]). Then target[s] remains -1. That's fine.
   - We must ensure that we only add an edge if s != t. Because if s==t, no operation needed for that position.
   - The graph only includes letters that appear in S and have a different target.

   Complexity: O(N + 26^2) worst-case, but essentially O(N).

   Let's code accordingly.

   We'll also include a main guard.

   Now, the problem statement says: "Enclose your code within delimiters as follows. Ensure that when the python program runs, it reads the inputs, runs the algorithm and writes output to STDOUT." So we should provide the code in a block.

   Let's write the final code.</mm:think>### NOTES
The operation is a global substitution: picking `x, y` replaces all `x` in `S` with `y`. This is equivalent to building a function `v` from the 26 letters to themselves (initially identity) where each operation `(x→y)` updates `v` by setting `v(z) = y` for all `z` with `v(z) = x`. The final string has `v(S[i])` at position `i`.  
Reachable functions `v` are exactly the **idempotent** ones: `v(v(c)) = v(c)` for all `c`. This means the functional graph consists of stars: each component has a fixed point root `r` (with `v(r)=r`) and leaves `L` mapping directly to `r`. No directed cycles of length >1 appear in an idempotent function.  

However, a cycle in the desired mapping (e.g. `a→b, b→c, c→a`) is not a valid `v`, but it can still be achieved by spending one extra operation to break the cycle using a temporary letter. Thus the problem is always possible unless a letter in `S` is required to become two different letters in `T`.  

**Feasibility:** For every letter `c` appearing in `S`, all positions where `S[i]=c` must have the same `T[i]`. If not, output `-1`.  

**Minimum operations:**  
- Count `k` = number of letters `c` in `S` with required target `t_c ≠ c`. Each such letter needs at least one operation.  
- Count `c` = number of directed cycles of length >1 in the graph formed by edges `c → t_c` (ignoring self-loops). Each cycle requires one extra operation to break.  
- Answer = `k + c`.  

The graph has at most 26 nodes, so we can detect cycles with a simple DFS/walk.

## worker: Omit next step since solution is complete.
The solution works by first checking that each letter in `S` consistently maps to at most one target in `T`. If any letter has conflicting targets, output `-1`.  
Otherwise, we build a directed graph where an edge `c → target[c]` exists if `c` must change. The number of such edges is `k`.  
We then count how many directed cycles of length >1 exist in this graph. Each such cycle requires one extra operation to break (by using a temporary letter), so the total minimum operations is `k + cycles`.  
The graph has only 26 nodes, so cycle detection is trivial using a walk with a set to track the current path.
