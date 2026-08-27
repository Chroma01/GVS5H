We need to compute S = Σ_{l≤r} (sum_{i=l..r} A_i)^K mod 998244353 for N up to 2e5 and K≤10.
Expand (sum)^K using multinomial: (Σ A_i)^K = K! / (c1!...cN!) * Π A_i^{c_i} over compositions of K into N nonnegative parts with sum K, but this is too large. Use prefix sums S_0=0, S_i = Σ_{j≤i} A_j, then (sum_{l..r})^K = (S_r - S_{l-1})^K = Σ_{t=0..K} binom(K,t) (-1)^{K-t} S_r^t S_{l-1}^{K-t}. Summing over all intervals, answer = Σ_{t=0..K} binom(K,t) (-1)^{K-t} C_t where C_t = (Σ_{r≥t?}) depends: total sum = Σ_{l≤r} (S_r - S_{l-1})^K = Σ_{0≤p<q≤N} (S_q - S_p)^K.
Let p=l-1, q=r, so 0≤p<q≤N. So answer = Σ_{0≤p<q≤N} (S_q - S_p)^K.
Define function F(x) = Σ_{q=0..N} (S_q + x)^K. Then answer = Σ_{p=0..N} F(-S_p) - Σ_{p=q} (S_q - S_p)^K (zero), but easier: answer = Σ_{0≤p<q≤N} (S_q - S_p)^K = Σ_{0≤p<q≤N} Σ_{t=0..K} binom(K,t) S_q^t (-S_p)^{K-t} = Σ_{t=0..K} binom(K,t) (-1)^{K-t} (Σ_{q>t?}) Actually we can compute directly: let cnt[d] = Σ_{i=0..N} S_i^d for d=0..K. Then answer = Σ_{t=0..K} binom(K,t) (-1)^{K-t} * ( (Σ_{q} S_q^t) * (Σ_{p} S_p^{K-t}) - Σ_{i=0..N} S_i^K ). Wait: Σ_{0≤p<q≤N} f(S_q) g(S_p) = (Σ_{q} f(S_q))(Σ_{p} g(S_p)) - Σ_{i} f(S_i)g(S_i) when p,q range over same set (including p=q). For f(x)=x^t, g(x)=(-x)^{K-t}. So answer = Σ_{t=0..K} binom(K,t) (-1)^{K-t} ( (Σ S_q^t)(Σ S_p^{K-t}) - Σ S_i^K ). The double-counted diagonal has p=q contributing (S_q - S_q)^K=0, so subtract it fully. Since we subtract Σ S_i^K once per t, summed over t=0..K, the total subtract = Σ_{i} S_i^K * Σ_{t=0..K} binom(K,t) (-1)^{K-t} = Σ_i S_i^K * (1-1)^K = 0. So no correction needed! Thus answer = Σ_{t=0..K} binom(K,t) (-1)^{K-t} (Σ_{i=0..N} S_i^t) (Σ_{i=0..N} S_i^{K-t}) / 2? Wait double counting: we want sum over ordered pairs (p,q) with p<q. If we sum over all ordered pairs p≠q, that's (Σ f)(Σ g) - Σ f(i)g(i). For each unordered {p,q}, we count (p,q) once where p<q: that's exactly ordered p≠q divided by 2, because for p≠q both (p,q) and (q,p) appear. But here f depends on q and g on p, and for p<q we use specific orientation. Actually (S_q - S_p)^K is not symmetric in p,q: (S_q - S_p)^K = (-1)^K (S_p - S_q)^K. For K even it's symmetric; for K odd it's antisymmetric. So we cannot just halve.
Better: directly sum over p<q. Let pref[d] = Σ_{i=0..N} S_i^d. Then Σ_{p<q} (S_q - S_p)^K = Σ_{p<q} Σ_{t=0..K} binom(K,t) S_q^t (-S_p)^{K-t}
= Σ_{t=0..K} binom(K,t) (-1)^{K-t} Σ_{p<q} S_q^t S_p^{K-t}.
Now Σ_{p<q} S_q^t S_p^{K-t} = (1/2)[ (Σ_q S_q^t)(Σ_p S_p^{K-t}) - Σ_i S_i^{t+K-t} ]? No, this trick is for unordered pairs with product symmetric. Here S_q^t S_p^{K-t} is not symmetric. So we need different approach.
Alternative: iterate over q as right endpoint, maintain running sums of S_p^{K-t}. For each q, contribution = Σ_{t=0..K} binom(K,t) (-1)^{K-t} S_q^t * (running sum of S_p^{K-t}). This is O(N*K) which is fine (N=2e5, K≤10). We maintain arrays R[d] = Σ_{p=0..q-1} S_p^d for d=0..K. Initialize all 0. For each q from 0 to N: compute val = Σ_{t=0..K} binom(K,t) (-1)^{K-t} S_q^t * R[K-t]. Add to answer. Then update R[d] += S_q^d for d=0..K. This gives O(N*K^2) if we compute each t, but K≤10 so K^2=100, N=2e5, total 2e7 operations - feasible in Python.
Compute S_i = prefix sum, include S_0=0.
Precompute binom(K,t) and sign = (-1)^{K-t} mod MOD.
For each q, compute pow_s_t = S_q^t for t=0..K by repeated multiplication. Since K≤10, recompute each time O(K) per q is fine.
Actually O(N*K^2) is okay but we can do O(N*K): val = Σ_{t=0..K} C(t) * S_q^t * R[K-t] where C(t) = binom(K,t)*(-1)^{K-t}. This is convolution of S_q^t with R reversed. We can compute it in O(K) per q directly.

Let MOD = 998244353.

Steps:
1. Read N, K, array A.
2. Compute prefix S of length N+1: S[0]=0, S[i]=S[i-1]+A[i-1] mod MOD.
3. Precompute binom(K,t) for t=0..K, and coeff[t] = binom(K,t) * (-1)^(K-t) mod MOD.
4. Initialize R = [0]*(K+1).
5. ans = 0.
6. For q in 0..N:
   s = S[q]
   # compute powers s^t
   pow_t = [1]*(K+1)
   for t in 1..K: pow_t[t] = pow_t[t-1]*s % MOD
   for t in 0..K:
       ans += coeff[t] * pow_t[t] % MOD * R[K-t] % MOD
   ans %= MOD
   # update R
   for d in 0..K:
       R[d] = (R[d] + pow_t[d]) % MOD
7. Print ans.

Let's verify on sample 1: N=3, K=2, A=[3,1,2]. S=[0,3,4,6].
K=2, binom(2,0)=1, binom(2,1)=2, binom(2,2)=1. coeff[t] = binom(2,t)*(-1)^(2-t):
t=0: 1*(-1)^2=1
t=1: 2*(-1)^1=-2 => MOD-2
t=2: 1*(-1)^0=1
R=[0,0,0].
q=0, s=0, pow=[1,0,0]. R[2]=R[0]=R[1]=0 => ans=0. Update R: R[0]+=1=>1, R[1]+=0, R[2]+=0.
q=1, s=3, pow=[1,3,9]. t=0: coeff0*1*R[2]=0. t=1: coeff1*3*R[1]=0. t=2: coeff2*9*R[0]=1*9*1=9. ans=9. Update R: R[0]=1+1=2, R[1]=0+3=3, R[2]=0+9=9.
q=2, s=4, pow=[1,4,16]. t=0: 1*1*R[2]=9. t=1: MOD-2*4*R[1] = -2*4*3 = -24. t=2: 1*16*R[0] = 16*2=32. Sum = 9-24+32=17. ans=9+17=26. Update R: R[0]=3, R[1]=7, R[2]=25.
q=3, s=6, pow=[1,6,36]. t=0: 1*1*25=25. t=1: -2*6*7=-84. t=2: 1*36*3=108. Sum=25-84+108=49. ans=26+49=75. Matches.

Sample 2: N=1, K=10, A=[0]. S=[0,0]. All S_i=0, R remains zero except R[0] increments by 1 each step but pow for t>0 is zero. The sum will be zero. OK.

Complexity: O(N*K) for powers, O(N*K) for update, O(N*K) for the sum = O(N*K^2) if done naively? Wait the inner loop for t=0..K is K+1 iterations, so per q we do O(K) for sum and O(K) for update. Total O(N*K). Since K≤10, this is ~2e6 operations, very fast.

We should compute powers iteratively to avoid repeated pow calls, but recomputing from s each time is O(K). So overall O(N*K).

Implementation details:
- Use pow_t = [1]*(K+1), then for i in range(1,K+1): pow_t[i] = pow_t[i-1]*s % MOD.
- coeff[t] = binom(K,t) * pow(-1, K-t, MOD) % MOD.
- Precompute binom via simple formula or math.comb.

Edge cases: N=2e5, K=10, mod is prime. Use integer arithmetic.

Thus final code.