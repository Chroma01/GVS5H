import sys
import bisect

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    arrA = list(map(int, data[idx:idx+n])); idx += n
    arrB = list(map(int, data[idx:idx+n])); idx += n
    arrC = list(map(int, data[idx:idx+n])); idx += n

    # R: must turn 1->0 ; T: must turn 0->1 ; M: A=B=1, optional off/on
    R = []; T = []; M = []
    for i in range(n):
        a = arrA[i]; b = arrB[i]
        if a == 1 and b == 0:
            R.append(arrC[i])
        elif a == 0 and b == 1:
            T.append(arrC[i])
        elif a == 1 and b == 1:
            M.append(arrC[i])

    R.sort(reverse=True)   # offs: descending C
    T.sort()               # ons: ascending C
    M.sort(reverse=True)   # optional offs: descending C

    r = len(R); q = len(T); s = len(M)

    PM = [0]*(s+1)     # prefix sums of M (desc)
    PjM = [0]*(s+1)
    for j in range(1, s+1):
        v = M[j-1]
        PM[j] = PM[j-1] + v
        PjM[j] = PjM[j-1] + j*v
    CM = PM[s]

    SumT = sum(T)
    SD = 0
    for i in range(q):
        SD += (i+1)*T[i]
    SA = 0
    for i in range(r):
        SA += i*R[i]

    Masc = M[::-1]     # ascending
    Rasc = R[::-1]     # ascending

    # g[i] = #{mu >= R[i]}
    g = [0]*r
    for i in range(r):
        g[i] = s - bisect.bisect_left(Masc, R[i])

    prefixH = [0]*(r+1)
    for i in range(r):
        prefixH[i+1] = prefixH[i] + R[i]*g[i]
    suffixR = [0]*(r+1)
    for i in range(r-1, -1, -1):
        suffixR[i] = suffixR[i+1] + R[i]

    prefixC = [0]*(s+1)
    prefixD = [0]*(s+1)
    for j in range(1, s+1):
        v = M[j-1]
        grgt = r - bisect.bisect_right(Rasc, v)    # #{rho > v}
        prefixC[j] = prefixC[j-1] + v*grgt
        gtlt = bisect.bisect_left(T, v)            # #{t < v}
        prefixD[j] = prefixD[j-1] + v*gtlt

    # delta[i] = #{mu > T[i]}
    delta = [0]*q
    for i in range(q):
        delta[i] = s - bisect.bisect_right(Masc, T[i])

    suffixT = [0]*(q+1)
    suffixTD = [0]*(q+1)
    for i in range(q-1, -1, -1):
        suffixT[i] = suffixT[i+1] + T[i]
        suffixTD[i] = suffixTD[i+1] + T[i]*delta[i]

    ans = None
    bi = 0      # count of g[i] <= p
    i0 = q      # first index with delta[i] < p
    for p in range(s+1):
        while bi < r and g[bi] <= p:
            bi += 1
        Bval = prefixH[bi] + p*suffixR[bi]

        while i0 > 0 and delta[i0-1] < p:
            i0 -= 1
        E = p*suffixT[i0] - suffixTD[i0]

        m = r + q + 2*p
        K = CM - PM[p]
        phase1 = SA + Bval + prefixC[p] + (PjM[p] - PM[p])
        bb = q + p
        phase2 = ((bb+1)*SumT - SD - E) + (bb*PM[p] - prefixD[p] - p*PM[p] + PjM[p])
        total = m*K + phase1 + phase2
        if ans is None or total < ans:
            ans = total

    print(ans)

main()