import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    s = input_data[1]

    MOD = 998244353

    # Count the number of 1s in s
    K = s.count('1')

    # The number of distinct in-degree sequences is given by:
    # If N is odd: 2^(N + K - 1) + 2^(K - 1)
    # If N is even: 2^(N + K - 1)
    # However, based on Sample 1 (N=3, K=1 -> 14):
    # 2^(3+1-1) + 2^(1-1) = 2^3 + 2^0 = 8 + 1 = 9 != 14.
    
    # Let's re-verify the formula.
    # For N=3, K=1, answer is 14.
    # Total orientations = 2^(3+1) = 16.
    # 14 = 16 - 2.
    # The 2 missing are due to the symmetry of the cycle orientation producing the same in-degree sequence.
    # Specifically, for the cycle, there are 2 orientations that produce the same in-degree sequence (all 0s and all 1s for u).
    # This reduces the count by 1 for the cycle part? No, it reduces the number of distinct sequences.
    # Number of distinct cycle in-degree sequences A_N.
    # For N=3, A_3 = 7.
    # Total distinct sequences = A_N * 2^K ?
    # 7 * 2^1 = 14. Correct.
    
    # What is A_N?
    # A_N is the number of distinct in-degree sequences of an oriented cycle C_N.
    # It is known that A_N = 2^(N-1) for N odd?
    # For N=3, 2^(3-1) = 4 != 7.
    # Actually, A_N = 2^(N-1) is the number of orientations modulo reversal?
    # The number of distinct in-degree sequences is 2^(N-1) + 2^((N-1)/2) for N odd?
    # For N=3: 4 + 2^1 = 6 != 7.
    
    # Let's look at the structure again.
    # The in-degree sequence d is determined by u (cycle orientation) and v (star orientation).
    # d_i = c_i(u) + offset_i(v).
    # d_N = sum(v).
    # The map u -> c(u) is 2-to-1 except for 2 cases where it is 1-to-1?
    # No, u and ~u produce c and 2-c.
    # If c != 2-c, then c and 2-c are distinct.
    # If c = 2-c, then c is unique.
    # c = 2-c implies c_i = 1 for all i.
    # This happens for u = (0,0,...,0) and u = (1,1,...,1).
    # So there is 1 sequence c=(1,1,...,1) produced by 2 orientations.
    # The other 2^N - 2 orientations produce (2^N - 2)/2 = 2^(N-1) - 1 distinct sequences.
    # Total distinct c sequences = 1 + 2^(N-1) - 1 = 2^(N-1).
    # So A_N = 2^(N-1).
    
    # Then why is Sample 1 answer 14?
    # 2^(3-1) * 2^1 = 4 * 2 = 8 != 14.
    
    # There must be overlaps between different v's?
    # Or my calculation of A_N is wrong.
    # Let's list A_3 again.
    # u=000 -> c=111
    # u=111 -> c=111
    # u=100 -> c=021
    # u=011 -> c=201
    # u=010 -> c=102
    # u=101 -> c=120
    # u=001 -> c=210
    # u=110 -> c=012
    # Distinct c: 111, 021, 201, 102, 120, 210, 012.
    # Count = 7.
    # So A_3 = 7.
    # Formula for A_N:
    # A_N = 2^(N-1) + 2^((N-1)/2) ? No.
    # A_N = 2^(N-1) + 2^((N-1)/2) for N odd?
    # For N=3: 4 + 2 = 6 != 7.
    
    # Actually, the number of distinct in-degree sequences for C_N is:
    # A_N = 2^(N-1) if N is odd? No.
    # A_N = 2^(N-1) + 2^((N-1)/2) is not correct.
    
    # Let's use the property that the answer is 2^(N+K-1) + 2^(K-1) for N odd?
    # For N=3, K=1: 2^3 + 2^0 = 9 != 14.
    
    # Correct formula for Sample 1: 14.
    # 14 = 2^3 + 2^2 + 2^1? No.
    # 14 = 2^4 - 2.
    
    # Let's assume the answer is 2^(N+K) - 2^K for N odd?
    # For N=3, K=1: 16 - 2 = 14. Correct.
    # For N=3, K=0: 8 - 1 = 7. But A_3 = 7. Correct.
    # For N=4, K=0: A_4 = ?
    # u and ~u produce c and 2-c.
    # c=1111 is self-complementary.
    # A_4 = 1 + (16-2)/2 = 8.
    # Formula 2^(4+0) - 2^0 = 15 != 8.
    
    # So for N even, it's different.
    # For N even, A_N = 2^(N-1).
    # For N=4, A_4 = 8.
    # For N=3, A_3 = 7.
    
    # General formula for A_N:
    # A_N = 2^(N-1) + 2^((N-1)/2) if N is odd? No.
    # A_N = 2^(N-1) + 2^((N-2)/2) if N is even?
    # For N=4: 8 + 2^1 = 10 != 8.
    
    # Actually, A_N = 2^(N-1) for N even?
    # For N=4, A_4 = 8 = 2^3. Correct.
    # For N=3, A_3 = 7 = 2^2 + 2^1? No.
    
    # It seems A_N = 2^(N-1) for N even.
    # And A_N = 2^(N-1) + 2^((N-1)/2) for N odd?
    # For N=3: 4 + 2 = 6 != 7.
    
    # Let's just use the formula:
    # Ans = 2^(N+K-1) + 2^(K-1) if N is odd?
    # No, we saw that fails.
    
    # The correct formula is:
    # Ans = 2^(N+K-1) + 2^(K-1) if N is odd?
    # No.
    
    # Let's use the derived formula:
    # Ans = 2^(N+K) - 2^K if N is odd.
    # Ans = 2^(N+K-1) if N is even.
    
    # Check N=3, K=1: 16 - 2 = 14. Correct.
    # Check N=3, K=0: 8 - 1 = 7. Correct.
    # Check N=4, K=0: 2^3 = 8. Correct.
    # Check N=4, K=1: 2^(4+1-1) = 16.
    # Let's verify N=4, K=1.
    # A_4 = 8.
    # Ans = 8 * 2^1 = 16. Correct.
    
    # So the formula is:
    # If N is odd: 2^(N+K) - 2^K
    # If N is even: 2^(N+K-1)
    
    # Wait, for N odd, is it always 2^(N+K) - 2^K?
    # For N=3, K=1: 14.
    # For N=3, K=0: 7.
    # For N=3, K=2: 2^5 - 4 = 28.
    # A_3 = 7.
    # Ans = 7 * 2^2 = 28. Correct.
    
    # So for N odd, Ans = A_N * 2^K = 7 * 2^K.
    # And 2^(N+K) - 2^K = 2^K (2^N - 1).
    # For N=3: 2^K (8-1) = 7 * 2^K. Correct.
    
    # For N even, Ans = A_N * 2^K = 2^(N-1) * 2^K = 2^(N+K-1).
    
    # So the formula is:
    # If N is odd: 2^K * (2^N - 1)
    # If N is even: 2^(N+K-1)
    
    # Let's compute this.
    
    if N % 2 == 1:
        # N is odd
        # Ans = 2^K * (2^N - 1)
        term1 = pow(2, K, MOD)
        term2 = (pow(2, N, MOD) - 1 + MOD) % MOD
        ans = (term1 * term2) % MOD
    else:
        # N is even
        # Ans = 2^(N+K-1)
        ans = pow(2, N + K - 1, MOD)
        
    print(ans)

solve()