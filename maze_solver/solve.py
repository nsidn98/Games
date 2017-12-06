import os
import sys
import math
import time
import logging #library I used for debugging
from PIL import Image

logging.basicConfig(level=logging.INFO, format="[%(levelname)s]: %(asctime)-15s %(message)s")

class Solver:

    def __init__(self,maze):
        self.COLOR_MAP={
            (0,255,0): 'GREEN',
            (255,0,0): 'RED',
            (0,0,255): 'BLUE',
            (255,255,255): 'WHITE',
            (0,0,0): 'BLACK'
        }
        self.COLOR_RED = (255,0,0)
        self.COLOR_GREEN = (0,255,0)
        self.COLOR_BLUE = (0,0,255)
        self.COLOR_WHITE = (255,255,255)
        self.COLOR_BLACK = (0,0,0)
        self.START_COLOR = self.COLOR_GREEN
        self.END_COLOR = self.COLOR_RED
        self.FRONTIER_COLOR = self.COLOR_GREEN
        self.memorized_color_map={}

        #output
        self.DIR_OUT='out'
        self.file_in=maze
        ext=maze.split('.')[-1]
        self.file_out=os.path.join(self.DIR_OUT, os.path.basename(maze).split('.')[0] + '.' + ext)

        #output parameters
        self.SNAPSHOT_FREQ=20000 # to save the image after every 20000 timesscale

        #load img
        self.image=Image.open(self.file_in)
        logging.info('loaded image ')
        self.image=self.image.convert('RGB')
        self.pixels=self.image.load()
        self.START=self._findStart()
        self.END=self._findEnd()
        self._cleanImage()

        #search parameters
        self.tmp_dir='tmp'
        self.iterations=0

    #to check for boundary
    def _inBounds(self,dim,x,y):
        length,breadth=dim
        if x<0 or y<0 or x>=length or y>=breadth:
            return False
        return True

    def _isWhite(self,pixels,position):
        x,y=position
        r,g,b=pixels[x,y]
        threshold=240
        if pixels[x,y]==self.COLOR_WHITE or pixels[x,y]==0 or (r>threshold and g>threshold and b>threshold)\
        or pixels[x,y]==self.END_COLOR:
            return True

    def _getNeighbours(self,position):
        x,y=position
        return [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]

    def _drawX(self,pos,color=(0,0,255)):
        x,y=pos
        d=5
        for i in range(-d,d):
            self.pixels[x+i,y]=color
        for j in range(-d,d):
            self.pixels[x,y+j]=color

    def _drawSquare(self,pos,color=(0,0,255)):
        x,y=pos
        d=1
        for i in range(-d,d):
            for j in range(-d,d):
                self.pixels[x+i,y+j]=color

    def _cleanImage(self):
        logging.info('Cleaning image...')
        x,y=self.image.size
        for i in range(x):
            for j in range(y):
                if (i,j)==self.START:
                    self.pixels[i,j]==self.START_COLOR
                    continue
                if (i,j)==self.END:
                    self.pixels[i,j]==self.END_COLOR
                    continue
                closest_color = self._findClosestColor(self.pixels[i,j])
                for color in [self.COLOR_WHITE, self.COLOR_BLACK]:
                    if closest_color == color: self.pixels[i,j] = color
                for color in [self.START_COLOR, self.END_COLOR]:
                    if closest_color == color: self.pixels[i,j] = self.COLOR_WHITE



    def _findClosestColor(self,color,memorize=False):
        colors=list(self.COLOR_MAP.keys())
        if color in self.memorized_color_map and memorize==True:
            return color
        closest_color=sorted(colors,key=lambda c:distance(c,color))[0]
        if memorize==True:
            self.memorized_color_map[color]=closest_color
        return closest_color

    def _findColorCenter(self,color):
        x_min,x_max,y_min,y_max=float('inf'),float('-inf'), float('inf'), float('-inf')
        x,y=self.image.size
        for i in range(x):
            for j in range(y):
                code=self._findClosestColor(self.pixels[i,j])
                if code==color:
                    x_min,y_min=min(x_min,i),min(y_min,j)
                    x_max,y_max=max(x_max,i),max(y_max,j)
        return (mean([x_min, x_max]), mean([y_min, y_max]))

    def _findStart(self):
        logging.info('Finding the start point...')
        start=self._findColorCenter(self.START_COLOR)
        self._drawSquare(start,self.START_COLOR)
        return start

    def _findEnd(self):
        logging.info('Finding the end point...')
        end=self._findColorCenter(self.END_COLOR)
        self._drawSquare(end,self.END_COLOR)
        return end

    def solve(self):
        logging.info('Solving...')
        path=self._BFS(self.START,self.END)
        if path is None:
            logging.error('No path found!!!')
            self._drawX(self.START)
            self._drawX(self.END)
            self.image.save(self.file_out)
            sys.exit(1)

        #draw
        for position in path :
            x,y=position
            self.pixels[x,y]=self.COLOR_RED

        #save
        self.image.save(self.file_out)
        logging.info("Solution is saved as '{0}'.".format(self.file_out))
        print('\n','Done')

    # Breadth First Search
    def _BFS(self,start,end):
        #copy the maze to hold temp search state
        image=self.image.copy()
        pixels=image.load()
        self.iterations=0
        explored=set() #to keep track of explored nodes
        Q=[[start]]#to store the explored paths
        img=0

        while len(Q)!=0:
            if self.iterations>0 and self.iterations%self.SNAPSHOT_FREQ==0:
                logging.info('...')
            path=Q.pop(0)
            node=path[-1]
            explored.add(node)

            if node==end:
                #draw solution path
                for position in path:
                    x,y=position
                    pixels[x,y]=self.COLOR_RED
                for i in range(10):
                    image.save('{0}/{1:05d}.jpg'.format(self.tmp_dir, img))
                    img+=1
                logging.info('Found a path after {0} iterations.'.format(self.iterations))
                image.show("Solution Path")
                return path

            for neighbour in self._getNeighbours(node):
                x,y=neighbour
                if (x,y) not in explored and self._inBounds(image.size,x,y) and self._isWhite(pixels, (x,y)) :
                    pixels[x,y]=self.FRONTIER_COLOR
                    new_path=list(path)
                    new_path.append(neighbour)
                    Q+=[new_path]
                if self.iterations % self.SNAPSHOT_FREQ==0:
                    image.save('{0}/{1:05d}.jpg'.format(self.tmp_dir, img))
                    img+=1
                self.iterations+=1
        print("Returning after ", self.iterations, " iterations.")
        return None


def mean(numbers):
    return int(sum(numbers))/max(len(numbers),1)

def distance(c1,c2):
    (r1,g1,b1)=c1
    (r2,g2,b2)=c2
    return math.sqrt((r1-r2)**2+(g1-g2)**2+(b1-b2)**2)


if __name__=='__main__':
    solver=Solver(sys.argv[1])
    solver.solve()
