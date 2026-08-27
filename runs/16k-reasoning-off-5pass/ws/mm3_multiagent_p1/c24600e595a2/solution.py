import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    A = [int(data[idx + i]) for i in range(N)]; idx += N
    B = [int(data[idx + i]) for i in range(N)]; idx += N
    C = [int(data[idx + i]) for i in range(N)]; idx += N
    
    S = 0
    off = []  # positions where A=1, B=0, need to flip 1->0
    on = []   # positions where A=0, B=1, need to flip 0->1
    for i in range(N):
        S += A[i] * C[i]
        if A[i] == 1 and B[i] == 0:
            off.append(C[i])
        elif A[i] == 0 and B[i] == 1:
            on.append(C[i])
    
    # Flip 1->0 first in decreasing C order to reduce S as much as possible early
    off.sort(reverse=True)
    # Then flip 0->1 in increasing C order to keep S low
    on.sort()
    
    total = 0
    for c in off:
        S -= c
        total += S
    for c in on:
        S += c
        total += S
    
    print(total)

main()