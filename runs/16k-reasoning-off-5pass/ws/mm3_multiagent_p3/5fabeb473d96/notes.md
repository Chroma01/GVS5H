
## ideation
The problem asks for the sum over all (N-1)! rooted trees (with parent sequence P) of the distance between two given vertices u and v, where edge weights are given by A_i. N, Q up to 2e5.

Key observations:
1. The total sum is Σ_{i=2}^N A_i * (# trees where edge (i, parent(i)) lies on the u-v path).
2. Edge (i, parent(i)) lies on the u-v path iff exactly one of u, v is in the subtree of i.
3. For random recursive trees (uniform over all (N-1)! trees), the probability that a given vertex i is an ancestor of j (for i < j) is 1/i.
4. For i > v, the probability is 0. For i = v, the probability is 1 (since v cannot be ancestor of u). For i = u, probability is 1 - 1/u (u could be ancestor of v).
5. For u < i < v, probability = 1/i (only v can be in subtree of i).
6. For i ≤ u, probability = 2/i - 2 * Pr(i is ancestor of both u and v).
7. The joint probability Pr(i ancestor of both u and v) for i ≤ u can be computed as: 
   - If i = 1, it's 1.
   - For i > 1, by counting trees with parent(u)=i and considering parent(v), we find it's 2 / (i * (i+1))? Wait, from the small cases: g(2,3,4)=1/3, g(2,3,5)=1/3, g(2,4,5)=1/3, g(3,4,5)=1/6. It appears g(i, u, v) = 2 / (i * (i+1))? For i=2, 2/(2*3)=1/3, correct. For i=3, 2/(3*4)=1/6, correct. For i=1, 2/(1*2)=1, correct. So the joint probability is 2/(i*(i+1)) for all i, u, v with i ≤ u < v. This is independent of u and v! This is a crucial simplification.
8. Therefore, for i ≤ u: f(i) = 2/i - 2*(2/(i*(i+1))) = 2/i - 4/(i*(i+1)) = (2(i+1) - 4) / (i(i+1)) = (2i - 2) / (i(i+1)) = 2(i-1)/(i(i+1)).
9. For u < i < v: f(i) = 1/i.
10. For i = v: f(i) = 1.
11. For i > v: f(i) = 0.
12. The total sum for query (u, v) with u < v is:
    (N-1)! * [ Σ_{i=2}^{u} A_i * 2(i-1)/(i(i+1)) + Σ_{i=u+1}^{v-1} A_i * (1/i) + A_v * 1 ] modulo 998244353.

We need to compute these sums efficiently for Q queries up to 2e5. We can precompute prefix sums of A_i * 2(i-1)/(i(i+1)) and A_i / i modulo MOD, and also precompute (N-1)! modulo MOD. Then each query can be answered in O(1) time.

Note: For i=2, the formula gives 2(1)/(2*3)=2/6=1/3, which matches the sample: for N=3, u=1, v=2, sum = A_2 * f(2) = 1 * 1 = 1? Wait, for u=1, v=2, i=2 is v, so f(2)=1, sum=1. But sample 1 query 1 (1,2) total is 2. Let's check: N=3, (N-1)! = 2. For query (1,2), our formula: i=2 is v, so f(2)=1, sum = 2 * (A_2 * 1) = 2*1=2. Correct.
For query (1,3): i=2 is u < i < v? Actually i=2 is u, so it's i ≤ u. i=3 is v. So sum = 2 * [ A_2 * 2(1)/(2*3) + A_3 * 1 ] = 2 * [1 * 2/6 + 1 * 1] = 2 * [1/3 + 1] = 2 * 4/3 = 8/3? But the sum is 3. 8/3 mod 998244353 is not 3. So there's a mistake.

Wait, for u=1, v=3, i=2 is u, so f(2) = 2(i-1)/(i(i+1)) = 2/6 = 1/3. i=3 is v, f(3)=1. So sum = 2 * (1/3 + 1) = 2 * 4/3 = 8/3. But the actual sum is 3. So the joint probability formula might be wrong? Let's check with N=3, u=1, v=3. The trees: (1,1) and (1,2). Distances: for (1,1): d(1,3)=1+1=2? Actually, A_2=1, A_3=1. In tree (1,1): 2->1, 3->1, so distance 1-3 is 1 (edge 3-1) + 1 (edge 1-2)? Wait, path from 1 to 3: 1-3 direct, weight A_3=1. So distance=1. In tree (1,2): 2->1, 3->2, path 1-3: 1-2 (A_2=1) and 2-3 (A_3=1), total 2. Sum=3. Our formula gave 8/3, which is not 3. So the joint probability g(1,3,?) is not 2/(1*2)=1? Actually, for i=1, subtree is whole tree, so both are in subtree with probability 1. Then f(1) = 2/1 - 2*1 = 0. So edge (1,parent(1)) doesn't exist. So we start from i=2. For i=2, u=1, v=3, i=2 is between u and v? Actually u=1, v=3, so i=2 is u < i < v? No, u=1, i=2, v=3, so i=2 is not ≤ u because u=1, so i > u. So for i=2, it falls in the case u < i < v? But u=1, so u < i is true. So f(2) = 1/i = 1/2. For i=3, i=v, f(3)=1. So sum = (N-1)! * (A_2 * 1/2 + A_3 * 1) = 2 * (1/2 + 1) = 2 * 1.5 = 3. Correct! So the case i ≤ u only applies when u ≥ i, i.e., i ≤ u. For u=1, there is no i ≤ u with i ≥2. So the sum is just over i from u+1 to v. So the formula is: for query (u,v), sum = (N-1)! * [ Σ_{i=u+1}^{v-1} A_i / i + A_v ] (since for i=v, f(i)=1, which is A_v * 1, and note that 1/i for i=v is 1/v, so it's not included in the sum). Actually, A_v is multiplied by 1, not 1/v. So we need to separate A_v.

Thus, the total sum is:
S(u,v) = (N-1)! * [ Σ_{i=u+1}^{v-1} A_i * (1/i) + A_v ] mod MOD.
Wait, what about i ≤ u? For i ≤ u, f(i) = 2(i-1)/(i(i+1)). So we need to include that if u ≥ 2. So the full formula:
If u == 1: S = (N-1)! * [ Σ_{i=2}^{v-1} A_i / i + A_v ]
If u ≥ 2: S = (N-1)! * [ Σ_{i=2}^{u} A_i * 2(i-1)/(i(i+1)) + Σ_{i=u+1}^{v-1} A_i / i + A_v ]

Check with sample 1: N=3, (N-1)! = 2.
Query (1,2): u=1, v=2. Sum = 2 * [ A_2 ] = 2*1=2. Correct.
Query (1,3): u=1, v=3. Sum = 2 * [ A_2/2 + A_3 ] = 2 * (1/2 + 1) = 3. Correct.

So the problem reduces to computing prefix sums of A_i * c1(i) and A_i * c2(i), where c1(i) = 2(i-1)/(i(i+1)) for i≥2, and c2(i) = 1/i for i≥2. Then for each query (u,v), if u=1, answer = fact * ( prefix2(v-1) ) + fact * A_v? Actually careful: A_v is separate. So we need to compute:
S(u,v) = fact * ( P1(u) + P2(v-1) - P2(u) + A_v ) mod MOD, where P1(x) = Σ_{i=2}^{x} A_i * c1(i), P2(x) = Σ_{i=2}^{x} A_i * c2(i). If u=1, then P1(1)=0, P2(1)=0, so it's fact * (0 + P2(v-1) - 0 + A_v) = fact*(P2(v-1) + A_v). If u>1, then S = fact*(P1(u) + P2(v-1) - P2(u) + A_v).

We need to compute modular inverses of i and i(i+1) for i up to N. Since MOD = 998244353 is prime, we can precompute inv[i] for i=1..N+1. Then c1(i) = 2*(i-1) * inv[i] * inv[i+1] mod MOD. c2(i) = inv[i].

Precompute fact = (N-1)! mod MOD.
Compute prefix sums:
pre1[0] = 0, for i=2..N: pre1[i] = pre1[i-1] + A_i * c1(i) mod MOD.
pre2[0] = 0, for i=2..N: pre2[i] = pre2[i-1] + A_i * c2(i) mod MOD.

Then for each query (u,v):
if u == 1:
    ans = fact * ( (pre2[v-1] if v-1 >=2 else 0) + A_v ) mod MOD.
else:
    ans = fact * ( pre1[u] + (pre2[v-1] - pre2[u]) + A_v ) mod MOD.

We need to ensure modulo operations are correct.

Let's test with sample 2: N=2, A_2=100. Q=1, u=1,v=2. fact = 1! = 1. pre2[v-1] = pre2[1] = 0. A_2=100. ans = 1 * (0 + 100) = 100. Correct.

Sample 3: N=9, A = [765689282, 93267307, 563699854, 951829154, 801512848, 389123318, 924504746, 596035433] for i=2..9.
We can compute but trust the formula.

We need to handle the case when v-1 < 2, i.e., v=2. Then pre2[v-1] = pre2[1]=0.

Also, for u>1, if v-1 < u, the sum over i=u+1 to v-1 is empty, so pre2[v-1] - pre2[u] should be 0. Since pre2 is prefix, we can compute: if v-1 < u, then pre2[v-1] = pre2[u] (if u > v-1, then the prefix up to v-1 is the same as up to u because we only go up to v-1, but our pre2 array is defined for indices up to N. We can just compute pre2[v-1] and pre2[u] and subtract, but we must ensure that we only sum up to v-1. If v-1 < u, then the sum from u+1 to v-1 is empty, so the contribution is 0. We can compute: term2 = pre2[v-1] - pre2[u] if v-1 >= u+1, else 0. But using prefix sums, if we define pre2[i] as sum up to i, then for i < 2, pre2[i]=0. So if v-1 < u, then pre2[v-1] is sum up to v-1, and pre2[u] is sum up to u, but since v-1 < u, pre2[v-1] is not necessarily equal to pre2[u] because pre2[u] includes terms up to u. But we only want the sum from u+1 to v-1, which is empty. So we should compute: sum from u+1 to v-1 = pre2[min(u, v-1)] - pre2[u]? Actually, if v-1 <= u, the sum is 0. So we can compute: if v-1 > u, then sum = pre2[v-1] - pre2[u]; else 0. So we need to handle that condition.

Thus, the algorithm:
1. Read N, Q.
2. Read A[2..N].
3. Precompute inv[1..N+1] using Fermat's little theorem or linear method.
4. Compute fact = (N-1)! mod MOD.
5. Compute pre1[0]=0, pre1[i] for i=1..N: pre1[i] = pre1[i-1]; if i>=2, pre1[i] += A[i] * 2*(i-1) % MOD * inv[i] % MOD * inv[i+1] % MOD.
6. Compute pre2[0]=0, pre2[i] for i=1..N: pre2[i] = pre2[i-1]; if i>=2, pre2[i] += A[i] * inv[i] % MOD.
7. For each query (u,v):
   - if u == 1:
        sum2 = pre2[v-1] if v-1 >= 2 else 0.
        ans = fact * (sum2 + A[v]) % MOD.
   - else:
        sum1 = pre1[u] - pre1[1]? Actually pre1[u] is sum from i=2 to u. So pre1[u] is correct (pre1[1]=0). So sum1 = pre1[u].
        if v-1 > u:
            sum2 = pre2[v-1] - pre2[u];
        else:
            sum2 = 0;
        ans = fact * (sum1 + sum2 + A[v]) % MOD.
   - Print ans.

We must be careful with modulo for negative values: add MOD.

Let's test with sample 1: N=3, fact=2.
A: A2=1, A3=1.
inv: inv1=1, inv2=499122177, inv3=332748118, inv4=748683265.
pre1: pre1[1]=0; i=2: A2 * 2*(1) * inv2 * inv3 = 1 * 2 * 1/2 * 1/3? Actually 2*(1)*inv2*inv3 = 2 * 499122177 * 332748118 mod 998244353. Compute: inv2=499122177, inv3=332748118, product = 1/6 mod = 166374059? Actually 2 * inv2 = 1, so 1 * inv3 = inv3 = 332748118. So pre1[2] = 332748118. pre1[3] = pre1[2] (since i=3, but pre1 only adds for i=2? Actually we only add for i>=2, so for i=3, we don't add c1 because c1 is only for i≤u? Actually our pre1 is for all i, but c1(i) is defined for i>=2. So we add for all i>=2. So pre1[3] = pre1[2] + A3 * c1(3). c1(3) = 2*(2)/(3*4) = 4/12 = 1/3. So A3 * inv3 = 1 * 332748118. So pre1[3] = 332748118 + 332748118 = 665496236.
pre2: pre2[1]=0; i=2: A2*inv2 = 499122177; pre2[2]=499122177. i=3: A3*inv3 = 332748118; pre2[3]= 499122177+332748118 = 831870295.
Now queries:
(1,2): u=1, v=2. sum2 = pre2[1]=0. ans = 2 * (0 + A2) = 2*1=2. Correct.
(1,3): u=1, v=3. sum2 = pre2[2] = 499122177. ans = 2 * (499122177 + A3) = 2 * (499122177+1) = 2 * 499122178 = 998244356 mod 998244353 = 3. Correct.

So the formula works.

We need to implement efficiently in Python. N, Q up to 2e5, so O(N+Q) is fine.

Pitfalls:
- Inverse computation: precompute inv[i] for i=1..N+1 using pow(i, MOD-2, MOD) or linear method. Since MOD is prime, we can do inv[i] = pow(i, MOD-2, MOD) for each i, but that would be O(N log MOD). For N=2e5, it's fine. But we can also do linear: inv[1]=1; for i>1: inv[i] = MOD - MOD//i * inv[MOD%i] % MOD. That's O(N).
- Factorial: fact = 1; for i=2..N-1: fact = fact * i % MOD. If N=2, fact=1.
- Prefix sums: use lists of size N+1.
- A array: read A_2..A_N, store in 1-indexed array A[1..N], but A[1] is not used.
- For pre1 and pre2, we can compute up to N.

Let's code accordingly.

## worker: Implement the solution in Python: precompute modul
The solution is based on the following combinatorial derivation:
- The total sum over all trees of the distance between u and v is Σ A_i * (number of trees where edge (i, parent(i)) is on the u-v path).
- Edge (i, parent(i)) is on the path iff exactly one of u, v is in the subtree of i.
- Using properties of random recursive trees (uniform over all (N-1)! rooted trees), the probability that vertex i is an ancestor of j (for i < j) is 1/i.
- By case analysis on the relative order of i, u, v, we obtain:
  - If i > v: probability = 0.
  - If i = v: probability = 1.
  - If u < i < v: probability = 1/i.
  - If i ≤ u: probability = 2/i - 2 * Pr(i ancestor of both u and v) = 2(i-1)/(i(i+1)).
- Thus, the total sum is (N-1)! * [ Σ_{i=u+1}^{v-1} A_i / i + A_v + (if u≥2) Σ_{i=2}^{u} A_i * 2(i-1)/(i(i+1)) ] modulo 998244353.
- Precompute modular inverses, factorial, and two prefix sums to answer each query in O(1).
