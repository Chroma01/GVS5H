import sys


def mask_to_str(mask, n):
    return ''.join('1' if (mask >> i) & 1 else '0' for i in range(n))


def run_checker(max_n=8):
    # Brute-force verification for all N <= 8 and all 1 <= X,Y <= N.
    # Bit position 0 is the first character of the string.
    for n in range(1, max_n + 1):
        m = 1 << n
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                parent = list(range(m))
                rank = [0] * m

                def find(a):
                    while parent[a] != a:
                        parent[a] = parent[parent[a]]
                        a = parent[a]
                    return a

                def union(a, b):
                    ra = find(a)
                    rb = find(b)
                    if ra == rb:
                        return
                    if rank[ra] < rank[rb]:
                        ra, rb = rb, ra
                    parent[rb] = ra
                    if rank[ra] == rank[rb]:
                        rank[ra] += 1

                # Add all one-step moves.
                # Operation A: 0^X 1^Y -> 1^Y 0^X
                # Operation B: 1^Y 0^X -> 0^X 1^Y
                if x + y <= n:
                    full = (1 << (x + y)) - 1
                    pat_a = ((1 << y) - 1) << x
                    pat_b = (1 << y) - 1
                    limit = n - x - y + 1

                    for mask in range(m):
                        for i in range(limit):
                            seg = (mask >> i) & full
                            if seg == pat_a:
                                nm = (mask & ~(full << i)) | (pat_b << i)
                                union(mask, nm)
                            elif seg == pat_b:
                                nm = (mask & ~(full << i)) | (pat_a << i)
                                union(mask, nm)

                roots = [find(i) for i in range(m)]

                # Candidate complete invariant:
                # (number of ones, ordered one positions modulo X,
                #  ordered zero positions modulo Y)
                inv = []
                for mask in range(m):
                    ones = []
                    zeros = []
                    for pos in range(n):
                        if (mask >> pos) & 1:
                            ones.append(pos % x)
                        else:
                            zeros.append(pos % y)
                    inv.append((len(ones), ones, zeros))

                # Check exact equality of reachability classes and invariant classes.
                for a in range(m):
                    ra = roots[a]
                    ia = inv[a]
                    for b in range(a + 1, m):
                        same_class = (ra == roots[b])
                        same_inv = (ia == inv[b])
                        if same_class != same_inv:
                            print("Counterexample found")
                            print(f"N={n} X={x} Y={y}")
                            print(f"S={mask_to_str(a, n)}")
                            print(f"T={mask_to_str(b, n)}")
                            print(f"same_class={same_class} same_inv={same_inv}")
                            print(f"invS={ia}")
                            print(f"invT={inv[b]}")
                            return

    print("No counterexample found for N<=8")


def solve():
    data = sys.stdin.read().strip().split()

    # If no input is supplied, run the brute-force checker.
    if not data:
        run_checker()
        return

    # If input is supplied, solve the original problem.
    if len(data) < 5:
        run_checker()
        return

    n = int(data[0])
    x = int(data[1])
    y = int(data[2])
    s = data[3]
    t = data[4]

    if s.count('1') != t.count('1'):
        print("No")
        return

    def invariant(st):
        ones = []
        zeros = []
        for i, ch in enumerate(st):
            if ch == '1':
                ones.append(i % x)
            else:
                zeros.append(i % y)
        return (len(ones), ones, zeros)

    print("Yes" if invariant(s) == invariant(t) else "No")


if __name__ == "__main__":
    solve()