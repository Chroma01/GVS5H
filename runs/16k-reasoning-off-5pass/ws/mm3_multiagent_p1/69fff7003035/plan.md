We need to compute the sum over all permutations P of (1..N) of the integer formed by concatenating the decimal strings of P_i. Each permutation contributes a number whose value can be expressed as Σ_i P_i * 10^{total_len_of_suffix_i}, where suffix_len_i = sum of lengths of elements after position i. Since each element appears equally often in each position across all permutations, the contribution of value v to the sum is v * (number of permutations where v is at position i) * 10^{suffix_len_i}. The number of permutations with v at position i is (N-1)! (any arrangement of the remaining N-1 elements). However, the suffix length depends on which elements are after v, not just the count. So we need to sum over all permutations: Σ_{perm} Σ_{i} P_i * 10^{len(P_{i+1})+...+len(P_N)}.

We can rewrite the total sum as Σ_{i=1}^N Σ_{perm} P_i * 10^{suffix_len_i}. For a fixed position i, the factor 10^{suffix_len_i} depends on the set of elements placed after position i. Since each element appears in position i in (N-1)! permutations, but the suffix length varies. We can think of building permutations sequentially: choose an ordering of all N elements. The contribution of element x when placed at some position is x * 10^{sum of lengths of elements that come after it}. So the total sum equals Σ_{x=1}^N x * (sum over all permutations of 10^{sum of lengths of elements after x}).

For a fixed x, consider all permutations of the remaining N-1 elements. The elements after x form some subset S of the other N-1 elements, and the order of S matters only for the lengths sum (which is sum of lengths of elements in S, independent of order). Actually 10^{sum of lengths} depends only on the set S, not on the order within S. So for each subset S of {1..N}\{x}, the number of permutations where the elements after x are exactly S (in any order) is: choose which elements are after x (that's the subset S), then arrange them in any order, and arrange the elements before x (the complement) in any order. So count = |S|! * (N-1-|S|)!.

Thus contribution of x is x * Σ_{k=0}^{N-1} (number of subsets of size k) * k! * (N-1-k)! * 10^{sum of lengths of elements in a size-k subset}. But the sum of lengths depends on which specific elements are in the subset, not just size. So we need to sum over all subsets S of size k: 10^{sum_{y in S} len(y)}.

Let L[y] = number of digits of y. We need to compute for each k: Σ_{S subset of [N]\{x}, |S|=k} 10^{Σ_{y in S} L[y]}. This is like a combinatorial sum over subsets with weights. Since N up to 2e5, we need an efficient method.

Observation: The function 10^{Σ L[y]} is multiplicative over elements: 10^{Σ L[y]} = Π_{y in S} 10^{L[y]}. So the sum over subsets of size k of product of weights w_y = 10^{L[y]}. This is the elementary symmetric sum e_k of the multiset {w_y : y ≠ x}. So the contribution of x is x * Σ_{k=0}^{N-1} e_k^{(x)} * k! * (N-1-k)!, where e_k^{(x)} is the k-th elementary symmetric sum of the weights of all elements except x.

Thus total sum = Σ_{x=1}^N x * Σ_{k=0}^{N-1} e_k^{(x)} * k! * (N-1-k)!.

We can precompute factorials and inverse factorials modulo MOD = 998244353.

Now we need to compute e_k^{(x)} for all x efficiently. Since N is large (2e5), we need O(N log N) or O(N) time.

Let w_i = 10^{L[i]} mod MOD. Then e_k^{(x)} is the elementary symmetric sum of all w_i except w_x. We can compute the full symmetric sums E_k = Σ_{S subset of [N], |S|=k} Π_{i in S} w_i for all k. Then e_k^{(x)} = E_k - w_x * e_{k-1}^{(x)}? Actually we can use the relation: E_k = e_k^{(x)} + w_x * e_{k-1}^{(x)}. Because any subset of size k either does not contain x (contributing to e_k^{(x)}) or contains x (contributing w_x times a subset of size k-1 from the rest). So e_k^{(x)} = E_k - w_x * e_{k-1}^{(x)}. This is a recurrence that allows us to compute e_k^{(x)} for all k given E_k and w_x, but we need e_{k-1}^{(x)} to compute e_k^{(x)}. However, we can compute e_k^{(x)} for all x and k using DP or generating functions.

Alternatively, we can compute the generating polynomial P(t) = Π_{i=1}^N (1 + w_i t). Then E_k is coefficient of t^k. For each x, the polynomial without x is P(t) / (1 + w_x t). So e_k^{(x)} are coefficients of that quotient. We can compute P(t) as a polynomial of degree N (but N is 2e5, we can store array of length N+1). Then for each x, we can compute the coefficients of Q_x(t) = P(t) / (1 + w_x t) using the recurrence: Q_x(t) = P(t) * (1 - w_x t + w_x^2 t^2 - ... )? Actually division by (1 + w t) can be done via recurrence: if Q(t) = Σ q_k t^k, then (1 + w t) Q(t) = P(t). So q_k + w * q_{k-1} = p_k, with q_{-1}=0. Thus q_k = p_k - w * q_{k-1}. So we can compute q_k for k=0..N-1 (since degree reduces by 1). This is O(N) per x, too slow.

But we can use the fact that we need Σ_{k} e_k^{(x)} * k! * (N-1-k)!. Let's denote F_x = Σ_{k=0}^{N-1} e_k^{(x)} * k! * (N-1-k)!. Then total sum = Σ_x x * F_x.

We can try to compute F_x efficiently using convolution or generating functions.

Let’s define A_k = e_k^{(x)} (for a fixed x). Then F_x = Σ_{k} A_k * k! * (N-1-k)!.

We can write F_x = (N-1)! * Σ_{k} A_k / C(N-1, k). Because k! * (N-1-k)! = (N-1)! / C(N-1, k). So F_x = (N-1)! * Σ_{k=0}^{N-1} A_k * invC(N-1, k), where invC is modular inverse of binomial coefficient.

Thus total sum = (N-1)! * Σ_{x=1}^N x * Σ_{k=0}^{N-1} e_k^{(x)} * invC(N-1, k).

Now Σ_{x} x * e_k^{(x)} is something we can compute. Let's denote S_k = Σ_{x=1}^N x * e_k^{(x)}. Then total sum = (N-1)! * Σ_{k=0}^{N-1} S_k * invC(N-1, k).

So we need to compute S_k for all k from 0 to N-1.

Now e_k^{(x)} is the elementary symmetric sum of weights of all elements except x. So x * e_k^{(x)} = x * Σ_{S subset of [N]\{x}, |S|=k} Π_{i in S} w_i.

Thus S_k = Σ_{x=1}^N x * Σ_{S subset of [N]\{x}, |S|=k} Π_{i in S} w_i.

We can swap sums: S_k = Σ_{S subset of [N], |S|=k} (Π_{i in S} w_i) * (sum of x over x not in S). Because for a fixed subset S of size k, the term x * Π_{i in S} w_i appears for each x not in S. So S_k = Σ_{S, |S|=k} (Π_{i in S} w_i) * (sum_{x ∉ S} x).

Let total_sum = Σ_{i=1}^N i = N(N+1)/2. Then sum_{x ∉ S} x = total_sum - sum_{i in S} i.

Thus S_k = total_sum * E_k - Σ_{S, |S|=k} (Π_{i in S} w_i) * (sum_{i in S} i).

Now we need to compute T_k = Σ_{S, |S|=k} (Π_{i in S} w_i) * (sum_{i in S} i). This is like a weighted elementary symmetric sum where each element i contributes weight w_i and also a "value" i. We can compute this using generating functions with two variables? Or we can compute it by considering the polynomial Q(t) = Σ_{i=1}^N i * w_i * t^{?}. Actually we can define a polynomial R(t) = Σ_{i=1}^N (w_i * t) * something? Let's think.

We want to compute for each k: Σ_{S, |S|=k} (Π_{i in S} w_i) * (Σ_{i in S} i). This is the coefficient of t^k in the expansion of (Σ_{i} i * w_i * t) * Π_{j ≠ i} (1 + w_j t)? Not exactly.

Alternatively, we can compute the generating function G(t) = Π_{i=1}^N (1 + w_i t). Then E_k = [t^k] G(t). To get T_k, we can consider derivative with respect to some parameter. Let’s define H(t) = Σ_{i=1}^N i * w_i * t * Π_{j ≠ i} (1 + w_j t). Actually note that:

∂/∂t (Π_{i} (1 + w_i t)) = Σ_{i} w_i * Π_{j ≠ i} (1 + w_j t).

But we need sum of i times product. So consider F(t) = Σ_{i} i * w_i * Π_{j ≠ i} (1 + w_j t). Then the coefficient of t^{k-1} in F(t) is Σ_{S, |S|=k} (Π_{i in S} w_i) * (sum_{i in S} i). Because when we expand F(t), each term i * w_i * Π_{j ≠ i} (1 + w_j t) contributes i times the product of (1 + w_j t) for j≠i. The coefficient of t^{k-1} in that product corresponds to choosing k-1 elements from the set {j≠i} to include their w_j factor, and the product includes w_i as well, giving total k elements. The sum over i of i times that product yields exactly T_k.

Thus T_k = coefficient of t^{k-1} in F(t) = Σ_{i} i * w_i * Π_{j ≠ i} (1 + w_j t).

We can compute F(t) efficiently? Note that Π_{j ≠ i} (1 + w_j t) = G(t) / (1 + w_i t). So F(t) = Σ_{i} i * w_i * G(t) / (1 + w_i t) = G(t) * Σ_{i} i * w_i / (1 + w_i t).

Thus T_k is coefficient of t^{k-1} in G(t) * Σ_{i} i * w_i / (1 + w_i t). This seems complicated.

Alternatively, we can compute T_k directly using a DP similar to computing elementary symmetric sums with weights. Since N is 2e5, we can compute E_k and also T_k in O(N^2) naive, but we need O(N log N) or O(N).

We can compute E_k using standard DP: initialize E_0 = 1, E_k = 0 for k>0. For each i from 1 to N: for k from i down to 1: E_k = E_k + w_i * E_{k-1}. This is O(N^2) which is too slow for N=2e5.

But we can use the fact that w_i = 10^{L[i]} takes only a few distinct values? Let's examine L[i] = number of digits of i. For i from 1 to N, L[i] is small: for N up to 2e5, digits are 1 to 6 (since 2e5 < 10^6). Actually 2e5 = 200,000, which has 6 digits? 200,000 is 6 digits? 200,000 has 6 digits (2*10^5). Wait 10^5 = 100,000 (6 digits? 100000 is 6 digits). Actually digits: 1-9: 1 digit; 10-99: 2 digits; 100-999: 3 digits; 1000-9999: 4 digits; 10000-99999: 5 digits; 100000-199999: 6 digits. So up to 2e5, we have digits 1 to 6. So w_i = 10^{d} where d is number of digits. So w_i takes only 6 possible values: 10, 100, 1000, 10000, 100000, 1000000. That's constant! Great.

Thus we have only a constant number of distinct weights. Let’s denote the groups: for each digit length d (1 to 6), let count c_d = number of integers i in [1,N] with L[i]=d. And the actual values i vary within the group. But w_i depends only on d, not on i. However, the factor i in the sum S_k depends on the actual value i, not just the digit length. So we cannot treat all elements with same weight as identical because the coefficient i differs.

But we can still use the fact that w_i is constant within groups. So we can compute E_k as product of (1 + w t) raised to counts? Actually E_k is the elementary symmetric sum of the multiset of w_i. Since w_i are not all distinct but there are only 6 distinct values, we can compute the generating function G(t) = Π_{i=1}^N (1 + w_i t) = Π_{d=1}^6 (1 + 10^d t)^{c_d}. This is a product of polynomials (1 + a t)^{c} where a = 10^d. We can expand this product efficiently using convolution? Since c_d can be up to N (e.g., c_1 = 9, c_2 = 90, etc., but total N=2e5). The degree of G(t) is N. We need coefficients up to degree N. We can compute G(t) by multiplying polynomials (1 + a t)^{c} for each d. But (1 + a t)^{c} is a polynomial of degree c. Multiplying 6 such polynomials of degree up to N each would be O(N^2) if done naively. However, we can use the fact that a is a constant and we can compute the coefficients of (1 + a t)^c using binomial coefficients: coefficient of t^k is C(c, k) * a^k. So G(t) = Σ_{k=0}^N ( Σ_{ (k1+...+k6 = k) } Π_{d=1}^6 C(c_d, k_d) * (10^d)^{k_d} ) t^k.

Thus E_k = Σ_{k1+...+k6 = k} Π_{d=1}^6 C(c_d, k_d) * (10^d)^{k_d}.

This is a convolution of 6 sequences. Since 6 is constant, we can compute E_k for all k using multi-dimensional DP or iterative convolution. For each d, we have a sequence A^{(d)}_k = C(c_d, k) * (10^d)^k for k=0..c_d. Then E is the convolution of these 6 sequences. We can compute it by starting with array E of length N+1 initialized to [1,0,0,...], then for each d, convolve E with A^{(d)}. Since each A^{(d)} has length c_d+1, and c_d sum to N, the total work if we do naive convolution O(N * c_d) per d would be O(N^2). But we can use FFT (NTT) to convolve in O(N log N). Since MOD = 998244353 is NTT-friendly, we can use NTT to multiply polynomials. However, we have 6 polynomials, we can multiply them sequentially using NTT. Each multiplication of two polynomials of degree up to N takes O(N log N). With 5 multiplications (since 6 polynomials), total O(N log N). That's feasible for N=2e5.

But we also need T_k = Σ_{S, |S|=k} (Π w_i) * (sum i in S). We can compute T_k similarly using generating functions with two variables? Or we can compute S_k directly using a similar approach.

Recall S_k = total_sum * E_k - T_k. So if we can compute T_k, we get S_k.

Now T_k = coefficient of t^{k-1} in F(t) = Σ_{i} i * w_i * Π_{j ≠ i} (1 + w_j t). As we wrote, F(t) = G(t) * Σ_{i} i * w_i / (1 + w_i t). But maybe we can compute T_k using a similar combinatorial decomposition by digit groups.

Since w_i depends only on digit length d, we can group by d. Let’s denote for each d, the set of indices I_d = {i : L[i]=d}. For i in I_d, w_i = 10^d. Then T_k = Σ_{S, |S|=k} (Π_{i in S} 10^{L[i]}) * (Σ_{i in S} i).

We can write T_k = Σ_{d1,...,d6} (10^{d1+...+d6}) * (sum of i over i in S) where S has k elements with specified digit lengths. But the sum of i depends on which specific i's are chosen, not just the counts per group.

We can compute T_k by considering the generating function H(t) = Σ_{i=1}^N i * w_i * t * Π_{j ≠ i} (1 + w_j t). But we can also compute T_k by using the derivative of G(t) with respect to a parameter that encodes i. Let's define a bivariate generating function: G(x, t) = Π_{i=1}^N (1 + w_i t * x^i). Then coefficient of x^a t^k is sum over subsets S of size k with product of w_i and x^{sum i in S}. Then T_k is the coefficient of t^k in ∂/∂x G(x,t) evaluated at x=1? Actually we want sum of i in S times product w_i. That is the derivative with respect to x at x=1: ∂/∂x G(x,t) |_{x=1} = Σ_{i} i * w_i t * Π_{j ≠ i} (1 + w_j t). So indeed F(t) = ∂/∂x G(x,t) |_{x=1}. So T_k is coefficient of t^{k-1} in F(t). So we need to compute the coefficients of F(t).

We can compute G(x,t) as a polynomial in t with coefficients that are polynomials in x. Since x is a formal variable, we can treat x as a constant and compute the polynomial in t. But the degree in x is huge (up to sum of i). However, we only need the derivative at x=1, which is a linear combination of the coefficients.

Alternatively, we can compute T_k by a DP that tracks both the number of elements and the sum of indices. Since w_i depends only on digit length, we can process groups.

Let’s define for each digit length d, we have a set of indices I_d. For each i in I_d, we have weight w = 10^d and value i. We want to compute the polynomial in t: P_d(t) = Σ_{i in I_d} (1 + i * w * t) ??? Not exactly.

We can think of building the generating function G(t) = Π_{i} (1 + w_i t). To incorporate the sum of i, we can consider the logarithmic derivative: d/dt log G(t) = Σ_i w_i / (1 + w_i t). Then G(t) * d/dt log G(t) = Σ_i w_i * Π_{j ≠ i} (1 + w_j t). That's close but we need i * w_i instead of w_i. So if we had a weighted version where each element i contributes weight w_i and also a factor i, we could use a similar trick.

Define H(t) = Σ_{i} i * w_i * Π_{j ≠ i} (1 + w_j t). We can write H(t) = G(t) * Σ_i i * w_i / (1 + w_i t). So if we can compute the series Σ_i i * w_i / (1 + w_i t) modulo t^N, we can multiply by G(t) to get H(t). Then T_k is coefficient of t^{k-1} in H(t).

Now Σ_i i * w_i / (1 + w_i t) = Σ_i i * w_i * Σ_{m=0}^∞ (-w_i t)^m = Σ_{m=0}^∞ (-1)^m t^m * Σ_i i * w_i^{m+1}.

Thus the coefficient of t^m in that series is (-1)^m * Σ_i i * w_i^{m+1}. Since w_i = 10^{L[i]}, w_i^{m+1} = 10^{(m+1)*L[i]}. So we need to compute for each m (0 <= m <= N-1) the sum A_m = Σ_{i=1}^N i * 10^{(m+1)*L[i]}. Then the series is Σ_{m>=0} (-1)^m A_m t^m.

Then H(t) = G(t) * Σ_{m>=0} (-1)^m A_m t^m. So the coefficient of t^{k-1} in H(t) is Σ_{m=0}^{k-1} (-1)^m A_m * E_{k-1-m} (where E_j is coefficient of t^j in G(t)). Because convolution: H(t) = Σ_{j} E_j t^j * Σ_{m} (-1)^m A_m t^m = Σ_{k} ( Σ_{m=0}^k (-1)^m A_m E_{k-m} ) t^k.

Thus T_k = coefficient of t^{k-1} in H(t) = Σ_{m=0}^{k-1} (-1)^m A_m * E_{k-1-m}.

We need T_k for k=1..N (k=0 term is 0). So we can compute E_j for j=0..N (the elementary symmetric sums of w_i). Then compute A_m for m=0..N-1. Then compute T_k via convolution.

Now we need to compute A_m = Σ_{i=1}^N i * 10^{(m+1)*L[i]}. Since L[i] is small (1 to 6), we can group by digit length d. For each d, let S_d = Σ_{i: L[i]=d} i. Then A_m = Σ_{d=1}^6 10^{(m+1)*d} * S_d.

Thus A_m is a linear combination of 6 terms: A_m = Σ_{d=1}^6 S_d * (10^d)^{m+1}. So we can precompute S_d for each d.

Now we need to compute E_j = coefficient of t^j in G(t) = Π_{d=1}^6 (1 + 10^d t)^{c_d}. We can compute E_j using NTT as described: compute the polynomial (1 + 10^d t)^{c_d} for each d, then multiply them. Since c_d can be up to N, but we only need coefficients up to degree N. We can compute each (1 + a t)^{c} as a polynomial of degree c using binomial coefficients: coefficient of t^k is C(c, k) * a^k. So we can generate an array of length c+1 for each d. Then multiply these 6 arrays using NTT. Since N=2e5, we can do NTT with size power of two >= 2N. That's fine.

Alternatively, we can compute E_j via DP using the fact that there are only 6 groups. Since c_d are not huge (c_1=9, c_2=90, c_3=900, c_4=9000, c_5=90000, c_6=200000-111111=88889? Actually for N=200000, digits: 1-9:9, 10-99:90, 100-999:900, 1000-9999:9000, 10000-99999:90000, 100000-200000:100001? Wait 100000 to 200000 inclusive is 100001 numbers. But total N=200000, so c_6 = 200000 - (9+90+900+9000+90000) = 200000 - 99999 = 100001. So c_6 = 100001. So the largest c_d is about 100k. Multiplying polynomials of degree up to 100k using NTT is O(N log N). With 6 multiplications, total O(N log N). That's acceptable.

But we also need to compute T_k = Σ_{m=0}^{k-1} (-1)^m A_m * E_{k-1-m}. This is a convolution of sequences A_m (with sign) and E_j. Specifically, define B_m = (-1)^m A_m for m=0..N-1. Then T_k = Σ_{m=0}^{k-1} B_m * E_{k-1-m} = (B * E)[k-1] (convolution). So we can compute the convolution of B and E using NTT as well. Since lengths are N and N+1, convolution length up to 2N-1. We need T_k for k=1..N, i.e., indices 0..N-1 of the convolution result.

Thus overall algorithm:

1. Precompute factorials and inverse factorials up to N for binomial coefficients and for final formula.
2. Compute c_d and S_d for d=1..6 (or up to max digit length for N).
3. Compute w_d = 10^d mod MOD.
4. Compute polynomial G(t) = Π_{d} (1 + w_d t)^{c_d}. We can compute each factor as an array F_d of length c_d+1: F_d[k] = C(c_d, k) * w_d^k mod MOD. Then multiply all F_d using NTT to get E array of length N+1 (E[0]=1).
5. Compute A_m for m=0..N-1: A_m = Σ_{d} S_d * (w_d)^{m+1} mod MOD. Since w_d^{m+1} = w_d * (w_d)^m. We can precompute powers of w_d for each d up to m=N. Since m up to N-1, and d up to 6, we can compute for each d an array pow_d[m] = w_d^m for m=0..N. Then A_m = Σ_d S_d * w_d * pow_d[m] (since (w_d)^{m+1} = w_d * w_d^m). Actually (w_d)^{m+1} = w_d * (w_d)^m. So A_m = Σ_d S_d * w_d * (w_d)^m.
6. Compute B_m = (-1)^m * A_m mod MOD.
7. Compute convolution C = B * E (where E is length N+1, B is length N). We need C[k] for k=0..N-1 (since T_{k+1} = C[k]). Actually T_k = C[k-1] for k>=1. So we can compute C array of length up to 2N. Then T_k = C[k-1] for k=1..N.
8. Compute S_k = total_sum * E_k - T_k for k=0..N-1 (note T_0 = 0). total_sum = N*(N+1)/2 mod MOD.
9. Compute invC(N-1, k) for k=0..N-1. We can precompute factorials and inv factorials: invC(n,k) = fact[n] * invfact[k] * invfact[n-k] mod MOD? Actually C(n,k) = fact[n] * invfact[k] * invfact[n-k]. So invC(n,k) = inv(C(n,k)) = invfact[n]^{-1}? Wait we need modular inverse of binomial coefficient. Since MOD is prime, invC(n,k) = inv(C(n,k)) = inv(fact[n] * invfact[k] * invfact[n-k]) = invfact[n]^{-1}? Actually we can compute invC(n,k) = inv(C(n,k)) = C(n,k)^{-1} mod MOD. Since C(n,k) = fact[n] * invfact[k] * invfact[n-k] mod MOD. So invC(n,k) = inv(fact[n]) * fact[k] * fact[n-k] mod MOD. Because inv(C) = inv(fact[n]) * fact[k] * fact[n-k]. So we can precompute fact and invfact, then compute invC = invfact[n] * fact[k] % MOD * fact[n-k] % MOD. But careful: invfact[n] is the modular inverse of fact[n]. So invC(n,k) = invfact[n] * fact[k] % MOD * fact[n-k] % MOD. Yes.

Alternatively, we can compute the term k! * (N-1-k)! directly and multiply by inv of (N-1)!? Actually we had F_x = (N-1)! * Σ e_k^{(x)} * invC(N-1,k). So we need invC(N-1,k). So we can precompute invC for all k.

10. Compute total sum = (N-1)! * Σ_{k=0}^{N-1} S_k * invC(N-1,k) mod MOD.

But careful: S_k is defined for k from 0 to N-1? Actually e_k^{(x)} is defined for k from 0 to N-1 (since we exclude x). So k ranges 0..N-1. So S_k is for k=0..N-1. E_k is defined for k=0..N (full set). But we need E_k for k up to N-1 in the convolution. So we can compute E up to N.

Now we need to ensure that the convolution for T_k uses E_{k-1-m} where m from 0 to k-1. So we need E indices up to N-1. That's fine.

Now we need to compute the convolution efficiently. Since N is up to 2e5, we can use NTT. We'll need to implement NTT for MOD=998244353, which is a prime with primitive root 3. We can use standard NTT implementation.

Steps in detail:

- Read N.
- Precompute factorials fact[0..N] and invfact[0..N] modulo MOD.
- Compute total_sum = N*(N+1)//2 % MOD.
- Determine max digit length D = number of digits of N. For i from 1 to N, compute L[i] = floor(log10(i)) + 1. But we can compute counts c_d and sums S_d by iterating over ranges.
  For d=1: i=1..9, count = min(N,9) - 1 + 1? Actually 1 to min(N,9). So c_1 = min(N,9). S_1 = sum_{i=1}^{min(N,9)} i.
  For d=2: i=10..99, count = max(0, min(N,99) - 10 + 1). S_2 = sum_{i=10}^{min(N,99)} i.
  Similarly for d=3,4,5,6. For d=6: i=100000..N, count = max(0, N - 100000 + 1). S_6 = sum_{i=100000}^{N} i.
  We can compute these using arithmetic series formulas.

- Compute w_d = pow(10, d, MOD) for d=1..D.

- Compute polynomial G(t) = Π_{d=1}^D (1 + w_d t)^{c_d}.
  For each d, create array F_d of length c_d+1: F_d[k] = C(c_d, k) * w_d^k % MOD.
  We can compute C(c_d, k) using factorials: fact[c_d] * invfact[k] * invfact[c_d-k] % MOD.
  Then multiply all F_d using NTT. Since D <= 6, we can multiply sequentially: start with poly = [1], then for each d, poly = convolution(poly, F_d) truncated to degree N (since we only need up to N). But convolution of two polynomials of degree a and b gives degree a+b. We need to keep degree up to N. So after each multiplication, we can truncate the array to length N+1. However, NTT requires power-of-two size. We can do NTT on arrays of size next power of two >= len1+len2-1. Since total degree is N, we can allocate size = 1 << ceil_pow2(N+1). For each multiplication, we can zero-pad to that size and do NTT. But doing NTT for each multiplication (5 times) with size O(N) each is O(5 N log N). That's fine.

  Alternatively, we can compute E directly via DP using the fact that c_d are small? But NTT is straightforward.

- After obtaining E array of length N+1 (E[0]=1, E[1..N] coefficients).

- Compute A_m for m=0..N-1:
  For each d, compute pow_w_d[m] = w_d^m mod MOD for m=0..N. We can compute iteratively: pow_w_d[0]=1, pow_w_d[m+1] = pow_w_d[m] * w_d % MOD.
  Then A_m = Σ_{d=1}^D S_d * w_d * pow_w_d[m] % MOD.

- Compute B_m = (-1)^m * A_m % MOD. For m even, sign = 1; odd, sign = MOD-1.

- Compute convolution C = B * E. B length N, E length N+1. Result length up to 2N. We need C[0..N-1] for T_{k+1}. Actually T_k = C[k-1] for k>=1. So we can compute C array of length N+N+1 = 2N+1. We'll compute full convolution and take first N elements (indices 0..N-1) as T_{k+1} for k=1..N. But careful: T_k is defined for k=1..N. So we need C[0] = T_1, C[1] = T_2, ..., C[N-1] = T_N. So we can compute C = convolution(B, E) and then for k=1..N, T_k = C[k-1].

- Compute S_k = total_sum * E_k - T_k for k=0..N-1. Note T_0 = 0. For k=0, E_0=1, T_0=0, so S_0 = total_sum * 1 - 0 = total_sum. That matches: sum over x of x * e_0^{(x)} = sum x * 1 = total_sum.

- Compute invC(N-1, k) for k=0..N-1. Using precomputed factorials: invC = invfact[N-1] * fact[k] % MOD * fact[N-1-k] % MOD.

- Compute ans = fact[N-1] * Σ_{k=0}^{N-1} S_k * invC(N-1,k) % MOD.

But wait: we had total sum = (N-1)! * Σ_{k} S_k * invC(N-1,k). So ans = fact[N-1] * sum_{k} (S_k * invC(N-1,k)) % MOD.

We need to ensure that S_k is computed correctly. Let's verify with small N.

Test N=1: permutations: (1). f=1. Sum=1.
Our algorithm: N=1. c_1=1, S_1=1. w_1=10.
E: (1 + 10 t)^1 = 1 + 10 t. So E_0=1, E_1=10.
A_m: m=0..0: A_0 = S_1 * w_1 * (w_1)^0 = 1*10*1=10.
B_0 = (-1)^0 * 10 = 10.
Convolution B*E: B length 1, E length 2. C = [10*1, 10*10] = [10, 100]. So C[0]=10 = T_1.
S_0 = total_sum * E_0 - T_0 = 1*1 - 0 = 1.
S_1 = total_sum * E_1 - T_1 = 1*10 - 10 = 0.
invC(0,0) = invC(0,0) = 1? Actually N-1=0, k=0: invC(0,0) = 1.
Sum = S_0 * invC(0,0) + S_1 * invC(0,1) but k only 0..0. So sum = 1*1 = 1.
ans = fact[0] * 1 = 1. Correct.

Test N=2: permutations: (1,2): f=12; (2,1): f=21. Sum=33.
Our algorithm: N=2.
c_1: i=1..2, count=2, S_1=1+2=3.
c_2: none.
w_1=10.
E = (1+10t)^2 = 1 + 20t + 100t^2. So E_0=1, E_1=20, E_2=100.
A_m: m=0: A_0 = S_1 * w_1 * (w_1)^0 = 3*10=30.
m=1: A_1 = S_1 * w_1 * (w_1)^1 = 3*10*10=300.
B_0 = 30, B_1 = -300 mod MOD = MOD-300.
Convolution B*E: B length 2, E length 3.
C[0] = B0*E0 = 30*1=30 = T_1.
C[1] = B0*E1 + B1*E0 = 30*20 + (-300)*1 = 600 - 300 = 300 = T_2.
C[2] = B0*E2 + B1*E1 = 30*100 + (-300)*20 = 3000 - 6000 = -3000 mod MOD.
So T_1=30, T_2=300.
total_sum = 3.
S_0 = 3*1 - 0 = 3.
S_1 = 3*20 - 30 = 60 - 30 = 30.
S_2? k only 0..1 (N-1=1). So we need S_0 and S_1.
invC(1,0)=1, invC(1,1)=1.
Sum = S_0*1 + S_1*1 = 3+30=33.
ans = fact[1] * 33 = 1*33=33. Correct.

Test N=3: sample answer 1332.
Compute manually? Let's trust.

So algorithm seems correct.

Now we need to implement NTT. Since MOD=998244353, we can use standard NTT with primitive root 3. We'll need to compute bit-reversal, roots, etc.

We also need to compute factorials up to N. N up to 2e5, so fact array size N+1.

We need to compute binomial coefficients C(c_d, k) for k up to c_d. Since c_d can be up to 100001, we need factorials up to max(c_d) which is at most N. So we can precompute fact up to N.

Now steps in code:

1. Read N.
2. Precompute fact[0..N] and invfact[0..N].
3. Compute total_sum = N*(N+1)//2 % MOD.
4. Compute digit groups:
   Initialize arrays c = [0]*7, S = [0]*7.
   For d from 1 to 6:
       lo = 10**(d-1) (for d=1, lo=1)
       hi = min(N, 10**d - 1)
       if lo > hi: continue
       c[d] = hi - lo + 1
       S[d] = (lo + hi) * c[d] // 2 % MOD? Actually sum of arithmetic series: (lo+hi)*count//2. But we need modulo MOD. Since numbers are small (up to 2e5), we can compute exactly and then mod. But careful: sum can be up to ~2e10, fits in 64-bit. So compute as integer then mod.
   Actually we need S_d modulo MOD for later multiplication. But we also need S_d as integer for computing A_m? A_m uses S_d * w_d^{m+1}. Since w_d is mod MOD, we can take S_d mod MOD. So we can compute S_d mod MOD.
   So compute S_d = (lo+hi) * c[d] // 2 % MOD. But careful with division by 2: since MOD is odd, we can multiply by inv2. But since lo+hi and c[d] are integers, we can compute integer sum then mod. Actually (lo+hi)*c[d] is even? Not necessarily. But we can compute using integer arithmetic then take mod. Since numbers are small, we can compute sum as integer and then mod. For example, sum = (lo+hi)*c[d] // 2. But if we do integer division, we need to ensure it's exact. Since lo+hi and c[d] have same parity? Actually sum of arithmetic series: count * (first+last)/2. The product count*(first+last) is always even because either count is even or first+last is even. So integer division is safe. We can compute as integer then mod.
   So: s = (lo + hi) * c[d] // 2; S[d] = s % MOD.

5. Compute w_d = pow(10, d, MOD) for d=1..6.

6. Compute polynomial E:
   Initialize poly = [1] (length 1).
   For each d from 1 to 6:
       if c[d] == 0: continue.
       Build array F of length c[d]+1:
           F[k] = C(c[d], k) * pow(w_d, k, MOD) % MOD.
       Multiply poly and F using NTT, then truncate to length N+1 (i.e., keep first N+1 coefficients).
   After processing all d, poly is E array of length N+1.

   NTT implementation:
   We'll write a function ntt(a, invert) that performs in-place NTT.
   For multiplication: given two arrays a and b, compute convolution:
       n = 1
       while n < len(a) + len(b) - 1: n <<= 1
       pad a and b to length n with zeros.
       ntt(a, False); ntt(b, False)
       for i in range(n): a[i] = a[i] * b[i] % MOD
       ntt(a, True)
       result = a[:len(a)+len(b)-1]
   But we need to truncate to N+1. So after multiplication, we can take first min(N+1, len(result)) elements.

   Since we have 6 multiplications, we can do them sequentially. However, each multiplication requires resizing to next power of two. The total time is O(6 * N log N). With N=2e5, log N ~ 18, so about 6*2e5*18 ~ 2e7 operations, fine.

   But we need to be careful with memory: arrays of size up to next power of two of 2N, which is about 2^19 = 524288, fine.

7. Compute A_m for m=0..N-1:
   Precompute pow_w_d for each d: array pow_d of length N+1.
   For each d:
       pow_d[0] = 1
       for m in range(1, N+1): pow_d[m] = pow_d[m-1] * w_d % MOD
   Then for m in 0..N-1:
       A[m] = sum_{d} S[d] * w_d % MOD * pow_d[m] % MOD.
   Actually w_d * pow_d[m] = w_d^{m+1}. So we can compute term = S[d] * w_d % MOD * pow_d[m] % MOD.
   Since D <= 6, we can loop.

8. Compute B[m] = A[m] if m even else MOD - A[m].

9. Compute convolution C = B * E. B length N, E length N+1. Result length up to 2N. We need C[0..N-1] for T_{k+1}. So we can compute full convolution and take first N elements.

   NTT multiplication: similar to above.

10. Compute S_k for k=0..N-1:
    S[0] = total_sum * E[0] % MOD  (since T_0=0)
    For k=1..N-1:
        S[k] = (total_sum * E[k] - C[k-1]) % MOD
    Note: C[k-1] is T_k.

11. Compute invC(N-1, k) for k=0..N-1:
    invC[k] = invfact[N-1] * fact[k] % MOD * fact[N-1-k] % MOD

12. Compute sum_val = Σ_{k=0}^{N-1} S[k] * invC[k] % MOD.

13. ans = fact[N-1] * sum_val % MOD.

14. Print ans.

We need to ensure that all operations are modulo MOD.

Now we need to implement NTT. Let's write a standard NTT for MOD=998244353.

We need primitive root g=3. The maximum power of two for NTT is 2^23 = 8388608, which is > 2*2e5, so fine.

We'll implement ntt(a, invert):
- n = len(a)
- bit-reversal permutation
- for len = 2,4,8,...,n:
    wlen = pow(g, (MOD-1)//len, MOD) if not invert else pow(g, (MOD-1)//len, MOD) and then invert? Actually standard: wlen = pow(g, (MOD-1)//len, MOD). If invert, use inverse of wlen.
- for i from 0 to n step len:
    w = 1
    for j in 0..len/2-1:
        u = a[i+j]
        v = a[i+j+len/2] * w % MOD
        a[i+j] = (u+v) % MOD
        a[i+j+len/2] = (u-v) % MOD
        w = w * wlen % MOD
- if invert: multiply all a[i] by inv_n = pow(n, MOD-2, MOD).

We need to compute modular inverse of n.

Now, we need to be careful with the convolution: after ntt(a, False), ntt(b, False), multiply pointwise, then ntt(a, True). The result is in a.

Now, we need to handle large arrays. We'll use list of ints.

Potential issues: The polynomial (1 + w_d t)^{c_d} has coefficients C(c_d, k) * w_d^k. We can compute these using factorials. Since c_d can be up to 100001, we need factorials up to that. We already have fact up to N, so fine.

But we need to compute C(c_d, k) for all k from 0 to c_d. That's O(c_d) per d. Total O(N). That's fine.

Now, we need to compute pow(w_d, k) for k up to c_d. We can compute iteratively: pow_w = 1; for k in range(c_d+1): F[k] = C(c_d, k) * pow_w % MOD; pow_w = pow_w * w_d % MOD.

Now, we need to multiply polynomials. Since we have 6 polynomials, we can multiply them one by one. However, the degree of the product is sum c_d = N. So after each multiplication, the degree increases. We can truncate to N+1 to save time and memory. But NTT requires size to be power of two >= len1+len2-1. If we truncate, we might lose some coefficients that are needed for later multiplications? Actually we need the final polynomial E of degree N. If we truncate after each multiplication to degree N, we might lose contributions from higher degree terms that could later combine with lower degree terms from other factors to produce lower degree terms? No, because when multiplying polynomials, the degree of the product is sum of degrees. If we truncate to degree N, we are discarding terms of degree > N. But since the final degree is exactly N, and we are multiplying factors that sum to N, any term of degree > N in an intermediate product cannot be canceled by later factors (since all factors have non-negative coefficients). Actually, when multiplying (1 + w_d t)^{c_d}, the coefficients are positive. So if we truncate to degree N, we are safe because the final polynomial has degree N, and any term of degree > N in an intermediate product would correspond to selecting more than N elements total, which is impossible because total elements is N. So we can safely truncate to degree N after each multiplication. However, we must ensure that we don't lose terms that are exactly degree N? We keep up to N. So it's fine.

But careful: when we multiply poly (degree up to N) with F_d (degree c_d), the product degree is up to deg(poly)+c_d. Since deg(poly) is at most sum of previous c's, and c_d is the remaining, the total sum is N. So after multiplication, degree is exactly sum of c's so far. So we can truncate to min(N, current_degree+1). Actually we can just keep the full result up to N+1 length. Since the result length is len(poly)+len(F_d)-1. We can compute that and then take first N+1 elements. That's fine.

Now, we need to compute the convolution for T_k. B length N, E length N+1. Result length 2N. We need first N elements. We can compute full convolution and slice.

Now, we need to compute factorials up to N. We'll use list of size N+1.

Now, let's test with N=3 manually to verify.

N=3:
c_1: i=1..3, count=3, S_1=6.
c_2: none.
w_1=10.
E = (1+10t)^3 = 1 + 30t + 300t^2 + 1000t^3.
E_0=1, E_1=30, E_2=300, E_3=1000.
A_m: m=0: A0 = S1 * w1 * (w1)^0 = 6*10=60.
m=1: A1 = 6*10*10=600.
m=2: A2 = 6*10*100=6000.
B: B0=60, B1=-600, B2=6000.
Convolution B*E:
C0 = 60*1 = 60 = T1.
C1 = 60*30 + (-600)*1 = 1800 - 600 = 1200 = T2.
C2 = 60*300 + (-600)*30 + 6000*1 = 18000 - 18000 + 6000 = 6000 = T3.
C3 = 60*1000 + (-600)*300 + 6000*30 = 60000 - 180000 + 180000 = 60000.
So T1=60, T2=1200, T3=6000.
total_sum = 6.
S0 = 6*1 = 6.
S1 = 6*30 - 60 = 180 - 60 = 120.
S2 = 6*300 - 1200 = 1800 - 1200 = 600.
S3? k only 0..2 (N-1=2). So we need S0,S1,S2.
invC(2,0)=1, invC(2,1)=inv(2)= (MOD+1)//2? Actually C(2,1)=2, inv = 499122177. invC(2,2)=1.
Sum = S0*1 + S1*invC(2,1) + S2*1 = 6 + 120*inv2 + 600.
inv2 = (MOD+1)//2 = 499122177.
120 * 499122177 mod MOD = 120 * 499122177 = 59894661240 mod 998244353. Compute: 499122177 * 100 = 49912217700, *20 = 9982443540, sum = 59894661240. 998244353 * 60 = 59894661180. Difference = 60. So 120*inv2 = 60 mod MOD? Let's compute properly: inv2 = (MOD+1)//2 = 499122177. 120 * 499122177 = 120 * (499122177) = 59894661240. Now divide by MOD: 998244353 * 60 = 59894661180. Remainder = 60. So indeed 120*inv2 = 60. So sum = 6 + 60 + 600 = 666.
ans = fact[2] * 666 = 2 * 666 = 1332. Correct.

So algorithm works.

Now we need to implement NTT efficiently. We'll write a class or functions.

We also need to compute modular inverse of n for NTT inverse.

Now, we need to handle the case where N is small (e.g., N=1). The algorithm should work.

Now, we need to consider memory and time. N=2e5, NTT size up to 2^19=524288. Each multiplication does a few NTTs. Total time should be fine.

Now, we need to implement the convolution for E. Since we have 6 factors, we can multiply them sequentially. But we can also multiply all at once using divide and conquer, but sequential is fine.

Potential optimization: Since c_d for d>=2 are large, we can compute their polynomials using the binomial expansion. But we need to compute C(c_d, k) for all k. That's O(c_d) per d. Total O(N). That's fine.

Now, we need to compute pow(w_d, k) for k up to c_d. We can compute iteratively.

Now, we need to compute A_m. We have D up to 6. We can precompute pow_d[m] for each d. That's O(D*N) = O(6N) = 1.2e6, fine.

Now, we need to compute B and convolution. That's one NTT multiplication.

Now, we need to compute S_k and final sum. That's O(N).

Now, we need to ensure that we handle modulo correctly for negative numbers.

Now, let's write the code.

We'll structure as:

- MOD = 998244353
- inv2 = (MOD+1)//2

- Function ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    len_ = 2
    while len_ <= n:
        wlen = pow(ROOT, (MOD-1)//len_, MOD)
        if invert:
            wlen = pow(wlen, MOD-2, MOD)
        for i in range(0, n, len_):
            w = 1
            half = len_ // 2
            for j in range(i, i+half):
                u = a[j]
                v = a[j+half] * w % MOD
                a[j] = (u + v) % MOD
                a[j+half] = (u - v) % MOD
                w = w * wlen % MOD
        len_ <<= 1
    if invert:
        inv_n = pow(n, MOD-2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

- Function convolution(a, b):
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = a + [0]*(n - len(a))
    fb = b + [0]*(n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:len(a)+len(b)-1]

Now, in the main:

- Read N.
- Precompute fact and invfact.
- Compute total_sum.
- Compute c and S for d=1..6.
- Compute w_d.
- Compute E:
    poly = [1]
    for d in range(1, 7):
        if c[d] == 0: continue
        # build F_d
        F = [0]*(c[d]+1)
        pow_w = 1
        for k in range(c[d]+1):
            # C(c[d], k) = fact[c[d]] * invfact[k] * invfact[c[d]-k] % MOD
            F[k] = fact[c[d]] * invfact[k] % MOD * invfact[c[d]-k] % MOD * pow_w % MOD
            pow_w = pow_w * w_d % MOD
        # multiply poly and F
        poly = convolution(poly, F)
        # truncate to N+1
        if len(poly) > N+1:
            poly = poly[:N+1]
    E = poly + [0]*(N+1 - len(poly))  # ensure length N+1
    # Actually poly length should be N+1 after truncation? Since degree is N, length is N+1. But after last multiplication, length might be exactly N+1. We can pad to N+1.

- Compute A_m:
    A = [0]*N
    pow_d = [ [0]*(N+1) for _ in range(7) ]  # index d
    for d in range(1,7):
        if c[d]==0: continue
        pow_d[d][0] = 1
        for m in range(1, N+1):
            pow_d[d][m] = pow_d[d][m-1] * w_d % MOD
    for m in range(N):
        val = 0
        for d in range(1,7):
            if c[d]==0: continue
            # term = S[d] * w_d * pow_d[d][m] % MOD
            term = S[d] * w_d % MOD * pow_d[d][m] % MOD
            val = (val + term) % MOD
        A[m] = val

- Compute B:
    B = [0]*N
    for m in range(N):
        if m % 2 == 0:
            B[m] = A[m]
        else:
            B[m] = (MOD - A[m]) % MOD

- Compute convolution C = convolution(B, E). C length = N + (N+1) - 1 = 2N.
- Compute T_k = C[k-1] for k=1..N. We'll store T in array of length N+1, with T[0]=0.
    T = [0]*(N+1)
    for k in range(1, N+1):
        T[k] = C[k-1]

- Compute S_k:
    S = [0]*N
    for k in range(N):
        S[k] = (total_sum * E[k] - T[k]) % MOD

- Compute invC:
    invC = [0]*N
    inv_fact_N_1 = invfact[N-1]
    for k in range(N):
        invC[k] = inv_fact_N_1 * fact[k] % MOD * fact[N-1-k] % MOD

- Compute sum_val:
    sum_val = 0
    for k in range(N):
        sum_val = (sum_val + S[k] * invC[k]) % MOD

- ans = fact[N-1] * sum_val % MOD
- print(ans)

Now, we need to ensure that we handle N=1 correctly. For N=1, c_1=1, S_1=1. E = (1+10t)^1 = [1,10]. A_0 = 1*10*1=10. B_0=10. C = convolution([10], [1,10]) = [10,100]. T_1 = C[0]=10. S_0 = total_sum*E0 - T0 = 1*1 - 0 = 1. invC(0,0)=1. sum_val=1. ans=fact[0]*1=1. Good.

Now, we need to test with N=2 and N=3 as above.

Now, we need to consider the case where N is large, e.g., 2e5. The NTT size for E multiplication: we multiply poly (degree up to N) with F_d (degree c_d). The size needed is next power of two of len(poly)+len(F_d)-1. Since len(poly) grows, the maximum size is for the last multiplication when len(poly) is close to N and c_d is large. The sum of lengths is at most N+1 + c_d+1 -1 = N + c_d +1. Since c_d <= N, the maximum is 2N+1. So next power of two is at most 2^19 for N=2e5. That's fine.

Now, we need to implement the convolution function efficiently. We'll use the ntt function.

Now, we need to be careful with recursion depth? No recursion.

Now, we need to ensure that we compute factorials up to N. We'll use list of size N+1.

Now, we need to compute modular inverse of factorials. We can compute invfact[N] = pow(fact[N], MOD-2, MOD), then invfact[i-1] = invfact[i] * i % MOD for i from N down to 1.

Now, we need to compute the digit groups. We'll compute for d=1..6:

lo = 10**(d-1)
hi = min(N, 10**d - 1)
if lo <= hi:
    c[d] = hi - lo + 1
    s = (lo + hi) * c[d] // 2
    S[d] = s % MOD

But note: for d=1, lo=1, hi=min(N,9). For N<9, hi=N. So c_1 = N if N<=9. That's correct.

Now, we need to compute w_d = pow(10, d, MOD). Since d up to 6, we can compute directly.

Now, we need to compute pow_d[d][m] for m up to N. That's O(D*N). We can compute for each d separately.

Now, we need to compute A_m. We can compute in a loop.

Now, we need to compute B and convolution.

Now, we need to compute S_k and final sum.

Now, we should test with sample inputs.

Sample 1: N=3 -> output 1332.
Sample 2: N=390 -> output 727611652.
Sample 3: N=79223 -> output 184895744.

We can test with small N manually.

Now, we need to consider potential overflow in intermediate sums like (lo+hi)*c[d]. Since lo and hi are up to 2e5, product up to ~4e10, fits in Python int.

Now, we need to ensure that we use integer division // for sum of arithmetic series. Since (lo+hi)*c[d] is always even, integer division is safe.

Now, we need to ensure that we handle modulo correctly for negative numbers in S_k: (total_sum * E[k] - T[k]) % MOD. In Python, % MOD gives non-negative.

Now, we need to ensure that we compute T[k] correctly. T array length N+1, with T[0]=0, T[k]=C[k-1] for k>=1.

Now, we need to ensure that we compute E[k] for k up to N-1. E array length N+1, indices 0..N.

Now, we need to compute invC for k=0..N-1. inv_fact_N_1 = invfact[N-1]. For N=1, N-1=0, invfact[0]=1. fact[0]=1. So invC[0] = 1*1*1=1. Good.

Now, we need to compute ans = fact[N-1] * sum_val % MOD. For N=1, fact[0]=1.

Now, we need to consider the case where N is large and we have many multiplications. The NTT function might be called multiple times. We should ensure that we don't create too many large lists. But it's fine.

Now, we need to write the code in Python. We'll define ntt and convolution as nested functions or separate.

Now, we need to be careful with the NTT implementation: the primitive root for MOD=998244353 is 3. We need to compute wlen = pow(ROOT, (MOD-1)//len, MOD). For invert, we use inverse of wlen.

Now, we need to compute the bit-reversal permutation. We'll use the standard iterative method.

Now, we need to ensure that we handle the case when len(a) is not a power of two? In convolution, we pad to power of two.

Now, we need to test the NTT with small examples.

Now, let's write the code.

We'll also need to import sys for input.

Now, we need to consider that N can be up to 2e5, so we need to read input efficiently.

Now, we need to output the answer.

Now, we should also consider that the problem might have N=0? No, N>=1.

Now, we need to ensure that we handle the case where c_d=0 for some d. That's fine.

Now, we need to ensure that we compute the polynomial F_d correctly. For c_d=0, we skip.

Now, we need to ensure that we truncate poly after each multiplication to N+1. But if poly length is less than N+1, we don't need to truncate. But we can always take min(N+1, len(poly)).

Now, we need to ensure that after the last multiplication, poly has length exactly N+1. Since the sum of c_d is N, the degree of the product is N, so length is N+1. So we can assert that.

Now, we need to compute the convolution for T_k. B length N, E length N+1. The result length is 2N. We need C[0..N-1]. So we can compute full convolution and slice.

Now, we need to ensure that we don't run out of memory. The NTT arrays are of size up to 2^19, which is about 500k integers, fine.

Now, we need to consider that we are doing 6 multiplications for E, plus 1 for T_k. That's 7 NTT-based multiplications. Each multiplication involves 3 NTTs (forward for a, forward for b, inverse). So total 21 NTTs. Each NTT is O(n log n). With n up to 2^19, log n=19, so about 21 * 500k * 19 ~ 200 million operations? Actually each NTT does O(n log n) operations, each operation is modular multiplication and addition. 500k * 19 = 9.5 million per NTT. 21 NTTs = 200 million. That might be a bit slow in Python if not optimized. But we can optimize by using iterative loops and local variables. However, 200 million modular operations in Python might be borderline but should pass within time limit if optimized (using PyPy or CPython with fast I/O). We can try to reduce the number of NTTs by combining the multiplications for E using a divide-and-conquer approach? But that would still require similar number of NTTs. Alternatively, we can compute E using DP with the fact that there are only 6 groups. Since c_d are not huge, we can compute E via convolution using the fact that we can multiply the polynomials in a tree: multiply pairs, then multiply results. That would reduce the number of NTTs from 5 to 3 (since log2(6) ~ 3). But we still need to compute the polynomials for each group. Actually we have 6 polynomials. We can multiply them in a balanced binary tree: multiply F1 and F2, multiply F3 and F4, multiply F5 and F6, then multiply the three results. That's 3 multiplications instead of 5. But each multiplication still requires NTT. However, the sizes of the intermediate polynomials vary. The total work is similar. But we can do that to reduce constant factor.

But maybe we can compute E without NTT by using the fact that the weights are powers of 10 and we only need coefficients up to N. Since N=2e5, we can compute E using DP with O(N * number_of_groups) = O(6N) = 1.2e6, which is much faster than NTT. Wait, is that possible? Let's think: E_k = Σ_{k1+...+k6 = k} Π_{d} C(c_d, k_d) * (10^d)^{k_d}. This is a 6-dimensional convolution. We can compute it using dynamic programming: start with array E of length N+1 initialized to [1,0,...]. Then for each d, we update E by convolving with the sequence A_d where A_d[k] = C(c_d, k) * (10^d)^k. This is a 1D convolution. We can do this using O(N * c_d) per d, which is O(N^2) in worst case because c_d can be up to N. But we can use the fact that c_d is the count of elements with digit length d. For d=6, c_6 can be up to 100001. So O(N * c_6) = O(N^2) = 4e10, too slow.

But we can use the fact that A_d is a sequence of length c_d+1, and we are convolving with E which has length