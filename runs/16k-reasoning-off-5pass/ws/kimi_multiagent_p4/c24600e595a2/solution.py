import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    A = [int(x) for x in data[idx:idx+N]]; idx += N
    B = [int(x) for x in data[idx:idx+N]]; idx += N
    C = [int(x) for x in data[idx:idx+N]]; idx += N

    D0 = 0
    deltas = []
    for i in range(N):
        if A[i] == 1:
            D0 += C[i]
        if A[i] != B[i]:
            if A[i] == 0:
                deltas.append(C[i])    # 0 -> 1 flip increases running dot
            else:
                deltas.append(-C[i])   # 1 -> 0 flip decreases running dot

    m = len(deltas)
    deltas.sort()  # ascending: most negative first, paired with largest weight
    total = m * D0
    weight = m
    for d in deltas:
        total += weight * d
        weight -= 1

    print(total)

main()