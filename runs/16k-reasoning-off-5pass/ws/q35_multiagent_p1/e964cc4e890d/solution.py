import sys

# Set recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    S = input_data[1]

    MOD = 998244353
    G = 3 # Primitive root for 998244353

    # If the last vertex is Black, it has out-degree 0 (no base edge from 2N, no added edge FROM Black).
    # Thus, the graph cannot be strongly connected.
    if S[-1] != 'W':
        print(0)
        return

    # We need to compute Ans[N] where:
    # Total[m] = m!
    # Total[m] = sum_{k=1 to m} Ans[k] * Total[m-k]
    # This implies A(x) * T(x) = T(x) - 1, where A(x) = sum Ans[m] x^m and T(x) = sum m! x^m.
    # So A(x) = 1 - 1/T(x).
    # We need the coefficient of x^N in A(x), which is - (coefficient of x^N in 1/T(x)).
    # Let InvT(x) = 1/T(x). Then Ans[N] = - InvT[N] mod MOD.
    
    # Construct T(x) = sum_{m=0 to N} m! x^m
    # We only need coefficients up to x^N.
    T = [1] * (N + 1)
    f = 1
    for i in range(1, N + 1):
        f = (f * i) % MOD
        T[i] = f

    # Compute inverse of T(x) modulo x^{N+1} using Newton's method
    # We want P(x) such that P(x) * T(x) = 1 mod x^{N+1}
    
    def poly_inv(poly, n):
        """
        Computes the inverse of a polynomial poly modulo x^n.
        poly[0] must be invertible.
        Returns a list of length n.
        """
        # Base case: inverse of constant term
        # inv(poly[0])
        inv0 = pow(poly[0], MOD - 2, MOD)
        res = [inv0]
        
        # Current length of result
        curr_len = 1
        
        while curr_len < n:
            # We want to double the precision
            next_len = min(curr_len * 2, n)
            
            # We need to compute res_new = res * (2 - poly * res) mod x^{next_len}
            # Let's compute poly * res mod x^{next_len}
            
            # Truncate poly to next_len
            poly_trunc = poly[:next_len]
            
            # Multiply poly_trunc by res
            # Result length will be next_len + curr_len - 1, but we only care up to next_len
            # Use NTT for multiplication
            
            # Size for NTT
            size = 1
            while size < next_len + curr_len:
                size *= 2
            
            # Prepare arrays for NTT
            # a = poly_trunc
            a = [0] * size
            for i in range(len(poly_trunc)):
                a[i] = poly_trunc[i]
                
            # b = res
            b = [0] * size
            for i in range(len(res)):
                b[i] = res[i]
                
            # Multiply a and b using NTT
            prod = ntt_multiply(a, b, size)
            
            # prod now contains poly * res
            # We want 2 - prod
            # res_new = res * (2 - prod)
            
            # Compute (2 - prod) mod x^{next_len}
            # Note: prod[0] should be 1 because res is inverse of poly up to curr_len
            # So 2 - prod starts with 1.
            
            two_minus_prod = [0] * next_len
            two_minus_prod[0] = (2 - prod[0]) % MOD
            for i in range(1, next_len):
                two_minus_prod[i] = (-prod[i]) % MOD
                
            # Multiply res by (2 - prod)
            # res has length curr_len
            # two_minus_prod has length next_len
            # Result has length curr_len + next_len - 1, but we only need up to next_len
            
            # Prepare for NTT
            a2 = [0] * size
            for i in range(len(res)):
                a2[i] = res[i]
                
            b2 = [0] * size
            for i in range(len(two_minus_prod)):
                b2[i] = two_minus_prod[i]
                
            prod2 = ntt_multiply(a2, b2, size)
            
            # Take first next_len coefficients
            res = prod2[:next_len]
            curr_len = next_len
            
        return res[:n]

    def ntt_multiply(a, b, size):
        """
        Multiplies two polynomials a and b using NTT.
        size must be a power of 2 and >= len(a) + len(b) - 1.
        """
        fa = ntt(a, size, False)
        fb = ntt(b, size, False)
        
        fc = [0] * size
        for i in range(size):
            fc[i] = (fa[i] * fb[i]) % MOD
            
        return ntt(fc, size, True)

    def ntt(a, size, invert):
        """
        Performs NTT or Inverse NTT on array a of length size (power of 2).
        """
        j = 0
        for i in range(1, size):
            bit = size >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
                
        length = 2
        while length <= size:
            w_len = pow(G, (MOD - 1) // length, MOD)
            if invert:
                w_len = pow(w_len, MOD - 2, MOD)
            
            for i in range(0, size, length):
                w = 1
                for j in range(length // 2):
                    u = a[i + j]
                    v = (a[i + j + length // 2] * w) % MOD
                    a[i + j] = (u + v) % MOD
                    a[i + j + length // 2] = (u - v + MOD) % MOD
                    w = (w * w_len) % MOD
            length <<= 1
            
        if invert:
            inv_size = pow(size, MOD - 2, MOD)
            for i in range(size):
                a[i] = (a[i] * inv_size) % MOD
                
        return a

    # Compute inverse of T(x)
    # T has length N+1
    InvT = poly_inv(T, N + 1)
    
    # Ans[N] = - InvT[N] mod MOD
    ans_N = (-InvT[N]) % MOD
    print(ans_N)

if __name__ == '__main__':
    solve()