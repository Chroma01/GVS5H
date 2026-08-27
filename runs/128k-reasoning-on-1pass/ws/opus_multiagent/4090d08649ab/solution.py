import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    T = n * (n + 1) // 2

    prev = [0] * (n + 2)
    pos = [[] for _ in range(n + 2)]
    term1 = 0
    i = 1
    for a in A:
        term1 += (i - prev[a]) * (n - i + 1)
        prev[a] = i
        pos[a].append(i)
        i += 1

    # miss[v] = number of subarrays containing no occurrence of v
    miss = [T] * (n + 2)
    for v in range(1, n + 1):
        P = pos[v]
        if P:
            s = 0
            pr = 0
            for p in P:
                g = p - pr - 1
                s += g * (g + 1) // 2
                pr = p
            g = n - pr
            s += g * (g + 1) // 2
            miss[v] = s

    total2 = 0
    for v in range(1, n):
        Pa = pos[v]
        if not Pa:
            continue
        Pb = pos[v + 1]
        if not Pb:
            continue
        M = Pa + Pb
        M.sort()
        s = 0
        pr = 0
        for p in M:
            g = p - pr - 1
            s += g * (g + 1) // 2
            pr = p
        g = n - pr
        s += g * (g + 1) // 2
        total2 += T - miss[v] - miss[v + 1] + s

    sys.stdout.write(str(term1 - total2) + "\n")

main()