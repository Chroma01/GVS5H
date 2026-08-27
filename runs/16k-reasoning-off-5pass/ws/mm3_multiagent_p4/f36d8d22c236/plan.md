We need to determine if we can transform string S into T using operations that replace all occurrences of a chosen letter x with another letter y. This is essentially a mapping problem: we can think of a directed graph of letters where an edge x→y means we have applied the operation replacing x with y. Since we can apply multiple operations, the final mapping from each letter in S to its target in T must be consistent (no letter maps to two different targets). If any letter in S maps to two different letters in T, it's impossible.

If possible, we need to find the minimum number of operations. The key observation: if a letter x already maps to itself (i.e., all occurrences of x in S correspond to x in T), we don't need to perform any operation involving x as the source. However, if x maps to y ≠ x, we need at least one operation to change x to y. But we can chain operations: if x→y and y→z, we can do x→y then y→z, or directly x→z. The minimum number of operations is related to the structure of the mapping graph.

We can model the mapping as a functional graph on 26 letters. Each letter maps to at most one target. The graph consists of several connected components, each containing exactly one cycle (possibly a self-loop). For a component:
- If the cycle is a self-loop (letter maps to itself), then all letters in the component that map to this self-loop can be handled in a chain. The minimum operations for such a component is (number of letters in component) - 1, because we can chain them: map the farthest letter to the next, etc., ending at the self-loop.
- If the cycle has length > 1 (a cycle of distinct letters), then we need to break the cycle. Since we cannot have a cycle of replacements (that would be infinite), we must perform an operation that maps some letter in the cycle to a letter outside the cycle (or to itself, but that's not possible if it's a cycle). Actually, if we have a cycle x→y→...→x, we need to perform an operation that maps one of these letters to a different letter (possibly itself, but that would break the cycle). The minimum operations for a cycle of length L is L + 1: we need to map each letter in the cycle to the next (L operations) plus one extra operation to map the last letter to itself or to some letter outside? Wait, let's think carefully.

Actually, the standard solution for this problem (from AtCoder ABC 285 E or similar) is:
- Build the mapping from S to T: for each position i, if S[i] ≠ T[i], we need to map S[i] to T[i]. But we can only map one letter to one other letter. So we check if the mapping is consistent: for each letter c, all positions where S[i]=c must have the same T[i]. If not, impossible.
- If consistent, we have a partial function f: letters → letters. Some letters may not appear in S, or may map to themselves.
- We need to find the minimum number of operations to achieve this mapping. The operations can be seen as building a directed graph where we apply edges. The final state is that for each letter c, all occurrences of c in S become f(c). We can perform operations in any order.

The optimal strategy: For each connected component in the mapping graph (considering only letters that appear in S or are targets), we need to determine the minimum operations. The mapping graph is a collection of trees feeding into cycles. Since each letter has at most one outgoing edge, each component has exactly one cycle.

Case 1: The cycle is a self-loop (c → c). Then we have a tree rooted at c. We can process the tree from leaves to root: each leaf maps to its parent, etc. The number of operations is (number of nodes in component) - 1.

Case 2: The cycle has length ≥ 2. Then we have a cycle with trees attached. We need to break the cycle. The optimal way: we can map one letter in the cycle to some other letter (possibly itself, but that would require an operation that maps it to itself? Actually, we can map a letter to itself, but that doesn't change anything. However, if we map a letter in the cycle to a letter outside the cycle, we break the cycle. But we need to ensure all letters in the cycle get mapped correctly. The standard approach: we can map all letters in the cycle to the next one in the cycle (L operations), and then we need one extra operation to map the last one to itself or to something else? Actually, if we have a cycle a→b→c→a, we can do: a→b, b→c, c→a. But after these three operations, a becomes b, b becomes c, c becomes a. That's not what we want. We want a to become b, b to become c, c to become a. Wait, that's exactly the mapping: a→b, b→c, c→a. But if we perform these operations in sequence: first replace a with b: now all a's become b's. Then replace b with c: now all b's (including those that were originally a) become c's. Then replace c with a: now all c's (including those that were originally b) become a's. So after these three operations, original a's become c, original b's become a, original c's become b. That's not the intended mapping.

We need to achieve the mapping f. The operations are applied sequentially, and each operation replaces all occurrences of x with y at that moment. So the order matters. The standard solution for this problem (which is AtCoder ABC 285 E? Actually it's ABC 285 D? Let me recall: it's "Replace by MEX" or something? Actually it's "Replace by Letters" or similar. I think it's from AtCoder ABC 285 F? No.

Wait, I recall a problem: "Determine if it is possible to make S identical to T by repeatedly choosing two lowercase English letters x, y and replacing every occurrence of x in S with y." This is exactly AtCoder ABC 285 E? Actually ABC 285 E is about something else. Let me search memory: This is AtCoder ABC 285 D? No, ABC 285 D is "Change Usernames". Actually, this is AtCoder ABC 285 F? No.

I think it's AtCoder ABC 285 E? Wait, ABC 285 E is "Avoiding Collision". Not that.

Actually, this is AtCoder ABC 285 D? Let me check: ABC 285 D is "Change Usernames". The problem statement: "You are given a positive integer N and two strings S and T, each of length N and consisting of lowercase English letters. Determine whether it is possible to make S identical to T by repeating the operation below any number of times (possibly zero). If it is possible, also find the minimum number of operations required." Yes, that's ABC 285 D.

The solution for ABC 285 D:
- Build the mapping from S to T. For each letter c, if there exists i such that S[i]=c and T[i]≠c, then we need to map c to T[i]. But we must ensure that for a given c, all T[i] are the same. If not, impossible.
- If possible, we have a directed graph on 26 letters where each node has out-degree at most 1. The graph consists of several connected components, each containing exactly one cycle.
- For each component, if the cycle is a self-loop (c→c), then the minimum operations is (number of nodes in component) - 1.
- If the cycle has length ≥ 2, then the minimum operations is (number of nodes in component) + 1. Why? Because we need to break the cycle. We can do this by mapping one of the letters in the cycle to some other letter (preferably one that is already in the component or outside) and then process the trees. Actually, the standard answer: for a cycle of length L with trees attached, the minimum operations is (total nodes in component) + 1. Because we need to perform L operations to map each letter in the cycle to the next, and then one extra operation to map the last one to itself? Wait, let's derive.

Consider a simple cycle a→b, b→a. We want to achieve: all a's become b's, all b's become a's. Can we do it in 2 operations? Let's try: first replace a with b: now S has only b's (original a's become b, original b's remain b). Then replace b with a: now all become a. That's not right. We want original a's to become b, original b's to become a. So we need: after operations, original a's are b, original b's are a. If we do: first replace b with a: original b's become a, original a's remain a. Then replace a with b: all become b. That's not right either.

Actually, we can do: first replace a with b: original a's become b, original b's remain b. Then replace b with a: all become a. That's wrong.

What if we do: first replace b with a: original b's become a, original a's remain a. Then replace a with b: all become b. That's also wrong.

We need a sequence that results in the swap. Is it possible? Let's think: we want to swap a and b. The operation replaces all occurrences of x with y. So if we want to swap, we need to change a to b and b to a simultaneously, but operations are sequential. So we need to do something like: first change a to some temporary c, then change b to a, then change c to b. That would be 3 operations. But we don't have a temporary letter necessarily. However, we can use any letter. So if we have a cycle of length 2, we need at least 3 operations? Let's test with letters a and b only. We want to swap. We can do: a→c (using some c not in S or T), then b→a, then c→b. That's 3 operations. But if we have other letters available, we can use them. So the minimum for a 2-cycle is 3? But the sample 4: S="abac", T="bcba". Let's analyze: S: a b a c, T: b c b a. Mapping: a→b, b→c, c→a. That's a 3-cycle. The answer is 4. So for a 3-cycle, answer is 4. That suggests for a cycle of length L, answer is L+1.

But wait, sample 1: S="afbfda", T="bkckbb". Mapping: a→b, f→k, d→b, b→c. Let's build graph: a→b, b→c, f→k, d→b. So we have: a→b→c (c is self-loop? Actually c maps to? In S, c doesn't appear, so no outgoing edge from c. But c appears in T, so it's a target. So c has no outgoing edge. So the component containing a,b,c: a→b, b→c, c has no outgoing edge. That's a chain ending at c. Since c has no outgoing edge, it's not a cycle. Actually, we need to consider only letters that appear in S. Because operations only affect letters in S. So we only care about letters that appear in S. For letters that don't appear in S, we don't need to map them. So the mapping is defined only for letters that appear in S. For each such letter, we have a target (which may be any letter). So the graph has nodes = letters that appear in S. Each node has out-degree 1 (to its target). The target may or may not be in S. If the target is not in S, then that node has no incoming edges from other nodes in S? Actually, it could have incoming edges. So the graph is a functional graph on the set of letters that appear in S. Each component has exactly one cycle (possibly a self-loop if a letter maps to itself). But if a letter maps to a letter not in S, then that target is not a node in the graph, so the chain ends. So the cycle can only be among letters that appear in S. So if a letter maps to a letter not in S, that letter is a sink (no outgoing edge in the graph of S-letters). So the component is a tree rooted at that sink? Actually, if a letter maps to a letter not in S, then that letter is not in the graph, so the edge goes out of the graph. So the component is a tree with a root that has an edge to outside. But since we only care about operations on letters in S, we can think of the target as a sink. So the component is a directed tree where each node has out-degree 1, and the root has out-degree 1 but points to a letter not in S. So there is no cycle. In that case, the minimum operations is the number of nodes in the component. Because we can process from leaves to root: each leaf maps to its parent, etc., until the root maps to its target (which is not in S, so we don't need to worry about it). Actually, we need to map the root to its target as well. So if the root maps to a letter not in S, we still need to perform an operation to replace the root with that target. So the number of operations is the number of nodes in the component. For example, in sample 1: a→b, b→c, f→k, d→b. Letters in S: a,b,f,d. Targets: b,c,k,b. b is in S, c is not, k is not. So component1: a→b→c. Here a and b are in S, c is not. So nodes: a,b. That's 2 nodes. We need to map a to b and b to c. We can do: first b→c, then a→b. That's 2 operations. Component2: f→k. f is in S, k is not. So 1 node, 1 operation. Component3: d→b. d is in S, b is in S. But b is already in component1. So actually d→b means d is in the same component as a and b? Because b is in S. So the graph is: a→b, b→c (c not in S), d→b. So nodes: a,b,d. That's 3 nodes. We need to map a→b, b→c, d→b. We can do: first b→c, then a→b, then d→b. That's 3 operations. But the answer is 4. So my count is off by 1. Let's recalculate: The operations in sample 1: b→c, a→b, f→k, d→b. That's 4 operations. So for the component with a,b,d, we did 3 operations: b→c, a→b, d→b. That's 3 operations. And for f→k, 1 operation. Total 4. So my count matches: component size 3 gives 3 operations, component size 1 gives 1 operation. So the rule seems to be: for a component that is a tree (no cycle), the number of operations equals the number of nodes in the component. But wait, what about the root? In the component a,b,d, the root is b? Actually, b maps to c (not in S), so b is a root. d maps to b, a maps to b. So it's a tree with root b. We need to map b to c, and then map a and d to b. We can do b→c first, then a→b, then d→b. That's 3 operations. So number of operations = number of nodes.

But what if there is a cycle? Consider a cycle among letters in S. For example, a→b, b→a. Both in S. That's a 2-cycle. How many operations? We need to map a to b and b to a. As argued, we need at least 3 operations: we can use a temporary letter c (not in S) to break the cycle: a→c, b→a, c→b. That's 3 operations. So for a cycle of length L, we need L+1 operations? For L=2, that's 3. For L=3, that's 4. Sample 4 has a 3-cycle and answer 4. So that matches.

But what if the cycle has trees attached? For example, a→b, b→c, c→a, and d→a. Then the component has nodes a,b,c,d. The cycle is a,b,c. We need to map a→b, b→c, c→a, d→a. We can do: first break the cycle by mapping one of them to a temporary, but we can also use the tree to help. The optimal way: we can map d→a first? But that doesn't break the cycle. Actually, we need to map all letters in the cycle to their targets. Since the cycle is a→b→c→a, we need to achieve that. One method: map a→b, b→c, c→a. But as we saw, that doesn't work because after a→b, a's become b, then b→c makes b's become c, then c→a makes c's become a. So original a's become c, original b's become a, original c's become b. That's the reverse cycle. So we need to do it in reverse order? Let's think: we want original a's to become b, original b's to become c, original c's to become a. If we do: first c→a: original c's become a, original a's remain a, original b's remain b. Then a→b: all a's (including original c's) become b. Then b→c: all b's (including original a's and original c's) become c. So after these three operations, original a's become c, original b's become c? Wait, let's track carefully.

Start: S has a, b, c.
Operation 1: c→a. Now: original c's become a. So now we have: original a's (a), original b's (b), original c's (a). So letters: a, b, a.
Operation 2: a→b. Now: all a's become b. So original a's become b, original c's become b. So now we have: original a's (b), original b's (b), original c's (b). All b.
Operation 3: b→c. Now: all b's become c. So all become c. That's not right.

We want original a's to become b, original b's to become c, original c's to become a. So we need a different order. What if we do: first a→b: original a's become b. Now: original a's (b), original b's (b), original c's (c). Then b→c: all b's become c. Now: original a's (c), original b's (c), original c's (c). Then c→a: all c's become a. All become a. Not right.

What if we do: first b→c: original b's become c. Now: original a's (a), original b's (c), original c's (c). Then c→a: all c's become a. Now: original a's (a), original b's (a), original c's (a). Then a→b: all a's become b. All become b. Not right.

So three operations on the cycle alone cannot achieve the mapping. We need an extra operation. The standard solution is to use a letter outside the cycle (or a self-loop) to break it. For a cycle of length L, we need L+1 operations. The extra operation is to map one of the letters in the cycle to some other letter (preferably one that is already mapped correctly, like a self-loop, or a letter not in S). Then we can process the rest.

So the algorithm:
1. For each letter c that appears in S, determine its target f(c) = T[i] for some i where S[i]=c. If there are multiple different T[i] for the same c, then impossible.
2. Build the directed graph on letters that appear in S. Each node c has an edge to f(c). Note that f(c) may or may not be in S.
3. Find connected components in this graph. Since each node has out-degree 1, each component has exactly one cycle. The cycle may be a self-loop (c→c) or a longer cycle.
4. For each component, count the number of nodes (letters in S that are in the component). Let size = number of nodes.
   - If the cycle is a self-loop (i.e., there exists a node c in the component such that f(c)=c), then the minimum operations for this component is size - 1.
   - If the cycle has length ≥ 2, then the minimum operations for this component is size + 1.
5. Sum over all components. If any inconsistency, output -1.

Why size - 1 for self-loop? Because we can chain the operations: start from the leaves, map each leaf to its parent, etc., until we reach the self-loop. The self-loop doesn't need an operation because mapping a letter to itself is not needed (or we can consider it as 0 operations). Actually, if a letter maps to itself, we don't need to perform any operation for that letter. So we can process the tree in reverse topological order: each node maps to its parent, and the root (self-loop) is already correct. So number of operations = number of non-root nodes = size - 1.

Why size + 1 for cycle? Because we need to break the cycle. We can do this by mapping one of the letters in the cycle to some other letter (preferably a letter that is already correct, like a self-loop in another component, or a letter not in S). Then the cycle becomes a chain ending at that letter. Then we can process the chain. The number of operations: we need to map each letter in the cycle to the next (L operations), plus one extra operation to map the last one to the breaking letter. But wait, that would be L+1 operations for the cycle itself. But we also have trees attached. The trees can be processed similarly: each tree node maps to its parent in the cycle. So total operations = (number of nodes in trees) + (L+1). But number of nodes in trees = size - L. So total = (size - L) + (L+1) = size + 1. So that matches.

But is it always possible to break the cycle using a letter outside the component? We need to ensure that there is at least one letter that is not in the cycle and that we can map to. Actually, we can always use a letter that is not in S at all. Since there are 26 letters and at most 26 letters in S, if the cycle uses all 26 letters, then we cannot use a letter outside S. But if the cycle uses all 26 letters, then size = 26 and L=26. Then we need 27 operations? But we only have 26 letters. However, we can map a letter in the cycle to itself? That would break the cycle? If we map a letter to itself, that doesn't change anything. But if we map a letter in the cycle to itself, then that letter becomes a self-loop, and the cycle is broken. But mapping a letter to itself is an operation that does nothing? Actually, the operation is: choose x and y, replace every occurrence of x with y. If we choose x=y, then it replaces x with x, which does nothing. So we can perform such an operation, but it counts as an operation. So we can break the cycle by mapping one letter in the cycle to itself. That would be an extra operation. So even if all letters are in the cycle, we can still do it. So the formula holds.

But wait: what if the cycle has length L and there is no letter outside the cycle that we can map to? We can always map to itself. So it's fine.

However, there is a subtlety: if we map a letter in the cycle to itself, then that letter becomes a self-loop, and the rest of the cycle becomes a chain ending at that self-loop. But then we need to process the chain. The number of operations would be: for the self-loop, we don't need to map it (since it maps to itself). For the chain, we need to map each letter to the next. So if we have a cycle a→b→c→a, and we map a→a (operation), then we have: a is self-loop, b→c, c→a. Now we need to map b→c and c→a. We can do: c→a, then b→c. That's 2 operations. Plus the initial a→a operation, total 3. But L=3, so L+1=4. That's one more. So mapping to itself doesn't save an operation. Actually, if we map a→a, we still need to map b and c. So total operations: a→a (1), c→a (1), b→c (1) = 3. But we need to achieve: a→b, b→c, c→a. After these operations: start: a,b,c. After a→a: no change. After c→a: c becomes a. Now: a,b,a. After b→c: b becomes c. Now: a,c,a. That's not correct: we want a→b, so original a should become b. But here original a remains a. So we need to map a to b as well. So we need an operation a→b. So total 4 operations. So indeed, we need L+1 operations.

But can we do better by using a letter outside the cycle? If there is a letter d not in the cycle, we can do: a→d, b→a, c→b, d→c. That's 4 operations as well. So no improvement.

So the formula size + 1 for a component with a cycle of length ≥ 2 seems correct.

Now, we need to implement this.

Steps:
- Read N, S, T.
- Initialize an array target[26] to -1.
- For each i from 0 to N-1:
   - c = S[i], d = T[i].
   - If target[c] == -1, set target[c] = d.
   - Else if target[c] != d, then impossible (output -1).
- If no inconsistency, build the graph. We only care about letters that appear in S. Let used[c] = true if c appears in S.
- For each c where used[c] is true, we have an edge from c to target[c]. Note that target[c] may not be used.
- We need to find connected components in this graph. Since the graph is directed, but we can treat it as undirected for connectivity? Actually, we need to consider the structure: each node has out-degree 1. So we can find cycles by traversing.
- We can do a DFS or use union-find? But we need to detect cycles and count component sizes.
- Since there are only 26 letters, we can simply iterate over all letters and do a traversal.
- For each unvisited letter c that is used, we can follow the edges until we reach a letter that is not used (sink) or a cycle. But we need to count the number of nodes in the component.
- Alternatively, we can build the graph as an array of 26 nodes, and do a DFS from each node, marking visited, and for each component, determine if it has a cycle and the cycle length.
- Since the graph is small (26 nodes), we can do a simple loop.

Implementation:
- Create an array next[26] = -1 for all.
- For each c in used, set next[c] = target[c].
- Now, we want to find components. We can use a visited array.
- For each c from 0 to 25:
   - If used[c] and not visited[c]:
       - Start a DFS or BFS to collect all nodes in the component. Since the graph is directed, we need to follow both forward and backward edges? Actually, to find the component, we need to consider all nodes reachable from c by following edges in either direction? But the edges are only from used nodes to their targets. So if we start from c, we can follow the edge from c to next[c]. But next[c] might not be used. If next[c] is not used, then the component is just {c}? But wait, there might be other nodes that point to c. So we need to include all nodes that can reach c or are reached from c. So we need to do a traversal that follows edges in both directions. So we can build an undirected graph: for each used node c, add an undirected edge between c and next[c] (if next[c] is used, otherwise just c is isolated? But if next[c] is not used, then no other node can point to next[c] because next[c] is not used, so no one has next[c] as their source. So the component is just {c}. But wait, there could be nodes that point to c. So if next[c] is not used, then c is a sink in the directed graph. But other nodes might point to c. So we need to include those nodes. So we need to traverse both directions.
- So we can build an adjacency list for the undirected graph: for each used node c, if next[c] is used, add edge between c and next[c]. If next[c] is not used, then c is only connected to nodes that point to it. So we need to find all nodes that point to c. So we can also build reverse edges: for each used node c, if next[c] is used, then c is a parent of next[c]? Actually, we can just do a DFS on the directed graph but following edges forward and also following reverse edges. Since the graph is small, we can do a simple recursive DFS that visits all nodes reachable by following edges in either direction.

Simpler: Since there are only 26 letters, we can just iterate over all letters and for each unvisited used letter, we can perform a BFS/DFS that explores both forward and backward edges. We can precompute reverse edges: for each used node c, we can store that c is a parent of next[c] if next[c] is used. So we can have a list of children for each node. But we need to explore both directions. So we can do: from a start node, we can go to next[c] (if used), and also go to all nodes d such that next[d] == c (i.e., nodes that point to c). So we need to know for each node, which nodes point to it. We can build an array rev[26] = list of nodes that point to this node. For each used c, if next[c] is used, add c to rev[next[c]].

Then, to find a component, we can start from an unvisited used node, and do a stack-based DFS: push the node, mark visited, then for each neighbor: if next[node] is used and not visited, push it; and for each d in rev[node], if not visited, push d. This will collect all nodes in the undirected component.

Once we have the set of nodes in the component, we need to determine if there is a cycle. Since each node has out-degree 1, the component will have exactly one cycle if we consider only the directed edges. But if the component includes nodes that point to a node not in the component? Actually, if next[c] is not used, then c has no outgoing edge to another used node. So in the undirected component, c is only connected via reverse edges. So the directed edges within the component form a functional graph. There will be exactly one cycle if the component has at least one node with next[c] in the component. If no node has next[c] in the component, then there is no cycle? But that's impossible because if there is no cycle, then following edges from any node will eventually lead to a node whose next is not in the component. But since the component is closed under reverse edges, if a node's next is not in the component, then that node is a sink. But then there must be some node that points to it, so it's in the component. So the component is a tree with a root that points outside. In that case, there is no cycle. But wait, if the root points outside, then the directed edges form a tree (each node has out-degree 1, and the root has out-degree 1 but points to a node not in the component). So there is no cycle. So the component is a tree. In that case, the cycle length is 0? Actually, we can think of the cycle as being of length 1 if the root points to itself? But if the root points to a node not in the component, then it's not a cycle. So we need to detect if there is a cycle within the component. A cycle exists if there is a node c such that following next repeatedly from c eventually returns to c, and all nodes in the cycle are in the component. Since the component is closed under reverse edges, if there is a cycle, it must be entirely within the component. So we can detect a cycle by checking if any node in the component has next[c] in the component and following the chain leads back to itself. But since the component is small, we can simply check for each node in the component, if next[c] is in the component and if following the chain from c leads to a cycle. Alternatively, we can check if there exists a node c in the component such that next[c] == c (self-loop) or if there is a cycle of length >1.

Simpler: For each component, we can count the number of nodes that have next[c] in the component. If that number is equal to the number of nodes in the component, then every node's next is in the component, so there must be a cycle (since finite). Actually, if every node's next is in the component, then the directed graph is a permutation on the component, so it consists of cycles. But since each node has out-degree 1, it could be one cycle or multiple cycles? But wait, if the component is connected in the undirected sense, and every node's next is in the component, then the directed graph is a collection of cycles that are connected? But if there are multiple cycles, they would not be connected because there are no edges between cycles (since each node has out-degree 1, and if there were an edge from one cycle to another, that would merge them). So if the component is connected, there can be only one cycle. So we can check: if for all nodes in the component, next[c] is in the component, then there is a cycle. Otherwise, there is no cycle (it's a tree).

But wait, what about a self-loop? If a node has next[c] == c, then next[c] is in the component, so it counts. So that's fine.

So algorithm for each component:
- Let nodes = list of nodes in the component.
- Let size = len(nodes).
- Check if there exists a node c in nodes such that next[c] is not in nodes. If such a node exists, then the component is a tree (no cycle). In that case, the minimum operations is size.
- If no such node exists, then every node's next is in the component, so there is a cycle. Now we need to determine if the cycle is a self-loop or longer. We can check if there exists a node c in nodes such that next[c] == c. If yes, then the cycle is a self-loop, and minimum operations is size - 1. If no, then the cycle has length ≥ 2, and minimum operations is size + 1.

But wait, in the tree case, is the minimum operations always size? Let's test with sample 1: component with a,b,d. nodes: a,b,d. next[a]=b (in component), next[b]=c (not in component), next[d]=b (in component). So there is a node (b) whose next is not in component. So it's a tree. size=3, operations=3. That matches.

What about a component that is just a single node c with next[c] = c? That's a self-loop. size=1, operations=0. That matches.

What about a component with two nodes: a→b, b→a. Both next in component. No self-loop. size=2, operations=3. That matches.

So the rules seem correct.

Now, we need to implement the component finding. Since there are only 26 letters, we can do:

- Initialize used[26] = False.
- For each character in S, mark used[ord(c)-97] = True.
- Initialize next[26] = -1.
- For each c in used, set next[c] = target[c] (where target[c] is the consistent target from T).
- Initialize visited[26] = False.
- Initialize rev[26] as empty list.
- For each c in used:
   - If next[c] is used (i.e., next[c] != -1 and used[next[c]]), then add c to rev[next[c]].
- For each c from 0 to 25:
   - If used[c] and not visited[c]:
       - Do a stack-based DFS: push c, mark visited.
       - While stack not empty:
           - pop node u.
           - Add u to component list.
           - If next[u] is used and not visited, push next[u] and mark visited.
           - For each v in rev[u], if not visited, push v and mark visited.
       - Now we have component list.
       - Compute size = len(component list).
       - Check if there exists a node u in component such that next[u] is not in component. To check if next[u] is in component, we can have a set of nodes in component.
       - If such a node exists, then operations += size.
       - Else:
           - Check if there exists a node u in component such that next[u] == u. If yes, operations += size - 1.
           - Else, operations += size + 1.

But wait: in the tree case, we said operations = size. But is that always true? Consider a tree where the root points to a letter not in S. We need to map each node to its parent. We can do a post-order traversal: for each leaf, map it to its parent. But the root also needs to be mapped to its target (which is not in S). So we need to perform an operation for the root as well. So total operations = number of nodes. That seems correct.

But what if the root points to a letter that is in S but in a different component? Then that letter is not in this component. So next[root] is not in component. So it's still a tree. So operations = size.

Now, what about the case where the component has a cycle but also has a node that points outside? That can't happen because if there is a cycle, then every node in the cycle has next in the cycle. And if a node points outside, it cannot be part of a cycle. So if there is a node that points outside, then there is no cycle. So the condition "exists a node with next not in component" is equivalent to "no cycle".

So the algorithm is sound.

Now, we need to handle the case where target[c] is not defined? Actually, for each c that appears in S, we have a target. So next[c] is always defined for used c.

One more thing: what if target[c] is the same as c? That's a self-loop. Then next[c] = c, which is in component. So it will be treated as a cycle. And since next[c] == c, it will be counted as a self-loop, so operations = size - 1. That is correct: if a letter maps to itself, we don't need to perform any operation for it. But if there are other letters mapping to it, we need to map them. So size - 1 is correct.

Now, let's test with sample 4: S="abac", T="bcba". used: a,b,c. next[a]=b, next[b]=c, next[c]=a. All next in component. No self-loop. size=3, operations=3+1=4. Correct.

Sample 2: S="abac", T="abac". used: a,b,c. next[a]=a, next[b]=b, next[c]=c. Each is a self-loop. So each component is size 1, operations 0. Total 0. Correct.

Sample 3: S="abac", T="abrc". used: a,b,c. next[a]=a (from positions 0 and 2: T[0]=a, T[2]=b? Wait, S="abac": positions: 0:a,1:b,2:a,3:c. T="abrc": 0:a,1:b,2:r,3:c. So for a: T[0]=a, T[2]=r. Conflict. So impossible. Output -1. Correct.

So the algorithm works.

Now, we need to implement it efficiently. Since N can be up to 2e5, but we only care about the mapping from letters to letters, which is at most 26 entries. So we can process in O(N + 26^2) time.

Implementation steps:

1. Read N.
2. Read S and T.
3. Initialize target array of size 26 with -1.
4. For i in range(N):
   - c = ord(S[i]) - ord('a')
   - d = ord(T[i]) - ord('a')
   - If target[c] == -1: target[c] = d
   - Else if target[c] != d: print(-1) and exit.
5. Initialize used array of size 26 with False.
6. For each character in S: used[ord(c)-97] = True.
7. Initialize next array of size 26 with -1.
8. For each c in range(26):
   - If used[c]: next[c] = target[c]
9. Initialize rev list of size 26 as empty lists.
10. For each c in range(26):
    - If used[c] and next[c] != -1 and used[next[c]]:
        - rev[next[c]].append(c)
11. Initialize visited array of size 26 with False.
12. Initialize total_ops = 0.
13. For each c in range(26):
    - If used[c] and not visited[c]:
        - component = []
        - stack = [c]
        - visited[c] = True
        - while stack:
            - u = stack.pop()
            - component.append(u)
            - v = next[u]
            - if v != -1 and used[v] and not visited[v]:
                - visited[v] = True
                - stack.append(v)
            - for w in rev[u]:
                - if not visited[w]:
                    - visited[w] = True
                    - stack.append(w)
        - size = len(component)
        - comp_set = set(component)  # or use a boolean array for component
        - has_outside = False
        - for u in component:
            - v = next[u]
            - if v == -1 or not used[v] or v not in comp_set:
                - has_outside = True
                - break
        - if has_outside:
            - total_ops += size
        - else:
            - has_self_loop = False
            - for u in component:
                - if next[u] == u:
                    - has_self_loop = True
                    - break
            - if has_self_loop:
                - total_ops += size - 1
            - else:
                - total_ops += size + 1
14. Print total_ops.

But we need to be careful: the condition "v not in comp_set" is equivalent to "v is not in the component". Since we only add used nodes to the component, and v is used if next[u] is used. So we can check: if next[u] is used and next[u] is in the component. So we can precompute a set or a boolean array for the component.

Since component size is at most 26, we can just use a list and check membership with a set.

Now, let's test with sample 1 manually:

S="afbfda", T="bkckbb"
used: a,b,f,d
target: a->b, f->k, d->b, b->c
next: a->b, b->c, f->k, d->b
rev: b: [a,d], c: [b], k: [f]
Components:
Start with a: stack: a. visited a. component: a. next[a]=b, used, not visited -> push b. rev[a] empty.
Pop b: component: a,b. next[b]=c, used, not visited -> push c. rev[b]: [a,d] -> a visited, d not visited -> push d.
Pop d: component: a,b,d. next[d]=b, used, visited. rev[d] empty.
Pop c: component: a,b,d,c. next[c]? c is used? Actually, c is not in S, so used[c] is False. So next[c] is -1. So we don't push. rev[c]: [b] -> visited.
So component: {a,b,d,c}. size=4.
Now check has_outside: for u in component:
- a: next[a]=b, b in component? yes.
- b: next[b]=c, c in component? yes.
- d: next[d]=b, b in component? yes.
- c: next[c]=-1, so outside.
So has_outside = True. So operations += 4.
But wait, we earlier said component size should be 3? Because c is not in S, so it shouldn't be in the component. But in our DFS, we included c because we followed next[b]=c, and c is used? Actually, used[c] is False because c does not appear in S. So in the DFS, we check: if v != -1 and used[v] and not visited[v]. Since used[c] is False, we do not push c. So c is not added to the component. Let's correct: in the DFS, we only push v if used[v] is True. So for b, next[b]=c, but used[c] is False, so we do not push c. So component is {a,b,d}. size=3. Then check has_outside: for u in component:
- a: next[a]=b, b in component? yes.
- b: next[b]=c, c is not used, so outside.
- d: next[d]=b, b in component? yes.
So has_outside = True. operations += 3.
Then next unvisited used: f. component: {f}. size=1. next[f]=k, k not used, so outside. operations += 1.
Total = 4. Correct.

So the algorithm works.

Now, we need to implement it in Python.

One more thing: we need to handle the case where target[c] is not defined? Actually, for each used c, we have set target[c] from the loop. So it's always defined.

Now, let's write the code.

We'll use sys.stdin.read to read all input.

Potential pitfalls: The graph might have multiple components. We need to ensure we visit all.

Complexity: O(N + 26^2) which is fine.

Now, let's code.### PLAN
We need to determine if we can transform string S into T using operations that replace all occurrences of a chosen letter x with another letter y. The key insight is that each letter in S must map consistently to a single target letter in T. If any letter in S maps to multiple different targets, it's impossible. Otherwise, we build a directed graph on the 26 letters where each letter that appears in S has an edge to its target. The graph consists of connected components, each containing exactly one cycle (possibly a self-loop). For each component, the minimum number of operations depends on its structure: if the component is a tree (no cycle), the operations equal the number of nodes; if it has a self-loop cycle, operations equal (number of nodes - 1); if it has a cycle of length ≥ 2, operations equal (number of nodes + 1). We sum these over all components.