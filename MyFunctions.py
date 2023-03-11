import math


def get_angle(p1, p2):
    # Difference in x coordinates
    dx = p2[0] - p1[0]

    # Difference in y coordinates
    dy = p2[1] - p1[1]

    # Angle between p1 and p2 in radians
    theta = math.atan2(dy, -dx)
    
    #convert to degrees
    x = math.degrees(theta)

    #pygame.display.set_caption(str(x))

    return x

def get_distance(x1, y1, x2, y2):
    distance = math.sqrt(((x2 - x1) ** 2) + (y2 - y1) ** 2)
    #pygame.display.set_caption(str(distance))
    return distance

def get_distance_from_pts(p1, p2):
    return get_distance(p1[0], p1[1], p2[0], p2[1])
    

# TODO: bug: when other blocks are on top on this shape, the dots still appear at the
# top blocks, but it should only show the dots on the blocks below this
# gets the top most blocks in the shape
def get_points_on_top(points: list, offset_to_add: float): #TetriminoShape list
    # copy
    a = [i for i in points]

    # ignore - same as above
    #a = [[j for j in i.shape] for i in self.blocks]
    
    # sort by x-axis
    a.sort(key = lambda x: x[0])
    found_points = []
    while(len(a) > 0):
        # filter by most-left-only (can be more than one)
        b = [[j for j in i] for i in a if i[0] == a[0][0]] #a[0][i] must match above x[i]!!

        # now sort by y-axis to find the top most point
        b.sort(key = lambda x: x[1])

        # if there are any points in list
        if(len(b) > 0):
            # add point to found-points  
            found_points.append(b[0])

            # remove newly found points from original list
            a = [i for i in a if i not in b]
        
        else:# if nothing is left then just return
            break
    
    # move points to the top of the block
    for pts in found_points:
        pts[1] += offset_to_add
        
    return found_points
