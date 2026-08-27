import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + n]))

    total = 0
    for v in a:
        total ^= v

    # Enumerate the smaller side: chosen items or their complement.
    r = k if k <= n - k else n - k
    use_complement = (k > n - k)

    ans = 0

    if r == 0:
        # K == N (K == 0 is outside constraints): only one possible choice.
        ans = total if use_complement else 0
    else:
        idx = list(range(r))
        base = n - r  # maximum allowed value for idx[i] is base + i

        while True:
            x = 0
            for i in idx:
                x ^= a[i]

            cand = (total ^ x) if use_complement else x
            if cand > ans:
                ans = cand

            # Advance to the next lexicographic combination.
            i = r - 1
            while i >= 0 and idx[i] == base + i:
                i -= 1
            if i < 0:
                break

            idx[i] += 1
            nxt = idx[i]
            for j in range(i + 1, r):
                nxt += 1
                idx[j] = nxt

    sys.stdout.write(str(ans))

if __name__ == "__main__":
    main()