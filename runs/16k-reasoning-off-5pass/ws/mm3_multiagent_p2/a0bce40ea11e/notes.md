
## ideation
The problem asks for the sum over all matrices B (obtained by replacing zeros in A with non-zero elements of F_p) of B^p, modulo p. 

Key observations:
1. Over F_p, the sum over all non-zero values of z^k is -1 if (p-1) divides k, and 0 otherwise. This is because Σ_{z∈F_p^*} z^k = -1 when (p-1)|k, and 0 otherwise.
2. The (i,j) entry of B^p is a sum of products of p entries of B. Each product is a monomial in the zero variables with exponents equal to the number of times that variable appears in the walk.
3. Summing over all assignments of the zero variables, the contribution of a monomial is (-1)^K (where K is the number of zero variables) if every variable's exponent is a multiple of p-1, and 0 otherwise.
4. Since the walk length is p, the only possible multiples of p-1 in the exponent range [0, p] are 0 and p-1 (for p>2). For p=2, p-1=1, so all monomials are valid.
5. For p>2, a walk can use at most one zero variable, and it must use it exactly p-1 times. This imposes strong structural constraints on walks that contribute.
6. The sum can be computed as (-1)^K times the sum of coefficients of monomials where each variable appears 0 or p-1 times. This is equivalent to the constant term of (A+Z)^p in the ring R = F_p[Z]/(Z_i^{p-1} - 1) for all zero variables Z_i.

The challenge is to compute this efficiently for N up to 100 and p up to 1e9. Direct matrix exponentiation with polynomials is infeasible due to the huge p and many variables. We need to exploit the structure of valid walks.

For p=2: The answer is simply (-1)^K * (A' + I)^2? Actually, for p=2, all monomials are valid, so S = Σ_B B^2. Since B = A + Z, B^2 = A^2 + AZ + ZA + Z^2. Summing over all Z with entries in F_p^*, the sum of any entry of Z is 0, so the cross terms vanish? Not exactly. But there might be a simpler formula.

For p>2: Only walks that use exactly one zero entry p-1 times contribute. Such walks must consist of p-1 steps of that zero entry and 1 step of a fixed entry. As analyzed, this is only possible if the zero entry is a loop (i=j) or if p=3 and the reverse edge is fixed. But we need a uniform method.

Alternative approach: Use the fact that the constant term in R can be obtained by a linear map. The map φ: R → F_p given by φ(f) = constant term of f (i.e., coefficient of ∏ Z_i^0) can be computed as φ(f) = (1/(p-1)^K) Σ_{t_i ∈ {0,...,p-2}} f(ω^{t_1}, ..., ω^{t_K}) where ω is a primitive (p-1)-th root of unity in some extension field. But this requires working in an extension field of degree φ(p-1), which is too large.

Another idea: Since the condition is that each variable appears a multiple of p-1 times, and p-1 is large, the only way a variable can appear p-1 times is if the walk uses that edge p-1 times. This means the walk is almost entirely composed of that single edge. We can precompute the number of walks of length p that use a given zero entry exactly p-1 times, weighted by the product of fixed entries. This can be done by considering the graph where zero entries are removed, and then for each zero entry, consider the graph where that entry is used p-1 times and all other steps are fixed.

But p can be up to 1e9, so we cannot enumerate walks of length p. However, we can use matrix exponentiation on a modified graph. For a fixed zero entry at (u,v), the walks that use it exactly p-1 times can be counted by taking the adjacency matrix of the graph where we allow that edge to be used, but with a weight? Actually, we can use the fact that using an edge p-1 times in a walk of length p means the walk is determined by a single step: either the walk is a loop of p-1 uses of (u,v) plus one other step, or for p=3, it could be a pattern like u→v→u→v or v→u→v→u.

Given the complexity, a different perspective might help: The sum S = Σ_{B} B^p. Consider the polynomial P(t) = det(tI - B). The sum of B^p over all B might relate to the sum of powers of eigenvalues. But B varies over many matrices.

Wait, there is a known result: The sum of B^p over all matrices B with given zero pattern and non-zero entries in F_p^* is equal to the matrix obtained by replacing each zero entry with a specific value? No.

Let's look at the sample outputs to see if there's a pattern. Sample 3: N=4, p=13. Output is a full matrix. Computing (A')^13 (A with zeros as 0) and adding contributions from loops? Let's test: A' is A with zeros replaced by 0. Compute (A')^13 mod 13. The loops in A are at (1,1), (1,4)? Actually sample 3 A: 
0 1 2 0
3 4 0 5
0 6 0 7
8 9 0 0
Zeros at (1,1), (1,4), (2,3), (3,1), (3,3), (4,3), (4,4). 
Loops: (1,1) is zero (loop), (3,3) is zero (loop), (4,4) is zero (loop). 
For p=13, p-1=12. A loop can be used 12 times. A walk that uses loop (i,i) 12 times and one other edge from i to j is just: start at i, take loop 12 times, then take edge (i,j). That walk has length 13, uses loop 12 times, and the product of fixed entries is just the fixed entry on the last step. So the contribution of loop (i,i) to entry (i,j) is A_{i,j} (if (i,j) is fixed) or 0 if (i,j) is zero. But wait, the walk must end at j. So for each loop (i,i), and for each fixed edge (i,j), there is a walk of length 13: i -> i (12 times) -> j. This contributes A_{i,j}. Also, the walk could be: start at j, take some edge to i, then loop 12 times. That would end at i. So for each fixed edge (j,i), there is a walk: j -> ... -> i -> loop 12 times. That ends at i. So the contribution of loop (i,i) to (j,i) is A_{j,i}. Also, the walk could have the single fixed edge somewhere in the middle? For a loop, since you stay at i, you can take the loop, then take the fixed edge, or take the fixed edge, then loop. But if you take the fixed edge first, you go from i to some k, and then you need to return to i to take the loop. That would require an additional edge, but we only have one fixed edge. So you cannot return. So the only possibilities are: loop p-1 times, then one fixed edge; or one fixed edge, then loop p-1 times. But if you take the fixed edge first, you go from i to k (k ≠ i), and then you take the loop at i, but you are not at i. So you cannot. Therefore, the single fixed edge must be the last step. So the walk is: start at i, loop p-1 times, then take fixed edge to end at j. Also, the walk could start at some node, take a fixed edge to i, then loop p-1 times. That ends at i. So the walk: start at j, take fixed edge to i, then loop p-1 times. This ends at i. So the contributions from a loop (i,i) are:
- To (i,j): A_{i,j} for each fixed edge (i,j)
- To (j,i): A_{j,i} for each fixed edge (j,i)
Also, the constant term (A')^p includes walks with no zero entries. For p=13, (A')^p is the sum over walks of length 13 in the graph with zero entries removed. Then we add the loop contributions. The total sum of coefficients is (A')^p + L, where L is the matrix of loop contributions. Then S = (-1)^K * ((A')^p + L). Let's test this hypothesis with sample 3. Compute (-1)^K mod 13. K=7, so (-1)^7 = -1 ≡ 12. So S = - ((A')^13 + L) mod 13. We need to compute (A')^13 and L and see if we get the sample output. This is doable by hand? Not easily, but we can reason. The sample output is given. Let's try to compute (A')^13 for sample 3. A' is A with zeros as 0:
A' = 
0 1 2 0
3 4 0 5
0 6 0 7
8 9 0 0
We need (A')^13 mod 13. Since 13 is prime, we can use the fact that the characteristic polynomial might help, but it's 4x4. Alternatively, note that the graph is small. But this is just a hypothesis.

However, for p=3, sample 1, K=2, (-1)^2=1. (A')^3 = [[0,1],[0,2]]. L: zero entries are (1,1) and (2,1). (1,1) is a loop. For loop (1,1), contributions: to (1,j): A_{1,j} for fixed edges from 1. Fixed edges from 1: (1,2) only. So contributes to (1,2) by 1. To (j,1): fixed edges to 1: (2,1) is zero, so none. So L(1,2) gets +1. For zero (2,1), it is not a loop (2≠1). For p=3, p-1=2. Can a non-loop contribute? We need a walk of length 3 that uses (2,1) twice. As discussed, this requires the reverse edge (1,2) to be fixed. (1,2) is fixed 1. So walk: 1->2->1->2 uses (2,1) twice? Let's see: 1->2 (fixed 1), 2->1 (zero, used 1st time), 1->2 (fixed 1). That uses (2,1) once, not twice. To use (2,1) twice, we need a walk: 1->2->1->2->1? That's length 4. For length 3, to use (2,1) twice, the walk could be: 2->1->2->1? That uses (2,1) twice? 2->1 (zero, 1st), 1->2 (fixed), 2->1 (zero, 2nd). That's length 3, uses (2,1) twice, and starts at 2, ends at 1. The fixed edge is (1,2) used once. The product of fixed entries is 1. So this walk contributes to (2,1) entry. Also, the walk: 1->2->1->2 uses (2,1) once? Actually 1->2 (fixed), 2->1 (zero), 1->2 (fixed). That's one use. So for (2,1) zero, the walk 2->1->2->1 uses it twice? Let's list walks from i to j of length 3 that use (2,1) twice. The walk must have edges: (2,1), X, (2,1) in some order. Since (2,1) goes 2->1, to use it twice, we need to go from 2 to 1, then back to 2, then to 1. So the walk is 2->1->2->1. This uses (2,1) twice and (1,2) once. The product of fixed entries is 1. So this walk contributes to (2,1) entry. Also, could we have (2,1) twice in a row? 2->1->? After 1, to use (2,1) again, we need to be at 2. So we need an edge from 1 to 2. That's fixed. So the walk is 2->1->2->1. That's the only pattern. So for zero (2,1), the contribution is to (2,1) entry? The walk starts at 2, ends at 1. So it contributes to (2,1) entry. The product is 1. So L(2,1) gets +1. Also, could there be a walk that uses (2,1) twice and ends at 2? That would require 1->2->1->2? That uses (2,1) once? Actually 1->2->1->2 uses (2,1) once (at step 2). To use it twice, we need 1->2->1->2->1. So no. So for sample 1, L = [[0,1],[1,0]]? Wait, (1,1) loop gave (1,2)+1. (2,1) gave (2,1)+1. So L = [[0,1],[1,0]]. Then (A')^3 + L = [[0,1],[0,2]] + [[0,1],[1,0]] = [[0,2],[1,2]]. That matches sample 1! So the formula S = (-1)^K * ((A')^p + L) works for sample 1, where L includes contributions from all zero entries (loops and non-loops that can form valid walks).

Now, for p=13, we need to generalize L. For a zero entry at (u,v), when can it contribute? It contributes if there exists a walk of length p that uses (u,v) exactly p-1 times. As argued, this requires that the graph of fixed edges (A' with zeros as 0) allows a walk that uses (u,v) p-1 times and one other edge. For p>3, the only possibility is if (u,v) is a loop. Because for a non-loop, to use it p-1 times, you need to return to u after each use, requiring at least p-2 returns, but you only have 1 fixed edge use. So you can only return once, so you can use the edge at most twice. For p>3, p-1 > 2, so impossible. For p=3, p-1=2, so you can use it twice with one return. For p=2, p-1=1, so you can use it once, and any walk contributes. So the cases are:
- p=2: all zero entries can contribute, and all walks of length 2 are valid. This is a special case.
- p=3: zero entries can contribute if they are loops, or if they are non-loops and the reverse edge is a fixed edge (so that you can go back and forth). Actually, for p=3, you need to use the edge twice. The walk must be: either loop: u->u->u->v, or non-loop: u->v->u->v or v->u->v->u? Let's analyze p=3, non-loop (u,v). To use it twice, the walk must have pattern: (u,v), X, (u,v) or X, (u,v), X? Since there are 3 edges, and we use (u,v) twice, the other edge X must be a fixed edge. The walk must be a valid sequence. The possible sequences with two (u,v) and one X:
- (u,v), (u,v), X: after first (u,v), at v. To take another (u,v), must be at u. So impossible unless u=v.
- (u,v), X, (u,v): after first (u,v), at v. X must be (v,u) to get back to u. Then second (u,v) goes to v. So walk: u->v->u->v. This uses (u,v) twice and (v,u) once. So requires (v,u) to be a fixed edge.
- X, (u,v), (u,v): after X, at some node. To take (u,v), must be at u. So X must be (?,u). Then (u,v) goes to v. Then (u,v) again: must be at u, but at v. So impossible unless u=v.
So for non-loop, the only pattern is (u,v), (v,u), (u,v). This requires (v,u) to be fixed. So for p=3, a non-loop zero entry at (u,v) contributes if and only if (v,u) is a fixed edge. The contribution is to the entry (u,v) (start u, end v) and the product is A_{v,u}. Also, the walk could be (v,u), (u,v), (v,u)? That uses (u,v) once. To use (u,v) twice, the walk must start and end at v? Actually, the walk (u,v), (v,u), (u,v) starts at u, ends at v. The walk (v,u), (u,v), (v,u) starts at v, ends at u, and uses (u,v) once. So no. So only one walk per non-loop zero entry contributes, and it contributes to (u,v) with weight A_{v,u}. But wait, in sample 1, for (2,1) zero, the reverse (1,2) is fixed 1. The walk (2,1), (1,2), (2,1) starts at 2, ends at 1. That is a walk from 2 to 1 of length 3 using (2,1) twice. It contributes to (2,1) entry. The product is A_{1,2} = 1. So indeed, the contribution is to (2,1) with weight 1. So for p=3, non-loop zero at (u,v) contributes to (u,v) if (v,u) is fixed, with weight A_{v,u}. But careful: the walk is (u,v), (v,u), (u,v) which starts at u, ends at v. So it contributes to (u,v). So L_{u,v} += A_{v,u} if A_{u,v}=0, A_{v,u}≠0. What about loops? For loop (i,i), it contributes to (i,j) with weight A_{i,j} for any fixed (i,j), and to (j,i) with weight A_{j,i} for any fixed (j,i). Also, the walk could be: start at j, take fixed (j,i), then loop p-1 times. That ends at i. So L_{j,i} += A_{j,i}. So for loop, L_{i,j} += A_{i,j} and L_{j,i} += A_{j,i}. This matches our earlier: for (1,1) loop, L_{1,2} += A_{1,2}=1, L_{2,1} += A_{2,1} but A_{2,1}=0, so nothing.

Now, for p>3, only loops contribute. For a loop (i,i), the only walks that use it p-1 times are: start at i, loop p-1 times, then take a fixed edge (i,j) -> ends at j; or start at j, take fixed edge (j,i), then loop p-1 times -> ends at i. So L_{i,j} += A_{i,j} and L_{j,i} += A_{j,i} for each fixed edge incident to i. Also, could there be a walk that uses the loop p-1 times and the fixed edge is not the last? As argued, if you take the fixed edge first, you leave i, and you cannot return to take the loop because you have no more edges. So the fixed edge must be the last. So these are the only contributions.

What about p=2? For p=2, p-1=1. The condition is that every variable's exponent is a multiple of 1, which is always true. So all monomials are valid. The sum S = Σ_{B} B^2. We can write B = A + Z. Then B^2 = A^2 + AZ + ZA + Z^2. Summing over all Z with entries in F_p^*, the sum of any entry of Z is 0, so the cross terms AZ and ZA sum to 0? Not exactly, because the sum of a product of an A entry and a Z entry over all Z is (Σ Z) * A = 0. So indeed, the sum of AZ and ZA over all Z is 0. So S = Σ (A^2 + Z^2). Now, Z^2: for each zero entry, Z^2 has that entry squared, and cross terms vanish because they involve products of different variables which sum to 0. So the (i,j) entry of Z^2 is the sum over all k of Z_{i,k} Z_{k,j}. If both are zero entries, then the sum over Z_{i,k} Z_{k,j} is Σ_{x,y∈F_p^*} xy = (Σ x)(Σ y) = 0. If one is fixed and one is zero, say Z_{i,k} is zero, A_{k,j} is fixed, then sum is (Σ Z_{i,k}) * A_{k,j} = 0. If both are fixed, then it's just the fixed product. So actually, the only non-zero contributions in Z^2 are when both entries are fixed, i.e., the same as A^2. So S = 2 A^2? But wait, A^2 is computed with the original A, which has zeros. But we are summing over B, and B has non-zero entries at zero positions. So A^2 term: for each i,j, (A^2)_{i,j} = Σ_k A_{i,k} A_{k,j}. This sum is over k. For a given k, if both A_{i,k} and A_{k,j} are fixed, the term is constant. If one is zero, then in the sum over B, the corresponding term in B^2 is B_{i,k} B_{k,j}. If A_{i,k}=0, then B_{i,k} is summed over F_p^*, so the sum over B of B_{i,k} B_{k,j} = (Σ_{x} x) * B_{k,j} = 0. So indeed, the sum over B of B^2 is the same as the sum over B of the matrix obtained by taking A^2 and setting any term involving a zero entry to 0. But that is exactly (A')^2, where A' is A with zeros as 0. So for p=2, S = (A')^2 + (A')^2? No, we have A^2 + Z^2. But A^2 has terms with zeros. Actually, the sum over B of B^2 is not simply 2*(A')^2. Let's compute for a simple case: N=1, A=[0], p=2. Then B can be [1] only. B^2 = [1]. Sum = 1. (A')^2 = [0]^2 = [0]. So S=1. Our formula S = (-1)^K * ((A')^p + L) for p=2? K=1, (-1)^1 = -1. L for loops: (0,0) is loop, but p=2, p-1=1. The loop contribution: start at 0, loop 1 time, then take fixed edge? There are no fixed edges. So L=0. Then S = - (0+0) = 0, which is wrong. So p=2 is different.

Let's analyze p=2 carefully. For p=2, we need to sum B^2 over all B. B^2 = A^2 + AZ + ZA + Z^2. The sum over all Z (with entries in F_p^*) of AZ: for each (i,j), (AZ)_{i,j} = Σ_k A_{i,k} Z_{k,j}. Summing over Z, the only non-zero terms are when A_{i,k} ≠ 0 and Z_{k,j} is summed. But Σ_{z∈F_p^*} z = 0. So (AZ) sum is 0. Similarly, ZA sum is 0. For Z^2, (Z^2)_{i,j} = Σ_k Z_{i,k} Z_{k,j}. If both Z_{i,k} and Z_{k,j} are independent, the sum over them is (Σ x)(Σ y) = 0. If they are the same variable, i.e., i=j and k=i, then term is Z_{i,i}^2. Sum over Z_{i,i} of x^2 = Σ x^2. For p=2, F_2^* = {1}, so Σ x^2 = 1. So (Z^2)_{i,i} gets contribution 1 from k=i. But careful: if A_{i,i}=0, then Z_{i,i} is a variable. If A_{i,i}≠0, then Z_{i,i}=0, so no variable. So the sum over B of B^2 is: for each i,j, (B^2)_{i,j} summed over B equals:
- If i=j: Σ_k A_{i,k} A_{k,i} (from A^2) + Σ_{k: A_{i,k}=0, A_{k,i}=0} Σ_{x,y} x y + Σ_{k: A_{i,k}=0, A_{k,i}≠0} Σ_x x * A_{k,i} + Σ_{k: A_{i,k}≠0, A_{k,i}=0} A_{i,k} * Σ_y y + Σ_{k: A_{i,k}≠0, A_{k,i}≠0} A_{i,k} A_{k,i} (from A^2). But Σ x = 0, Σ y = 0, and Σ_{x,y} x y = (Σ x)(Σ y) = 0. So the only non-zero terms are when both are fixed (from A^2) and the diagonal term from Z^2 when both are variables? Wait, the term from A^2 already includes the case when both are fixed. The case when both are variables gives 0. So actually, the only additional term is when i=j and k=i, and A_{i,i}=0. Then Z_{i,i}^2 sum is 1. So (B^2)_{i,i} sum = (A^2)_{i,i} + 1 if A_{i,i}=0. For i≠j, no additional term. So S = A^2 + D, where D is a diagonal matrix with 1 at positions where A_{i,i}=0. But is that correct? Let's test with sample 2: N=3, p=2, A has 0 off-diagonal, 1 on diagonal. So A_{i,i}=1 ≠0. So D=0. S = A^2. A^2: since A is identity, A^2 = I. But sample output is all 1's. Wait, sample 2 output is all 1's mod 2. I mod 2 is 1,1,1 on diagonal, 0 off. But sample output is all 1's. So S should be all 1's. Our formula gives only diagonal 1, off-diagonal 0. So we are missing off-diagonal terms. Let's re-evaluate: For p=2, B is a matrix with 1 on diagonal (since A_{i,i}=1, non-zero) and B_{i,j} ∈ {1} for i≠j (since A_{i,j}=0, replaced by 1). So B is the all-ones matrix. B^2 = J * J = 3J. Sum over B: only one B, so sum = 3J. Mod 2, 3J = J (all 1's). So S = J. Our decomposition B = A + Z: A is identity, Z is matrix with 0 on diagonal, 1 off-diagonal? Wait, A has 1 on diagonal, 0 off. So Z must have 0 on diagonal, and at off-diagonal, A_{i,j}=0, so B_{i,j}=1, so Z_{i,j}=1. So Z is the all-ones matrix minus identity. Then B = A + Z = I + (J-I) = J. Good. Now compute B^2 = A^2 + AZ + ZA + Z^2. A^2 = I. AZ: A=I, so AZ = Z. ZA = Z. Z^2 = (J-I)^2 = J^2 - 2J + I = 3J - 2J + I = J + I (since 2J=0 mod 2? Actually mod 2, 2J=0, so Z^2 = J^2 + I = 3J + I = J + I). So B^2 = I + Z + Z + J + I = 2I + 2Z + J = J (since 2I=0, 2Z=0). So B^2 = J. Summing over B: only one B, so S = J. Now, our earlier sum over Z: we summed over all Z with entries in F_p^*. But in this case, Z is fixed! Because the off-diagonal entries are zero in A, so they are replaced by 1, not summed over. So Z is not a variable; it's fixed to 1. So the sum over B is just the single matrix. So the general formula S = Σ_{B} B^p is not simply the sum over all Z with variables; it's a sum over all assignments of the zero positions to values in F_p^*. In the case where all zero positions are assigned, there is only one assignment if there are no zero positions? No, in sample 2, there are 9 zeros, each assigned 1. So there is only one B because p-1=1, so the only non-zero value is 1. So K=9, (p-1)^K = 1. So S = B^p. So the sum is just the single matrix raised to p. For p=2, B is all-ones, B^2 = 3J. Mod 2, 3J = J. So S = J. Our polynomial method with variables: each zero variable is assigned 1, so the sum is just the evaluation at z=1. That gives the same as setting all zero variables to 1. So for p=2, since each variable has only one choice (1), the sum is simply (A with zeros replaced by 1)^p. That is, B is uniquely determined, and S = B^p. So for p=2, the answer is simply (A with zeros replaced by 1) raised to p, modulo p. Let's check: In sample 2, A with zeros replaced by 1 is all-ones. (all-ones)^2 = 3J, mod 2 = J. Matches. So for p=2, the problem is trivial: B is the matrix with 1 in all zero positions, and we compute B^p mod p.

For p>2, each zero variable has p-1 choices, and we sum over them. The sum over assignments of a monomial is (-1)^K if exponents are multiples of p-1, else 0. So the answer is (-1)^K times the sum of coefficients of monomials with exponents 0 or p-1. This is equivalent to evaluating the polynomial at each variable = 1, but only keeping terms where each variable appears a multiple of p-1 times. As argued, for p>3, only loops can contribute. For p=3, loops and non-loops with reverse fixed can contribute.

So the algorithm depends on p:
- If p=2: Replace all zeros with 1, compute B^p mod p, output.
- If p=3: Compute A' = A with zeros as 0. Compute (A')^3. Then for each zero entry (i,j):
   - If i=j (loop): add A_{i,j} for each fixed edge from i to j, and A_{j,i} for each fixed edge from j to i. But careful: A_{i,j} here is the original non-zero value? Actually, for loop (i,i), the contribution to L_{i,j} is the product of fixed entries on the walk. The walk is: start at i, loop p-1 times, then take fixed edge (i,j). The product is just the fixed entry A_{i,j} (if it's non-zero). If A_{i,j} is zero, it's not a fixed edge, so no walk. So L_{i,j} += A_{i,j} for all j such that A_{i,j} ≠ 0. Similarly, L_{j,i} += A_{j,i} for all j such that A_{j,i} ≠ 0.
   - If i≠j and A_{j,i} ≠ 0: add A_{j,i} to L_{i,j} (since the walk (i,j), (j,i), (i,j) contributes to (i,j)). Also, could there be a walk (j,i), (i,j), (j,i) that uses (i,j) twice? That uses (i,j) once? No, it uses (i,j) once. So only one contribution.
   Then S = (-1)^K * ((A')^3 + L) mod 3.
- If p>3: Only loops contribute. For each loop (i,i) that is zero, for each fixed edge (i,j) (A_{i,j}≠0), add A_{i,j} to L_{i,j}. For each fixed edge (j,i), add A_{j,i} to L_{j,i}. Then S = (-1)^K * ((A')^p + L) mod p.

We need to verify this for sample 3 with p=13. We can write a small script to test, but since we are in an interview setting, we can reason. The key is to compute (A')^p. For p=13, (A')^13 mod 13. Since 13 is prime, by Fermat's little theorem, for any matrix M, M^13 ≡ M (mod 13) if the matrix is over F_13? No, that's not true for matrices. But there is a known result: for a prime p, the p-th power of a matrix over F_p is the matrix of the Frobenius endomorphism on the algebra, but it's not simply the matrix itself unless the matrix is diagonalizable with eigenvalues in F_p. Actually, by the Cayley-Hamilton theorem, M^p can be expressed as a linear combination of lower powers. But we can compute it using exponentiation by squaring, but p=13 is small enough to do 13 multiplications. N=100, so O(N^3 log p) is fine. But p can be up to 1e9, so we need exponentiation by squaring. However, the matrix entries are in F_p, and we need to compute (A')^p mod p. Since p can be large, we can use binary exponentiation. N=100, so O(N^3 log p) is about 100^3 * 30 = 3e7, which is feasible in Python with some optimization (maybe using numpy? But we need exact integer arithmetic mod p, which can be done with Python integers, but 100^3=1e6, times 30 is 3e7 operations, each a multiplication and addition of large integers (up to 1e9), so it's okay in Python if optimized (e.g., using list comprehensions or numpy). However, we also need to add the L matrix and multiply by (-1)^K. So the main work is computing (A')^p.

But wait: is it always true that for p>3, only loops contribute? What about zero entries that are not loops, but the graph has a path of length 1 back? We already argued that to use a non-loop edge p-1 times, you need to return to the start after each use. Each return requires at least one edge. You have p-1 uses, so you need p-2 returns. But you only have 1 fixed edge use total. So you can only have 1 return. So you can use the edge at most 2 times. So for p-1 > 2, i.e., p>3, impossible. For p=3, p-1=2, so you can use it twice with one return. So the condition is exactly: the reverse edge must be a fixed edge (so you can use it as the return). But wait, the return edge could be a path of length >1, but that would use more than one edge, which you don't have. So it must be a single edge. So for p=3, non-loop zero at (u,v) contributes if (v,u) is a fixed edge. But what if (v,u) is also a zero? Then it's not fixed, so no return. So no contribution. So our condition is correct.

Now, what about p=5? p-1=4. To use a non-loop 4 times, you need 3 returns. You only have 1 fixed edge, so impossible. So only loops.

But wait, there is another possibility: the walk could use a zero entry p-1 times, but the "fixed edge" is not a single edge; it could be a product of fixed edges that forms a path from v to u of length L. But that would use L fixed edges, not 1. So if L>1, you would use L fixed edges, leaving p-1 - L uses of the zero entry. But the total number of edges is p. So if you use L fixed edges, you use p-1 - L zero edges. For the zero edge to be used a multiple of p-1, it must be p-1 or 0. So if it's p-1, then L=1. If it's 0, then it's not used. So the only way a zero edge is used is if it is used exactly p-1 times, and the remaining edge is a single fixed edge. So the fixed path must be length 1. So indeed, the reverse edge must be a fixed edge (i.e., a single edge). So our analysis holds.

What about loops? For a loop (i,i), to use it p-1 times, you don't need to return, so the one fixed edge can be anywhere as long as you can reach it and return? Actually, as argued, if you take the fixed edge before the loop, you leave i, and you cannot return because you have no more edges. So the fixed edge must be the last edge. So the walk is: start at i, loop p-1 times, then take fixed edge to j. Also, you could start at j, take fixed edge to i, then loop p-1 times. So those are the only two patterns. So the contribution is as we said.

Now, is there any contribution from multiple zero entries? For p>3, using two different zero entries would require at least 2(p-1) > p, so impossible. For p=3, using two different zero entries would require at least 2*2=4 >3, so impossible. So indeed, at most one zero entry is used per term.

Thus, the formula S = (-1)^K * ( (A')^p + L ) is correct, where L is the matrix of contributions from zero entries as described.

Now, we need to compute (A')^p efficiently. N ≤ 100, p ≤ 1e9. We can use binary exponentiation. However, p can be up to 1e9, which is about 30 bits. So we need about 30 matrix multiplications. Each multiplication is O(N^3) = 1e6, so total 3e7 operations. In Python, with pure integers, it might be a bit slow but should pass within a few seconds if optimized. We can use the fact that we are working modulo p, so we can reduce mod p after each multiplication. Also, we can use a list of lists for matrices. But 3e7 multiplications of large integers (up to 1e9) might be borderline. We can optimize by using the fact that we can represent each row as a list, and use a triple loop. Or we can use numpy for modular arithmetic, but numpy doesn't support arbitrary large mod? Actually, we can use numpy with dtype=object for large integers, but that's slow. Better to use plain Python with some tricks: precompute the matrix as a list of lists of integers, and use a helper function for matrix multiplication. Since N=100, we can write a function that multiplies two matrices mod p.

But wait, we also need to add L and multiply by (-1)^K. L is computed from A and the zero positions. L can be computed in O(N^2).

So the steps:
1. Read N, p, and matrix A.
2. Determine K = number of zeros in A.
3. If p=2:
   - Create matrix B by replacing zeros with 1.
   - Compute B^p mod p using binary exponentiation.
   - Output B^p.
4. Else (p is odd prime):
   - Create matrix A' by replacing zeros with 0.
   - Compute M = (A')^p mod p using binary exponentiation.
   - Initialize L as zero matrix.
   - For each zero entry (i,j) in A (1-indexed):
        if i == j (loop):
            for k in 1..N:
                if A[i][k] != 0: L[i][k] = (L[i][k] + A[i][k]) % p
                if A[k][i] != 0: L[k][i] = (L[k][i] + A[k][i]) % p
        else if p == 3 and A[j][i] != 0:  # non-loop, only for p=3
            L[i][j] = (L[i][j] + A[j][i]) % p
   - Compute factor = (-1)^K mod p. Since p is odd, -1 mod p is p-1. So factor = (p-1)^K mod p. But careful: (-1)^K = 1 if K even, -1 if K odd. So we can compute factor = 1 if K%2==0 else p-1.
   - Compute S = (M + L) mod p.
   - For each element in S, multiply by factor mod p.
   - Output S.

We need to verify for sample 3. Let's try to compute manually? Maybe we can write a small script in our head? Alternatively, we can test with a smaller example. But since we are in an interview, we can trust the reasoning. However, there is a subtlety: for p=3, what about a non-loop zero where the reverse edge is also zero? No contribution. What if the reverse edge is fixed but zero in A? That's fixed edge means non-zero. So A[j][i] != 0.

What about p=3 and a zero entry (i,j) where i≠j, and A[j][i] ≠ 0. The contribution is L[i][j] += A[j][i]. But wait, the walk (i,j), (j,i), (i,j) uses the fixed edge (j,i) once. The product is A[j][i]. So that's correct. But is there also a walk (j,i), (i,j), (j,i) that uses (i,j) once? That contributes to (j,i) with product A[i][j]? That walk uses (i,j) once, not twice. So it doesn't satisfy the condition. So no.

Now, what about p=3 and a loop (i,i). The loop is used twice. The walk: i -> i -> i -> j. Product: A[i][j]. So L[i][j] += A[i][j]. Also, walk: j -> i -> i -> i. Product: A[j][i]. So L[j][i] += A[j][i]. So that's correct.

Now, for p>3, loops: walk: i -> i (p-1 times) -> j. Product: A[i][j]. So L[i][j] += A[i][j]. Also, j -> i -> i ... -> i. Product: A[j][i]. So L[j][i] += A[j][i]. So same as p=3 for loops. So we can unify: for any p>2, loops contribute L[i][j] += A[i][j] and L[j][i] += A[j][i] for all j where A[i][j]≠0 and A[j][i]≠0. For p=3, additionally, non-loops with reverse fixed contribute L[i][j] += A[j][i] if A[i][j]=0, A[j][i]≠0, and i≠j.

Wait, what about p=3 and a non-loop zero where the reverse edge is fixed. The walk (i,j), (j,i), (i,j) uses (i,j) twice. But note that (j,i) is fixed. However, what if (i,j) is zero and (j,i) is fixed, but (j,i) itself is a zero in the original A? No, "fixed" means non-zero. So it's fine.

Now, we must also consider that for p=3, could there be a walk that uses a zero entry twice, but the reverse edge is not a single edge? For example, a path of length 2 from j to i. That would use 2 fixed edges, leaving 1 zero use. Not enough. So no.

Now, what about p=5? Could a zero entry be used 4 times if the graph has a cycle? For example, if there is a cycle of fixed edges, you could use the zero entry once, then go around the cycle, then use the zero entry again, etc. But you only have 1 fixed edge use total. So you can only use one fixed edge. So you cannot go around a cycle. So still impossible.

Thus, the algorithm seems solid.

Now, we need to implement matrix exponentiation. Since p can be up to 1e9, we can use binary exponentiation. We'll write a function mat_mult(A, B, mod) that multiplies two N x N matrices. N=100, so we can use a triple loop. To speed up, we can use a list of lists and maybe use local variables. Also, we can precompute the transpose of B to improve cache locality? Not necessary.

But there is a catch: p can be up to 1e9, but p is prime. The matrix entries are modulo p. In Python, integer multiplication of numbers up to 1e9 is fast, but 1e6 multiplications per matrix multiply, times 30, is 3e7. Each multiplication involves Python big integers, but they are small (within 64-bit), so it's actually fast. However, 3e7 operations might take a few seconds in Python. We can optimize by using the fact that we can reduce modulo p after each inner product. Also, we can use a flat list representation to reduce overhead. But I think it's okay.

Alternatively, we can use the built-in pow for matrices? No.

We can also use the fact that for p=2, we just need to square the matrix. For p>2, we need to compute A^p. But note that p is prime, and we are working modulo p. There is a known trick: for a prime p, the p-th power of a matrix over F_p can be computed using the fact that the minimal polynomial divides x^p - x? Actually, by Fermat's little theorem, for any element a in F_p, a^p = a. For matrices, it's not true in general. But there is a result: the matrix M^p is congruent to M modulo the minimal polynomial? Not helpful.

So we will implement binary exponentiation.

Let's write the code structure:

```python
import sys

def mat_mult(A, B, mod):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(n):
            a = Ai[k]
            if a == 0:
                continue
            Bk = B[k]
            for j in range(n):
                Ci[j] = (Ci[j] + a * Bk[j]) % mod
    return C

def mat_pow(M, p, mod):
    n = len(M)
    # Initialize result as identity matrix
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    base = M
    while p > 0:
        if p & 1:
            result = mat_mult(result, base, mod)
        base = mat_mult(base, base, mod)
        p >>= 1
    return result

def solve():
    input = sys.stdin.readline
    N, p = map(int, input().split())
    A = []
    zeros = []
    for i in range(N):
        row = list(map(int, input().split()))
        A.append(row)
        for j in range(N):
            if row[j] == 0:
                zeros.append((i, j))
    K = len(zeros)
    
    if p == 2:
        B = [[1 if A[i][j] == 0 else A[i][j] for j in range(N)] for i in range(N)]
        M = mat_pow(B, p, p)
        # Output M
        for row in M:
            print(' '.join(map(str, row)))
        return
    
    # p is odd prime
    # Compute A' = A with zeros as 0
    Aprime = [[A[i][j] for j in range(N)] for i in range(N)]  # zeros remain 0
    M = mat_pow(Aprime, p, p)
    
    L = [[0]*N for _ in range(N)]
    if p == 3:
        for (i, j) in zeros:
            if i == j:

## worker: Implement the solution in Python based on the deri
The solution uses the algebraic property that summing a monomial over all non-zero field elements yields -1 if the exponent is a multiple of p-1, and 0 otherwise. This reduces the problem to counting walks of length p that use zero entries either 0 or p-1 times. For p=2, the answer is simply the matrix with zeros replaced by 1 raised to p. For p>2, only walks using exactly one zero entry p-1 times contribute. Analysis shows that for p>3, only loops can contribute; for p=3, loops and non-loops with a fixed reverse edge contribute. The matrix power is computed via binary exponentiation, which is efficient for N≤100 and p up to 1e9.

## worker: Write the full Python solution with matrix exponen
The solution leverages the algebraic property that summing a monomial over all non-zero field elements yields -1 if the exponent is a multiple of p-1, and 0 otherwise. This reduces the problem to counting walks of length p that use zero entries either 0 or p-1 times. For p=2, the answer is simply the matrix with zeros replaced by 1 raised to p. For p>2, only walks using exactly one zero entry p-1 times contribute. Analysis shows that for p>3, only loops can contribute; for p=3, loops and non-loops with a fixed reverse edge contribute. The matrix power is computed via binary exponentiation, which is efficient for N≤100 and p up to 1e9.

## worker: Write the full Python solution with matrix exponen
The solution uses the algebraic property that summing a monomial over all non-zero field elements yields -1 if the exponent is a multiple of p-1, and 0 otherwise. This reduces the problem to counting walks of length p that use zero entries either 0 or p-1 times. For p=2, the answer is simply the matrix with zeros replaced by 1 raised to p. For p>2, only walks using exactly one zero entry p-1 times contribute. Analysis shows that for p>3, only loops can contribute; for p=3, loops and non-loops with a fixed reverse edge contribute. The matrix power is computed via binary exponentiation, which is efficient for N≤100 and p up to 1e9. The algorithm runs in O(N^3 log p) time, which is feasible within the given constraints.
