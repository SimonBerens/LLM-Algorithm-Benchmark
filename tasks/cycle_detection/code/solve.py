V = int(input())
g = [[] for _ in range(V)]
for u in range(V):
    E = int(input())
    if E:
        g[u] = list(map(int, input().split()))

status = [0] * V


def dfs(u):
    status[u] = 1
    for v in g[u]:
        if (status[v] == 0 and dfs(v)) or status[v] == 1:
            return True
    status[u] = 2
    return False


cycle_start = -1
for u in range(V):
    if status[u] == 0 and dfs(u):
        cycle_start = u
        break
cycle_found = cycle_start != -1
print(cycle_found, cycle_start)
