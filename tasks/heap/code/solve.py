from heapq import heappush, heappop

n = int(input())
h = []
res = []
for _ in range(n):
    t, *rest = map(int, input().split())
    if t == 0:
        heappush(h, rest[0])
    elif t == 1:
        heappop(h)
    else:
        res.append(h[0])
print(res)