import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    s = data[1]
    MOD = 998244353

    # 7-state DP (groups of states related by complement symmetry).
    # x = relation state 15, y = 9, u = {5,10}, v = {1,8},
    # w = {2,4}, z = {3,12}, q = {11,13}.  Start = identity relation 9.
    x = 0
    y = 1
    u = 0
    v = 0
    w = 0
    z = 0
    q = 0

    for ch in s:
        if ch == 48:  # '0' : labels {0,1,2}
            nu = (x + 2 * u + q) % MOD
            nv = (v + w + z) % MOD
            nw = (y + v + w + z + q) % MOD
            u, v, w = nu, nv, nw
            # x, y, z, q unchanged
        else:         # '1' : labels {0,1,2,3}
            nx = (2 * x + 2 * u + 2 * q) % MOD
            nu = (x + 2 * u + q) % MOD
            nv = (v + w + z) % MOD
            nw = (y + v + w + z + q) % MOD
            nz = (v + w + 2 * z) % MOD
            nq = (y + q) % MOD
            x, u, v, w, z, q = nx, nu, nv, nw, nz, nq
            y = 0

    # accepting groups: x, y, {u}, {v}, {z}, {q}; w rejects
    ans = (x + y + 2 * u + 2 * v + 2 * z + 2 * q) % MOD
    sys.stdout.write(str(ans) + "\n")

main()