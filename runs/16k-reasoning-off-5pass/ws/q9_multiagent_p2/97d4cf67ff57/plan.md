The problem asks for the maximum size of a subgraph that is an "alkane" (a tree where every node has degree 1 or 4, with at least one node of degree 4). This structure implies the subgraph consists of a central "core" of degree-4 nodes connected by paths of degree-2 nodes (which are not allowed in the final set, so the paths must be reduced to single edges between degree-4 nodes or degree-4 to degree-1 nodes). Actually, looking closer: the subgraph must *only* contain vertices of degree 1 or 4. This means we cannot have any internal nodes of degree 2 or 3 in the subgraph. Therefore, the subgraph is formed by selecting a set of vertices $S$ such that in the induced subgraph (or rather, the subgraph formed by edges connecting vertices in $S$), every vertex in $S$ has degree 1 or 4. Since the original graph is a tree, the subgraph is also a forest. To be a single alkane, it must be connected.
The structure is essentially a "star-like" or "tree-like" arrangement where degree-4 nodes are connected directly to each other or to degree-1 nodes. If two degree-4 nodes are connected, the edge between them counts towards both degrees. If a degree-4 node connects to a degree-1 node, that's a leaf.
Crucially, we cannot have a path of length > 1 between two degree-4 nodes unless the intermediate nodes are also degree 4 (which would make them part of the core) or degree 1 (impossible, as they would have degree 2 in the path). Wait, if we pick a set of vertices, the degree in the *subgraph* is the number of neighbors in that set.
So, we need to select a subset of vertices $V' \subseteq V$ such that the induced subgraph (using only edges from $T$ where both endpoints are in $V'$) is connected, has no isolated vertices (implied by degree $\ge 1$), and every vertex in $V'$ has degree 1 or 4 in this induced subgraph, with at least one vertex having degree 4.
Since the original graph is a tree, the induced subgraph on $V'$ is a forest. For it to be an alkane, it must be a single tree.
This looks like we are selecting a "skeleton" of degree-4 nodes and attaching leaves to them.
Let's re-evaluate the constraints. If we pick a set of vertices, say $u$ and $v$, and the path between them in $T$ is $u - x - v$. If we include $u, v, x$, then in the subgraph, $x$ has degree 2. This is forbidden. Thus, we cannot include intermediate nodes on paths between selected nodes unless those intermediate nodes also become degree 4 or 1. But an intermediate node on a simple path in a tree has degree 2 in the path. To make its degree 4 in the subgraph, it must connect to 2 other neighbors in the subgraph. To make it degree 1, it must be a leaf.
This implies that the "backbone" of the alkane must consist *only* of edges connecting two degree-4 nodes, or a degree-4 node to a degree-1 node. We cannot have a chain of degree-4 nodes connected by degree-2 nodes because those degree-2 nodes would be excluded, breaking the connection.
Wait, if $u$ and $v$ are both degree 4 in the subgraph, and they are connected by an edge $(u,v)$ in $T$, that's fine. If they are connected by a path $u-x-v$ in $T$, and we include $u, v, x$, then $x$ has degree 2. Forbidden. So $u$ and $v$ must be adjacent in $T$ if they are both in the subgraph and connected?
No, that's too restrictive. Let's trace carefully.
In the subgraph, vertices have degrees 1 or 4.
Consider the component. It's a tree.
Sum of degrees = $2 \times (N_{sub} - 1)$.
Let $k$ be the number of degree-4 nodes, $m$ be the number of degree-1 nodes.
$4k + 1m = 2(N_{sub} - 1) = 2(k+m-1) \implies 4k + m = 2k + 2m - 2 \implies 2k = m - 2 \implies m = 2k + 2$.
Total vertices $N_{sub} = k + m = 3k + 2$.
So any valid alkane has $k$ nodes of degree 4 and $2k+2$ nodes of degree 1.
Now, how are they connected?
A degree-4 node must have 4 neighbors in the subgraph. These neighbors can be degree-4 or degree-1.
If a neighbor is degree-1, it's a leaf attached to the core.
If a neighbor is degree-4, they are connected.
Since the subgraph is a tree, there are no cycles.
Can we have a path of degree-4 nodes? $u - v - w$.
In this path, $v$ has neighbors $u$ and $w$. To have degree 4, $v$ needs 2 more neighbors. They must be leaves (degree 1).
So the structure is a tree where "internal" nodes (degree > 1) are all degree 4, and "leaves" are degree 1.
This means we just need to select a set of vertices $S$ such that in the induced subgraph, every node has degree 1 or 4.
Since the original graph is a tree, the induced subgraph is a forest. We need it to be connected.
The condition "degree 1 or 4" in the induced subgraph means:
For any $v \in S$, let $N_S(v) = N(v) \cap S$. Then $|N_S(v)| \in \{1, 4\}$.
This implies we cannot have any node in $S$ with degree 2 or 3 in the induced subgraph.
This effectively means we cannot select a node $v$ and two of its neighbors $u, w$ unless $v$ has exactly 4 neighbors in $S$ (if $v$ is internal) or 1 neighbor (if $v$ is a leaf).
Actually, if $v$ is connected to $u$ and $w$ in the subgraph, and $v$ is not a leaf, it must have degree 4. So it must have exactly 2 more neighbors in $S$.
This suggests a DP approach on trees.
Root the tree arbitrarily (say at 1).
For each subtree, we can maintain states based on the "interface" with the parent.
The interface can be:
1. The node is not selected.
2. The node is selected and is a leaf in the subgraph (degree 1 in subgraph). This means it is connected only to its parent.
3. The node is selected and is an internal node (degree 4 in subgraph). This means it is connected to its parent and 3 children, or not connected to parent but connected to 4 children?
Wait, if it's connected to the parent, it needs 3 children. If it's not connected to the parent, it needs 4 children.
But if it's not connected to the parent, it must be the root of the component.
However, we need a single connected component.
Let's refine the DP state for a subtree rooted at $u$:
We need to decide whether $u$ is included in the alkane.
If $u$ is included:
- Case A: $u$ is a leaf in the alkane. It connects only to its parent (if parent is included). If $u$ is the root of the whole alkane, it must have degree 4? No, the problem says "at least one vertex of degree 4". The root of the alkane (if we view the alkane as a tree) could be degree 4. But in our DP rooted at $T$'s root, the connection to the parent is the "up" edge.
Let's define states based on the degree of $u$ *within the subgraph restricted to the current subtree*.
Actually, the degree in the final subgraph depends on connections to the parent.
State 0: $u$ is not selected.
State 1: $u$ is selected, and in the subgraph formed by $u$ and its descendants, $u$ has degree 0 (meaning it's waiting for the parent to connect to make it degree 1).
State 2: $u$ is selected, and in the subgraph formed by $u$ and its descendants, $u$ has degree 1 (meaning it's connected to one child, and needs 3 more connections? No, if it's connected to parent, it needs 3 children. If it's connected to 1 child, and parent, total 2. Not 4.
Let's rethink. The degree constraint is global for the subgraph.
If $u$ is selected:
- If $u$ is a leaf in the final alkane: it has exactly 1 neighbor in the alkane.
- If $u$ is an internal node in the final alkane: it has exactly 4 neighbors in the alkane.

When processing $u$, we don't know if it will connect to the parent.
Let's define DP states for the subtree at $u$:
- $dp[u][0]$: Max vertices in a valid alkane component entirely within the subtree of $u$, where $u$ is NOT part of the component.
- $dp[u][1]$: Max vertices in a valid alkane component entirely within the subtree of $u$, where $u$ IS part of the component and $u$ is a LEAF in this component (degree 1). This implies $u$ is connected to exactly one child in the subtree.
- $dp[u][2]$: Max vertices in a valid alkane component entirely within the subtree of $u$, where $u$ IS part of the component and $u$ is an INTERNAL node (degree 4) in this component. This implies $u$ is connected to exactly 4 children in the subtree.
Wait, what if $u$ is connected to the parent?
If $u$ is connected to the parent, then in the subtree component, $u$ must have degree 0 (if it becomes a leaf via parent) or degree 3 (if it becomes internal via parent).
So we need states representing the "pending" degree from the parent side.
Let's redefine:
$dp[u][0]$: $u$ not selected.
$dp[u][1]$: $u$ selected, and currently has degree 0 in the subtree (needs 1 connection from parent to become a leaf, or 4 connections from children to become internal? No).
Let's track the number of children connected to $u$ in the subtree.
If $u$ is selected:
- Option A: $u$ will be a leaf in the final alkane. It needs 1 neighbor total. If it connects to parent, it needs 0 children. If it doesn't connect to parent (root of alkane), it needs 1 child? No, if it's the root of the alkane and a leaf, degree is 1. But the alkane must have at least one degree 4 node.
- Option B: $u$ will be an internal node (degree 4). It needs 4 neighbors total.
  - If it connects to parent, it needs 3 children.
  - If it doesn't connect to parent, it needs 4 children.

So states for $u$ (selected):
- State 0: $u$ selected, degree 0 in subtree (needs 1 from parent to be leaf, or 4 from children to be internal? No, if it needs 1 from parent, it has 0 children. If it needs 4 from children, it has 0 children? No, if it needs 4 from children, it has 0 connections to parent? No, if it connects to parent, it needs 3 children. If it doesn't, it needs 4 children).
Let's simplify. The "interface" is how many edges $u$ has to its children in the chosen subgraph.
Possible values for edges to children: 0, 1, 2, 3, 4.
But constraints:
- If $u$ connects to parent:
  - If $u$ is leaf: needs 0 children. (Total degree 1).
  - If $u$ is internal: needs 3 children. (Total degree 4).
- If $u$ does NOT connect to parent (root of component):
  - If $u$ is leaf: needs 1 child. (Total degree 1).
  - If $u$ is internal: needs 4 children. (Total degree 4).

So we can define:
$dp[u][0]$: $u$ not selected.
$dp[u][1]$: $u$ selected, connected to 0 children. (Needs parent to be leaf).
$dp[u][2]$: $u$ selected, connected to 3 children. (Needs parent to be internal).
$dp[u][3]$: $u$ selected, connected to 1 child. (Root of component, leaf).
$dp[u][4]$: $u$ selected, connected to 4 children. (Root of component, internal).

Wait, can we have a component that is just a single node? No, degree must be 1 or 4. Single node has degree 0. Invalid.
Can we have a component with only leaves? No, must be connected.
So valid components must have at least one internal node.
The states 3 and 4 represent components that are "complete" within the subtree (they don't need the parent to satisfy degree constraints, except for connectivity if they are attached to something else? No, if they are complete, they are isolated components).
But we are building one big component.
Actually, the standard tree DP for "max size subgraph with property P" usually involves:
- $f[u][0]$: $u$ not in subgraph.
- $f[u][1]$: $u$ in subgraph, degree in subgraph (considering children) is $k$.
But we don't know the parent connection yet.
Let's stick to the "needs" logic.
States for $u$ (selected):
- $S_0$: $u$ has 0 children connected. (Needs 1 from parent to be leaf. If no parent, invalid as leaf unless it's the only node? No, single node invalid).
- $S_1$: $u$ has 1 child connected. (If no parent, $u$ is leaf. Valid component if it has an internal node elsewhere? No, this component must eventually merge or be part of a larger one. But if this is the only component, it's invalid. However, we can track if the component contains a degree-4 node).
- $S_2$: $u$ has 3 children connected. (Needs 1 from parent to be internal. If no parent, invalid as internal).
- $S_3$: $u$ has 4 children connected. (No parent needed. $u$ is internal. Valid component if it exists).

Wait, what if $u$ has 2 children? Then degree is 2. Invalid.
What if $u$ has 1 child and connects to parent? Degree 2. Invalid.
So the only valid configurations for $u$ (selected) are:
1. 0 children + 1 parent (Leaf)
2. 3 children + 1 parent (Internal)
3. 1 child + 0 parent (Leaf) -> Only valid if this is the root of the alkane? But alkane must have degree 4 node. So a component with only leaves is invalid.
4. 4 children + 0 parent (Internal)

So, if we are building a single component, we can have:
- A "pending leaf" (needs parent): 0 children.
- A "pending internal" (needs parent): 3 children.
- A "complete leaf" (1 child, 0 parent): This is a valid component ONLY if it contains a degree 4 node. But a leaf component has no degree 4 node. So this state is invalid as a standalone component. It can only be merged with something else? No, if it has 0 parent connection, it's disconnected from the rest. So it must be invalid.
- A "complete internal" (4 children, 0 parent): Valid standalone component (contains degree 4 node).

So the states are:
- $dp[u][0]$: $u$ not selected.
- $dp[u][1]$: $u$ selected, 0 children connected. (Needs parent).
- $dp[u][2]$: $u$ selected, 3 children connected. (Needs parent).
- $dp[u][3]$: $u$ selected, 4 children connected. (Complete, contains degree 4).

Wait, is it possible to have a component where $u$ is a leaf (1 child, 0 parent) and it's part of a larger structure? No, if 0 parent, it's disconnected.
So $dp[u][3]$ is the only "complete" state.
But we need to ensure the final answer has at least one degree 4 node.
We can add a flag or handle it at the end.
Actually, if we have a "complete internal" node, we have a degree 4 node.
If we have a "pending" node, it might become a leaf or internal.
If the final root is a "pending leaf" (0 children), it means the root of the whole tree is a leaf in the alkane. That's fine, as long as there is another degree 4 node somewhere.
If the final root is "pending internal" (3 children), it means the root is internal. Fine.
If the final root is "complete internal" (4 children), fine.
If the final root is "complete leaf" (1 child), invalid (no degree 4).

So states:
0: Not selected.
1: Selected, 0 children (needs parent).
2: Selected, 3 children (needs parent).
3: Selected, 4 children (complete, has deg 4).

Transitions for $u$:
Calculate max vertices for each state by combining children.
For each child $v$, we can either:
- Not include $v$ in the component connected to $u$. Then $v$'s subtree contributes nothing (or a separate component, but we only care about the one connected to $u$). So contribution 0.
- Include $v$ and connect it to $u$. Then $v$ must be in a state compatible with connecting to parent.
  - If $u$ is building a "needs parent" state (0 or 3 children needed), $v$ can be:
    - A leaf child: $v$ needs 0 children (state 1). Then $u$ gets 1 child.
    - An internal child: $v$ needs 1 parent (state 2). Then $u$ gets 1 child.
  - If $u$ is building a "complete" state (4 children), $v$ can be state 1 or 2.

Let's formalize:
$dp[u][0] = 0$ (or -inf if we enforce selection? No, 0 is fine).
$dp[u][1]$: $u$ selected, 0 children.
  We must select $u$. Children must NOT be connected to $u$.
  So for all children $v$, we take $dp[v][0]$.
  Sum of $dp[v][0]$ + 1 (for $u$).
  Wait, if we don't connect $v$, $v$ is not in the component. Correct.
$dp[u][2]$: $u$ selected, 3 children.
  Select $u$. Choose 3 children to connect. For each connected child $v$, we can take $dp[v][1]$ (leaf child) or $dp[v][2]$ (internal child).
  For unconnected children, take $dp[v][0]$.
  Maximize sum.
$dp[u][3]$: $u$ selected, 4 children.
  Select $u$. Choose 4 children to connect. For each connected child $v$, take $dp[v][1]$ or $dp[v][2]$.
  For unconnected, $dp[v][0]$.
  This state guarantees a degree 4 node ($u$).

Wait, what if $u$ is a leaf in the final alkane but has 1 child?
That corresponds to $u$ having 1 child and 0 parent.
This is a valid configuration for $u$, but as discussed, if $u$ is the root of the component and has 1 child, the component has no degree 4 node (unless the child has one).
But if $u$ has 1 child, $u$ is degree 1. The child must be degree 4 (internal) or degree 1 (leaf).
If child is degree 1, then $u$-child is a path of 2 leaves. Invalid (no degree 4).
If child is degree 4, then the child must have 4 neighbors. One is $u$. So child has 3 other neighbors.
So the state "u selected, 1 child" is valid ONLY if the child is an internal node (state 2 or 3?).
But in our DP, we only allow connecting if the child is in state 1 (needs parent) or 2 (needs parent).
State 3 is "complete". If we connect a state 3 node to $u$, then $u$ has a neighbor that is already complete (degree 4). Then $u$'s degree would be 1 (from child) + ...?
If $v$ is state 3, it has 4 children. It does not need a parent. If we connect $u$ to $v$, $v$'s degree becomes 5. Invalid.
So we can only connect to children in state 1 or 2.
So "u selected, 1 child" means $u$ connects to one child $v$ which is in state 1 or 2.
If $v$ is state 1 (leaf), $v$ has 0 children. $u$ has 1 child. $u$ is leaf. Component: $u-v$. No degree 4. Invalid.
If $v$ is state 2 (internal), $v$ has 3 children. $u$ has 1 child. $v$ is degree 4. $u$ is degree 1. Component valid.
So we need to track if the component has a degree 4 node.
Let's add a boolean flag or separate states for "has degree 4".
States:
- 0: Not selected.
- 1: Selected, 0 children (needs parent). (Has deg 4? No, $u$ is leaf. Depends on children? No children. So no deg 4 here. But children might have deg 4? No, children not connected).
- 2: Selected, 3 children (needs parent). (Has deg 4? No, $u$ needs parent. But children might have deg 4? No, children are leaves or internal needing parent. If child is internal (state 2), it has 3 children. So child is deg 4. Yes).
- 3: Selected, 4 children (complete). (Has deg 4? Yes, $u$ is deg 4).
- 4: Selected, 1 child (complete leaf). (Has deg 4? Depends on child. Child must be state 2 (internal). So if child is state 2, yes. If child is state 1, no).

This is getting complicated.
Alternative: Just compute max size for each state, and at the end, check if the component has a degree 4 node.
Actually, if a component has a degree 4 node, it must contain at least one node with 4 children (in the subtree view) OR a node with 3 children + parent.
In our DP:
- State 3 (4 children): Definitely has deg 4.
- State 2 (3 children): Has deg 4 if the component formed by children has a deg 4 node? No, $u$ itself is not deg 4 yet. But one of the children might be deg 4.
  - If a child is state 2, that child has 3 children. Is that child deg 4? No, it needs parent.
  - If a child is state 3, that child is deg 4. But we can't connect to state 3.
  - So in state 2, no child is deg 4 yet. $u$ is not deg 4 yet. So state 2 component has NO deg 4 node.
- State 1 (0 children): No deg 4.
- State 4 (1 child): $u$ is leaf. Child is state 2 (needs parent). Child has 3 children. Child is not deg 4. So no deg 4.
Wait, if we connect $u$ to $v$ (state 2), $v$ becomes deg 4.
So if we have a component where $u$ is state 2 (needs parent), and we attach it to parent, $u$ becomes deg 4.
So the "has deg 4" property is dynamic.
Let's define:
$dp[u][0]$: max size, $u$ not selected.
$dp[u][1]$: max size, $u$ selected, 0 children. (Needs parent).
$dp[u][2]$: max size, $u$ selected, 3 children. (Needs parent).
$dp[u][3]$: max size, $u$ selected, 4 children. (Complete, $u$ is deg 4).

We also need to know if the component contains a deg 4 node.
Let $has4[u][state]$ be true if the component in state has a deg 4 node.
- $has4[u][0] = false$.
- $has4[u][1] = false$ (no children, $u$ is leaf).
- $has4[u][2] = \exists v \in children, has4[v][1] \lor has4[v][2]$. (Since $u$ is not deg 4, need child to be deg 4).
  - But wait, if $v$ is state 2, $v$ needs parent. $v$ is not deg 4.
  - If $v$ is state 3, $v$ is deg 4. But we can't connect to state 3.
  - So in state 2, no child is deg 4. So $has4[u][2] = false$.
- $has4[u][3] = true$ ($u$ is deg 4).
- What about the case where $u$ is state 2, and we attach it to parent? Then $u$ becomes deg 4.
- What about the case where $u$ is state 1, and we attach to parent? $u$ becomes leaf.
- What about the case where $u$ is state 2, and we attach to parent? $u$ becomes deg 4.
- What about the case where $u$ is state 1, and we attach to parent? $u$ becomes leaf.
- Is it possible to have a deg 4 node that is not $u$?
  - Only if a child is state 3. But we can't connect to state 3.
  - So in any component connected to $u$ (via parent or not), the only potential deg 4 nodes are $u$ (if it gets 4 connections) or children that are state 3 (impossible).
  - Wait, what if a child is state 2, and we connect it to $u$? Then child has 3 children + 1 parent = 4. So child becomes deg 4.
  - So if we connect a state 2 child to $u$, that child becomes deg 4.
  - So in state 2 (u has 3 children), if any child is state 2, that child becomes deg 4 when connected to $u$.
  - So $has4[u][2]$ should be true if any connected child is state 2.
  - Similarly, $has4[u][1]$ is false (0 children).
  - $has4[u][3]$ is true.

So:
$dp[u][1]$: sum of $dp[v][0]$ + 1. $has4 = false$.
$dp[u][2]$: choose 3 children to connect. For each, take max($dp[v][1], dp[v][2]$).
  - If we pick a child $v$ in state 2, then $v$ becomes deg 4. So $has4 = true$.
  - If all picked children are state 1, $has4 = false$.
  - So we need to track if we picked any state 2 child.
$dp[u][3]$: choose 4 children. Similar logic. $has4 = true$ (since $u$ is deg 4).

This requires tracking "has deg 4" as a separate state or combining.
Actually, we can just compute two values for each state:
- $max\_size$: max vertices.
- $max\_size\_with\_deg4$: max vertices if the component has a deg 4 node, else -inf.
Then:
$dp[u][1]$:
  - $max\_size = 1 + \sum dp[v][0]$.
  - $max\_size\_with\_deg4 = -\infty$.
$dp[u][2]$:
  - We need to pick 3 children.
  - For each child, we can pick:
    - Option A: $v$ not selected ($dp[v][0]$).
    - Option B: $v$ selected, 0 children ($dp[v][1]$).
    - Option C: $v$ selected, 3 children ($dp[v][2]$).
  - We want to maximize sum.
  - Also track if any Option C is chosen.
  - Let $S_0 = dp[v][0]$, $S_1 = dp[v][1]$, $S_2 = dp[v][2]$.
  - We need to select 3 children to be "active".
  - For each child, we can choose to be active (B or C) or inactive (A).
  - If active, we get $S_1$ or $S_2$. If $S_2$ is chosen, we get a deg 4 node.
  - So for each child, we have pairs: $(S_0, false)$, $(S_1, false)$, $(S_2, true)$.
  - We need to pick 3 pairs to maximize sum, and track if any $true$.
  - This is a small knapsack-like problem (pick 3).
  - Since we need to know if we have a deg 4, we can compute:
    - $best\_no\_deg4$: max sum using only $S_0, S_1$.
    - $best\_with\_deg4$: max sum using at least one $S_2$.
  - Then $dp[u][2].size = \max(best\_no\_deg4, best\_with\_deg4)$.
  - $dp[u][2].has4 = best\_with\_deg4 > -\infty$.
$dp[u][3]$:
  - Pick 4 children.
  - $u$ is deg 4, so $has4 = true$ always.
  - Maximize sum of 4 active children (from $S_1, S_2$) + inactive ($S_0$).
  - Note: $S_2$ is allowed and gives deg 4 (but $u$ already gives it).

Final Answer:
Check root.
Possible states:
- Root not selected: 0.
- Root selected, 0 children: $dp[root][1]$. (Needs parent? No parent. Invalid unless it's a leaf in a component with deg 4 elsewhere? No, if root has 0 children, it's isolated. Invalid).
- Root selected, 3 children: $dp[root][2]$. (Needs parent? No parent. Invalid as internal. But if it has deg 4 from children? No, needs parent to be deg 4. So invalid).
- Root selected, 4 children: $dp[root][3]$. (Complete. Valid).
- Wait, what if the root is a leaf (1 child)?
  - We didn't define state for "1 child".
  - But if root has 1 child, and that child is state 2 (becomes deg 4), then root is leaf, child is internal. Valid.
  - So we need state "1 child".
  - Let's add $dp[u][4]$: $u$ selected, 1 child.
    - Pick 1 child to be active ($S_1$ or $S_2$).
    - Others inactive ($S_0$).
    - $has4 = true$ if child is $S_2$.
  - Final answer candidates:
    - $dp[root][3]$ (always has deg 4).
    - $dp[root][4]$ (has deg 4 if child is $S_2$).
    - $dp[root][2]$? No, needs parent.
    - $dp[root][1]$? No, needs parent.
    - What if the component is just a single node? Invalid.
    - What if the component is a path? No, must be alkane.

So states: 0, 1 (0 kids), 2 (3 kids), 3 (4 kids), 4 (1 kid).
Transitions for 2 and 4 involve picking $k$ children.
For 2: pick 3.
For 4: pick 1.
For 3: pick 4.

Complexity: $O(N \times 5 \times \text{degree})$. Since sum of degrees is $2N$, it's $O(N)$.

Implementation details:
- Use -1 for impossible.
- For picking $k$ children, sort children by gain ($S_1 - S_0$ and $S_2 - S_0$) to pick best?
  - We need to pick exactly $k$ children to be active.
  - For each child, we have options:
    - Inactive: $S_0$.
    - Active type 1: $S_1$. (Gain $S_1 - S_0$).
    - Active type 2: $S_2$. (Gain $S_2 - S_0$, flag=true).
  - We need to select $k$ active options to maximize sum.
  - This is equivalent to: for each child, choose one of 3 options, such that count of active is $k$.
  - Since $k$ is small (1, 3, 4), we can just iterate or use a simple greedy if we separate "with deg 4" and "without".
  - Actually, for "without deg 4", we only consider $S_0, S_1$. We must pick $k$ from these. If a child has no $S_1$ (i.e., $S_1 = -1$), we can't pick it as type 1.
  - For "with deg 4", we must pick at least one type 2.
  - We can compute:
    - $max\_no\_deg4$: max sum picking $k$ from $\{S_0, S_1\}$.
    - $max\_with\_deg4$: max sum picking $k$ from $\{S_0, S_1, S_2\}$ with at least one $S_2$.
  - To compute $max\_no\_deg4$: For each child, best is $\max(S_0, S_1)$. But we need exactly $k$ active.
    - So we need to choose $k$ children to be active (type 1) and $N-k$ inactive.
    - This is: pick $k$ children with largest $S_1 - S_0$ (if $S_1 > S_0$) and set them to active?
    - No, we can choose any $k$ children to be active.
    - Let $diff = S_1 - S_0$. If $diff < 0$, we shouldn't pick it? But we MUST pick $k$ active.
    - So we pick the $k$ children with largest $S_1 - S_0$. If $S_1$ is invalid (-1), treat as $-\infty$.
    - Sum = $\sum S_0 + \sum_{chosen} (S_1 - S_0)$.
  - Similarly for $max\_with\_deg4$:
    - We need at least one $S_2$.
    - We can iterate over which child provides the $S_2$, then pick remaining $k-1$ from $\{S_0, S_1, S_2\}$? No, remaining can be $S_2$ too.
    - Better: Compute best sum with $k$ active allowing $S_2$, then subtract the case where no $S_2$ is used?
    - Or: For each child, we have options $O_0=S_0, O_1=S_1, O_2=S_2$.
    - We need to pick $k$ options (one per child) such that count of non-$O_0$ is $k$, and at least one is $O_2$.
    - This is slightly complex. Given $k$ is small, we can just do a small DP or greedy.
    - Actually, since $k$ is small (1, 3, 4), and number of children can be large, we can't iterate all subsets.
    - But we only need to pick $k$ children.
    - Strategy:
      - Calculate $val_1 = S_1 - S_0$, $val_2 = S_2 - S_0$.
      - We need to choose $k$ children to be active.
      - For "no deg 4": choose $k$ children with largest $val_1$ (if $val_1 > 0$? No, must pick $k$).
        - If we must pick $k$, we pick the $k$ largest $val_1$. If some $S_1$ is -1, that child cannot be active type 1.
        - So we collect all valid $val_1$ for all children, sort descending, pick top $k$.
      - For "with deg 4":
        - We need at least one $S_2$.
        - Option A: Pick one child to be $S_2$, and $k-1$ children to be $S_1$ (or $S_0$? No, active means $S_1$ or $S_2$).
        - Wait, active means we use $S_1$ or $S_2$.
        - So we need to pick $k$ children to be active. At least one is $S_2$.
        - For the chosen $k$ children, we assign each to $S_1$ or $S_2$.
        - To maximize, for a fixed set of $k$ children, we assign $S_2$ to those with $S_2 > S_1$, and $S_1$ to others.
        - But we need at least one $S_2$.
        - So:
          - Calculate potential gain for each child if active: $g_1 = S_1 - S_0$, $g_2 = S_2 - S_0$.
          - We need to pick $k$ children.
          - For each child, we can contribute $\max(g_1, g_2)$ if we allow $S_2$.
          - But we need at least one $S_2$.
          - So:
            - Compute sum of $\max(g_1, g_2)$ for top $k$ children? No, we need to pick the set of $k$ children that maximizes the sum.
            - This is: pick $k$ children with largest $\max(g_1, g_2)$.
            - Then check if any of them used $S_2$.
            - If yes, done.
            - If no (all used $S_1$), we need to swap one $S_1$ with an $S_2$ from outside or inside.
            - This is getting messy.
            - Simpler: Since $k$ is small, we can just compute:
              - $best\_no\_deg4$: Pick $k$ children with largest $g_1$. (If $g_1 < 0$, we still pick if forced? Yes, we must pick $k$).
              - $best\_with\_deg4$:
                - Iterate over each child $i$ as the one providing $S_2$.
                - Then pick $k-1$ other children with largest $\max(g_1, g_2)$.
                - Sum = $S_2 + \sum_{others} \max(g_1, g_2)$.
                - Take max over all $i$.
                - This is $O(N \cdot k)$. Since $k \le 4$, it's $O(N)$. Perfect.

Let's code this.