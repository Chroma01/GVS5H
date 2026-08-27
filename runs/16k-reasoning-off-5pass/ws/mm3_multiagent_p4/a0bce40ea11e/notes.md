
## ideation
The problem requires computing the sum over all matrices B (formed by replacing zeros in A with nonzero values 1..p-1) of B^p, modulo prime p. N ≤ 100, p up to 1e9.

Key observations:
1. Over F_p, raising a matrix to the p-th power is not entrywise, but we can expand (B^p)_{ij} as a sum over walks of length p of products of entries.
2. Summing over all B means summing each monomial (product of p entries) over independent choices of variables (zeros).
3. The sum over a variable x of x^e mod p is 0 unless (p-1) | e, in which case it equals -1 mod p.
4. Thus, a monomial survives only if each zero position's exponent is a multiple of p-1. Since total degree is p, the only possibilities are:
   - No zeros used (all steps are fixed nonzero entries).
   - Exactly one zero position used p-1 times, and one fixed step (the remaining step).
5. In both cases, the contribution of a surviving walk is (-1)^K times the product of the fixed entries along the walk.
6. Therefore, the desired sum S = (-1)^K * T, where T_{ij} is the sum over all valid walks (of both types) of the product of fixed entries.
7. For p=2, p-1=1, so every walk is valid; T is exactly (F^2) where F is the matrix with zeros replaced by 1. The factor (-1)^K is 1 mod 2, so S = F^2 mod 2.
8. For p>2, we need to compute T = (F^p) + extra contributions from walks that use exactly one zero position p-1 times. The extra contribution for a zero at (a,b) involves walks where p-1 steps are (a,b) and one step is a fixed edge. This can be expressed using matrix powers and the structure of the walk.

However, a simpler unified approach exists: The sum S can be computed by noting that the generating function for each zero entry x is the polynomial Σ_{v=1}^{p-1} x^v? No, we sum over values, not powers.

Alternative: The sum over B of B^p is equal to the coefficient of something in a matrix exponential? Not directly.

We can use the fact that the sum over v of v^e is -1 if (p-1)|e else 0. This is the evaluation of the polynomial (x^{p-1}-1)/(x-1) at x=0? Actually, Σ_{v=1}^{p-1} v^e = 0 if p-1 ∤ e, and = -1 if p-1 | e. This is exactly the result of applying the operator that maps x to 1 - x^{p-1}? Not exactly.

Another approach: The matrix M where M_{ij} = A_{ij} for nonzero, and M_{ij} = y for zeros. We want Σ_{y_v ∈ {1..p-1}} (M^p). The sum over each y_v of y_v^e is S(e). We can think of this as replacing each y_v by a formal variable and then applying a linear functional. But we can encode S(e) by noting that S(e) = -1 if e ≡ 0 mod p-1, else 0. This is the same as the coefficient of x^e in the polynomial P(x) = -1 + 0*x + ... + 0*x^{p-2} - 1*x^{p-1} + 0*x^p + ...? Actually, S(e) is periodic with period p-1. We can use the discrete Fourier transform: S(e) = - (1/(p-1)) Σ_{k=0}^{p-2} ω^{-ke} where ω is a primitive (p-1)th root of unity in some extension. But we are working mod p, and p-1 divides p-1, but we don't have primitive roots in F_p necessarily? Actually, F_p^* is cyclic of order p-1, so there exists a primitive root g. Then Σ_{v=1}^{p-1} v^e = Σ_{i=0}^{p-2} g^{ie} = 0 if g^e ≠ 1, i.e., p-1 ∤ e, and = p-1 ≡ -1 if p-1 | e. So S(e) = -1 if p-1|e, else 0.

Thus, for each variable x, the sum over its values of x^e is S(e). We can think of this as the result of applying the linear map that sends the monomial x^e to S(e). This map can be realized by replacing x with a matrix? Not easily.

But we can use the fact that in the expansion of (M^p), the coefficient of a monomial Π x_v^{e_v} is the number of walks with those exponents. Summing over assignments gives Σ_{walks} Π S(e_v(w)). As argued, this is (-1)^K times the number of walks where each e_v is a multiple of p-1, times the product of fixed entries.

Now, to compute T efficiently, we can construct a larger matrix that tracks the usage of zero positions. Since p-1 is large (up to 1e9), we cannot track exact counts. But note that the condition is that the total number of times a particular zero is used is either 0 or p-1 (or higher multiples, but only p-1 is possible due to length). So we can think of it as: each zero position can be used 0 times or p-1 times. In a walk of length p, if a zero is used p-1 times, it must be used in p-1 steps, and the remaining one step is fixed.

We can model this by considering the matrix F of fixed entries, and for each zero position z = (a,b), we consider a modified matrix where we "insert" p-1 steps of z. But inserting p-1 steps of a self-loop is like multiplying by the (p-1)th power of a matrix with that entry? Not exactly, because the steps are not necessarily consecutive, but for a self-loop they can be anywhere, and for non-self-loop they must be arranged to avoid consecutive same steps unless a=b.

Actually, the number of ways to arrange p-1 identical steps of a self-loop and 1 fixed step in a sequence of p steps is C(p,1) = p. But the walk's vertices must be consistent. For a self-loop at a, the walk can start anywhere, then take the self-loop p-1 times (staying at a), then take the fixed step from a to some b. So the walk is: start at some v0, then if the fixed step is not the first, we need to get to a. Actually, the walk must be a sequence of vertices. If the self-loop is used p-1 times, the vertex a must be visited at least p-1 times. The only way is that the walk enters a, then stays at a for p-1 steps via the self-loop, then exits via the fixed step. The entry to a could be via a fixed step as well, but we only have one fixed step. So the fixed step could be the entry or the exit. Let's analyze carefully.

Let the zero be (a,b). The steps are p-1 times (a,b) and 1 fixed step. The walk has p+1 vertices v0,...,vp. The steps are (v_{s-1}, v_s). For each variable step, (v_{s-1}, v_s) = (a,b). This implies that for each such step, v_{s-1}=a and v_s=b. If a ≠ b, then consecutive variable steps are impossible because v_s would be b, and the next step would require v_s=a. So for a≠b, the variable steps cannot be adjacent. Thus the single fixed step must separate the variable steps into two groups. Since there are p-1 variable steps and they cannot be adjacent, the only possibility is that the fixed step is in the middle, and there is at most one variable step on each side. But p-1 ≥ 2 for p≥3, so we would need at least two variable steps on one side, which would be adjacent. Therefore, for a≠b, the only possible p is 3 (p-1=2), where we can have one variable step before and one after the fixed step. For p>3, no such walk exists for a≠b.

For a=b (self-loop), consecutive steps are allowed. The walk can be: enter a via a fixed step (or start at a), then take the self-loop p-1 times, then exit via a fixed step. But we only have one fixed step. So either the entry is the fixed step and the exit is a variable step? No, the fixed step is only one. So the walk must be: start at some vertex, then take the fixed step to a, then take the self-loop p-1 times, then? There is no more fixed step to exit. The walk would end at a. So the walk is: v0 -> a (fixed), then a->a (self-loop) p-1 times, end at a. So the walk goes from v0 to a. Or: start at a, take self-loop p-1 times, then take fixed step a->v_p, ending at v_p. So the walk goes from a to v_p. Or: start at a, take some self-loops, then a fixed step, then more self-loops? But the fixed step is only one, and after the fixed step, the vertex is v_p. If we have self-loops after the fixed step, they would be at v_p, not at a. So that would require a self-loop at v_p. So if the fixed step ends at a, and we have self-loops after, they must be at a. So the fixed step must start at a? Let's formalize.

Suppose we have a self-loop at a. The walk consists of p-1 self-loops and 1 fixed step. The self-loops can be placed anywhere. The fixed step is (x,y) with x≠a or y≠a (unless the fixed step is also a self-loop, but fixed entries are nonzero, could be a self-loop if A_{a,a}≠0, but then it's not a zero position). So the fixed step changes the vertex. The self-loops keep the vertex at a. So the walk can only be at a when taking self-loops. Therefore, the walk must consist of a segment at a, possibly with a fixed step entering a or leaving a. Since there is only one fixed step, the walk is either:
- Start at a, take some self-loops, then take the fixed step a->y, then? No more self-loops because we left a. So all self-loops must be before the fixed step. So the walk is: a -> a -> ... -> a (p-1 times) -> y. This goes from a to y. The product of fixed entries is F_{a,y}.
- Start at x, take the fixed step x->a, then take self-loops at a p-1 times. This goes from x to a. Product F_{x,a}.
- Or, could the fixed step be in the middle of self-loops? For example: self-loops, then fixed step, then self-loops. But after the fixed step, we are at y. To take self-loops, we need a self-loop at y. So if y=a, then the fixed step must be a self-loop, but it's fixed, so A_{a,a}≠0, contradiction because (a,a) is a zero. So no.
- Could we have fixed step not touching a? If the fixed step is elsewhere, then the walk must be at a for all self-loops, but the fixed step is elsewhere, so the walk would be disconnected. So the fixed step must be adjacent to the self-loop segment: either entering a or leaving a.

Thus, for a self-loop zero at a, the valid walks are:
- From a to y: path of p-1 self-loops at a followed by edge a->y (where F_{a,y}≠0). The number of such walks: for each y with F_{a,y}≠0, there is exactly one walk (the sequence of p-1 loops then the edge). Actually, the self-loops are all at a, so the walk is a, a, ..., a, y. That's one walk. But wait, the self-loops are p-1 times, so the walk has vertices: a (start), then after first self-loop still a, ..., after p-1 self-loops still a, then the fixed step to y. So the walk is determined uniquely by y. So the number of walks from a to y using this zero is 1 if F_{a,y}≠0, else 0. But the product of fixed entries is F_{a,y}. So contribution to T_{a,y} is F_{a,y}.
- From x to a: path x->a (fixed) then p-1 self-loops at a. This is a walk from x to a. The product is F_{x,a}. So contribution to T_{x,a} is F_{x,a}.

But wait, are there any other self-loops at a? The self-loops are p-1 times, but we could also have the walk start at a, take some self-loops, then the fixed step, then more self-loops? As argued, no, because after fixed step we are at y≠a (since fixed edge is nonzero and not at (a,a) because that's zero), and there is no self-loop at y. So only the two types above.

Thus, for a self-loop zero at a, the extra contribution to T is: for each y with F_{a,y}≠0, add F_{a,y} to T_{a,y}; for each x with F_{x,a}≠0, add F_{x,a} to T_{x,a}.

For a non-self-loop zero at (a,b) with a≠b, we argued that only p=3 allows a walk. For p=3, the walk must be: a->b (zero), b->c (fixed), c->a (zero) or b->a? Wait, the zero is (a,b). The steps are (a,b) twice and one fixed step. The walk must have two (a,b) steps and one fixed step. Since a≠b, the two (a,b) steps cannot be consecutive. So the fixed step must be in the middle. The walk is: start at a, step1: (a,b) (zero), now at b. Step2: fixed step (b,c) (must be nonzero), now at c. Step3: (c,d) = (a,b) => c=a, d=b. So the fixed step must be (b,a). So the walk is a -> b -> a -> b. This goes from a to b. The product of fixed entries is F_{b,a}. So contribution to T_{a,b} is F_{b,a}. Also, could the walk start at b? Start at b, step1: fixed step (b,c), step2: (a,b), step3: (a,b)? But then step2 and step3 are consecutive (a,b), impossible. So only the above. Also, could the fixed step be at the ends? Start at a, step1: (a,b), step2: (a,b) consecutive, impossible. So only the middle fixed step works. So for each non-self-loop zero (a,b) with a≠b, if p=3, we get an extra contribution: for each fixed edge (b,c) with F_{b,c}≠0, we have a walk a->b->c->? Wait, the walk is a->b->c->? Actually, the walk is: a (start) -> b (zero), b->c (fixed), c->? must be (a,b), so c=a, and then end at b. So the fixed step is (b,a). So we need a fixed edge from b to a. So the walk is a->b (zero), b->a (fixed), a->b (zero). This goes from a to b. The product is F_{b,a}. So contribution to T_{a,b} is F_{b,a}. Note that this requires F_{b,a} ≠ 0. If F_{b,a}=0, then no contribution. Also, could the walk go from b to a? Symmetric: b->a (zero), a->b (fixed), b->a (zero) gives walk b->a, product F_{a,b}. So for each non-self-loop zero (a,b), if p=3, we get two extra walks: a->b using fixed (b,a), and b->a using fixed (a,b). So contributions: T_{a,b} += F_{b,a}, T_{b,a} += F_{a,b}.

For p>3 and a≠b, no extra contributions.

Thus, the extra matrix E can be constructed as:
- For each zero position (a,b):
  - If a == b (self-loop):
    - For each y with F_{a,y} ≠ 0: E_{a,y} += F_{a,y}.
    - For each x with F_{x,a} ≠ 0: E_{x,a} += F_{x,a}.
  - If a != b and p == 3:
    - If F_{b,a} ≠ 0: E_{a,b} += F_{b,a}.
    - If F_{a,b} ≠ 0: E_{b,a} += F_{a,b}.

Then T = F^p + E, and S = (-1)^K * T mod p.

Let's test this formula on sample 1.
p=3, K=2, (-1)^K=1.
F = [[0,1],[0,2]].
F^3 = [[0,1],[0,2]] as before.
Zeros: (1,1) self-loop, (2,1) non-self-loop.
For (1,1): self-loop at 1. Fixed edges from 1: (1,2) with F=1. So E_{1,2} += 1. Fixed edges to 1: none (since (1,1) is zero, (2,1) is zero, (1,2) is fixed but goes to 2, not 1). So E_{1,1} +=? No. So E gets +1 at (1,2).
For (2,1): non-self-loop, p=3. Fixed edge (1,2) from 1 to 2. So we need F_{1,2}? The rule: for (a,b)=(2,1), we add F_{b,a} = F_{1,2} to E_{2,1}. F_{1,2}=1. So E_{2,1} += 1. Also, we add F_{a,b}=F_{2,1} to E_{b,a}=E_{1,2}, but F_{2,1}=0 (since it's a zero). So no.
Thus E = [[0,1],[1,0]].
Then T = F^3 + E = [[0,1],[0,2]] + [[0,1],[1,0]] = [[0,2],[1,2]].
S = 1 * T = [[0,2],[1,2]]. Matches sample!

Test sample 2: p=2, N=3, A has ones on diagonal, zeros elsewhere. So F = A (since all entries are 1 or 0? Actually nonzero entries are 1, so F = A). Zeros: all off-diagonal. K = 6. (-1)^6 = 1 mod 2. p=2, so we use the p=2 case: S = F^2 mod 2. F is matrix with 1 on diagonal, 0 elsewhere. F^2 = I (since diagonal 1, off-diagonal 0). But sample output is all ones. Wait, sample 2 output is all ones. But F^2 = I, which is diagonal ones, not all ones. Something is wrong.

Let's re-examine sample 2. Input:
3 2
1 0 0
0 1 0
0 0 1
So A has 1 on diagonal, 0 elsewhere. Zeros: all off-diagonal. p=2.
Our p=2 rule: replace zeros with 1 (since p-1=1). So B is all ones matrix. B^2 = 3 * J, where J is all-ones. Mod 2, 3 ≡ 1, so B^2 ≡ J. So S = J (all ones). That matches sample.
But our formula S = F^2 with F being the matrix of fixed entries? For p=2, we said S = B^2 where B has zeros replaced by 1. But F is the matrix of fixed entries (nonzero entries of A). In sample 2, fixed entries are the diagonal ones. So F is the identity matrix. F^2 = I. That's not B^2. So our p=2 rule was incomplete: we need to include the variable contributions as well? Wait, for p=2, p-1=1. The sum over a variable of x^e is Σ_{v=1}^{1} v^e = 1. So S(e) = 1 for all e. Thus every monomial survives with factor 1. So S = sum over all B of B^2, but since there's only one B (zeros become 1), it's just B^2. And B is A with zeros replaced by 1. So we need to compute B^2, not F^2. So for p=2, the answer is simply (A' )^2 mod 2, where A' is A with zeros replaced by 1. That is not F^2 unless all entries are fixed. So our general formula S = (-1)^K * (F^p + E) does not apply for p=2. We need a separate case for p=2.

For p=2, we can just set B_{ij} = 1 if A_{ij}=0, else A_{ij}. Then compute B^2 mod 2. N ≤ 100, O(N^3) is fine.

Now for p>2, we have S = (-1)^K * (F^p + E) mod p.
Let's test sample 3: p=13, N=4, A given. Compute K and E.
We can write a program to compute this and verify.

But we need to be sure about the E construction. Let's derive E more systematically.

We want T = sum over valid walks w of length p of weight(w), where weight is product of fixed entries.
Valid walks: either all steps fixed, or exactly one zero position z used p-1 times and one fixed step.
For a fixed zero z = (a,b):
- Case 1: a = b (self-loop).
  The walk must be: either enter a via a fixed step, then p-1 self-loops; or start at a, p-1 self-loops, then exit via a fixed step.
  - Subcase 1a: start at a, p-1 self-loops, then fixed step a->y. Walk: a -> a -> ... -> a (p times) -> y. Length: p-1 self-loops + 1 fixed = p steps. Vertices: a, a, ..., a, y. This is a valid walk from a to y. Weight = F_{a,y}. This exists for any y with F_{a,y} ≠ 0.
  - Subcase 1b: start at x, fixed step x->a, then p-1 self-loops. Walk: x -> a -> a -> ... -> a. Length: 1 fixed + p-1 self-loops = p steps. This is a walk from x to a. Weight = F_{x,a}. Exists for any x with F_{x,a} ≠ 0.
  Note: Could we have both entry and exit? That would require two fixed steps, but we only have one. So no.
- Case 2: a ≠ b.
  As argued, for p=3, we can have the walk: a -> b (zero), b -> c (fixed), c -> d (zero) with (c,d) = (a,b) => c=a, d=b. So fixed step is (b,a). Walk: a -> b -> a -> b. This is from a to b. Weight = F_{b,a}. Also, the symmetric walk: b -> a -> b -> a (using zero (a,b) twice? Wait, the zero is (a,b). The walk b -> a uses the zero? Actually, the zero is (a,b) meaning entry a, exit b. So a step (a,b) goes from a to b. So to go from b to a, we need the zero (b,a)? But the zero is (a,b), not (b,a). So the walk b -> a cannot use the zero (a,b) because that goes from a to b. Let's check: In the walk a->b->a->b, the steps are: (a,b) zero, (b,a) fixed, (a,b) zero. So the zero is used twice, both times from a to b. The fixed step is from b to a. So the walk starts at a and ends at b. What about a walk from b to a using the same zero? That would require steps: (b,?) zero? But the zero is (a,b), so it must start at a. So to start at b, we need a fixed step from b to a first? Let's try: b -> a (fixed), a -> b (zero), b -> a (zero)? The second and third steps: (a,b) and (b,a). The third step is (b,a), but our zero is (a,b), not (b,a). So the third step would need to be (a,b), but that goes from a to b, not b to a. So we cannot have a step (b,a) unless (b,a) is also a zero or fixed. So the only walk using zero (a,b) twice is the one that starts and ends with the zero's direction. Actually, the zero is an edge from a to b. In a walk, we can traverse it only in the forward direction. So we can only use the edge a->b. So the walk must have the pattern: ... -> a -> b -> ... -> a -> b -> ... with the fixed step in between. The fixed step must go from b to a to make the next a->b possible. So the walk is: start at a, a->b (zero), b->a (fixed), a->b (zero). End at b. So from a to b. What about starting at b? To start at b, we need a step from b. But the first step cannot be zero because zero is a->b. So it must be a fixed step. If we start at b with a fixed step b->c, then we need a zero a->b. So we need c=a. So fixed step b->a. Then we are at a. Then we can take zero a->b. Then we need to end. So walk: b -> a (fixed), a -> b (zero). That's only 2 steps, need 3 steps. To have 3 steps, we need another step. If we add another zero a->b, we would be at b, but then we need a step to continue? Actually, length 3: steps: b->a (fixed), a->b (zero), b->? The third step cannot be zero a->b because that starts at a. So we need another fixed step? But we only have one fixed step. So the walk b->a->b is only 2 steps. To make it 3 steps, we could insert a self-loop? Not allowed. So the only 3-step walk using zero (a,b) twice is the one starting at a and ending at b. So the extra contribution is only T_{a,b} += F_{b,a}. No T_{b,a} addition.

Wait, in our earlier manual enumeration for (2,1) in sample 1, we had a walk 2->1->2->1. Here a=2, b=1. Zero is (2,1). Walk: 2->1 (zero), 1->2 (fixed), 2->1 (zero). This is from 2 to 1. So it contributed to S_{2,1} with weight F_{1,2}=1. That matches T_{a,b} with a=2, b=1, and F_{b,a}=F_{1,2}=1. So T_{2,1} += 1. And there was no T_{1,2} from this zero. So our rule for non-self-loop zeros is: for each zero (a,b) with a≠b, if p=3, then T_{a,b} += F_{b,a}. No addition to T_{b,a}.

But wait, what if (b,a) is also a zero? Then F_{b,a}=0, so no contribution. That's fine.

Now, what about p>3 and a≠b? As argued, no extra contributions.

Thus, the extra matrix E is:
- For each zero (a,b):
  - If a == b:
    - For each y: if F_{a,y} ≠ 0, E_{a,y} += F_{a,y}.
    - For each x: if F_{x,a} ≠ 0, E_{x,a} += F_{x,a}.
  - If a != b and p == 3:
    - If F_{b,a} ≠ 0, E_{a,b} += F_{b,a}.

Now, is this complete? Let's consider the possibility of using a zero position that is a fixed entry? No, zeros are zeros.

Also, note that for p>2, we have S = (-1)^K * (F^p + E) mod p.
For p=2, S = (A')^2 mod 2, where A' is A with zeros replaced by 1.

We should test sample 3 with this formula.

Sample 3:
N=4, p=13.
A:
0 1 2 0
3 4 0 5
0 6 0 7
8 9 0 0

Zeros: positions with 0.
(1,1), (1,4), (2,3), (3,1), (3,3), (4,3), (4,4). Total K=7.
(-1)^7 = -1 mod 13 = 12.

F (nonzero entries):
[0, 1, 2, 0]
[3, 4, 0, 5]
[0, 6, 0, 7]
[8, 9, 0, 0]

We need to compute F^p = F^13 mod 13. N=4, we can compute by fast exponentiation, O(N^3 log p) = 64 * 30 = 1920 operations, fine.
Then compute E as above.
Then S = 12 * (F^13 + E) mod 13.

Let's try to compute manually? Might be tedious, but we can trust the formula and implement it.

We should also verify that for p>3, the extra contributions from non-self-loop zeros are indeed zero. What about self-loops that are not zeros? They are fixed, so they are in F.

What about the case where the fixed step in a Type 1 walk is also a self-loop at a? That is covered in Case 1: if the fixed step is a->y, and y=a, then F_{a,a} ≠ 0, so the walk is a->a->...->a (all self-loops). But the fixed step is a self-loop at a. However, the zero is also a self-loop at a. So the walk uses the zero p-1 times and the fixed self-loop once. But wait, the fixed step is (a,a). In the walk, we have p-1 zero self-loops and 1 fixed self-loop. The product of fixed entries is F_{a,a}. The walk is valid: start at a, take p-1 zero self-loops, then one fixed self-loop. All steps are at a. So the walk is from a to a. According to our rule for self-loop zero: Subcase 1a: start at a, p-1 self-loops, then fixed step a->y. Here y=a, so E_{a,a} += F_{a,a}. This is correct.

Also, could there be a walk where the fixed step is the entry to a? Subcase 1b: fixed step x->a, then p-1 self-loops. If x=a, then fixed step is a->a, so F_{a,a} is used. Then walk: a->a (fixed), then p-1 self-loops. That's the same as above but order reversed. In our rule, we add F_{a,a} to E_{a,a} from both subcases? Actually, Subcase 1b adds to E_{x,a} with x=a, so E_{a,a} += F_{a,a}. So if both x=a and y=a, we add twice. But is that correct? Let's check: The walk could be: start at a, take fixed self-loop, then p-1 zero self-loops. That's a valid walk. It is different from start at a, p-1 zero self-loops, then fixed self-loop. Both are valid walks and they are distinct (the order of steps is different). So we should count both. In the sum over walks, we sum over all sequences of steps. So both should be included. Our E construction adds both. So that's correct.

What about p=2? For p=2, p-1=1. A Type 1 walk uses one variable and one fixed step? Actually, for p=2, total length 2. The condition for variable exponent: multiple of 1 is always true. So any assignment of the variable works. But we already handled p=2 separately.

Now, we must also consider the possibility of using more than one variable position? As argued, for p>2, the total number of variable entries used must be a multiple of p-1. Since p-1 ≥ 2, the only multiples ≤ p are 0 and p-1. So we cannot use two different variables, because that would require at least 2(p-1) ≥ 4 > p for p>3, or for p=3, 2(p-1)=4 >3. So no.

Thus, the formula seems solid.

Now, we need to implement:
- Read N, p, matrix A.
- If p == 2:
  - Create matrix B where B_{ij} = 1 if A_{ij} == 0 else A_{ij}.
  - Compute B^2 mod 2.
  - Output B^2.
- Else (p odd prime):
  - Compute K = number of zeros in A.
  - Compute sign = 1 if K is even, -1 if K is odd, i.e., sign = (-1)^K mod p.
  - Construct F: F_{ij} = A_{ij} if A_{ij} != 0 else 0.
  - Compute F^p mod p using fast exponentiation (O(N^3 log p)).
  - Initialize E as zero matrix.
  - For each zero position (i,j) in A:
    - If i == j:
      - For each y: if F_{i,y} != 0, E_{i,y} = (E_{i,y} + F_{i,y}) mod p.
      - For each x: if F_{x,i} != 0, E_{x,i} = (E_{x,i} + F_{x,i}) mod p.
    - Else if p == 3:
      - If F_{j,i} != 0, E_{i,j} = (E_{i,j} + F_{j,i}) mod p.
  - Compute T = (F^p + E) mod p.
  - Compute S = (sign * T) mod p.
  - Output S.

Let's test this algorithm on sample 1 manually.
p=3, odd. K=2, sign=1.
F = [[0,1],[0,2]].
F^3 = [[0,1],[0,2]].
E: zeros: (1,1) self-loop, (2,1) non-self-loop.
(1,1): i=j=1. For y: F_{1,2}=1, so E_{1,2} += 1. For x: F_{x,1}: F_{1,1}=0, F_{2,1}=0. So E_{1,1} no add. E = [[0,1],[0,0]].
(2,1): i=2,j=1, p=3. F_{1,2}=1, so E_{2,1} += 1. E = [[0,1],[1,0]].
T = F^3 + E = [[0,1],[0,2]] + [[0,1],[1,0]] = [[0,2],[1,2]].
S = 1 * T = [[0,2],[1,2]]. Correct.

Sample 3: We can code it and trust.

Edge cases: p=2 handled separately.
What about p=3 and a self-loop zero? The self-loop rule adds both entry and exit. For p=3, could there be additional contributions from non-self-loop zeros besides the T_{a,b} += F_{b,a}? We argued no.

Wait, for p=3 and a self-loop zero, the self-loop rule adds E_{a,y} += F_{a,y} and E_{x,a} += F_{x,a}. But is there also a walk where the fixed step is in the middle of two self-loops? For p=3, p-1=2 self-loops. The walk has 2 self-loops and 1 fixed step. The self-loops are both at a. The fixed step is (x,y). The walk must be consistent. Possibilities:
- Fixed step first: x -> y, then y -> a? But then the next step is self-loop at a, so y must be a. So fixed step is x->a. Then self-loop: a->a. Then another self-loop: a->a. So walk: x -> a -> a -> a. This is from x to a. This is covered by Subcase 1b: fixed step x->a, then p-1=2 self-loops. So E_{x,a} += F_{x,a}.
- Fixed step last: self-loop, self-loop, fixed step a->y. This is a->a->a->y. Covered by Subcase 1a: E_{a,y} += F_{a,y}.
- Fixed step in the middle: self-loop, fixed step, self-loop. Then: a -> a (self-loop), then a -> y (fixed), then y -> a (self-loop). But the third step is a self-loop, so it must be at y, requiring y=a. So fixed step a->a. Then walk: a->a->a->a. This is from a to a. This is covered by both Subcase 1a and 1b when y=a and x=a. Specifically, Subcase 1a with y=a: E_{a,a} += F_{a,a}. Subcase 1b with x=a: E_{a,a} += F_{a,a}. So we add F_{a,a} twice. Is that correct? Let's enumerate the walks for a self-loop zero at a and fixed self-loop at a (if F_{a,a}≠0). The walk is a sequence of 3 steps: two are zero self-loops, one is fixed self-loop. The number of such sequences is C(3,1)=3 (choose position of fixed step). The walks are:
- Fixed, zero, zero: a->a (fixed), a->a (zero), a->a (zero). Walk: a,a,a,a. Weight: F_{a,a}.
- Zero, fixed, zero: a->a (zero), a->a (fixed), a->a (zero). Weight: F_{a,a}.
- Zero, zero, fixed: a->a (zero), a->a (zero), a->a (fixed). Weight: F_{a,a}.
All three walks are from a to a. So total contribution to T_{a,a} should be 3 * F_{a,a}. Our rule adds F_{a,a} from Subcase 1a (zero,zero,fixed) and F_{a,a} from Subcase 1b (fixed,zero,zero). It misses the middle one (zero,fixed,zero). So we are missing one contribution!

Ah! This is a crucial catch. For a self-loop zero, when the fixed step is also a self-loop at the same vertex, the walk with fixed step in the middle is not captured by our two subcases. Subcase 1a is zero...zero,fixed. Subcase 1b is fixed,zero...zero. The middle fixed step is zero,fixed,zero. So we need to add that as well.

In general, for a self-loop zero at a, the p-1 self-loops and 1 fixed step can be arranged in p ways (choose position of fixed step). The fixed step could be anywhere. The walk will be valid as long as the fixed step's endpoints match the surrounding self-loops. If the fixed step is not a self-loop, then it changes the vertex. For the walk to be valid, the vertex before the fixed step must be a, and the vertex after must be a? Actually, the self-loops keep the vertex at a. If the fixed step is at position t, then the steps before t are self-loops at a, so the vertex before the fixed step is a. The fixed step is (a, y). After the fixed step, the vertex is y. The steps after t are self-loops. For those to be valid, we need y = a. So the fixed step must be a self-loop at a. Otherwise, the walk would be at y after the fixed step, and self-loops at y would be needed, but we only have self-loops at a. So if the fixed step is not a self-loop at a, then the fixed step must be the last step (so no self-loops after) or the first step (so no self-loops before). If it's the last step, then all self-loops are before, so vertex before fixed is a, fixed is a->y, and we end at y. This is Subcase 1a. If it's the first step, then fixed is x->a, and all self-loops are after, so we end at a. This is Subcase 1b. If the fixed step is in the middle, then we need self-loops both before and after, so the fixed step must be a self-loop at a to keep the vertex at a. So for a self-loop zero at a, the extra walks are:
- If the fixed step is a->y with y≠a: it must be the last step. Contribution: E_{a,y} += F_{a,y}.
- If the fixed step is x->a with x≠a: it must be the first step. Contribution: E_{x,a} += F_{x,a}.
- If the fixed step is a->a (i.e., F_{a,a} ≠ 0): it can be in any of the p positions. The walk is all self-loops. There are p such walks (one for each position of the fixed step). All go from a to a. So contribution: E_{a,a} += p * F_{a,a} mod p. Since p ≡ 0 mod p, this is 0! Wait, p * F_{a,a} mod p = 0. So the contribution from the middle positions is 0 mod p. That's why we missed it: it contributes 0 mod p. So we don't need to add it.

Let's verify: For sample 1, (1,1) is a self-loop zero. F_{1,1}=0, so no issue. For a case where F_{a,a} ≠ 0, the contribution from the middle fixed steps is a multiple of p, hence 0 mod p. So our rule of adding only the first and last positions is correct mod p.

Thus, the self-loop rule is correct as is.

Now, what about non-self-loop zeros? For p=3, we have two self-loops? No, the zero is (a,b) with a≠b. The steps are two times (a,b) and one fixed step. The fixed step must be in the middle to avoid consecutive (a,b). So the walk is a->b (zero), b->c (fixed), c->d (zero) with (c,d)=(a,b) => c=a, d=b. So fixed step is b->a. This is the only arrangement. So no other possibilities.

Thus, the construction of E is correct.

Now, we need to compute F^p mod p for N up to 100. N^3 = 1e6, log2(1e9) ≈ 30, so about 3e7 operations, which is fine in Python with optimized loops (using list comprehensions or numpy? but we must implement in pure Python). We should use efficient matrix multiplication mod p. Since p can be up to 1e9, we need to use Python's big integers, but modulo operation is fast. N=100, matrix multiplication is O(N^3) = 1e6. 30 steps = 3e7 multiplications. In Python, 3e7 multiplications might be slow (around 1-2 seconds per 1e7?). We need to optimize.

We can use the fact that p is prime and we are working mod p. We can implement matrix multiplication using nested loops and avoid modulo at every step? But p can be up to 1e9, so intermediate products can be up to (p-1)^2 ≈ 1e18, which fits in Python int but we should take mod to keep numbers small. Actually, we can accumulate in a Python int and mod at the end of each row or column. Standard triple loop:

def mat_mul(A, B, mod):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k] == 0: continue
            aik = A[i][k]
            for j in range(n):
                C[i][j] = (C[i][j] + aik * B[k][j]) % mod
    return C

This is O(N^3) with a check for zero. For sparse matrices, it helps, but F might be dense. We can also use the fact that we only need F^p, and p is up to 1e9, so we need about 30 squarings. 30 * 1e6 = 3e7 operations. In Python, 3e7 simple operations might be around 3-5 seconds, which is acceptable? We should optimize by using local variables and maybe list of lists.

Alternatively, we can use numpy? But we cannot rely on external libraries. We must implement in pure Python.

We can also note that N is only 100, so we can use the standard algorithm. To speed up, we can precompute the transpose of B to improve cache locality? Not necessary.

Another optimization: Since we are computing F^p, and F is the fixed matrix, we can exponentiate by squaring.

Now, the extra matrix E: we need to iterate over zeros (up to 10000) and then over N for each self-loop. That's O(K*N) = up to 1e6, fine.

Now, we need to handle the sign (-1)^K. K can be up to 10000. Compute sign = 1 if K even else p-1 (since -1 mod p = p-1).

Now, for p=2, we need to compute B^2 mod 2. B is A with zeros replaced by 1. So B_{ij} = 1 if A_{ij} == 0 else A_{ij} % 2. Since A_{ij} is 0 or 1, B is just 1-A? Actually, if A_{ij}=0, B_{ij}=1; if A_{ij}=1, B_{ij}=1. So B is all ones! Wait, in sample 2, A had 1 on diagonal and 0 off-diagonal. After replacing zeros with 1, B becomes all ones. But in general, A entries can be 0 or 1 (since p=2, values are 0 or 1). So B_{ij} = 1 if A_{ij}=0, else 1 (since A_{ij}=1). So B is the all-ones matrix? No, if A_{ij}=1, B_{ij}=1. If A_{ij}=0, B_{ij}=1. So yes, B is the all-ones matrix! Because for p=2, the only nonzero value is 1. So regardless of A, B is the matrix with 1 everywhere. Wait, is that true? The problem says each element of A is between 0 and p-1 inclusive. For p=2, that means 0 or 1. Nonzero values are only 1. So indeed, B is the matrix with all entries 1. Then B^2 is the matrix where each entry is the sum of N ones = N. Mod 2, N mod 2. So the answer is a matrix where every entry is N mod 2. But sample 2: N=3, N mod 2 = 1, so all ones. That matches. For N=4, p=2, A arbitrary, answer is all entries = 0 if N even, 1 if N odd. Let's check: B = J (all ones). B^2 = N * J. Mod 2, N mod 2. So yes, the answer is simply the matrix with all entries equal to N mod 2. That's a huge simplification for p=2! We don't need to compute B^2; we just output N mod 2 for all entries.

But wait, is that always true? B is all ones because every zero is replaced by 1, and every 1 stays 1. So B is indeed all ones. Then (B^2)_{ij} = Σ_k 1*1 = N. So mod 2, it's N mod 2. So for p=2, answer is simply N % 2 for all entries. That's O(1) after reading N.

Let's double-check with another p=2 case: N=2, p=2, A = [[0,0],[0,0]]. B = [[1,1],[1,1]]. B^2 = [[2,2],[2,2]] ≡ [[0,0],[0,0]] mod 2. N=2, N mod 2 = 0. Correct.
N=1, p=2, A=[0]. B=[1]. B^2=[1]. N=1, N mod 2 = 1. Correct.
So for p=2, the answer is trivially (N % 2) for all entries.

Thus, the algorithm is:
- If p == 2: print (N % 2) for all N*N entries.
- Else:
  - Compute K = number of zeros.
  - sign = 1 if K % 2 == 0 else p-1.
  - F = matrix with A_{ij} if A_{ij} != 0 else 0.
  - Compute P = F^p mod p using fast exponentiation.
  - E = zero matrix.
  - For each i,j with A_{ij} == 0:
    - If i == j:
      - For y in 0..N-1: if F[i][y] != 0: E[i][y] = (E[i][y] + F[i][y]) % p
      - For x in 0..N-1: if F[x][i] != 0: E[x][i] = (E[x][i] + F[x][i]) % p
    - Else if p == 3:
      - If F[j][i] != 0: E[i][j] = (E[i][j] + F[j][i]) % p
  - T = (P + E) % p.
  - S = (sign * T) % p.
  - Print S.

We should verify sample 3 with this code.

Let's manually compute a small part of sample 3 to ensure no mistake.
Sample 3: N=4, p=13.
A:
0 1 2 0
3 4 0 5
0 6 0 7
8 9 0 0

Zeros: (0,0), (0,3), (1,2), (2,0), (2,2), (3,2), (3,3) using 0-index.
K=7. sign = (-1)^7 = -1 mod 13 = 12.

F:
[0,1,2,0]
[3,4,0,5]
[0,6,0,7]
[8,9,0,0]

Compute F^13 mod 13. This is tedious by hand, but we can compute small powers? Maybe we can write a small script in mind? Not feasible. We'll trust the algorithm.

But let's test another small case to be sure.
Suppose N=2, p=5, A = [[0,0],[0,0]]. All zeros. K=4, sign=1.
F = zero matrix. F^5 = zero.
E: zeros: (0,0), (0,1), (1,0), (1,1).
Self-loops: (0,0): F[0][y] for y: F[0][0]=0, F[0][1]=0. So no. F[x][0]: F[0][0]=0, F[1][0]=0. So no.
(1,1): similarly no.
Non-self-loops: p=5 ≠ 3, so no.
Thus E=0. T=0. S=0. So answer is all zeros.
Let's check by brute force: B has 4^4=256 possibilities? Actually, each zero is 1..4, so 4^4=256 matrices. B^5 for each. Since F=0, B has no fixed entries. We need to sum B^5. Is it zero? For any B, B^5 is some matrix. Sum over all B? Since there is symmetry, likely zero. For example, B = all ones. B^5 = 2^4 * J? Actually, J^2 = 2J, J^5 = 2^4 J. Sum over all B? Not obviously zero. But our formula says zero. Let's test with a smaller case: N=1, p=5, A=[0]. B can be 1,2,3,4. B^5 = B by FLT. Sum = 1+2+3+4=10 ≡ 0 mod 5. So yes. For N=2, p=5, all zeros. Let's test a few B's. B = [[1,1],[1,1]]. B^5 = (2^4) J = 16 J. 16 mod 5 = 1. So B^5 = J. If we take B = [[1,2],[3,4]], compute B^5? Hard. But sum over all 4^4=256 matrices. The formula gave 0. Is that correct? Let's think: The sum over all B of B^p. For each entry (i,j), it's the sum over all B of a homogeneous polynomial of degree p. Since all entries are variables, the sum factors as product of sums over each variable of some power. For a monomial, each variable's exponent must be multiple of p-1=4 to survive. Total degree p=5. We need exponents e_v summing to 5, each e_v multiple of 4. The only way is one variable has 4, and the remaining 1? No, 1 is not multiple of 4. So no monomial survives. Thus total sum is 0. So correct.

Another test: N=2, p=5, A = [[1,0],[0,0]]. Zeros: (0,1), (1,0), (1,1). K=3, sign = -1 mod 5 = 4.
F = [[1,0],[0,0]].
F^5: F is idempotent? F^2 = F, so F^5 = F.
E: zeros:
(0,1): non-self, p=5≠3, no.
(1,0): non-self, no.
(1,1): self-loop at 1. F[1][y]: F[1][0]=0, F[1][1]=0. F[x][1]: F[0][1]=0, F[1][1]=0. So no.
E=0.
T = F = [[1,0],[0,0]].
S = 4 * T = [[4,0],[0,0]] mod 5.
So answer: row0: 4 0; row1: 0 0.
Let's verify by brute force for small p? p=5 is large, but we can try p=3 for similar.
N=2, p=3, A = [[1,0],[0,0]]. Zeros: (0,1), (1,0), (1,1). K=3, sign = -1 mod 3 = 2.
F = [[1,0],[0,0]].
F^3 = F.
E: (0,1): non-self, p=3. F[1][0]=0, so no.
(1,0): non-self, p=3. F[0][1]=0, no.
(1,1): self-loop. F[1][0]=0, F[1][1]=0; F[0][1]=0, F[1][1]=0. So no.
E=0.
T = [[1,0],[0,0]].
S = 2 * T = [[2,0],[0,0]] mod 3.
So answer: 2 0; 0 0.
Let's brute force p=3, N=2, A=[[1,0],[0,0]].
Variables: B_{0,1} ∈ {1,2}, B_{1,0} ∈ {1,2}, B_{1,1} ∈ {1,2}.
B = [[1, a], [b, c]].
Compute B^3. We can sum over a,b,c.
We can write a small program in mind? Maybe just trust.

Given the logic, the algorithm seems correct.

Now, we need to implement matrix exponentiation efficiently. Since N=100, we can store matrices as lists of lists. The multiplication function should be optimized.

Potential pitfalls:
- p can be up to 1e9, but p is prime. p=2 is handled separately.
- p=3 requires the extra E from non-self-loops.
- For p>3, non-self-loops give no E.
- Self-loops always give E as described.
- The sign (-1)^K: we can compute as 1 if K even else p-1.
- Modulo operations: ensure we mod after additions.
- When computing F^p, we need to handle the case where F is zero matrix (then F^p is zero).
- The exponentiation: while p > 0: if p & 1: res = res * F; F = F * F; p >>= 1.
- We need to copy matrices or create new ones to avoid aliasing.

Complexity: O(N^3 log p) for F^p, O(K N) for E. K ≤ N^2 = 10000, so O(N^3) total.

We should also consider p=1? The problem says p is a prime such that 1 ≤ p ≤ 10^9. So p can be 2,3,5,... p=2 is the only even prime. p=1 is not prime. So p>=2.

Edge case: p=2 handled separately.

Now, let's write the code.

We'll define:
def mat_mul(A, B, mod):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(n):
            aik = Ai[k]
            if aik:
                Bk = B[k]
                for j in range(n):
                    Ci[j] = (Ci[j] + aik * Bk[j]) % mod
    return C

def mat_pow(F, power, mod):
    n = len(F)
    # Initialize result as identity matrix
    res = [[0]*n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    while power > 0:
        if power & 1:
            res = mat_mul(res, F, mod)
        F = mat_mul(F, F, mod)
        power >>= 1
    return res

But wait: for p=2, we don't need mat_pow. For p>2, we compute F^p.

Now, constructing E:
n = N
E = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if A[i][j] == 0:
            if i == j:
                # self-loop
                for y in range(n):
                    if F[i][y] != 0:
                        E[i][y] = (E[i][y] + F[i][y]) % mod
                for x in range(n):
                    if F[x][i] != 0:
                        E[x][i] = (E[x][i] + F[x][i]) % mod
            elif p == 3:
                if F[j][i] != 0:
                    E[i][j] = (E[i][j] + F[j][i]) % mod

Note: F[j][i] is the entry at row j, col i. We need to be careful with indices.

Then T = (P + E) % mod.
S = (sign * T) % mod.
If sign is -1 mod p, we can compute sign = p-1 if K odd else 1.
Then for each i, j, print S[i][j] with spaces.

We should also ensure that for p=2, we output (N % 2) for all entries.

Let's test with sample 1:
N=2, p=3, A as above.
K=2, sign=1.
F^3 computed.
E: (0,0) self: F[0][1]=1 -> E[0][1]+=1. F[x][0]: none.
(1,0) non-self: p=3, F[0][1]=1 -> E[1][0] += 1.
E = [[0,1],[1,0]].
T = F^3 + E.
We computed F^3 = [[0,1],[0,2]].
T = [[0,2],[1,2]].
S = T.
Output matches.

Sample 2: p=2, N=3. N%2=1. Output all ones. Matches.

Sample 3: We need to run the code to verify, but it should match.

One more check: p=3, N=2, A = [[0,0],[0,0]]. All zeros. K=4, sign=1.
F = zero. F^3 = zero.
E: (0,0) self: F all zero, so no.
(0,1) non-self: p=3, F[1][0]=0, no.
(1,0) non-self: F[0][1]=0, no.
(1,1) self: no.
E=0. T=0. S=0. So answer zero matrix. Is that correct? Let's brute force: p=3, N=2, all zeros. B entries in {1,2}. B^3 sum over all 2^4=16 matrices. For each B, B^3 is some matrix. The sum should be zero because of symmetry? Let's test a simple one: B = [[1,1],[1,1]]. B^2 = [[2,2],[2,2]] ≡ [[-1,-1],[-1,-1]] mod 3. B^3 = B^2 * B = [[-1,-1],[-1,-1]] * [[1,1],[1,1]] = [[-2,-2],[-2,-2]] ≡ [[1,1],[1,1]] mod 3. So B^3 = J. Another B: [[1,1],[1,2]]. Compute? Hard. But likely sum is zero. Our formula says zero.

Another test: p=5, N=2, A = [[0,0],[0,1]]. One fixed entry (1,1)=1. K=3, sign = -1 mod 5 = 4.
F = [[0,0],[0,1]].
F^5: F is idempotent? F^2 = F, so F^5 = F.
E: zeros: (0,0), (0,1), (1,0).
(0,0) self: F[0][y]: F[0][0]=0, F[0][1]=0. F[x][0]: F[0][0]=0, F[1][0]=0. No.
(0,1) non-self: p=5≠3, no.
(1,0) non-self: no.
E=0. T = F = [[0,0],[0,1]].
S = 4 * T = [[0,0],[0,4]] mod 5.
So answer: row0: 0 0; row1: 0 4.
Let's test with brute force for p=5? Too large, but we can test p=3, N=2, A=[[0,0],[0,1]].
p=3, K=3, sign = 2 mod 3.
F = [[0,0],[0,1]].
F^3 = F.
E: (0,0) self: no. (0,1) non-self: p=3, F[1][0]=0, no. (1,0) non-self: F[0][1]=0, no.
E=0. T = F.
S = 2 * F = [[0,0],[0,2]].
So answer: 0 0; 0 2.
Now brute force p=3: variables: a=B00, b=B01, c=B10. B = [[a,b],[c,1]]. Sum over a,b,c ∈ {1,2}.
Compute B^3. We can compute symbolically? Let's do small program in head? Maybe trust.

Thus, the algorithm seems consistent.

Now, implement in Python.

We need to be careful with input reading. N can be up to 100, p up to 1e9.

Code structure:
import sys
def solve():
    input = sys.stdin.readline
    N, p = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(N)]
    if p == 2:
        val = N % 2
        for i in range(N):
            print(' '.join([str(val)] * N))
        return
    mod = p
    K = 0
    for i in range(N):
        for j in range(N):
            if A[i][j] == 0:
                K += 1
    sign = 1 if K % 2 == 0 else mod - 1
    # Build F
    F = [[A[i][j] if A[i][j] != 0 else 0 for j in range(N)] for i in range(N)]
    # Compute F^p
    P = mat_pow(F, p, mod)
    # Build E
    E = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if A[i][j] == 0:
                if i == j:
                    for y in range(N):
                        if F[i][y] != 0:
                            E[i][y] = (E[i][y] + F[i][y]) % mod
                    for x in range(N):
                        if F[x][i] != 0:
                            E[x][i] = (E[x][i] + F[x][i]) % mod
                elif p == 3:
                    if F[j][i] != 0:
                        E[i][j] = (E[i][j] + F[j][i]) % mod
    T = [[(P[i][j] + E[i][j]) % mod for j in range(N)] for i in range(N)]
    S = [[(sign * T[i][j]) % mod for j in range(N)] for i in range(N)]
    for i in range(N):
        print(' '.join(map(str, S[i])))

We need to define mat_pow and mat_mul. But note: p can be large, up to 1e9, so we need to exponentiate by p. The exponent is p, not a power of 2? Wait, we are computing F^p. p is the prime, which can be up to 1e9. So we are raising the matrix to the p-th power. So the exponent is p. We can use fast exponentiation with exponent p. That's O(log p) matrix multiplications. log2(1e9) ≈ 30. So 30 squarings. That's fine.

But wait: p is the prime modulus and also the exponent. So we are computing F^p mod p. Yes.

Now, the mat_pow function will take power = p. So while power > 0: if power & 1: res = res * F; F = F * F; power >>= 1.

Now, we need to be careful with the identity matrix. It should be I.

Now, let's test sample 3 with a mental run? Not possible. We'll trust.

One more check: For p=3, the non-self-loop extra E: we add F[j][i] to E[i][j]. This is for a zero at (i,j) with i≠j. The walk is i->j->i->j. The fixed step is (j,i). So the product is F[j][i]. So we add to E[i][j] the value F[j][i]. This matches our earlier manual: for zero (2,1), i=2,j=1, add F[1][2] to E[2][1]. Correct.

What about p=3 and a zero at (i,j) with i≠j, but F[j][i] is also a zero? Then no addition. That's fine.

What about p=3 and multiple zeros? E accumulates correctly.

Now, consider the case where p=3 and a self-loop zero. Our code adds F[i][y] and F[x][i]. This is correct.

Now, consider p>3 and a self-loop zero. Our code adds F[i][y] and F[x][i]. Is that correct? For p>3, a self-loop zero can be used p-1 times. The walks are: start at i, p-1 self-loops, then fixed step i->y; or fixed step x->i, then p-1 self-loops. Are there any other walks? For p>3, p-1 ≥ 4. The fixed step cannot be in the middle because then the vertex would change. So only the two ends. So correct.

Now, consider p=3 and a self-loop zero. The fixed step could be in the middle if it's a self-loop at i. But that contributes p * F[i][i] = 3 * F[i][i] ≡ 0 mod 3. So no need to add. Our code doesn't add it, which is correct.

Now, what about p=2? We handled separately.

Thus, the algorithm is complete.

One more thought: For p=3, the non-self-loop zero (i,j) with i≠j gives a walk i->j->i->j. But what if j=i? That's self-loop, handled separately. So i≠j is correct.

Now, is there any overlap between the extra walks and the F^p walks? The extra walks use exactly one variable, while F^p uses none. They are distinct, so we can simply add E to F^p.

Now, we must ensure that the sign is applied correctly. (-1)^K mod p. For K even, sign=1. For K odd, sign=p-1. Since p is odd,

## worker: Implement the solution in Python based on the deri
The solution exploits the fact that for prime \(p\), the sum \(\sum_{v=1}^{p-1} v^e \equiv 0 \pmod p\) unless \((p-1) \mid e\), in which case it equals \(-1\). In the expansion of \(B^p\) as a sum over walks of length \(p\), each monomial corresponds to a walk, and the sum over all \(B\) survives only if every zero position is used a multiple of \(p-1\) times. Since the walk length is \(p\), the only possibilities are walks using no zeros, or walks using exactly one zero position \(p-1\) times and one fixed step. Both cases contribute a factor \((-1)^K\) times the product of fixed entries along the walk. The total sum is therefore \((-1)^K (F^p + E)\), where \(F\) is the matrix of fixed entries, and \(E\) accounts for the walks that use exactly one zero. The extra matrix \(E\) is constructed as: for self-loop zeros at \((a,a)\), add \(F_{a,y}\) to \(E_{a,y}\) and \(F_{x,a}\) to \(E_{x,a}\); for \(p=3\) and non-self-loop zero \((a,b)\), add \(F_{b,a}\) to \(E_{a,b}\). The case \(p=2\) is trivial because the only nonzero value is \(1\), so \(B\) is the all-ones matrix and \(B^2 = N \cdot J\), giving all entries \(N \bmod 2\).
