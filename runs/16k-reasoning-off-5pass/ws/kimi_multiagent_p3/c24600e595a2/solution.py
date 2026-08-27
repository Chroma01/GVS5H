import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    A = [int(x) for x in data[idx:idx+N]]; idx += N
    B = [int(x) for x in data[idx:idx+N]]; idx += N
    C = [int(x) for x in data[idx:idx+N]]; idx += N

    cnt_S = 0
    sum_out = 0   # sum of C_i over i not in S with A_i == 1
    ones = []     # C_i for i in S with A_i == 1 (flip 1 -> 0)
    zeros = []    # C_i for i in S with A_i == 0 (flip 0 -> 1)

    for i in range(N):
        a = A[i]; b = B[i]; c = C[i]
        if a != b:
            cnt_S += 1
            if a == 1:
                ones.append(c)
            else:
                zeros.append(c)
        else:
            if a == 1:
                sum_out += c

    m1 = len(ones)
    m0 = len(zeros)

    # Non-flipped positions with A=1 contribute to every operation.
    ans = sum_out * cnt_S

    # Flip all 1->0 mismatches first, largest C earliest.
    # The element flipped at slot p (1-indexed) contributes C*(p-1).
    ones.sort(reverse=True)
    for k, c in enumerate(ones):
        ans += c * k  # multipliers 0,1,...,m1-1

    # Then flip all 0->1 mismatches, smallest C earliest.
    # Element at slot p contributes C*(|S|-p+1); with slots m1+1..|S|,
    # multipliers are m0, m0-1, ..., 1 paired with ascending C.
    zeros.sort()
    for k, c in enumerate(zeros):
        ans += c * (m0 - k)

    print(ans)

main()