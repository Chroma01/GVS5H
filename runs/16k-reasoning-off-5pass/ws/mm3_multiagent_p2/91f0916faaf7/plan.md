We are given constraints: For consecutive pair (S_i, S_{i+1}) with P/Q = S_i/S_{i+1} in reduced form, we need P*Q = A_i. This implies S_i = P * d_i, S_{i+1} = Q * d_i for some positive integer d_i. In other words, for each adjacent pair, S_i and S_{i+1} have a known ratio P_i/Q_i (a rational in lowest terms) with P_i*Q_i = A_i.

Observation: For each i, factorization of A_i gives a unique set of possible (P_i, Q_i) pairs: choose a divisor p of A_i, let q = A_i / p, then reduce (p, q) to lowest terms. Only those reduced pairs where p*q = A_i are possible, i.e., we pick P_i = p/g, Q_i = q/g with g = gcd(p, q). Equivalent: P_i*Q_i = A_i / g^2, so g^2 must divide A_i. So for each square factor g^2 | A_i we get a candidate ratio (A_i/(g*Q), ...). Better to enumerate all positive integer d, set P = d, Q = A_i / d, then reduce.

Since A_i ≤ 1000, we can precompute for each i a list of allowed (P_i, Q_i) pairs. For each pair, we know the multiplicative factor connecting adjacent elements: S_{i+1} = S_i * Q_i / P_i. Thus S_i values follow a sequence of multiplicative steps: S_1 is some positive integer, and S_{k+1} = S_k * (Q_k / P_k). Since S_k must be integer, S_1 must be divisible by the denominator when reducing the product of ratios.

Define product of ratios: R_i = Q_i / P_i (as a rational). Then S_{i+1} = S_1 * (R_1 * R_2 * ... * R_i). Write cumulative product: let a_i, b_i such that product of first i ratios = a_i / b_i in lowest terms. Then S_{i+1} = S_1 * a_i / b_i, requiring b_i | S_1. So S_1 must be a multiple of L = lcm(b_1, b_2, ..., b_{N-1}). Then S_k = (L / b_{k-1}) * a_{k-1} * t where t = S_1 / L, with a_0 = b_0 = 1 (for k=1).

But we also need gcd(S_1,...,S_N) = 1. Compute gcd across S_k expression.

Goal: sum of product ∏_{k=1}^{N} S_k over all good sequences.

We can treat S_1 = L * t for t positive integer. Then S_k = (L * t) * a_{k-1} / b_{k-1} = t * (L * a_{k-1} / b_{k-1}). Since L is multiple of b_{k-1}, each S_k is t * C_k where C_k is integer independent of t.

Thus product ∏ S_k = t^N * (∏ C_k). The gcd condition becomes gcd(t*C_1, t*C_2, ..., t*C_N) = 1 => t * gcd(C_1,...,C_N) = 1, so t must be 1. Wait, more carefully: Since C_k have fixed values, the overall gcd of S_k is t * g where g = gcd(C_1,...,C_N). To have gcd = 1, we need t * g = 1 => t = 1 and g = 1. If g > 1, then t must be 1/g? No, t integer, so only possible if g=1. Thus t must be 1. So S_1 = L, uniquely. Thus the whole sequence S is uniquely determined once we pick for each i a ratio (P_i, Q_i) that satisfies the product constraints and ensures gcd of resulting S's = 1.

Wait, is t forced to be 1? Let's analyze carefully. We defined S_{k} = S_1 * (product_{i=1}^{k-1} R_i) where R_i = Q_i/P_i. For S_k to be integer, S_1 must be divisible by the denominator of the cumulative product. Let the cumulative product in lowest terms be a_{k-1} / b_{k-1}. So S_k = S_1 * a_{k-1} / b_{k-1}. Since a_{k-1}, b_{k-1} coprime, b_{k-1} must divide S_1. Let L = lcm(b_1, b_2, ..., b_{N-1}). Then S_1 = L * t for some positive integer t. Then S_k = t * (L * a_{k-1} / b_{k-1}) = t * C_k, where C_k = L * a_{k-1} / b_{k-1} ∈ ℕ. Indeed C_k are integers.

Now compute G = gcd(C_1, ..., C_N). Then gcd(S_1,...,S_N) = t * G. To have gcd = 1, we need t * G = 1. Since t, G are positive integers, the only solution is t=1 and G=1.

Thus if for a given choice of (P_i, Q_i) pairs the resulting C_k have gcd 1, then the only feasible S_1 is L, and the whole sequence is determined uniquely. If G > 1, then there is no S_1 that makes overall gcd 1 (since any t multiplies G, giving gcd >1). Therefore, such a choice of (P_i, Q_i) yields zero good sequences. Conversely, if G=1, there is exactly one good sequence (with t=1). So the total sum of scores is sum over all choices of (P_i, Q_i) (for i=1..N-1) that produce G=1, of product of S_k (which equals product of C_k because t=1, S_k = C_k). Since t=1, product of S_k = ∏ C_k.

Thus the problem reduces to: For each i, choose a reduced ratio (P_i, Q_i) such that P_i*Q_i = A_i. Compute cumulative product fractions a_i/b_i (a_0 = b_0 = 1). Let L = lcm(b_1,...,b_{N-1}). Compute C_k = L * a_{k-1} / b_{k-1} for k=1..N. Compute G = gcd(C_1,...,C_N). If G=1, then contribution = ∏ C_k (mod M). Sum contributions modulo 998244353.

We need to enumerate all possible ratios. For each A ≤ 1000, number of divisors is at most around 32 (since 1000 < 2^10, divisor count of 1008 max is 32?). Actually 840 has 32 divisors, 720 has 30, 960 has 28. So at most ~32. Each divisor d yields (P_raw, Q_raw) = (d, A/d). Reduce to lowest terms: divide by g = gcd(d, A/d). So we get a pair (P, Q) = (d/g, (A/d)/g). This pair satisfies P*Q = (d * A/d) / g^2 = A / g^2. So we need P*Q = A. But the condition is that P*Q must equal A. So for (d, A/d) to give a valid (P, Q) we need A / g^2 = A => g^2 = 1 => g=1. Thus d and A/d must be coprime. So not all divisors are valid: only those divisor pairs (d, A/d) where d and A/d are coprime (i.e., d is a unitary divisor of A). Indeed unitary divisor: a divisor d of A such that gcd(d, A/d) = 1. So for each A_i, we need to consider unitary divisors.

Thus number of possible ratios per i is the number of unitary divisors of A_i, which is 2^{ω(A_i)} where ω is number of distinct prime factors of A_i. For A_i ≤ 1000, max prime factors? 2*3*5*7*11 = 2310 >1000, so at most 4 distinct primes (e.g., 2*3*5*7=210, 2*3*5*11=330, 2*3*5*13=390, 2*3*5*17=510, 2*3*5*19=570, 2*3*5*23=690, 2*3*5*29=870, 2*3*5*31=930; 5 primes would be 2*3*5*7*11=2310 >1000). So at most 4 primes, thus at most 2^4 = 16 unitary divisors per A_i. Good.

So total number of possible (P_i, Q_i) combinations across all i is product of per-i counts, at most 16^{N-1} which is huge for N up to 1000. We need a DP.

Observation: The product of ratios across the sequence is a rational number. The condition G=1 depends on the entire chain.

We can think of each step as scaling S by factor Q_i / P_i. The LCM of denominators grows. But N is up to 1000, each step has up to 16 options, total combinations huge; we need a smarter DP.

We need to compute the sum over all sequences of (∏ C_k) with G=1, where C_k = L * a_{k-1} / b_{k-1} and L = lcm(b_1,...,b_{N-1}). This looks like a global condition that depends on the entire sequence, making naive DP difficult.

Alternative approach: The condition gcd(S_1,...,S_N)=1 is equivalent to the condition that for each prime p, not all S_i are divisible by p. The sum over sequences with product of S_i may be expressed via inclusion-exclusion? Or maybe we can compute sum over all sequences (without gcd condition) and then subtract those where gcd > 1. But sum over all sequences might be infinite? Let's examine: For each i, we have finitely many choices of (P_i, Q_i). That yields a unique S sequence? Actually for a fixed sequence of ratios, S_1 must be a multiple of L (denominator L). We argued that to have gcd=1, t must be 1. But if we ignore gcd condition, any t gives a valid integer sequence S, and product of S_i = t^N * ∏ C_k. Sum over t from 1 to infinity diverges. So we cannot ignore gcd condition; we need to consider only t=1 (if G=1) else none. So each choice of ratios yields either 0 or 1 good sequence. So total number of good sequences equals number of ratio combinations where G=1. Since per i at most 16 options, total combinations up to 16^{999} huge, but perhaps the condition G=1 is rarely satisfied? Not necessarily; we need to count them.

We need to compute sum of ∏ C_k over those ratio combinations where G=1. Since each combination yields exactly one sequence (S_1 = L). The product ∏ S_i = ∏ C_k. So we need to sum ∏ C_k over valid ratio sequences.

Observation: The product ∏ C_k can be expressed in terms of the ratios. Let's try to express product in simpler form.

We have S_k = L * a_{k-1} / b_{k-1}. Then product_{k=1}^{N} S_k = L^N * ∏_{k=1}^{N} a_{k-1} / b_{k-1} = L^N * (∏_{k=0}^{N-1} a_k) / (∏_{k=0}^{N-1} b_k). Note a_0 = b_0 = 1.

But we have recurrence: a_i = a_{i-1} * Q_i / g_i, b_i = b_{i-1} * P_i / g_i, where g_i = gcd(a_{i-1} * Q_i, b_{i-1} * P_i) (ensuring reduced). Actually we maintain a_i/b_i = (a_{i-1}/b_{i-1}) * (Q_i/P_i) in lowest terms.

Let’s denote after reduction: a_i = a_{i-1} * Q_i / g_i, b_i = b_{i-1} * P_i / g_i, where g_i = gcd(a_{i-1} * Q_i, b_{i-1} * P_i). This ensures a_i, b_i coprime.

Now L = lcm(b_1, ..., b_{N-1}). The expression L^N / (∏ b_k) = (L / b_0) * (L / b_1) * ... * (L / b_{N-1})? Wait product over k=0..N-1 of (L / b_k) = L^N / (∏_{k=0}^{N-1} b_k). Since b_0 = 1, that's okay. So product = (∏_{k=0}^{N-1} a_k) * (∏_{k=0}^{N-1} L / b_k). This is product of a_k times product of L/b_k.

Alternatively, product = L^N * (∏ a_k) / (∏ b_k). But note that a_k and b_k are coprime, but not necessarily related to L.

We can also write product = ∏_{i=1}^{N-1} (L / b_i) * (a_i) ? Let's compute product S_1 * S_2 * ... * S_N:

S_1 = L (since a_0/b_0 = 1, S_1 = L * 1/1 = L). Wait S_1 = L * a_0 / b_0 = L.

S_2 = L * a_1 / b_1.

...

S_N = L * a_{N-1} / b_{N-1}.

Thus product = L^N * ∏_{i=0}^{N-1} a_i / b_i = L^N * (∏ a_i) / (∏ b_i).

But note that for i from 0 to N-1, a_i and b_i are coprime.

Now G = gcd(C_1, ..., C_N) = gcd(L, L * a_1 / b_1, ..., L * a_{N-1} / b_{N-1}) = L * gcd(1, a_1 / b_1, ..., a_{N-1} / b_{N-1})? Wait gcd of numbers of the form L * x where x is integer. Since L divides all C_k, G = L * d where d = gcd(1, a_1 / b_1, ..., a_{N-1} / b_{N-1})? Actually C_1 = L. C_2 = L * a_1 / b_1. Since a_1/b_1 is a rational in lowest terms, a_1 / b_1 is integer only if b_1 = 1. In general, C_2 = L * a_1 / b_1 = (L / b_1) * a_1, which is integer because L is multiple of b_1. So we can write C_k = (L / b_{k-1}) * a_{k-1}. So G = gcd_{k=1..N} ( (L / b_{k-1}) * a_{k-1} ). Since a_{k-1}, b_{k-1} are coprime.

Observation: G = L / D where D = something? Let's compute G more concretely. Since L is common factor, G = L * g where g = gcd( a_0 / b_0, a_1 / b_1, ..., a_{N-1} / b_{N-1} )? But a_k / b_k are rationals, not necessarily integer. Actually C_k = L * a_{k-1} / b_{k-1} = (L / b_{k-1}) * a_{k-1}. Since L/b_{k-1} is integer, we can factor L out: C_k = L * (a_{k-1} / b_{k-1}). However, a_{k-1} / b_{k-1} may not be integer. So we cannot factor L out of gcd. But we can write C_k = (L / b_{k-1}) * a_{k-1}. The gcd of these numbers is the gcd of (L * a_{k-1} / b_{k-1}) for k=1..N.

Let’s define D_k = L / b_{k-1}. Then C_k = D_k * a_{k-1}. Note that D_k is an integer, and a_{k-1} is coprime with b_{k-1}. But D_k may share factors with a_{k-1}.

We need G = gcd(C_1,...,C_N) = 1 for a valid sequence.

Since L is the lcm of all b_i (i=1..N-1), each b_i divides L. So D_k = L / b_{k-1} is integer. For k=1, b_0=1, D_1 = L. So C_1 = L. So G divides L. Actually C_1 = L, so G = gcd(L, C_2, ..., C_N). Since C_1 = L, G = gcd(L, C_2, ..., C_N). So G is a divisor of L. In fact G = gcd(L, C_2, ..., C_N). Since each C_k is multiple of D_k = L / b_{k-1}, and D_k may be smaller than L.

We need G=1. So the condition is that there is no prime p that divides all C_k. Since C_1 = L, any prime dividing L will divide C_1. To have G=1, we need that for each prime p dividing L, there is some k such that p does not divide C_k. In other words, the intersection of the sets of prime divisors of C_k is empty.

But C_k = L * a_{k-1} / b_{k-1} = (L / b_{k-1}) * a_{k-1}. Since b_{k-1} | L, L / b_{k-1} is integer. So C_k = (L / b_{k-1}) * a_{k-1}. Let’s factor L = ∏ p^{e_p}. Then b_{k-1} has some exponents f_{p,k} ≤ e_p. Then L / b_{k-1} has exponent e_p - f_{p,k}. Also a_{k-1} is coprime to b_{k-1}, but may share primes with L. However, a_{k-1} is derived from the ratios: a_i / b_i = ∏_{j=1}^{i} (Q_j / P_j) reduced.

Thus a_{k-1} may have prime factors that also appear in L (i.e., in some b_i). So C_k's prime exponents are (e_p - f_{p,k}) + g_{p,k} where g_{p,k} is exponent of p in a_{k-1}. Since a_{k-1} and b_{k-1} are coprime, g_{p,k} is zero if f_{p,k} > 0? Wait b_{k-1} and a_{k-1} are coprime, so for any prime p, at most one of them has positive exponent. So if p divides b_{k-1}, then p does not divide a_{k-1}. Conversely, if p divides a_{k-1}, then p does not divide b_{k-1}.

Thus for each prime p and each k, either f_{p,k} = exponent of p in b_{k-1} (could be 0) and g_{p,k} = 0, or g_{p,k} > 0 and f_{p,k} = 0.

Therefore, exponent of p in C_k is:

- If p | b_{k-1}: then exponent = e_p - f_{p,k} (since a_{k-1} not divisible by p).
- If p ∤ b_{k-1}: then exponent = g_{p,k} (exponent in a_{k-1}).

Note that b_{k-1} is the denominator of the cumulative product up to step k-1. It divides L. For each prime p dividing L, there is some k such that p | b_{k-1} (specifically, p may appear in some b_i). Actually L is lcm of b_i, so for each p, the max exponent across b_i is e_p. For a given k, b_{k-1} may or may not have p.

Now G = gcd(C_1,...,C_N). For each prime p, the exponent in G is min over k of exponent of p in C_k.

Since C_1 = L, exponent of p in C_1 is e_p.

Thus for G to be 1, we need for each prime p, there exists some k (2 ≤ k ≤ N) such that exponent of p in C_k is 0. That is, p does not divide C_k. Because min over k includes C_1 with exponent e_p > 0 (if p|L). So we need min_k v_p(C_k) = 0. This means there is some k where p ∤ C_k.

When does p ∤ C_k? Two cases:

- If p | b_{k-1}, then exponent = e_p - f_{p,k}. Since f_{p,k} ≤ e_p. For p not to divide C_k, we need e_p - f_{p,k} = 0, i.e., f_{p,k} = e_p. So b_{k-1} must contain the full exponent e_p of p. In other words, b_{k-1} must be a multiple of p^{e_p}. Since L is lcm, that means b_{k-1} is a multiple of the maximal power of p among all b_i. Actually e_p is the maximum exponent of p across all b_i (since L = lcm). So we need b_{k-1} to have exponent e_p (i.e., be divisible by p^{e_p}). That is, b_{k-1} must be a multiple of p^{e_p}.

- If p ∤ b_{k-1}, then exponent = g_{p,k} (exponent of p in a_{k-1}). Since a_{k-1} and b_{k-1} are coprime, p ∤ b_{k-1} implies p may divide a_{k-1} or not. For p not to divide C_k, we need g_{p,k} = 0, i.e., p ∤ a_{k-1}.

Thus the condition for G=1 is: For each prime p dividing L, there exists some index k (2 ≤ k ≤ N) such that either (i) p^{e_p} divides b_{k-1}, or (ii) p does not divide a_{k-1} and also p does not divide b_{k-1}? Wait case (ii) is p ∤ b_{k-1} and p ∤ a_{k-1}. But if p ∤ b_{k-1} and p ∤ a_{k-1}, then p does not appear in the fraction a_{k-1}/b_{k-1} at all, meaning p does not appear in the cumulative product up to k-1. That is possible if p never appeared in any numerator or denominator of the ratios up to k-1. But p divides L, which is lcm of b_i. So p appears in some b_i. The earliest index i where p appears in b_i is some i0. Then for k-1 < i0, b_{k-1} not divisible by p, and a_{k-1} also not divisible by p (since p hasn't been introduced yet). So for k ≤ i0, we have p ∤ a_{k-1} and p ∤ b_{k-1}. In that case, p ∤ C_k? Let's check: C_k = L * a_{k-1} / b_{k-1}. Since b_{k-1} has no p, denominator has no p. a_{k-1} has no p. So a_{k-1}/b_{k-1} has no p in numerator. But L has p^{e_p}. So C_k = (L / b_{k-1}) * a_{k-1}. Since b_{k-1} has no p, L / b_{k-1} still has p^{e_p}. So C_k is divisible by p^{e_p} unless a_{k-1} contains p in denominator? No, a_{k-1} is integer. So C_k is divisible by p^{e_p}. Wait we need to be careful: C_k = L * a_{k-1} / b_{k-1} is integer. If p ∤ b_{k-1}, then the factor p^{e_p} in L remains in numerator, multiplied by a_{k-1} (which has no p). So C_k is divisible by p^{e_p}. So p divides C_k.

Thus case (ii) (p ∤ b_{k-1}) does not help to avoid p dividing C_k, because L still has p. The only way to have p ∤ C_k is to have b_{k-1} contain the full p^{e_p} to cancel the p's in L. Indeed, since C_k = (L / b_{k-1}) * a_{k-1}, and a_{k-1} is coprime to b_{k-1}, the exponent of p in C_k is (e_p - f_{p,k}) + g_{p,k}, where f_{p,k} = v_p(b_{k-1}), g_{p,k} = v_p(a_{k-1}). Since a_{k-1} and b_{k-1} are coprime, g_{p,k} > 0 implies f_{p,k} = 0, and vice versa. So the exponent is either e_p - f_{p,k} (if p|b_{k-1}) or g_{p,k} (if p∤b_{k-1}). In the latter case, g_{p,k} could be zero, but then exponent is 0, so p ∤ C_k. Wait earlier we said if p ∤ b_{k-1}, exponent = g_{p,k}. If g_{p,k}=0, then exponent=0, so p does not divide C_k. That would be a case where p ∤ C_k. However, is it possible that p ∤ b_{k-1} and p ∤ a_{k-1}? Yes, if p hasn't been introduced into the cumulative fraction at all. But then L still has p^{e_p}. However, C_k = (L / b_{k-1}) * a_{k-1}. If b_{k-1} has no p, then L / b_{k-1} still has p^{e_p}. Multiplying by a_{k-1} (which has no p) yields p^{e_p} factor. So p divides C_k. Wait, there's a confusion: The expression C_k = (L / b_{k-1}) * a_{k-1} is correct. L contains p^{e_p}. b_{k-1} has no p. So L / b_{k-1} contains p^{e_p}. a_{k-1} has no p. So product contains p^{e_p}. So p divides C_k. So exponent is e_p. So min exponent is at least e_p > 0. So p divides all C_k. So G would have p.

Thus the only way to reduce the exponent of p in C_k is to have b_{k-1} contain some p's to cancel those in L. The exponent of p in C_k is e_p - v_p(b_{k-1}) (since a_{k-1} has no p). So to make exponent 0, we need v_p(b_{k-1}) = e_p. That is, b_{k-1} must be divisible by the full power p^{e_p} that appears in L.

Thus the condition for G=1 is: For each prime p dividing L, there exists some index k (2 ≤ k ≤ N) such that v_p(b_{k-1}) = e_p. In other words, for each prime p, the denominator b_{k-1} must at some point attain the maximal exponent of p among all b_i.

Since L is the lcm of all b_i, the maximum exponent e_p is max_i v_p(b_i). So we need that for each p, there is some index i (i from 1 to N-1) such that v_p(b_i) = e_p (i.e., b_i achieves the maximum). Then for k = i+1, we have b_{k-1} = b_i, so v_p(b_{k-1}) = e_p, thus C_{i+1} = (L / b_i) * a_i. Since L / b_i has no p (because v_p(L) = e_p, v_p(b_i) = e_p), and a_i is coprime to b_i, so a_i has no p. Thus C_{i+1} is not divisible by p. So the minimal exponent across all C_k is 0. So G=1.

Thus the condition reduces to: For each prime p, there exists at least one i (1 ≤ i ≤ N-1) such that the denominator b_i (the denominator of the cumulative product of ratios up to i) has the maximal exponent of p among all b_j.

Alternatively, since b_i are the denominators of the cumulative product ∏_{j=1}^{i} (Q_j / P_j) in lowest terms. The exponents of primes in b_i are determined by the prime factorizations of the ratios.

Thus the problem is: For each i, we have a set of possible ratios (P_i, Q_i) with P_i*Q_i = A_i and gcd(P_i, Q_i) = 1. We need to count sequences of ratios such that for each prime p, the denominator b_i (cumulative denominator) achieves the maximal exponent of p across all i at least once.

Additionally, we need to compute the sum of products ∏ C_k, where C_k = (L / b_{k-1}) * a_{k-1}, with L = lcm(b_1,...,b_{N-1}), a_{i}/b_i = ∏_{j=1}^{i} (Q_j / P_j) reduced.

We need to sum over all valid ratio sequences the product of C_k. Since each valid sequence yields a unique good sequence, the sum of scores is sum of product of S_k = sum of product of C_k.

Now, N up to 1000, A_i up to 1000. Number of distinct primes across all A_i is limited (primes ≤ 1000, but only those dividing any A_i). There are at most 168 primes ≤ 1000. But per sequence, only primes dividing L matter. However, L is lcm of denominators b_i. The denominators b_i are products of primes dividing the P_j (denominators of ratios). Since P_j and Q_j are coprime and P_j*Q_j = A_j, the prime factors of P_j are a subset of prime factors of A_j. So all primes involved are ≤ 1000 and divide some A_i.

But the number of distinct primes across all A_i could be up to 168. However, we cannot do DP over subsets of primes directly (2^168 huge). We need to find a simpler structure.

Observation: The condition about maximal exponent of each prime being achieved at some step is similar to ensuring that the lcm of denominators is "covered" by at least one denominator having each prime's full power.

But perhaps we can approach the problem differently: Since the number of possible (P_i, Q_i) per i is small (≤ 16), we can treat the whole sequence as a product of N-1 steps. However N=1000, total combinations 16^999 is impossible.

But maybe the product of scores can be expressed in a way that factorizes per prime, and we can compute contributions using DP over exponents per prime? Since the condition for each prime is independent? Let's examine.

The sequence of ratios determines a sequence of fractions a_i / b_i. The product of C_k involves a_i and b_i. The condition for G=1 is per prime: each prime's maximal exponent in denominators must be attained at some step. This is a global condition across steps but separable per prime: the condition for each prime p is that max_i v_p(b_i) = e_p (which is defined as that max) and there exists i with v_p(b_i) = e_p. That's always true by definition of e_p. Wait we need that for each prime p dividing L, there exists some i such that v_p(b_i) = e_p. But e_p is defined as max_i v_p(b_i). So by definition there is at least one i achieving the max. So the condition is always satisfied? Wait, earlier we deduced that G=1 iff for each prime p, there is some k (2..N) such that v_p(b_{k-1}) = e_p. Since e_p is max over i of v_p(b_i), there is some i with v_p(b_i) = e_p. Then for k = i+1, we have b_{k-1} = b_i, so condition holds. So it seems that for any sequence of ratios, G=1 always holds? That would imply every combination of ratios yields a good sequence. But the sample says there are 16 good sequences for N=6, A = [1,9,2,2,9]. Let's compute number of possible ratios per i:

A_1 = 1. Unitary divisors of 1: only 1. So (P1,Q1) = (1,1). So first ratio fixed.

A_2 = 9 = 3^2. Unitary divisors: 1, 3, 9? Wait unitary divisor d such that gcd(d,9/d)=1. For 9, divisors: 1,3,9. Check: d=1: 1 and 9 are coprime, yes. d=3: 3 and 3 are not coprime (gcd=3), so not unitary. d=9: 9 and 1 are coprime, yes. So unitary divisors are 1 and 9. So (P,Q) = (1,9) or (9,1). So two options.

A_3 = 2. Unitary divisors: 1,2. (1,2) or (2,1). Two options.

A_4 = 2. Same: 2 options.

A_5 = 9. Two options: (1,9) or (9,1).

Total combos: 1*2*2*2*2 = 16. Indeed there are 16 combos. And sample says there are 16 good sequences. So indeed all combos are good! So our earlier deduction that G=1 always holds might be correct for this case. Let's test with N=2, A_1=9. Unitary divisors: (1,9) or (9,1). Two combos, both yield good sequences. Sample output: 2 good sequences, both score 9. Let's compute:

Case (1,9): S1/S2 = 1/9 => S1=1, S2=9? Actually S1 = P * d, S2 = Q * d, with d positive integer. Since gcd(P,Q)=1, the ratio is P/Q. So S1 = d*P, S2 = d*Q. For (P,Q)=(1,9), S1=d, S2=9d. To have gcd(S1,S2)=1, we need gcd(d,9d)=d*gcd(1,9)=d = 1 => d=1. So sequence (1,9). Product = 9.

Case (P,Q)=(9,1): S1=9d, S2=d. gcd= d*gcd(9,1)=d => d=1. Sequence (9,1). Product = 9. So both good.

Thus for N=2, both combos are good. So maybe indeed all combos are good. Let's test with a case where maybe some combos are not good. For example, N=2, A=4. Unitary divisors: d must be coprime to 4/d. Divisors of 4: 1,2,4. d=1: 1 and 4 coprime => (1,4). d=2: 2 and 2 not coprime => no. d=4: 4 and 1 coprime => (4,1). So two combos. For (1,4): S1=d, S2=4d, gcd=d => d=1 => (1,4) product 4. For (4,1): S1=4d, S2=d, gcd=d => d=1 => (4,1) product 4. So both good.

What about N=3, A1=2, A2=2. Unitary divisors: each has (1,2) or (2,1). So 4 combos. Let's enumerate:

Sequence of ratios: (P1/Q1, P2/Q2). Compute S1, S2, S3.

Let’s denote P1,Q1 and P2,Q2. S1 = d1 * P1, S2 = d1 * Q1 = d2 * P2, S3 = d2 * Q2.

We need integer d1,d2 such that S1,S2,S3 integers (they are) and gcd(S1,S2,S3)=1.

We can set d1 = some integer, then S2 = d1*Q1 = d2*P2 => d2 = d1*Q1 / P2 must be integer. So d1 must be multiple of P2 / gcd(Q1, P2). Then gcd condition.

Let's test (P1,Q1) = (1,2), (P2,Q2) = (1,2). Then S1 = d1, S2 = 2 d1, S3 = 2 d2 = 2*(2 d1 / 1) = 4 d1. So sequence: (d1, 2d1, 4d1). gcd = d1. To be 1, d1=1. So (1,2,4) product 8.

Case (1,2) and (2,1): P1=1,Q1=2; P2=2,Q2=1. Then S1=d1, S2=2d1 = 2 d2? Wait S2 = d1*Q1 = 2 d1. Also S2 = d2*P2 = 2 d2. So 2 d1 = 2 d2 => d1 = d2. Then S3 = d2*Q2 = d2*1 = d1. So sequence: (d1, 2d1, d1). gcd = d1. Must be 1. So d1=1. Sequence (1,2,1). Product = 2.

Case (2,1) and (1,2): S1=2d1, S2= d1 = d2*1 => d2 = d1. S3 = d2*2 = 2d1. Sequence: (2d1, d1, 2d1). gcd = d1. So d1=1 => (2,1,2). Product = 4.

Case (2,1) and (2,1): S1=2d1, S2= d1 = 2 d2 => d2 = d1/2. Must be integer => d1 even. Let d1=2k, then d2=k. S3 = d2*1 = k. Sequence: (4k, 2k, k). gcd = k. So k=1 => (4,2,1). Product = 8.

All four combos yield a good sequence. So seems all combos are good.

Is there any case where no good sequence exists? Consider N=2, A=1. Unitary divisors: (1,1). Only one combo. S1=S2=d, gcd=d => d=1 => (1,1). Good.

Consider N=2, A=6. Unitary divisors of 6: divisors d where gcd(d,6/d)=1. 6=2*3. Divisors: 1,2,3,6. d=1: (1,6) coprime yes. d=2: (2,3) gcd(2,3)=1 yes. d=3: (3,2) yes. d=6: (6,1) yes. So 4 combos. Let's test (2,3): S1=2d, S2=3d, gcd=d => d=1 => (2,3) product 6. Similarly others. So all good.

It appears that for any choice of ratios, there is a unique scaling factor (d_i) that makes gcd=1. Wait earlier we argued that t must be 1 and G must be 1. But perhaps we made a mistake: S_1 = L * t, but t can be any positive integer, and gcd(S_1,...,S_N) = t * G. To have gcd=1, we need t * G = 1 => t=1 and G=1. So if G>1, no solution. But if G=1, then t must be 1, giving unique sequence. So the question is: does G=1 always hold? Let's compute G for a general sequence.

We have C_k = (L / b_{k-1}) * a_{k-1}. Since a_{k-1} and b_{k-1} are coprime. L is lcm of b_i.

Compute G = gcd(C_1, C_2, ..., C_N). C_1 = L.

We need to see if G is always 1. Let's test with a simple case: N=2, one ratio (P,Q) with P*Q = A. Then b_1 = P (since cumulative product is Q/P reduced: a_1 = Q, b_1 = P). L = lcm(P) = P. Then C_1 = L = P. C_2 = (L / b_1) * a_1 = (P / P) * Q = Q. So C_1 = P, C_2 = Q. G = gcd(P, Q) = 1 because P and Q are coprime (by definition of ratio). So G=1 always. Good.

N=3: ratios (P1,Q1), (P2,Q2). Compute cumulative:

a_1 = Q1, b_1 = P1.
a_2 = a_1 * Q2 / g2, b_2 = b_1 * P2 / g2, where g2 = gcd(a_1 * Q2, b_1 * P2) = gcd(Q1 * Q2, P1 * P2). Since P1,Q1 coprime, P2,Q2 coprime.

L = lcm(b_1, b_2) = lcm(P1, b_2). b_2 = (P1 * P2) / g2.

C_1 = L.
C_2 = (L / b_1) * a_1 = (L / P1) * Q1.
C_3 = (L / b_2) * a_2.

We need to see if gcd(L, C_2, C_3) = 1 always? Let's test with an example where P1=2, Q1=3 (so A1=6). P2=2, Q2=3 (A2=6). Compute:

a1=3, b1=2.
g2 = gcd(3*3=9, 2*2=4) = 1.
a2 = 3*3/1 = 9, b2 = 2*2/1 = 4.
L = lcm(2,4) = 4.
C1 = 4.
C2 = (4/2)*3 = 2*3 = 6.
C3 = (4/4)*9 = 9.
gcd(4,6,9) = 1. Yes.

Another example: P1=2, Q1=9 (A1=18). P2=3, Q2=2 (A2=6). Let's compute:

A1=2*9=18, unitary? gcd(2,9)=1 yes. A2=3*2=6, gcd(3,2)=1.

a1=9, b1=2.
g2 = gcd(9*2=18, 2*3=6) = gcd(18,6)=6.
a2 = (9*2)/6 = 3, b2 = (2*3)/6 = 1.
L = lcm(2,1) = 2.
C1 = 2.
C2 = (2/2)*9 = 9.
C3 = (2/1)*3 = 6.
gcd(2,9,6) = 1.

Seems always 1? Let's try to find a counterexample.

We need a prime p dividing L, and also dividing all C_k. Since C_1 = L, p divides C_1. For p to divide C_2, we need p | (L / b_1) * a_1. Since a_1 and b_1 are coprime, p could divide L/b_1 or a_1.

Case 1: p | b_1. Then b_1 contains p. Since b_1 = P1 (for N=2 case). In general, b_{k-1} may contain p. For C_2, denominator b_1 = P1. If p | b_1, then v_p(L/b_1) = v_p(L) - v_p(b_1). If v_p(L) = v_p(b_1), then L/b_1 has no p, and a_1 has no p (coprime), so C_2 not divisible by p. So p does not divide C_2. Thus gcd would not have p.

If v_p(L) > v_p(b_1), then L/b_1 has p, and a_1 has no p (since coprime), so C_2 has p. So to avoid p dividing all C_k, we need some k where v_p(b_{k-1}) = v_p(L). Since L is lcm of all b_i, there is some i with v_p(b_i) = v_p(L). Then for k = i+1, C_{k} will have no p. So G cannot have p. Therefore G=1 always.

Wait, is it guaranteed that for each prime p dividing L, there is some i such that v_p(b_i) = v_p(L)? Yes, by definition of L as lcm, the maximum exponent is attained. So there is at least one i where b_i has that exponent. Then for that i, C_{i+1} = (L / b_i) * a_i. Since L / b_i has exponent 0 for p, and a_i is coprime to b_i, so a_i has no p. Thus C_{i+1} not divisible by p. So p does not divide all C_k. Therefore G=1.

Thus for any sequence of ratios (P_i, Q_i) with gcd(P_i, Q_i)=1 and P_i*Q_i = A_i, the corresponding C sequence always has G=1. Therefore every choice of ratios yields exactly one good sequence.

Thus the number of good sequences equals the number of ways to choose for each i a unitary divisor of A_i (i.e., a divisor d of A_i such that gcd(d, A_i/d) = 1). And the sum of scores is the sum over all such choices of the product of S_i (or C_i) for the unique sequence determined.

Thus the problem reduces to: For each i (1..N-1), choose a unitary divisor d_i of A_i. Set P_i = d_i, Q_i = A_i / d_i. Then the unique good sequence S is defined as S_1 = L (the lcm of denominators b_i), and S_{k+1} = S_k * Q_k / P_k. Actually we can compute S directly: S_1 = L, and for each step, S_{i+1} = S_i * Q_i / P_i. Since S_i is integer.

Alternatively, we can compute the product of all S_i as described: product = L^N * (∏ a_i) / (∏ b_i), where a_i/b_i = ∏_{j=1}^{i} (Q_j / P_j) reduced.

But perhaps there is a simpler expression for the product in terms of the chosen d_i.

Let's attempt to find a formula for the product.

Let’s define for each i: ratio r_i = Q_i / P_i = (A_i / d_i) / d_i = A_i / d_i^2.

Since gcd(P_i, Q_i) = 1, we have d_i is a unitary divisor: d_i and A_i/d_i are coprime. This implies that d_i^2 divides A_i? Wait, if gcd(d_i, A_i/d_i) = 1, then d_i and A_i/d_i share no prime factors. So d_i is a product of some subset of prime powers of A_i, where each prime power is taken entirely. That is, if A_i = ∏ p^{e_p}, then d_i = ∏_{p in S} p^{e_p}, where S is a subset of primes dividing A_i. So d_i is a unitary divisor.

Then Q_i = A_i / d_i = ∏_{p not in S} p^{e_p}.

Thus ratio r_i = Q_i / P_i = (A_i / d_i) / d_i = A_i / d_i^2. Since d_i contains the full prime power for primes in S, and A_i/d_i contains the full prime powers for primes not in S, we have r_i = (∏_{p not in S} p^{e_p}) / (∏_{p in S} p^{e_p}) = ∏_{p} p^{e_p * (1_{p∉S} - 1_{p∈S})} = ∏_{p} p^{e_p * (1 - 2*1_{p∈S})}.

Thus r_i is a rational number where for each prime p dividing A_i, if p ∈ S (i.e., d_i includes p), then exponent is -e_p; if p ∉ S, exponent is +e_p. So r_i is essentially the product of p^{e_p} for primes not chosen in d_i, divided by p^{e_p} for primes chosen in d_i.

Thus r_i = ∏_{p|A_i} p^{e_p * (1 - 2*χ_i(p))}, where χ_i(p) = 1 if p|d_i, else 0.

Now the cumulative product after i steps: R_i = ∏_{j=1}^{i} r_j = ∏_{p} p^{∑_{j=1}^{i} e_{j,p} * (1 - 2*χ_j(p))}, where e_{j,p} is exponent of p in A_j (could be zero if p ∤ A_j). This is messy.

But maybe we can compute the product of S_i more directly.

Recall S_1 = L = lcm(b_1, ..., b_{N-1}), where b_i = denominator of R_i = ∏_{j=1}^{i} P_j / g_i? Actually b_i is the denominator of R_i in lowest terms. Since P_j and Q_j are coprime, but the product of P_j may share factors with Q_j, leading to cancellation.

However, note that P_j = d_j, Q_j = A_j / d_j. Since d_j and A_j/d_j are coprime, the prime factors of P_j and Q_j are disjoint. Thus across different j, P_j and Q_k may share primes if the same prime appears in both A_j and A_k. But the reduction step cancels common factors between the cumulative numerator and denominator.

But perhaps we can find a simpler expression for the product ∏ S_i.

Alternatively, we can compute S_i directly via the formula: S_{i+1} = S_i * Q_i / P_i. Starting from S_1 = L. Then S_i = L * ∏_{j=1}^{i-1} (Q_j / P_j). But we need to keep them integer. Since L is lcm of denominators, S_i is integer.

We can compute product P = ∏_{i=1}^{N} S_i = L^N * ∏_{i=1}^{N-1} (Q_i / P_i)^{N-i}? Let's derive:

S_1 = L.
S_2 = L * (Q_1 / P_1).
S_3 = L * (Q_1 / P_1) * (Q_2 / P_2).
...
S_k = L * ∏_{j=1}^{k-1} (Q_j / P_j).

Thus product over k=1..N: ∏_{k=1}^{N} S_k = L^N * ∏_{k=1}^{N} ∏_{j=1}^{k-1} (Q_j / P_j) = L^N * ∏_{j=1}^{N-1} (Q_j / P_j)^{N-j}.

Because each factor (Q_j / P_j) appears in S_{j+1}, S_{j+2}, ..., S_N, total (N - j) times.

Thus product = L^N * ∏_{j=1}^{N-1} (Q_j / P_j)^{N-j}.

Since Q_j / P_j = r_j = A_j / d_j^2.

Thus product = L^N * ∏_{j=1}^{N-1} (A_j / d_j^2)^{N-j}.

But we need to compute L and also ensure that the product is integer (it is, because each S_k is integer). The expression involves rational powers, but overall integer.

Alternatively, we can write product = L^N * ∏_{j=1}^{N-1} A_j^{N-j} / ∏_{j=1}^{N-1} d_j^{2(N-j)}.

Thus product = (L^N * ∏ A_j^{N-j}) / (∏ d_j^{2(N-j)}).

Since we need to compute this modulo 998244353, we can compute numerator and denominator modulo M, as long as denominator is invertible (i.e., not divisible by M). M is prime (998244353). Since A_j ≤ 1000, d_j ≤ A_j ≤ 1000, so denominator is product of small numbers, not divisible by M. So we can compute modular inverse.

But we also need L = lcm(b_1, ..., b_{N-1}). b_i are denominators of cumulative product.

We can compute b_i recursively: b_0 = 1. For i from 1 to N-1: let numerator = a_{i-1} * Q_i, denominator = b_{i-1} * P_i. Let g = gcd(numerator, denominator). Then a_i = numerator / g, b_i = denominator / g.

But we need to compute L = lcm(b_1, ..., b_{N-1}). Since b_i can be large (product of many numbers up to 1000, N up to 1000, product can be huge, far beyond 64-bit). But we only need the final product modulo M, and also L modulo M? Actually L appears in the product formula as L^N. So we need L modulo M. Since M is about 1e9, and L can be huge, but we can compute L modulo M, but careful: L appears in denominator? Actually product = L^N * something / something. Since we compute modulo M, we can compute L mod M, raise to N, multiply by other factors mod M. However, is the expression valid modulo M? The product is integer, so we can compute it modulo M by computing the integer value mod M. The formula L^N * ∏ A_j^{N-j} / ∏ d_j^{2(N-j)} is integer, so we can compute it modulo M by modular arithmetic, provided we compute L mod M, A_j mod M, d_j mod M, and use modular inverse for denominator. Since denominator is not divisible by M, it's fine.

But we need to compute L = lcm(b_1, ..., b_{N-1}) modulo M. However, L is defined as integer lcm, but we can compute it modulo M by computing each b_i modulo M and then computing lcm modulo M? LCM modulo M is not well-defined because lcm involves factoring, but we can compute L as integer (potentially huge) and then take mod M. Since N ≤ 1000 and b_i are products of numbers ≤ 1000, the exponents can be up to N * log(1000) ~ 1000*10 = 10000 bits, which is huge but we can handle with big integers in Python? Python supports big integers, but we need to compute L exactly to get L mod M. L can be astronomically large (product of many numbers up to 1000, each possibly with prime powers). For N=1000, L could be something like product of all primes up to 1000 raised to N? Actually each b_i is the denominator after reduction, which is a divisor of product of P_j. P_j are unitary divisors of A_j, each ≤ 1000. So b_i is a divisor of product of some of them. The lcm of many such numbers could be huge, but we can compute it using prime factorization: L = ∏ p^{max_i v_p(b_i)}.

Thus we can compute L's prime factorization. Since primes up to 1000, and exponent per prime could be up to N * max exponent in a single P_j. P_j is a unitary divisor of A_j, so its prime exponents are either 0 or full exponent of A_j. For a given prime p, v_p(P_j) is either 0 or e_{j,p} (the exponent of p in A_j). Since P_j and Q_j are coprime, the prime factors of P_j are those primes where we chose to put the full power in P_j.

Now b_i is the denominator of the cumulative product after i steps. The denominator b_i is obtained by starting with 1, and for each step, multiply by P_j and cancel common factors with the numerator.

But perhaps we can compute the exponents of L directly from the sequence of choices.

We need to compute for each prime p, the maximum exponent of p in any b_i (i from 1 to N-1). Let's denote e_p = max_{1≤i≤N-1} v_p(b_i). Then L = ∏ p^{e_p}.

Thus we need to track the sequence of b_i exponents.

We can think of the process as a random walk on exponents: we have a current rational a/b (with a,b coprime). At step i, we multiply by Q_i/P_i. Since P_i and Q_i are coprime, the multiplication adds exponents of primes in P_i to denominator, and exponents of primes in Q_i to numerator, then reduce by canceling any common factors between new numerator and denominator.

But because P_i and Q_i have disjoint prime sets (since they are coprime and their product is A_i, and each prime's full power goes either to P_i or Q_i), the cancellation can only happen between the new numerator (a_{i-1} * Q_i) and the new denominator (b_{i-1} * P_i). Since Q_i's primes are disjoint from P_i's primes, the only possible cancellation is between Q_i and the existing denominator b_{i-1}, or between P_i and the existing numerator a_{i-1}. Because a_{i-1} and b_{i-1} are coprime, but they may share primes with Q_i or P_i respectively.

Specifically, let’s write a_{i-1} and b_{i-1} coprime. Multiply by Q_i (which has primes not in P_i) and by P_i (which has primes not in Q_i). The new numerator is a_{i-1} * Q_i, denominator is b_{i-1} * P_i. The gcd of these is gcd(a_{i-1} * Q_i, b_{i-1} * P_i). Since a_{i-1} and b_{i-1} are coprime, and Q_i shares no primes with P_i, we can separate:

gcd(a_{i-1} * Q_i, b_{i-1} * P_i) = gcd(a_{i-1}, b_{i-1} * P_i) * gcd(Q_i, b_{i-1} * P_i) / gcd(...)? Actually since a_{i-1} and b_{i-1} coprime, any common factor must involve a_{i-1} with P_i (since a_{i-1} shares no primes with b_{i-1}), or Q_i with b_{i-1} (since Q_i shares no primes with P_i). Also possible that a_{i-1} shares with b_{i-1}? No. So gcd = gcd(a_{i-1}, P_i) * gcd(Q_i, b_{i-1}). Because a_{i-1} and b_{i-1} are coprime, so gcd(a_{i-1}, b_{i-1}) = 1. Also a_{i-1} and Q_i are coprime? Not necessarily: a_{i-1} may have prime factors that are in Q_i if those primes were introduced in previous steps as numerators. Similarly, b_{i-1} may have prime factors that are in P_i.

But note that P_i and Q_i have disjoint prime sets. So the primes in P_i are a subset of primes dividing A_i, and similarly for Q_i. a_{i-1} may contain primes from previous Q_j's. b_{i-1} may contain primes from previous P_j's.

Thus the cancellation g_i = gcd(a_{i-1} * Q_i, b_{i-1} * P_i) = gcd(a_{i-1}, P_i) * gcd(Q_i, b_{i-1}) * gcd(a_{i-1}, b_{i-1})? Wait a_{i-1} and b_{i-1} are coprime, so last term is 1. Also need to consider if any prime appears in both a_{i-1} and Q_i? That would be a common factor between a_{i-1} and Q_i, but since we are computing gcd of product a_{i-1}*Q_i with b_{i-1}*P_i, a prime that divides both a_{i-1} and Q_i would divide the numerator, but does it divide the denominator? It would divide denominator only if it also divides b_{i-1}*P_i. Since it divides a_{i-1}, and a_{i-1} and b_{i-1} are coprime, it does not divide b_{i-1}. Does it divide P_i? Since P_i and Q_i are coprime, if a prime divides Q_i, it does not divide P_i. So such a prime does not divide denominator. So it doesn't contribute to gcd. Similarly, a prime dividing both Q_i and b_{i-1} is a candidate. A prime dividing both P_i and a_{i-1} is a candidate. A prime dividing both P_i and b_{i-1}? Since b_{i-1} and a_{i-1} are coprime, but P_i and b_{i-1} could share primes? b_{i-1} contains primes from previous P_j's. P_i is a unitary divisor of A_i, which may share primes with previous A_j's. So yes, b_{i-1} may have primes that are also in P_i. In that case, that prime divides both P_i and b_{i-1}, so divides denominator. Does it divide numerator a_{i-1}*Q_i? It could divide Q_i? No, because P_i and Q_i are coprime. It could divide a_{i-1}? Possibly, if that prime was introduced as a numerator in a previous step and not cancelled. But if it divides b_{i-1}, it does not divide a_{i-1} (coprime). So a prime dividing P_i and b_{i-1} divides denominator but not numerator, so not in gcd. So the only contributions to gcd are from primes that divide both a_{i-1} and P_i, or both Q_i and b_{i-1}.

Thus g_i = gcd(a_{i-1}, P_i) * gcd(Q_i, b_{i-1}).

Since a_{i-1} and b_{i-1} are coprime, and P_i and Q_i are coprime, these two gcds are coprime to each other (no overlapping primes). So g_i is product of two coprime numbers.

Thus we can write:

a_i = a_{i-1} * Q_i / (gcd(Q_i, b_{i-1}) * gcd(a_{i-1}, P_i)?) Wait need to divide by g_i = gcd(a_{i-1}, P_i) * gcd(Q_i, b_{i-1}).

But note: a_{i-1} * Q_i may have common factors with b_{i-1} * P_i. The factor gcd(a_{i-1}, P_i) cancels some part of P_i from denominator, and gcd(Q_i, b_{i-1}) cancels some part of b_{i-1} from denominator? Actually denominator is b_{i-1} * P_i. The gcd includes factors from b_{i-1} (specifically those that also divide Q_i) and factors from P_i (those that also divide a_{i-1}). So after division:

New denominator b_i = (b_{i-1} * P_i) / (gcd(Q_i, b_{i-1}) * gcd(a_{i-1}, P_i)).

Similarly, new numerator a_i = (a_{i-1} * Q_i) / (gcd(Q_i, b_{i-1}) * gcd(a_{i-1}, P_i)).

But since a_{i-1} and b_{i-1} are coprime, gcd(a_{i-1}, P_i) is the part of P_i that is already present in a_{i-1} (i.e., primes that were previously in numerators). Similarly, gcd(Q_i, b_{i-1}) is the part of Q_i that is already present in denominator (primes previously in denominators).

Thus the process is: we have a current fraction a/b. For each step, we choose a split of A_i into P_i and Q_i (disjoint prime sets). Then we multiply numerator by Q_i, denominator by P_i, then cancel any common factors: primes that appear in both numerator and denominator (i.e., primes that were in Q_i and previously in denominator, or primes that were in P_i and previously in numerator). This reduces the fraction.

Thus the exponent of a prime p in b_i after step i depends on the history: it increases when p appears in P_i and is not cancelled by a_{i-1}, and decreases when p appears in Q_i and cancels with b_{i-1} (if p was present in denominator). Actually p appears in b_{i-1} (denominator) if it was previously in some P_j and not cancelled. Then if p appears in Q_i, it cancels that amount from denominator (since Q_i * b_{i-1} shares p). If p appears in P_i and not in a_{i-1}, it adds to denominator. If p appears in both Q_i and a_{i-1}? No, Q_i and a_{i-1} are coprime? Not necessarily: a_{i-1} may contain p if p was previously in a Q_j and not cancelled. But Q_i and a_{i-1} can share primes: p could be in a_{i-1} (as a numerator) and also in Q_i (as a numerator now). Then p would be in numerator a_{i-1} * Q_i, but not in denominator (since P_i doesn't have p). So p would stay in numerator, increasing exponent in a_i.

Thus the exponent of p in b_i evolves as:

v_p(b_i) = v_p(b_{i-1}) + v_p(P_i) - min(v_p(b_{i-1}), v_p(Q_i)) - min(v_p(a_{i-1}), v_p(P_i))? Wait, need to be careful.

Let x = v_p(b_{i-1}), y = v_p(a_{i-1}). Since a_{i-1} and b_{i-1} are coprime, at most one of x,y is non-zero.

Now v_p(P_i) = e_{i,p} if p ∈ S_i (i.e., p chosen in denominator), else 0.
v_p(Q_i) = e_{i,p} if p ∉ S_i, else 0.

Since P_i and Q_i are disjoint, exactly one of v_p(P_i), v_p(Q_i) equals e_{i,p}, the other 0.

Now compute g_i = gcd(a_{i-1} * Q_i, b_{i-1} * P_i). The exponent of p in g_i is:

v_p(g_i) = min( v_p(a_{i-1}) + v_p(Q_i), v_p(b_{i-1}) + v_p(P_i) ).

But since a_{i-1} and b_{i-1} are coprime, at most one of v_p(a_{i-1}), v_p(b_{i-1}) is non-zero. So two cases:

Case A: v_p(b_{i-1}) > 0, v_p(a_{i-1}) = 0.
Then v_p(g_i) = min( v_p(Q_i), v_p(b_{i-1}) + v_p(P_i) ).
But v_p(Q_i) is either 0 or e_{i,p}. If p is in Q_i (so v_p(Q_i) = e_{i,p} > 0), then min(e_{i,p}, x + v_p(P_i)). If p is in P_i, then v_p(Q_i)=0, so min(0, x + v_p(P_i)) = 0.

Case B: v_p(a_{i-1}) > 0, v_p(b_{i-1}) = 0.
Then v_p(g_i) = min( v_p(a_{i-1}) + v_p(Q_i), v_p(P_i) ).
If p in P_i (v_p(P_i)=e_{i,p}), then min(y + v_p(Q_i), e_{i,p}). If p in Q_i, v_p(P_i)=0, min(y + e_{i,p}, 0) = 0.

Thus v_p(g_i) = 
- If p in Q_i: min(e_{i,p}, x) (since v_p(P_i)=0).
- If p in P_i: min(y, e_{i,p}) (since v_p(Q_i)=0).
(where x = v_p(b_{i-1}), y = v_p(a_{i-1})).

Thus the cancellation is limited by the existing exponent in the opposite part.

Then new exponent in denominator:

v_p(b_i) = v_p(b_{i-1}) + v_p(P_i) - v_p(g_i).

Similarly, v_p(a_i) = v_p(a_{i-1}) + v_p(Q_i) - v_p(g_i).

Since v_p(g_i) is the amount cancelled from both numerator and denominator.

Now, since