import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A = list(map(int, input_data[1:]))
    
    # Maximum possible value of A_i is 10^7, so max sum is 2 * 10^7
    MAX_VAL = 10**7
    MAX_SUM = 2 * MAX_VAL
    
    # Frequency array for values in A
    freq = [0] * (MAX_VAL + 1)
    for x in A:
        freq[x] += 1
        
    # Get distinct values present in A, sorted
    distinct_vals = [x for x in range(1, MAX_VAL + 1) if freq[x] > 0]
    
    ans = 0
    
    # For each odd d, and for each k such that s = d * 2^k <= MAX_SUM
    # We iterate over all odd d from 1 to MAX_SUM
    for d in range(1, MAX_SUM + 1, 2):
        s = d
        while s <= MAX_SUM:
            # Count pairs (i, j) with i <= j such that A_i + A_j = s
            count = 0
            half_s = s // 2
            
            # Iterate over distinct values a such that a <= half_s
            for a in distinct_vals:
                if a > half_s:
                    break
                b = s - a
                # Check if b is a valid value in A
                if b <= MAX_VAL and freq[b] > 0:
                    if a < b:
                        count += freq[a] * freq[b]
                    else: # a == b
                        count += freq[a] * (freq[a] + 1) // 2
            
            ans += d * count
            s *= 2
            
    print(ans)

solve()