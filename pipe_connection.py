import pandas as pd

# Main functionww
def source_to_sinks(path: str) -> str:
    
    # Establish pipe directionality vector dictionary
    # Each index in the vector will represnt the left, right, up and downward allowed directionality of each cell. 
    # Source, alphabetical Letters and missng values directionality values will het initialized once grid can be formed. 
    pipe_direction = {'═': [1,1,0,0], '║':[0,0,1,1], '╔':[0,1,0,1], '╗':[1,0,0,1], '╚':[0,1,1,0], '╝':[1,0,1,0], '╠':[0,1,1,1], '╣':[1,0,1,1], '╦':[1,1,0,1], '╩':[1,1,1,0]}

    # Read the name of the file
    with open(path, 'r') as r:
        rows = r.readlines()

    #Extract data
    points = []
    for row in rows:
        symbol, x, y = row.split()
        x = int(x) 
        y = int(y)
        # Assuming that you can go through the source and each sink in any direction. 
        # They both get initialied as [1,1,1,1]
        direction = pipe_direction[symbol] if symbol in pipe_direction else [1,1,1,1]    
        points.append((symbol, x, y, direction))
        
    data = pd.DataFrame(points, columns=['symbol', 'X', 'Y', 'dir']).sort_values(by=['X','Y'])

    # Find max ranges for 2D array
    x_max = data['X'].max()
    y_max = data['Y'].max()
    
    # Create a grid with the pipe, source and sink layouts. 
    # Unfilled cells get automatically converted to NA with the directionality of [0,0,0,0]. 
    grid = pd.DataFrame(index=range(y_max + 1), columns=range(x_max + 1))
    grid = grid.map(lambda x: ['NA', [0, 0, 0, 0]])
    
    # for each corresponding x,y in the data DF, insert the symbol + its directionality vector
    for row in data.itertuples(index=False):
        grid.iloc[row[2], row[1]] = [row[0],row[3]]
    
    # Used to visualize the pathway the way the example shows it.
    grid = grid.sort_index(axis=0, ascending=False)
    
    # Uncommenting the print code will visualize the purpose of each pipe and its directionality vectors. 
    # print(grid)
    
    source = data[data['symbol'] == "*"]
    source_col = source.iat[0,1]
    source_row = source.iat[0,2]    
    
    visited = []
    connected = []

    def is_valid(row: int, col: int) -> bool: 
        
        return ((col >= 0) and (col < len(grid.columns) ) and (row >= 0) and (row < len(grid.index)))
    
    def is_alpha(row: int, col: int) -> bool:
        
        return str(grid.loc[row,col][0]).isalpha()
    
    def is_na(row: int, col: int) -> bool:
        
        return grid.loc[row , col][0] == 'NA'
    
    def is_visited(row: int, col: int):
        
        return [row, col] in visited
    
    # Depth First Search: DFS will allow for a complete chain exploration rather than a shortest path search. 
    def dfs(row, col):
        
        # Initially mark the current cell as visited. 
        # This is done for formatiing reasons
        visited.append([row, col])
        
        # Recursive conditions: each "if" statement branch represents a move upward, downward, leftward, rightward. 
        # The conditions are that each cell's directionality vector index has to correspond to its counterparts inverse index.
        # e.g: Since each element is given a directionality pathway represented by a length 4 array: [left, right, up, down]
        #      If the cell wants to move upwards; which means that it has a 1 on index 2 which is the upward index: ([0, 0, 1, 0])
        #      Its counter part has to have a 1 in index 3, which is the downward index: ([0, 0, 0, 1])
        
        if is_alpha(row, col):
            connected.append(grid.loc[row,col][0])
                
        if is_valid(row + 1, col) and not is_na(row + 1, col) and not is_visited(row+1,col): # Up
            
            if grid.loc[row,col][1][2] == grid.loc[row + 1,col][1][3]: 
                
                dfs(row + 1, col) # succesfully moving up

        if is_valid(row - 1, col) and not is_na(row - 1 , col) and not is_visited(row-1,col): # Down
                
            if grid.loc[row,col][1][3] == grid.loc[row - 1, col][1][2]:
                        
                dfs(row - 1, col) # succesfully moving down
                
        if is_valid(row, col - 1) and not is_na(row , col - 1) and not is_visited(row,col - 1): # Left
            
            if grid.loc[row,col][1][0] == grid.loc[row, col -1][1][1]:
                
                dfs(row, col - 1) # succesfully moving left

        if is_valid(row, col + 1) and not is_na(row , col + 1) and not is_visited(row,col + 1): # Right
            
            if grid.loc[row,col][1][1] == grid.loc[row, col + 1][1][0]:
                            
                dfs(row, col + 1) # succesfully moving right
            
        else:
            
            return       
                               
    # Initiate search                                
    dfs(source_row, source_col)
    
    # Return sorted connected sinks
    print(str.join('',sorted(connected))) 
    
if __name__ == "__main__":


    print(source_to_sinks("db_pipe.txt"))

