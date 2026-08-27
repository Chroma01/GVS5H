import sys

def small_count(a, n):
    s = set(a)
    contains = s.__contains__
    ans = 0
    for i in range(n - 1):
        ai = a[i]
        for j in range(i + 1, n):
            t = ai + a[j]
            if (t & 1) == 0 and contains(t >> 1):
                ans += 1
    return ans

def big_count(a, n, mn, L):
    e_len = L // 2 + 1
    o_len = L // 2 + 1
    e_ba = bytearray((20 * e_len + 7) // 8)
    o_ba = bytearray((20 * o_len + 7) // 8)

    for i, v in enumerate(a):
        t = v - mn
        a[i] = t
        k = t >> 1
        byte_i = (5 * k) >> 1
        bit = 16 if (k & 1) else 1
        if t & 1:
            o_ba[byte_i] = bit
        else:
            e_ba[byte_i] = bit

    e = int.from_bytes(e_ba, 'little')
    o = int.from_bytes(o_ba, 'little')
    del e_ba, o_ba

    e2 = e * e
    o2 = o * o
    del e, o

    req_e = (20 * (2 * e_len) + 7) // 8 + 3
    req_o = (20 * (2 * o_len) + 7) // 8 + 3
    eb = e2.to_bytes(req_e, 'little')
    ob = o2.to_bytes(req_o, 'little')
    del e2, o2

    ans = 0
    mask = 0xFFFFF
    eb_l = eb
    ob_l = ob
    for x in a:
        k = x >> 1
        if x & 1:
            base = 5 * k
            off = base + 2
            ex = (eb_l[off] | (eb_l[off + 1] << 8) | (eb_l[off + 2] << 16)) >> 4
            off = base
            ox = (ob_l[off] | (ob_l[off + 1] << 8) | (ob_l[off + 2] << 16)) & mask
        else:
            base = 5 * k
            off = base
            ex = (eb_l[off] | (eb_l[off + 1] << 8) | (eb_l[off + 2] << 16)) & mask
            if x:
                off = base - 3
                ox = (ob_l[off] | (ob_l[off + 1] << 8) | (ob_l[off + 2] << 16)) >> 4
            else:
                ox = 0
        ans += (ex + ox - 1) >> 1
    return ans

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    if n < 3:
        print(0)
        return
    a = list(map(int, data[1:1 + n]))
    del data
    mn = min(a)
    mx = max(a)
    L = mx - mn
    if n == L + 1:
        ans = ((n - 1) // 2) * (n // 2)
    elif n <= 2000:
        ans = small_count(a, n)
    else:
        ans = big_count(a, n, mn, L)
    print(ans)

if __name__ == '__main__':
    main()