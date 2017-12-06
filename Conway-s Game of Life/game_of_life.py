
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N=100
ON=255
OFF=0


####################################################################
#Initialization of the grid

grid=np.random.choice(255,N*N).reshape(N,N)

for i in range(N):
    for j in range(N):
        if grid[i,j]>127:
            grid[i,j]=ON
        else:
            grid[i,j]=OFF
            
####################################################################

def update_grid(data):
    global grid
    new_grid=grid.copy() #to make a copy to put the new new grid
    for i in range(N):
        for j in range(N):
            #get the total number of neighbours
            #assuming wrapping of the board around the edges
            neighbours=((grid[i,(j+1)%N]+grid[i,(j-1)%N]+
                        grid[(i+1)%N,j]+grid[(i-1)%N,j]+
                        grid[(i+1)%N,(j+1)%N]+grid[(i-1)%N,(j+1)%N]+
                        grid[(i+1)%N,(j-1)%N]+grid[(i-1)%N,(j-1)%N]))/255
            #conditions of Conway's Game of Life
            if grid[i,j]==ON:
                if neighbours<2:
                    new_grid[i,j]=OFF
                elif (neighbours==2 or neighbours==3):
                    new_grid[i,j]=ON
                elif neighbours>3:
                    new_grid[i,j]=OFF

            elif grid[i,j]==OFF:
                if neighbours==3:
                    new_grid[i,j]=ON

    updated_grid.set_data(new_grid)
    grid=new_grid
    return [updated_grid]

####################################################################
# Animation

fig,ax=plt.subplots()
plt.title("Conway's Game of Life")
updated_grid=ax.matshow(grid)
anime=animation.FuncAnimation(fig,update_grid,interval=100,save_count=50)
plt.show()
