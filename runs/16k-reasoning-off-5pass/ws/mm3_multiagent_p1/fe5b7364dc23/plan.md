We need to compute S = Σ_{l≤r} (sum_{i=l..r} A_i)^K mod 998244353, with N up to 2e5 and K ≤ 10. Direct O(N^2) is too slow.

Idea: Use generating functions / polynomial prefix sums. Let prefix sums P_0=0, P_i = Σ_{j=1..i} A_j. Then each subarray sum equals P_r - P_{l-1}. So S = Σ_{0 ≤ i < j ≤ N} (P_j - P_i)^K.

We need to efficiently compute Σ_{i<j} (P_j - P_i)^K. Expand via binomial theorem:
(P_j - P_i)^K = Σ_{t=0..K} C(K, t) * P_j^t * (-P_i)^{K-t} = Σ_{t=0..K} C(K, t) * (-1)^{K-t} * P_j^t * P_i^{K-t}.

So S = Σ_{t=0..K} C(K, t) * (-1)^{K-t} * ( Σ_{j=0..N} P_j^t ) * ( Σ_{i=0..N} P_i^{K-t} ), but careful: indices i<j, not all pairs. We can fix by including diagonal and adjusting.

Alternatively, compute full sum over all ordered pairs (i,j) with 0≤i,j≤N, then correct:
T = Σ_{i,j} (P_j - P_i)^K. This includes i=j (term 0) and double counts unordered pairs. Since K≥1, (P_j-P_i)^K is antisymmetric when K odd? Actually (P_j-P_i)^K = - (P_i-P_j)^K, so for odd K, T = 0. For even K, T = 2 S.

We can compute:
Let Q_m = Σ_{i=0..N} P_i^m for m=0..K.
Then T = Σ_{i,j} Σ_{t=0..K} C(K,t) P_j^t (-P_i)^{K-t}
= Σ_{t=0..K} C(K,t) (-1)^{K-t} (Σ_j P_j^t) (Σ_i P_i^{K-t})
= Σ_{t=0..K} C(K,t) (-1)^{K-t} Q_t * Q_{K-t}.

If K is odd, T=0, S=0. If K is even, S = T/2 mod MOD (with modular inverse of 2). Also note i=j gives (P_i-P_i)^K=0, so it doesn't affect S anyway. But unordered pairs i≠j are counted twice in T (once as (i,j), once as (j,i)). So indeed S = T/2 for even K.

Thus algorithm:
1. Compute prefix sums P[0..N].
2. Compute Q[m] = Σ_{i=0..N} (P_i)^m mod MOD for m=0..K.
   - P_i can be large, but we can reduce mod MOD.
3. Compute T = Σ_{t=0..K} C(K,t) * (-1)^{K-t} * Q[t] * Q[K-t] mod MOD.
4. If K odd: answer = 0.
   Else: answer = T * inv2 mod MOD (inv2 = (MOD+1)//2 = 499122177).
5. Output answer.

Complexities: O(N*K) to compute Q (each P_i raised to powers via incremental multiplication). N up to 2e5, K≤10, fine.

Precompute binomials C(K,t) modulo MOD (K small, can compute via factorial or direct).

Edge cases: A_i can be zero. P_i mod MOD is fine because sums are computed mod MOD, but (P_j - P_i)^K mod MOD only equals original sum mod MOD if we reduce properly: (P_j - P_i) mod MOD is congruent to actual difference mod MOD, and raising to K preserves congruence. So computing everything mod MOD is correct.

Check sample 1:
N=3, K=2, A=[3,1,2]
P=[0,3,4,6]
Q[0]=4 (four zeros count), Q[1]=0+3+4+6=13, Q[2]=0+9+16+36=61.
T = Σ_{t=0..2} C(2,t) (-1)^{2-t} Q[t]Q[2-t]
t=0: C=1, (-1)^2=1, Q0*Q2=4*61=244
t=1: C=2, (-1)^1=-1, 2 * -1 * Q1*Q1 = -2*169 = -338
t=2: C=1, (-1)^0=1, Q2*Q0=244
T = 244 -338 +244 = 150
K even => S = 150 * inv2 = 75 mod MOD. Correct.

Check K odd: say N=1, K=1, A=[x].
P=[0,x]
Q0=2, Q1=x.
T = C(1,0)(-1)^1 Q0*Q1 + C(1,1)(-1)^0 Q1*Q0 = -1*2x + 1*2x = 0. So T=0, S=0. But actual sum over subarrays: (x)^1 = x. Wait discrepancy! Let's check.

We defined S = Σ_{l≤r} (sum_{i=l..r} A_i)^K. In prefix notation, S = Σ_{0 ≤ i < j ≤ N} (P_j - P_i)^K. Note that i = l-1, j = r, so i < j. For K=1, S = Σ_{i<j} (P_j - P_i) = Σ_{j} (j * P_j - Σ_{i<j} P_i)? Actually known identity: Σ_{i<j} (P_j - P_i) = Σ_{j} P_j * (number of i<j) - Σ_i P_i * (number of j>i). But we used full sum over all i,j. Let's recompute.

Our T = Σ_{i,j} (P_j - P_i)^K includes i=j (0) and i>j. For K=1: (P_j - P_i). Sum over all i,j: Σ_{i,j} P_j - Σ_{i,j} P_i = (N+1) Σ_j P_j - (N+1) Σ_i P_i = 0. So T=0. But S = Σ_{i<j} (P_j - P_i) is not zero. So our relation S = T/2 for even K is false for odd K? Let's test with K=1.

Take A=[x], N=1. Subarrays: [1,1] sum = x. S=x.
P=[0,x], i=0,j=1: (P1-P0)=x. So S=x.
Our formula: T = Σ_{i,j} (P_j - P_i) = 0. So S != T/2 (which is 0). For odd K, T=0, but S is not zero generally.

Wait earlier I claimed for odd K, T=0, and S=0. But sample 2 has K=10 (even). Let's test with K=1 manually: A=[3,1,2], N=3, K=1. S = sum of subarray sums = 3+1+2+4+3+6=19.
Compute T: P=[0,3,4,6], Q0=4, Q1=13.
T = C(1,0)(-1)^1 Q0*Q1 + C(1,1)(-1)^0 Q1*Q0 = -4*13 + 13*4 = 0.
So T=0, but S=19. So my earlier statement "for odd K, S=0" is wrong.

So we need to handle odd K correctly. The expansion:
(P_j - P_i)^K = Σ_{t=0..K} C(K,t) P_j^t (-P_i)^{K-t}.
Summing over i<j (strict) gives:
S = Σ_{i<j} Σ_{t=0..K} C(K,t) (-1)^{K-t} P_j^t P_i^{K-t}
= Σ_{t=0..K} C(K,t) (-1)^{K-t} Σ_{i<j} P_j^t P_i^{K-t}.

We can write Σ_{i<j} P_j^t P_i^{K-t} = (Σ_j P_j^t)(Σ_i P_i^{K-t}) - Σ_{i=j} P_i^t P_i^{K-t} - Σ_{i>j} P_j^t P_i^{K-t}.
Note that for t and K-t, the term Σ_{i>j} P_j^t P_i^{K-t} is similar to Σ_{i<j} P_i^t P_j^{K-t} by swapping indices.
Specifically, let U_{a,b} = Σ_{i<j} P_i^a P_j^b.
Then Σ_{i>j} P_j^t P_i^{K-t} = Σ_{i<j} P_i^t P_j^{K-t} (by renaming i<->j, and swapping exponents). Actually:
Σ_{i>j} P_j^t P_i^{K-t} = Σ_{j<i} P_j^t P_i^{K-t} = Σ_{i<j} P_i^t P_j^{K-t} (swap i,j). So it's U_{t, K-t}.

Thus Σ_{i<j} P_j^t P_i^{K-t} = U_{K-t, t}? Let's be careful.

Define U(a,b) = Σ_{i<j} P_i^a P_j^b.
We want V(t) = Σ_{i<j} P_j^t P_i^{K-t}.
If we set a = K-t, b = t, then U(a,b) = Σ_{i<j} P_i^{K-t} P_j^t = V(t). So V(t) = U(K-t, t).

Then total sum over all ordered pairs (i,j) (including i=j and i>j) is:
W(t) = Σ_{i,j} P_j^t P_i^{K-t} = (Σ_j P_j^t)(Σ_i P_i^{K-t}) = Q_t * Q_{K-t}.
This equals V(t) + Σ_{i=j} P_i^t P_i^{K-t} + Σ_{i>j} P_j^t P_i^{K-t}.
Diagonal term: Σ_i P_i^{K} (since t + (K-t) = K). So diag = Q_K.
And Σ_{i>j} P_j^t P_i^{K-t} = U(t, K-t) (by definition with a=t, b=K-t).
Thus:
Q_t * Q_{K-t} = V(t) + Q_K + U(t, K-t).

But V(t) = U(K-t, t).
So we have:
Q_t * Q_{K-t} = U(K-t, t) + U(t, K-t) + Q_K.

Thus U(K-t, t) + U(t, K-t) = Q_t * Q_{K-t} - Q_K.

Now S = Σ_{t=0..K} C(K,t) (-1)^{K-t} U(K-t, t).

We can pair terms t and K-t. Let s = t, then the term for t and for K-t are:
C(K,s)(-1)^{K-s} U(K-s, s) + C(K,K-s)(-1)^{s} U(s, K-s).
Since C(K,K-s)=C(K,s) and (-1)^{s} = (-1)^{K-(K-s)}.
So sum = C(K,s) [ (-1)^{K-s} U(K-s, s) + (-1)^{K-s} U(s, K-s) ] because (-1)^{K-s} = (-1)^{K-(K-s)}? Wait: (-1)^{K - (K-s)} = (-1)^{s}. But we have (-1)^s in the second term. Actually the second term is (-1)^{K - (K-s)} = (-1)^{s}. So the sign is (-1)^{K-s} for first, (-1)^s for second. Are they same? Only if (-1)^{K-s} = (-1)^s, i.e., (-1)^K = 1 => K even. So for even K, the signs are same, and we can combine:
For K even, s and K-s have same sign, so sum = C(K,s) (-1)^{K-s} [U(K-s, s) + U(s, K-s)] = C(K,s) (-1)^{K-s} (Q_s * Q_{K-s} - Q_K).

For K odd, s and K-s have opposite signs. Then the two terms cancel if U(K-s,s) = U(s,K-s)? But generally they are not equal. So we need a different approach.

Alternative: Directly compute S using prefix sums and convolution? But K is small, maybe we can compute S via DP or polynomial multiplication.

Another approach: Use generating function of prefix sums. Let f(x) = Σ_{i=0..N} x^{P_i}? Not helpful.

We can compute S = Σ_{0 ≤ i < j ≤ N} (P_j - P_i)^K. Expand:
S = Σ_{i<j} Σ_{t=0..K} C(K,t) P_j^t (-P_i)^{K-t}
= Σ_{t=0..K} C(K,t) (-1)^{K-t} Σ_{i<j} P_j^t P_i^{K-t}.

Let’s define arrays:
For each t, we need Σ_{i<j} P_j^t P_i^{K-t}.
We can compute prefix sums of P_i^m. Let’s define for each m, prefix of P_i^m: Suffix? Actually:
Σ_{i<j} P_j^t P_i^{K-t} = Σ_{j=1..N} P_j^t * (Σ_{i=0..j-1} P_i^{K-t}).
So we can precompute for each m, the prefix sums of P_i^m: pre_m[j] = Σ_{i=0..j} P_i^m (inclusive). Then Σ_{i=0..j-1} P_i^{K-t} = pre_{K-t}[j-1].
Then V(t) = Σ_{j=1..N} P_j^t * pre_{K-t}[j-1].
This is O(N*K) to compute all V(t) for t=0..K. Then S = Σ_t C(K,t)(-1)^{K-t} V(t).

Complexities: O(N*K) time and O(N*K) memory if we store pre_m for all m. But we can compute on the fly: for each j, we have P_j. For each t, we need P_j^t and pre_{K-t}[j-1]. We can maintain an array cur[m] = Σ_{i=0..j-1} P_i^m. Initially cur[m] = P_0^m (i=0). Then iterate j from 1 to N:
  For each t from 0 to K:
    V(t) += P_j^t * cur[K-t].
  Then update cur[m] += P_j^m for all m=0..K.
After loop, we have V(t) for all t. Then compute S.

But careful: V(t) is defined as Σ_{i<j} P_j^t P_i^{K-t}. The sum over i from 0 to j-1. Our initial cur includes i=0. In the loop, when j=1, we have cur including i=0. So correct. After processing j, we add P_j to cur for next iteration. So this works.

Total time: O(N*K). N=2e5, K=10, fine. Memory: O(K) for cur and P_powers.

We need to compute P_j^m mod MOD for m=0..K. Since P_j can be large, we reduce mod MOD. P_j^0 = 1. We can compute incrementally: p_pow[0]=1, p_pow[m]=p_pow[m-1]*P_j mod MOD.

Similarly for cur: initially cur[m] = (P_0)^m. P_0 = 0. So cur[0]=1, cur[m>0]=0.

Then for j from 1 to N:
  p = P_j mod MOD.
  p_pow[0] = 1
  p_pow[m] = p_pow[m-1] * p % MOD
  For t=0..K:
    V[t] = (V[t] + p_pow[t] * cur[K-t]) % MOD
  For m=0..K:
    cur[m] = (cur[m] + p_pow[m]) % MOD

At the end, S = Σ_{t=0..K} C(K,t) * (-1)^{K-t} * V[t] mod MOD.

Check with sample 1: N=3, K=2, A=[3,1,2].
P: [0,3,4,6].
cur initially: cur[0]=1, cur[1]=0, cur[2]=0.
V[0..2] = 0.
j=1: P=3.
p_pow: 1,3,9.
t=0: V[0] += 1 * cur[2] = 0.
t=1: V[1] += 3 * cur[1] = 0.
t=2: V[2] += 9 * cur[0] = 9*1=9.
Update cur: cur[0]=2, cur[1]=3, cur[2]=9.
j=2: P=4.
p_pow: 1,4,16.
t=0: V[0] += 1 * cur[2] = 9.
t=1: V[1] += 4 * cur[1] = 4*3=12 => V[1]=12.
t=2: V[2] += 16 * cur[0] = 16*2=32 => V[2]=41.
Update cur: cur[0]=3, cur[1]=7, cur[2]=25.
j=3: P=6.
p_pow: 1,6,36.
t=0: V[0] += 1 * cur[2] = 25 => V[0]=34.
t=1: V[1] += 6 * cur[1] = 6*7=42 => V[1]=54.
t=2: V[2] += 36 * cur[0] = 36*3=108 => V[2]=149.
Now V = [34,54,149].
C(2,0)=1, (-1)^2=1: term = 1*34 = 34
C(2,1)=2, (-1)^1=-1: term = 2*(-1)*54 = -108
C(2,2)=1, (-1)^0=1: term = 1*149 = 149
S = 34 -108 +149 = 75. Correct.

Check K=1: N=1, A=[x], P=[0,x].
cur init: [1,0]
V[0..1] = 0.
j=1: P=x.
p_pow: 1,x.
t=0: V[0] += 1*cur[1]=0.
t=1: V[1] += x*cur[0]=x.
S = C(1,0)(-1)^1 V[0] + C(1,1)(-1)^0 V[1] = -0 + x = x. Correct.

So algorithm is correct.

Complexities: O(N*K). K≤10, N≤2e5, so 2e6 operations, very fast.

Precompute binomials C(K,t) mod MOD using factorial and inv factorial, or just compute iteratively: C(K,0)=1, C(K,t)=C(K,t-1)*(K-t+1)/t mod MOD.

We also need to handle negative signs: (-1)^{K-t}. We can precompute sign array: sign[t] = 1 if (K-t) even else -1. Or multiply by -1 when K-t odd.

Implementation details:
- Read N, K.
- Read array A (0-indexed or 1-indexed).
- Compute prefix sums P[0..N] (mod MOD). Actually we can compute P_j = (P_{j-1} + A_j) % MOD.
- Initialize cur array of size K+1: cur[0]=1, cur[1..K]=0.
- Initialize V array of size K+1: all zero.
- For j from 1 to N:
    p = P[j] (which is already mod MOD)
    p_pow[0] = 1
    for m in 1..K:
        p_pow[m] = p_pow[m-1] * p % MOD
    for t in 0..K:
        V[t] = (V[t] + p_pow[t] * cur[K-t]) % MOD
    for m in 0..K:
        cur[m] = (cur[m] + p_pow[m]) % MOD
- Compute binomial coefficients C(K,t) for t=0..K.
- Compute ans = Σ_{t=0..K} C(K,t) * (-1)^{K-t} * V[t] mod MOD.
- Ensure ans positive: (ans + MOD) % MOD.
- Print ans.

Check K odd: works fine.

Edge cases: A_i can be up to MOD-1, but we reduce mod MOD. P_j can be any value mod MOD. P_0=0.

Memory: P array size N+1, but we only need current P_j, not full array. Actually we need P_j for each j sequentially. So we can compute prefix on the fly:
cur_P = 0
cur[0]=1, cur[1..K]=0
V all zero
for each A in A:
    cur_P = (cur_P + A) % MOD
    p = cur_P
    compute p_pow...
    update V and cur.

Yes, no need to store all P. This is O(1) extra memory besides a few small arrays.

Let's test with sample 2: N=1, K=10, A=[0].
cur_P=0.
p=0, p_pow[0]=1, p_pow[m>0]=0.
V[t] all zero.
cur[0]=1+1=2, cur[m>0]=0.
After loop: V all zero. ans = 0. Correct.

Sample 3: N=10, K=5, A given. We trust.

Potential overflow: MOD ~ 1e9, multiplication of two ints up to MOD^2 ~ 1e18, fits in Python int (big int), but we use % MOD. In Python, no issue.

Time complexity: O(N*K) = 2e5 * 10 = 2e6, plus overhead. Fast.

Thus the plan is solid.

We should write the code accordingly.

Now, the problem statement says "Be sure to find the sum modulo 998244353." So we must output ans % MOD.

Implementation steps:
1. Define MOD = 998244353.
2. Read N, K.
3. Read list A of length N.
4. Precompute binomials: C = [0]*(K+1); C[0]=1; for t in 1..K: C[t] = C[t-1] * (K - t + 1) % MOD * pow(t, MOD-2, MOD) % MOD. Or use factorials: fact[K] * inv_fact[t] * inv_fact[K-t]. Since K small, simple loop.
5. Initialize cur = [0]*(K+1); cur[0] = 1.
6. Initialize V = [0]*(K+1).
7. cur_P = 0.
8. Loop over a in A:
    cur_P = (cur_P + a) % MOD
    p = cur_P
    p_pow = [1]*(K+1)
    for m in range(1, K+1):
        p_pow[m] = p_pow[m-1] * p % MOD
    for t in range(K+1):
        V[t] = (V[t] + p_pow[t] * cur[K-t]) % MOD
    for m in range(K+1):
        cur[m] = (cur[m] + p_pow[m]) % MOD
9. ans = 0
   for t in range(K+1):
        sign = 1 if (K - t) % 2 == 0 else -1
        ans = (ans + sign * C[t] * V[t]) % MOD
10. ans = (ans + MOD) % MOD
11. Print ans.

Double-check the loop for V: we need cur[K-t] which is defined. cur has length K+1, so index K-t is valid for t=0..K.

Test with small case: N=2, A=[1,1], K=1.
P: 0,1,2.
cur init: [1,0]
V=[0,0]
j=1: p=1, p_pow=[1,1]
t=0: V[0] += 1*cur[1]=0
t=1: V[1] += 1*cur[0]=1
cur: [2,1]
j=2: p=2, p_pow=[1,2]
t=0: V[0] += 1*cur[1]=1
t=1: V[1] += 2*cur[0]=2*2=4 => V[1]=5
cur: [3,3]
Now V=[1,5]
C(1,0)=1, (-1)^1=-1: -1*1 = -1
C(1,1)=1, (-1)^0=1: 1*5 = 5
ans = 4.
Check manually: subarrays: [1], [2], [1,1] sums: 1+1+2=4. Correct.

Test K=2: N=2, A=[1,1].
P:0,1,2.
cur:[1,0,0]
V:[0,0,0]
j=1: p=1, p_pow=[1,1,1]
t=0: V0+=1*cur2=0
t=1: V1+=1*cur1=0
t=2: V2+=1*cur0=1
cur:[2,1,1]
j=2: p=2, p_pow=[1,2,4]
t=0: V0+=1*cur2=1
t=1: V1+=2*cur1=2*1=2
t=2: V2+=4*cur0=4*2=8 => V2=9
V=[1,2,9]
C(2,0)=1, (-1)^2=1: 1
C(2,1)=2, (-1)^1=-1: -4
C(2,2)=1, (-1)^0=1: 9
ans = 1-4+9=6.
Manually: sums: 1,1,2,1,1,2,1+1=2,1+1=2,1+1+1=3? Wait A=[1,1], subarrays: [1], [1], [1,1]. Sums: 1,1,2. Squares: 1,1,4. Sum=6. Correct.

So algorithm is correct.

Now we need to write the final answer. The code should be in Python, reading from stdin, writing to stdout.

One optimization: p_pow can be computed without list allocation? Not needed, K is small.

Potential issue: When p=0, p_pow[m>0]=0, correct.

Now, the problem constraints: N up to 2e5, K up to 10. The code runs in about 0.5 seconds in Python.

We should ensure to use sys.stdin for fast reading.

Now produce the final response.</mm:think>### PLAN
We rewrite the sum in terms of prefix sums \(P_0=0\) and \(P_i=\sum_{j=1}^i A_j\). For each subarray \(l..r\), the sum is \(P_r-P_{l-1}\). Thus the answer is
\[
S = \sum_{0\le i<j\le N} (P_j-P_i)^K.
\]
Expanding by the binomial theorem,
\[
(P_j-P_i)^K = \sum_{t=0}^{K} \binom{K}{t} P_j^t (-P_i)^{K-t},
\]
so
\[
S = \sum_{t=0}^{K} \binom{K}{t} (-1)^{K-t} \sum_{i<j} P_j^t P_i^{K-t}.
\]
The inner sum \(\sum_{i<j} P_j^t P_i^{K-t}\) can be computed in a single left‑to‑right pass:
keep an array \(\text{cur}[m]=\sum_{i\ \text{processed}} P_i^m\) and accumulate
\(V[t] \mathrel{+}= P_j^t \cdot \text{cur}[K-t]\) at each step \(j\), then update \(\text{cur}\) with \(P_j^m\).  
All operations are performed modulo \(M=998244353\). The overall complexity is \(O(NK)\) with \(O(K)\) extra memory.