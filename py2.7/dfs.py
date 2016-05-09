class dfs(object):
    def __init__(self,game,player):
        self.game=game
        self.player=player
        self.rowSize=len(game)
        self.colSize=len(game[0])
        self.visited=[ [0 for i in range(0,self.rowSize)] for j in range(0,self.colSize)]
        self.direction_map={
                            "R":(0,1),      # R---> Right
                            "L":(0,-1),      # L---> Left
                            "U":(-1,0),      # U---> UP
                            "D":(1,0),      # D---> Down
                            "UL":(-1,-1),     # UL--> UP Left
                            "UR":(-1,1),      # UR--> UP right
                            "DR":(1,1),     # DR--> Down Right
                            "DL":(1,-1)      # DL--> Down Left
                            }
        self.direction={"horizontal":["R","L"],"vertical":["U","D"],"right_diagonal":["UR","DL"],"left_diagonal":["UL","DR"]}


    def __is_safe(self,position):
        return position[0]<self.rowSize and position[1]>=0 and position[1]<self.colSize and position[1] >=0 and self.visited[position[0]][position[1]]!=1
    def run(self,position,direction=''):
        if(direction==''):
            direction={"horizontal":0,"vertical":0,"right_diagonal":0,"left_diagonal":0}

            direction["horizontal"]=self.dfs_searh(position,"horizontal",4)
            direction["vertical"]=self.dfs_searh(position,"vertical",4)
            direction["right_diagonal"]=self.dfs_searh(position,"right_diagonal",4)
            direction["left_diagonal"]=self.dfs_searh(position,"left_diagonal",4)
            return direction
            
        else:

            return self.dfs_searh(position,direction)
    def dfs_searh(self,position,direction,lookahead):
        if lookahead==0:
            return 0
        row=position[0]
        col=position[1]
        if not self.__is_safe(position) or self.game[row][col]!=-1 and self.game[row][col]!=self.player:
            return 0
        elif not self.is_downward_empty(position[0],position[0]-1):
            return 0

            
        updated_position0=self.__get_row_col_from_direction(position,self.direction[direction][0])
        updated_position1=self.__get_row_col_from_direction(position,self.direction[direction][1])
        self.visited[position[0]][position[1]]=1
        ret=1+self.dfs_searh(updated_position0,direction,lookahead-1)+self.dfs_searh(updated_position1,direction,lookahead-1)
        self.visited[position[0]][position[1]]=0
        return ret

    def __get_row_col_from_direction(self,position,direction):
        direction=self.direction_map[direction]
        return (position[0]+direction[0],position[1]+direction[1])

    def is_downward_empty(self,i,j):
        if i<self.rowSize and self.game[i][j]!=-1:
            return 1
        return 0





"""class Islands(object):

    def __init__(self,grid,row,col):
    boolean isSafe(int M[][], int row, int col,
                   boolean visited[][])
    {
        // row number is in range, column number is in range
        // and value is 1 and not yet visited
        return (row >= 0) && (row < ROW) &&
               (col >= 0) && (col < COL) &&
               (M[row][col]==1 && !visited[row][col]);
    }
 
    // A utility function to do DFS for a 2D boolean matrix.
    // It only considers the 8 neighbors as adjacent vertices
    void DFS(int M[][], int row, int col, boolean visited[][])
    {
        // These arrays are used to get row and column numbers
        // of 8 neighbors of a given cell
        int rowNbr[] = new int[] {-1, -1, -1,  0, 0,  1, 1, 1};
        int colNbr[] = new int[] {-1,  0,  1, -1, 1, -1, 0, 1};
 
        // Mark this cell as visited
        visited[row][col] = true;
 
        // Recur for all connected neighbours
        for (int k = 0; k < 8; ++k)
            if (isSafe(M, row + rowNbr[k], col + colNbr[k], visited) )
                DFS(M, row + rowNbr[k], col + colNbr[k], visited);
    }
 
    // The main function that returns count of islands in a given
    //  boolean 2D matrix
    int countIslands(int M[][])
    {
        // Make a bool array to mark visited cells.
        // Initially all cells are unvisited
        boolean visited[][] = new boolean[ROW][COL];
 
 
        // Initialize count as 0 and travese through the all cells
        // of given matrix
        int count = 0;
        for (int i = 0; i < ROW; ++i)
            for (int j = 0; j < COL; ++j)
                if (M[i][j]==1 && !visited[i][j]) // If a cell with
                {                                 // value 1 is not
                    // visited yet, then new island found, Visit all
                    // cells in this island and increment island count
                    DFS(M, i, j, visited);
                    ++count;
                }
 
        return count;
    }
    """