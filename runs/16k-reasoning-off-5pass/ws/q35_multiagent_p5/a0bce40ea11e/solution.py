import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        p = int(next(iterator))
    except StopIteration:
        return

    A = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(next(iterator)))
        A.append(row)

    # Special case for p=2
    if p == 2:
        # Construct B by replacing 0 with 1
        B = []
        for i in range(N):
            row = []
            for j in range(N):
                if A[i][j] == 0:
                    row.append(1)
                else:
                    row.append(A[i][j] % 2)
            B.append(row)
        
        # Compute B^2 mod 2
        # Result[i][j] = sum(B[i][k] * B[k][j]) mod 2
        res = [[0] * N for _ in range(N)]
        for i in range(N):
            for k in range(N):
                if B[i][k] == 0:
                    continue
                val_ik = B[i][k]
                for j in range(N):
                    res[i][j] = (res[i][j] + val_ik * B[k][j]) % 2
        
        for row in res:
            print(" ".join(map(str, row)))
        return

    # General case for p > 2
    # Initialize result matrix
    res = [[0] * N for _ in range(N)]
    
    # Iterate over all zero-edges (u, v)
    for u in range(N):
        for v in range(N):
            if A[u][v] == 0:
                # Check if the reverse edge (v, u) is non-zero
                if A[v][u] != 0:
                    val = A[v][u]
                    # Contribution is -val for each valid path configuration
                    # The number of valid positions k for the non-zero edge depends on parity
                    
                    if p % 2 == 0:
                        # p is even
                        # k even: i=u, j=u. Count = p // 2
                        # k odd: i=v, j=v. Count = p // 2
                        cnt = p // 2
                        contrib = (val * cnt) % p
                        
                        res[u][u] = (res[u][u] - contrib) % p
                        res[v][v] = (res[v][v] - contrib) % p
                    else:
                        # p is odd
                        # k even: i=u, j=v. Count = (p - 1) // 2
                        # k odd: i=v, j=u. Count = (p + 1) // 2
                        
                        cnt_uv = (p - 1) // 2
                        cnt_vu = (p + 1) // 2
                        
                        contrib_uv = (val * cnt_uv) % p
                        contrib_vu = (val * cnt_vu) % p
                        
                        res[u][v] = (res[u][v] - contrib_uv) % p
                        res[v][u] = (res[v][u] - contrib_vu) % p

    # Print the result
    for row in res:
        print(" ".join(map(str, row)))

if __name__ == '__main__':
    solve()