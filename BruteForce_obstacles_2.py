import numpy as np
time_map = np.array([[3,1,4,2,5],
                    [3,2,3,3,2],
                    [2,0,3,3,2],
                    [5,0,0,3,1],
                    [3,4,3,3,5],
                    [2,3,4,4,0],
                    [1,2,0,1,3],
                    [0,2,0,3,2],
                    [3,0,0,0,4],
                    [3,1,0,4,2]])

dims = [dim+1 for dim in list(time_map.shape)]
ns_dist = 15
ew_dist = 20

def get_index(x,y):
    return x*dims[1]+y
def get_node(index):
    return (int(index / dims[1]), index % dims[1])
def get_hori_street(index):
    return (int(index / (dims[1]+1))+0.5, index % (dims[1]+1))
def get_vert_street(index):
    return (int(index / dims[1]), index % dims[1]+0.5)

def generate_grid(time_map, remove):
    grid = {}
    for row in range(dims[0]):
        for col in range(dims[1]):
            node = get_index(row,col)
            grid[node] = []
            for shift in [(-1,0),(0,-1),(0,1),(1,0)]:
                shifted = get_index(row+shift[0], col+shift[1])
                if row+shift[0] < 0 or row+shift[0] > dims[0]-1 or col+shift[1] < 0 or col+shift[1] > dims[1]-1:
                    continue
                if (node,shifted) in remove or (shifted,node) in remove:
                    continue
                grid[node].append(shifted)
    return grid

def draw_grid(grid, facilities=[]):
    for row in range(dims[0]):
        for col in range(dims[1]):
            cell = get_index(row,col)
            if cell in facilities:
                print("X",end="")
            else:
                print(".",end="")
            if cell + 1 in grid[cell]:
                print("--",end="")
            else:
                print("  ",end="")
        print()
        for col in range(dims[1]):
            cell = get_index(row,col)
            if cell + dims[1] in grid[cell]:
                print("|  ",end="")
            else:
                print("   ",end="")
        print()

def construct_path(path_dict, current):
    path = [current]
    while current in path_dict:
        current = path_dict[current]
        path.append(current)
    return list(reversed(path))

def get_path_len(path):
    total = 0
    for i in range(len(path)-1):
        if abs(path[i]-path[i+1]) == 1:
            total += ew_dist
        else:
            total += ns_dist
    return total

def a_star(start, goal, grid):
    if start == goal:
        return 0
    to_visit = [start]
    path = {}
    costs = {i:(ns_dist+ew_dist)*dims[0]*dims[1] for i in range(dims[0]*dims[1])}
    costs[start] = 0

    dists = {i:(ns_dist+ew_dist)*dims[0]*dims[1] for i in range(dims[0]*dims[1])}
    dists[start] = dist(start,goal)

    while to_visit != []:
        to_visit = sorted(to_visit, key=lambda node: dist(node,goal))
        curNode = to_visit[0]
        if curNode == goal:
            return get_path_len(construct_path(path, curNode))
        to_visit.remove(curNode)
        for nextNode in grid[curNode]:
            score = costs[curNode] + dist(curNode,nextNode)
            if score < costs[nextNode]:
                path[nextNode] = curNode
                costs[nextNode] = score
                dists[nextNode] = score + dist(nextNode,goal)
                if nextNode not in to_visit:
                    to_visit.append(nextNode)
    return -1

def dist(p1: int, p2: int):
    node1 = get_node(p1)
    node2 = get_node(p2)
    return ns_dist*abs(node1[0] - node2[0]) + ew_dist*abs(node1[1] - node2[1])

def get_corner_times(g):
    times = np.array([[[-1 for _ in range(dims[1])] for _ in range(dims[0])] for _ in range(dims[0]*dims[1])])
    for i in range(len(times)):
        for j in range(dims[0]):
            for k in range(dims[1]):
                times[i][j][k] = a_star(i,get_index(j,k),g)
                # times[i][j][k] = dist(i,get_index(j,k))
    for i in range(len(times)):
        for j in range(dims[0]):
            for k in range(dims[1]):
                times[i][j][k] = min(times[i][j][k],times[get_index(j,k)][get_node(i)[0]][get_node(i)[1]])
    return times

def get_hori_street_times(corner_times):
    hori_times = np.array([[[-1 for _ in range(dims[1]-1)] for _ in range(dims[0])] for _ in range((dims[0])*(dims[1]))])
    dirs = [(0,0), (0,1)]
    for i in range((dims[0])*(dims[1])):
        for j in range(dims[0]):
            for k in range(dims[1]-1):
                hori_times[i][j][k] = min([corner_times[i][p1[0]+j][p1[1]+k] for p1 in dirs])+ew_dist/2
    return hori_times

def get_vert_street_times(corner_times):
    vert_times = np.array([[[-1 for _ in range(dims[1])] for _ in range(dims[0]-1)] for _ in range((dims[0])*(dims[1]))])
    dirs = [(0,0), (1,0)]
    for i in range((dims[0])*(dims[1])):
        for j in range(dims[0]-1):
            for k in range(dims[1]):
                vert_times[i][j][k] = min([corner_times[i][p1[0]+j][p1[1]+k] for p1 in dirs])+ns_dist/2
    return vert_times

def find_best(v_times, h_times):
    size = dims[0]*dims[1]
    best_pair = [0,1]
    best_time = v_times[0][-1][-1]*size
    for p1 in range(size):
        for p2 in range(p1,size):
            v_grid = np.minimum(v_times[p1],v_times[p2])
            h_grid = np.minimum(h_times[p1],h_times[p2])
            time = np.sum(np.multiply(v_grid[:,:-1],time_map))/4 + np.sum(np.multiply(v_grid[:,1:],time_map))/4 + \
                   np.sum(np.multiply(h_grid[:-1],time_map))/4 + np.sum(np.multiply(h_grid[1:],time_map))/4
            if time < best_time:
                best_time = time
                best_pair = [p1,p2]
    return best_time, best_pair

def draw_street_grid(grid, facilities=[], vtimes=[], htimes=[]):
    for row in range(dims[0]):
        print(" ",end="")
        for col in range(dims[1]):
            cell = get_index(row,col)
            if cell in facilities:
                print("X",end="")
            else:
                print(".",end="")
            if cell + 1 in grid[cell]:
                time = min(htimes[f][row][col] for f in facilities)
                print("- {0:3} -".format(time),end="")
            else:
                print("       ",end="")
        print()
        for col in range(dims[1]):
            cell = get_index(row,col)
            if cell + dims[1] in grid[cell]:
                time = min(vtimes[f][row][col] for f in facilities)
                print("{0:3}     ".format(time),end="")
            else:
                print("        ",end="")
        print()

g = generate_grid(time_map,[(get_index(3,1),get_index(3,2)),
                            (get_index(3,2),get_index(4,2)),
                            (get_index(8,2),get_index(8,3))])
corner_times = get_corner_times(g)
vert_street_times = get_vert_street_times(corner_times)
hori_street_times = get_hori_street_times(corner_times)
best_time, best_pair = find_best(vert_street_times, hori_street_times)

print("Best Facility Locations are at", get_node(best_pair[0]), "and", get_node(best_pair[1]))
print("Average Response Time:",best_time/np.sum(time_map))
print("\nResponse Time Table:")
draw_street_grid(g, best_pair, vert_street_times, hori_street_times)