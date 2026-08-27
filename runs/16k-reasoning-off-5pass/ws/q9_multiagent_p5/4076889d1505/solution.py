import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from standard input efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        # First token is the number of test cases
        num_test_cases = int(next(iterator))
    except StopIteration:
        return

    results = []
    
    for _ in range(num_test_cases):
        try:
            n_str = next(iterator)
            n = int(n_str)
        except StopIteration:
            break
        
        if n == 1:
            # For N=1, we need A^1 - 1 to be a multiple of M.
            # The sample output suggests (2, 1).
            # 2^1 - 1 = 1, which is divisible by 1.
            # The smallest n such that 2^n - 1 is divisible by 1 is n=1.
            results.append("2 1")
        else:
            # For N > 1, we choose A = 2 and M = 2^N - 1.
            # Proof of correctness:
            # 1. By definition, 2^N - 1 is divisible by M (since M = 2^N - 1).
            #    So, 2^N = 1 (mod M).
            # 2. Suppose there exists a positive integer d < N such that 2^d = 1 (mod M).
            #    This implies M divides (2^d - 1).
            #    So, 2^N - 1 divides 2^d - 1.
            #    However, for d < N, 2^d - 1 < 2^N - 1.
            #    A positive integer cannot divide a smaller positive integer.
            #    Therefore, no such d exists.
            # The multiplicative order of 2 modulo (2^N - 1) is exactly N.
            
            a = 2
            # Using bit shift for efficiency: 2^N is 1 << N
            m = (1 << n) - 1
            results.append(f"{a} {m}")

    # Print all results separated by newlines
    print('\n'.join(results))

if __name__ == '__main__':
    solve()