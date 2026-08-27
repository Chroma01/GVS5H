import sys
from math import comb

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])
    n = N // 2
    # Precompute binomial coefficients mod P
    maxN = n * n
    fact = [1] * (maxN + 1)
    for i in range(1, maxN + 1):
        fact[i] = fact[i-1] * i % P
    inv_fact = [1] * (maxN + 1)
    inv_fact[maxN] = pow(fact[maxN], P-2, P)
    for i in range(maxN, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % P
    def C(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * inv_fact[b] % P * inv_fact[a-b] % P
    
    # Precompute g(p,q,e): number of ways to choose a subset of p left vertices and q right vertices 
    # such that the bipartite graph between them is connected and has exactly e edges.
    # This is done by inclusion-exclusion on the right side.
    g = [[[0]*(maxN+1) for _ in range(n+1)] for __ in range(n+1)]
    for p in range(n+1):
        for q in range(n+1):
            for e in range(p*q+1):
                val = 0
                for k in range(q+1):
                    if e > p*(q-k):
                        continue
                    val = (val + ((-1)**k) * C(q,k) * C(p*(q-k), e)) % P
                g[p][q][e] = val % P
    
    # Generate all valid layer partitions (a1,...,ak) with sum odd = n, sum even = n-1
    partitions = []
    def gen(odd_sum, even_sum, is_odd, current):
        if odd_sum == 0 and even_sum == 0:
            partitions.append(current[:])
            return
        if is_odd:
            if odd_sum > 0:
                for a in range(1, odd_sum+1):
                    current.append(a)
                    gen(odd_sum - a, even_sum, False, current)
                    current.pop()
        else:
            if even_sum > 0:
                for a in range(1, even_sum+1):
                    current.append(a)
                    gen(odd_sum, even_sum - a, True, current)
                    current.pop()
    gen(n, n-1, True, [])
    
    Nfact = fact[N]
    maxM = n*n
    ans = [0] * (maxM + 1)
    
    for part in partitions:
        # Weight: number of ways to assign vertices to layers, with vertex 1 fixed in L0
        # = N! / (1! * a1! * a2! ... ak!)
        weight = Nfact
        for a in part:
            weight = weight * inv_fact[a] % P
        
        # DP: state is (p, m) where p is number of vertices in current layer connected to L0
        sizes = [1] + part
        dp = {1: {0: 1}}  # Initially, L0 has 1 vertex (vertex 1), connected with 0 edges
        
        for i in range(len(sizes)-1):
            a_i = sizes[i]
            a_ip1 = sizes[i+1]
            new_dp = {}
            for p, m_dict in dp.items():
                for m, count in m_dict.items():
                    # Choose subset of size q from L_{i+1} that will be connected to the p vertices in L_i
                    for q in range(1, a_ip1+1):
                        c_q = C(a_ip1, q)
                        for e1 in range(p*q+1):
                            g_val = g[p][q][e1]
                            if g_val == 0:
                                continue
                            # Edges from p vertices in L_i to the remaining a_{i+1}-q vertices in L_{i+1}
                            max_e2 = p * (a_ip1 - q)
                            c_e2_list = [C(max_e2, e2) for e2 in range(max_e2+1)]
                            # Edges from the remaining a_i - p vertices in L_i to the remaining a_{i+1}-q vertices in L_{i+1}
                            max_e3 = (a_i - p) * (a_ip1 - q)
                            c_e3_list = [C(max_e3, e3) for e3 in range(max_e3+1)]
                            for e2 in range(max_e2+1):
                                c_e2 = c_e2_list[e2]
                                if c_e2 == 0:
                                    continue
                                for e3 in range(max_e3+1):
                                    c_e3 = c_e3_list[e3]
                                    if c_e3 == 0:
                                        continue
                                    add = count * c_q % P * g_val % P * c_e2 % P * c_e3 % P
                                    new_m = m + e1 + e2 + e3
                                    if new_m > maxM:
                                        continue
                                    if q not in new_dp:
                                        new_dp[q] = {}
                                    new_dp[q][new_m] = (new_dp[q].get(new_m, 0) + add) % P
            dp = new_dp
        
        # At the last layer, we require all a_k vertices to be connected (p = a_k)
        a_k = sizes[-1]
        if a_k in dp:
            for m, count in dp[a_k].items():
                if m <= maxM:
                    ans[m] = (ans[m] + count * weight) % P
    
    total_edges = N*(N-1)//2
    out = []
    for M in range(N-1, total_edges+1):
        if M <= maxM:
            out.append(str(ans[M] % P))
        else:
            out.append('0')
    print(' '.join(out))

if __name__ == "__main__":
    solve()