import sys

def solve() -> None:
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    # S is the next n integers
    s_list = list(map(int, input_data[1:n+1]))
    
    # Find the maximum value to determine the bitset size
    if not s_list:
        print(0)
        return
        
    max_val = max(s_list)
    
    # Create a bitmask where the i-th bit is set if i is in S
    # We use a large integer as a bitset.
    # bit 0 corresponds to value 0 (which is not in S as S_i >= 1, but it's fine)
    # bit v corresponds to value v.
    mask = 0
    for x in s_list:
        mask |= (1 << x)
        
    total_fine_triplets = 0
    
    # We iterate over all possible differences d.
    # For a fixed d, a triplet (A, B, C) with B-A = C-B = d exists if:
    # A = B - d, C = B + d are both in S.
    # This is equivalent to checking if there exists B such that (B-d) in S and (B+d) in S.
    # In terms of the bitset:
    # Let V be the bitmask for S.
    # (V >> d) has bit B-d set if B-d was in S (shifted to position B).
    # (V << d) has bit B+d set if B+d was in S (shifted to position B).
    # The AND of these two shifted masks will have bit B set if both B-d and B+d were in S.
    # The number of set bits in (V >> d) & (V << d) is the number of valid middle elements B for difference d.
    
    # The maximum possible difference d is max_val // 2, because we need B-d >= 1 and B+d <= max_val.
    # Actually, B can be up to max_val, so B+d <= max_val => d <= max_val - B.
    # Also B-d >= 1 => d <= B-1.
    # So d ranges from 1 to max_val // 2.
    
    limit_d = max_val // 2
    
    for d in range(1, limit_d + 1):
        # Shift the mask
        # Note: In Python, large integer operations are efficient but O(N/word_size).
        # We do this for d up to 500,000. Total operations ~ 500,000 * (10^6 / 64) bit-ops.
        # This might be tight in Python, but it's the best algorithmic approach.
        
        # We can optimize by checking if the shifted masks have any overlap quickly?
        # No, we need the count.
        
        shifted_right = mask >> d
        shifted_left = mask << d
        
        # The valid B's are at positions where both shifted masks have a 1.
        # However, shifted_left might have bits set beyond max_val, which is fine, 
        # as long as we only count bits that correspond to valid B.
        # A valid B must satisfy B-d >= 1 and B+d <= max_val.
        # The bitset approach naturally handles this if we consider the range.
        # Specifically, if we mask the result to only consider bits up to max_val - d?
        # Actually, if bit B is set in (V>>d) & (V<<d), it means V had bit B-d and B+d set.
        # Since V only has bits set for values in S (which are <= max_val), 
        # B-d >= 0 and B+d <= max_val. Since S_i >= 1, B-d >= 1 implies B >= d+1.
        # And B+d <= max_val implies B <= max_val - d.
        # So any set bit B in the result corresponds to a valid B in S?
        # Wait, B itself must be in S? No, the definition of fine triplet requires A, B, C in S.
        # Our condition was: A = B-d in S, C = B+d in S.
        # Does B have to be in S? Yes, the problem states A, B, C in S.
        # So we must also check if B is in S.
        # The AND operation (V>>d) & (V<<d) checks if B-d in S and B+d in S.
        # It does NOT check if B in S.
        # So we need to intersect with V again.
        
        common = shifted_right & shifted_left
        # Now intersect with the original mask to ensure B is in S
        common_with_B = common & mask
        
        # Count the number of set bits
        total_fine_triplets += common_with_B.bit_count()
        
    print(total_fine_triplets)

if __name__ == '__main__':
    solve()