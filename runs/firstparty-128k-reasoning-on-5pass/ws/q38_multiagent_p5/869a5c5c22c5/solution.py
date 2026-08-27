import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []
    append = out.append
    SHIFT = 10**6

    for _ in range(t):
        R = int(data[idx])
        B = int(data[idx + 1])
        idx += 2

        if R == 2 and B == 3:
            append("Yes")
            append("B 2 3")
            append("R 3 2 ")
            append("B 2 2")
            append("B 3 3")
            append("R 2 4")
            continue

        if R + B < 2 or (R & 1) or (R == 0 and (B & 1)):
            append("No")
            continue

        append("Yes")

        if R > 0 and B > 0:
            m = R // 2 - 1

            # Red snake: (0,0), (0,-1), ..., (0,-m), (1,-m), ..., (1,0)
            for c in range(0, -m - 1, -1):
                append(f"R {SHIFT} {SHIFT + c}")
            for c in range(-m, 1):
                append(f"R {SHIFT + 1} {SHIFT + c}")

            if B & 1:
                # B = 2L + 1
                L = B // 2
                append(f"B {SHIFT + 1} {SHIFT + 1}")
                for k in range(1, L + 1):
                    append(f"B {SHIFT + 1 - k} {SHIFT + 1 + k}")
                for k in range(L, 0, -1):
                    append(f"B {SHIFT - k} {SHIFT + k}")
            else:
                # B = 2L + 2
                L = B // 2 - 1
                append(f"B {SHIFT + 2} {SHIFT}")
                for k in range(0, L + 1):
                    append(f"B {SHIFT + 1 - k} {SHIFT + 1 + k}")
                for k in range(L, 0, -1):
                    append(f"B {SHIFT - k} {SHIFT + k}")

        elif B == 0:
            # All red: 1-based 2 x (R/2) perimeter starting at (1,1)
            K = R // 2
            for c in range(1, K + 1):
                append(f"R 1 {c}")
            for c in range(K, 0, -1):
                append(f"R 2 {c}")

        else:
            # All blue: 2 x (B/2) perimeter in (a,b), mapped to (r,c)=(a+b,a-b)
            K = B // 2
            for b in range(K):
                append(f"B {SHIFT + b} {SHIFT - b}")
            for b in range(K - 1, -1, -1):
                append(f"B {SHIFT + 1 + b} {SHIFT + 1 - b}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()