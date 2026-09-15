import sys
import math

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    ptr = 0
    N = data[ptr]; ptr += 1
    A = data[ptr:ptr+N]; ptr += N
    B = data[ptr:ptr+N]; ptr += N
    K = data[ptr]; ptr += 1
    X_list = [0]*K
    Y_list = [0]*K
    for k in range(K):
        X_list[k] = data[ptr]; ptr += 1
        Y_list[k] = data[ptr]; ptr += 1

    S = max(1, int(N / math.sqrt(K)))
    if S > N:
        S = N
    Pmax = N // S
    Qmax = N // S

    p_list = [x // S for x in X_list]
    q_list = [y // S for y in Y_list]

    p_groups = [[] for _ in range(Pmax+1)]
    for k in range(K):
        p_groups[p_list[k]].append((Y_list[k], q_list[k], k))
    q_groups = [[] for _ in range(Qmax+1)]
    for k in range(K):
        q_groups[q_list[k]].append((X_list[k], k))

    P_val = [0]*K
    C_val = [0]*K
    Q_val = [0]*K

    # Sweep P
    orderB = sorted(range(N), key=lambda i: B[i])
    B_sorted = [B[i] for i in orderB]
    B_pairs = list(zip(B_sorted, orderB))
    H = [0]*N
    for p in range(Pmax+1):
        if p > 0:
            block = A[(p-1)*S : p*S]
            block.sort()
            sz = S
            sum_total = sum(block)
            ptr = 0
            sum_le = 0
            H_local = H
            block_local = block
            for b_val, orig in B_pairs:
                while ptr < sz and block_local[ptr] <= b_val:
                    sum_le += block_local[ptr]
                    ptr += 1
                H_local[orig] += b_val * (2*ptr - sz) + sum_total - 2*sum_le
        if p_groups[p]:
            events = []
            for Y, q, idx in p_groups[p]:
                events.append((Y, idx, 0))
                events.append((q*S, idx, 1))
            events.sort()
            run = 0
            j = 0
            for thresh, idx, typ in events:
                while j < thresh:
                    run += H[j]
                    j += 1
                if typ == 0:
                    P_val[idx] = run
                else:
                    C_val[idx] = run

    # Sweep Q
    orderA = sorted(range(N), key=lambda i: A[i])
    A_sorted = [A[i] for i in orderA]
    A_pairs = list(zip(A_sorted, orderA))
    H2 = [0]*N
    for q in range(Qmax+1):
        if q > 0:
            block = B[(q-1)*S : q*S]
            block.sort()
            sz = S
            sum_total = sum(block)
            ptr = 0
            sum_le = 0
            H2_local = H2
            block_local = block
            for a_val, orig in A_pairs:
                while ptr < sz and block_local[ptr] <= a_val:
                    sum_le += block_local[ptr]
                    ptr += 1
                H2_local[orig] += a_val * (2*ptr - sz) + sum_total - 2*sum_le
        if q_groups[q]:
            events = []
            for X, idx in q_groups[q]:
                events.append((X, idx))
            events.sort()
            run = 0
            j = 0
            for thresh, idx in events:
                while j < thresh:
                    run += H2[j]
                    j += 1
                Q_val[idx] = run

    # Tailtail and answers
    out = []
    for k in range(K):
        X = X_list[k]
        Y = Y_list[k]
        p = p_list[k]
        q = q_list[k]
        startA = p*S
        startB = q*S
        A_tail = A[startA:X]
        B_tail = B[startB:Y]
        total = 0
        if A_tail and B_tail:
            A_tail.sort()
            B_tail.sort()
            szB = len(B_tail)
            sumB = sum(B_tail)
            ptr = 0
            sum_le = 0
            for a in A_tail:
                while ptr < szB and B_tail[ptr] <= a:
                    sum_le += B_tail[ptr]
                    ptr += 1
                total += a * ptr - sum_le + (sumB - sum_le) - a * (szB - ptr)
        ans = P_val[k] + Q_val[k] - C_val[k] + total
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()