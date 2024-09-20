import numpy as np
map = np.array([[3,1,4,2,5],
                [3,2,3,3,2],
                [2,0,3,3,2],
                [5,0,0,3,1],
                [3,4,3,3,5],
                [2,3,4,4,0],
                [1,2,0,1,3],
                [0,2,0,3,2],
                [3,0,0,0,4],
                [3,1,0,4,2]])

ns_dist = 15
ew_dist = 20

def get_corner_times(dim1,dim2):
    times = np.array([[[-1 for _ in range(dim2)] for _ in range(dim1)] for _ in range(dim1*dim2)])
    for i in range(len(times)):
        coord = (int(i / dim2), i % dim2)
        for j in range(dim1):
            for k in range(dim2):
                times[i][j][k] = ns_dist*abs(j-coord[0]) + ew_dist*abs(k-coord[1])
    return times

def get_grid_times(corner_times,dim1,dim2):
    times = np.array([[[-1 for _ in range(dim2)] for _ in range(dim1)] for _ in range((dim1+1)*(dim2+1))])
    dirs = [(0,0),(0,1),(1,0),(1,1)]
    for i in range((dim1+1)*(dim2+1)):
        for j in range(dim1):
            for k in range(dim2):
                    times[i][j][k] = min([corner_times[i][p1[0]+j][p1[1]+k] for p1 in dirs])
    return times

def find_best(times,count):
    best_pair = [0,1]
    best_time = times[0][-1][-1]*count
    for p1 in range(count):
        for p2 in range(p1,count):
            grid = np.minimum(times[p1],times[p2])
            time = np.sum(np.multiply(grid,map))
            if time < best_time:
                best_time = time
                best_pair = [p1,p2]
            # print(p1,p2,time)
            # print(grid,end="\n\n")
    return best_time, best_pair

print()
corner_times = get_corner_times(len(map)+1,len(map[0])+1)
grid_times = get_grid_times(corner_times,len(map),len(map[0]))
best_time, best_pair = find_best(grid_times,(len(map)+1)*(len(map[0])+1))

grid = np.minimum(grid_times[best_pair[0]],grid_times[best_pair[1]])
time = np.sum(np.multiply(grid,map))
print((int(best_pair[0]/(len(map[0])+1)),best_pair[0]%(len(map[0])+1)),(int(best_pair[1]/(len(map[0])+1)),best_pair[1]%(len(map[0])+1)), time, np.sum(map),time/np.sum(map))
print(grid,end="\n\n")
