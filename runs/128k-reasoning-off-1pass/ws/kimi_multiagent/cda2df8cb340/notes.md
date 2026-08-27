
## ideation
Core difficulty: N up to 2e5, A_i up to 1e7, so O(N^2) pair enumeration is impossible; need a divide-and-conquer / counting approach exploiting 2-adic structure of f (the odd part).

Key structural facts:
- f(x) = odd part of x.
- Parity split: odd+even = odd, so f(a+b) = a+b directly for mixed-parity pairs. odd+odd and even+even sums are even: f(a+b) = f((a+b)/2).
- This gives a recursion: S(A) = (sum over mixed pairs of a+b) + S(evens/2) + S(odds mapped (o+1)/2? careful). Actually for two odds o1,o2: f(o1+o2) = f((o1+o2)/2) where (o1+o2)/2 = (o1-1)/2 + (o2-1)/2 + 1. So define B_i = (o_i - 1)/2 for odds; then f(o1+o2) = f(B_i + B_j + 1). The "+1" shift complicates a clean recursion. Alternative: handle pairs (i<=j) including i=j; recursion must include self-pairs consistently.

Alternative cleaner viewpoint: group by t_i = v2(A_i), odd part o_i. Cross-group pairs (t_i != t_j): f = o_small_t + 2^{dt}*o_large_t — direct computable sums if we process groups in order with prefix sums over odd parts scaled by powers of 2. Within-group: need sum of f(o_i+o_j) over odd o's — same type of problem but now all odd; pair sums are even; f(o_i+o_j) = f((o_i+o_j)/2). Recursing on (o-1)/2 with a +1 shift, or on (o+1)/2 variants, needs care.

A robust route: recursive function solve(list of values) returning sum over i<=j of f(v_i+v_j):
- Split into evens E (values/2) and odds O.
- Mixed pairs contribute sum of (e+o) = |O|*sumE_vals + |E|*sumO_vals (using original values).
- Even-even pairs: recurse on E/2 (values halved) — f(2(x+y)) = f(x+y).
- Odd-odd pairs: f(o1+o2) = f((o1+o2)/2); (o1+o2)/2 = floor(o1/2)+floor(o2/2)+1. So recurse on values (o-1)/2 but with an extra +1 inside f's argument: f(x_i + x_j + 1). So we need a generalized recursion solve(list, c) = sum f(v_i + v_j + c)? The shift c may grow. Hmm: f(o1+o2) with o odd: write o = 2u+1, sum = 2(u1+u2+1), f = f(u1+u2+1). Then next level: parity of u1+u2+1 depends... this becomes sum of f over shifted sums; the shift stays 1? If we define g(list, s) = sum_{i<=j} f(v_i+v_j+s), recursion: split by parity of v. Mixed: v_e+v_o+s parity = parity(s+1)... depends on s parity. This is workable but fiddly.

Simpler: think bitwise. f(s) for s = a+b: answer sum over pairs of oddpart(a+b). Known technique: process by 2-adic valuation levels: total = sum over pairs (a+b) / 2^{v2(a+b)}. Equivalent: sum over k>=0 of [contribution]. Or: oddpart(s) = sum over odd d... Another angle: oddpart(s) = s / 2^{v2(s)}. We can compute sum over pairs by iterating on levels: at each level, pairs whose sum is still even get halved. Define process: current multiset of "values" representing (a+b) after dividing out 2s? Pairs evolve jointly — recursion on pairs is the D&C above.

Pitfalls:
- Including i=j pairs (diagonal): f(2A_i) = f(A_i). Recursion must handle i<=j, not just i<j.
- Mixed-pair direct sum must use original (unhalved) values at that recursion level, and the recursion transforms values correctly.
- The odd-odd "+1" shift: handle via generalized shift parameter s, where recursion branches: for shift s, split values by parity; mixed parity pairs: v_e + v_o + s has parity = 1 + s mod 2... wait v_e even, v_o odd => sum odd => +s gives parity (1+s)%2. If s is odd, mixed sums are even — they join recursion instead. So cases depend on s parity. Let's define F(values, s): sum_{i<=j} f(v_i+v_j+s). Parity of v_i+v_j+s: if s even: mixed pairs odd -> direct; EE and OO even -> recurse: EE: (v_i/2 + v_j/2 + s/2) -> F(E/2, s/2). OO: v_i=2u_i+1: sum+s = 2(u_i+u_j+1+s/2) -> F(U, 1+s/2). If s odd: EE: even+even+odd = odd -> direct sum of (v_i+v_j+s). OO: odd+odd+odd = odd -> direct. Mixed: even -> recurse: (v_e/2 + u_o + (s+1)/2)... v_e+v_o+s = 2(v_e/2 + u_o + (s+1)/2). So F(mixed pairs) = sum f of halved = treat as F over cross pairs with new shift — but cross-pair recursion (i from E, j from O) isn't the same form as F (which is pairs within one list). Need G(E, O, s) = sum_{i in E, j in O} f(e_i + o_j + s). More general two-list version. This is getting complex but still O(N log M) if implemented carefully with combined function H(X, Y, s) = sum_{i in X, j in Y} f(x_i + y_j + s), with X==Y meaning i<=j. Recursion on parity of s and parities of x, y. Depth O(log(max sum)) ~ 25 levels; each level processes each element once per node — total O(N log M) if we partition lists at each node. Memory/time fine in Python if iterative with lists? 2e5 * 25 = 5e6 operations — OK.

But maybe simpler: avoid shift entirely. Original problem has s=0, X=Y. f(o1+o2) for odds: = f((o1+o2)/2). Note (o1+o2)/2 = ceil(o1/2)+floor(o2/2)... Alternatively map odd o -> (o+1)/2: then (o1+1)/2 + (o2+1)/2 = (o1+o2)/2 + 1. Shift again. Or map o -> (o-1)/2 gives +1 shift. Unavoidable.

Alternative simpler approach: digit DP / counting by 2-adic valuation directly on original numbers: Sum over pairs f(a+b). Group numbers by (t, o). Cross t-groups: easy with sorted groups and prefix sums: for t1 < t2: contribution o1 + 2^{t2-t1} o1'? wait f = o1 + 2^{t2-t1} * o2 where o1 is from smaller t. Sum over pairs across groups: need sum over group pairs — number of distinct t values up to ~24 (since A_i <= 1e7 < 2^24). So t in 0..23. Pairs of groups: 24*24/2 ~ 276 group pairs; for each, cross sum = n2 * sum_o1 + 2^{dt} * n1 * sum_o2. O(1) per group pair. Within same t: need sum_{i<=j in group} f(o_i+o_j) with o odd, o <= 1e7. Recurse: for odd o's, f(o_i+o_j) = f((o_i+o_j)/2). Let m_i = (o_i - 1)/2 >= 0, then (o_i+o_j)/2 = m_i + m_j + 1. So need sum f(m_i + m_j + 1). Now define the problem with shift 1: P(list, s=1). Hmm still shift.

But note: f(m+1) where... maybe handle shift-1 problem directly: sum_{i<=j} f(m_i+m_j+1). Split m by parity: m even (m=2u): m_i+m_j+1 odd -> direct. m odd (m=2u+1): sum+1 = 2(u_i+u_j+1)+... m_i+m_j+1 = 2u_i+2u_j+3 odd -> direct! Wait: odd+odd+1 = odd. even+even+1 = odd. Only mixed parity: even+odd+1 = even -> f = f(u_e + u_o + 1). So shift-1 problem reduces to cross-parity pairs with shift 1: sum over e in Evens, o in Odds of f(u_e + u_o + 1) where u_e = m_e/2, u_o = (m_o-1)/2. Two-list shift-1 problem: H(X, Y) = sum f(x_i + y_j + 1). Split X, Y by parity: x+y+1 even iff x,y same parity. Same-parity pairs recurse (halving, shift stays 1: x=2u: x+y+1 with y=2v: 2(u+v)+1 odd — wait that's odd! x even, y even: x+y+1 odd -> direct. x odd, y odd: x+y+1 = 2u+2v+3 odd -> direct. Mixed: even -> f(u + v + 1) recurse. So H(X,Y) = direct sums for same-parity pairs + H(X_even_halved, Y_odd_halved) + H(X_odd_halved, Y_even_halved). Clean! Shift stays 1 forever. 

Similarly the base problem (shift 0): sum f(x_i+x_j): mixed parity direct; EE recurse shift 0; OO -> shift 1 cross... OO with shift 0: f(o1+o2) = f(m1+m2+1) — that's the shift-1 same-list problem P1(list of m's). And P1(list) = direct for same-parity pairs + cross H between halved evens and halved odds with shift 1. And H(X,Y,shift1) recursion as above. So overall we need:
- F0(list): sum_{i<=j} f(a_i+a_j).
- F1(list): sum_{i<=j} f(a_i+a_j+1).
- H1(X, Y): sum_{i in X, j in Y} f(x_i+y_j+1) (all ordered cross pairs).
Recursions:
F0(A): E=evens, O=odds. = [sum_{e in E, o in O} (e+o)] + F0(E/2) + F1((O-1)/2).
F1(A): E=evens (a=2u), O=odds (a=2u+1). Same-parity pairs: a_i+a_j+1 odd -> direct: sum over i<=j within E of (a_i+a_j+1) + within O likewise. Cross: f(2u_e + 2u_o+1 + 1) = f(u_e+u_o+1) -> H1(U_E, U_O). Note cross pairs i in E, j in O all ordered (i<=j automatically across distinct sets). So F1(A) = directSameParity + H1(U_E, U_O).
H1(X, Y): split X into XE, XO; Y into YE, YO. Same-parity cross pairs: x+y+1 odd -> direct sums. Mixed: H1(XE/2, YO') + H1(XO', YE/2) where XO' = (x-1)/2 etc.
Termination: when a list is empty -> 0. Values shrink each recursion (halving), depth <= ~25. But F0(E/2) keeps values halving; also lists can contain 0 (m = (o-1)/2 can be 0 when o=1). f(0+0+1)=f(1)=1 fine. In F0, values stay >= 1? E/2 could be... A_i >= 1, evens >= 2, E/2 >= 1. OK. In F1/H1, zeros appear; f(0+0+1) = 1 fine; parity of 0 is even; recursion: XE/2 = 0 stays 0 — infinite loop if all zeros! E.g., H1([0],[0]): x+y+1 = 1 odd -> direct, no recursion. F1([0]): same parity direct. F0 with zeros never happens. H1 recursion only on mixed-parity pairs; values halve each time; if XE = [0] and YO = [1]: H1([0],[0])? (1-1)/2 = 0. H1([0],[0]) -> direct (same parity). Terminates because mixed-parity requires at least one odd value >= 1, halving strictly reduces max. Max value strictly decreases in recursive calls (odds >= 1 become (o-1)/2 < o; evens halved, if even=0 it stays 0 but then it's in XE and paired with YO which shrinks). Depth O(log max). Good.

Complexity: each recursion level partitions lists; total element processing O(N * depth) = 2e5 * 25 = 5e6 — fine in Python with list comprehensions, though constant factors matter. Use iterative or recursive with lists; recursion depth of call tree is O(log M) ~ 25 deep but branching — total nodes O(N log M) worst? Each element participates in one node per level along its path; total work O(N log M). Fine.

Direct sum formulas:
- Cross direct (different lists X, Y, shift s): sum_{x,y} (x+y+s) = |Y|*sumX + |X|*sumY + |X|*|Y|*s.
- Same-list direct i<=j with shift s: sum_{i<=j} (a_i+a_j+s) = sum_i (i-th...) formula: sum_{i<=j}(a_i+a_j) = (n+1)*sum(a)? Check: sum_{i<=j} (a_i + a_j) = sum_i a_i*(count of j>=i) + sum_j a_j*(count of i<=j) = sum_i a_i*(n-i) + sum_j a_j*j (0-indexed j) = sum_i a_i*(n - i + i) = n*sum(a). Wait 0-indexed: for element at index i, as first element pairs with j=i..n-1: (n-i) times; as second with i'=0..i: (i+1) times. Total (n+1) times. So sum_{i<=j}(a_i+a_j) = (n+1)*sum(a). Plus s * n(n+1)/2. 

Also F0 diagonal: f(2a) = f(a) — recursion handles it naturally since pairs i<=j included in sub-lists.

Alternative much simpler implementation: recursive function solve(vals, s) handling same-list with shift s in {0,1}, plus cross helper. But cross H1 needs two-list recursion anyway. Could unify: general function cross(X, Y, s) for two lists (all pairs), and same-list via... same-list isn't cross of list with itself (that double counts i!=j and includes i=j once — actually cross(A,A) ordered = 2*sum_{i<j} + sum_i f(2a_i + s); sum_{i<=j} = (cross(A,A) + sum_i f(2a_i+s))/2 — messy). Keep separate functions.

Let me double check F1 same-parity direct: F1(A): pairs i<=j both in E: a_i+a_j+1 = even+even+1 = odd -> f = value. Both in O: odd+odd+1 = odd -> direct. Cross E-O: even+odd+1 = even -> f((2u_e + 2u_o+1+1)/2) = f(u_e+u_o+1). Yes H1(U_E, U_O).

H1(X,Y): pairs x in X, y in Y. x+y+1: x even,y even -> odd direct. x odd,y odd -> odd+odd+1 = odd direct. Mixed -> halve: x even (2u), y odd (2v+1): sum+1 = 2u+2v+2 = 2(u+v+1) -> f(u+v+1): H1(XE/2, YO'). Similarly H1(XO', YE/2). Good.

Now top-level: answer = F0(A). Check sample 1: A=[4,8]. E=[4,8], O=[]. F0 = 0 + F0([2,4]) + F1([]) = F0([2,4]) = F0([1,2]): E=[2], O=[1]: mixed direct: 2+1=3. + F0([1]) + F1([0]). F0([1]): E=[], O=[1]: mixed 0 + F0([]) + F1([0]). F1([0]): n=1, same parity direct: (n+1)*sum + s*n(n+1)/2 = 2*0 + 1*1 = 1. So F0([1]) = 1. F1([0]) = 1. Total: 3 + 1 + 1 = 5. ✓

Sample 2: A=[51,44,63]. E=[44], O=[51,63]. Mixed: 44+51 + 44+63 = 95+107=202. F0([22]): -> F0([11]) -> F1([5]): F1([5]): O=[5], same-parity direct: (1+1)*5 + 1*1 = 11. So F0([11])=11, F0([22])=11. F1([(51-1)/2, (63-1)/2]) = F1([25,31]): both odd: direct same parity: (n+1)*sum + n(n+1)/2 = 3*56 + 3 = 171. Total: 202 + 11 + 171 = 384. ✓ 

Implementation plan:
- Read N, list A.
- Define f0(vals), f1(vals), h1(X, Y) recursively with lists; use sys.setrecursionlimit high; depth ~ 60 max (values up to 2*10^7, halving ~25 times, but recursion chain f0 -> f0 -> ... depth ~25; branching fine).
- Each call: partition via list comprehensions; compute sums and counts; direct formulas.
- Use integers; answer up to ~ N^2 * 2e7 ~ 4e10 * 2e7 = 8e17 fits in Python int anyway.

Complexity concern: worst case all A_i odd -> F0(A) -> F1 of size N with values ~5e6, then F1 splits into H1 calls etc. Each level total elements across all nodes <= N (each element in exactly one node per level). Levels <= ~26. Total ops ~ 5-10 million — okay in Python (~2-4 s). Optimize: use local variables, avoid function call overhead where possible; maybe implement iteratively with a stack of tasks. Recursion with many small lists creates overhead but total elements bounded.

Edge cases: N=1. Values 0 in F1/H1 handled. Empty lists return 0.

One more check on H1 termination with zeros: H1(X,Y) where X=[0], Y=[2]: same parity (both even) -> direct. X=[0], Y=[1]: mixed -> H1([0],[0]) -> direct. Fine.

Also f0 with vals containing zeros? Only if called with E/2 where E contains 0 — E comes from evens of A (>=2) or evens of previous f0 lists (>=1 values; even values >=2 -> /2 >= 1). So no zeros in F0. Good.

Now write code.

def solve():
    import sys
    sys.setrecursionlimit(1000000)
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); A = list(map(int, data[1:1+n]))
    
    def f0(vals):
        if not vals: return 0
        E = []; O = []
        for v in vals:
            if v & 1: O.append(v)
            else: E.append(v)
        total = 0
        if E and O:
            total += len(O)*sum(E) + len(E)*sum(O)
        if E:
            total += f0([v>>1 for v in E])
        if O:
            total += f1([(v-1)>>1 for v in O])
        return total
    
    def f1(vals):
        if not vals: return 0
        E = []; O = []
        for v in vals:
            if v & 1: O.append(v)
            else: E.append(v)
        total = 0
        nE = len(E); nO = len(O)
        if nE:
            sE = sum(E)
            total += (nE+1)*sE + nE*(nE+1)//2
        if nO:
            sO = sum(O)
            total += (nO+1)*sO + nO*(nO+1)//2
        if E and O:
            UE = [v>>1 for v in E]
            UO = [(v-1)>>1 for v in O]
            total += h1(UE, UO)
        return total
    
    def h1(X, Y):
        if not X or not Y: return 0
        XE=[];XO=[];YE=[];YO=[]
        for v in X:
            if v&1: XO.append(v)
            else: XE.append(v)
        for v in Y:
            if v&1: YO.append(v)
            else: YE.append(v)
        total = 0
        # same parity direct: XE-YE, XO-YO with shift 1
        if XE and YE:
            total += len(YE)*sum(XE) + len(XE)*sum(YE) + len(XE)*len(YE)
        if XO and YO:
            total += len(YO)*sum(XO) + len(XO)*sum(YO) + len(XO)*len(YO)
        if XE and YO:
            total += h1([v>>1 for v in XE], [(v-1)>>1 for v in YO])
        if XO and YE:
            total += h1([(v-1)>>1 for v in XO], [v>>1 for v in YE])
        return total
    
    print(f0(A))

Wait — check f1 same-parity direct formula: sum_{i<=j} (a_i + a_j + 1) = (n+1)*sum(a) + n(n+1)/2. Yes.

Check h1 direct: sum_{x in X, y in Y} (x + y + 1) = |Y|*sumX + |X|*sumY + |X|*|Y|. Yes.

Recursion depth: f0 chain depth ~24 (A <= 1e7). f1/h1 similar. Total depth could be ~50. setrecursionlimit safe.

Performance: worst case all odd -> f0 partitions once, calls f1 with N elements; f1 splits into E/O and calls h1 on subsets; h1 recursion: each element per level. Total ~ N * 2 * 25 operations with list building. Should run in ~2-5s. Might optimize inner loops with comprehensions:

E = [v for v in vals if not v&1]; O = [v for v in vals if v&1] — two passes; or single loop. Fine.

Potential worst case: h1 branching creates many nodes; each level each element appears in at most one sub-call per branch — in h1, XE goes to one call, XO to another; so per level each element in exactly one node. Depth <= ~25. Total element-processings <= 25N per top call. Good.

Let me verify sample 2 mentally already done = 384 ✓. Sample 1 = 5 ✓.

Also verify f0 mixed uses original values (not halved): yes, f(e+o) = e+o since odd.

Double-check f0 odd-odd: f(o1+o2) = f((o1+o2)/2), (o1+o2)/2 = (o1-1)/2 + (o2-1)/2 + 1. So f0's odd part -> f1 over (o-1)/2. ✓.

Check diagonal in f1: i=j: 2a_i+1 odd always -> direct; formula includes i=j: (n+1)*sum includes each element... for i=j term: 2a_i + 1. Sum over i: 2*sum + n. And i<j terms: each pair a_i+a_j+1. Total = sum_{i<j}(a_i+a_j) + 2sum + n + (n choose 2)... let's verify formula: (n+1)*sum + n(n+1)/2. n=2, a=[1,3]: pairs: (1,1):3, (1,3):5, (3,3):7 total 15. Formula: 3*4 + 3 = 15 ✓.

Now confirm no integer overflow issues — Python arbitrary precision.

I think solution is correct. Write final code with fast I/O. Also micro-optimize: avoid recomputing sums via built-in sum. Use sys.stdout.write.

One concern: recursion with many small lists — number of nodes could blow up? Each node does O(size) work; total O(N log M). Node count also O(N log M) worst? Each node with k elements spawns <= 2 children covering <= k elements; leaves are empty lists (pruned: we check `if E and O` etc. before recursing, and base case empty returns). Node count O(total work). Fine.

Also handle input where N and list on same/different lines — reading all tokens handles it.

## worker: Implement the full solution in Python: recursive f
- f(x) is the odd part of x. The answer is F0(A) = Σ_{i≤j} f(A_i + A_j).
- Three mutually recursive functions, all based on parity splitting:
  - **f0(vals)**: mixed-parity pairs give odd sums → contribute their value directly (|O|·ΣE + |E|·ΣO). Even-even: f(2x+2y)=f(x+y) → recurse f0 on halved evens. Odd-odd: f((2u+1)+(2w+1)) = f(u+w+1) → recurse f1 on (o−1)/2.
  - **f1(vals)** (shift +1, pairs i≤j): same-parity pairs give odd sums → direct via Σ_{i≤j}(a_i+a_j+1) = (n+1)·Σa + n(n+1)/2. Mixed pairs: (2u)+(2w+1)+1 = 2(u+w+1) → h1 on halved lists.
  - **h1(X,Y)** (cross pairs, shift +1): same-parity cross pairs are odd → direct via |Y|·ΣX + |X|·ΣY + |X|·|Y|. Mixed cross pairs recurse with halving; the shift stays 1 forever.
- Termination: recursive calls only involve halved values (max strictly decreases when any odd ≥1 exists; zeros only occur in same-parity/direct branches). Depth ≤ ~25 since A_i ≤ 10^7 < 2^24.
- Complexity: each element appears in exactly one node per recursion level → O(N log maxA) ≈ 5×10^6 element operations.
- Verified by hand:
  - Sample 1 ([4,8]): mixed 3 + f0([1])=1 + f1([0])=1 → 5 ✓
  - Sample 2 ([51,44,63]): mixed 202 + f0([22])=11 + f1([25,31])=171 → 384 ✓
- Diagonal pairs i=j are handled correctly: in f0, f(2a)=f(a) via recursion; direct-sum formulas use the (n+1)·Σa identity which counts each element n+1 times across all i≤j pairs.

## worker: Verify the implementation logic against samples an
Hand-verification of the implementation:

**Sample 1: A=[4,8] → 5**
- f0([4,8]): E=[4,8], O=[]. → f0([2,4])
- f0([2,4]): E=[2,4], O=[]. → f0([1,2])
- f0([1,2]): E=[2], O=[1]. Mixed: 1·2 + 1·1 = 3. f0([1]) + f1([0]).
  - f0([1]): O=[1] → f1([0]).
  - f1([0]): nE=1, sE=0 → (1+1)·0 + 1·2//2 = 1. ✓ (f(0+0+1)=f(1)=1)
- Total: 3 + 1 + 1 = 5 ✓

**Sample 2: A=[51,44,63] → 384**
- f0: E=[44], O=[51,63]. Mixed: 2·44 + 1·114 = 202.
- f0([22]) → f0([11]) → f1([5]): nO=1, sO=5 → 2·5+1 = 11 ✓ (f(22+22)=f(44)=11)
- f1([25,31]): both odd, nO=2, sO=56 → 3·56 + 3 = 171. Check directly: f(51+51)=f(102)=51, f(51+63)=f(114)=57, f(63+63)=f(126)=63 → 51+57+63=171 ✓
- Total: 202+11+171 = 384 ✓

**N=1, A=[1]**: f0([1]) → f1([0]) → 1. Correct: f(1+1)=f(2)=1 ✓

**All-even A=[2,4]**: f0→f0([1,2]): mixed 3, f0([1])=1, f1([0])=1 → 5. Direct: f(4)=1, f(6)=3, f(8)=1 → 5 ✓

**All-odd A=[1,3]**: f0 → f1([0,1]): E=[0]→1, O=[1]→(2·1+1)=3, h1([0],[0]): same parity direct: 1·0+1·0+1=1. Total 1+3+1=5. Direct: f(2)=1, f(4)=1, f(6)=3 → 5 ✓

**Zeros in f1/h1**: value 0 is even; in f1 same-parity branch it's handled directly (no recursion on it); in h1, 0 only recurses when paired with an odd ≥1, which strictly shrinks ((o−1)/2 < o). Termination guaranteed; recursion depth ≤ ~25 since A_i ≤ 10⁷ < 2²⁴.

**Direct-sum formulas**: Σ_{i≤j}(a_i+a_j+s) = (n+1)·Σa + s·n(n+1)/2 (each element appears n+1 times across i≤j pairs — verified n=2 above). Cross: Σ(x+y+1) = |Y|ΣX + |X|ΣY + |X||Y| ✓.

Complexity: O(N log maxA) ≈ 5×10⁶ element operations; Python ints unbounded.
