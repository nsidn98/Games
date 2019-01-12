# maze_solver
Give an image of a maze and it will find the path

Assuming that the input image has a green color at the start and red color at the end and the explorable space to be white with walls in black this program can take any image of a maze and give the path.

Breadth First Search was used in 'solve.py'

# Usage

Clone this repo and cd to the directory where this is downloaded.
Type `python3 solve.py mazes/maze1.jpg`

This will run the solution for maze1 stored in the mazes folder.

If you want to use your own maze,put it in 'mazes' folder and type `python3 solve.py mazes/your_maze.jpg`

If you want to use it in python2 you will have to make the following changes in solve.py:

Line 179 `for i in range(10):` -> `for i in xrange(10):`

## Output:
![image](https://github.com/nsidn98/Games/blob/master/maze_solver/output/00101.jpg)
