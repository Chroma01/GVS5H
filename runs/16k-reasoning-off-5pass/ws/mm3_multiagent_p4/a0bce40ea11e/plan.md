We need to compute S = Σ_{B ∈ choices} B^p (mod p) where each zero entry of A can be any of the p-1 nonzero values mod p. Since p is prime, we can exploit Fermat's little theorem and properties of matrix powers modulo p.

Key idea: Over a field of characteristic p, the map B → B^p is the Frobenius endomorphism, which is linear over the subfield F_p (scalars). That is, (B^p) = (B_{ij}^p) where each entry is raised to the p-th power. By Fermat, for any x ∈ F_p, x^p = x. So for entries that are nonzero, B^p = B entrywise. For zeros, x^p = 0.

Thus the sum reduces to: For each entry (i,j), sum over all B of (B_{ij})^p. Since (B_{ij})^p = B_{ij} if A_{ij} ≠ 0, and 0 if A_{ij}=0. So we only need to sum B_{ij} over all B.

But B_{ij} varies over all possible nonzero values (1..p-1) for each zero in A, and is fixed for nonzero entries. Since choices are independent across zero positions, the total sum factorizes.

Let K = number of zeros. For each zero position, the value runs over {1,...,p-1}, sum = p(p-1)/2 ≡ 0 (mod p) because p | p(p-1)/2. Actually p(p-1)/2 mod p = 0. So the sum over a zero entry is 0. For a fixed entry, it equals the product of sums for each zero (if the entry is zero, then that zero contributes sum_{v} v = p(p-1)/2 ≡ 0; if entry is fixed, it contributes that value times product of sums for other zeros, also 0). Wait, need to be careful.

If the entry (i,j) is zero: B_{ij} ranges over 1..p-1, while other zeros range independently. Sum = (Σ_{v=1}^{p-1} v) * (product over other zeros of Σ_{v=1}^{p-1} 1) * ... Actually for each other zero, the entry doesn't depend on it, so sum factorizes: total sum = (Σ_{v} v) * (p-1)^{K-1} = (p(p-1)/2) * (p-1)^{K-1}. Mod p, p(p-1)/2 ≡ 0, so result is 0.

If the entry (i,j) is fixed to a (a≠0): then B_{ij}=a always. Sum over all B = a * (p-1)^K (since each zero can be any of p-1 values, independent of B_{ij}). Mod p, a*(p-1)^K ≡ a * ((-1)^K) mod p (since p-1 ≡ -1). So result is a * (-1)^K mod p.

Thus answer matrix C where:
- C_{ij} = 0 if A_{ij} = 0
- C_{ij} = A_{ij} * (-1)^K mod p (where K = number of zeros in A)

We just need to compute K, then for each nonzero entry multiply by (-1)^K mod p, output.

Let's test with sample 1: N=2, p=3, A = [[0,1],[0,2]]. Zeros: K=2. (-1)^2 = 1. So nonzero entries: (1)→1*1=1, (2)→2*1=2. Output:
0 1
0 2
But sample output is:
0 2
1 2
Wait mismatch. Let's re-examine.

Sample 1: p=3, A = [[0,1],[0,2]]. According to our formula, C = [[0,1*1=1],[0,2*1=2]] = [[0,1],[0,2]]. But sample output is [[0,2],[1,2]].

Something is off. Let's recompute manually. The sample enumerated all B and summed B^3 (mod 3). Let's compute using our linear Frobenius argument.

We said B^p = B entrywise mod p because x^p = x for all x in F_p. However, this is only true if B is a matrix with entries in F_p, and we compute B^p as matrix multiplication, then take each entry to the p-th power? Wait, the Frobenius endomorphism (raising each entry to p) is not equal to matrix power unless the matrix is over a commutative ring? Actually for matrices over a field of characteristic p, (B^p)_{ij} = Σ_{k1,...,k_{p-1}} B_{i,k1} B_{k1,k2} ... B_{k_{p-1},j}. This is not equal to (B_{ij})^p in general. The Frobenius endomorphism is the map that raises each entry to p, but matrix multiplication does not commute with entrywise power.

Wait, the statement: Over a field of characteristic p, the map φ: M → M^p (matrix power) is not linear. However, there is a known trick: For any matrix M over F_p, M^p ≡ M (mod p) if M commutes with something? No.

Actually there's a known result: For any integer matrix M, M^p ≡ M (mod p) if M is a matrix over integers? No, that's false. For example, M = [[1,1],[0,1]], p=2, M^2 = [[1,0? wait compute: [[1,1],[0,1]]^2 = [[1,2],[0,1]] = [[1,0],[0,1]] mod 2 = I, but M ≠ I. So M^p ≠ M mod p in general.

But we have the sum over all B of B^p. Perhaps we can use the fact that p is prime and the sum over all nonzero values in each zero position leads to simplifications using combinatorial identities (e.g., sum of powers, multinomial sums).

Let's think more carefully.

We need to compute S_{ij} = Σ_{B} (B^p)_{ij} mod p.

We can think of (B^p)_{ij} as sum over all walks of length p from i to j in the directed graph defined by B (weighted). Specifically, (B^p)_{ij} = Σ_{i1,...,i_{p-1}} B_{i,i1} B_{i1,i2} ... B_{i_{p-1},j}. This is a sum of products of p entries of B.

Thus S_{ij} is a polynomial in the entries of B (the variable entries are the zeros). We need to sum this polynomial over all assignments of nonzero values to zero positions.

Because p is prime, we can use the fact that for any integer m, Σ_{x=1}^{p-1} x^m mod p is:
- 0 if (p-1) ∤ m
- -1 if (p-1) | m (by standard result using primitive root or FLT).

Specifically, Σ_{x∈F_p^*} x^m = 0 if p-1 ∤ m, and = -1 mod p if p-1 | m (since sum of all (p-1)th roots of unity is 0? Actually sum_{x≠0} x^m = Σ_{x=1}^{p-1} x^m. If p-1 | m, then x^m = 1 for all x≠0, sum = p-1 ≡ -1 mod p. If p-1 ∤ m, sum = 0.

This is a crucial fact.

Now, (B^p)_{ij} is a homogeneous polynomial of degree p in the entries of B. When we expand and sum over all assignments, we get a sum of monomials. Each monomial is a product of p entries (with possible repetitions) from B. Since B entries are either fixed (nonzero) or variables (zeros). Summation over each variable ranges over 1..p-1. The sum over all variables factorizes: total sum = product over variables of (Σ_{v=1}^{p-1} v^{e_v}), where e_v is the exponent of that variable in the monomial.

Thus the total contribution of a monomial is nonzero mod p only if for each variable, the exponent of that variable is a multiple of p-1 (i.e., e_v ≡ 0 mod (p-1)). If any variable's exponent is not divisible by p-1, the sum over that variable is 0, making the whole monomial 0.

But note: The monomial has total degree p (since it's a product of p entries). However, we have K variables (zero positions). The exponents e_v for each variable are nonnegative integers summing to p. The condition for nonzero contribution is that each e_v is divisible by p-1. Since p-1 > p for p>2? Let's check: p-1 >= p? No, p-1 < p for p>=2. The only way a sum of nonnegative integers equals p and each is a multiple of (p-1) is if one variable has exponent p-(p-1)=1? Wait, multiples of p-1 are 0, p-1, 2(p-1), ... Since total sum is p, and p-1 > p/2 for p>2, the only possibilities are:
- One variable has exponent p-1 and another has exponent 1? But 1 is not a multiple of p-1 unless p-1=1 (p=2). For p>2, p-1 >=2, so multiples are 0, p-1, 2(p-1)>=2(p-1) > p for p>2. So the only way to have sum p with each e_v a multiple of p-1 is if one variable has exponent p-1 and the rest have exponent 0? That sums to p-1, not p. So impossible.

Wait, maybe we need to consider that the sum over each variable is Σ_{v=1}^{p-1} v^{e_v}, which is 0 unless (p-1) | e_v, in which case it's -1 mod p. So for a monomial to have nonzero sum, each variable's exponent must be a multiple of p-1. Since total degree is p, and each exponent is a multiple of p-1, the only way is that some variables have exponent p-1 and the rest 0, but sum would be (p-1)*k = p => k = p/(p-1) which is not integer for p>2. So no monomial can satisfy the condition for p>2? But sample 1 has p=3 and we got a nonzero answer. Let's examine.

For p=3, p-1=2. Total degree p=3. Multiples of 2 are 0,2,4,... To sum to 3 using multiples of 2: possible? 2+1 (no), 0+0+3 (3 not multiple of 2). So indeed no monomial has all exponents divisible by 2. Then according to this reasoning, all monomials sum to 0, giving total sum 0. But sample 1 is nonzero. So my reasoning is flawed.

Let's re-evaluate: The sum over each variable v is Σ_{x=1}^{p-1} x^{e}. The result is:
- 0 if (p-1) ∤ e
- -1 if (p-1) | e (i.e., e ≡ 0 mod p-1)

But wait, is that true for e=0? Σ_{x=1}^{p-1} x^0 = p-1 ≡ -1 mod p. So yes, e=0 is considered multiple of p-1 (0 mod p-1). So exponent 0 also gives -1.

Thus for a monomial to survive, each variable's exponent must be either 0 or a positive multiple of p-1. Since total degree is p, we need to partition p into a sum of numbers each of which is either 0 or a multiple of p-1. The only positive multiple of p-1 ≤ p is p-1 itself (for p>2). So we can have at most one variable with exponent p-1, and the rest 0. That gives total degree p-1, not p. So impossible for p>2. So how can we get nonzero sum for p=3?

Let's test with a simple case: N=1, p=3, A=[0]. Then K=1. B can be 1 or 2. Sum of B^3 = 1^3 + 2^3 = 1+8=9 ≡ 0 mod 3. Output 0. That matches our formula (zero entry => 0). So for N=1, sum is 0. In sample 1, there are two zeros, and we have nonzero sum. Let's see: B^3 for 2x2 matrix. Let's compute sum directly using the expansion.

We can think of (B^3)_{ij} as sum over all words of length 3 (i->i1->i2->j) of product of three entries. The sum over all B of this is sum over all assignments of the product. The product is a monomial of degree 3. For each variable (zero entry), the exponent is the number of times that position appears in the word.

For a fixed word (i,i1,i2,j), the monomial involves entries B_{i,i1}, B_{i1,i2}, B_{i2,j}. The exponents for each variable (zero position) is the number of times that position is used in this word. For each assignment of B, we sum the product.

We need to sum over all B. The sum factorizes: for each variable position, we have Σ_{v=1}^{p-1} v^{e_v}, where e_v is the number of times that position appears across all words? Wait, careful: The sum is over all B, which means for each word, we compute the product (which depends on B), then sum over B. This is equivalent to summing over all B of Σ_{words} monomial. Interchanging sum: Σ_{words} Σ_{B} monomial. For a given word, the monomial is a product of variables (some may be repeated). Summing over B means summing over each variable independently: Σ_{B} Π_{variables} v^{e_v} = Π_{variables} (Σ_{v=1}^{p-1} v^{e_v}). So for each word, the contribution is product over variables of S(e_v), where S(e) = Σ_{v=1}^{p-1} v^e mod p.

Thus the total sum S_{ij} = Σ_{words of length p from i to j} Π_{variables} S(e_v(word)), where e_v(word) is the count of variable v in the word.

Now, S(e) = 0 if (p-1) ∤ e, and = -1 if (p-1) | e. So for a word to contribute, each variable's count in the word must be a multiple of p-1.

For p=3, p-1=2. So each variable must appear 0 or 2 or 4... times in the word. Since word length is 3, the only way is to have one variable appear 2 times and another variable appear 1 time? No, 1 is not multiple of 2. So it seems impossible. But we know sample 1 has nonzero sum. Let's compute a specific case manually to see where the sum is nonzero.

Sample 1: p=3, A = [[0,1],[0,2]]. Variables: position (1,1) and (2,1). Fixed entries: (1,2)=1, (2,2)=2.

We sum over B1 ∈ {1,2}, B2 ∈ {1,2} (B1 = B_{1,1}, B2 = B_{2,1}).

Compute B matrix:
[ B1, 1 ]
[ B2, 2 ]

Compute B^3.

Let's compute B^2 first: B^2 = B * B.
Row1: [B1,1] * B = [B1*B1 + 1*B2, B1*1 + 1*2] = [B1^2 + B2, B1 + 2]
Row2: [B2,2] * B = [B2*B1 + 2*B2, B2*1 + 2*2] = [B1*B2 + 2B2, B2 + 4] = [B2(B1+2), B2+4]

Simplify mod 3: 4 ≡ 1.
So B^2 = [[B1^2 + B2, B1 + 2], [B2(B1+2), B2+1]]

Now B^3 = B^2 * B.
Compute (1,1): [B1^2+B2, B1+2] * [B1; B2] (col1) = (B1^2+B2)*B1 + (B1+2)*B2 = B1^3 + B1*B2 + B1*B2 + 2*B2 = B1^3 + 2*B1*B2 + 2*B2.
Wait: (B1+2)*B2 = B1*B2 + 2*B2. So sum = B1^3 + B2*B1 + B1*B2 + 2*B2 = B1^3 + 2*B1*B2 + 2*B2.

Similarly (1,2): [B1^2+B2, B1+2] * [1;2] = (B1^2+B2)*1 + (B1+2)*2 = B1^2 + B2 + 2*B1 + 4 = B1^2 + B2 + 2*B1 + 1.

(2,1): [B2(B1+2), B2+1] * [B1; B2] = B2(B1+2)*B1 + (B2+1)*B2 = B1*B2*(B1+2) + B2^2 + B2 = B1^2*B2 + 2*B1*B2 + B2^2 + B2.

(2,2): [B2(B1+2), B2+1] * [1;2] = B2(B1+2)*1 + (B2+1)*2 = B2*B1 + 2*B2 + 2*B2 + 2 = B1*B2 + 4*B2 + 2 = B1*B2 + B2 + 2 (since 4≡1, wait 4*B2 = (3+1)*B2 = B2, so 4*B2 ≡ B2. So 2*B2 + 2*B2 = 4*B2 ≡ B2. So total: B1*B2 + B2 + 2.

Now sum over B1, B2 ∈ {1,2}. Let's compute sums of monomials. Since p=3, we can compute mod 3.

First, note that B1, B2 take values 1,2 each. Sum over both: Σ_{B1=1,2} Σ_{B2=1,2} f(B1,B2).

We can compute S_{11} = Σ (B1^3 + 2*B1*B2 + 2*B2) mod 3.
Compute Σ B1^3: For B1=1, 1^3=1; B1=2, 8≡2 (mod 3). Sum = 1+2=3 ≡0. For each B2, multiply by 2 (since B2 doesn't affect B1^3 term). Actually term is B1^3 * 1 (no B2). So sum_{B1,B2} B1^3 = (Σ_{B1} B1^3) * (Σ_{B2} 1) = 0 * 2 = 0.

Term 2*B1*B2: Sum = 2 * (Σ B1) * (Σ B2) = 2 * (1+2) * (1+2) = 2 * 3 * 3 = 2*9=18 ≡ 0 mod 3.

Term 2*B2: Sum = 2 * (Σ_{B1} 1) * (Σ_{B2} B2) = 2 * 2 * (1+2) = 2*2*3 = 12 ≡ 0.

So S_{11} = 0. That matches sample output (0 at (1,1)).

Now S_{12} = Σ (B1^2 + B2 + 2*B1 + 1) mod 3.
Compute Σ B1^2: B1=1 =>1, B1=2=>4≡1. Sum = 2. Times Σ_{B2} 1 = 2 => total 2*2=4≡1.
Σ B2: Σ_{B1}1 * Σ B2 = 2*3=6≡0.
Σ 2*B1: 2* Σ B1 * Σ 1 = 2*3*2 = 12≡0.
Σ 1: (p-1)^K = 2^2=4≡1.
Total S_{12} = 1 + 0 + 0 + 1 = 2 mod 3. Sample output (1,2) is 2. Good.

S_{21} = Σ (B1^2*B2 + 2*B1*B2 + B2^2 + B2).
Term B1^2*B2: Σ B1^2 * Σ B2 = (1+1)*(1+2) = 2*3=6≡0.
2*B1*B2: 2*3*3=18≡0.
B2^2: Σ 1 * Σ B2^2 = 2*2=4≡1.
B2: Σ 1 * Σ B2 = 2*3=6≡0.
Total = 1. Sample output (2,1) is 1. Good.

S_{22} = Σ (B1*B2 + B2 + 2) = Σ B1*B2 + Σ B2 + Σ 2.
Σ B1*B2 = 3*3=9≡0.
Σ B2 = 2*3=6≡0.
Σ 2 = 2 * 2 * 2 = 8 ≡ 2 (since 8 mod 3 = 2). Actually Σ over B1,B2 of constant 2: 2 * (number of terms) = 2 * 4 = 8 ≡ 2.
Total = 2. Sample output (2,2) is 2. Good.

So our factorization method works. Let's apply the rule: S(e) = Σ_{v=1}^{p-1} v^e mod p.
- If e = 0: S(0) = p-1 ≡ -1 mod p.
- If e > 0 and (p-1) | e: S(e) = p-1 ≡ -1.
- Else: S(e) = 0.

Thus a monomial contributes (-1)^{#variables with exponent>0} times product of something? Wait, for each variable, the factor is S(e_v). If e_v > 0 and (p-1) ∤ e_v, factor is 0, killing the monomial. If e_v = 0, factor is -1. If e_v > 0 and (p-1) | e_v, factor is -1 as well. So any monomial where for all variables either exponent 0 or a positive multiple of p-1 contributes (-1)^{#variables involved} (i.e., number of variables with exponent > 0). But note: if a variable has exponent 0, factor is -1. So each variable contributes factor -1 regardless of whether its exponent is 0 or a positive multiple of p-1. However, if exponent is a positive multiple of p-1, factor is also -1. So effectively, for each variable, the factor is -1 if the exponent is either 0 or a multiple of p-1; otherwise 0.

Thus the total sum S_{ij} = Σ_{words} [ (-1)^{#variables with exponent not divisible by p-1? Wait no: if any variable has exponent not divisible by p-1 and not zero, the factor is 0. So only words where every variable's exponent is either 0 or a positive multiple of p-1 survive. For each surviving word, the product of factors is (-1)^{K} (since each variable contributes -1). Actually careful: For a word, we have K variables total. For each variable, the factor is:
- If exponent e_v = 0: factor = -1.
- If e_v > 0 and (p-1) | e_v: factor = -1.
- Else: factor = 0.

Thus for a word to survive, for each variable, either e_v = 0 or e_v is a positive multiple of p-1. In either case, the factor is -1. So the product over all variables is (-1)^K. So each surviving word contributes (-1)^K.

Therefore, S_{ij} = (-1)^K * (number of words of length p from i to j such that for each variable (zero position), the number of times it appears in the word is either 0 or a positive multiple of p-1).

Now, we need to count the number of such words. Since K can be up to N^2 (10000), and p can be up to 1e9, we cannot enumerate words.

But note: p-1 is large (up to 1e9-1). The condition that e_v is a positive multiple of p-1 means e_v >= p-1. Since total length of word is p, and p-1 is close to p, the only possible positive multiple of p-1 ≤ p is p-1 itself (for p>2). For p=2, p-1=1, so any exponent works? Let's handle p=2 separately.

Case 1: p=2.
Then p-1=1. Condition: each variable's exponent is either 0 or a multiple of 1, i.e., any nonnegative integer. So all words survive! For p=2, S(e) = Σ_{v=1}^{1} v^e = 1^e = 1 for all e (since only v=1). Actually p-1=1, so the set of nonzero values is just {1}. So B is uniquely determined? Wait, p=2, values are 0 and 1. Nonzero values are only 1. So B is uniquely determined: all zeros become 1. So there is exactly one B. Then B^2 is computed. So sum is just B^2. But our formula: K = number of zeros. (-1)^K = (-1)^K mod 2. Since p=2, we work mod 2. Number of words of length 2 from i to j: that's (B^2)_{ij} where B is that unique matrix. So we need to compute B^2 mod 2.

Our derived formula says S_{ij} = (-1)^K * (number of valid words). For p=2, all words are valid, so number of words = (B^2)_{ij} (with B being the unique matrix). But B is the matrix where zeros are replaced by 1. So we need to compute B^2 mod 2. However, the expression "(-1)^K * (number of words)" is modulo 2. Since p=2, (-1) ≡ 1 mod 2. So S_{ij} = number of words mod 2 = (B^2)_{ij} mod 2. So we just need to compute B^2 mod 2 for the unique B.

But wait, is that correct? Let's test sample 2: p=2, N=3, A has zeros on off-diagonal, ones on diagonal. So B is all ones matrix (since zeros become 1). B^2 = 3*J? Actually all-ones matrix J of size 3. J^2 = 3J. Mod 2, 3≡1, so J^2 ≡ J. So B^2 is all ones. Sample output is all ones. Yes.

So for p=2, answer is simply B^2 mod 2 where B is A with zeros replaced by 1. That's easy to compute: just set zeros to 1, then square mod 2. N ≤ 100, O(N^3) is fine.

Case 2: p > 2 (odd prime).
Then p-1 ≥ 2. For a word of length p, the exponent e_v for a variable is the number of times that variable's position is used in the word. Since total length is p, and p-1 is the smallest positive multiple, the only way to have e_v > 0 and e_v divisible by p-1 is e_v = p-1. But sum of all e_v over variables used in the word is p (since the word has p entries). If one variable has e_v = p-1, then the sum of the rest must be 1. But 1 is not divisible by p-1 (unless p-1=1, i.e., p=2). So we cannot have any variable with exponent p-1 because the remaining sum 1 cannot be expressed as sum of numbers each either 0 or multiple of p-1 (since p-1 > 1). Therefore, for p>2, there are no variables with positive exponent divisible by p-1. Thus the only way for a word to survive is that for every variable, e_v = 0. That means the word uses no variable entries at all; i.e., all entries used in the word are fixed (nonzero) entries of A.

Thus, for p>2, the sum S_{ij} = (-1)^K * (number of words of length p from i to j using only fixed entries of A).

But wait, is that correct? Let's test with sample 1: p=3, K=2. (-1)^2 = 1. Number of words of length 3 from i to j using only fixed entries. The fixed entries are (1,2)=1 and (2,2)=2. Let's see the graph of fixed entries: edges: 1->2 (weight 1), 2->2 (weight 2). The adjacency matrix for fixed entries is:
[0, 1]
[0, 2]
This is a directed graph. We need to count walks of length 3 from i to j using only these edges. Compute (M^3)_{ij} where M is the fixed-entry matrix (with zeros where A is zero). Let's compute M^3.

M = [[0,1],[0,2]].
M^2: row1: [0*0+1*0, 0*1+1*2] = [0,2]; row2: [0*0+2*0, 0*1+2*2] = [0,4] = [0,1] mod 3? 4≡1.
So M^2 = [[0,2],[0,1]].
M^3 = M^2 * M:
(1,1): [0,2]*[0;0] = 0.
(1,2): [0,2]*[1;2] = 0*1 + 2*2 = 4 ≡ 1.
(2,1): [0,1]*[0;0] = 0.
(2,2): [0,1]*[1;2] = 0*1 + 1*2 = 2.
So M^3 = [[0,1],[0,2]].
Then S = (-1)^K * M^3 = 1 * M^3 = [[0,1],[0,2]]? But sample output is [[0,2],[1,2]]. Wait, we got (1,2)=1 but sample says 2. Mismatch.

Our computed M^3 gives (1,2)=1, but sample says 2. Let's recompute manually using our earlier expansion: we found S_{12}=2, S_{21}=1, S_{22}=2. The matrix M^3 we computed is [[0,1],[0,2]] which is not the answer. So something is off.

Wait, we said S_{ij} = (-1)^K * (number of words using only fixed entries). But number of words is (M^p)_{ij} where M is the matrix of fixed entries. However, the product of fixed entries along a word contributes a factor (the product of the entries). In our sum, for a word using only fixed entries, the monomial is just the product of those fixed entries (which are numbers). When we sum over all B, the fixed entries are constant, and the variables (zero positions) are not used, so the factor for each variable is Σ_{v=1}^{p-1} v^0 = p-1 ≡ -1. So the total contribution of such a word is (product of fixed entries) * (-1)^K.

Thus S_{ij} = (-1)^K * Σ_{words using only fixed entries} (product of fixed entries along the word). This is exactly (-1)^K * (M^p)_{ij}, where M is the matrix of fixed entries (i.e., A with zeros replaced by 0? Wait, fixed entries are the nonzero entries of A. The zero entries are replaced by variables. In the sum, for a word that avoids all zero positions, the monomial is just the product of the nonzero entries traversed. So we can define a matrix M where M_{ij} = A_{ij} if A_{ij} ≠ 0, and M_{ij} = 0 if A_{ij} = 0. Then (M^p)_{ij} is the sum over walks of length p of the product of entries. So S_{ij} = (-1)^K * (M^p)_{ij} mod p.

Let's test with sample 1: K=2, (-1)^2 = 1. M = [[0,1],[0,2]]. Compute M^3. We computed M^3 = [[0,1],[0,2]] earlier? Let's recompute carefully.

M = [[0, 1], [0, 2]].
M^2 = M * M.
(1,1): 0*0 + 1*0 = 0.
(1,2): 0*1 + 1*2 = 2.
(2,1): 0*0 + 2*0 = 0.
(2,2): 0*1 + 2*2 = 4 ≡ 1 mod 3.
So M^2 = [[0,2],[0,1]].

M^3 = M^2 * M.
(1,1): [0,2] dot [0,0] = 0*0 + 2*0 = 0.
(1,2): [0,2] dot [1,2] = 0*1 + 2*2 = 4 ≡ 1.
(2,1): [0,1] dot [0,0] = 0.
(2,2): [0,1] dot [1,2] = 0*1 + 1*2 = 2.
So M^3 = [[0,1],[0,2]].

Thus S = 1 * M^3 = [[0,1],[0,2]]. But sample output is [[0,2],[1,2]]. Still mismatch.

Wait, we have (1,2)=1 vs 2, (2,1)=0 vs 1. So we are missing some contributions.

Our earlier manual expansion gave S_{12}=2, S_{21}=1, S_{22}=2. So the answer is not simply M^3.

Let's examine the words of length 3. There are walks of length 3. Some walks may use variable entries (zeros). In our earlier analysis, we said for p=3, a variable's exponent must be 0 or 2. Since total length is 3, we cannot have a variable with exponent 2 because the remaining length 1 cannot be assigned to any variable with exponent 0 or 2 (since 1 is not allowed). However, we have two variables: (1,1) and (2,1). Could a word use both variables? For example, a word might use (1,1) twice and (2,1) once. Exponents: e_{(1,1)} = 2, e_{(2,1)} = 1. Then for variable (1,1), exponent 2 is multiple of 2 (p-1=2), so factor S(2) = -1. For variable (2,1), exponent 1 is not multiple of 2, so factor S(1) = 0. Thus overall factor 0. So that word contributes 0.

What about a word using only (1,1) three times? Exponent 3, not multiple of 2, factor 0.

What about a word using (1,1) twice and (2,1) zero times? Then total length is 2, not 3. So not possible.

Thus according to the condition, any word that uses any variable must have that variable's exponent be a multiple of 2. Since total length is 3, the only way is to have one variable with exponent 2 and the rest 0, but that gives length 2, not 3. So no word with variables should survive. Yet we have nonzero answer. So our condition is insufficient.

Wait, we forgot that the sum over a variable is Σ_{v=1}^{p-1} v^e. For p=3, p-1=2. The sum S(e) = Σ_{v=1}^{2} v^e.
Compute:
e=0: 1+1=2 ≡ -1.
e=1: 1+2=3 ≡ 0.
e=2: 1+4=5 ≡ 2 ≡ -1.
e=3: 1+8=9 ≡ 0.
e=4: 1+16=17 ≡ 2 ≡ -1.
So pattern: S(e) = -1 if e even, 0 if e odd.

Thus for p=3, the condition is: e_v must be even (including 0) to get factor -1; if e_v is odd, factor 0.

So a word survives if for every variable, its exponent in the word is even. Since total length is 3 (odd), the sum of exponents over all variables is the number of variable positions used in the word. The total length of the word is p = 3. Let x be the number of variable positions used (i.e., total count of variable entries in the word). The remaining p - x entries are fixed entries. The exponents of variables are nonnegative integers summing to x. We need each exponent to be even. So x must be even (sum of even numbers is even). But p=3 is odd, so x must be even and ≤ 3. Possible x = 0 or 2. x=0: word uses no variables, i.e., all fixed entries. x=2: word uses exactly two variable entries (could be same variable twice or two different variables each once? Wait, if two different variables each once, exponents are 1 and 1, both odd -> not allowed. If one variable twice and another zero times, that's one variable with exponent 2 (even) and the other 0 (even). That works. So x=2 is possible: one variable appears twice, the other variable not at all. Then the word has length 3: two entries are that variable, one entry is a fixed entry. So the word uses exactly one variable twice.

Thus for p=3, surviving words are those that use no variables, or use exactly one variable twice (and the third entry is fixed). The factor for the variable with exponent 2 is S(2) = -1. The other variable has exponent 0, factor S(0) = -1. So total factor = (-1)*(-1) = 1 = (-1)^K? K=2, (-1)^2=1. Yes. So each such word contributes 1 times the product of the fixed entry and the variable's value squared? Wait, careful: The product of entries in the word includes the variable entry twice. So the monomial is (variable)^2 * (fixed entry). When summing over B, the variable runs over {1,2}, and Σ_{v} v^2 = 2 ≡ -1. So the contribution of the variable part is -1. The fixed entry is constant. So the word contributes (-1) * (fixed entry). But we also have the other variable's factor: S(0) = -1. So total factor = (-1) * (-1) = 1. So the word contributes (fixed entry) * 1. That is, the variable is "integrated out" and leaves a factor of -1, but the other variable also contributes -1, canceling.

Wait, we need to be precise. For a word w, let V be the set of variables used, with multiplicities. The monomial is Π_{v∈V} v^{e_v} * Π_{fixed edges} (fixed value). Summing over B gives (Π_{v} S(e_v)) * (Π_{fixed} value). For p=3, S(e) = -1 if e even, 0 if e odd. So for the word to survive, all e_v must be even. Then S(e_v) = -1. So product over v of S(e_v) = (-1)^{|V|}? Actually each variable in V contributes -1, and variables not in V have e_v=0, also contribute -1. Wait, variables not in V have exponent 0, so S(0) = -1 as well. So the product over all K variables is (-1)^K, regardless of which variables are used. So the factor is constant (-1)^K. Then the contribution of the word is (-1)^K * (product of fixed entries in the word). This is independent of the variable values; the variable choices have been summed out, leaving a constant factor.

Thus the total sum S_{ij} = (-1)^K * Σ_{words w of length p from i to j} (product of fixed entries along w), where the sum is over all words (including those that use variables) but only those words where each variable's exponent is even contribute. However, we just argued that the factor is always (-1)^K for any word that satisfies the parity condition, and 0 otherwise. So S_{ij} = (-1)^K * Σ_{words satisfying parity condition} (product of fixed entries along w).

But earlier we thought only words with no variables survive. That was wrong because we considered the condition "exponent is multiple of p-1", but for p=3, p-1=2, so multiple of 2 means even. And a word can have one variable with exponent 2 and the rest 0, which is allowed. So the condition is: for each variable, e_v is a multiple of (p-1). Since p-1=2, e_v must be even. So the word can have some variables with exponent 2, 4, etc. Since total length p=3, the only possible positive multiple of 2 is 2. So we can have at most one variable with exponent 2 (since 2+2=4>3). And the rest 0. So the word uses exactly one variable twice, and the third entry is fixed. So the word consists of two edges that are the same variable position, and one fixed edge.

Thus the sum can be computed by considering all words of length p, and for each word, we need to check if the multiset of variable positions used has each multiplicity divisible by p-1. Since p-1 is large (close to p), the possibilities are limited.

Generalizing: For prime p, the condition for a word to contribute is: for each variable v, the number of times v appears in the word is a multiple of (p-1). Let d_v = e_v / (p-1). Then d_v are nonnegative integers, and Σ_v d_v * (p-1) = number of variable entries in the word = x. But the total word length is p, so x ≤ p. Also x = Σ_v e_v. Since each e_v is a multiple of p-1, we have e_v = (p-1) * d_v, with d_v ≥ 0 integer. The sum Σ e_v = (p-1) * Σ d_v = x. So x must be a multiple of p-1. Since x ≤ p, the only possible values are x = 0 or x = p-1 (if p-1 ≤ p, which is true for p≥2). x=0 means no variables used. x=p-1 means exactly p-1 variable entries are used, and 1 fixed entry is used (since total length p). In the x=p-1 case, the p-1 variable entries are distributed among variables, each variable's count is a multiple of p-1. Since total variable count is p-1, the only way is that exactly one variable has count p-1 and all others have count 0. So the word uses exactly one variable position, and uses it p-1 times. The remaining one step is a fixed entry.

Thus, for any prime p, the surviving words are:
1. Words that use only fixed entries (no variables). Contribution: product of fixed entries.
2. Words that use exactly one variable position v, and use it p-1 times, and one fixed entry. Contribution: product of fixed entries in the word (the variable is summed out, contributing factor S(p-1) = p-1 ≡ -1 for the used variable, and S(0) = -1 for all other variables, total (-1)^K). Wait, we need to include the factor for the used variable: S(p-1) = Σ_{v=1}^{p-1} v^{p-1} = p-1 ≡ -1 mod p. And for each of the other K-1 variables, S(0) = p-1 ≡ -1. So product of S(e_v) over all variables is (-1)^K. So the factor is (-1)^K. The monomial includes the variable raised to p-1, but the sum over variable gives -1, and the product of fixed entries is constant. So the contribution of such a word is (-1)^K * (product of fixed entries in the word).

Thus, in both cases, the contribution of a surviving word is (-1)^K times the product of the fixed entries traversed.

Therefore, the total sum S_{ij} = (-1)^K * (sum over all words w of length p from i to j of the product of fixed entries along w), where the sum is over all words (including those that use variables) but only the two types of words above survive. However, we can unify: For any word w, define its "weight" as the product of fixed entries. But words that don't satisfy the condition contribute 0. So we need to count, for each i,j, the sum of weights of words of length p that either use no variables, or use exactly one variable p-1 times and one fixed entry.

This seems complicated to compute directly, but maybe there's a matrix formulation.

Let F be the matrix of fixed entries: F_{ij} = A_{ij} if A_{ij} ≠ 0, else 0.
Let Z be the indicator matrix of zero positions: Z_{ij} = 1 if A_{ij} = 0, else 0.
We have K = sum Z_{ij}.

We need to compute S = (-1)^K * T, where T_{ij} = sum over words w of length p of weight(w), with weight(w) = product of F_{ab} for each step (a,b) in w, but only for words w that either have no Z-positions, or have exactly one Z-position appearing p-1 times and the remaining one step being a fixed position.

But note: If a word uses a Z-position, that position contributes 0 to the product of F because F_{ij}=0 there. However, the weight of the word is defined as product of fixed entries; if the word uses a Z-position, that step is not a fixed entry, so it contributes 1 to the product? Wait, careful: In the monomial for a word, the entries are B_{ab}. If (a,b) is a zero position, B_{ab} is a variable. The product of fixed entries along the word means we take the product over steps that are fixed positions. Steps that are variable positions are not fixed, so they are not included in that product. In the contribution after summing over variables, the variable positions are replaced by their sum factor (-1). So the weight contributed to T is simply the product of F_{ab} for the fixed steps in the word. For a word with no variables, weight = product of F along the path. For a word with one variable used p-1 times, weight = product of F at the one fixed step. For a word with variables used in other ways, weight is irrelevant because contribution is 0.

Thus T_{ij} = sum_{w: i->...->j, length p, w valid} (product of F on fixed steps of w).

We can think of this as: The set of valid words consists of:
- Type 0: All steps are fixed. Weight = product of F along the path.
- Type 1: Exactly one step is fixed, and the other p-1 steps are the same variable position (a,b). The weight is just F at the fixed step.

But wait: In Type 1, the variable position is used p-1 times. The steps are a sequence of p steps. The positions of the steps are: p-1 of them are (a,b) (the same), and one of them is a fixed step (c,d). The product of fixed entries is F_{c,d} (since only that step is fixed). The variable (a,b) is used p-1 times, so it doesn't contribute to the product of fixed entries.

Thus T_{ij} can be expressed as:
T = (F^p)_{ij} + sum over all zero positions (a,b) of [ contribution from words where (a,b) is the variable used p-1 times ].

But careful: In Type 0, the word is a walk of length p in the graph of fixed edges. (F^p)_{ij} is the sum over all walks of length p of the product of F along the walk. That's exactly Type 0.

In Type 1, we have a word where one step is fixed, say at position t (1-indexed) in the sequence of p steps, and the other p-1 steps are at a specific zero position (a,b). The walk must be consistent: the sequence of vertices must match. That is, we have a walk i = v0 -> v1 -> ... -> vp = j. The step at time t is (v_{t-1}, v_t) which is a fixed edge (so F_{v_{t-1},v_t} ≠ 0). The other p-1 steps are all the same edge (a,b) = (v_{s-1}, v_s) for all s ≠ t. That means for all s ≠ t, v_{s-1} = a and v_s = b. This imposes strong constraints on the walk.

Specifically, for s ≠ t, we have v_{s-1} = a and v_s = b. So for consecutive s, say s and s+1 (both ≠ t), we have v_{s-1}=a, v_s=b, and v_s=a? Wait, if step s is (a,b), then v_{s-1}=a, v_s=b. If step s+1 is also (a,b), then v_s must equal a (since the start of step s+1 is v_s). But we have v_s = b from step s. So we need b = a. Thus for two consecutive steps to be the same edge (a,b), we need a = b. But zero positions can be any (i,j), possibly with i=j. If a ≠ b, then you cannot have two consecutive steps of the same edge (a,b) because the end of one step must equal the start of the next. So the p-1 steps of the variable must be arranged in the walk such that the vertices match.

Let's analyze the structure of a walk where p-1 steps are the same edge (a,b). The walk has p steps. Let's denote the steps as e_1, e_2, ..., e_p. Suppose the variable steps are at positions S ⊂ {1,...,p} with |S| = p-1. Let t be the index of the fixed step. For each step s in S, we have (v_{s-1}, v_s) = (a,b). For the walk to be valid, we need v_s = v_{s+1} for consecutive steps? Actually, the walk is defined by vertices v_0, v_1, ..., v_p. The step s is (v_{s-1}, v_s). If step s and step s+1 are both in S, then v_s is the end of step s and the start of step s+1. So we have v_s = b (from step s) and v_s = a (from step s+1). Thus a = b. So if a ≠ b, we cannot have two consecutive variable steps. Therefore, the p-1 variable steps must be non-consecutive in the sequence. But there are p steps total, and p-1 of them are variable. The only way to have p-1 non-consecutive indices in a sequence of length p is that they occupy all positions except one, and the missing position is the fixed step. However, are they non-consecutive? Let's see: If the fixed step is at position t, then the variable steps are at all other positions. For any two consecutive positions s and s+1 both ≠ t, they are both variable. So we have consecutive variable steps unless t is at one of the ends? Wait, if t=1, then variable steps are at 2,3,...,p. Then steps 2 and 3 are consecutive variable steps. So we would have v_2 = b and v_2 = a, requiring a=b. So if a≠b, we cannot have two consecutive variable steps. Thus to avoid consecutive variable steps, the fixed step must be placed such that no two variable steps are adjacent. But with p-1 variable steps and 1 fixed step, the fixed step can separate the variable steps at most into two blocks. The maximum number of non-consecutive indices in a sequence of length p with one fixed index is: if fixed index is in the middle, we have a block of length L on left and R on right, with L+R = p-1. The variable steps are consecutive within each block. So there will be consecutive variable steps unless one of the blocks has length 0 or 1? Actually, if a block has length ≥2, then there are consecutive variable steps. The only way to avoid any consecutive variable steps is if each block of variable steps has length at most 1. But total variable steps is p-1. The only way to have p-1 steps partitioned into blocks of size ≤1 is impossible for p-1 > 2. For p=3, p-1=2. The fixed step at position 2: variable steps at 1 and 3, which are not consecutive. That works: steps 1 and 3 are variable, step 2 is fixed. For p=5, p-1=4. If fixed step is at position 3, variable steps at 1,2,4,5. Steps 1-2 are consecutive variable steps, requiring a=b. So unless a=b, this fails.

Thus, for p>3, it's impossible to have p-1 variable steps without consecutive ones, unless a=b (self-loop). But a can be any zero position. For a≠b, the only possible words of Type 1 are those where the variable steps are not consecutive, which is only possible if p-1 ≤ 2, i.e., p ≤ 3. For p=2, p-1=1, so one variable step, no consecutiveness issue. For p=3, p-1=2, we can have variable steps at positions 1 and 3, with fixed step at 2. For p>3, p-1 ≥ 4, and any placement of the fixed step will leave at least two consecutive variable steps (since the gaps are at most the distance to the fixed step). So for p>3, there are no Type 1 words unless a=b (self-loop). But even for a=b, consecutive steps of (a,a) are allowed because a=b. So for a=b, we can have any arrangement of the p-1 variable steps. So for self-loops at zero positions, Type 1 words exist for any p.

Wait, we need to be careful: If a=b, then the edge is a self-loop. The step (a,a) goes from a to a. So v_{s-1}=a, v_s=a. So consecutive such steps are fine: v_s = a = a. So for a self-loop, we can have any number of consecutive steps on that loop.

Thus, the analysis depends on whether the zero position is a self-loop (i=j) or not.

But perhaps there's a simpler way: The sum S_{ij} can be expressed in terms of matrix operations. Let's try to find a closed form.

Recall that we have the factorization: S = (-1)^K * T, where T is the sum over words of weight of fixed entries, with words allowed to use variable positions as long as the total number of times each variable is used is a multiple of p-1. But we can think of the sum over all words of length p of the product of "something". Since the sum over variables factorizes, we can incorporate the variable sum into the matrix entries.

Specifically, consider an extended matrix where each entry is a polynomial in a variable representing the sum over choices. But we need to be careful.

Alternatively, note that the condition that each variable's exponent is a multiple of p-1 is equivalent to saying that in the sum over all assignments, the contribution is nonzero only if the monomial's degree in each variable is a multiple of p-1. This is reminiscent of the fact that the sum of (p-1)th powers of variables is p-1, and the sum of any other power is 0. So we can think of the generating function: For each variable x (corresponding to a zero position), we have a "weight" that is 1 if we don't use it, or if we use it a multiple of p-1 times, we get a factor of -1. But it's easier to use matrix exponentiation with a modified matrix.

Consider the matrix M defined as:
M_{ij} = A_{ij} if A_{ij} ≠ 0,
M_{ij} = y_{ij} if A_{ij} = 0, where y_{ij} is a formal variable.
Then (M^p)_{ij} is a homogeneous polynomial of degree p in the y's. We want to sum this polynomial over all assignments y_{ij} ∈ {1,...,p-1} and then multiply by the product of fixed entries? Wait, no: The sum over B of B^p is exactly the evaluation of (M^p) where each y_{ij} is replaced by the sum over its values? No.

Actually, consider the matrix B. B_{ij} = A_{ij} if A_{ij} ≠ 0, else a variable. The sum over B of B^p is the sum over all assignments of the matrix power. If we define a matrix where each variable entry is replaced by a formal variable, then the sum over assignments is obtained by applying a linear operator that maps each variable x to Σ_{v=1}^{p-1} v^e for the term x^e. But that's not linear.

However, we can use the fact that the sum over v of v^e is 0 unless (p-1)|e, in which case it's -1. So we can define a "summation" operator that for a monomial Π x_v^{e_v} returns (-1)^{#v with e_v>0} if all e_v are multiples of p-1, else 0. This is equivalent to setting each variable to 1? No.

Wait, there is a trick: For each variable x, we have Σ_{v=1}^{p-1} v^e = 0 if (p-1) ∤ e, and = -1 if (p-1) | e. This is exactly the evaluation of the polynomial Σ_{v=1}^{p-1} v^e. But note that for any integer e, Σ_{v=1}^{p-1} v^e ≡ Σ_{v=1}^{p-1} v^{e mod (p-1)} (by FLT, v^{p-1} ≡ 1, so v^e depends on e mod p-1). Actually, v^e = v^{e mod (p-1)} if we consider v^{p-1} ≡ 1, but v=0 is not in the sum. So the sum is 0 unless e ≡ 0 mod p-1.

Now, consider the matrix exponential: We want to compute S = Σ_{B} B^p. This is similar to computing the p-th power of a matrix where each variable entry is replaced by a "sum" over its values. But since the sum over values is not linear in the entry, we cannot simply replace the entry by a constant.

However, note that the sum over v of v^e is equal to the coefficient of something? There is a known identity: For any prime p, Σ_{v=1}^{p-1} v^e ≡ 0 mod p if (p-1) ∤ e, and ≡ -1 mod p if (p-1) | e. This is the same as the evaluation of the polynomial (x^{p-1} - 1)/(x-1) at x=0? Not exactly.

But we can use the following: The sum over v ∈ F_p^* of v^e is equal to the sum of the e-th powers of all nonzero elements. This is -1 if p-1 | e, and 0 otherwise.

Now, in the expansion of (M^p)_{ij}, we have a sum over walks of length p of the product of the entries. If we replace each variable entry x by a formal variable, the monomial is a product of variables and fixed entries. The sum over assignments is obtained by replacing each variable x^e with Σ_{v} v^e. So the total sum is obtained by applying the linear map φ that sends x^e to S(e) = Σ_{v=1}^{p-1} v^e.

Since S(e) is nonzero only when (p-1) | e, and in that case S(e) = -1, we can think of φ as the projection onto the subspace of polynomials where each variable has degree a multiple of p-1, scaled by (-1)^{#variables}. But that seems complicated.

Maybe we can use the matrix M defined as:
M_{ij} = A_{ij} if A_{ij} ≠ 0,
M_{ij} = 1 if A_{ij} = 0? No.

Wait, we have the result from sample 1 that S = (-1)^K * (F^p + something). Let's compute F^p + something to match sample 1.

Sample 1: p=3, K=2, (-1)^K=1.
F = [[0,1],[0,2]]. F^3 = [[0,1],[0,2]] as computed.
We need S = [[0,2],[1,2]].
So S - F^3 = [[0,1],[1,0]].

Thus there is an extra matrix E = [[0,1],[1,0]] such that S = F^3 + E.

What is E? It corresponds to Type 1 words. Let's enumerate Type 1 words for sample 1.

Zero positions: (1,1) and (2,1). Both have a≠b? (1,1) is a self-loop (a=b=1). (2,1) is not a self-loop (2≠1).

For each zero position v, we consider words where v is used p-1=2 times, and one fixed step. The product of fixed entries is the value of that fixed step.

First, zero position (1,1) (self-loop at 1). Variable used twice. The walk has 3 steps. The variable steps are (1,1) twice. The fixed step is some edge. The walk must be consistent. Let's find all walks of length 3 from i to j that use (1,1) exactly twice and one fixed edge.

Let the walk be v0,v1,v2,v3. Two of the steps are (1,1), one is fixed. Since (1,1) is a self-loop, it can appear anywhere. But the walk must start at i and end at j.

Case: Fixed step is step 1 (from v0 to v1). Then v0->v1 is fixed, v1->v2 = (1,1), v2->v3 = (1,1). So v1 = a? Actually step 1 is fixed, so (v0,v1) is a fixed edge. Step 2: (v1,v2) = (1,1) => v1=1, v2=1. Step 3: (v2,v3) = (1,1) => v2=1, v3=1. So v1 must be 1, so the fixed edge must end at 1: (v0,1) with v0 arbitrary? But fixed edge (v0,1) must be a nonzero entry in A. Fixed edges: (1,2) and (2,2). Neither ends at 1. So no such walk.

Fixed step is step 2: v0->v1 = (1,1), v1->v2 fixed, v2->v3 = (1,1). So v0=1, v1=1. Then fixed edge (1,v2) must be nonzero: (1,2) is nonzero, so v2=2. Then step 3: (v2,v3) = (1,1) => v2=1, but v2=2. Contradiction. So no.

Fixed step is step 3: v0->v1 = (1,1), v1->v2 = (1,1), v2->v3 fixed. So v0=1, v1=1, v2=1. Fixed edge (1,v3) must be nonzero: (1,2) works, so v3=2. This gives walk: 1->1 (zero), 1->1 (zero), 1->2 (fixed). This is a walk from 1 to 2 using zero (1,1) twice and fixed (1,2) once. Product of fixed entries: F_{1,2} = 1. So contribution: weight = 1.

Case: Fixed step is step 1: v0->v1 fixed, v1->v2 = (1,1), v2->v3 = (1,1). As before, v1=1, v2=1, v3=1. Fixed edge (v0,1). None.

Fixed step step 2: v0->v1 = (1,1), v1->v2 fixed, v2->v3 = (1,1). v0=1, v1=1. Fixed (1,v2) nonzero: v2=2. Then v2->v3 = (1,1) forces v2=1, contradiction.

Fixed step step 3: v0->v1 = (1,1), v1->v2 = (1,1), v2->v3 fixed. v0=1, v1=1, v2=1. Fixed (1,v3) nonzero: v3=2. So walk 1->1->1->2. This is from 1 to 2. So contributes to S_{1,2} weight 1.

Now, zero position (2,1) (not self-loop). a=2, b=1. Used twice. Walk length 3. The variable steps are (2,1). The fixed step is some edge.

We need a walk v0,v1,v2,v3 with two steps (2,1) and one fixed step. The two (2,1) steps must be placed such that the vertices match. Since (2,1) goes from 2 to 1, consecutive (2,1) steps would require the end of first (1) to be the start of second (2), so 1=2, impossible. So the two (2,1) steps cannot be consecutive. Thus the fixed step must separate them. So the only possible arrangement is: step 1: (2,1), step 2: fixed, step 3: (2,1). Or step 1: fixed, step 2: (2,1), step 3: (2,1)? But step 2 and 3 would be consecutive (2,1), impossible. Or step 1: (2,1), step 2: (2,1) consecutive, impossible. So only arrangement: fixed step in the middle.

Thus: v0->v1 = (2,1) => v0=2, v1=1.
v1->v2 fixed => (1, v2) fixed. Fixed edges: (1,2) gives v2=2. (2,2) starts at 2, not 1. So only (1,2) works, so v2=2.
v2->v3 = (2,1) => v2=2, v3=1.
So walk: 2->1 (zero), 1->2 (fixed), 2->1 (zero). This goes from v0=2 to v3=1. So it contributes to S_{2,1}. The fixed step is (1,2) with value 1. Weight = 1.

Also, could the fixed step be at the ends? Let's try fixed step step 1: v0->v1 fixed, v1->v2 = (2,1), v2->v3 = (2,1). Then v1->v2 = (2,1) => v1=2, v2=1. v2->v3 = (2,1) => v2=2, but v2=1. Contradiction.
Fixed step step 3: v0->v1 = (2,1), v1->v2 = (2,1). v0=2, v1=1. v1->v2 = (2,1) => v1=2, but v1=1. Contradiction.
So only the middle fixed step works.

Thus, from zero (2,1), we get one walk: 2->1->2->1, contributing to S_{2,1} weight = F_{1,2} = 1.

Now, also we could have the fixed step being (2,2) in the middle? The fixed step must be (v1,v2). v1 is the end of first (2,1) which is 1. So the fixed edge must start at 1. Only (1,2) starts at 1. So no.

Thus total extra matrix E (from Type 1) has contributions:
- From (1,1): walk 1->1->1->2 gives S_{1,2} += 1.
- From (2,1): walk 2->1->2->1 gives S_{2,1} += 1.
Also, could there be walks ending at other nodes? For (1,1), we also could have fixed step at the beginning? We checked, no. Could we have the walk start at 2? Let's see: For (1,1) self-loop, we could have walk starting at 2: v0=2, then we need two (1,1) steps and one fixed. But (1,1) steps require the vertex to be 1. So if we start at 2, the first step must be fixed to get to 1. Let's try: step1 fixed, step2 (1,1), step3 (1,1). v0=2, v1->v2 fixed, v2->v3 = (1,1) => v2=1, v3=1. v1->v2 fixed means (v1,1) fixed. Fixed edges ending at 1: none. So no.
Step1 (1,1), step2 fixed, step3 (1,1): v0=1, v1=1. So start must be 1. So only start at 1.
Step1 (