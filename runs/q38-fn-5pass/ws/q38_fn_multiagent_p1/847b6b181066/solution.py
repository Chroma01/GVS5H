import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    target_r = int(data[1])
    target_c = int(data[2])
    s = data[3]

    # Prefix coordinates are in [-N, N].
    # Query coordinates P_t - (R, C) are in [-2N, 2N].
    shift = 2 * n + 5
    base = 4 * n + 11

    r = 0
    c = 0

    # Encode (0, 0)
    seen = {shift * base + shift}
    ans = bytearray()

    n_ord = ord('N')
    s_ord = ord('S')
    w_ord = ord('W')

    for ch in s:
        if ch == n_ord:
            r -= 1
        elif ch == s_ord:
            r += 1
        elif ch == w_ord:
            c -= 1
        else:  # 'E'
            c += 1

        # Smoke exists at (target_r, target_c) iff
        # some previous prefix equals current prefix - (target_r, target_c).
        query = (r - target_r + shift) * base + (c - target_c + shift)
        if query in seen:
            ans.append(49)  # '1'
        else:
            ans.append(48)  # '0'

        seen.add((r + shift) * base + (c + shift))

    ans.append(10)  # newline
    sys.stdout.buffer.write(ans)

if __name__ == "__main__":
    main()