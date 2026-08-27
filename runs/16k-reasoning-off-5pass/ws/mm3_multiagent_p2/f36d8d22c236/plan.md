We need to model the allowed operation: choose a source letter x and a target letter y, then replace **every** occurrence of x in S with y. This is a "bulk substitution" of a whole letter class. We cannot replace a single occurrence; all x's become y's simultaneously. After several operations, the final character at each position depends only on the original letter at that position and the sequence of global substitutions applied. Importantly, the operation is deterministic: if we apply (x→y), then later apply (y→z), all former x's become z; later applying (x→w) does nothing because there are no x's left. The process is equivalent to building a mapping f from the 26 original letters to the 26 final letters, where f is a function (each original letter maps to exactly one final letter) and this function can be built using operations of the form “set all letters currently mapped to x to y”. The question: can we find a function f such that for all i, f(S[i]) = T[i]? If not, answer -1. If yes, minimize the number of operations.

**Key observation:** Because every original letter x must become a single final letter f(x) (cannot split), feasibility is: for each original letter x, all positions where S[i]=x must have the same T[i]. If any S[i]=x and S[j]=x with T[i]!=T[j], impossible → output -1.

If feasible, we have a desired function f: 26→26. Initially the identity map (each letter maps to itself). The operation (x→y) updates the mapping: for all letters z with f(z)=x, set f(z)=y. This is exactly the standard “DSU” (union-find with parent tracking) where we merge the set containing x into the set containing y. The cost is 1 per merge.

But we can also make a letter already equal to its target by “self-loop” (x→x), which costs 0 and is unnecessary. So the minimum number of operations equals the number of merges needed to realize the target function f, assuming we never merge two letters that are already in the same set (that would be useless but might be required? Actually we can avoid unnecessary merges). The target function f may be identity on some letters, constant on others, or even have cycles (e.g., a→b, b→a). Cycles are achievable: we can first set a→b (cost 1), then b→a (cost 1). But we could also achieve the same final mapping with a different sequence? Let's analyze.

We need to transform the identity mapping to f. The mapping is a function from letters to letters; applying a bulk operation (x→y) composes the current function g with a substitution: new g = g ∘ σ_{x→y}, where σ_{x→y} maps x to y and all other letters to themselves. Equivalently, the operation replaces the target of every source that currently maps to x by y.

Thus we have a set of 26 elements, each with a current value in 0..25 (initial = element). Operation: for a given current value x, set the current value of **all elements whose current value is x** to y. This is exactly the DSU merge operation. The number of operations needed to achieve a desired final assignment of values is the number of merges required to partition the letters into groups, where all letters in a group end up with the same final value, and the value assigned to the group must be a letter that was originally in the group (since we can only merge into existing values, and the value of a group after merges is one of its original elements). Actually, the value of a group after a sequence of merges is the last y used to merge into. If we want group G to have final value v, we need v to be an element of G (so that v's current value stays v after merges that only affect other elements, and finally we don't need to change it). In other words, the target function f must be a mapping where for each cycle (or fixed point) of f, we can achieve it by merging all elements of the cycle into one representative, then optionally setting that representative to any of the cycle's elements? Wait, the final value of a group must be one of the letters in the group, because we never introduce a new value; the only values that appear are letters that have been used as y in some operation (or initial identity). Starting from identity, we have all letters present. When we merge x into y, the value y may already have been merged from something else; ultimately, each group has a representative which is the last y used (or the original element if never changed). The final value of all elements in the group is that representative. So the set of final values is a subset of original letters, specifically one per group. Therefore, the target assignment f is realizable iff for each group (connected component of the relation “must have same final value”), the common final value v belongs to the set of original letters that map to that group. More formally, consider the undirected graph where we connect S[i] and T[i] whenever S[i] != T[i]? Wait, let's think in terms of constraints.

Feasibility condition: For each original letter c, all occurrences in S must correspond to the same target letter in T. Let f(c) be that target letter (if c never appears in S, f(c) can be anything, but we can leave it as c for free). If any c has multiple required targets, impossible.

Now the question: Given f, what is the minimum number of operations to achieve it? This is a known problem: We have 26 nodes, initially each node maps to itself. Operation: pick a node x and a node y, and set the mapping of x (and all nodes currently mapping to x) to y. This is equivalent to directed graph: each node has an outgoing edge to its current value. Initially self-loops. Operation (x→y) redirects all incoming edges of x to y. The final mapping is a functional graph where each node's out-edge is its final value f(c). The cost is the number of times we redirect edges.

We can think in terms of merging components: Initially 26 singleton components {a},{b},..., each with a label equal to the element. Operation merges the component containing x into the component containing y, and the resulting component's label becomes the label of y's component (the "root"). This is exactly union-find with direction: we always merge the root of x into the root of y, and the new root is the root of y. The cost is 1 per union.

Goal: We want the final mapping to be f. That means for each letter c, after operations, find(c) = f(c). In union-find terms, the representative of c's set must be f(c). Since the representative must be an element of the set, we need that for each set in the final partition, there is a designated "target" element t in that set such that for all c in the set, f(c) = t. This is exactly the same as the feasibility condition: if c and d are in the same set (i.e., after merges they become same), then f(c) must equal f(d). But also, the representative t must be an element of the set. Since the set is built by merging letters that are forced to share the same final value (by f), the set is the connected component of the relation "must have same final value". Let's define an undirected graph on 26 letters: connect c and f(c) if c != f(c). The condition that f is a function means each node has at most one outgoing edge, but we treat it as an undirected edge for connectivity. However, cycles in f create strongly connected components of size >1. For example, if f(a)=b and f(b)=a, then the set is {a,b}, and we need to achieve a mapping where both a and b map to the same value? No, we need find(a)=b and find(b)=a. But in union-find, the representative of a must be b, and representative of b must be a. That's impossible because a representative is a single element. Wait! This reveals a subtlety: The union-find model with a single representative per set cannot accommodate cycles where two distinct elements must map to each other. Because if we have a set {a,b} and we want find(a)=b and find(b)=a, that's contradictory. But in the actual operation, we can achieve f(a)=b and f(b)=a? Let's test with small example. N=2, S="ab", T="ba". Is it possible? Operation: (a→b) makes S="bb". Then (b→a) makes S="aa". Not "ba". Try (b→a) first: S="aa". Then (a→b): S="bb". Still not "ba". So impossible. Indeed, the condition is stricter: For each original letter c, all positions with S[i]=c must have same T[i]. Here S[0]=a, T[0]=b; S[1]=b, T[1]=a. So a→b, b→a. This is impossible because to make a become b, we need to apply (a→b) at some point, but then all a's become b. However, b is also a letter that must become a. After (a→b), there are no a's left, so we cannot turn b's into a's because b is not a. So indeed impossible. In general, the mapping must be a function that has no directed cycles of length >1? Let's analyze.

After operations, each original letter c ends up as some letter v. The transformation is a function f: Σ→Σ. But can f be a permutation with cycles? Suppose f is a 2-cycle (a↔b). Can we achieve it? Starting with identity. To make a→b, we need to apply (a→b) at some time. After that, all a's are b's. But we also need b→a. However, after (a→b), the letter b is still b. To change b's to a, we would need to apply (b→a). But after (a→b), there are no a's anywhere. Applying (b→a) would change all b's to a's. But then the a's that we previously turned into b's are now gone (they were turned into b's, then b's turned into a's). So at the end, all letters become a. Not what we want. What if we apply (b→a) first? Then all b's become a's. Then apply (a→b): all a's (including those that were originally b) become b. So everything becomes b. So we cannot achieve a 2-cycle. What about longer cycles? Same issue. So the realizable functions f are exactly those that are "idempotent" in the sense that f(f(c)) = f(c) for all c, i.e., f is a projection onto a subset where each element maps to itself. In other words, f must be a function where the image consists of fixed points. This is equivalent to saying: the functional graph of f has no directed cycles of length >1; all cycles are self-loops. So f is a function where every element either maps to itself or eventually reaches a fixed point. This is exactly the condition that f is "rooted" (a forest of trees of height 1, i.e., each component is a star with center being a fixed point). Let's verify.

We need to find if there exists a sequence of operations (x→y) that transforms identity to f. The operation (x→y) replaces the current value of x with y, and also replaces the current value of any element that currently maps to x with y. This is equivalent to: for any element z, after operations, its value is determined by the last operation that affected its current value. This is essentially building a mapping by merging sets. The final mapping is a function f. The question: which functions f are achievable? As argued, if we have a set of letters that are merged together, they all end up with the same value, which is the value of the "root" (the last target used). The root must be one of the letters in the set. So for any two letters a,b that are in the same merged set, they must have the same final value f(a)=f(b). Moreover, that value must be an element of the set. So the set is a subset of letters, and the target value is one of them. This means that if we look at the preimage f^{-1}(v) for each v in the image, the preimage is a set containing v itself. Because v must be in its own preimage. Therefore, for any v that appears as a target, v must map to itself: f(v)=v. This implies that the image of f consists of fixed points. So the necessary and sufficient condition is: for every letter c, f(f(c)) = f(c). Equivalently, there is no letter c such that f(c) = d and f(d) = e with d != e and c != d? Actually, the condition is that no letter maps to a different letter that does not map to itself. More precisely, f is a function such that for all c, if f(c) != c, then f(f(c)) = f(c). So f(c) is a fixed point. This is exactly the condition that the functional graph has no cycles of length >1.

Let's check the sample 1: S="afbfda", T="bkckbb". Let's compute f. Positions: i=0: a→b, i=1: f→k, i=2: b→c, i=3: f→k, i=4: d→b, i=5: a→b. So f(a)=b, f(b)=c, f(f)=k, f(d)=b. Check fixed points: f(b)=c, but f(c) is not defined? Wait, c does not appear in S? S has letters a,f,b,d. c is not in S. For letters not in S, we can choose f arbitrarily. We can set f(c)=c (fixed point). So f(b)=c, and f(c)=c. So f(f(b)) = f(c) = c = f(b). So condition holds. For a: f(a)=b, f(b)=c != a, but f(f(a)) = f(b) = c = f(a). So condition holds. For d: f(d)=b, f(b)=c != d, but f(f(d)) = f(b) = c = f(d). So condition holds. So f is realizable.

Now, the minimal number of operations: We need to find the minimal number of merges to achieve f, given the constraint that we can only merge sets into existing values (i.e., we cannot create a new value). However, we have the freedom to choose the order of merges. The cost is the number of union operations performed. But we don't need to merge all letters; we only need to ensure that for each c, after operations, its value is f(c). This is equivalent to: for each c with f(c) != c, we need to "redirect" c (and any other letters that have been merged into c's set) to f(c). The minimal number of operations can be computed as the number of connected components in a certain graph minus the number of fixed points? Let's think.

We can think of the process as building a forest of trees where each non-fixed point points to its parent (the fixed point). The number of operations needed is the number of edges in this forest? Not exactly.

Consider the relation: we have a set of letters. For each c with f(c) != c, we need to change c to f(c). However, if multiple letters need to become the same target t, we can merge them together before redirecting to t, saving operations. For example, if a→b and c→b, we could first merge a and c (cost 1) to a set {a,c}, then merge that set into b (cost 1), total 2. Alternatively, we could do a→b (cost 1) and c→b (cost 1), total 2. Same. But if a→b and b→c, we cannot merge a and b first because b is also moving to c. Actually, we need to eventually have a→c and b→c. We can do b→c (cost 1), then a→b (but after b→c, there is no b left? Wait, after b→c, all b's become c. Then applying a→b does nothing because there are no b's. So we need to apply a→c directly. Or we could do a→b (cost 1) then b→c (cost 1). After a→b, a's are b's. Then b→c changes all b's (including those from a) to c. So both end up c. Total 2. So order matters.

In general, the minimal number of operations to achieve a given f (satisfying the fixed-point condition) is equal to the number of letters c such that f(c) != c, minus the number of "chains" that can be merged? Let's derive.

We can think of each letter as a node. The desired final mapping f can be represented as a directed graph where each node c has an edge to f(c) if f(c) != c, and a self-loop if fixed. Since f(f(c)) = f(c), this graph consists of stars: a center (fixed point) with leaves pointing to it. Some leaves may themselves have other leaves pointing to them? Wait, if a leaf c has f(c)=t (t fixed), and another leaf d has f(d)=c, but f(c)=t, then d's target is c, which is not fixed. But we require f(f(d)) = f(c) = t, and f(d) = c. Then f(f(d)) = t, but f(d) = c != t, so the condition f(f(d)) = f(d) would require c = t, which is false. So such a chain is not allowed. So indeed, the only allowed non-fixed mappings are direct edges to fixed points. Because if f(c) = d and d != c, then f(d) must equal d (since f(f(c)) = f(c) => f(d) = d). So d is a fixed point. Therefore, the graph is a set of stars: each fixed point t has zero or more leaves directly mapping to it. No longer chains.

Thus the structure is simple: Partition the alphabet into groups: each group has a "root" r (a fixed point, f(r)=r), and a set of other letters L that map directly to r. The groups are disjoint because each non-root maps to exactly one root.

Now, what is the minimal number of operations to achieve this? We start with identity: each letter is its own group. We need to merge all letters in L into the group containing r, and then ensure the group's value is r. Actually, after merging, the group's representative is the last target used. We want the representative to be r. If we merge L into r's group one by one, each merge costs 1. However, we might be able to merge some leaves together first, then merge the combined set into r. For example, if L = {a,b} and r=c, we could do a→b (cost 1), then b→c (cost 1). Or b→c (cost 1), then a→c (cost 1). Or a→c (1), b→c (1). So seems always 2 operations for |L| leaves. But is there a way to do it in fewer? Suppose we have three leaves a,b,d mapping to c. Could we do a→b (1), d→b (1), b→c (1) = 3 operations. Or a→c (1), b→c (1), d→c (1) = 3. So for k leaves, we need at least k operations? Let's think: each operation can change the value of a set of letters. We start with each letter having its own value. We need to change k letters (the leaves) to value c, while keeping c as c. The leaves initially have values a,b,d. Each operation can set all letters currently having value x to y. This is like we have k+1 items (the leaves and c). We need to make the k items have value c. Each operation picks a source x and target y. If we pick x = some leaf's current value, we can change that leaf (and any other leaf that currently shares that value) to y. This is similar to building a spanning tree on the k+1 nodes where edges are directed towards c. Each operation corresponds to directing an edge from some node to another. The minimal number of operations to connect k leaves to c is k: we need to change each leaf at least once. However, we can combine multiple leaves if they share the same value at some point. For instance, if we first merge a and b: a→b (now a and b both have value b). Then merge that group into c: b→c. That's 2 operations for 2 leaves. For k leaves, we can pair them up: first merge leaf1 into leaf2 (1), leaf3 into leaf4 (1), ..., then merge each pair into c (k/2). So for k leaves, we need exactly k operations? Let's verify: each leaf must undergo at least one "change" from its original value to c. However, if two leaves are merged together, one of them doesn't need to be changed directly to c; it changes to the other leaf's value, which later changes to c. So the number of operations equals the number of edges in a spanning forest where each component containing leaves is connected to c. The minimal number of operations to connect k leaves to c is k: because we have k+1 items, and we need to connect k items to c, which requires at least k edges in a tree (or forest plus connection to c). Actually, consider a set of items. Initially each has its own value. An operation (x→y) merges the class of x into the class of y. This is exactly a union operation. To make all k leaves have the same value as c, we need to unify the k+1 classes (k leaves and c) into one class. The number of union operations needed to combine m items into one set is m-1. Here m = number of distinct letters that are either the root c or a leaf that must end up as c. So if there are k leaves, then m = k+1, so at least k operations are needed. And we can achieve k by a sequence of unions (e.g., union each leaf with c one by one). So the minimal number of operations for a group with root r and L leaves is |L|.

But wait: what about letters that are not in any S and not in any T? They are irrelevant; we can ignore them. For letters that appear in S but not in T? Actually, T has same length N, so every position in S corresponds to a position in T. If a letter c appears in S, it must map to some T[i] for those positions. If it never appears in S, we can leave it as is, no cost.

So the total minimum number of operations is the sum over all fixed points r of (number of non-fixed letters c such that f(c) = r). In other words, for each letter r that is a fixed point (f(r)=r), count how many other letters map to r. Sum these counts.

But is that always achievable without interfering with other groups? Yes, because the groups are disjoint: each non-root maps to exactly one root, and roots are distinct. We can process each group independently. For group with root r and leaves L, we need |L| operations to merge all leaves into r. Since groups are disjoint (no letter appears in two groups), operations on one group do not affect letters in other groups (except if we use a letter from another group as intermediate, which would be suboptimal). So we can just do |L| operations per group, total sum.

Wait, but there might be a more efficient way: could we use a leaf from one group to help merge leaves in another group? For example, group1: root a, leaf b (b→a). Group2: root c, leaf d (d→c). Could we do b→c (now b and d are c? No, b→c changes b to c, but d is still d. Then we need to change d to c. That doesn't save. What if we do d→b (now d is b), then b→a (now d is a, not c). So not helpful. So groups are independent.

Thus the answer is simply the number of letters c such that f(c) != c. However, we must also consider that if f(c) = c for all c, answer is 0. If some f(c) != c but the fixed-point condition is violated, answer is -1.

Let's test with sample 1: Letters: a→b, f→k, b→c, d→b. Fixed points: which letters have f(x)=x? We need to determine f for all 26 letters. For letters not in S, we can set f(x)=x. For letters in S, we have constraints. Let's list: S letters: a, f, b, d. For each, target: a→b, f→k, b→c, d→b. So f(a)=b, f(f)=k, f(b)=c, f(d)=b. Now check fixed-point condition: f(b)=c. Is c a fixed point? c is not in S, so we can set f(c)=c. So condition holds: f(f(b)) = f(c) = c = f(b). Similarly for a: f(a)=b, f(b)=c, so f(f(a)) = c = f(a). For d: f(d)=b, f(b)=c, so f(f(d)) = c = f(d). For f: f(f)=k. Is k a fixed point? k is not in S, so f(k)=k. So condition holds. So f is valid. The number of non-fixed mappings: a,b,d,f are 4 letters with f(x)!=x. So answer would be 4. Matches sample output 4? Wait sample output is 4. Yes.

Sample 2: S=T, so f(x)=x for all x in S. Others can be fixed. So 0 operations. Output 0.

Sample 3: S="abac", T="abrc". Let's compute: positions: i=0: a→a, i=1: b→b, i=2: a→a, i=3: c→r. So f(a)=a (fixed), f(b)=b (fixed), f(c)=r. Now check condition: f(c)=r. Is r a fixed point? r is not in S. We can set f(r)=r. So condition holds: f(f(c)) = f(r) = r = f(c). So why is answer -1? Wait sample 3 says -1. Let's re-examine: S="abac", T="abrc". The letters in S are a,b,c. T is a,b,r,c. So for c, it maps to r. For r, it appears in T but not in S. The condition we derived says it's possible. But sample says impossible. Let's think: Operation: replace every occurrence of x in S with y. We want S to become T. S has a,b,a,c. We need c to become r. So we can do (c→r). That changes S to a,b,a,r. Then we have r at position 3, but T has r at position 3. So it matches! Wait, S becomes "abar"? Actually S="abac". Replace c with r: "abar". T="abrc". That's not equal. The third character is 'a' in S, but T has 'r' at position 2? Let's index: S: 0:a,1:b,2:a,3:c. T:0:a,1:b,2:r,3:c. So we need position 2 (a) to become r, and position 3 (c) to become c. So we need to change a to r, but keep c as c. But if we change a to r, we also change the a at position 0 to r, which is wrong. So we cannot change a to r because it appears elsewhere where it should stay a. The feasibility condition: for each original letter c, all occurrences in S must have the same target in T. Here letter 'a' appears at positions 0 and 2. In T, position 0 is 'a', position 2 is 'r'. So a has two different targets: a and r. Therefore impossible. Indeed, my earlier mapping f(a) was not well-defined because a appears with different T values. So the feasibility condition is: for each c in S, all T[i] where S[i]=c must be identical. If not, -1.

In sample 3, a appears at 0 and 2, T[0]=a, T[2]=r, conflict. So -1.

In sample 1, a appears at 0 and 5, both T are b. f appears at 1 and 3, both T are k. b appears at 2, T=c. d appears at 4, T=b. So all consistent.

Now sample 4: S="abac", T="bcba". Let's compute: S: a,b,a,c. T: b,c,b,a. For a: positions 0,2 → T[0]=b, T[2]=b → target b. For b: position 1 → T[1]=c → target c. For c: position 3 → T[3]=a → target a. So f(a)=b, f(b)=c, f(c)=a. This is a 3-cycle. Check condition: f(a)=b, f(b)=c, f(c)=a. For c, f(c)=a, but f(a)=b != c. So f(f(c)) = f(a) = b != f(c)=a. So violates the fixed-point condition. Thus impossible? But sample output is 4, not -1. Wait, sample 4 says answer is 4. Let's read sample 4 carefully:

Sample Input 4:
4
abac
bcba

Sample Output 4:
4

But we just argued that a→b, b→c, c→a is a cycle, which should be impossible. Let's test manually: S="abac". Want T="bcba". Can we do it? Operation: choose x,y replace all x with y. Try: we need a→b, b→c, c→a. Is there a sequence? Let's try: (c→a): S becomes "abaa". (a→b): S becomes "bbbb". (b→c): S becomes "cccc". Not good. Try (b→c): S becomes "acac". (c→a): S becomes "aaaa". (a→b): S becomes "bbbb". Not good. Try (a→b): S becomes "bbbc". (b→c): S becomes "cccc". (c→a): S becomes "aaaa". Not good. Try (c→a): "abaa". (a→b): "bbbb". (b→c): "cccc". No. It seems impossible to get "bcba". But the sample says 4. Let's re-examine the sample explanation? The problem statement only gives sample 4 input and output 4, but no explanation. Perhaps my analysis is wrong? Let's think again. Maybe the operation is different? It says: "Choose two lowercase English letters x, y and replace every occurrence of x in S with y." So it's a global substitution. So my model is correct. Why would sample 4 be possible? Let's try to find a sequence. We need S[0]=a → b, S[1]=b → c, S[2]=a → b, S[3]=c → a. So we need to transform a's to b, b's to c, c's to a. This is a cyclic permutation. Is there a way? Suppose we do (a→b): S becomes "bbbc". Now we have only b's and c. We need the first three to be b,c,b and last to be a? Wait T is "bcba": positions: 0:b,1:c,2:b,3:a. After (a→b), S="bbbc": positions 0:b,1:b,2:b,3:c. We need to change position 1 to c, position 3 to a. But we also need position 0,2 to be b (they are). So we need to change the b at position 1 to c, and the c at position 3 to a. But we cannot change just one b; we must change all b's or none. If we change all b's to something, we affect positions 0 and 2. So we need to change b to c, but that would make positions 0 and 2 become c, which is wrong. So we need to change b to c, but then later change some c's back to b? Let's see: after (a→b), S="bbbc". If we do (b→c): S becomes "cccc". All become c. Then we need to get back to "bcba". We could do (c→b) to get "bbbb". Not helpful. What if we do (c→a) first? S="abaa". Then (a→b): "bbbb". Then (b→c): "cccc". No. What about doing (b→c) first: S="acac". Then (a→b): "bcbc". Then (c→a): "baba". That's "baba", not "bcba". We have positions 0:b,1:a,2:b,3:a. We need 1:c,3:a. So we need to change the a at position 1 to c, and keep the a at position 3 as a. But all a's are the same. So we need to change a to c, but then position 3 also becomes c. So no.

Maybe the answer 4 is not for S="abac", T="bcba"? Let's check the sample input again: "4\nabac\nbcba\n" and output "4". The problem statement says sample output 4 is 4. But is it actually possible? Let's search memory: This problem is from AtCoder ABC 297 F? Or maybe it's ABC 285 F? Actually, I recall a problem: "Substring and Subsequence" no. Wait, there is a problem called "Substitution" where you can replace all occurrences of a character with another, and you want to make S equal to T. The answer is -1 if there's a conflict, otherwise count something. But I think the answer is the number of connected components in a graph minus something. Let me think: In AtCoder ABC 285 F? No.

Wait, I recall a problem: "String Equivalence" or "Make Them Equal". Actually, there is an AtCoder problem: "Substitution" (maybe ABC 302 F?). Let me think of the exact problem. There's a problem where you have two strings S and T, and you can choose a character c in S and replace it with another character d. But that's per occurrence. Here it's bulk.

Maybe the operation allows x=y? That does nothing, cost 1? Unlikely.

Wait, perhaps I misread sample 4. Let's re-express: N=4, S="abac", T="bcba". Could it be 4? Let's try a different approach: We can use intermediate letters. For example, we need a→b, b→c, c→a. We can do: a→x (some new letter), b→y, c→z, then x→b, y→c, z→a. But we only have 26 letters. However, the operation only allows replacing x with y where x and y are letters. We can use any letter, even if not in S or T. So we have 26 letters as "palette". So we could do: a→d (1), b→e (1), c→f (1), then d→b (1), e→c (1), f→a (1). That's 6 operations. But the answer is 4, so there is a better way.

Wait, maybe we can do: a→b (1), then b→c (1), then c→a (1). That's 3 operations. But as we saw, after a→b, S becomes "bbbc". Then b→c: "cccc". Then c→a: "aaaa". Not "bcba". So that doesn't work. But what if we interleave: a→b, c→a, b→c? Let's try: Step1: a→b. S="bbbc". Step2: c→a. S="bbba". (Since c at pos3 becomes a). Now S="bbba". Step3: b→c. S="ccca". Not good. Step3: a→c? S="bbbc"? No.

What about: b→c, a→b, c→a? Step1: b→c. S="acac". Step2: a→b. S="bcbc". Step3: c→a. S="baba". Not "bcba".

What about using the fact that we can choose any x,y, not necessarily related to S? For instance, we could introduce a new letter: a→x, then b→c, then x→b, then c→a? Let's try: Step1: a→d. S="dbdc". Step2: b→c. S="dcdc". Step3: d→b. S="bcbc". Step4: c→a. S="baba". Not "bcba". We have "baba". We need "bcba". So we need the second character to be c, but we have a. So we need to change that a to c. But that a came from d, which was b. Actually, in "baba", positions: 0:b,1:a,2:b,3:a. The a's are at 1 and 3. We need 1:c, 3:a. So we need to change a to c, but that would affect position 3. So not good.

What if we do: a→d, b→c, c→a, d→b? That's 4 ops: Step1: a→d. S="dbdc". Step2: b→c. S="dcdc". Step3: c→a. S="dada". Step4: d→b. S="baba". Same result.

What about a→b, b→d, d→c, c→a? That's 4 ops. Step1: a→b. S="bbbc". Step2: b→d. S="dddc". Step3: d→c. S="cccc". Step4: c→a. S="aaaa". No.

It seems impossible. But the sample says 4. Let's double-check the sample input and output. The problem statement given by the user includes four samples. Sample 4: Input: 4, abac, bcba. Output: 4. But maybe I misread the string? Could it be S="abac", T="bcba"? Or maybe T="bcba" but S is different? The user wrote: "Sample Input 4\n4\nabac\nbcba\nSample Output 4\n4". It's possible the sample is correct and my analysis is missing something. Let's think more deeply.

Maybe the operation is not "replace every occurrence of x in S with y", but "choose a character x in S and replace it with y"? No, the problem says "replace every occurrence of x in S with y". So it's global.

Wait, perhaps the operation can be applied to any string, and we can apply it multiple times, but the order matters. Could we do something like: a→b, then later b→a? But that would revert. But we need a net effect of a→b, b→c, c→a. Is there a way to achieve a cyclic permutation using bulk operations? Consider the group theory: The operation (x→y) generates a transformation on the set of strings. What is the group generated by these operations? Each operation is a function f_{x→y} that maps a string by replacing all x with y. The set of all such functions generates a monoid. We want to know if the permutation of letters (a→b, b→c, c→a) is in this monoid. Let's see: we can think of the effect on the letters. The initial string has letters a,b,a,c. The final string has b,c,b,a. This is a cyclic shift of the multiset? Actually, the multiset of S is {a,a,b,c}. T is {a,b,b,c}. So the multiset differs: S has two a's, T has two b's. So we need to change the a's to b's, and the b to c, and c to a. So it's a 3-cycle on the counts? Let's see: counts: S: a:2, b:1, c:1. T: a:1, b:2, c:1. So we need to decrease a by 1, increase b by 1, and keep c same? Wait, c: S has 1, T has 1. But we also need to change c to a. So c becomes a, adding one a. So net a: 2 (original) +1 (from c) = 3, but T has 1 a. So we need to lose two a's. So overall, we need to convert a→b (2 a's become b), b→c (1 b becomes c), c→a (1 c becomes a). The net change: a: 2 - 2 (converted) + 1 (from c) = 1. b: 1 - 1 (converted) + 2 (from a) = 2. c: 1 - 1 (converted) + 1 (from b) = 1. So the counts match! So it's possible in terms of counts. But can we achieve the exact positions? The operation is global, so the positions are determined by the original letters. After applying the cycle, each original letter becomes a specific other letter. So the transformation is a function from original letters to final letters. For the transformation a→b, b→c, c→a, the function is f(a)=b, f(b)=c, f(c)=a. This is a 3-cycle. As argued, such a function is not realizable because the operation is a projection onto fixed points. But wait, is it truly not realizable? Let's test with a smaller example: N=1, S="a", T="b". We can do (a→b). That works: f(a)=b, f(b)=b? Actually after operation, the string is "b". So the letter 'a' is gone, replaced by 'b'. So the transformation is a→b. That's a projection: f(a)=b, and f(b)=b. So it's not a cycle; b maps to itself. For N=2, S="ab", T="ba". This is a transposition. Can we do it? We need a→b and b→a. Let's try: (a→b): S becomes "bb". (b→a): S becomes "aa". Not "ba". (b→a): S becomes "aa". (a→b): S becomes "bb". So we cannot get "ba". So indeed, a 2-cycle is impossible. What about a 3-cycle with N=3? S="abc", T="bca". We need a→b, b→c, c→a. Try: (a→b): "bbc". (b→c): "ccc". (c→a): "aaa". Not "bca". (b→c): "acc". (a→b): "bcc". (c→a): "bba". Not "bca". So seems impossible.

But sample 4 says 4. So either my interpretation of the operation is wrong, or the sample is different. Let's read the problem statement again carefully: "Choose two lowercase English letters x, y and replace every occurrence of x in S with y." That's clear. "any number of times (possibly zero)". So it's a sequence of global replacements.

Maybe the operation can be applied to any string, not just S? No, it says "in S".

Wait, could it be that we are allowed to choose x and y such that we replace every occurrence of x in S with y, but we can also choose x=y, which does nothing but counts as an operation? That would be silly.

Maybe the sample 4 is actually possible with a clever sequence. Let's search my memory: There is a known problem: "You are given two strings S and T of length N. You can choose an index i and replace S[i] with any character." That's different. But here it's bulk.

Wait, I recall a problem: "Substitution" from AtCoder Beginner Contest 285 (Problem F?). Actually, ABC 285 F is "Substring of Sorted String". No. ABC 297 F? No. Let's think: There's a problem called "Make Them Equal" where you can replace all occurrences of a character with another, and you want to minimize operations. The answer is related to the number of connected components in a graph where you draw edges from S[i] to T[i]. Actually, I think the condition is: for each character c, if it appears in S, all its occurrences in T must be the same? No, the condition is: for each character c in S, there must exist a character d such that all positions where S[i]=c have T[i]=d. That is, the mapping from S letters to T letters is a function. That's necessary. But is it sufficient? As we saw with the 3-cycle, it is not sufficient because the function must be a projection. However, in the 3-cycle example, the mapping is a→b, b→c, c→a. This is a function, but it is not a projection. So it should be impossible. But sample 4 says it's possible with 4 operations. So maybe the function can be any function? Let's test the 3-cycle with a computer program in mind: can we achieve "bcba" from "abac" in 4 operations? Let's try to think of a sequence that works.

We want final S = "bcba". Let's denote the desired mapping: position 0: a→b, pos1: b→c, pos2: a→b, pos3: c→a. So we need a→b, b→c, c→a.

Consider using a temporary letter. For example, we can do:
1. a→x (where x is some letter not in {a,b,c}, say 'd'). S becomes "dbdc".
2. b→y (say 'e'). S becomes "dedc".
3. c→z (say 'f'). S becomes "dedf".
4. d→b, e→c, f→a? But that's more than 4 ops. We need exactly 4.

Maybe we can combine: after step 1, S="dbdc". We want to get to "bcba". We need d→b, b→c, c→a. But we have b and c in the string. Let's do step 2: b→c. S="dcdc". Step 3: d→b. S="bcbc". Step 4: c→a. S="baba". That's "baba", not "bcba". We have "baba". The second character is a, but we need c. The fourth is a, need a. So we need to change the second a to c. But we can't change just one a.

What if we use a different sequence:
1. a→b. S="bbbc".
2. c→a. S="bbba".
3. b→c. S="ccca".
4. a→b? S="cccb"? No.

1. a→b. S="bbbc".
2. b→d. S="dddc".
3. d→c. S="cccc".
4. c→a. S="aaaa". No.

1. b→c. S="acac".
2. a→d. S="dcdc".
3. c→a. S="dada".
4. d→b. S="baba". Same as before.

1. b→c. S="acac".
2. c→a. S="aaaa".
3. a→d. S="dddd".
4. d→b. S="bbbb". No.

What if we do:
1. a→b. S="bbbc".
2. c→d. S="bbbd".
3. b→c. S="cccd".
4. d→a. S="ccca". Not "bcba".

Maybe we need to use the fact that we can replace x with y where x=y? No.

Wait, maybe the operation is: choose x,y and replace every occurrence of x in S with y, but we can also choose x and y such that x is a letter that currently exists in S, and y is any letter. So the palette is all 26 letters. So we have 26 possible targets. In the 3-cycle, we need to map a to b, b to c, c to a. This is a permutation. Is it possible to achieve a permutation using these bulk operations? Let's think about the monoid generated by the operations f_{x→y}. Each operation is a projection onto the set of letters that are not x, union {y}. More precisely, the operation replaces all x's with y. So the image of the operation is the set of all letters except x, plus y. The effect on the letter set is: the letter x is "absorbed" into y. So the operation reduces the number of distinct letters in the string by at most 1 (if x is present). But we can also introduce new letters? No, we only replace x with y, so the set of letters after operation is (original set \ {x}) ∪ {y}. So if y is already present, the number of distinct letters may stay the same. If y is new, it may increase. But we are not restricted to the letters in the string; we can choose any y.

In the 3-cycle, we want to end up with the same set of letters as T: {a,b,c}. So we need to transform the multiset. But can we achieve a permutation? Let's consider the effect on the count of each letter. The operation (x→y) changes the count of x to 0, and adds the old count of x to the count of y. So it's a transfer of all mass from x to y. This is like moving tokens. We start with some distribution. We want to reach another distribution. This is possible if the final distribution is reachable by a sequence of such transfers. But we also care about the positions: the operation does not move letters arbitrarily; it replaces all x's with y, so the relative order of other letters is preserved. So the sequence of letters is determined by the original string and the sequence of operations. Since the operation is deterministic given the current string, the final string is a function of the original string and the operation sequence. The question is: for a given original string and target string, does there exist a sequence? And if so, what's the minimum length?

This is a known problem: AtCoder ABC 285 F? Actually, I think it's ABC 302 F: "Task and Bug" or something. Let me search my memory: There is a problem "Substitution" from AtCoder Regular Contest? Wait, I recall a problem: "You are given a string S. You can perform the following operation: choose two characters x and y, and replace all occurrences of x in S with y. Find the minimum number of operations to make S a palindrome." Not that.

Maybe it's from a contest: "AtCoder Beginner Contest 285 - F? No, 285 F is "Substring of Sorted String". 297 F is "Minimum Sum". 302 F is "Find the Forest". Not that.

Wait, I think it's AtCoder Beginner Contest 285 - D? No.

Let's think logically. The operation (x→y) is idempotent: applying it twice does nothing extra. Also, the order of operations matters only in that later operations override earlier ones for the letters involved. Specifically, the final letter at a position originally having letter c0 is determined by the last operation in the sequence that had source equal to the current letter at that time. This is similar to evaluating a composition of functions. As we process operations, each letter c has a current value. Initially v(c)=c. Operation (x→y): for all c with v(c)=x, set v(c)=y. So v is a function from original letters to current letters. The final string S' is given by S'[i] = v(S[i]). The goal is to achieve v(S[i]) = T[i] for all i.

So we need to find a function v: Σ→Σ such that v(S[i]) = T[i] for all i, and v can be obtained by a sequence of operations. As argued, the set of obtainable v is exactly the set of functions that are projections onto their image (i.e., idempotent: v(v(c)) = v(c)). Because each operation makes the function more "merged". Let's prove: Initially v0(c)=c, which is idempotent. Operation (x→y): new v(c) = y if v(c)=x, else v(c). So if v was idempotent, is new v idempotent? Suppose v'(v'(c)) = v'(c). If v(c) != x, then v'(c)=v(c), and v'(v(c)) = v(v(c)) = v(c) by idempotence of v. If v(c)=x, then v'(c)=y. Then v'(y) = y if y != x? Actually, we need to check: v'(y) = y if y != x and v(y) != x? Wait, v'(y) = y if v(y) != x, else if v(y)=x then v'(y)=y. So v'(y) = y always? Not necessarily: if v(y)=x, then v'(y)=y. If v(y)!=x, then v'(y)=v(y). But since v is idempotent, v(y) is either y or something that maps to y. In any case, v'(y) = y because either y maps to y or y maps to x and then to y. Let's compute: v'(c) = y. Then v'(v'(c)) = v'(y). If v(y) = x, then v'(y) = y. If v(y) != x, then v'(y) = v(y). But we need this to equal y. So we need v(y) = y. Is that guaranteed? Not necessarily. For example, suppose v is a→b, b→b. That's idempotent. Apply (b→c): new v: a→c, b→c. Is that idempotent? v'(a)=c, v'(c)=? c is not x (b), so v'(c)=v(c)=c. So v'(v'(a)) = v'(c) = c = v'(a). v'(b)=c, v'(c)=c. So idempotent. Another example: v is a→b, b→c, c→c. That's not idempotent because b→c, c→c, but a→b, so v(v(a))=v(b)=c = v(a)? Actually v(a)=b, v(b)=c, so v(v(a))=c. v(a)=b. So not idempotent. But can we get such v from operations? Starting from identity, apply (a→b): v1: a→b, others identity. That's idempotent. Apply (b→c): v2: a→c, b→c, others identity. Idempotent. So we cannot get a non-idempotent v. Indeed, each operation preserves idempotence. And any idempotent function can be achieved? Let's see: Given an idempotent function v, we can achieve it by processing each "tree" in the functional graph. Since v is idempotent, the graph consists of rooted trees where each root is a fixed point (v(r)=r) and all other nodes point directly to the root? Wait, idempotent means v(v(c)) = v(c). This means that for any c, v(c) is a fixed point. Because let d = v(c). Then v(d) = v(v(c)) = v(c) = d. So d is a fixed point. Therefore, the functional graph of an idempotent function has no directed cycles of length >1; every node points to a fixed point. And since v(d)=d, the fixed point is unique for each connected component? Actually, each component has exactly one fixed point (the root), and all other nodes point to it. But could a node point to another node that is not a fixed point? No, because v(c) must be a fixed point. So the graph is a set of stars: each component has a center r (fixed point) and leaves L where each leaf l has v(l)=r. There are no edges from leaves to other leaves, because if v(l)=r, then r is fixed. So indeed, the structure is exactly as I described: disjoint stars.

Now, is every such function achievable? Yes: for each star with root r and leaves L, we can apply operations to merge all leaves into r. As argued, we need |L| operations for that star. Since stars are disjoint (no letter appears in two stars), we can process each star independently, and the total operations is sum of |L| over all stars. The number of leaves across all stars is exactly the number of letters c such that v(c) != c. Because each non-root maps to a root. So the minimal number of operations is the number of non-fixed letters in the final mapping v.

But is that always achievable without interference? Yes, because the stars are on disjoint sets of letters. When we perform an operation (x→y), we only affect the star containing x. If we process each star separately, we can achieve the mapping. For example, for star with root r and leaves L, we can do: for each leaf l in L, apply (l→r). That costs |L| operations. After that, all leaves become r, and r remains r. So v is achieved. So any idempotent v is achievable with exactly |{c: v(c) != c}| operations.

Now, is it possible to achieve it with fewer operations? Suppose we have two leaves a,b in the same star (both map to r). Can we do it in 1 operation? If we do (a→b), then a becomes b. Now a and b both have value b. But we need them to have value r. So we still need to change b to r. So at least 2 operations. In general, to change k leaves to r, we need at least k operations because each operation can change at most one "new" leaf to r? Actually, an operation can change multiple leaves if they currently share the same value. For example, if we first merge a and b: (a→b), now a and b are both b. Then one operation (b→r) changes both to r. So 2 operations for 2 leaves. For k leaves, we can do a sequence of merges: first merge leaf1 and leaf2 (1 op), now they are leaf2. Then merge that with leaf3 (1 op), etc. Total k-1 merges to combine all leaves into one, plus 1 op to change that one to r, total k. So minimal is k. And we cannot do better because each leaf must undergo at least one "change" from its original value to r. However, could a leaf be changed indirectly without a direct operation on it? Yes, by being merged into another leaf that is later changed. That still counts as one operation (the merge) plus the final change. So total operations for a star with k leaves is at least k. And we can achieve k. So the formula holds.

Now, the crucial question: Given S and T, we need to find if there exists an idempotent function v such that v(S[i]) = T[i] for all i. If not, -1. If yes, the minimal operations is the number of c with v(c) != c.

But wait: is it always true that any such v must be idempotent? We argued that any sequence of operations yields an idempotent v. So if there is a sequence achieving S=T, then the final v is idempotent. Therefore, a necessary condition is that there exists an idempotent v with v(S[i]) = T[i]. So we need to find an idempotent v satisfying the constraints, and among those, we want to minimize the number of non-fixed letters. However, the constraints v(S[i]) = T[i] for all i may force certain assignments. For letters that never appear in S, we can choose v arbitrarily. For letters that appear in S, v is constrained.

So the problem reduces to: For each letter c that appears in S, let required(c) be the set of T[i] for positions where S[i]=c. If |required(c)| > 1, impossible. If |required(c)| = 1, let t_c be that unique target. Then we must have v(c) = t_c. However, we also need v to be idempotent. So for each c with v(c) = t_c, we need v(t_c) = t_c. That is, t_c must be a fixed point. So for any c with t_c != c, we need t_c to be a fixed point, meaning that either t_c does not appear in S (so v(t_c) can be t_c), or if t_c appears in S, then its required target must be t_c itself. In other words, if a letter t appears as a target for some c, and t also appears in S, then all occurrences of t in S must also map to t (i.e., t is a fixed point). If not, we have a conflict: v(t) would be forced to be something else, violating v(t)=t.

So the condition is: For each letter c in S, let t_c be the unique T value at positions where S=c. If c != t_c, then we must have that t_c is a fixed point. This means:
- If t_c appears in S, then for that letter t_c, we must have t_{t_c} = t_c (i.e., its target is itself).
- If t_c does not appear in S, we can set v(t_c) = t_c freely.

This is exactly the condition that there is no cycle of length >1 in the mapping from S letters to T letters. More precisely, define a directed graph on the letters that appear in S: for each c in S, if c != t_c, add a directed edge c → t_c. This graph must be acyclic (except possibly self-loops). Because if there is a cycle c1 → c2 → ... → ck → c1 with all edges c_i -> c_{i+1} and c_k -> c1, then we have v(c1)=c2, v(c2)=c3, ..., v(ck)=c1. Then v(v(c1)) = v(c2) = c3, but v(c1)=c2, so not idempotent unless c2=c3 etc., which would mean the cycle is length 1. So indeed, the graph must be a DAG where all edges eventually lead to a fixed point (a node with self-loop or no outgoing edge). Since each node has out-degree at most 1, the graph is a set of directed trees with edges pointing towards the root, and roots are fixed points (either self-loop or a node not in S). But if a root is not in S, we can set v(root)=root. So the condition is: there is no directed cycle of length >1 in the mapping from S letters to their target T letters.

In sample 4: S letters: a, b, c. T targets: a→b, b→c, c→a. This is a cycle a→b→c→a. So it violates the condition! Therefore, according to this logic, it should be impossible. But the sample says 4. So either my condition is wrong, or the sample is different, or the problem allows something else.

Let's re-read sample 4 from the problem statement as given by the user:

Sample Input 4
4
abac
bcba

Sample Output 4
4

Wait, could it be that the strings are S="abac", T="bcba"? Yes. But maybe I miscomputed the mapping. Let's list positions:
i=0: S[0]='a', T[0]='b' -> a→b
i=1: S[1]='b', T[1]='c' -> b→c
i=2: S[2]='a', T[2]='b' -> a→b
i=3: S[3]='c', T[3]='a' -> c→a
So mapping is a→b, b→c, c→a. Cycle of length 3.

But wait! Is it possible that we can achieve this with operations by using the fact that we can choose any y, not necessarily a letter that appears in S or T? For instance, we can use an intermediate letter d. Let's try to find a sequence of 4 operations that works. We need to end up with "bcba". Let's denote the string after each step.

Start: abac

Goal: bcba

We need to change the first a to b, second a to b, b to c, c to a. So we need a→b, b→c, c→a.

Consider the following sequence:
1. a→d. String: dbdc
2. b→c. String: dcdc
3. d→b. String: bcbc
4. c→a. String: baba

Result: baba. Not bcba.

What if we change the order:
1. b→c. String: acac
2. a→d. String: dcdc
3. c→a. String: dada
4. d→b. String: baba. Same.

What if we use a different intermediate:
1. a→b. String: bbbc
2. c→a. String: bbba
3. b→d. String: ddda
4. d→c. String: ccca. No.

1. a→b. String: bbbc
2. b→d. String: dddc
3. d→c. String: cccc
4. c→a. String: aaaa. No.

1. a→d. String: dbdc
2. d→b. String: bbbc
3. b→c. String: cccc
4. c→a. String: aaaa. No.

1. c→a. String: abaa
2. a→b. String: bbbb
3. b→c. String: cccc
4. c→d. String: dddd. No.

What if we don't use intermediates, just direct:
1. a→b. (bbbc)
2. b→c. (cccc)
3. c→a. (aaaa)
4. a→b. (bbbb). No.

Maybe we can do a sequence that doesn't simply apply the cycle in order, but uses the fact that after some operations, letters may have changed values, so we can target the new values. For example, to get c→a, we can do (c→a) at a time when c is present. But in the target, we need c at position 1 and a at position 3. So we need the original b to become c, and original c to become a. So we need to apply (b→c) and (c→a). But after (b→c), the original b is now c. Then if we apply (c→a), it will change all c's (including the newly converted b) to a. That would turn the original b into a, not c. So we need to apply (c→a) before (b→c)? But if we apply (c→a) first, original c becomes a. Then apply (b→c), original b becomes c. Then we have: original a is still a (if we didn't change it), original b is c, original c is a. So we get: a, c, a, a. That's "acaa". We need "bcba". So we also need to change a to b. But we have two a's: original a and original c. We need original a to be b, and original c to be a. So we need to change a to b, but not change the a that came from c. That's impossible because both are a's. So we need to differentiate them. How can we differentiate? By using an intermediate letter for one of them. For example, before changing a to b, we can change the a from c to something else. Let's try:
1. b→c. S="acac"
2. c→a. S="aaaa"
Now we have four a's. We need to end up with "bcba". We need to change the first a to b, second a to c, third a to b, fourth a to a. So we need to change a to b and c, but selectively. That's impossible with bulk operations on a. So we need to avoid merging the a's. How to avoid merging? We must not let the original c become a before we change the original a. So we should not do (c→a) early. Instead, we can do (a→b) first, then (c→a), then (b→c)? Let's try:
1. a→b. S="bbbc"
2. c→a. S="bbba"
3. b→c. S="ccca"
Now we have three c's and one a. We need "bcba". We have c,c,c,a. We need b,c,b,a. So we need to change the first c to b, and the second c to b, keep third c as c? Wait, positions: after step3, S="ccca": positions 0:c,1:c,2:c,3:a. Target: b,c,b,a. So we need pos0: c→b, pos1: c→c, pos2: c→b, pos3: a→a. So we need to change c to b, but only at positions 0 and 2, not 1. That's impossible because all c's are identical. So we need to avoid making the b at position 1 become c. So we should not change the b at position 1 to c. But in step3, we changed all b's to c. Position 1 was originally b, and we changed it to c. But we needed it to remain c in the final? Actually, in the target, position 1 is c. So that's good! Wait, target is b,c,b,a. So position 1 is c. After step3, position 1 is c. That's correct! Let's check step by step:
Start: a b a c
1. a→b: b b b c
2. c→a: b b b a
3. b→c: c c c a
Now S = c c c a. Target = b c b a.
We need to change the first c to b, second c to c (good), third c to b, and keep a as a.
So we need to change c to b, but not affect the second c. So we need to somehow protect the second c. How? By changing it to something else before changing c to b. But we only have one step left (we want total 4 operations, so one more). If we do (c→b), all c's become b, giving b b b a. Then we need to change the second b back to c, but that would require another operation. So 5 operations. Alternatively, we can do (c→d) and then (d→b) and (the other c to c)? No.

What if we use a different sequence:
1. a→b: b b b c
2. b→d: d d d c
3. d→c: c c c c
4. c→a: a a a a. No.

1. a→b: b b b c
2. b→d: d d d c
3. c→a: d d d a
4. d→b: b b b a. No.

1. a→b: b b b c
2. c→d: b b b d
3. b→c: c c c d
4. d→a: c c c a. Same as before.

1. a→d: d b d c
2. b→c: d c d c
3. d→b: b c b c
4. c→a: b a b a. No.

1. a→d: d b d c
2. d→b: b b b c
3. b→c: c c c c
4. c→a: a a a a. No.

1. a→d: d b d c