import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3].strip()
    
    # Direction vectors
    dr = {'N': -1, 'S': 1, 'W': 0, 'E': 0}
    dc = {'N': 0, 'S': 0, 'W': -1, 'E': 1}
    
    # Prefix sums P_i = (r_i, c_i) for i=0..N
    # P_0 = (0,0)
    pr = [0] * (N + 1)
    pc = [0] * (N + 1)
    for i in range(1, N + 1):
        pr[i] = pr[i-1] + dr[S[i-1]]
        pc[i] = pc[i-1] + dc[S[i-1]]
    
    # Set of prefix sums at birth times
    # Initially, birth time 0 is always included
    birth_set = set()
    birth_set.add((0, 0))
    
    # We will compute the answer string
    ans = []
    
    # For each t from 1 to N, we need to check if (R,C) is occupied at time t+0.5
    # Condition: exists b in birth_set (with b <= t) such that P_b = P_t - (R,C)
    # Equivalently, (P_t - (R,C)) is in the set of P_b for b in birth_set.
    # We maintain the set of P_b for b in birth_set as we go.
    
    # We need to update birth_set as we go: after processing time t, we determine if t is a birth time.
    # But careful: the birth time t is determined by checking P_t against the current birth_set (which contains P_b for b < t that are birth times).
    # So we can process t from 1 to N:
    #   - First, check if (R,C) is occupied at time t+0.5 using the current birth_set (which contains birth times up to t-1? Actually, we need birth times b <= t. But the birth time t itself is not yet known when we check at time t+0.5? Wait: at time t+0.5, the particles present are those born at times b <= t. The birth time t is determined by the state at time t-0.5, which depends on birth times < t. So when we are at time t, the birth times up to t-1 are already known. The birth time t is not yet known, but it will be a particle that appears at time t+0.5. So for the query at time t+0.5, we need to consider birth times b <= t. The birth time t itself is valid if P_t is not in the set of P_b for b in birth_set (which currently contains birth times up to t-1). So we can:
    #   - Check the query using the current birth_set (which has birth times up to t-1) plus possibly b=t if it is a birth time. But we don't know yet if t is a birth time. However, we can check the query using the current birth_set, and then if t is a birth time, we also need to include it. But wait: the query at time t+0.5 includes the particle born at time t if it exists. So we need to check if (R,C) is occupied by either an old particle (b < t) or the new one (b = t). The new one is at (0,0) at time t+0.5? No, the new particle is generated at time t+0.5 at (0,0). So if (R,C) = (0,0), then the new particle would occupy it. But the new particle is generated only if origin is empty after shift. So we need to handle that.
    # Actually, the condition we derived: (R,C) is occupied at time t+0.5 iff there exists b in B with b <= t such that P_t - P_b = (R,C). This includes b=t. So we need to know if t is in B. But we can determine if t is in B by checking if P_t is not in the set of P_b for b in B (current, which has b < t). So we can do:
    #   - Compute V = P_t - (R,C).
    #   - Check if V is in birth_set (which contains P_b for b in B, b < t).
    #   - Additionally, if t is a birth time (i.e., P_t not in birth_set), then we also need to check if V == P_t (since for b=t, P_t - P_t = (0,0), so if (R,C) = (0,0), then V = P_t, and we need to include that). Wait, careful: For b=t, the condition is P_t - P_t = (0,0) = (R,C). So if (R,C) = (0,0), then V = P_t. So if t is a birth time, then V = P_t is a valid match. But if t is not a birth time, then b=t is not in B, so we don't consider it.
    # So the algorithm:
    #   For t = 1..N:
    #     V = (pr[t] - R, pc[t] - C)
    #     occupied = (V in birth_set) or ( (R,C) == (0,0) and t is a birth time? Actually, if (R,C) == (0,0), then V = P_t. So we need to check if P_t is in birth_set or if t is a birth time. But note: if t is a birth time, then P_t is not in birth_set (by definition of birth time). So we need to check separately: if (R,C) == (0,0), then occupied = (P_t in birth_set) or (t is a birth time). But wait, is it possible that P_t is in birth_set and t is a birth time? No, because if t is a birth time, P_t is not in birth_set. So they are mutually exclusive. So we can just check: occupied = (V in birth_set) or ( (R,C) == (0,0) and t is a birth time ). But actually, if (R,C) == (0,0), V = P_t. So V in birth_set is exactly the condition that P_t is in birth_set. And the additional condition is that t is a birth time. So we can write:
    #     occupied = (V in birth_set) or ( (R,C) == (0,0) and t is a birth time )
    #   Then, after that, we update: if P_t not in birth_set, then add P_t to birth_set (i.e., t becomes a birth time).
    
    # Let's test this logic with the SN example.
    # N=2, S="SN", R=0, C=0.
    # P_0=(0,0); P_1=(1,0); P_2=(0,0).
    # birth_set initially: {(0,0)}.
    # t=1: V = P_1 - (0,0) = (1,0). Is (1,0) in birth_set? No. (R,C)==(0,0) and t is birth time? t=1: is P_1 in birth_set? No, so t is a birth time. So occupied = False or True = True. So ans[1] = 1. Correct: at time 1.5, (0,0) is occupied by the new particle.
    # Then update: P_1=(1,0) not in birth_set, so add it. birth_set = {(0,0), (1,0)}.
    # t=2: V = P_2 - (0,0) = (0,0). Is (0,0) in birth_set? Yes. So occupied = True. So ans[2] = 1. Correct: at time 2.5, (0,0) is occupied by the old particle.
    # Then update: P_2=(0,0) is in birth_set, so do not add. birth_set remains.
    # So ans = "11". But wait, the sample output for some query might be different. Let's test with a different query.
    
    # Another test: S="NS", R=0, C=0.
    # d_1=N=(-1,0), d_2=S=(1,0). P_0=(0,0); P_1=(-1,0); P_2=(0,0).
    # birth_set = {(0,0)}.
    # t=1: V = (-1,0). Not in birth_set. (R,C)==(0,0) and t is birth time? P_1 not in birth_set, so yes. occupied = True. ans[1]=1.
    # Update: add (-1,0). birth_set = {(0,0), (-1,0)}.
    # t=2: V = (0,0). In birth_set. occupied = True. ans[2]=1.
    # Update: P_2=(0,0) in birth_set, no add.
    # So ans = "11". Is that correct? Let's simulate:
    # t=0: {(0,0)}
    # t=1: wind N: shift to (-1,0). Origin empty -> add (0,0). So at 1.5: {(-1,0), (0,0)}. (0,0) occupied.
    # t=2: wind S: shift to (0,0) and (1,0). Origin occupied (by the shifted old particle). No new. So at 2.5: {(0,0), (1,0)}. (0,0) occupied. So yes, both times (0,0) is occupied. So "11" is correct.
    
    # Now test with R=1, C=0 for S="SN".
    # t=1: V = (1,0) - (1,0) = (0,0). In birth_set? Yes. occupied = True. ans[1]=1.
    # t=2: V = (0,0) - (1,0) = (-1,0). In birth_set? No. (R,C)==(0,0)? No. So occupied = False. ans[2]=0.
    # Simulation: at 1.5, particles at (1,0) and (0,0). So (1,0) is occupied. At 2.5, particles at (0,0) and (-1,0). So (1,0) is not occupied. Correct.
    
    # So the algorithm works.
    
    # Implementation details:
    # We need to store the set of (r,c) for birth times. Since N up to 200k, we can store tuples.
    # But checking membership in a set of tuples is O(1) average.
    
    # Let's code it.
    
    for t in range(1, N + 1):
        vr = pr[t] - R
        vc = pc[t] - C
        # Check if (vr, vc) is in birth_set
        if (vr, vc) in birth_set:
            ans.append('1')
        elif R == 0 and C == 0:
            # Special case: if (R,C) is origin, we also need to check if t is a birth time
            # because then the new particle is at origin.
            # But wait: if (R,C) is origin, then vr = pr[t], vc = pc[t]. So we are checking if P_t is in birth_set.
            # If it is, then occupied. If not, but t is a birth time, then also occupied.
            # So we need to check if t is a birth time. But we haven't determined that yet.
            # Actually, we can determine if t is a birth time by checking if P_t is in birth_set.
            # If P_t is not in birth_set, then t is a birth time.
            # So we can write:
            if (pr[t], pc[t]) not in birth_set:
                ans.append('1')
            else:
                ans.append('0')
        else:
            ans.append('0')
        
        # Update birth_set: if P_t is not in birth_set, add it.
        if (pr[t], pc[t]) not in birth_set:
            birth_set.add((pr[t], pc[t]))
    
    print(''.join(ans))

if __name__ == "__main__":
    solve()