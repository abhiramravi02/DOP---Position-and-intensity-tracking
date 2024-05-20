import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

xyval = []
prev_xyval = []
updated_coordinates = {}
intensities = []
# Path to the tiff file
path = r'C:\Users\abhir\OneDrive\Desktop\DOP\op_3'
 
# List to store the loaded image
images = []
 
ret, images = cv2.imreadmulti(mats=images,
                              filename=path+'\img.tif',
                              start=0,
                              count=455,
                              flags=cv2.IMREAD_UNCHANGED)

for imgcnt in range(3, 455, 5):
    s = path+'tif_image.png'
    cv2.imwrite(s, images[imgcnt])
    s = path+'tif_image.png'
    img = cv2.imread(s)

    # Convert to grayscale. [  m, ]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray, (3, 3)) 
    ret, thresh1 = cv2.threshold(gray_blurred, 19, 255, cv2.THRESH_BINARY) 
    #Find the contrours in the image
    contours, heirarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    ar = []
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if area > 500:
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            if (x > 20 and x < 1616) and (y > 20 and y < 1068):
                ar.append(contours[i])

    prev_xyval.clear()
    for i in range(len(xyval)):
        try:
            prev_xyval.append(updated_coordinates[i])
        except KeyError:
            pass
    xyval.clear()

    for i in range(len(ar)):
        cnt = ar[i]
        M = cv2.moments(cnt)
        cx = M['m10']/M['m00']
        cy = M['m01']/M['m00']
        cx = float("{:.3f}".format(cx))
        cy = float("{:.3f}".format(cy))
        center = (cx,cy)
        xyval.append(center)

    print(len(xyval))

    if imgcnt > 5:
        for i in range(len(prev_xyval)):
            mindist = 1000
            for j in range(len(xyval)):
                if ((abs(prev_xyval[i][1] - xyval[j][1]) < 20) and abs(prev_xyval[i][0] - xyval[j][0]) < 20):
                    dist = math.sqrt((abs(prev_xyval[i][0] - xyval[j][0])) ** 2 + (abs(prev_xyval[i][1] - xyval[j][1])) ** 2)
                    if dist < mindist and dist < 30:
                        mindist = dist
                        minflag = j
            updated_coordinates[i] = xyval[minflag]
    
    else:
        for i in range(len(xyval)):
            updated_coordinates[i] = xyval[i]

    file1 = open("C:\\Users\\abhir\\OneDrive\\Desktop\\DOP\\XY_coordinates\\Coordinates"+f"{imgcnt:03}"+".txt","w")
    
    for i in range(len(updated_coordinates)):
        (x, y) = (updated_coordinates[i][0], updated_coordinates[i][1])
        file1.write(str(i))
        file1.write(" : ")
        file1.write(str(x))
        file1.write(", ")
        file1.write(str(y))
        file1.write("\n")
        cv2.putText(img,str(i),(int(x-15), int(y+15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    
    file1.close()
    
    xpoints = []
    ypoints = []

    #Writing the intensities into a file 
    for i in range(len(updated_coordinates)):
        (x, y) = (updated_coordinates[i][0], updated_coordinates[i][1])
        x = int(x)
        y = int(y)
        intensity_val = 0
        for length in range(x-5, x+5, 1):
            for breadth in range(y-5, y+5, 1):
                intensity_val += images[imgcnt-1][int(y)][int(x)]
        intensity_val /= 100
        if imgcnt == 3:
            file1 = open("C:\\Users\\abhir\\OneDrive\\Desktop\\DOP\\Intensities\\Intensities"+f"{i:03}"+".txt","w")
            intensities.append(intensity_val)
        else:
            file1 = open("C:\\Users\\abhir\\OneDrive\\Desktop\\DOP\\Intensities\\Intensities"+f"{i:03}"+".txt","a")
        file1.write(str(int((imgcnt+2)/5)))
        file1.write(" : ")
        file1.write(str(float("{:.3f}".format(intensity_val/intensities[i]))))
        file1.write("\n")
        file1.close()

    #draw the obtained contour lines(or the set of coordinates forming a line) on the original image
    cv2.drawContours(img, ar, -1, (120,50,120), 2)
    s = path+'\img'
    s+=(f"{imgcnt:03}"+'.png')
    cv2.imwrite(s, img)

intensities.clear()
fig, (ax1, ax2) = plt.subplots(2, 1)
histplot = [0]*100

for i in range(len(updated_coordinates)):
    f = open("C:\\Users\\abhir\\OneDrive\\Desktop\\DOP\\Intensities\\Intensities"+f"{i:03}"+".txt","r")
    xpoints = []
    ypoints = []
    point_count = 1
    for file_intensities in f:
        file_intensities = file_intensities.strip('\n')
        if point_count < 10:
            xpoints.append(float(file_intensities[4:]))
        else:
            xpoints.append(float(file_intensities[5:]))
        ypoints.append(point_count)
        point_count+=1

    plotflag = 0
    xpoints_count = 0
    xpoints=np.array(xpoints)
    ypoints=np.array(ypoints)
    ax1.plot(ypoints,xpoints, color = 'red', linewidth=0.3)
    histplot.append(xpoints[len(xpoints)-1])

ax2.hist(histplot, bins=100, color='skyblue', edgecolor='black')
plt.savefig(r'C:\Users\abhir\OneDrive\Desktop\DOP\Intensities\Intensity_plot.png')
plt.show()
