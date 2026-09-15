import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    adj = [[] for _ in range(n)]
    max_z = 0
    idx = 2

    for _ in range(m):
        x = data[idx] - 1
        y = data[idx + 1] - 1
        z = data[idx + 2]
        idx += 3

        adj[x].append((y, z))
        adj[y].append((x, z))

        if z > max_z:
            max_z = z

    bits = max_z.bit_length()
    masks = [1 << b for b in range(bits)]

    # val[v] is the value of A_v relative to the component root.
    # -1 means unvisited.
    val = [-1] * n
    ans = [0] * n
    write = sys.stdout.write

    for s in range(n):
        if val[s] != -1:
            continue

        val[s] = 0
        stack = [s]
        comp = [s]
        has_nonzero = False

        while stack:
            u = stack.pop()
            du = val[u]

            for v, w in adj[u]:
                nd = du ^ w

                if val[v] == -1:
                    val[v] = nd
                    if nd:
                        has_nonzero = True
                    stack.append(v)
                    comp.append(v)
                elif val[v] != nd:
                    write("-1\n")
                    return

        c = 0

        # If all relative values are zero, choosing c = 0 is optimal.
        if bits and len(comp) > 1 and has_nonzero:
            size = len(comp)
            half = size >> 1
            vals = val

            for mask in masks:
                cnt = 0
                for v in comp:
                    if vals[v] & mask:
                        cnt += 1

                # Set this bit of c iff it makes fewer ones in this component.
                if cnt > half:
                    c |= mask

        for v in comp:
            ans[v] = val[v] ^ c

    write(" ".join(map(str, ans)) + "\n")


if __name__ == "__main__":
    solve()