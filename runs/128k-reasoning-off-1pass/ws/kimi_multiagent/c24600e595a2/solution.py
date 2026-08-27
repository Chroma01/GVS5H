import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = [int(x) for x in data[pos:pos+N]]; pos += N
    B = [int(x) for x in data[pos:pos+N]]; pos += N
    C = [int(x) for x in data[pos:pos+N]]; pos += N

    DR = []  # required downs: A=1, B=0
    UR = []  # required ups:   A=0, B=1
    OP = []  # optional (A=1, B=1): may be flipped down then up as a "shield"
    for a, b, c in zip(A, B, C):
        if a == 1 and b == 0:
            DR.append(c)
        elif a == 0 and b == 1:
            UR.append(c)
        elif a == 1 and b == 1:
            OP.append(c)
        # a == 0, b == 0: flipping never helps

    DR.sort()
    UR.sort()
    OP.sort(reverse=True)

    def prefix_sums(arr):
        pref = [0] * (len(arr) + 1)
        for i, v in enumerate(arr):
            pref[i+1] = pref[i] + v
        return pref

    prefDR = prefix_sums(DR)
    prefUR = prefix_sums(UR)

    def pairs_min(arr):
        # arr ascending; sum over unordered pairs of min = sum_i v_i * (k-1-i)
        k = len(arr)
        total = 0
        for i, v in enumerate(arr):
            total += v * (k - 1 - i)
        return total

    m0 = len(DR) + len(UR)
    sumOP = sum(OP)

    # Total(0): no optional activated; inactive optionals stay 1 for all m0 ops
    total = pairs_min(DR) + pairs_min(UR) + sum(UR) + sumOP * m0
    ans = total

    K = len(OP)
    suff = [0] * (K + 1)  # suff[t] = sum of OP[t:]
    for t in range(K - 1, -1, -1):
        suff[t] = suff[t+1] + OP[t]

    lenDR = len(DR)
    lenUR = len(UR)

    for t in range(1, K + 1):
        c = OP[t-1]
        idx = bisect_left(DR, c)          # first DR index with value >= c
        cntGE_DR = lenDR - idx
        sumLT_DR = prefDR[idx]
        idx2 = bisect_left(UR, c)
        cntGE_UR = lenUR - idx2
        sumLT_UR = prefUR[idx2]

        m_prev = m0 + 2 * (t - 1)
        delta = (c * (cntGE_DR + (t - 1)) + sumLT_DR
                 + c * (cntGE_UR + (t - 1)) + sumLT_UR
                 + c
                 + 2 * suff[t] - c * m_prev)
        total += delta
        if total < ans:
            ans = total

    print(ans)

main()