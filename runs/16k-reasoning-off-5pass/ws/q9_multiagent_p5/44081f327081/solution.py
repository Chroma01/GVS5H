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
        K = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Edge case: If K=1, the max GCD of a subset of size 1 containing A_i is A_i itself.
    if K == 1:
        sys.stdout.write('\n'.join(map(str, A)) + '\n')
        return

    # Determine the maximum value in A to size our arrays
    max_val = 0
    for x in A:
        if x > max_val:
            max_val = x

    # Frequency array
    cnt = [0] * (max_val + 1)
    for x in A:
        cnt[x] += 1

    # Array to store the count of multiples for each number g
    # multiples_count[g] will store how many numbers in A are multiples of g
    multiples_count = [0] * (max_val + 1)

    # Sieve-like process to count multiples
    # Complexity: O(V log V) where V = max_val
    for g in range(1, max_val + 1):
        count = 0
        for j in range(g, max_val + 1, g):
            count += cnt[j]
        multiples_count[g] = count

    # Array to store the answer for each number x
    # ans[x] will store the maximum g such that multiples_count[g] >= K and g divides x
    ans = [0] * (max_val + 1)

    # Iterate g from max_val down to 1
    # If multiples_count[g] >= K, then g is a valid GCD for all its multiples.
    # Since we iterate downwards, the first time we set ans[j], it is the maximum possible.
    for g in range(max_val, 0, -1):
        if multiples_count[g] >= K:
            for j in range(g, max_val + 1, g):
                ans[j] = g

    # Output results
    output = [str(ans[x]) for x in A]
    sys.stdout.write('\n'.join(output) + '\n')

if __name__ == '__main__':
    solve()