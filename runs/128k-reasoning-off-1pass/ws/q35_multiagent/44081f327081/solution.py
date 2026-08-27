import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    A = [int(x) for x in data[2:2+N]]
    
    max_A = max(A) if A else 0
    
    # Count frequency of each number in A
    freq = [0] * (max_A + 1)
    for x in A:
        freq[x] += 1
    
    # For each g from 1 to max_A, count how many elements in A are divisible by g
    count = [0] * (max_A + 1)
    for g in range(1, max_A + 1):
        c = 0
        for multiple in range(g, max_A + 1, g):
            c += freq[multiple]
        count[g] = c
    
    # For each value v from 1 to max_A, find the largest divisor d of v such that count[d] >= K
    # We do this by iterating g from max_A down to 1, and for each g with count[g] >= K,
    # we set ans[v] = g for all multiples v of g that haven't been set yet.
    ans = [0] * (max_A + 1)
    for g in range(max_A, 0, -1):
        if count[g] >= K:
            for multiple in range(g, max_A + 1, g):
                if ans[multiple] == 0:
                    ans[multiple] = g
    
    # Output the answer for each A_i
    results = []
    for x in A:
        results.append(str(ans[x]))
    
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    main()