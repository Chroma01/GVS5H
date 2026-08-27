import sys


def solve() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    MOD = 998244353

    # Number of distinct in-degree sequences over all orientations of G
    # equals T_G(2,1) = number of forests (acyclic edge subsets) of G.
    # G = cycle C_N (vertices 0..N-1) + hub vertex N with spokes at {i : s_i='1'}.
    #
    # DP around the cycle counting forests, tracking the connectivity partition
    # of {vertex 0, current vertex i, hub h}:
    #   s0: all separate        -> a
    #   s1: 0~i, h separate     -> provably constant 1 (new_s1 = old_s1 always)
    #   s2: i~h, 0 separate     -> b
    #   s3: 0~h, i separate     -> d
    #   s4: 0~i~h all together  -> c
    # Adding vertex i+1 brings path edge {i,i+1} and (if s_{i+1}='1') spoke
    # {i+1,h}; taking both is forbidden exactly when i~h (closes a cycle).
    # Init at vertex 0 (0 and i coincide): "0 not~ h" -> s1=1;
    # "0~h" via spoke (if s_0='1') -> s4 = s_0.
    a = 0
    b = 0
    c = 1 if s[0] == '1' else 0
    d = 0

    for ch in s[1:]:
        if ch == '1':
            a, b, c, d = (
                (2 * (a + d) + b + 1) % MOD,
                (2 * (a + b) + 1) % MOD,
                (2 * (c + d) + 1) % MOD,
                c,
            )
        else:
            a, d = (2 * (a + d) + b + 1) % MOD, c

    # Closing edge {N-1,0}: freely optional unless 0~N-1 already
    # (states 1 and 4 -> factor 1; states 0,2,3 -> factor 2).
    ans = (2 * a + 2 * b + 2 * d + c + 1) % MOD
    print(ans)


solve()