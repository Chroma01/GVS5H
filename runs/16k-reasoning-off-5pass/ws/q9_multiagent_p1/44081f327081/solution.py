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
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Determine the maximum value in A to size our frequency array
    max_val = 0
    for x in A:
        if x > max_val:
            max_val = x

    # Frequency count of each number
    # cnt[x] stores how many times x appears in A
    cnt = [0] * (max_val + 1)
    for x in A:
        cnt[x] += 1

    # Calculate total_multiples[g]: number of elements in A that are multiples of g
    # We use a sieve-like approach.
    # total_multiples[g] = sum(cnt[j] for j in g, 2g, 3g, ...)
    total_multiples = [0] * (max_val + 1)
    for g in range(1, max_val + 1):
        count = 0
        # Iterate through multiples of g: g, 2g, 3g, ...
        for multiple in range(g, max_val + 1, g):
            count += cnt[multiple]
        total_multiples[g] = count

    # Determine the answer for each distinct value v in A.
    # ans_map[v] will store the maximum g such that v is a multiple of g and total_multiples[g] >= K.
    # We iterate g from max_val down to 1. If total_multiples[g] >= K, then g is a valid GCD.
    # Any multiple of g can potentially have g as its answer. Since we want the maximum,
    # and we iterate downwards, the first time we encounter a valid g for a multiple v,
    # that is the best answer for v.
    
    ans_map = [0] * (max_val + 1)
    
    for g in range(max_val, 0, -1):
        if total_multiples[g] >= K:
            # Mark all multiples of g that haven't been assigned an answer yet
            # Since we go downwards, the first assignment is the largest possible g.
            for multiple in range(g, max_val + 1, g):
                if ans_map[multiple] == 0:
                    ans_map[multiple] = g

    # Prepare output
    output = []
    for x in A:
        output.append(str(ans_map[x]))
    
    sys.stdout.write('\n'.join(output) + '\n')

if __name__ == '__main__':
    solve()