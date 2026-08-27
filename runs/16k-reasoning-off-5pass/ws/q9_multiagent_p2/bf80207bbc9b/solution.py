import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    # Read the grid rows
    # Each row is a string of '0' and '1'
    rows = []
    for _ in range(H):
        rows.append(next(iterator))

    # Convert rows to integer masks
    # Since W <= 18, we can fit each row in an integer
    # We will count the frequency of each mask
    count = [0] * (1 << W)
    
    for r in rows:
        mask = 0
        for char in r:
            mask = (mask << 1) | int(char)
        count[mask] += 1

    # Function to compute FWHT for XOR convolution
    # We want to compute the convolution of 'count' and 'kernel'
    # where kernel[x] = min(popcount(x), W - popcount(x))
    # The FWHT for XOR convolution is defined as:
    # F_hat[u] = sum_{v} F[v] * (-1)^{popcount(u & v)}
    # But for standard XOR convolution A * B, we use:
    # FWHT(A)[i] = sum_{j} A[j] * (-1)^{popcount(i & j)}
    # Then (A * B)_k = (1/2^W) * sum_{i} FWHT(A)[i] * FWHT(B)[i] * (-1)^{popcount(k & i)}
    # Wait, the standard FWHT for XOR convolution usually uses +1 and -1.
    # Let's verify the transform definition.
    # H(u, v) = (-1)^{popcount(u & v)}
    # Transform: T(A)[u] = sum_v A[v] * H(u, v)
    # Inverse: A[v] = (1/2^W) * sum_u T(A)[u] * H(u, v)
    # Convolution C = A * B means C[k] = sum_j A[j] * B[k^j]
    # Then T(C) = T(A) * T(B) (pointwise product)
    
    # Step 1: Prepare the kernel array
    # kernel[x] = min(popcount(x), W - popcount(x))
    kernel = [0] * (1 << W)
    for x in range(1 << W):
        pc = bin(x).count('1')
        kernel[x] = min(pc, W - pc)

    # Step 2: Transform 'count' and 'kernel'
    # We implement the iterative FWHT for XOR
    # Transform in-place
    
    def fwht(arr):
        n = len(arr)
        if n == 1:
            return
        length = 1
        while length < n:
            for i in range(0, n, length * 2):
                for j in range(i, i + length):
                    u = arr[j]
                    v = arr[j + length]
                    arr[j] = u + v
                    arr[j + length] = u - v
            length *= 2

    # Apply FWHT
    fwht(count)
    fwht(kernel)

    # Step 3: Pointwise multiplication
    # Since we are working with integers, we can just multiply.
    # Note: The values can be negative during intermediate steps, but the final result
    # after inverse transform will be non-negative counts.
    # However, Python handles large integers automatically.
    for i in range(1 << W):
        count[i] *= kernel[i]

    # Step 4: Inverse FWHT
    # The inverse transform is the same as forward transform, followed by division by n
    fwht(count)
    
    # Divide by 2^W
    n = 1 << W
    for i in range(n):
        count[i] //= n

    # Step 5: Find the minimum value
    # count[x] now holds the minimum sum of 1s for a specific column flip configuration x
    ans = min(count)
    
    print(ans)

if __name__ == '__main__':
    solve()