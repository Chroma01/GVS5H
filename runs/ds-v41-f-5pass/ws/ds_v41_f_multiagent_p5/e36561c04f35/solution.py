import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        A = list(map(int, data[idx:idx+n])); idx += n

        # Online process: maintain groups with sizes.
        # For each element, either extend the current group of its value
        # (cost = number of elements in groups after it) or create a new group
        # at the end (cost = 1).
        # Greedy rule used here: create a new group iff the extend cost > 1.
        G = 0
        cur = {}
        bit = [0] * (n + 2)

        def bit_add(i, v):
            while i <= n:
                bit[i] += v
                i += i & -i

        def bit_sum(i):
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & -i
            return s

        cost = 0
        total = 0
        for x in A:
            total += 1
            if x not in cur:
                G += 1
                cur[x] = G
                bit_add(G, 1)
                cost += 1
            else:
                g = cur[x]
                prefix = bit_sum(g)
                cost_extend = (total - 1) - prefix
                if cost_extend > 1:
                    G += 1
                    cur[x] = G
                    bit_add(G, 1)
                    cost += 1
                else:
                    cost += cost_extend
                    bit_add(g, 1)
        out.append(str(cost))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()