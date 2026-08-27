- **Model:** Treat each index as a vertex and each constraint as an undirected edge with xor weight z. A valid sequence is a labeling A such that A_u xor A_v = z for every edge.
- **Consistency check:** For each unvisited vertex, run an iterative stack traversal. Set root potential to 0 and assign pot[to] = pot[v] xor w when first reaching to. If an edge connects two already assigned vertices and pot[u] xor pot[v] != w, print -1. This catches self-loops with nonzero weight and conflicting parallel edges.
- **Solution space:** In a consistent component, every valid labeling is pot[v] xor mask for one component-wide mask. Different components have independent masks.
- **Bitwise optimization:** The sum is additive over bits. For bit b, if c of the component potentials have bit 1, mask bit 0 leaves c ones and mask bit 1 leaves size-c ones. Choose mask bit 1 exactly when c > size-c; ties choose 0. Bits above the maximum input weight are always zero in potentials, so they are never set.
- **Implementation details:** Read all integers at once. Build adjacency list of (neighbor, weight). Reuse the potential array as the final answer: after a component is processed, xor its mask into pot[v] for all v in the component. Isolated vertices remain 0. If M is 0 or all weights are 0, all zeros is immediately optimal.
- **Complexity:** With B = 31 (or max(31, max_z.bit_length())), time is O(N + M + N*B), memory O(N + M). Iterative traversal avoids recursion depth issues.
- **Edge cases:** N=1, self-loops, parallel edges, zero-weight components, ties in bit counts, and large disconnected graphs are handled. Output any minimum sequence.

This is good. No headings inside. No ALLCAPS lines. "N=1" okay. "M" okay. "B" okay. No bold-only lines. Each bullet has text. Under 800 words.

Now, let's think if the note "If M is 0 or all weights are 0, all zeros is immediately optimal." In code, for all weights 0 we still build adj before output, but conceptually. Good.

Now, let's consider if the note "Bits above the maximum input weight are always zero in potentials" is true if max_z=0? Yes. If max_z>0, potentials xor of weights, no higher bits. Good.

Now, let's think about if the note "B = 31 (or max(31, max_z.bit_length()))" uses uppercase B, fine. Not ALLCAPS line.

Now, let's ensure the final answer doesn't include analysis. Only sections.

Before final, let's maybe consider if there is a hidden issue with using `max_z == 0` special-case: Suppose there is a constraint A_u xor A_v = 0, all zeros satisfies. Yes. No other constraints. Good.

Now, let's think about if there is a hidden issue with minimizing sum when components independent: The total sum is sum over components, masks independent. Good.

Now, let's consider if there is a possibility that a component's optimal mask is not unique due to ties; our choice 0 for ties. Good.

Now, let's think about if the code's `MAXB = max(31, max_z.bit_length())` and bit_range range(MAXB) means if max_z.bit_length()=31, we count bits 0..30. If max_z=2^30 (1073741824) which is >1e9 but bit_length=31, bit30 can be set. Good. If max_z=2^30-1 bit_length=30, bit30 zero, but we count bit30 due to max(31). Good.

Now, let's consider if `max_z.bit_length()` for max_z=1 is 1, MAXB=31. Good.

Now, let's think about if we can reduce MAXB to 30 for constraints? 1e9 <2^30, bits 0..29. But sample uses 4,3. 30 bits enough. But user says 0..30. Use 31.

Now, let's consider if there is any issue with Python's `int.bit_length` for 0: 0. But max_z==0 returned. Good.

Now, let's think about if the code should handle `M` negative? Constraints no.

Now, let's maybe run through a random small brute force mentally to verify optimization. For N=2, constraint z=2. Solutions: (a, a^2). Sum = 2a + bit? Actually a + (a^2). Min over a nonnegative. Our pot 0,2. size2, bit1 c=1 tie mask0 => (0,2) sum2. Is there a with sum <2? a=1 =>1+3=4, a=2=>2+0=2, a=3=>3+1=4. Min2. Good. For z=3, pot0,3. bit0 c=1 tie, bit1 c=1 tie => (0,3) sum3. a=1=>1+2=3, a=2=>2+1=3, a=3=>3+0=3. Good. For N=3 constraints A1^A2=1, A1^A3=1. pot0,1,1. size3 bit0 c=2>1 mask1 => (1,0,0) sum1. Brute: a1=a, a2=a^1,a3=a^1. Sum=3a? If a=0 sum2, a=1 sum1, a=2 sum?2+3+3=8. Min1. Good.

Now, let's think about if there is a case where choosing mask bit majority for each bit independently yields a mask that is not the one minimizing sum due to integer carries? Already addressed. Example: two bits, choosing mask bit0=1 and bit1=0 vs bit0=0 bit1=1 could have different carries but value linear. Good.

Now, let's consider if the problem might require the sequence elements to be within 32-bit? No.

Now, let's think about if the code's output for all zeros uses `'0 ' * (N - 1) + '0\n'`. For N=200000, string length 399999? '0 ' repeated 199999 = 399998 chars, + '0\n' = 400000. Good. No trailing space. For N=1, '0\n'. Good.

Now, let's think about if final output join for pot where pot contains Python ints maybe some are bool? No.

Now, let's consider if we should convert pot to strings with `map(str, pot)`. Good.

Now, let's think about if `del adj` before output could cause error if `adj` not defined? It is defined if M>0 and max_z>0. If M==0 or max_z==0, we return before. Good.

Now, let's consider if `del data` before max_z==0? In code, we del data after building, then if max_z==0 return. Good.

Now, let's think about if we can free `data` earlier in M==0? Return, program ends. Good.

Now, let's consider if there is any issue with using `idx` and data length. For M lines, idx ends at 2+3M = len(data). Good.

Now, let's think about if input may have extra integers? Constraints no. If extra, ignored? Our loop reads M triples, ignores extra. Fine.

Now, let's consider if the code should be in a single fenced block. Yes.

Now, let's maybe think about a possible bug: In BFS, we check `elif (pv ^ pt) != w`. Suppose `to` is unvisited, we set pot[to] and push. But if there is a self-loop on `to` with nonzero weight, it will be checked when `to` is popped. Good. If there is an edge from `v` to `to` with weight w1 and another from `v` to `to` with weight w2, the first sets pot[to], the second checks. Good.

Potential bug: If an edge is encountered from `v` to `to` where `to` is unvisited, we set pot[to] = pv ^ w. But what if `to` is actually the root of a previously processed component? Then pot[to] != -1, so check. Good.

Potential bug: If graph has an edge with weight w and pot values final from previous component? That would mean components connected, impossible if previous component processed and edge exists; the vertex would have been visited. But if due to bug? No.

Now, let's think about if the iterative traversal could miss an edge check because we only check when both endpoints visited. Every edge is in adjacency of both endpoints. When the first endpoint is popped, if the other is unvisited, we assign and don't check (but assignment enforces). When the second endpoint is popped, the first is visited, check. If the other was already visited before first endpoint popped, check at first endpoint. So every edge checked at least once. Good.

Now, let's consider if a tree edge is checked when second endpoint popped: pot[u]^pot[v] = w by assignment, so passes. Good.

Now, let's think about if there is a cycle and contradiction, detected when processing an edge to a visited vertex that is not the one that assigned it. Good.

Now, let's consider if the graph is not connected and a later component has an edge to an earlier component? Then it would be connected, impossible. Good.

Now, let's think about if the code's `if not adj[s]: pot[s]=0; continue` could skip a vertex that has a self-loop? `adj[s]` would not be empty. Good.

Now, let's consider if the code's `size == 1: continue` leaves pot[s]=0. If there was a self-loop zero, okay. If there was a self-loop nonzero, contradiction. If there was an edge to another vertex, size >1. Good.

Now, let's think about if a component of size 1 with multiple self-loops zero, pot
