import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
        B = []
        for _ in range(N):
            B.append(int(next(iterator)))
    except StopIteration:
        return

    # Extract known values (non -1)
    VA = [x for x in A if x != -1]
    VB = [x for x in B if x != -1]
    
    kA = len(VA)
    kB = len(VB)
    
    # Calculate the minimum number of pairs (a, b) with a+b=S that we MUST form.
    # Let p be the number of pairs where both A and B are known and sum to S.
    # The remaining (kA - p) knowns in A must be paired with -1s in B.
    # The number of -1s in B is (N - kB).
    # Constraint: kA - p <= N - kB  =>  p >= kA + kB - N.
    # Similarly for B: kB - p <= N - kA => p >= kA + kB - N.
    # Also p >= 0.
    forced_pairs = max(0, kA + kB - N)
    
    # If forced_pairs == 0, we don't need to form any specific pairs summing to S.
    # We can choose S = max(VA U VB) (or 0 if sets are empty).
    # Since we can rearrange A, we can always pair any known A with a -1 in B (if available)
    # or any known B with a -1 in A. The only constraint is S >= all known values.
    # If forced_pairs == 0, it implies we have enough -1s to cover all unmatched knowns
    # without needing to match known A with known B.
    # Thus, a valid S always exists.
    if forced_pairs == 0:
        print("Yes")
        return

    # If forced_pairs > 0, we must find an S such that we can form at least forced_pairs pairs (a, b) with a+b=S.
    # Additionally, for any unpaired known value x (either in A or B), the corresponding filled value must be non-negative.
    # This implies S - x >= 0 => S >= x.
    # Therefore, we must have S >= max(VA U VB).
    
    # Precompute max value to check validity quickly
    max_val = 0
    if VA:
        max_val = max(max_val, max(VA))
    if VB:
        max_val = max(max_val, max(VB))
    
    # We need to check if there exists an S >= max_val such that count(a+b=S) >= forced_pairs.
    # Since N <= 2000, |VA|*|VB| <= 4*10^6, which is acceptable in Python.
    
    # We use a frequency map (dictionary) for sums.
    sum_counts = {}
    
    # Iterate over all pairs to generate candidate sums
    for a in VA:
        for b in VB:
            s = a + b
            if s >= max_val:
                sum_counts[s] = sum_counts.get(s, 0) + 1
    
    # Check if any sum has count >= forced_pairs
    possible = False
    for s, count in sum_counts.items():
        if count >= forced_pairs:
            possible = True
            break
            
    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()