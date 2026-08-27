import sys
import itertools
import math

def max_pair_xor(arr):
    """Find maximum XOR of any two numbers in arr using divide-and-conquer with linear basis."""
    if len(arr) < 2:
        return 0

    def build_basis(nums):
        basis = [0] * 60
        for x in nums:
            y = x
            for b in range(59, -1, -1):
                if (y >> b) & 1:
                    if basis[b] == 0:
                        basis[b] = y
                        break
                    else:
                        y ^= basis[b]
        return basis

    def query_basis(basis, x):
        res = x
        for b in range(59, -1, -1):
            if (res ^ basis[b]) > res:
                res ^= basis[b]
        return res

    arr_copy = arr[:]

    def solve(l, r, bit):
        if l >= r or bit < 0:
            return 0
        i = l
        j = r
        while i <= j:
            while i <= j and ((arr_copy[i] >> bit) & 1) == 0:
                i += 1
            while i <= j and ((arr_copy[j] >> bit) & 1) == 1:
                j -= 1
            if i <= j:
                arr_copy[i], arr_copy[j] = arr_copy[j], arr_copy[i]
                i += 1
                j -= 1
        if j < l:
            return solve(l, r, bit-1)
        if i > r:
            return solve(l, r, bit-1)
        left_max = solve(l, j, bit-1)
        right_max = solve(i, r, bit-1)
        if (j - l + 1) < (r - i + 1):
            basis = build_basis(arr_copy[l:j+1])
            cross_max = 0
            for idx in range(i, r+1):
                cross_max = max(cross_max, query_basis(basis, arr_copy[idx]))
        else:
            basis = build_basis(arr_copy[i:r+1])
            cross_max = 0
            for idx in range(l, j+1):
                cross_max = max(cross_max, query_basis(basis, arr_copy[idx]))
        return max(left_max, right_max, cross_max)

    return solve(0, len(arr_copy)-1, 59)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    if K == 1:
        print(max(A))
        return

    if K == 2:
        ans = max_pair_xor(A)
        print(ans)
        return

    # For K >= 3, use brute force over combinations
    # The constraint binom(N,K) <= 1e6 ensures that N is small for K >= 3.
    # We can safely enumerate all K-combinations.
    ans = 0
    for combo in itertools.combinations(A, K):
        x = 0
        for num in combo:
            x ^= num
        if x > ans:
            ans = x
    print(ans)

if __name__ == "__main__":
    main()