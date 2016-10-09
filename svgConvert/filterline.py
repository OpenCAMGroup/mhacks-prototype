import math

def cos_theta(x,y):
    dot = x[0] * y[0] + x[1] * y[1]
    mag = lambda x: (x[0]**2 + x[1]**2)**.5
    cosq = dot/mag(x)/mag(y)
    return cosq

def relative_vectors(x, y, z):
    x1 = x[0] - y[0]
    y1 = x[1] - y[1]
    x2 = z[0] - y[0]
    y2 = z[1] - y[1]
    return ((x1, y1), (x2, y2))


def filter_lines(x, thresh):
    #thresh is IN DEGREES
    threshold = math.sin(math.radians(thresh))
    to_pop = []
    for i in range(len(x)-2):

        rel_vecs = relative_vectors(x[i], x[i+1], x[i+2])
        if abs(cos_theta( rel_vecs[0], rel_vecs[1])+1)  < threshold:
            to_pop.append(i+1)
    to_pop.reverse()
    [x.pop(z) for z in to_pop]
    return x




if __name__ == "__main__":
    print relative_vectors([-1, 0], [1,1], [1, 0])
    print filter_lines([[-1, 0], [0,0], [1, 5] ,[2, 0]], 1)
    print filter_lines([[1, 0], [0, 0.1], [-1, 0]], 1)
    print filter_lines([[-1, -1], [.1, 0.1], [1,1]], 1)
    print filter_lines([[-1, -1], [-.1, .1], [1,1]], 90)
    print filter_lines([[1, 0], [-1, -1], [1, 1], [2, 2], [3, 3]], 1)
    print filter_lines([[-1, 0],[0,0], [0, -1]], 1)
