import sys
import heapq

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    try:
        T = next(it)
    except StopIteration:
        return

    out_lines = []
    push = heapq.heappush
    pop  = heapq.heappop

    for i in range(T):
        N = next(it)
        tasks = []
        for i in range(N):
            s = next(it); t = next(it)
            d = s + t
            tasks.append((d, t))
        tasks.sort()  # sort by d ascending

        total = 0
        heap = []  # min-heap - simulated max-heap
        for d, t in tasks:
            push(heap, -t)
            total += t
            if total > d:
                total += pop(heap)  # pop returns negative largest t; adding subtracts it

        out_lines.append(str(len(heap)))

    sys.stdout.write("\n".join(out_lines) + "\n")

if __name__ == "__main__":
    main()