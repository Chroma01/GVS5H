The problem requires finding a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$. A simple and robust construction is to choose $M$ as a prime number $p$ such that $p-1$ is a multiple of $N$. Then, if we can find an $A$ such that $A^N \equiv 1 \pmod p$ and no smaller power works, we are done. However, a much simpler construction exists: let $M = 2N + 1$ (if prime) or more generally, we can construct $M$ based on the properties of cyclotomic polynomials or simply use the fact that if we pick $A=2$, we need an $M$ where the order is $N$.
Actually, the most direct constructive proof for this specific problem (which appeared in a contest like AtCoder ABC 213 Problem E or similar variations) relies on choosing $M$ such that $M$ divides $A^N - 1$ but not $A^k - 1$ for $k < N$.
A standard solution strategy is:
1. If $N=1$, we can output $(2, 1)$ since $2^1-1=1$ is divisible by 1, and no $n<1$ exists.
2. For $N > 1$, we can choose $A = 2$. We need an $M$ such that the order of 2 mod $M$ is $N$.
   A reliable way is to set $M = 2N + 1$ if it is prime? Not necessarily.
   Let's reconsider the simplest algebraic construction:
   We know that $x^N - 1 = \prod_{d|N} \Phi_d(x)$.
   If we choose $A$ such that $A$ is a primitive root modulo some prime $p$ where $p-1 = k \cdot N$, the order is $N$ if $N | p-1$.
   However, there is a specific trick used in competitive programming for this exact problem statement (AtCoder ABC 213 D? No, it's likely a specific construction problem).
   Let's look at the sample cases:
   N=3 -> 2 7. Order of 2 mod 7 is 3 ($2^1=2, 2^2=4, 2^3=1$). Note $7 = 2*3 + 1$.
   N=16 -> 11 68. $11^{16} \equiv 1 \pmod{68}$. $68 = 4 \times 17$. Order of 11 mod 17 is 16 ($17-1=16$). Order of 11 mod 4 is 2. LCM(16, 2) = 16.
   N=1 -> 20250126 1. Order mod 1 is undefined/trivial, but condition holds vacuously or by definition $n=1$ is smallest.
   N=55 -> 33 662.
   
   General Strategy:
   We can construct $M$ as a product of primes $p_i$ such that the order of $A$ modulo each $p_i$ divides $N$, and the LCM of these orders is exactly $N$.
   Simpler approach found in similar problems:
   Choose $A = 2$.
   We need $M$ such that ord_M(2) = N.
   If we pick a prime $p$ such that $p = k \cdot N + 1$ and 2 is a primitive root mod $p$ (or has order $N$), then $M=p$ works. But finding such primes is hard.
   
   Alternative Construction:
   Let $M = 2N + 1$. If $2N+1$ is prime, does 2 have order $N$? Not necessarily.
   
   Let's try the construction: $A = 2$, $M = 2N + 1$? No.
   How about $A = 2$, $M = 2^N - 1$? No, order is $N$ only if $2^N-1$ is prime (Mersenne) or specific factors.
   
   Correct known construction for this problem (AtCoder ABC 213 Problem E is different, this looks like **ABC 213 Problem D** is not it, maybe **ABC 213 Problem F**? No. It is **AtCoder Beginner Contest 213 Problem E**? No. It is **AtCoder Beginner Contest 213 Problem D**? No.
   Actually, this is **AtCoder Beginner Contest 213 Problem E** is "Sum of gcd".
   Wait, the problem is **AtCoder Beginner Contest 213 Problem D**? No.
   It is **AtCoder Beginner Contest 213 Problem C**? No.
   It is **AtCoder Beginner Contest 213 Problem B**? No.
   
   Let's re-evaluate the math directly.
   We need $A^N \equiv 1 \pmod M$ and $A^k \not\equiv 1 \pmod M$ for $k < N$.
   Let's choose $M = 2N + 1$. If $2N+1$ is prime, let $g$ be a primitive root. Then $g^N \equiv -1$ or $1$?
   
   Let's try the construction from the sample logic:
   Case 1: N=3, A=2, M=7. $7 = 2*3+1$. Order of 2 mod 7 is 3.
   Case 2: N=16, A=11, M=68. $68 = 4 * 17$. Order of 11 mod 17 is 16. Order of 11 mod 4 is 2. LCM(16, 2) = 16.
   Case 3: N=1, A=..., M=1.
   Case 4: N=55, A=33, M=662. $662 = 2 * 331$. 331 is prime? $331-1 = 330 = 6*55$. Order of 33 mod 331?
   
   General Algorithm:
   1. If $N=1$, output `2 1`.
   2. If $N > 1$:
      We can construct $M$ as a product of primes $p_1, p_2, ...$ such that the order of $A$ mod $p_i$ is $d_i$, and $\text{lcm}(d_i) = N$.
      To make it simple, let's just pick one prime $p$ such that $p-1$ is a multiple of $N$, and $A$ has order $N$ mod $p$.
      But finding such $p$ requires primality testing and searching.
      
      Is there a deterministic construction without searching?
      Yes. Let $M = 2N + 1$. If $2N+1$ is prime, we need an $A$ with order $N$.
      What if we set $A = 2$?
      Actually, there is a very specific construction for this problem which is:
      $A = 2$, $M = 2N + 1$? No.
      
      Let's look at the constraints. $N \le 10^9$. We cannot iterate to find a prime.
      There must be a formula.
      Consider $M = 2N + 1$. If $2N+1$ is prime, then the group $(\mathbb{Z}/p\mathbb{Z})^*$ has order $p-1 = 2N$. The order of any element divides $2N$. If we pick $A$ such that $A^N \equiv -1 \pmod p$, then the order is $2N$. We want order $N$.
      So we need $A^N \equiv 1 \pmod p$.
      
      Let's try a different $M$.
      How about $M = 2^N - 1$? No.
      
      Let's go back to the sample 2: N=16, A=11, M=68.
      $68 = 4 \times 17$.
      $17$ is prime, $17-1=16$. $11$ is a primitive root mod 17? $11^1=11, 11^2=121=2, 11^4=4, 11^8=16=-1, 11^{16}=1$. Yes, order is 16.
      $4 = 2^2$. Order of 11 mod 4 is 2.
      LCM(16, 2) = 16.
      
      Can we generalize this?
      We need a prime $p$ such that $p-1$ is a multiple of $N$.
      If we pick $p = kN + 1$.
      If we can find a prime $p$ of form $kN+1$, then we can find an element of order $N$ in $\mathbb{Z}_p^*$?
      Not necessarily an element of order $N$ easily without discrete log, but we can just pick $A$ such that $A = g^k$ where $g$ is a primitive root and $k = (p-1)/N$. Then $A^N = g^{p-1} = 1$. And order is $N$ because $g$ has order $p-1$.
      So the strategy is: Find a prime $p = kN + 1$. Then set $A = 2^k \pmod p$? Or just $A = 2$ if $2$ happens to have order $N$?
      But finding $p$ is hard.
      
      Wait, there is a simpler construction used in this specific problem (AtCoder ABC 213 Problem E is not it, this is **AtCoder Beginner Contest 213 Problem D**? No. It is **AtCoder Beginner Contest 213 Problem C**? No. It is **AtCoder Beginner Contest 213 Problem B**? No. It is **AtCoder Beginner Contest 213 Problem A**? No.
      Actually, this problem is **AtCoder Beginner Contest 213 Problem E**? No.
      It is **AtCoder Beginner Contest 213 Problem F**? No.
      It is **AtCoder Beginner Contest 213 Problem G**? No.
      
      Let's search for the problem text online mentally. "Find one pair of positive integers (A, M) satisfying... A^n - 1 is a multiple of M... smallest n is N".
      This is **AtCoder Beginner Contest 213 Problem E**? No.
      It is **AtCoder Beginner Contest 213 Problem D**? No.
      It is **AtCoder Beginner Contest 213 Problem C**? No.
      It is **AtCoder Beginner Contest 213 Problem B**? No.
      It is **AtCoder Beginner Contest 213 Problem A**? No.
      
      Ah, it is **AtCoder Beginner Contest 213 Problem E** is "Sum of gcd".
      Maybe it is **AtCoder Beginner Contest 213 Problem F**? No.
      
      Wait, the problem is **AtCoder Beginner Contest 213 Problem E** is not it.
      It is **AtCoder Beginner Contest 213 Problem D**? No.
      
      Let's ignore the contest number and solve it mathematically.
      We need $A^N \equiv 1 \pmod M$ and $A^k \not\equiv 1 \pmod M$ for $k < N$.
      Consider $M = 2N + 1$. If $2N+1$ is prime, then $p-1 = 2N$. The order of any element divides $2N$.
      If we choose $A$ such that $A^N \equiv 1 \pmod p$, then order divides $N$.
      If we choose $A$ such that $A^N \not\equiv 1 \pmod p$, then order does not divide $N$.
      We want order exactly $N$.
      So we need $A^N \equiv 1$ and $A^{N/2} \not\equiv 1$ (if $N$ is even).
      
      Is there a guaranteed construction?
      Yes. Let $M = 2N + 1$. If $2N+1$ is prime, then there exists an element of order $2N$. Let $g$ be a primitive root. Then $g^2$ has order $N$.
      So if $2N+1$ is prime, we can set $A = g^2 \pmod {2N+1}$.
      But we don't know if $2N+1$ is prime.
      
      What if we choose $M = 2N + 1$ regardless?
      If $2N+1$ is composite, does it work?
      Sample 1: N=3, M=7 (prime).
      Sample 2: N=16, M=68 (not $2*16+1=33$).
      
      Let's try the construction: $A = 2$, $M = 2N + 1$?
      If $N=16$, $M=33$. $2^{16} \pmod{33}$. $33 = 3 \times 11$.
      $2^{16} \pmod 3 = 2^2 \equiv 1$.
      $2^{16} \pmod{11}$. Order of 2 mod 11 is 10. $16 \equiv 6 \pmod{10}$. $2^6 = 64 = 9 \neq 1$.
      So $2^{16} \not\equiv 1 \pmod{33}$.
      
      Okay, let's look at the sample 2 again: $N=16, A=11, M=68$.
      $68 = 4 \times 17$.
      $17$ is prime, $17-1=16$.
      $4 = 2^2$.
      This suggests we are looking for a prime $p$ such that $p-1$ is a multiple of $N$.
      Specifically, $p = kN + 1$.
      If we can find a prime $p$ of the form $kN+1$, then we can set $M = p$ (or a multiple) and $A$ appropriately.
      But finding such a prime is not guaranteed for small $k$.
      
      Wait, there is a specific construction for this problem:
      $A = 2$, $M = 2N + 1$? No.
      How about $A = 2$, $M = 2^N - 1$? No.
      
      Let's try the construction: $M = 2N + 1$.
      If $2N+1$ is prime, we are good (with appropriate A).
      If not, maybe $M = 2N + 1$ still works with a different A?
      
      Actually, the problem statement says "It can be proved that such a pair... always exists".
      There is a known solution:
      $A = 2$.
      $M = 2N + 1$.
      Is it true that for any $N$, there exists an $A$ such that ord_M(A) = N?
      Not necessarily for $M=2N+1$.
      
      Let's try the construction from the sample 2 again.
      $N=16$. $M=68$. $68 = 4 \times 17$.
      $17 = 1 \times 16 + 1$.
      So $17$ is a prime of form $1 \cdot N + 1$.
      $4$ is just to make it composite? Or maybe $M$ is just $17$?
      If $M=17$, $A=11$. $11^{16} \equiv 1 \pmod{17}$. Order is 16.
      Why did they choose 68? Maybe to show multiple solutions or just a random valid one.
      So for $N=16$, we could have output `11 17`.
      
      So the strategy is: Find a prime $p$ such that $p \equiv 1 \pmod N$. Then find an $A$ of order $N$ mod $p$.
      How to find such a prime efficiently?
      We can iterate $k=1, 2, ...$ and check if $kN+1$ is prime.
      Since $N \le 10^9$, $kN+1$ can be large. But we only need one.
      By Dirichlet's theorem, there are infinitely many primes of form $kN+1$.
      The first one might be small.
      For $N=16$, $1*16+1=17$ (prime).
      For $N=3$, $1*3+1=4$ (no), $2*3+1=7$ (prime).
      For $N=55$, $1*55+1=56$ (no), $2*55+1=111$ (div by 3), $3*55+1=166$ (no), $4*55+1=221=13*17$, $5*55+1=276$, $6*55+1=331$ (prime).
      So for $N=55$, $p=331$. $331-1 = 6*55$.
      We need $A$ such that order is 55.
      $A = g^6 \pmod{331}$ where $g$ is a primitive root.
      Or simply $A = 2^6 \pmod{331}$?
      $2^6 = 64$.
      Check order of 64 mod 331.
      $64^{55} = (2^6)^{55} = 2^{330} = 2^{331-1} \equiv 1 \pmod{331}$.
      Does $64^k \equiv 1$ for $k < 55$?
      Order of 64 is $330 / \gcd(6, 330) = 330 / 6 = 55$.
      Yes!
      So the algorithm is:
      1. If $N=1$, output `2 1`.
      2. Iterate $k = 1, 2, 3, ...$
         a. Let $p = k \cdot N + 1$.
         b. Check if $p$ is prime.
         c. If prime, calculate $A = 2^{(p-1)/N} \pmod p$.
         d. Output $A$ and $p$.
         e. Break.
      
      Constraints: $N \le 10^9$.
      How large can $k$ be?
      The gap between primes is small relative to $p$.
      We expect to find a prime quickly.
      However, we need a primality test for numbers up to $\approx 10^9 \times \text{small constant}$.
      Miller-Rabin is suitable.
      Also, we need to compute modular exponentiation.
      
      Is it guaranteed that $k$ is small?
      For $N=10^9$, the next prime after $10^9$ is close.
      We are looking for $p \equiv 1 \pmod N$.
      The density of primes is $1/\ln p$.
      The density of primes $\equiv 1 \pmod N$ is $1/(\phi(N) \ln p)$.
      This might be sparse if $N$ has many factors.
      But we only need one.
      In competitive programming, usually $k$ is small (like < 100).
      Let's assume $k$ is small enough.
      
      Wait, what if $N$ is even?
      If $N$ is even, $kN+1$ is odd (for $k \ge 1$).
      If $N$ is odd, $kN+1$ can be even if $k$ is odd.
      So if $N$ is odd, we must choose $k$ even to make $p$ odd (since $p>2$).
      So step 2a: if $N$ is odd, start $k=2, 4, 6...$ else $k=1, 2, 3...$
      
      Implementation details:
      - Read T.
      - Loop T times.
      - Read N.
      - If N=1, print "2 1".
      - Else:
        - k = 1 if N%2==0 else 2
        - while True:
          - p = k*N + 1
          - if is_prime(p):
            - A = pow(2, (p-1)//N, p)
            - print(f"{A} {p}")
            - break
          - k += 1 (if N odd, k+=2)
      
      Primality test: Miller-Rabin.
      Since $p \approx 10^9$, deterministic Miller-Rabin with bases [2, 7, 61] is sufficient for $p < 4,759,123,141$.
      
      Complexity:
      T = 10^4.
      For each test case, we might check ~10-100 numbers.
      Miller-Rabin takes $O(\log^3 p)$.
      Total operations roughly $10^4 \times 100 \times (\log 10^9)^3 \approx 10^6 \times 1000 \approx 10^9$?
      Wait, $\log_2(10^9) \approx 30$. $30^3 = 27000$.
      $10^4 \times 100 \times 27000 = 2.7 \times 10^{10}$. Too slow.
      We need faster primality or fewer checks.
      Actually, for $p < 2 \cdot 10^9$, the gap is small.
      But maybe we don't need to check many.
      Also, we can optimize the Miller-Rabin.
      Or maybe there's a simpler construction?
      
      Alternative:
      $A = 2$, $M = 2N + 1$? No.
      What if we use $M = 2N + 1$ and $A = 2$?
      We saw it fails for N=16.
      
      Is there a construction that doesn't require searching for a prime?
      Maybe $M = 2^N - 1$? No.
      
      Let's reconsider the constraints and time limit. Usually 2 seconds.
      $10^4$ test cases is a lot.
      Maybe the average $k$ is very small.
      Or maybe we can use a precomputed list of primes? No, $N$ varies.
      
      Wait, is there a simpler $A, M$?
      How about $A = 2$, $M = 2N + 1$?
      If $2N+1$ is not prime, maybe $M = 2N+1$ still works with $A=2$?
      No, order must divide $\phi(M)$.
      
      Let's trust the "find prime $p=kN+1$" approach.
      Is it possible that $k$ is always small?
      Yes, for random $N$, the first prime of form $kN+1$ is usually found with small $k$.
      The worst case is when $N$ is highly composite, making $kN+1$ composite for many $k$.
      But even then, the gap between primes in arithmetic progression is not huge for $N \le 10^9$.
      The worst known gaps are much smaller than $N$.
      So $k$ will be small (likely < 100).
      The number of Miller-Rabin tests per case is small.
      $10^4 \times 50 \times 3$ (bases) $\times 30$ (modular exp steps) $\approx 4.5 \times 10^7$ ops.
      This is well within 2 seconds.
      
      So the plan is solid.
      
      Steps:
      1. Implement Miller-Rabin for $n < 2 \cdot 10^9$.
      2. Handle $N=1$ separately.
      3. Loop $k$ to find prime $p = kN+1$.
      4. Compute $A = 2^{(p-1)/N} \pmod p$.
      5. Print $A, p$.