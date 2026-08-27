import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    intervals = []
    full = -1
    for i in range(M):
        L = int(next(it))
        R = int(next(it))
        intervals.append((L, R, i))
        if L == 1 and R == N:
            full = i

    ops = [0] * M

    def emit(k):
        sys.stdout.write(str(k) + "\n" + " ".join(map(str, ops)) + "\n")

    if full != -1:
        ops[full] = 1
        emit(1)
        return

    arr = sorted(intervals, key=lambda x: (x[0], x[1]))
    max_r = -1
    max_i = -1
    min_r = N + 1
    min_i = -1

    for L, R, i in arr:
        if max_r >= R:
            ops[max_i] = 1
            ops[i] = 2
            emit(2)
            return
        if min_r < L:
            ops[min_i] = 2
            ops[i] = 2
            emit(2)
            return
        if R > max_r:
            max_r = R
            max_i = i
        if R < min_r:
            min_r = R
            min_i = i

    p = 0
    while p < M:
        q = p + 1
        while q < M and arr[q][0] == arr[p][0]:
            q += 1
        if q - p >= 2:
            gi = arr[p][2]
            gr = arr[p][1]
            mi = arr[p][2]
            mr = arr[p][1]
            for k in range(p, q):
                Lk, Rk, ik = arr[k]
                if Rk > gr:
                    gr = Rk
                    gi = ik
                if Rk < mr:
                    mr = Rk
                    mi = ik
            if gi == mi:
                for k in range(p, q):
                    if arr[k][2] != gi:
                        mi = arr[k][2]
                        break
            ops[gi] = 1
            ops[mi] = 2
            emit(2)
            return
        p = q

    a = -1
    ia = -1
    b = N + 1
    ib = -1
    for L, R, i in intervals:
        if L == 1 and R > a:
            a = R
            ia = i
        if R == N and L < b:
            b = L
            ib = i
    if ia != -1 and ib != -1 and a + 1 >= b:
        if ia == ib:
            ops[ia] = 1
            emit(1)
            return
        ops[ia] = 1
        ops[ib] = 1
        emit(2)
        return

    if M >= 3:
        min_l = N + 1
        il = -1
        max_r2 = -1
        ir = -1
        for L, R, i in intervals:
            if L < min_l:
                min_l = L
                il = i
            if R > max_r2:
                max_r2 = R
                ir = i
        if il == ir:
            ops[il] = 1
            c = 0
            for i in range(M):
                if i != il:
                    ops[i] = 2
                    c += 1
                    if c == 2:
                        break
        else:
            ops[il] = 2
            ops[ir] = 2
            for i in range(M):
                if i != il and i != ir:
                    ops[i] = 1
                    break
        emit(3)
        return

    sys.stdout.write("-1\n")

if __name__ == "__main__":
    solve()