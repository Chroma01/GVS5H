import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    Y = int(data[idx]); idx += 1
    S = data[idx]; idx += 1
    T = data[idx]; idx += 1

    # Precompute right_run[i] = length of maximal run of S[i] starting at i.
    right_run = [0] * N
    for i in range(N - 1, -1, -1):
        if i == N - 1:
            right_run[i] = 1
        elif S[i] == S[i + 1]:
            right_run[i] = right_run[i + 1] + 1
        else:
            right_run[i] = 1

    i = 0  # pointer in S
    j = 0  # pointer in T

    while j < N:
        if i >= N:
            print("No")
            return

        if S[i] == T[j]:
            i += 1
            j += 1
        elif S[i] == '0':
            if right_run[i] >= X:
                i += X
            else:
                print("No")
                return
        else:  # S[i] == '1'
            if right_run[i] >= Y:
                i += Y
            else:
                print("No")
                return

    print("Yes")

if __name__ == "__main__":
    solve()