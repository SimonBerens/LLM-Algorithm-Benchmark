V, E = map(int, input().split())
g = [[] for _ in range(V)]
for _ in range(E):
    u, v = map(int, input().split())
    g[u].append(v)

status = [0] * V
res = []

def dfs(u):
    status[u] = 1
    res.append(u)
    for v in g[u]:
        if status[v] == 0:
            dfs(v)


for u in range(V):
    if status[u] == 0:
        dfs(u)
print(res)
