import sys
import struct

MAX_VALUE = 1000000


def read_input():
    data = sys.stdin.buffer.read()
    present = bytearray(MAX_VALUE + 1)

    num = 0
    in_num = False
    first = True

    even_count = 0
    odd_count = 0
    max_s = 0
    max_even = 0
    max_odd = 0

    for c in data:
        # Input contains only digits and whitespace; whitespace bytes are < 48.
        if c >= 48:
            num = num * 10 + (c - 48)
            in_num = True
        elif in_num:
            if first:
                first = False
            else:
                present[num] = 1
                if num > max_s:
                    max_s = num
                if num & 1:
                    odd_count += 1
                    if num > max_odd:
                        max_odd = num
                else:
                    even_count += 1
                    if num > max_even:
                        max_even = num
            num = 0
            in_num = False

    if in_num and not first:
        present[num] = 1
        if num > max_s:
            max_s = num
        if num & 1:
            odd_count += 1
            if num > max_odd:
                max_odd = num
        else:
            even_count += 1
            if num > max_even:
                max_even = num

    return present, even_count, odd_count, max_s, max_even, max_odd


def padded_bytes(sq, max_idx, base):
    if max_idx < 0:
        max_idx = 0
    need = (base * (max_idx + 1) + 7) >> 3
    bl = (sq.bit_length() + 7) >> 3
    if bl > need:
        need = bl
    return sq.to_bytes(need + 8, 'little')


def main():
    present, even_count, odd_count, max_s, max_even, max_odd = read_input()
    n = even_count + odd_count

    if n < 3:
        print(0)
        return

    base = max(even_count, odd_count).bit_length()
    if base < 1:
        base = 1
    mask = (1 << base) - 1

    if even_count:
        even_arr = bytearray((base * ((max_even >> 1) + 1) + 7) >> 3)
    else:
        even_arr = None

    if odd_count:
        odd_arr = bytearray((base * ((max_odd >> 1) + 1) + 7) >> 3)
    else:
        odd_arr = None

    pres = present
    b = base

    if even_count:
        arr = even_arr
        pos = b
        for u in range(1, (max_even >> 1) + 1):
            if pres[u << 1]:
                arr[pos >> 3] |= 1 << (pos & 7)
            pos += b

    if odd_count:
        arr = odd_arr
        pos = 0
        for u in range(0, (max_odd >> 1) + 1):
            if pres[(u << 1) + 1]:
                arr[pos >> 3] |= 1 << (pos & 7)
            pos += b

    if even_count:
        even_int = int.from_bytes(even_arr, 'little')
        del even_arr
        even_sq = even_int * even_int
        del even_int
        even_data = padded_bytes(even_sq, max_s, base)
        del even_sq
    else:
        even_data = None

    if odd_count:
        odd_int = int.from_bytes(odd_arr, 'little')
        del odd_arr
        odd_sq = odd_int * odd_int
        del odd_int
        odd_data = padded_bytes(odd_sq, max_s - 1, base)
        del odd_sq
    else:
        odd_data = None

    unpack = struct.unpack_from
    fmt = '<Q'
    m = mask
    total = 0

    if even_count and odd_count:
        ed = even_data
        od = odd_data
        step = b << 1

        bp = b
        for s in range(1, max_s + 1, 2):
            if pres[s]:
                total += (unpack(fmt, ed, bp >> 3)[0] >> (bp & 7)) & m
                bp_odd = bp - b
                total += (unpack(fmt, od, bp_odd >> 3)[0] >> (bp_odd & 7)) & m
            bp += step

        bp = b << 1
        for s in range(2, max_s + 1, 2):
            if pres[s]:
                total += (unpack(fmt, ed, bp >> 3)[0] >> (bp & 7)) & m
                bp_odd = bp - b
                total += (unpack(fmt, od, bp_odd >> 3)[0] >> (bp_odd & 7)) & m
            bp += step

    elif even_count:
        ed = even_data
        step = b << 1
        bp = b << 1
        for s in range(2, max_s + 1, 2):
            if pres[s]:
                total += (unpack(fmt, ed, bp >> 3)[0] >> (bp & 7)) & m
            bp += step

    else:
        od = odd_data
        step = b << 1
        bp = 0
        for s in range(1, max_s + 1, 2):
            if pres[s]:
                total += (unpack(fmt, od, bp >> 3)[0] >> (bp & 7)) & m
            bp += step

    print((total - n) // 2)


if __name__ == '__main__':
    main()