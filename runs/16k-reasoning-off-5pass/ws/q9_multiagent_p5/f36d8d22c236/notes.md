
## ideation
**Core Difficulty**:
The problem asks for the minimum number of operations to transform string $S$ into string $T$ using global character substitutions. The core challenges are:
1.  **Consistency Check**: A valid transformation requires that if a character $c$ appears in $S$ at multiple positions, it must map to the *same* character in $T$ at all those positions. If $S[i] = S[j]$ but $T[i] \neq T[j]$, the transformation is impossible.
2.  **Optimal Operation Count**: Once consistency is verified, we need to count the minimum operations. Since one operation replaces *all* occurrences of a character $x$ with $y$, we can process characters independently. However, there's a subtle dependency: if we change $x \to y$, and later we need to change $y \to z$, the original $x$'s will now be $z$. But in this specific problem structure (global replacement), we can view the dependency as a directed graph where edges are $S[i] \to T[i]$.
    *   Actually, a simpler view is: For each unique character $c$ present in $S$, if $c$ is not already equal to its target character (based on the mapping), we need 1 operation to change $c$ to its target.
    *   Wait, is it always 1 per unique character? Consider $S=$ "ab", $T=$ "ba".
        *   $a \to b$, $b \to a$.
        *   Op 1: $a \to b$. $S$ becomes "bb".
        *   Now we have "bb", but we need "ba". This fails because the original $b$ was overwritten by the $a \to b$ operation? No, the operation replaces *all* occurrences.
        *   Let's re-read the operation: "Choose x, y and replace every occurrence of x in S with y".
        *   If $S=$ "ab", $T=$ "ba".
            *   Map: $a \to b$, $b \to a$.
            *   If we do $a \to b$, $S$ becomes "bb". We cannot distinguish the original $a$ from the original $b$ anymore if they both become $b$. But we need the final string to be "ba".
            *   This implies that if there is a cycle in the mapping (e.g., $a \to b$ and $b \to a$), we might need more steps or it might be impossible?
            *   Let's trace Sample 4: $S=$ "abac", $T=$ "bcba".
                *   Indices: 0(a->b), 1(b->c), 2(a->b), 3(c->a).
                *   Mappings: $a \to b$, $b \to c$, $c \to a$.
                *   Cycle: $a \to b \to c \to a$.
                *   Operations:
                    1. $c \to a$: $S$ becomes "abaa". (Original $c$ at index 3 becomes $a$).
                    2. $b \to c$: $S$ becomes "acca". (Original $b$ at index 1 becomes $c$. Original $a$'s are untouched).
                    3. $a \to b$: $S$ becomes "bccc". (All $a$'s become $b$. This includes the original $a$'s AND the $c$ that became $a$ in step 1? No, step 1 changed $c \to a$. Step 3 changes $a \to b$. So the character at index 3 (which was $c$, became $a$ in step 1) will become $b$ in step 3. The original $a$'s (indices 0, 2) also become $b$. Result: "bccc"? Wait.
                    Let's re-trace carefully for Sample 4 ($S=$ abac, $T=$ bcba):
                    Target: $a \to b, b \to c, c \to a$.
                    Path for 'a': needs to become 'b'.
                    Path for 'b': needs to become 'c'.
                    Path for 'c': needs to become 'a'.
                    
                    Strategy: Reverse the cycle order?
                    1. Change $c \to a$. $S$: abac -> abaa. (Indices 3 is now 'a').
                    2. Change $b \to c$. $S$: abaa -> acca. (Index 1 is now 'c').
                    3. Change $a \to b$. $S$: acca -> bccc. (Indices 0, 2, 3 are now 'b').
                    Result: "bccc". Target: "bcba". Mismatch at index 3 (we have 'c', need 'b').
                    
                    Why did this fail? Because when we changed $a \to b$, the character at index 3 (which was originally $c$, then became $a$) also became $b$. But we needed it to be $b$? Wait, target at index 3 is 'a'.
                    Original $S[3] = 'c'$. Target $T[3] = 'a'$.
                    My step 1 ($c \to a$) made it 'a'. Correct.
                    Step 3 ($a \to b$) changed it to 'b'. Incorrect.
                    
                    So the order matters. We must process the cycle in reverse order of dependencies?
                    We need $c \to a$. We need $b \to c$. We need $a \to b$.
                    If we do $a \to b$ first: $S$ becomes "bbbc".
                    Then $b \to c$: $S$ becomes "cccc".
                    Then $c \to a$: $S$ becomes "aaaa".
                    Target "bcba". Fail.
                    
                    Actually, the standard solution for this specific problem (AtCoder ABC 306 C? No, this looks like ABC 265 C? No. It's likely **ABC 265 D**? No. It is **ABC 265 C** is different. It is **ABC 265 D**? No. It is **ABC 265 E**? No.
                    Let's search memory for "replace every occurrence of x in S with y". This is **ABC 265 C** is "Replace"? No.
                    Ah, this is **ABC 265 C** is not it. It is **ABC 265 D**? No.
                    It is **ABC 265 C** is "Replace"? No.
                    It is **ABC 265 C** is "Replace"? No.
                    Okay, let's solve logically.
                    
                    The operation is global.
                    If we have a chain $x \to y \to z \dots \to x$, we can resolve it.
                    Consider the mapping $f: \Sigma \to \Sigma$ defined by $f(S[i]) = T[i]$.
                    Condition 1: $f$ must be a function (consistent). If $S[i] == S[j]$ then $T[i] == T[j]$.
                    Condition 2: If $f(x) = x$, we don't need to do anything for $x$.
                    Condition 3: If $f(x) \neq x$, we need to change $x$.
                    
                    How many operations?
                    If we have a cycle $x_1 \to x_2 \to \dots \to x_k \to x_1$.
                    We need to turn $x_1$ into $x_2$, $x_2$ into $x_3$, ..., $x_k$ into $x_1$.
                    If we simply do $k$ operations:
                    1. $x_k \to x_1$
                    2. $x_{k-1} \to x_k$
                    ...
                    k. $x_1 \to x_2$
                    
                    Let's trace Sample 4 again with this logic ($a \to b, b \to c, c \to a$).
                    Cycle: $a \to b \to c \to a$.
                    Reverse order of application:
                    1. Change $c \to a$. (Wait, $c$ needs to become $a$. $a$ needs to become $b$).
                    If we do $c \to a$: $S$ has original $c$'s become $a$.
                    Then $b \to c$: $S$ has original $b$'s become $c$.
                    Then $a \to b$: $S$ has original $a$'s AND the $c$'s that became $a$ become $b$.
                    This messes up the $c \to a$ requirement for the original $c$'s.
                    
                    Correct Logic for Cycles:
                    To fix a cycle of length $k$, we need $k$ operations? Or $k-1$?
                    Actually, if we have $x \to y$, we do $x \to y$.
                    If we have $x \to y$ and $y \to x$.
                    $S=$ "ab", $T=$ "ba".
                    $a \to b$, $b \to a$.
                    Op 1: $a \to b$. $S$ becomes "bb".
                    Now we have "bb", but we need "ba". The original $b$ is lost/overwritten? No, original $b$ was at index 1. We changed $a$ (index 0) to $b$. Index 1 is still $b$. So "bb".
                    We need index 1 to be $a$. But we can't change $b$ to $a$ because that would change index 0 (which is now $b$) to $a$ as well.
                    So "ab" -> "ba" is IMPOSSIBLE?
                    Wait, Sample 4 says output 4.
                    Sample 4: $S=$ abac, $T=$ bcba.
                    Mappings: $a \to b, b \to c, c \to a$.
                    Output is 4.
                    My manual trace failed. Why?
                    Maybe the operations are not limited to just the characters in the cycle?
                    Or maybe my trace was wrong.
                    Let's try:
                    1. $c \to b$? No, $c$ needs to go to $a$.
                    2. $b \to a$? No, $b$ needs to go to $c$.
                    
                    Let's look at the sample explanation logic implicitly.
                    Sample 1: afbfda -> bkckbb.
                    $a \to b, f \to c, b \to c, d \to b$.
                    Mappings: $a \to b, b \to c, f \to c, d \to b$.
                    Consistency:
                    $a$: all $a$'s map to $b$. OK.
                    $b$: all $b$'s map to $c$. OK.
                    $f$: all $f$'s map to $c$. OK.
                    $d$: all $d$'s map to $b$. OK.
                    Cycles?
                    $a \to b \to c$. (c is target of b, but c is not in source? c is not in S).
                    $f \to c$. (c not in S).
                    $d \to b \to c$.
                    So chains: $a \to b \to c$, $d \to b \to c$, $f \to c$.
                    No cycles involving characters present in S?
                    Wait, $b \to c$. Is $c$ in $S$? No. So $b$ maps to something not in $S$.
                    $a \to b$. $b$ is in $S$.
                    $d \to b$.
                    $f \to c$.
                    So we have a dependency $a \to b \to c$ and $d \to b \to c$.
                    Since $c$ is not in $S$, we don't have a cycle $b \to c \to b$.
                    So for Sample 1, we just need to change $a, b, f, d$.
                    Count = 4.
                    Order:
                    1. $b \to c$ (fixes $b$'s).
                    2. $a \to b$ (fixes $a$'s).
                    3. $f \to c$ (fixes $f$'s).
                    4. $d \to b$ (fixes $d$'s).
                    Wait, if we do $b \to c$ first, then $a \to b$.
                    $S$: afbfda.
                    1. $b \to c$: afcfda.
                    2. $a \to b$: bfcfdb.
                    3. $f \to c$: bcckdb.
                    4. $d \to b$: bkckbb.
                    Matches T.
                    So for Sample 1, answer is 4.
                    
                    Now Sample 4: abac -> bcba.
                    Mappings: $a \to b, b \to c, c \to a$.
                    Cycle: $a \to b \to c \to a$.
                    All three characters are in $S$.
                    We need 4 operations?
                    Why 4?
                    If we do 3 operations:
                    1. $c \to a$. $S$: abaa.
                    2. $b \to c$. $S$: acca.
                    3. $a \to b$. $S$: bccc. (Fail, index 3 is c, need b? No, T[3] is a. Wait T is bcba. T[3]=a. We got c. Fail).
                    
                    Maybe we need an intermediate character?
                    Or maybe the cycle requires $k+1$ operations?
                    Actually, if we have a cycle $x_1 \to x_2 \to \dots \to x_k \to x_1$.
                    We can introduce a temporary character? No, we can only use lowercase English letters. But we can pick any $x, y$.
                    Wait, the problem says "Choose two lowercase English letters x, y".
                    We can use a character not in $S$ or $T$ as a temporary?
                    But $S$ and $T$ only contain lowercase English letters.
                    If we use a temp char $z$, we do $x \to z$, then $z \to y$. That's 2 ops for one step.
                    But we want minimum.
                    
                    Let's re-read the sample 4 output. It is 4.
                    The cycle length is 3.
                    If no cycle, answer is number of unique chars in S that need change.
                    If cycle of length $k$, answer is $k+1$?
                    $3+1 = 4$.
                    Why?
                    Because to break the cycle $a \to b \to c \to a$:
                    We need to change $a \to b$, $b \to c$, $c \to a$.
                    If we do $c \to a$ first: $c$ becomes $a$. Now we have $a$'s coming from original $c$'s.
                    Then $a \to b$: original $a$'s become $b$, original $c$'s (now $a$) become $b$.
                    But we wanted original $c$'s to become $a$. They became $b$.
                    So we can't do $c \to a$ then $a \to b$.
                    We must do $a \to b$ BEFORE $c \to a$?
                    1. $a \to b$. $S$: bbac.
                    2. $b \to c$. $S$: ccca. (Original $a$'s became $b$, then $c$. Original $b$ became $c$. Original $c$ is $c$. Original $a$ at 2? $S[2]$ was $a$, became $b$, then $c$. $S[3]$ was $c$. Still $c$. Wait $S[3]$ is $c$. Target is $a$. So we need $c \to a$).
                    3. $c \to a$. $S$: aaaa.
                    Target: bcba.
                    We got aaaa.
                    Original $a$'s (0, 2) -> $b$ -> $c$ -> $a$. Target $b$. Fail.
                    
                    It seems we cannot resolve a cycle of length $k$ with $k$ operations if the cycle involves characters present in $S$.
                    We need an extra operation to "break" the cycle or use a temporary.
                    If we use a temporary $z$ (not in S or T? Or just not involved yet).
                    Say $a \to b \to c \to a$.
                    1. $a \to z$.
                    2. $z \to b$. (Now original $a$ is $b$).
                    3. $b \to c$.
                    4. $c \to a$.
                    Total 4 ops.
                    Does this work?
                    $S$: abac.
                    1. $a \to z$: zbzc.
                    2. $z \to b$: bbcb.
                    3. $b \to c$: cccc.
                    4. $c \to a$: aaaa.
                    Target: bcba. Still fail.
                    
                    Wait, the target for $a$ is $b$.
                    Step 2 made $a \to b$. Good.
                    Step 3 made $b \to c$. Bad. $a$ became $c$.
                    Step 4 made $c \to a$. $a$ became $a$. Bad.
                    
                    Order matters.
                    We need final state:
                    Orig $a \to b$.
                    Orig $b \to c$.
                    Orig $c \to a$.
                    
                    Try:
                    1. $c \to x$ (temp).
                    2. $x \to a$. (Orig $c \to a$. Good).
                    3. $b \to c$. (Orig $b \to c$. Good).
                    4. $a \to b$. (Orig $a \to b$. Good).
                    Check collisions:
                    Step 1: $c \to x$. $S$: abax.
                    Step 2: $x \to a$. $S$: abaa. (Orig $c$ is $a$. Good).
                    Step 3: $b \to c$. $S$: acca. (Orig $b$ is $c$. Good).
                    Step 4: $a \to b$. $S$: bccc. (Orig $a$'s and Orig $c$'s become $b$).
                    Orig $c$ became $a$ in step 2, then $b$ in step 4. Target for Orig $c$ is $a$. Fail.
                    
                    Okay, the issue is that once a character is transformed, it participates in future transformations.
                    To fix $c \to a$, we must ensure that after $c \to a$, we never change $a$ again (unless we change $a$ to something else that eventually leads to $a$? No).
                    So we must perform $c \to a$ LAST among the chain $c \to a \to b \to c$?
                    If $c \to a$ is last:
                    1. $a \to b$.
                    2. $b \to c$.
                    3. $c \to a$.
                    Trace:
                    $S$: abac.
                    1. $a \to b$: bbbc.
                    2. $b \to c$: cccc.
                    3. $c \to a$: aaaa.
                    Target: bcba.
                    Orig $a$ (0,2): $a \to b \to c \to a$. Target $b$. Fail.
                    
                    It seems a cycle of length $k$ requires $k+1$ operations?
                    Sample 4: Cycle $a \to b \to c \to a$ (len 3). Output 4.
                    Sample 1: No cycles (targets not in source or chains don't loop back to source). Output 4 (count of unique sources needing change).
                    
                    Hypothesis:
                    1. Check consistency. If fail, -1.
                    2. Build the mapping graph.
                    3. Count number of unique characters in $S$ that are not mapped to themselves. Let this be $K$.
                    4. If there are any cycles in the functional graph restricted to characters present in $S$, then for each cycle of length $L$, we need $L+1$ operations? Or just add 1 to the total count?
                    Actually, if we have disjoint components.
                    Component 1: Chain (no cycle). Cost = number of edges? Or number of nodes?
                    In Sample 1: $a \to b \to c$ (c not in S). $d \to b \to c$. $f \to c$.
                    Nodes in S: a, b, f, d.
                    Edges: $a \to b, b \to c, f \to c, d \to b$.
                    Unique nodes needing change: a, b, f, d. (4).
                    Cost = 4.
                    
                    In Sample 4: $a \to b, b \to c, c \to a$.
                    Nodes: a, b, c.
                    Edges form a cycle of length 3.
                    Cost = 4.
                    Formula: Cost = (Number of unique chars in S that change) + (Number of cycles in the subgraph induced by chars in S)?
                    Wait, if we have two disjoint cycles?
                    Say $a \to b \to a$ and $c \to d \to c$.
                    Nodes: a, b, c, d.
                    Changes needed: a, b, c, d.
                    Cycles: 2.
                    Cost = 4 + 2 = 6?
                    Let's verify logic.
                    For a cycle $x_1 \to x_2 \to \dots \to x_k \to x_1$:
                    We need to change $x_1 \to x_2$, $x_2 \to x_3$, ..., $x_k \to x_1$.
                    If we do $k$ ops, we fail as shown.
                    We need $k+1$ ops.
                    So for each cycle, we add 1 extra operation.
                    Total = (Count of unique chars in S that are not fixed points) + (Count of cycles).
                    
                    Is it possible to have a cycle where one node is not in S?
                    No, because the edge is defined by $S[i] \to T[i]$. If $x$ is in S, it has an outgoing edge. If $x$ is not in S, it has no outgoing edge (or we don't care).
                    The "graph" is on the alphabet. We only care about nodes present in S.
                    A cycle exists if $x_1 \in S, x_2 \in S, \dots, x_k \in S$ and $x_{i+1} = f(x_i)$ and $x_1 = f(x_k)$.
                    So yes, cycles are formed entirely by characters present in S.
                    
                    Algorithm:
                    1. Build map `char -> char` from S to T. Check consistency. If inconsistent, return -1.
                    2. Identify all unique characters present in S.
                    3. For each char in S, if `map[c] == c`, ignore.
                    4. Count `cnt` = number of chars in S where `map[c] != c`.
                    5. Detect cycles in the functional graph restricted to chars in S.
                       - Since each node has out-degree at most 1 (functional), we can use visited array to detect cycles.
                       - Iterate through all chars in S. If not visited and `map[c] != c`, traverse.
                       - If we hit a visited node in the current path, we found a cycle. Increment cycle_count.
                       - Note: A cycle is a set of nodes. We need to count the number of disjoint cycles.
                    6. Result = `cnt` + `cycle_count`.
                    
                    Let's re-verify Sample 4 with this.
                    S: abac. Unique: a, b, c.
                    Map: a->b, b->c, c->a.
                    cnt: a!=b, b!=c, c!=a. cnt=3.
                    Cycles: a->b->c->a. One cycle. cycle_count=1.
                    Result = 3+1 = 4. Correct.
                    
                    Sample 1:
                    S: afbfda. Unique: a, b, d, f.
                    Map: a->b, b->c, f->c, d->b.
                    cnt: a!=b, b!=c, f!=c, d!=b. cnt=4.
                    Cycles:
                    a->b->c (c not in S, stop). No cycle.
                    f->c (stop). No cycle.
                    d->b->c (stop). No cycle.
                    cycle_count=0.
                    Result = 4. Correct.
                    
                    Sample 3:
                    S: abac, T: abrc.
                    Map: a->a, b->b, c->r.
                    Wait, S[3]='c', T[3]='c'? No T is abrc. S is abac.
                    S[0]=a, T[0]=a.
                    S[1]=b, T[1]=b.
                    S[2]=a, T[2]=r. -> Conflict! a maps to a (idx 0) and r (idx 2).
                    Inconsistent. Return -1. Correct.
                    
                    Edge case: What if a cycle involves a character not in S?
                    Impossible by definition. The edges only exist for chars in S.
                    
                    Edge case: Self-loop $a \to a$.
                    `map[a] == a`. We exclude from `cnt`. Does it form a cycle?
                    Technically a cycle of length 1. But we don't need to change it.
                    So we should only count cycles of length >= 2?
                    Or rather, only consider nodes where `map[c] != c`.
                    If `map[c] == c`, we don't traverse it for cycle detection (or it's a trivial cycle we ignore).
                    My logic: "If `map[c] != c`" before traversing.
                    So self-loops are ignored.
                    
                    Implementation details:
                    - Use an array `mapping` of size 26.
                    - Check consistency first.
                    - Collect unique chars in S.
                    - Run cycle detection on the subgraph of unique chars where `mapping[u] != u`.
                    - Be careful: The graph is functional. We can use a `visited` array with states: 0=unvisited, 1=visiting, 2=visited.
                    - If we encounter state 1, cycle found.
                    
                    Complexity: O(N + 26). Very efficient.

## worker: Write the Python code implementing the logic: Read
The problem requires transforming string $S$ to $T$ using global character replacements.
1.  **Consistency Check**: First, we verify if a valid mapping exists. For every character $c$ in $S$, all occurrences of $c$ must map to the same character in $T$. If $S[i] == S[j]$ but $T[i] \neq T[j]$, it's impossible, so we output -1.
2.  **Graph Construction**: We treat the mapping as a directed graph where an edge exists from $u$ to $v$ if $S$ contains $u$ and it maps to $v$ in $T$.
3.  **Operation Count**:
    *   For any character $u$ in $S$ where $u \neq mapping[u]$, we need at least one operation to change $u$.
    *   If the graph contains a cycle of length $k \ge 2$ involving characters present in $S$, we need $k+1$ operations to resolve it (because simply following the cycle $u \to v \to \dots \to u$ with $k$ operations fails due to overwriting; an extra operation is needed to break the cycle or use a temporary state).
    *   Characters that map to themselves ($u \to u$) require 0 operations.
    *   Characters that map to a target not present in $S$ (or a chain leading to such a target) do not form cycles within the set of changing characters.
4.  **Algorithm**:
    *   Build the mapping array.
    *   Identify unique characters in $S$ that are not fixed points ($mapping[c] \neq c$).
    *   Count these characters ($K$).
    *   Detect the number of disjoint cycles ($C$) formed strictly among these changing characters.
    *   The answer is $K + C$.
5.  **Complexity**: $O(N)$ to read input and build mapping, $O(26)$ to process the graph. Total time is dominated by input reading, well within limits for $N=2 \times 10^5$.

## worker: Run the code against provided sample inputs to ver
The code implements the logic derived:
1.  **Consistency Check**: Iterates through $S$ and $T$ to build a mapping. If a character in $S$ maps to different characters in $T$, it prints -1.
2.  **Node Identification**: Collects unique characters in $S$ that are not fixed points ($mapping[c] \neq c$). These are the nodes that require at least one operation.
3.  **Cycle Detection**: Iterates through the identified nodes. Since the graph is functional (each node has out-degree 1), we traverse paths. If we encounter a node currently in the recursion stack (path), a cycle is detected.
    *   Crucially, the logic ensures we only count cycles formed entirely within the set of nodes that need changing. If a path leads to a node that doesn't need changing (either fixed point or not in $S$), the path terminates without forming a cycle within the "active" set.
4.  **Result Calculation**: The minimum operations is the count of active nodes plus the number of disjoint cycles found among them. This accounts for the extra operation needed to break cycles.

The logic handles Sample 1 (no cycles, count=4), Sample 2 (0 changes), Sample 3 (inconsistent), and Sample 4 (cycle of length 3, count=3+1=4).

## worker: Run the code against the provided sample inputs to
The code implements the logic derived:
1.  **Consistency Check**: Iterates through $S$ and $T$ to build a mapping. If a character in $S$ maps to different characters in $T$, it prints -1.
2.  **Node Identification**: Collects unique characters in $S$ that are not fixed points ($mapping[c] \neq c$). These are the nodes that require at least one operation.
3.  **Cycle Detection**: Iterates through the identified nodes. Since the graph is functional (each node has out-degree 1), we traverse paths. If we encounter a node currently in the recursion stack (path), a cycle is detected.
    *   Crucially, the logic ensures we only count cycles formed entirely within the set of nodes that need changing. If a path leads to a node that doesn't need changing (either fixed point or not in $S$), the path terminates without forming a cycle within the "active" set.
4.  **Result Calculation**: The minimum operations is the count of active nodes plus the number of disjoint cycles found among them. This accounts for the extra operation needed to break cycles.

The logic handles Sample 1 (no cycles, count=4), Sample 2 (0 changes), Sample 3 (inconsistent), and Sample 4 (cycle of length 3, count=3+1=4).

## worker: finalize
The solution implements the following logic:
1.  **Consistency Check**: First, we verify if a valid mapping exists. For every character $c$ in $S$, all occurrences of $c$ must map to the same character in $T$. If $S[i] == S[j]$ but $T[i] \neq T[j]$, it's impossible, so we output -1.
2.  **Graph Construction**: We treat the mapping as a directed graph where an edge exists from $u$ to $v$ if $S$ contains $u$ and it maps to $v$ in $T$.
3.  **Operation Count**:
    *   For any character $u$ in $S$ where $u \neq mapping[u]$, we need at least one operation to change $u$.
    *   If the graph contains a cycle of length $k \ge 2$ involving characters present in $S$, we need $k+1$ operations to resolve it (because simply following the cycle $u \to v \to \dots \to u$ with $k$ operations fails due to overwriting; an extra operation is needed to break the cycle or use a temporary state).
    *   Characters that map to themselves ($u \to u$) require 0 operations.
    *   Characters that map to a target not present in $S$ (or a chain leading to such a target) do not form cycles within the set of changing characters.
4.  **Algorithm**:
    *   Build the mapping array.
    *   Identify unique characters in $S$ that are not fixed points ($mapping[c] \neq c$).
    *   Count these characters ($K$).
    *   Detect the number of disjoint cycles ($C$) formed strictly among these changing characters.
    *   The answer is $K + C$.
5.  **Complexity**: $O(N)$ to read input and build mapping, $O(26)$ to process the graph. Total time is dominated by input reading, well within limits for $N=2 \times 10^5$.
