import sys
sys.setrecursionlimit(1 << 25)


def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); X = int(data[1]); Y = int(data[2])
    S = data[3].decode()
    T = data[4].decode()

    if S == T:
        print("Yes")
        return

    # No operation possible at all
    if X + Y > n:
        print("No")
        return

    # Positions of 1s (0-indexed)
    ps = [i for i, c in enumerate(S) if c == '1']
    pt = [i for i, c in enumerate(T) if c == '1']
    k = len(ps)
    if k != len(pt):
        print("No")
        return
    if k == 0 or k == n:
        print("No")  # S != T impossible with all-equal strings
        return

    g = abs(X - Y)
    if g == 0:
        g = X  # slide unit when X == Y

    # Per-1 mod-g invariant
    for a, b in zip(ps, pt):
        if (a - b) % g != 0:
            print("No")
            return

    # Feasibility: simulate sliding 1s left/right by unit g.
    # A 1 can cross a 0 only in chunks: effectively each 1's reachable set is
    # an interval; we check the order-preserving matching via greedy bounds.

    # Compute for each 1 in S the leftmost reachable position, and match.
    # Movement constraint: a block of Y ones needs X zeros to its left to swap
    # (op A moves ones left by X-Y... net left movement requires X<Y case care).
    # Unified model: each 1 can move freely within its "g-lane" as long as the
    # string's 1-count prefix constraints hold; ends act as walls when the
    # leading/trailing run is too short.

    # Determine frozen prefix: leading run of S
    def lead_run(s):
        c = s[0]; i = 0
        while i < n and s[i] == c:
            i += 1
        return c, i

    def trail_run(s):
        c = s[-1]; i = n - 1
        cnt = 0
        while i >= 0 and s[i] == c:
            cnt += 1; i -= 1
        return c, cnt

    # Check via simulating the actual process greedily:
    # Move ones of S to match T using a stack-based approach on g-lanes.
    # Since each 1 stays in its mod-g class and order is preserved, and any
    # interior configuration is reachable, the only obstruction is at the ends.
    # We verify by attempting to transform S into T with a direct constructive
    # simulation on the run structure.

    # Constructive check: align ones one by one from left to right.
    s = list(S)
    ps_list = [i for i, c in enumerate(s) if c == '1']
    for idx in range(k):
        target = pt[idx]
        cur = ps_list[idx]
        if cur == target:
            continue
        diff = target - cur  # multiple of g
        # We move the idx-th 1 by swapping blocks; simulate at bit level using
        # the operation that moves a 1 left (op A moves Y ones left over X zeros
        # when X<Y net... ) — instead simulate abstractly: shift this single 1
        # by repeatedly swapping with adjacent 0s is NOT always legal.
        # Legal net move of a single boundary by g requires the block op.
        # We simulate the run-level transfer: moving the idx-th 1 left by g
        # corresponds to op A (if X>Y, boundary slides right by X-Y... ).
        # For correctness we do a direct local rewrite: moving one '1' across
        # '0's by distance g is achievable iff there is room; we emulate by
        # actually performing the swap of blocks around this position.
        step = g
        if diff < 0:
            # move left by -diff
            move = -diff
            # need to shift this 1 left across zeros; emulate block swaps
            # find the run of zeros immediately to the left of this 1's block
            # We perform: while move>0: apply op A at appropriate i
            # Locate current position of this 1
            p = ps_list[idx]
            while move > 0:
                # op A: 0^X 1^Y -> 1^Y 0^X moves a 1-block left by (X - Y)?
                # net left shift of ones happens when Y > X? Actually op A turns
                # 0..01..1 into 1..10..0: ones move LEFT by X, zeros move RIGHT by Y.
                # So a single boundary between 0-run and 1-run moves left by X
                # in terms of the 1-block start. The slide unit is g=|X-Y| per
                # the invariant, meaning combined ops shift by g.
                # Simplest: directly rewrite bits to move this 1 left by g,
                # assuming feasibility (interior). Check room:
                if p - g < 0:
                    print("No")
                    return
                # shift the 1 at p left by g: positions p-g..p-1 must be 0s
                # (they are, since previous 1 is at ps_list[idx-1] <= target)
                for j in range(p - g, p):
                    if s[j] == '1':
                        print("No")
                        return
                s[p] = '0'
                s[p - g] = '1'
                p -= g
                move -= g
            ps_list[idx] = p
        else:
            move = diff
            p = ps_list[idx]
            while move > 0:
                if p + g >= n:
                    print("No")
                    return
                for j in range(p + 1, p + g + 1):
                    if s[j] == '1':
                        print("No")
                        return
                s[p] = '0'
                s[p + g] = '1'
                p += g
                move -= g
            ps_list[idx] = p

    if ''.join(s) == T:
        print("Yes")
    else:
        print("No")


solve()