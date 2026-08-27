
## ideation
```python
import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    n = 1 << W
    cnt = [0] * n
    
    # Parse each row string and update counts
    # Each row is a binary string representing the row values
    for _ in range(H):
        s = next(iterator)
        # Convert binary string to integer
        val = int(s, 2)
        cnt[val] += 1
        
    # Precompute popcounts for 0 to n-1 to build the cost function array g
    # popcount[i] = number of set bits in i
    popcount = [0] * n
    for i in range(1, n):
        popcount[i] = popcount[i >> 1] + (i & 1)
        
    # Build the cost function array g
    # g[u] = min(popcount(u), W - popcount(u))
    # This represents the minimum 1s in a row of length W with popcount(u) ones
    # after optimal row flip.
    g = [0] * n
    half_w = W // 2
    for i in range(n):
        pc = popcount[i]
        if pc > half_w:
            g[i] = W - pc
        else:
            g[i] = pc
            
    # Fast Walsh-Hadamard Transform (FWHT) for cnt array
    # This computes the XOR convolution basis for cnt
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = cnt[j]
                y = cnt[j + h]
                cnt[j] = x + y
                cnt[j + h] = x - y
        h *= 2
        
    # Fast Walsh-Hadamard Transform (FWHT) for g array
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = g[j]
                y = g[j + h]
                g[j] = x + y
                g[j + h] = x - y
        h *= 2
        
    # Pointwise multiplication in the transformed domain
    # This corresponds to XOR convolution in the original domain
    for i in range(n):
        cnt[i] *= g[i]
        
    # Inverse FWHT (apply FWHT again and divide by n)
    # Since FWHT is its own inverse up to a factor of n
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = cnt[j]
                y = cnt[j + h]
                cnt[j] = x + y
                cnt[j + h] = x - y
        h *= 2
        
    # Divide by n to get the final result
    # The result at index C is the minimum sum of 1s for column mask C
    for i in range(n):
        cnt[i] //= n
        
    # The answer is the minimum value in the resulting array
    print(min(cnt))

if __name__ == '__main__':
    solve()
```
