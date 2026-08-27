import sys

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        out.append(f"{n + 1} {n * n}")
    sys.stdout.write("\n".join(out) + "\n")

main()