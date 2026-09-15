import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M, A, B = data[0], data[1], data[2], data[3]
    flat = []
    block_starts = []
    block_ends = []
    start = 1
    idx = 4
    def add_block(l, r):
        s = len(flat)
        left_end = l + B - 1
        if left_end > r:
            left_end = r
        right_start = r - B + 1
        if right_start < l:
            right_start = l
        if right_start <= left_end + 1:
            flat.extend(range(l, r + 1))
        else:
            flat.extend(range(l, left_end + 1))
            flat.extend(range(right_start, r + 1))
        block_starts.append(s)
        block_ends.append(len(flat))
    for _ in range(M):
        L = data[idx]; R = data[idx+1]; idx += 2
        if start <= L - 1:
            add_block(start, L - 1)
        start = R + 1
    if start <= N:
        add_block(start, N)
    P = len(flat)
    reach = bytearray(P)
    if P == 0:
        print("No")
        return
    reach[0] = 1
    max_len = 2 * B + 5
    ones = [b''] * (max_len + 1)
    for i in range(1, max_len + 1):
        ones[i] = ones[i-1] + b'\x01'
    flat_l = flat
    reach_l = reach
    P_l = P
    A_l = A
    B_l = B
    j_start = 0
    j_end = 0
    nb = len(block_starts)
    if A == 1:
        for bi in range(nb):
            s = block_starts[bi]; e = block_ends[bi]
            f = s
            while f < e and not reach_l[f]:
                f += 1
            if f < e:
                reach_l[f:e] = ones[e - f]
            for i in range(s, e):
                if not reach_l[i]:
                    continue
                p = flat_l[i]
                while j_end < P_l and flat_l[j_end] <= p + B_l:
                    j_end += 1
                while j_start < P_l and flat_l[j_start] < p + A_l:
                    j_start += 1
                start_k = e if e > j_start else j_start
                if start_k < j_end:
                    reach_l[start_k:j_end] = ones[j_end - start_k]
    elif A == B:
        mod = A
        for bi in range(nb):
            s = block_starts[bi]; e = block_ends[bi]
            # optional quick any? build res_lists
            res_lists = {}
            for pos_idx in range(s, e):
                r = flat_l[pos_idx] % mod
                lst = res_lists.get(r)
                if lst is None:
                    res_lists[r] = [pos_idx]
                else:
                    lst.append(pos_idx)
            processed = [False] * mod
            for i in range(s, e):
                if not reach_l[i]:
                    continue
                r = flat_l[i] % mod
                if not processed[r]:
                    processed[r] = True
                    for k in res_lists[r]:
                        if k > i:
                            reach_l[k] = 1
                p = flat_l[i]
                while j_end < P_l and flat_l[j_end] <= p + B_l:
                    j_end += 1
                while j_start < P_l and flat_l[j_start] < p + A_l:
                    j_start += 1
                start_k = e if e > j_start else j_start
                if start_k < j_end:
                    reach_l[start_k:j_end] = ones[j_end - start_k]
    else:
        threshold = A * (A - 1)
        pre = [False] * threshold
        for d in range(1, threshold):
            pre[d] = (d + B - 1) // B <= d // A
        for bi in range(nb):
            s = block_starts[bi]; e = block_ends[bi]
            for i in range(s, e):
                if not reach_l[i]:
                    continue
                p = flat_l[i]
                # same interval edges
                for k in range(i + 1, e):
                    d = flat_l[k] - p
                    if d >= threshold:
                        if k < e:
                            reach_l[k:e] = ones[e - k]
                        break
                    if pre[d]:
                        reach_l[k] = 1
                while j_end < P_l and flat_l[j_end] <= p + B_l:
                    j_end += 1
                while j_start < P_l and flat_l[j_start] < p + A_l:
                    j_start += 1
                start_k = e if e > j_start else j_start
                if start_k < j_end:
                    reach_l[start_k:j_end] = ones[j_end - start_k]
    print("Yes" if reach_l[P_l - 1] else "No")

if __name__ == "__main__":
    solve()