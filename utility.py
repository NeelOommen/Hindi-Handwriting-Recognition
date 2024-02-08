def collectArea(img, i, j):
    leftBound = j
    rightBound = j
    topBound = i
    bottomBound = i

    to_explore = []
    visited = []

    height, width = img.shape

    start_pixel = (i,j)
    to_explore.append(start_pixel)

    while len(to_explore) != 0 :
        currentI, currentJ = to_explore.pop(0)
        img[currentJ][currentI] = 0
        visited.append((currentI, currentJ))

        #add non zero neightbours
        tI = currentI-1
        while tI <= currentI+1 and tI < width:
            tJ = currentJ-1
            while tJ <= currentJ+1 and tJ < height:
                if img[tJ][tI] > 0 and tJ != currentJ and tI != currentI:
                    newPixel = (tI, tJ)
                    img[tJ][tI] = 0
                    if not (newPixel in to_explore) and not (newPixel in visited):
                        to_explore.append(newPixel)
                tJ+=1
            tI+=1 
        #print(s)

        #update limits
        leftBound = min(currentJ, leftBound)
        rightBound = max(currentJ, rightBound)
        topBound = min(currentI, topBound)
        bottomBound = max(currentI, bottomBound)
        


    print(f'bounds: {leftBound} {topBound} {rightBound} {bottomBound}')
    return (leftBound, topBound, rightBound, bottomBound)