import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    K = int(data[1])
    A = list(map(int, data[2:2 + n]))

    total = 0
    for x in A:
        total ^= x

    # Enumerate the smaller side: k = min(K, N-K).
    # XOR of K chosen = total ^ (XOR of the N-K unchosen).
    use_complement = K > n - K
    k = n - K if use_complement else K

    if k == 0:
        # K == N: must choose everything.
        print(total)
        return

    # First combination: 0,1,...,k-1
    comb = list(range(k))
    cur = 0
    for i in comb:
        cur ^= A[i]
    best = (total ^ cur) if use_complement else cur

    # Lexicographic next-combination generation with incremental XOR update.
    # Local variable binding for speed.
    a = A
    c = comb
    kk = k
    nn = n
    use_comp = use_complement
    tot = total

    while True:
        i = kk - 1
        # Find rightmost index that can be incremented.
        while i >= 0 and c[i] == nn - kk + i:
            i -= 1
        if i < 0:
            break
        # XOR out old tail values (positions i..k-1)
        for j in range(i, kk):
            cur ^= a[c[j]]
        c[i] += 1
        for j in range(i + 1, kk):
            c[j] = c[j - 1] + 1
        # XOR in new tail values
        for j in range(i, kk):
            cur ^= a[c[j]]
        cand = (tot ^ cur) if use_comp else cur
        if cand > best:
            best = cand

    print(best)

solve()