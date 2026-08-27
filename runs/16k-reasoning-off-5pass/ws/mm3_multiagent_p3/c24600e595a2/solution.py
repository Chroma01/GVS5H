import sys

def solve():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    A = list(map(int, data[idx:idx+N])); idx += N
    B = list(map(int, data[idx:idx+N])); idx += N
    C = list(map(int, data[idx:idx+N])); idx += N

    S = 0          # initial weighted sum of A
    sum_10 = 0     # sum of C_i for positions where A_i=1, B_i=0
    sum_01 = 0     # sum of C_i for positions where A_i=0, B_i=1
    x = 0          # count of 1->0 flips
    y = 0          # count of 0->1 flips

    for i in range(N):
        if A[i] == 1:
            S += C[i]
            if B[i] == 0:
                x += 1
                sum_10 += C[i]
        else:  # A[i] == 0
            if B[i] == 1:
                y += 1
                sum_01 += C[i]

    ans = x * S + y * (S - sum_10) + sum_01
    print(ans)

if __name__ == "__main__":
    solve()