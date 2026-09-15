import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3]
    T = data[4]

    def sig(w):
        o = []  # residues of '1' positions modulo X, in order
        z = []  # residues of '0' positions modulo Y, in order
        ao = o.append
        az = z.append
        for i, ch in enumerate(w):
            p = i + 1
            if ch == 49:          # ord('1')
                ao(p % X)
            else:
                az(p % Y)
        return o, z

    if sig(S) == sig(T):
        sys.stdout.write("Yes\n")
    else:
        sys.stdout.write("No\n")

if __name__ == "__main__":
    main()