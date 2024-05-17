import matplotlib.pyplot as plt
import matplotlib.pyplot as histogram
import numpy as np

fig, (ax1, ax2) = plt.subplots(2, 1)

histplot = [0]*100

for i in range(900):
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
plt.show()