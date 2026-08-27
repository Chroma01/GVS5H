import sys
import itertools

def insert_basis(basis, x):
    # Insert x into linear basis (row echelon form) over GF(2)
    # basis is a list of length 61 where basis[i] has bit i as highest set bit
    for i in range(60, -1, -1):
        if not (x >> i) & 1:
            continue
        if basis[i] == 0:
            basis[i] = x
            # Eliminate lower bits
            for j in range(i):
                if basis[i] & (1 << j):
                    basis[i] ^= basis[j]
            # Eliminate higher bits
            for j in range(i + 1, 61):
                if basis[j] & (1 << i):
                    basis[j] ^= basis[i]
            return
        x ^= basis[i]

def min_combine(basis, x):
    # Given basis, find minimum value of x ^ y where y is in span of basis
    for i in range(60, -1, -1):
        if basis[i] == 0:
            continue
        if (x ^ basis[i]) < x:
            x ^= basis[i]
    return x

def max_combine(basis, x):
    # Given basis, find maximum value of x ^ y where y is in span of basis
    for i in range(60, -1, -1):
        if basis[i] == 0:
            continue
        if (x ^ basis[i]) > x:
            x ^= basis[i]
    return x

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    total_xor = 0
    for v in A:
        total_xor ^= v

    R = N - K
    # If we minimize removed subset
    if R < K:
        mode = 'min'  # minimize XOR of R elements
        m = R
    else:
        mode = 'max'  # maximize XOR of K elements
        m = K

    if m == 0:
        # If we need to choose all elements (K=N) -> answer is total_xor
        # If K=0 not possible, but m=0 means R=0 => K=N
        print(total_xor)
        return

    # Split into two halves
    n1 = N // 2
    first = A[:n1]
    second = A[n1:]

    # Enumerate subsets of first half of size 0..m
    # For each subset, store (xor, size)
    first_subs = []
    len1 = len(first)
    for size in range(0, m + 1):
        if size > len1:
            break
        for combo in itertools.combinations(range(len1), size):
            xor_val = 0
            for idx in combo:
                xor_val ^= first[idx]
            first_subs.append((xor_val, size))

    # Enumerate subsets of second half of size 0..m
    # Group by size, and for each size build a linear basis
    len2 = len(second)
    # bases[size] = list of 61 ints (the basis)
    bases = {}
    # We also need to know which sizes have at least one subset (besides size 0)
    # For size 0, only one subset (empty), which has xor 0.
    for size in range(0, m + 1):
        if size > len2:
            break
        basis = [0] * 61
        if size == 0:
            bases[0] = basis
            continue
        for combo in itertools.combinations(range(len2), size):
            xor_val = 0
            for idx in combo:
                xor_val ^= second[idx]
            insert_basis(basis, xor_val)
        bases[size] = basis

    # Combine
    best = None
    for x1, s1 in first_subs:
        s2 = m - s1
        if s2 < 0 or s2 > len2:
            continue
        basis = bases.get(s2)
        if basis is None:
            continue
        if mode == 'min':
            # We want to minimize (x1 ^ y) where y is in span of basis
            combined = min_combine(basis, x1)
        else:
            # Maximize
            combined = max_combine(basis, x1)
        if best is None:
            best = combined
        elif mode == 'min' and combined < best:
            best = combined
        elif mode == 'max' and combined > best:
            best = combined

    if mode == 'min':
        answer = total_xor ^ best
    else:
        answer = best

    print(answer)

if __name__ == "__main__":
    solve()