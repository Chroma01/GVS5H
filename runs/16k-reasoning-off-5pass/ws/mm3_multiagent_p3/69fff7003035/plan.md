We need to compute sum over all permutations P of (1..N) of the integer formed by concatenating decimal representations of P_i. For each position i (1-indexed), the contribution of a value v placed there is v * 10^{total digits of all later elements}. Since each value appears equally often in each position (N-1)! times, we can compute:

Sum = (N-1)! * sum_{v=1..N} v * sum_{k=0..N-1} (10^{D_k}) where D_k is total digit count of the N-1 elements in the other positions.

But digit lengths vary per element. Better approach: For each element v, its contribution when placed at position i is v * 10^{sum of digit lengths of elements after it}. Since permutations are uniform, we can compute expected value of 10^{sum of digit lengths of remaining N-1 elements} and multiply by v * (N-1)!.

Let L(x) = number of digits of x. For each subset of size N-1, sum of L over that subset is total digits of that subset. The sum over all permutations of 10^{sum of L of suffix} can be computed by considering each element's contribution to the exponent.

Alternative: Process positions from right to left. Let total_digits = sum_{x=1..N} L(x). When we remove the rightmost element, the remaining total digits is total_digits - L(that element). So for each element v, the exponent when v is at position i is total_digits - (sum of L of elements after v). Over all permutations, each element v appears in each "position" (i.e., each rank from 1 to N) equally often. So the sum of 10^{exponent} over all permutations for a fixed v equals (N-1)! * sum_{k=0..N-1} 10^{total_digits - k} where k is the number of elements after v (0..N-1). Wait, that's not right because the elements after v have varying digit lengths, not just count.

We need to account for varying digit lengths. Let's think differently.

Consider building the concatenated number from left to right. For each element v, its contribution is v * 10^{sum of L of elements to its right}. Over all permutations, the distribution of "sum of L of elements to the right" depends on which elements are to the right.

We can compute the sum over all permutations of 10^{sum of L of suffix} by dynamic programming or combinatorial formula. Since N up to 2e5, we need O(N log N) or similar.

Observation: The digit lengths L(x) take only a few values: 1,2,3,4,5 (since N <= 2e5, max digits = 6? 2e5 has 6 digits). Actually 10^5 = 100000 (6 digits), 2e5 = 200000 (6 digits). So L(x) ∈ {1,2,3,4,5,6}.

Let cnt[d] = number of integers in 1..N with exactly d digits. Then total_digits = sum d * cnt[d].

For a permutation, the suffix sum of digit lengths is determined by which elements are in the suffix. We need sum over all permutations of 10^{suffix_digit_sum}.

We can compute this by considering the process of placing elements one by one from right to left. Let dp[k] = sum over all ways to choose an ordered sequence of k elements (from the remaining pool) of 10^{sum of their digit lengths}. But we need to weight by the number of permutations.

Actually, let's define: For a fixed set S of elements placed in the suffix (right part), the number of permutations where exactly S forms the suffix is (N - |S|)! * |S|! (choose and order the prefix, choose and order the suffix). But we need sum over all permutations of 10^{sum_{x in suffix} L(x)}.

We can compute: Sum_{permutations} 10^{suffix_sum} = sum_{S subset of {1..N}} (number of permutations where S is exactly the suffix) * 10^{sum_{x in S} L(x)}.

Number of permutations where S is exactly the suffix: Choose an ordering of S (|S|! ways) and an ordering of the complement ( (N-|S|)! ways). So total = |S|! * (N-|S|)!.

Thus Sum_{perm} 10^{suffix_sum} = sum_{k=0..N} (N-k)! * k! * (sum over subsets S of size k of 10^{sum_{x in S} L(x)}).

Now, sum over subsets of size k of 10^{sum L(x)} = coefficient of x^k in product_{i=1..N} (1 + 10^{L(i)} * x). Because each element either is in S (contributing factor 10^{L(i)} * x) or not (factor 1).

So we need to compute polynomial P(x) = prod_{i=1..N} (1 + 10^{L(i)} * x). Let P(x) = sum_{k=0..N} a_k x^k, where a_k = sum_{S, |S|=k} 10^{sum_{x in S} L(x)}.

Then Sum_{perm} 10^{suffix_sum} = sum_{k=0..N} (N-k)! * k! * a_k.

Then total answer = (N-1)! * sum_{v=1..N} v * (Sum_{perm} 10^{suffix_sum when v is at some position})? Wait, we need to be careful.

Actually, the total sum over permutations of f(P) = sum_{positions i} sum_{v} v * (number of permutations where v is at position i) * 10^{sum of L of elements after position i}.

Since each v appears at each position equally often: (N-1)! times at each position. So:

Total = (N-1)! * sum_{v=1..N} v * sum_{i=1..N} 10^{sum of L of elements after position i, averaged over permutations where v is at position i}.

But by symmetry, for a fixed v, the distribution of "sum of L of elements after v" over all permutations where v is at a specific position is the same as the distribution of "sum of L of a random subset of size i-1" where i is the position. However, since v is fixed, the remaining N-1 elements are a random permutation of the other N-1 elements. The suffix after v consists of some number of elements (0 to N-1) in some order, but the digit sum depends only on which elements are in the suffix, not their order.

So for fixed v, the sum over all permutations of 10^{suffix_sum} = sum_{S subset of {1..N}\{v}} (number of permutations where S is the suffix after v) * 10^{sum_{x in S} L(x)}.

Number of permutations where S is the suffix after v: v is fixed at some position. The elements before v can be any subset of size |before|, and the elements after v are S. The number of ways: choose an ordering of the prefix (size = N-1-|S|) and an ordering of S. So (N-1-|S|)! * |S|!.

Thus for fixed v: Sum_{perm with v} 10^{suffix_sum} = sum_{k=0..N-1} (N-1-k)! * k! * (sum over subsets S of size k from the other N-1 elements of 10^{sum L(x)}).

This is similar to before but with N-1 elements and excluding v. Since v is just one element, and L(v) varies, we need to compute this for each v. That would be O(N^2) if done naively.

But note: The sum over subsets of size k from the other N-1 elements of 10^{sum L(x)} = a_k^{(v)} where a_k^{(v)} is the coefficient in product_{i != v} (1 + 10^{L(i)} x).

We need sum_{v} v * sum_{k} (N-1-k)! k! a_k^{(v)}.

This seems expensive. However, we can use a different approach.

Alternative: Process the permutation from left to right. The contribution of element at position i is A_i * 10^{total_digits - sum_{j<=i} L(A_j)}. So:

Total = sum_{perm} sum_{i=1..N} A_i * 10^{total_digits - sum_{j<=i} L(A_j)}.

= sum_{perm} 10^{total_digits} * sum_{i=1..N} A_i * 10^{-sum_{j<=i} L(A_j)}.

But working with modular arithmetic and negative exponents is tricky. Instead, we can write:

Total = sum_{perm} sum_{i=1..N} A_i * 10^{sum_{j>i} L(A_j)}.

Now, consider the contribution of each element v. In a permutation, v appears at some position, and the exponent is sum of L of elements after it. Over all permutations, each element v appears in each "relative order" equally often.

We can compute the total sum by considering the process of building the permutation. Let's define:

Let total_digits = sum_{x=1..N} L(x).

For each permutation, f(P) = sum_{i=1..N} P_i * 10^{total_digits - sum_{j=1..i} L(P_j)}.

So Total = sum_{perm} sum_{i=1..N} P_i * 10^{total_digits - prefix_digit_sum_i}.

= 10^{total_digits} * sum_{perm} sum_{i=1..N} P_i * 10^{-prefix_digit_sum_i}.

But 10^{-x} mod p is the modular inverse of 10^x. Since p = 998244353, and 10 is invertible (gcd(10,p)=1), we can compute inv10 = 10^{-1} mod p, and 10^{-x} = inv10^x.

So Total = 10^{total_digits} * sum_{perm} sum_{i=1..N} P_i * inv10^{prefix_digit_sum_i}.

Now, sum_{perm} sum_{i=1..N} P_i * inv10^{prefix_digit_sum_i} = sum_{v=1..N} v * sum_{perm} [v is at position i] * inv10^{sum of L of elements before v}.

For fixed v, the elements before v form a random subset of the other N-1 elements, and their order matters for the prefix sum? Wait, prefix_digit_sum_i is sum of L of elements before position i. Since L depends only on the element, not its position, the sum of L of elements before v is just the sum of L of the set of elements that appear before v. The order doesn't matter for the sum.

So for fixed v, sum_{perm} inv10^{sum of L of elements before v} = sum_{S subset of others} (number of permutations where S is exactly the set before v) * inv10^{sum_{x in S} L(x)}.

Number of permutations where S is before v: v is at some position, S is the set before v (size k), and the complement (others \ S) is after v. The number of ways: choose ordering of S (k! ways), choose ordering of complement ((N-1-k)! ways). So total = k! * (N-1-k)!.

Thus for fixed v: sum_{perm} inv10^{sum L before v} = sum_{k=0..N-1} k! * (N-1-k)! * (sum over subsets S of size k from others of inv10^{sum L(x)}).

Let b_k^{(v)} = sum over subsets S of size k from {1..N}\{v} of inv10^{sum_{x in S} L(x)} = coefficient of x^k in product_{i != v} (1 + inv10^{L(i)} x).

Then contribution of v is v * sum_{k=0..N-1} k! (N-1-k)! b_k^{(v)}.

Total = 10^{total_digits} * sum_{v=1..N} v * sum_{k=0..N-1} k! (N-1-k)! b_k^{(v)}.

Now, we need to compute this efficiently. N up to 2e5, so we need O(N log N) or O(N sqrt N).

Observation: The product over all i of (1 + inv10^{L(i)} x) can be computed. Let Q(x) = prod_{i=1..N} (1 + inv10^{L(i)} x) = sum_{k=0..N} b_k x^k, where b_k = sum over subsets of size k of inv10^{sum L(x)}.

Then b_k^{(v)} = b_k * (1 + inv10^{L(v)} x) removed? Actually, product_{i != v} (1 + inv10^{L(i)} x) = Q(x) / (1 + inv10^{L(v)} x). But division of polynomials is not trivial.

However, we can write:

sum_{k} k! (N-1-k)! b_k^{(v)} = sum_{k} k! (N-1-k)! * [x^k] (Q(x) / (1 + inv10^{L(v)} x)).

We need sum_{v} v * this value.

This seems complicated. Let's think of another way.

Alternative approach: Use linearity and process elements one by one.

Consider the sum over all permutations of f(P). We can write:

Sum = sum_{perm} sum_{i=1..N} P_i * 10^{sum_{j>i} L(P_j)}.

Swap sums: Sum = sum_{i=1..N} sum_{perm} P_i * 10^{sum_{j>i} L(P_j)}.

For a fixed position i, the set of elements after position i is a random subset of size N-i of the remaining N-1 elements (excluding the one at position i). But the element at position i is also random.

Actually, we can compute the sum by considering the contribution of each element v when it is placed at position i. Since all permutations are equally likely, the probability that v is at position i is 1/N. The expected value of 10^{sum of L of elements after v} given that v is at position i is the same as the expected value of 10^{sum of L of a random subset of size N-i} from the other N-1 elements.

But the expected value over random subset of size k of 10^{sum L(x)} is (1/C(N-1,k)) * sum_{S, |S|=k} 10^{sum L(x)} = b_k / C(N-1,k), where b_k is the sum over subsets of size k of 10^{sum L(x)} from the N-1 elements (excluding v? Wait, this depends on v because the available elements are the other N-1. But if we consider the average over all v, maybe we can use symmetry.

Since the set of other elements is always the complement of {v}, and L(v) varies, the distribution of L of other elements depends on v. So we cannot simply average over v without accounting for L(v).

But we can compute the total sum as:

Total = sum_{v=1..N} v * (N-1)! * E_v, where E_v = expected value of 10^{sum of L of elements after v} over random permutations where v is at a uniformly random position? Actually, over all permutations, v appears at each position equally often. So the sum over permutations of 10^{suffix_sum after v} = (N-1)! * sum_{k=0..N-1} E[10^{sum L} | suffix size = k] * (number of permutations with suffix size k).

Wait, let's derive carefully.

For fixed v, consider all permutations of {1..N} where v appears. There are (N-1)! such permutations. In these permutations, v can be at any position from 1 to N. The number of permutations where v is at position i (so there are i-1 elements before and N-i after) is: choose which i-1 elements go before (C(N-1, i-1)), order them ((i-1)!), order the N-i after ((N-i)!). So count = C(N-1, i-1) * (i-1)! * (N-i)! = (N-1)!.

So indeed, for each position i, there are (N-1)! permutations with v at position i. Thus total permutations with v anywhere is N * (N-1)! = N!.

Now, for fixed v and fixed suffix size k = N-i (number of elements after v), the sum over permutations with v at position i of 10^{sum L of suffix} = (number of ways to choose and order prefix) * (number of ways to choose and order suffix) * 10^{sum L of suffix}.

Number of ways: choose subset S of size k from the other N-1 elements: C(N-1,k). Order S: k!. Order prefix (size N-1-k): (N-1-k)!. So count = C(N-1,k) * k! * (N-1-k)! = (N-1)!.

Thus for each k, there are (N-1)! permutations where v is at a position with exactly k elements after it. And the sum of 10^{sum L} over these permutations is (N-1)! * (average over subsets S of size k of 10^{sum L(x)}).

Therefore, sum over all permutations of 10^{suffix_sum after v} = sum_{k=0..N-1} (N-1)! * (N-1)! * (average over subsets of size k of 10^{sum L(x)} from the other N-1 elements).

Wait, careful: For each k, there are (N-1)! permutations with v at a position having k elements after. In each such permutation, the suffix is a specific ordered sequence of k elements. The sum of 10^{sum L} over these (N-1)! permutations is: sum over all ordered sequences of length k from the other N-1 elements of 10^{sum L}. This equals k! * (sum over subsets S of size k of 10^{sum L(x)}). Because for each subset S, there are k! orderings.

So sum over permutations with v at position with k after = k! * sum_{S, |S|=k} 10^{sum L(x)}.

Thus total sum over all permutations (with v anywhere) of 10^{suffix_sum} = sum_{k=0..N-1} k! * sum_{S, |S|=k} 10^{sum L(x)}.

Note: This does not depend on v! Because the set of other elements is always the complement of {v}, but the sum over subsets of size k of 10^{sum L(x)} depends on which elements are available. However, the available set is {1..N} \ {v}. So it does depend on v.

But wait, the sum over subsets S of size k from the other N-1 elements of 10^{sum L(x)} is exactly the coefficient a_k^{(v)} in the polynomial product_{i != v} (1 + 10^{L(i)} x).

So we need to compute for each v: sum_{k=0..N-1} k! * a_k^{(v)}.

Then total answer = sum_{v=1..N} v * sum_{k=0..N-1} k! * a_k^{(v)}.

But note: The factor (N-1)! is missing? Let's check.

We have: Total sum over permutations of f(P) = sum_{perm} sum_{i} P_i * 10^{suffix_sum_i}.

= sum_{v} v * (sum over permutations where v appears of 10^{suffix_sum after v}).

For fixed v, sum over permutations where v appears of 10^{suffix_sum} = sum_{k=0..N-1} (number of permutations with v at position having k after) * (average 10^{sum L} over those permutations).

Number of permutations with v at position having k after: choose which k elements are after (C(N-1,k)), order them (k!), order the prefix ((N-1-k)!). So count = C(N-1,k) * k! * (N-1-k)! = (N-1)!.

Average 10^{sum L} over those permutations: for a fixed set S of size k after v, there are k! orderings, each contributing 10^{sum_{x in S} L(x)}. So total contribution from all orderings of S is k! * 10^{sum L}. The average over the C(N-1,k) choices of S is (1/C(N-1,k)) * sum_{S} k! * 10^{sum L} = k! * (sum_{S} 10^{sum L}) / C(N-1,k).

Thus sum over permutations with v at position having k after = (N-1)! * k! * (sum_{S, |S|=k} 10^{sum L}) / C(N-1,k).

But C(N-1,k) = (N-1)! / (k! (N-1-k)!). So (N-1)! / C(N-1,k) = k! (N-1-k)!.

Thus sum over permutations with v at position having k after = k! (N-1-k)! * sum_{S, |S|=k} 10^{sum L}.

Therefore, total sum over permutations with v anywhere = sum_{k=0..N-1} k! (N-1-k)! * a_k^{(v)}, where a_k^{(v)} = sum_{S subset of others, |S|=k} 10^{sum L(x)}.

Then total answer = sum_{v=1..N} v * sum_{k=0..N-1} k! (N-1-k)! * a_k^{(v)}.

Now, we need to compute this efficiently.

Let P(x) = prod_{i=1..N} (1 + 10^{L(i)} x) = sum_{k=0..N} A_k x^k, where A_k = sum_{S, |S|=k} 10^{sum L(x)}.

Then a_k^{(v)} = coefficient of x^k in P(x) / (1 + 10^{L(v)} x).

We can write P(x) = (1 + 10^{L(v)} x) * Q_v(x), where Q_v(x) = prod_{i != v} (1 + 10^{L(i)} x) = sum_{k=0..N-1} a_k^{(v)} x^k.

So a_k^{(v)} = A_k - 10^{L(v)} * a_{k-1}^{(v)} (with a_{-1}=0). This recurrence allows us to compute a_k^{(v)} from A_k and a_{k-1}^{(v)}.

But we need sum_{k} k! (N-1-k)! a_k^{(v)} for each v. This is like evaluating a linear combination of a_k^{(v)} with weights w_k = k! (N-1-k)!.

We can compute for each v: S_v = sum_{k=0..N-1} w_k a_k^{(v)}.

Then answer = sum_{v} v * S_v.

Now, note that a_k^{(v)} depends on v only through L(v). So elements with the same digit length have the same a_k^{(v)} sequence. Thus we can group by digit length d.

Let cnt[d] = number of elements with L(x) = d. For each such element, a_k^{(v)} is the same. So we can compute S_d = sum_{k} w_k a_k^{(d)} where a_k^{(d)} corresponds to removing one element of digit length d.

Then answer = sum_{d} (sum_{v: L(v)=d} v) * S_d.

Now, how to compute a_k^{(d)} efficiently?

We have P(x) = prod_{i=1..N} (1 + 10^{L(i)} x). Let c_d = 10^d mod p.

Then P(x) = prod_{d=1..6} (1 + c_d x)^{cnt[d]}.

We can compute the coefficients A_k of P(x) up to k=N. N is up to 2e5, so we can compute the full polynomial in O(N log N) using NTT or divide and conquer. But we need a_k^{(d)} for each d, which is the coefficient sequence of P(x) / (1 + c_d x).

We can compute the polynomial division: Q_d(x) = P(x) * (1 - c_d x + c_d^2 x^2 - ...) but that's infinite. However, since P(x) has degree N, we can compute Q_d(x) = P(x) mod (1 + c_d x) ? Actually, division by (1 + c_d x) is easy: it's just a linear recurrence.

Given P(x) = sum A_k x^k, and we want Q(x) = P(x) / (1 + c x) where c = c_d.

Then (1 + c x) Q(x) = P(x). So Q_k + c Q_{k-1} = A_k, with Q_{-1}=0.

Thus Q_k = A_k - c Q_{k-1}.

So we can compute the sequence Q_k = a_k^{(d)} in O(N) for each d. Since there are only 6 possible d, total O(6N) = O(N). That's fine.

Then S_d = sum_{k=0..N-1} w_k Q_k, where w_k = k! (N-1-k)!.

We can precompute factorials and inverse factorials to get w_k mod p.

Then answer = sum_{d} (sum_{v: L(v)=d} v) * S_d mod p.

But wait: Is that correct? Let's verify with small N.

N=3. Elements: 1 (d=1), 2 (d=1), 3 (d=1). All have d=1. c_1 = 10.

P(x) = (1+10x)^3 = 1 + 30x + 300x^2 + 1000x^3.

A_0=1, A_1=30, A_2=300, A_3=1000.

For d=1, c=10. Q_k = A_k - 10 Q_{k-1}.

Q_0 = A_0 = 1.
Q_1 = A_1 - 10 Q_0 = 30 - 10 = 20.
Q_2 = A_2 - 10 Q_1 = 300 - 200 = 100.
Q_3 = A_3 - 10 Q_2 = 1000 - 1000 = 0. (degree N-1=2, so Q_3 should be 0, correct).

w_k = k! (2-k)! for k=0,1,2.
w_0 = 0! * 2! = 2.
w_1 = 1! * 1! = 1.
w_2 = 2! * 0! = 2.

S_1 = w_0 Q_0 + w_1 Q_1 + w_2 Q_2 = 2*1 + 1*20 + 2*100 = 2 + 20 + 200 = 222.

Sum of v for d=1: 1+2+3=6.

Answer = 6 * 222 = 1332. Matches sample.

Great!

So the algorithm is:

1. Compute L(x) for x=1..N. Count cnt[d] and sum_v[d] = sum of x with L(x)=d.
2. Compute c_d = 10^d mod p.
3. Compute polynomial P(x) = prod_{d} (1 + c_d x)^{cnt[d]}. We need coefficients A_k for k=0..N.
   - Since N is up to 2e5, we can compute this using NTT or by iterative multiplication. But note that cnt[d] can be large (up to N). We can compute the polynomial (1 + c x)^m efficiently using binomial theorem: coefficients are C(m, k) * c^k. But m = cnt[d] can be up to 2e5, and we need to multiply several such polynomials. The product of polynomials of degree up to N can be done with NTT in O(N log N). However, we have only 6 factors, each raised to a power. We can compute each (1 + c_d x)^{cnt[d]} using binomial coefficients, then multiply them together. The degree of each is cnt[d]. The total degree is N. Multiplying 6 polynomials of total degree N using NTT is O(N log N). That's fine.

   Alternatively, we can compute P(x) by dynamic programming: start with [1], then for each element i, multiply by (1 + 10^{L(i)} x). That's O(N^2) if done naively. But we can do it in O(N log N) using divide and conquer or NTT. Since N=2e5, O(N^2) is too slow. So we need NTT.

   However, note that the factors are of the form (1 + c x). We can compute the product using a segment tree or divide and conquer with NTT. Standard approach: build a binary tree, multiply leaves, combine. Complexity O(N log N).

   But we also need to compute Q_d(x) = P(x) / (1 + c_d x) for each d. We can compute P(x) first, then for each d, compute Q_d(x) using the recurrence Q_k = A_k - c_d Q_{k-1}. That's O(N) per d, total O(6N).

   Then compute S_d = sum_{k=0..N-1} w_k Q_k^{(d)}.

   Then answer = sum_d sum_v[d] * S_d mod p.

4. Precompute factorials fact[i] for i=0..N, and invfact[i] for i=0..N-1? Actually w_k = k! * (N-1-k)!. We need (N-1-k)! which is fact[N-1-k]. So we need fact up to N.

   Compute w_k = fact[k] * fact[N-1-k] % p.

5. Compute S_d = sum_{k=0}^{N-1} w_k * Q_k^{(d)} % p.

6. Answer = sum_{d=1..6} sum_v[d] * S_d % p.

But wait: We need to ensure that the polynomial P(x) is computed modulo p = 998244353, which is NTT-friendly. We can use NTT for multiplication.

However, we have to be careful: The coefficients of P(x) can be large, but we work modulo p.

Implementation steps:

- Read N.
- Compute L(x) for x=1..N. Since N <= 2e5, we can compute digit length by converting to string or using thresholds: d=1 for 1-9, d=2 for 10-99, d=3 for 100-999, d=4 for 1000-9999, d=5 for 10000-99999, d=6 for 100000-200000.
- Compute cnt[d] and sum_v[d] (sum of x with that digit length).
- Compute c_d = pow(10, d, p).
- Compute polynomial P(x) = prod_{d} (1 + c_d x)^{cnt[d]}.
  - For each d, compute the polynomial (1 + c_d x)^{cnt[d]} using binomial coefficients: coefficient of x^k is C(cnt[d], k) * c_d^k.
  - Since cnt[d] can be up to N, we need to compute binomial coefficients C(cnt[d], k) for k=0..cnt[d]. We can precompute factorials up to N and use fact[cnt[d]] * invfact[k] * invfact[cnt[d]-k].
  - Then multiply these 6 polynomials together using NTT. The total degree is N.
  - Alternatively, we can compute P(x) by iterating over all elements: start with poly = [1], for each element i, multiply poly by (1 + 10^{L(i)} x). That's N multiplications of degree up to N, which is O(N^2). Too slow.
  - So we need to group by digit length and use the binomial expansion, then multiply the resulting polynomials.

  Since there are only 6 digit lengths, we can compute the polynomial for each d as a vector of length cnt[d]+1. Then multiply them together. The product of polynomials of degrees d1, d2, ..., d6 (sum = N) can be done in O(N log N) using divide-and-conquer NTT.

  However, note that if cnt[d] is large, the polynomial (1 + c_d x)^{cnt[d]} has degree cnt[d]. Multiplying them one by one using NTT would be O(N log N) per multiplication, total O(6 N log N) which is fine. But we can also do divide and conquer.

  Simpler: Since there are only 6 polynomials, we can multiply them sequentially using NTT. Each multiplication takes O(N log N). Total O(6 N log N) = O(N log N). That's acceptable for N=2e5.

  But we need to implement NTT. Since p = 998244353 is a prime with primitive root, we can use standard NTT.

  However, we need to be careful with the size: the degree of P(x) is N. The convolution size will be up to N+1. We can use NTT with size being power of two >= N+1.

  Steps for each multiplication:
    - Take two polynomials A and B.
    - Compute convolution C = A * B using NTT.
    - Truncate C to degree N (since we only need up to x^N).
    - Replace A with C.

  Since we have 6 polynomials, we do 5 multiplications.

  But wait: The polynomial (1 + c_d x)^{cnt[d]} has degree cnt[d]. When we multiply them, the degree grows. We can truncate to N at each step to keep size manageable.

  Actually, we need the full polynomial up to degree N. So we can truncate after each multiplication.

  Complexity: O(6 * N log N) which is fine.

- After obtaining P(x) as vector A of length N+1 (A[k] = coefficient of x^k).
- For each d from 1 to 6:
    - Compute Q_d(x) = P(x) / (1 + c_d x). Since we only need Q_d for k=0..N-1, we can compute:
        Q_d[0] = A[0]
        for k=1..N-1:
            Q_d[k] = (A[k] - c_d * Q_d[k-1]) % p
    - Note: Q_d[N] should be 0, but we don't need it.
    - Compute S_d = sum_{k=0}^{N-1} fact[k] * fact[N-1-k] % p * Q_d[k] % p.
- Answer = sum_{d=1..6} sum_v[d] * S_d % p.

But wait: Is the formula correct? Let's double-check the derivation.

We had: Total = sum_{v} v * sum_{k=0}^{N-1} k! (N-1-k)! * a_k^{(v)}.

Where a_k^{(v)} = sum_{S subset of others, |S|=k} 10^{sum L(x)}.

We defined Q_d(x) = sum_{k=0}^{N-1} a_k^{(v)} x^k for any v with L(v)=d.

Then S_d = sum_{k} w_k Q_d[k].

Then answer = sum_d (sum_{v: L(v)=d} v) * S_d.

Yes.

Now, we need to compute Q_d(x) from P(x). Since P(x) = (1 + c_d x) Q_d(x), we have the recurrence.

But note: P(x) includes the factor for v. So Q_d(x) is exactly the polynomial for the other N-1 elements. So the recurrence is correct.

One more check: For N=1. There is only one permutation: (1). f(1) = 1. Sum = 1.

Our formula: N=1. Elements: 1 (d=1). cnt[1]=1, sum_v[1]=1.

P(x) = (1 + 10x)^1 = 1 + 10x. A_0=1, A_1=10.

For d=1: Q_0 = A_0 = 1. Q_1 = A_1 - 10 Q_0 = 10 - 10 = 0. (degree N-1=0, so Q_1 is not used).

w_k for k=0..N-1=0: w_0 = 0! * (0)! = 1.

S_1 = w_0 * Q_0 = 1*1 = 1.

Answer = sum_v[1] * S_1 = 1*1 = 1. Correct.

For N=2. Elements: 1 (d=1), 2 (d=1). Permutations: (1,2) -> 12, (2,1) -> 21. Sum = 33.

Our formula: cnt[1]=2, sum_v[1]=3.

P(x) = (1+10x)^2 = 1 + 20x + 100x^2. A_0=1, A_1=20, A_2=100.

For d=1: Q_0 = 1. Q_1 = 20 - 10*1 = 10. (Q_2 = 100 - 10*10 = 0, not needed).

w_0 = 0! * 1! = 1.
w_1 = 1! * 0! = 1.

S_1 = 1*1 + 1*10 = 11.

Answer = 3 * 11 = 33. Correct.

Great.

Now, we need to implement NTT for polynomial multiplication.

Since N <= 2e5, the final polynomial size is N+1 <= 200001. The next power of two is 262144. NTT with that size is fast.

We need to multiply up to 6 polynomials. We can do it sequentially.

However, we need to compute the initial polynomials (1 + c_d x)^{cnt[d]}. For each d, we need to compute the coefficients: C(cnt[d], k) * c_d^k for k=0..cnt[d]. We can precompute factorials up to N to get binomial coefficients quickly.

But note: cnt[d] can be up to N. So we need factorials up to N.

Implementation plan:

1. Read N.
2. Compute digit lengths for 1..N. Use thresholds:
   - d=1: 1-9
   - d=2: 10-99
   - d=3: 100-999
   - d=4: 1000-9999
   - d=5: 10000-99999
   - d=6: 100000-200000
   We can compute L(x) by checking x < 10, < 100, etc.
3. Initialize cnt[1..6] = 0, sum_v[1..6] = 0.
   For x in 1..N:
     d = digit length of x.
     cnt[d] += 1
     sum_v[d] += x
4. Precompute factorials fact[0..N] and inv_fact[0..N] modulo p.
   Also precompute pow10[d] = 10^d mod p for d=1..6.
5. For each d from 1 to 6:
   - If cnt[d] == 0, skip (polynomial is 1).
   - Compute poly_d[k] = C(cnt[d], k) * pow10[d]^k mod p for k=0..cnt[d].
   - This is a vector of length cnt[d]+1.
6. Multiply all non-empty poly_d together using NTT to get P(x).
   - Start with result = [1].
   - For each d with cnt[d] > 0:
       result = multiply(result, poly_d) truncated to degree N.
   - After multiplication, result has length up to N+1.
7. Now result is A[k] for k=0..N.
8. For each d from 1 to 6:
   - If cnt[d] == 0, then S_d = 0? Actually, if there are no elements with digit length d, we don't need to compute S_d. But we need to compute for d that appear.
   - Compute Q array of length N (or N+1, but we only need up to N-1).
     Q[0] = A[0]
     for k=1..N-1:
        Q[k] = (A[k] - pow10[d] * Q[k-1]) % p
   - Compute S_d = sum_{k=0}^{N-1} fact[k] * fact[N-1-k] % p * Q[k] % p.
   - Add sum_v[d] * S_d to answer.
9. Print answer mod p.

Potential issues:
- The polynomial multiplication: we need to truncate to degree N to avoid unnecessary computation. But when multiplying, the degree can exceed N. We can truncate after each multiplication.
- NTT implementation: need to handle modulo 998244353. Primitive root is 3.
- Factorials: need up to N. N up to 2e5, so fact array size N+1 is fine.
- pow10[d]: compute as pow(10, d, p).

Let's verify with sample 2: N=390. We can't compute manually, but trust the logic.

Edge cases: N=1, N=2, large N.

Complexity:
- Computing digit lengths: O(N).
- Computing factorials: O(N).
- Computing poly_d: O(N) total (since sum of cnt[d] = N).
- Polynomial multiplication: O(6 * N log N) = O(N log N).
- Computing Q and S_d: O(6N).
Total O(N log N).

Now, we need to implement NTT.

We can write a standard NTT implementation.

Alternatively, we can avoid NTT by using the fact that the polynomials are of the form (1 + c x)^m. We can compute P(x) by dynamic programming using the fact that we only need the coefficients, and we can use the recurrence:

P(x) = prod_{d} (1 + c_d x)^{cnt[d]}.

We can compute the coefficients A_k by iterating over d and using the binomial theorem, then convolving. But convolution is needed.

Another approach: Since the factors are simple, we can compute P(x) by starting with [1] and for each element i, multiply by (1 + 10^{L(i)} x). That's N multiplications of degree up to N. If we do each multiplication in O(N), total O(N^2). Too slow.

So NTT is needed.

We can implement a simple NTT class.

Let's write the code.

We'll need:
- mod = 998244353
- primitive root g = 3
- ntt function: takes vector a, invert flag.
- multiply function: takes two vectors, returns convolution truncated to length N+1.

But we need to be careful with the size: the convolution size should be power of two >= len(a) + len(b) - 1.

We can implement multiply(a, b, max_deg):
  - Compute convolution c = a * b.
  - Truncate c to length max_deg+1.

Since we only need up to degree N, we can set max_deg = N.

Now, let's code.

We'll precompute factorials and inverse factorials using Fermat's little theorem.

Compute pow10[d] = pow(10, d, mod).

Now, let's test with N=3.

N=3:
cnt[1]=3, sum_v[1]=6.
pow10[1]=10.
poly_1: C(3,k)*10^k: k=0:1, k=1:3*10=30, k=2:3*100=300, k=3:1*1000=1000.
Multiply: only one poly, so P = poly_1.
A = [1,30,300,1000].
For d=1:
Q[0]=1
Q[1]=30-10*1=20
Q[2]=300-10*20=100
Q[3]=1000-10*100=0 (not used)
w: fact[0]*fact[2]=1*2=2, fact[1]*fact[1]=1*1=1, fact[2]*fact[0]=2*1=2.
S = 2*1 + 1*20 + 2*100 = 222.
Answer = 6*222 = 1332. OK.

Now, for N=390, we trust.

One more check: The formula uses fact[N-1-k]. For k=N-1, fact[0]=1. For k=0, fact[N-1]. So we need fact up to N-1. We have fact up to N, so fine.

Now, we need to ensure that the polynomial multiplication is correct modulo p.

Potential overflow: use Python's big integers, but we take mod at each step.

Now, let's write the code.

We'll structure as:

def ntt(a, invert):
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
    length = 2
    while length <= n:
        wlen = pow(g, (mod-1)//length, mod)
        if invert:
            wlen = pow(wlen, mod-2, mod)
        for i in range(0, n, length):
            w = 1
            for j in range(i, i+length//2):
                u = a[j]
                v = a[j+length//2] * w % mod
                a[j] = (u + v) % mod
                a[j+length//2] = (u - v) % mod
                w = w * wlen % mod
        length <<= 1
    if invert:
        inv_n = pow(n, mod-2, mod)
        for i in range(n):
            a[i] = a[i] * inv_n % mod

def multiply(a, b, max_deg):
    # compute convolution of a and b, truncate to max_deg+1
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = a + [0]*(n - len(a))
    fb = b + [0]*(n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % mod
    ntt(fa, True)