import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + n]))

    total = 0
    for x in a:
        total ^= x

    if k > n - k:
        # Exclude mode: choose which (n - k) elements to remove.
        r = n - k
        base = total  # candidate = total XOR (xor of excluded)
        exclude = True
    else:
        r = k
        base = 0
        exclude = False

    if r == 0:
        # K == N: only one possible choice, the XOR of all elements.
        print(total)
        return

    best = -1
    # Iterative combination enumeration using an index array.
    idx = list(range(r))
    cur = 0
    for i in range(r):
        cur ^= a[i]
    cand = (base ^ cur) if exclude else cur
    if cand > best:
        best = cand

    while True:
        # Find the rightmost index that can be incremented.
        i = r - 1
        while i >= 0 and idx[i] == n - r + i:
            i -= 1
        if i < 0:
            break
        # XOR out the old value at position i, advance it, XOR in the new value.
        old = idx[i]
        cur ^= a[old]
        idx[i] = old + 1
        cur ^= a[old + 1]
        # Reset the tail positions to consecutive values, updating the running XOR.
        for j in range(i + 1, r):
            cur ^= a[idx[j]]
            idx[j] = idx[j - 1] + 1
            cur ^= a[idx[j]]
        cand = (base ^ cur) if exclude else cur
        if cand > best:
            best = cand

    print(best)

main()