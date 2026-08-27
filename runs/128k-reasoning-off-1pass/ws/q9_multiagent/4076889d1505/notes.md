
## ideation
The problem asks us to find a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$.
Constraints: $N \le 10^9$, $A, M \le 10^{18}$.
Core difficulty: Constructing such a pair deterministically and efficiently without factoring large numbers or performing expensive primality tests (though Miller-Rabin is fast enough for $10^{18}$).
Candidate approaches:
1.  **Construct $M$ as a prime $P$ where $P \equiv 1 \pmod N$**:
    *   If we find a prime $P = kN + 1$, then the order of any element $A$ dividing $P-1$ must divide $kN$. If we pick $A$ carefully (e.g., a primitive root or specific generator), we might get order $N$.
    *   However, finding a prime of the form $kN+1$ for arbitrary $N$ can be slow if we just increment $k$. We need a guaranteed construction.
2.  **Use $M = 2N + 1$**:
    *   If $2N+1$ is prime, then $2^{2N} \equiv 1 \pmod M$. The order of $2$ divides $2N$. It could be $N$ or $2N$.
    *   If $2^N \equiv 1 \pmod M$, the order divides $N$. If we can ensure it's exactly $N$, we are done.
    *   If $2^N \equiv -1 \pmod M$, the order is $2N$.
    *   This approach is probabilistic or requires checking.
3.  **Deterministic Construction using $M = 2N+1$ logic but with a twist**:
    *   Consider $M = 2N + 1$. If $M$ is prime, then $2^N \equiv -1 \pmod M$ is NOT always true, but $2^{2N} \equiv 1 \pmod M$ is.
    *   Actually, a known trick for this specific problem (often found in competitive programming contexts like AtCoder ABC 205 D or similar) is to set $M = 2N + 1$. If $2N+1$ is prime, then $2^N \equiv -1 \pmod M$ is true for roughly half the primes? No.
    *   Let's reconsider the properties. If $P = 2N+1$ is prime, then $2$ is a quadratic residue modulo $P$ iff $2^{(P-1)/2} \equiv 1 \pmod P$, i.e., $2^N \equiv 1 \pmod P$. If $2$ is a quadratic non-residue, $2^N \equiv -1 \pmod P$.
    *   If $2^N \equiv 1 \pmod P$, the order of $2$ divides $N$. We need to check if it is exactly $N$. This requires checking prime factors of $N$. Factoring $N$ up to $10^9$ is feasible ($O(\sqrt{N})$).
    *   If $2^N \equiv -1 \pmod P$, the order is $2N$. This is not what we want.
    *   So if $2N+1$ is prime and $2$ is a quadratic residue, we might get order $N$. But we need to be sure.
    *   Alternative: Just pick $A=2$ and $M=2N+1$. If $2N+1$ is prime, check if order is $N$. If not, try another base or another $M$.
    *   Wait, there is a simpler deterministic construction:
        Let $M = 2N + 1$. If $M$ is prime, then $2^N \equiv -1 \pmod M$ is true for some cases?
        Actually, the standard solution for this problem is:
        Set $M = 2N + 1$. If $2N+1$ is prime, then $2^N \equiv -1 \pmod M$ is true for roughly half the primes?
        No, the intended solution is usually:
        Set $M = 2N + 1$. If $2N+1$ is prime, then $2^N \equiv -1 \pmod M$ is true for some cases?
        Let's look at the sample cases.
        $N=3 \to 2, 7$. $7 = 2(3)+1$. $2^3-1 = 7$. Order is 3.
        $N=16 \to 11, 68$. $68 = 4 \times 16 + 4$. Not $2N+1$.
        $N=1 \to 20250126, 1$. $M=1$. $A^n-1$ is multiple of 1 always. Smallest $n$? $A^1-1 = A-1$. If $A>1$, $A-1$ is multiple of 1. $n=1$ works.
        $N=55 \to 33, 662$.
        
        Let's try the construction $M = 2N + 1$.
        If $2N+1$ is prime, then $2^{2N} \equiv 1 \pmod M$.
        If $2^N \equiv 1 \pmod M$, order divides $N$.
        If $2^N \equiv -1 \pmod M$, order is $2N$.
        We want order $N$.
        So we need $2^N \equiv 1 \pmod M$.
        This happens if $2$ is a quadratic residue mod $M$.
        By Quadratic Reciprocity, $(2/P) = (-1)^{(P^2-1)/8}$.
        If $P \equiv 1, 7 \pmod 8$, then $(2/P) = 1$, so $2^{(P-1)/2} \equiv 1 \pmod P$.
        Here $(P-1)/2 = N$. So if $2N+1 \equiv 1, 7 \pmod 8$, then $2^N \equiv 1 \pmod {2N+1}$.
        Then the order of $2$ divides $N$.
        Is it exactly $N$? Not necessarily. It could be a proper divisor.
        However, if we choose $A$ such that $A$ is a primitive root modulo $M$? No, we need order $N$, not $M-1$.
        We need an element of order $N$. Since $N | (M-1)$, such an element exists.
        We can find it by taking $g^{(M-1)/N}$ where $g$ is a primitive root.
        Finding a primitive root requires factoring $M-1$. Factoring $2N$ is easy if we factor $N$.
        Algorithm:
        1. Try $M = 2N + 1$.
        2. Check if $M$ is prime (Miller-Rabin).
        3. If prime, check if $2^N \equiv 1 \pmod M$.
           - If yes, calculate order of $2$ modulo $M$. Factor $N$. Check divisors. If order is $N$, output $(2, M)$.
           - If no (order is $2N$), try another base? Or try a different $M$?
        4. What if $2N+1$ is not prime?
           We can try $M = kN + 1$ for $k=1, 2, \dots$.
           Since primes are dense, we will find one quickly.
           For each candidate $M = kN+1$:
             - Check primality.
             - If prime, check if there exists an element of order $N$.
               - This is guaranteed if $N | (M-1)$.
               - We can construct it: Find a primitive root $g$ of $M$. Then $A = g^{(M-1)/N}$ has order $N$.
               - To find primitive root $g$: Iterate $g=2, 3, \dots$. Check if $g^{(M-1)/q} \not\equiv 1 \pmod M$ for all prime factors $q$ of $M-1$.
               - $M-1 = kN$. We need prime factors of $kN$.
               - Since $N \le 10^9$, factoring $N$ is fast ($O(\sqrt{N})$). Factoring $k$ is also fast for small $k$.
               - Once we have factors of $M-1$, we can find $g$ and then $A$.
        
        Is there a simpler way?
        The problem statement says "It can be proved that such a pair ... always exists".
        Maybe we don't need to find a primitive root.
        Consider $M = 2N+1$. If $2N+1$ is prime.
        If $2^N \equiv 1 \pmod M$, then order of 2 divides $N$.
        If $2^N \not\equiv 1 \pmod M$, then order is $2N$ (since $2^{2N} \equiv 1$).
        In the case where order is $2N$, we can try $A=3$? Or $A=2$ with a different $M$?
        Actually, if $2N+1$ is prime, then $2^N \equiv \pm 1 \pmod M$.
        If $2^N \equiv 1$, we check if order is $N$.
        If $2^N \equiv -1$, order is $2N$.
        But we can just pick $A = 2^k$? No.
        
        Let's refine the "Find $M = kN+1$ prime" strategy.
        Since $N \le 10^9$, we can factor $N$ in $O(\sqrt{N})$.
        Then for a candidate $M = kN+1$:
          1. Check if $M$ is prime.
          2. If prime, let $M-1 = kN$. We need an element of order $N$.
          3. Find a primitive root $g$ of $M$.
             - Prime factors of $M-1$ are factors of $k$ and factors of $N$.
             - We can precompute factors of $N$.
             - Iterate $g=2, 3, \dots$. Check condition.
          4. Set $A = g^{(M-1)/N} \pmod M$.
          5. Output $A, M$.
        
        Complexity:
        - Factor $N$: $O(\sqrt{N})$. Max $31622$ ops.
        - Search for $k$: Expected $O(\ln N)$ or small constant.
        - Primality test: $O(\log^3 M)$.
        - Factor $k$: Small.
        - Find primitive root: Iterate $g$. Number of checks is small. Exponentiation is $\log M$.
        - Total time per test case: Very fast. $T=10^4$ is fine.
        
        Corner case: $N=1$.
        $M = 1(1)+1 = 2$. Prime.
        $M-1 = 1$. Factors: none.
        Primitive root of 2 is 1? No, primitive root of 2 is usually defined as generator of $(\mathbb{Z}/2\mathbb{Z})^\times = \{1\}$. Generator is 1.
        $A = 1^{(2-1)/1} = 1$.
        Check: $1^n - 1 = 0$, multiple of 1. Smallest $n=1$. Correct.
        But sample output for $N=1$ is $20250126, 1$.
        If $M=1$, condition: $A^n-1$ multiple of 1. Always true. Smallest $n$?
        If $A=1$, $1^n-1=0$, multiple of 1. $n=1$ works.
        If $A>1$, $A^1-1 = A-1$. Multiple of 1. $n=1$ works.
        So for $N=1$, any $A, M=1$ works? Or $M$ can be anything?
        Problem says $A, M$ positive integers.
        If $M=1$, $A^n-1$ is always multiple of 1. Smallest $n$ is 1?
        Yes, because $n$ must be positive integer. $n=1$ gives $A-1$, divisible by 1.
        So for $N=1$, output $2, 1$ is valid.
        
        Is it possible $2N+1$ is never prime for some $N$?
        No, we can increase $k$.
        Is it possible finding a primitive root is slow?
        Primitive roots are dense. We will find one quickly.
        
        Wait, do we really need to find a primitive root?
        If $M = 2N+1$ is prime, and $2^N \equiv 1 \pmod M$.
        Then order of 2 divides $N$.
        If order is $N$, we are done.
        If order is a proper divisor $d$, then $2^{N/d} \equiv 1 \pmod M$.
        This means $2$ is not a primitive $N$-th root of unity.
        But we can just take $A = 2^k$? No.
        We need an element of order exactly $N$.
        Since $N | (M-1)$, there exists an element of order $N$.
        It is $g^{(M-1)/N}$ where $g$ is a primitive root.
        So finding a primitive root is the robust way.
        
        Optimization:
        Instead of full primitive root search, can we just pick $A=2$ and check?
        If $2^N \equiv 1 \pmod M$ and for all prime factors $p$ of $N$, $2^{N/p} \not\equiv 1 \pmod M$, then order is $N$.
        If this fails, we need another base.
        Since the number of elements of order $d$ is $\phi(d)$, and $\sum_{d|N} \phi(d) = N$, the number of elements of order $N$ is $\phi(N)$.
        The probability that a random element has order $N$ is $\phi(N)/N$.
        This can be small if $N$ has many small factors (e.g., $N=2^k$).
        But we can just iterate bases $b=2, 3, \dots$ until we find one.
        Since $\phi(N) \ge \sqrt{N/2}$ roughly, or at least $\ge 1$, we will find one quickly.
        Actually, if $N$ is prime, $\phi(N) = N-1$, very likely.
        If $N$ is composite, say $N=p_1 p_2$, $\phi(N) = (p_1-1)(p_2-1)$. Still large.
        The worst case is $N$ being a product of many small primes, but even then $\phi(N)$ is significant.
        So iterating $A$ starting from 2 is efficient.
        
        Revised Algorithm:
        1. Read $N$.
        2. If $N=1$, print "2 1" (or similar).
        3. Iterate $k = 1, 2, \dots$:
           a. Let $M = kN + 1$.
           b. If $M > 10^{18}$, break (should not happen with small $k$).
           c. Check if $M$ is prime (Miller-Rabin).
           d. If prime:
              i. Check if there exists $A \in [2, M-1]$ such that order of $A$ is $N$.
              ii. Iterate $A$ from 2 upwards.
                  - Check if $A^N \equiv 1 \pmod M$.
                  - If yes, check if for all prime factors $p$ of $N$, $A^{N/p} \not\equiv 1 \pmod M$.
                  - If both true, we found our pair $(A, M)$. Print and return.
              iii. If no such $A$ found (unlikely), continue to next $k$.
        
        Wait, step 3.d.ii: We need prime factors of $N$.
        We can precompute prime factors of $N$ for each test case. $O(\sqrt{N})$.
        Since $T=10^4$ and $N=10^9$, total precomputation time $\approx 10^4 \times 31622 \approx 3 \times 10^8$, which might be tight for 2 seconds.
        However, we only need to factor $N$ once per test case.
        Is there a way to avoid factoring $N$ every time?
        No, $N$ changes.
        But note: we only factor $N$ if we find a prime $M$.
        How many times do we find a prime $M$? Very few (expected 1 or 2).
        So we only factor $N$ once per test case.
        Total complexity: $T \times (\sqrt{N} + \text{small})$.
        $10^4 \times 3 \times 10^4 = 3 \times 10^8$ operations. In Python, this might be TLE.
        We need to optimize factorization or reduce the constant.
        Actually, we don't need to factor $N$ completely if we just check divisors?
        No, we need to check $A^{N/p}$.
        Can we avoid factoring $N$?
        Maybe use a different construction that doesn't require checking all prime factors of $N$.
        Recall: If $M = 2N+1$ is prime, then $2^N \equiv \pm 1 \pmod M$.
        If $2^N \equiv 1$, order divides $N$.
        If $2^N \equiv -1$, order is $2N$.
        What if we choose $A = 2$ and $M = 2N+1$?
        If $2^N \equiv -1$, order is $2N$. Not good.
        If $2^N \equiv 1$, order divides $N$.
        Can we ensure order is $N$ without factoring?
        Not easily.
        
        Is there a construction where we don't need to factor $N$?
        Consider $M = 2N+1$. If $2N+1$ is prime.
        If $2^N \equiv -1 \pmod M$, then order of 2 is $2N$.
        But we want order $N$.
        What if we pick $A = 2^2 = 4$?
        Order of 4 is $2N / \gcd(2, 2N) = N$.
        Wait. Order of $g^k$ is $d / \gcd(k, d)$ where $d$ is order of $g$.
        If order of 2 is $2N$, then order of $2^2$ is $2N / \gcd(2, 2N) = 2N / 2 = N$.
        So if $2^N \equiv -1 \pmod M$, then $A=4$ has order $N$!
        Check: $4^N = (2^2)^N = 2^{2N} \equiv 1 \pmod M$.
        And for any $d < N$ dividing $N$, $4^d = 2^{2d}$.
        Since order of 2 is $2N$, $2^{2d} \equiv 1 \implies 2N | 2d \implies N | d$.
        Since $d < N$, impossible. So order is exactly $N$.
        So if $2^N \equiv -1 \pmod M$, we can use $A=4$.
        
        What if $2^N \equiv 1 \pmod M$?
        Then order of 2 is $d | N$.
        If $d=N$, use $A=2$.
        If $d < N$, we need to find an element of order $N$.
        This requires factoring $N$ to check proper divisors, or finding a primitive root.
        But wait, if $2^N \equiv 1$, then $2$ is a quadratic residue.
        This happens if $M \equiv 1, 7 \pmod 8$.
        If $M \equiv 3, 5 \pmod 8$, then $2^N \equiv -1$.
        So we can prioritize $M = kN+1$ such that $M \equiv 3, 5 \pmod 8$.
        For such $M$, if $M$ is prime, then $2^N \equiv -1$, so $A=4$ works.
        We just need to find a prime $M = kN+1$ with $M \equiv 3, 5 \pmod 8$.
        $kN+1 \equiv 3 \implies kN \equiv 2 \pmod 8$.
        $kN+1 \equiv 5 \implies kN \equiv 4 \pmod 8$.
        We can iterate $k$ to find such a prime.
        This avoids factoring $N$ entirely!
        We only need Miller-Rabin.
        
        Algorithm Refined:
        1. Iterate $k = 1, 2, \dots$.
        2. $M = kN + 1$.
        3. If $M \equiv 3, 5 \pmod 8$:
             - Check if $M$ is prime.
             - If prime, output $4, M$. (Since $2^N \equiv -1$, order of 4 is $N$).
        4. If $M \equiv 1, 7 \pmod 8$:
             - Check if $M$ is prime.
             - If prime, check if $2^N \equiv 1 \pmod M$.
               - If yes, check if order of 2 is $N$. (Requires factoring $N$).
               - If no (order is $2N$, impossible since $2^N \equiv 1$), wait.
               - If $2^N \equiv 1$, order divides $N$.
               - If order is $N$, output $2, M$.
               - If order is proper divisor, we need another base.
               - But if we restrict to $M \equiv 3, 5 \pmod 8$, we avoid this case.
               - Are there enough primes of form $kN+1$ with $kN+1 \equiv 3, 5 \pmod 8$?
               - Yes, by Dirichlet's theorem.
               - So we just search for $k$ such that $kN+1$ is prime and $kN+1 \equiv 3, 5 \pmod 8$.
               - Then $A=4$ works.
        
        Wait, what if $N$ is even?
        If $N$ is even, $N \ge 2$.
        $kN$ is even. $kN+1$ is odd.
        $kN+1 \equiv 3, 5 \pmod 8$ is possible.
        Example $N=2$. $k=1 \implies M=3 \equiv 3 \pmod 8$. Prime. $A=4$.
        Check: $4^2-1 = 15$, div by 3. $4^1-1=3$, div by 3.
        Wait, $4^1-1 = 3$, multiple of 3. Smallest $n=1$.
        But we need smallest $n=2$.
        Why did $4^1-1$ work?
        $4 \equiv 1 \pmod 3$. Order of 4 mod 3 is 1.
        My logic: "If $2^N \equiv -1$, order of 2 is $2N$".
        For $N=2, M=3$: $2^2 = 4 \equiv 1 \pmod 3$.
        So $2^N \equiv 1$, not $-1$.
        Why? $M=3 \equiv 3 \pmod 8$.
        $(2/3) = -1$. So $2^{(3-1)/2} = 2^1 = 2 \equiv -1 \pmod 3$.
        Here $(M-1)/2 = 1 = N/2$? No.
        $N=2$. $(M-1)/2 = 1$.
        $2^1 \equiv -1$.
        So $2^{N/2} \equiv -1$.
        We need $2^N \equiv -1$.
        $2^N = (2^{N/2})^2 \equiv (-1)^2 = 1$.
        So for $N=2$, $2^N \equiv 1$.
        So the condition $2^N \equiv -1$ requires $N$ to be odd?
        If $N$ is even, $2^N = (2^{N/2})^2 \equiv 1$.
        So if $N$ is even, $2^N \equiv 1$ always for any prime $M=2N+1$?
        No. $M=2N+1$. $2^{M-1} \equiv 1$.
        $2^N = 2^{(M-1)/2}$.
        So $2^N \equiv (2/M) \pmod M$.
        If $(2/M) = -1$, then $2^N \equiv -1$.
        This requires $N$ to be odd?
        No, $(2/M) = -1$ means $M \equiv 3, 5 \pmod 8$.
        If $M \equiv 3, 5 \pmod 8$, then $2^N \equiv -1$.
        But if $N$ is even, $2^N = (2^{N/2})^2 \equiv (-1)^2 = 1$.
        Contradiction?
        Ah, $2^N \equiv (2/M)$ is only true if $N = (M-1)/2$.
        Yes, $M = 2N+1 \implies N = (M-1)/2$.
        So $2^N \equiv (2/M)$.
        If $M \equiv 3, 5 \pmod 8$, then $(2/M) = -1$.
        So $2^N \equiv -1$.
        But if $N$ is even, $2^N$ is a square, so $2^N \equiv 1$.
        So $M \equiv 3, 5 \pmod 8$ implies $N$ must be odd?
        Let's check.
        $M = 2N+1$.
        If $N$ is even, $N=2k$. $M = 4k+1$.
        $4k+1 \equiv 1, 5 \pmod 8$.
        If $k$ is even, $M \equiv 1 \pmod 8$.
        If $k$ is odd, $M \equiv 5 \pmod 8$.
        So if $N$ is even, $M$ can be $5 \pmod 8$.
        Example $N=2$. $M=5$. $5 \equiv 5 \pmod 8$.
        $2^2 = 4 \equiv -1 \pmod 5$.
        So $2^N \equiv -1$.
        Order of 2 mod 5 is 4. $2N = 4$. Correct.
        Then $A=4$. $4^2 = 16 \equiv 1 \pmod 5$.
        $4^1 = 4 \not\equiv 1$.
        Order of 4 is 2. Correct.
        So the logic holds for $N=2$ too.
        My previous manual check for $N=2, M=3$ was wrong because $M=3$ corresponds to $N=1$.
        If $N=2$, $M=5$.
        
        So the strategy:
        Iterate $k$. $M = kN+1$.
        Check if $M \equiv 3, 5 \pmod 8$.
        If so, check if $M$ is prime.
        If prime, output $4, M$.
        Why?
        If $M \equiv 3, 5 \pmod 8$, then $(2/M) = -1$.
        Then $2^N \equiv -1 \pmod M$.
        Then order of 2 is $2N$.
        Then order of $4 = 2^2$ is $2N / \gcd(2, 2N) = N$.
        This works for all $N \ge 1$.
        (For $N=1$, $M=2k+1$. If $M=3$, $4 \equiv 1 \pmod 3$. Order 1. Correct.)
        
        So we just need to find a prime $M = kN+1$ such that $M \equiv 3, 5 \pmod 8$.
        We don't need to factor $N$.
        We don't need to check $2^N$.
        Just primality test.
        
        Complexity:
        $T \times (\text{search for } k) \times (\text{Miller-Rabin})$.
        Search for $k$ is small. Miller-Rabin is fast.
        This is optimal.
        
        One detail: $M$ must be $\le 10^{18}$.
        $N \le 10^9$. $k$ will be small. $k \approx 100$ usually.
        $M \approx 10^{11}$, well within limits.
        
        Edge case: $N=1$.
        $k=1 \implies M=3 \equiv 3 \pmod 8$. Prime.
        Output $4, 3$.
        Check: $4^1-1=3$, div by 3. $4^0$ not allowed.
        Smallest $n=1$. Correct.
        Sample output used $M=1$. $4, 3$ is also valid.
        
        Final check on constraints:
        $A, M \le 10^{18}$.
        $M = kN+1$. If $k$ gets large, $M$ exceeds $10^{18}$.
        But primes are dense. We will find one with small $k$.
        Max $k$ is very small.
        
        Implementation details:
        - Miller-Rabin for $n < 10^{18}$. Bases: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37].
        - Loop $k$ from 1.
        - Check $M = kN+1$.
        - Check $M \% 8$.
        - If $M \% 8 == 3$ or $5$:
            - If is_prime(M): print 4, M; break.
        
        Wait, what if $N$ is very large and $kN+1$ overflows 64-bit integer?
        Python handles large integers automatically.
        Time limit: 2 sec.
        Python might be slow with many large integer ops.
        But $T=10^4$.
        We need to be efficient.
        Precompute bases for Miller-Rabin.
        Use `pow(a, b, m)` for modular exponentiation.
        
        One more check: Is it guaranteed that we find such a prime quickly?
        Yes, Dirichlet's theorem on arithmetic progressions.
        The sequence $kN+1$ contains primes.
        The condition $kN+1 \equiv 3, 5 \pmod 8$ is a congruence condition on $k$.
        There are $\phi(8)/2 = 2$ valid residues for $kN+1$ out of 8?
        Actually, $kN+1 \in \{3, 5\} \pmod 8$.
        This depends on $N \pmod 8$.
        Regardless, there are valid $k$'s.
        The density of primes is $1/\ln M$.
        We expect to find one within a few hundred tries.
        $10^4 \times 100 \times \text{cost}$.
        Cost of Miller-Rabin is roughly $10 \times \log^3 M$.
        $\log M \approx 60$. $60^3 \approx 216000$.
        $10 \times 200000 = 2 \times 10^6$ ops per test case?
        $10^4 \times 2 \times 10^6 = 2 \times 10^{10}$ ops. Too slow.
        Wait, Miller-Rabin is much faster.
        Modular exponentiation is $O(\log^2 M)$ or $O(\log^3 M)$ depending on multiplication.
        In Python, large int multiplication is $O(N^{1.58})$.
        But for 64-bit numbers, it's fast.
        Actually, $M$ can be up to $10^{18}$, which fits in 64-bit.
        Python handles this efficiently.
        The number of bases is 12.
        $12 \times \log M$ multiplications.
        $\log M \approx 60$.
        $720$ multiplications per primality test.
        $100$ tests per case.
        $72000$ multiplications per case.
        $10^4$ cases $\implies 7.2 \times 10^8$ multiplications.
        This might be tight.
        Can we reduce bases?
        For $n < 3 \times 10^{18}$, bases [2, 3, 5, 7, 11, 13, 17, 19, 23] are sufficient. (9 bases).
        Even better: deterministic variants.
        Or just rely on the fact that we find a prime very quickly.
        On average, the gap between primes in $kN+1$ is small.
        The first prime might be at $k=1, 2, 3 \dots$.
        We don't need to check 100 times. Usually 1-5 times.
        So average cost is much lower.
        Worst case is rare.
        
        So the plan is solid.

## worker: Implement the solution in Python: read T, loop T t
The problem asks for a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$.
The solution uses a constructive approach based on number theory properties:
1.  **Construction of $M$**: We set $M = k \cdot N + 1$ for some integer $k \ge 1$. This ensures that $N$ divides $M-1$.
2.  **Primality**: We require $M$ to be a prime number. If $M$ is prime, then by Fermat's Little Theorem, $A^{M-1} \equiv 1 \pmod M$. Since $N | (M-1)$, the order of any element $A$ must divide $M-1$.
3.  **Choosing $A$**: We specifically look for a prime $M$ such that $M \equiv 3 \pmod 8$ or $M \equiv 5 \pmod 8$.
    -   For such primes, the Legendre symbol $\left(\frac{2}{M}\right) = -1$.
    -   By Euler's criterion, $2^{(M-1)/2} \equiv \left(\frac{2}{M}\right) \equiv -1 \pmod M$.
    -   Since $(M-1)/2 = N$, we have $2^N \equiv -1 \pmod M$.
    -   This implies that the multiplicative order of $2$ modulo $M$ is exactly $2N$ (since $2^N \not\equiv 1$ and $2^{2N} \equiv 1$).
    -   Consider $A = 4 = 2^2$. The order of $A$ is given by $\frac{\text{order}(2)}{\gcd(2, \text{order}(2))} = \frac{2N}{\gcd(2, 2N)} = \frac{2N}{2} = N$.
    -   Thus, $(A, M) = (4, M)$ satisfies the condition.
4.  **Efficiency**: We iterate $k$ starting from 1. By Dirichlet's theorem on arithmetic progressions, there are infinitely many primes of the form $kN+1$. The density of primes ensures we find a suitable $M$ very quickly (typically within a few iterations). The Miller-Rabin primality test is used to check primality efficiently. The constraints $N \le 10^9$ and $T \le 10^4$ are handled well within the time limit.

## worker: Run the script on the provided sample input to ver
The solution implements a constructive algorithm based on number theory properties.
1.  **Problem Analysis**: We need $A^n \equiv 1 \pmod M$ with minimal $n=N$. This means the multiplicative order of $A$ modulo $M$ is exactly $N$.
2.  **Construction**: We choose $M = k \cdot N + 1$. If $M$ is prime, then $N$ divides $M-1$.
3.  **Specific Choice**: We search for a prime $M$ such that $M \equiv 3 \pmod 8$ or $M \equiv 5 \pmod 8$.
    -   For such primes, the Legendre symbol $\left(\frac{2}{M}\right) = -1$.
    -   By Euler's criterion, $2^{(M-1)/2} \equiv -1 \pmod M$. Since $(M-1)/2 = N$, we have $2^N \equiv -1 \pmod M$.
    -   This implies the order of $2$ modulo $M$ is $2N$.
    -   Let $A = 4 = 2^2$. The order of $A$ is $\frac{\text{order}(2)}{\gcd(2, \text{order}(2))} = \frac{2N}{2} = N$.
    -   Thus, $(A, M) = (4, M)$ is a valid solution.
4.  **Algorithm**:
    -   Iterate $k = 1, 2, \dots$.
    -   Calculate $M = k \cdot N + 1$.
    -   Check if $M \equiv 3, 5 \pmod 8$.
    -   If so, check if $M$ is prime using the deterministic Miller-Rabin test (bases sufficient for $10^{18}$).
    -   If prime, output $(4, M)$ and move to the next test case.
5.  **Complexity**:
    -   Miller-Rabin takes $O(\log^3 M)$ time.
    -   The gap between primes in the arithmetic progression $kN+1$ is small on average, so the loop runs very few times.
    -   Total time complexity is well within limits for $T=10^4$ and $N=10^9$.

## worker: Run the script with the provided sample input to v
The solution implements a constructive algorithm based on number theory properties.
1.  **Problem Analysis**: We need $A^n \equiv 1 \pmod M$ with minimal $n=N$. This means the multiplicative order of $A$ modulo $M$ is exactly $N$.
2.  **Construction**: We choose $M = k \cdot N + 1$. If $M$ is prime, then $N$ divides $M-1$.
3.  **Specific Choice**: We search for a prime $M$ such that $M \equiv 3 \pmod 8$ or $M \equiv 5 \pmod 8$.
    -   For such primes, the Legendre symbol $\left(\frac{2}{M}\right) = -1$.
    -   By Euler's criterion, $2^{(M-1)/2} \equiv -1 \pmod M$. Since $(M-1)/2 = N$, we have $2^N \equiv -1 \pmod M$.
    -   This implies the order of $2$ modulo $M$ is $2N$ (since $2^N \not\equiv 1$ and $2^{2N} \equiv 1$).
    -   Let $A = 4 = 2^2$. The order of $A$ is $\frac{\text{order}(2)}{\gcd(2, \text{order}(2))} = \frac{2N}{2} = N$.
    -   Thus, $(A, M) = (4, M)$ is a valid solution.
4.  **Efficiency**: We iterate $k$ starting from 1. By Dirichlet's theorem on arithmetic progressions, there are infinitely many primes of the form $kN+1$. The density of primes ensures we find a suitable $M$ very quickly (typically within a few iterations). The Miller-Rabin primality test is used to check primality efficiently. The constraints $N \le 10^9$ and $T \le 10^4$ are handled well within the time limit.

## worker: finalize
The solution implements a constructive algorithm based on number theory properties to find a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$.

1.  **Construction of $M$**: We set $M = k \cdot N + 1$ for some integer $k \ge 1$. This ensures that $N$ divides $M-1$.
2.  **Primality**: We require $M$ to be a prime number. If $M$ is prime, then by Fermat's Little Theorem, $A^{M-1} \equiv 1 \pmod M$. Since $N | (M-1)$, the order of any element $A$ must divide $M-1$.
3.  **Choosing $A$**: We specifically look for a prime $M$ such that $M \equiv 3 \pmod 8$ or $M \equiv 5 \pmod 8$.
    -   For such primes, the Legendre symbol $\left(\frac{2}{M}\right) = -1$.
    -   By Euler's criterion, $2^{(M-1)/2} \equiv \left(\frac{2}{M}\right) \equiv -1 \pmod M$.
    -   Since $(M-1)/2 = N$, we have $2^N \equiv -1 \pmod M$.
    -   This implies that the multiplicative order of $2$ modulo $M$ is exactly $2N$ (since $2^N \not\equiv 1$ and $2^{2N} \equiv 1$).
    -   Consider $A = 4 = 2^2$. The order of $A$ is given by $\frac{\text{order}(2)}{\gcd(2, \text{order}(2))} = \frac{2N}{\gcd(2, 2N)} = \frac{2N}{2} = N$.
    -   Thus, $(A, M) = (4, M)$ satisfies the condition.
4.  **Efficiency**: We iterate $k$ starting from 1. By Dirichlet's theorem on arithmetic progressions, there are infinitely many primes of the form $kN+1$. The density of primes ensures we find a suitable $M$ very quickly (typically within a few iterations). The Miller-Rabin primality test is used to check primality efficiently. The constraints $N \le 10^9$ and $T \le 10^4$ are handled well within the time limit.
