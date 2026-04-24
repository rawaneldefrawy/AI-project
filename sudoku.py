import numpy as np
import random
import sys,pygame as pg
pg.init()
screensize=1000,750
font1=pg.font.SysFont(None,50)
font2=pg.font.SysFont(None,60)
font5=pg.font.SysFont(None,100)
selected=None #tuple
N= 9
offset_y=150
message = ""
screen=pg.display.set_mode(screensize)
pg.display.set_caption("Sudoku")


grid=[[5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],]
original_grid = [row[:] for row in grid]


def drawtitle():
    title = font5.render("Sudoku", True, (44,62,80))
    screen.blit(title, (375, 50))



# draw large grid 
def drawbackground():
    
    
    screen.fill((30,30,40))  
    pg.draw.rect(screen,(230,235,245),pg.Rect(25,offset_y,504,504),7)   
    
    i=1
    while (i*56)<504:
        if i%3==0: linewidth=7 
        else: linewidth=3
        pg.draw.line(screen,(230,235,245),
                     pg.Vector2((i*56)+25,offset_y),
                     pg.Vector2((i*56)+25,145+504),linewidth)
        pg.draw.line(screen,(230,235,245),
                     pg.Vector2(25,(i*56)+offset_y),
                     pg.Vector2(523,(i*56)+offset_y),linewidth)
        i+=1
   
#return numbers of large grid
def returnnumbers():
     
    
     for row in range(0,9):
        for column in range(0,9):
            output=grid[row][column]
            if output!=0:
                color = pg.Color("lightblue") if original_grid[row][column] != 0 else (155,89,182)
                ntext = font1.render(str(output), True, color)
                cellrect = pg.Rect((column*56)+25, (row*56)+15+140, 56, 56)
                textrect = ntext.get_rect(center=cellrect.center)  
                screen.blit(ntext, textrect)


     


def possible(row,column,number):
                                #row1 2
    # constrains                                        #col1 2
    for i in range(0,9):
        if grid[row][i]==number:
            return False
    for i in range(0,9):
        if grid[i][column]==number:
            return False
    x0=column//3 *3
    y0=row//3 *3
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j]==number:
                return False
    return True  
def solve(grid,row=0,column=0):
    # Base case
    if row == N - 1 and column == N:
        return True
    if column== N :
        row+=1
        column=0
    # constrain
    if grid[row][column] > 0:
        return solve(grid,row,column+1)
    # Domain
    for number in range(1,N+1):
        if possible(row,column,number):
            grid[row][column]= number
            if solve(grid,row,column+1):
                return True
            grid[row][column] = 0
    return False
def is_valid_solution(grid):
    # check rows
    for row in grid:
        if sorted(row) != list(range(1,10)):
            return False

    # check columns
    for col in range(9):
        column = [grid[row][col] for row in range(9)]
        if sorted(column) != list(range(1,10)):
            return False

    # check 3x3 boxes
    for box_row in range(0,9,3):
        for box_col in range(0,9,3):
            box = []
            for i in range(3):
                for j in range(3):
                    box.append(grid[box_row+i][box_col+j])
            if sorted(box) != list(range(1,10)):
                return False

    return True
def resetgame():
    global grid, message
    message = ""
    for row in range(9):
        for col in range(9):
            if original_grid[row][col] == 0:
                grid[row][col] = 0

def show_message():
    global message
    if message != "":
        color = (39,174,96) if message=="Correct!" else (192,57,43)
        text = font2.render(message, True, color)
        screen.blit(text, (640, 500))

def newgame():
    global grid , original_grid , message
    message = ""
    
    grid = [[0]*9 for _ in range(9)]
    solve(grid,0,0)
    for i  in range (45):
        row=random.randint(0,8)
        col=random.randint(0,8)
        grid[row][col]=0
    original_grid = [row[:] for row in grid]
 
 #draw button


def drawbutton(text, y,color):
    rect=pg.Rect(620,y,222,50)
    if rect.collidepoint(pg.mouse.get_pos()):
        color=(color[0]+20,color[1]+20,color[2]+20)
    pg.draw.rect(screen, color, rect, border_radius=15)
    label = font1.render(text,True,"white")
    textrect = label.get_rect(center=rect.center)
    screen.blit(label,textrect)
    return rect


def drawcell():
    if selected:
        row, col = selected
        cellrect = pg.Rect((col*56)+25, (row*56)+25+125, 56, 56)
        pg.draw.rect(screen, (237,149,100), cellrect) 
         

def gameloop():
    drawbackground()
    drawcell()  
    drawtitle()  
    resetbutton = drawbutton("Reset",420,((231,76,60))) 
    checkbutton = drawbutton("Check",260,(155,89,182))
    newgamebutton=drawbutton("New Game",340,(52,152,219))
    solvebutton=drawbutton("Solve",180,(46,204,113))
    
    global selected, grid, message

    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type==pg.MOUSEBUTTONDOWN:
            x,y=event.pos
            if 25<x<519 and offset_y<y<offset_y+504:
                row = (y-offset_y)//56
                col = (x-25)//56
                selected = (row,col)

            if solvebutton.collidepoint(event.pos):
                solve(grid,0,0)  
                selected=None 
            if newgamebutton.collidepoint(event.pos):
                newgame() 
            if checkbutton.collidepoint(event.pos):
                if is_valid_solution(grid):
                    message = "Correct!" 
                else: 
                    message = "Wrong!"    
            if resetbutton.collidepoint(event.pos):
                resetgame()
                message = "Board Reset!"
         
        if event.type==pg.KEYDOWN and  selected: 
            row,col=selected
            if event.unicode.isdigit():
                number=int(event.unicode)    
                if number!=0:
                    grid[selected[0]][selected[1]]=number
                    selected = None 
            if event.key==pg.K_BACKSPACE:
                grid[row][col]=0    
                selected = None 
    
    show_message()
    returnnumbers()
    pg.display.flip()

newgame()   
while True:
    gameloop()








