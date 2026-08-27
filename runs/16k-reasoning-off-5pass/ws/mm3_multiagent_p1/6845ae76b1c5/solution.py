import sys
import bisect

def solve():
    import sys
    import bisect
    input = sys.stdin.readline
    
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    
    A.sort()
    B.sort()
    
    # prefix sums
    prefA = [0] * (N + 1)
    for i in range(N):
        prefA[i+1] = prefA[i] + A[i]
    prefB = [0] * (N + 1)
    for i in range(N):
        prefB[i+1] = prefB[i] + B[i]
    
    K = int(input())
    out = []
    for _ in range(K):
        X, Y = map(int, input().split())
        sumA_X = prefA[X]
        sumB_Y = prefB[Y]
        
        if X <= Y:
            total = 0
            for i in range(X):
                a = A[i]
                # count of B_j <= a in B[0..Y-1]
                cnt = bisect.bisect_right(B, a, 0, Y)
                sum_le = prefB[cnt]
                # contribution: (2*cnt - Y) * a + sumB_Y - 2*sum_le
                total += (2*cnt - Y) * a + sumB_Y - 2*sum_le
            out.append(str(total))
        else:
            total = 0
            for j in range(Y):
                b = B[j]
                # count of A_i <= b in A[0..X-1]
                cnt = bisect.bisect_right(A, b, 0, X)
                sum_le = prefA[cnt]
                # contribution: (2*cnt - X) * b + sumA_X - 2*sum_le
                total += (2*cnt - X) * b + sumA_X - 2*sum_le
            out.append(str(total))
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()