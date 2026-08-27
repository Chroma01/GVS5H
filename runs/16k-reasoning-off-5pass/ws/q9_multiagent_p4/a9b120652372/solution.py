import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        T_str = next(iterator)
    except StopIteration:
        return
        
    T = int(T_str)
    results = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            A = next(iterator)
            B = next(iterator)
        except StopIteration:
            break
            
        # Extract positions (0-indexed) of '1's
        S = [i for i, c in enumerate(A) if c == '1']
        T_pos = [i for i, c in enumerate(B) if c == '1']
        
        k = len(S)
        m = len(T_pos)
        
        # If we have fewer pieces than required targets, it's impossible
        if k < m:
            results.append("-1")
            continue
        
        # Calculate gaps between consecutive pieces
        # gaps_S[i] is the distance between S[i] and S[i+1]
        gaps_S = [S[i+1] - S[i] for i in range(k-1)]
        # gaps_T[i] is the distance between T_pos[i] and T_pos[i+1]
        gaps_T = [T_pos[i+1] - T_pos[i] for i in range(m-1)]
        
        extra = k - m
        
        # Helper to calculate ceil(x/2) for x > 0
        def get_req(val):
            if val <= 0:
                return 0
            return (val + 1) // 2
        
        # Base shift required for the first piece
        # We need S[0] to move to T_pos[0]
        # Net shift = T_pos[0] - S[0]
        Base = T_pos[0] - S[0]
        
        # If extra == 0, this case is handled by k < m check, but for safety:
        if extra == 0:
             results.append("-1")
             continue
        
        # If extra == 1, the target gap sequence is always gaps_T regardless of stack position.
        # We just calculate the cost once.
        if extra == 1:
            R = 0
            for i in range(k-1):
                diff = gaps_S[i] - gaps_T[i]
                if diff > 0:
                    R += get_req(diff)
            
            cost = 2 * R + abs(Base - R)
            results.append(str(cost))
            continue
            
        # If extra > 1, we iterate over all possible stack positions.
        # Stack position j (0 to m-1) means we stack extra pieces on T_pos[j].
        # This inserts (extra - 1) zeros into the target gap sequence.
        
        # Calculate initial R for j=0
        # H_0 structure: [0]*(extra-1) + gaps_T
        # We compare gaps_S[i] with H_0[i]
        
        R = 0
        split_idx = extra - 1
        
        # Part 1: i < split_idx -> compare gaps_S[i] with 0
        for i in range(split_idx):
            R += get_req(gaps_S[i])
            
        # Part 2: i >= split_idx -> compare gaps_S[i] with gaps_T[i - split_idx]
        for j in range(m - 1):
            val = gaps_S[split_idx + j]
            diff = val - gaps_T[j]
            if diff > 0:
                R += get_req(diff)
                
        current_R = R
        min_ops = 2 * current_R + abs(Base - current_R)
        
        # Iterate j from 0 to m-2 to update R for j+1
        # Transition from stack on T_pos[j] to stack on T_pos[j+1]
        # This moves the block of zeros one step to the right.
        # The element gaps_T[j] moves from the "suffix" (compared to 0) to the "prefix" (compared to gaps_S[j]).
        # The element gaps_S[j + extra - 1] moves from "compared to gaps_T[j]" to "compared to 0".
        
        for j in range(m - 1):
            idx1 = j
            idx2 = j + extra - 1
            
            # Remove contributions from current state (stack on j)
            # At idx1: compared to 0
            if gaps_S[idx1] > 0:
                R -= get_req(gaps_S[idx1])
            # At idx2: compared to gaps_T[j]
            if gaps_S[idx2] > gaps_T[j]:
                R -= get_req(gaps_S[idx2] - gaps_T[j])
            
            # Add contributions from next state (stack on j+1)
            # At idx1: compared to gaps_T[j]
            diff1 = gaps_S[idx1] - gaps_T[j]
            if diff1 > 0:
                R += get_req(diff1)
            
            # At idx2: compared to 0
            if gaps_S[idx2] > 0:
                R += get_req(gaps_S[idx2])
                
            current_R = R
            cost = 2 * current_R + abs(Base - current_R)
            if cost < min_ops:
                min_ops = cost
                
        results.append(str(min_ops))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()