from Tkinter import*
from tkMessageBox import*
import time
from random import randint, shuffle
import sys
import os

'''Aumenta o limite de recursao'''
sys.setrecursionlimit(1000000)

class Snake:
    def __init__(self, master):
        
        '''Variavel da janela de restart'''
        self.window = False

        #############################################################
        '''--------------------- C O R E S -----------------------'''
        '''Lista com as cores da comida'''
        self.Fcolors = ["#FFFF00", "#FF00FF", "#0000FF", "#FF0000"] # ["yellow", "magenta2", "blue", "red"]

        '''Variavel para mudar a cor da lista'''
        self.i = randint(0, (len(self.Fcolors)-1))
        
        '''Snake Classic'''
        self.Sheadcolor = "#175A07" #cor da cabeca da cobra "dark green"
        self.Scolor = "#00FF00" #cor da cobra "black"
        self.borderScolor = "#000000" #cor do contorno da cobra "black"
        self.Fcolor = self.Fcolors[self.i] #cores da comida 
        self.vFcolor = "#FF0000" #cor da vitamina "red"
        self.BGcolor = "#000000" #cor de fundo 
        self.lbl1color = "#175A07" #cor de fundo do label do nome do jogo "dark green"
        self.lbl2color = "#AAF9A3" #cor de fundo dos labels "pale green"
        self.Titlefontcolor = "#00FF00" #cor do titulo "green"
        self.fontcolor = "#175A07" #cor do texto "dark green"
        self.topbg = "#E0E0D6" #cor das janelas extra "seashell2"

        '''Define a cor do master'''
        self.master = master
        self.master["bg"] = "#041C65" #"midnight blue"
        '''-------------------------------------------------------'''
        #############################################################
        
        #############################################################
        '''-------------------- C A N V A S ----------------------'''
        '''Cria o frame para o canvas'''
        self.frame = Frame(master, borderwidth = 10, relief = "ridge")
        self.frame["bg"] = "#000000"
        self.frame.pack()
        
        '''Variaveis para determinar o tamanho do canvas'''
        self.cRow = 50 #linhas 50
        self.cCol = 60 #colunas 60
        self.cMtp = 10 #multiplicador para o espaco entre linhas ou colunas 10
        self.cWidth = self.cCol * self.cMtp + 1 #largura do canvas
        self.cHeight = self.cRow * self.cMtp + 1 #altura do canvas

        '''Variavel da diferenca entre ponto final e inicial de um obejeto do canvas'''
        self.dif = self.cWidth/self.cCol*2

        '''Extremos do canvas'''
        self.xMin = 2
        self.yMin = 2
        self.xMax = self.cCol*self.dif/2 + 2
        self.yMax = self.cRow*self.dif/2 + 2
        
        '''Espacos possiveis'''
        self.Lx = [] #lista das posicoes possiveis no eixo X
        for k in range(0, (self.cCol/2)):
            self.Lx.append(2 + 20*k) #adiciona as posicoes a lista
            
        self.Ly = [] #lista das posicoes possiveis no eixo Y
        for l in range(0, (self.cRow/2)):
            self.Ly.append(2 + 20*l) #adiciona as posicoes a lista

        self.randx = randint(3, len(self.Lx)-1) #sorteia um numero para ser usado como posicao da lista
        self.randy = randint(3, len(self.Ly)-1) #sorteia um numero para ser usado como posicao da lista
        '''-------------------------------------------------------'''
        #############################################################

        '''Dificuldade do jogo'''
        self.gameMode = "Hard"
        
        '''Pontos'''
        self.score = 0
        
        if os.path.exists('highScore.txt'):
            with open('highScore.txt', 'r+') as self.highScore:
                if self.highScore.read() >= "0":
                    pass
        else:
            with open('highScore.txt', 'w') as self.highScore:
                self.highScore.write("107") #recorde "hard coded" para nao precisar baixar documento de texto
        #############################################################
        '''-------------------- L A B E L S ----------------------'''
        '''Cria label para o nome dop jogo'''
        self.lbl_SNAKE = Label(self.frame, borderwidth = 1, relief = "solid", text = "SNAKE GAME", font = ("Calibri", 35, "italic", "bold"), bg = self.lbl1color, fg = self.Titlefontcolor)
        self.lbl_SNAKE.pack(side = TOP, fill = BOTH)

        '''Cria o Canvas e cofingura-o'''
        self.canvas = Canvas(self.frame)        #\
        self.canvas["width"] = self.cWidth      # \
        self.canvas["height"] = self.cHeight    #  configs do canvas
        self.canvas["bg"] = self.BGcolor        # /
        self.canvas.pack(side = LEFT)           #/

        '''Cria label para o placar'''
        self.scoreboard = Label(self.frame, borderwidth = 1, relief = "solid", text = " Score Board ", font = ("Calibri", 15, "italic", "bold"), bg = self.lbl2color, fg = self.fontcolor)
        self.scoreboard.pack(side = TOP, fill = BOTH)
        
        self.lbl_score = Label(self.frame, borderwidth = 1, relief = "solid", text = 0, font = ("Calibri", 25, "italic", "bold"), bg = self.lbl2color, fg = self.fontcolor)
        self.lbl_score.pack(side = TOP, fill = BOTH, expand = 1)

        self.highscoreboard = Label(self.frame, borderwidth = 1, relief = "solid", text = " Highscore ", font = ("Calibri", 15, "italic", "bold"), bg = self.lbl2color, fg = self.fontcolor)
        self.highscoreboard.pack(side = TOP, fill = BOTH)

        with open('highScore.txt', 'r') as self.highScore:
            self.high_score = self.highScore.read()

        self.lbl_highscore = Label(self.frame, borderwidth = 1, relief = "solid", text = self.high_score, font = ("Calibri", 25, "italic", "bold"), bg = self.lbl2color, fg = self.fontcolor)
        self.lbl_highscore.pack(side = TOP, fill = BOTH, expand = 1)
        
        self.lbl_walls = Label(self.frame, borderwidth = 1, relief = "solid", text = "Walls: On", font = ("Calibri", 10, "italic", "bold"), bg = self.lbl2color, fg = self.fontcolor)
        self.lbl_walls.pack(side = TOP, fill = BOTH)
        
        self.lbl_mode = Label(self.frame, borderwidth = 1, relief = "solid", text = "Mode: Hard", font = ("Calibri", 10, "italic", "bold"), bg = self.lbl2color, fg = self.fontcolor)
        self.lbl_mode.pack(side = TOP, fill = BOTH)
        
        self.lbl_speed = Label(self.frame, borderwidth = 1, relief = "solid", text = "Speed: High", font = ("Calibri", 10, "italic", "bold"), bg = self.lbl2color, fg = self.fontcolor)
        self.lbl_speed.pack(side = TOP, fill = BOTH)
        '''-------------------------------------------------------'''
        #############################################################

        #############################################################
        '''-------------------- C O R P O S ----------------------'''
        '''Coordenadas do corpo'''
        self.xi = self.Lx[self.randx]
        self.yi = self.Ly[self.randy]
        self.xf = self.xi + self.dif
        self.yf = self.yi + self.dif

        '''Lista com o corpo da cobra'''
        self.SnakeB = []
        self.SnakeBCoords = []

        '''Coordenadas da comida'''
        self.foodCoords = []
        
        '''Cria um quadrado para ser parte do corpo da cobra'''
        self.Snakebody = self.canvas.create_rectangle(self.xi, self.yi, self.xf, self.yf, fill = self.Sheadcolor, outline = self.borderScolor)

        '''Adiciona o quadrado(parte do corpo) a lista(corpo)'''
        self.SnakeB.append(self.Snakebody)
        self.SnakeBCoords.append(self.canvas.coords(self.Snakebody))

        '''Variavel da capacidade da lista de coordenadas'''
        self.lenCoords = 2

        '''Posicao da comida'''
        self.foodPosition = -2
        '''-------------------------------------------------------'''
        #############################################################
 
        #############################################################
        '''----------------- M O V I M E N T O -------------------'''
        '''Variaveis de condicao para o movimento'''
        self.game = True #True - jogo rodando, False - game over
        self.move = 1 #1 - permite trocar a direcao, 0 - nao permite trocar a direcao

        '''Velocidade do movimento'''
        self.sSpeed = 0.15      #\
        self.nSpeed = 0.1       # \
        self.hSpeed = 0.075     #  \   velocidade de 
        self.uSpeed = 0.035     #  / movimento da cobra
        self.lSpeed = 0.025     # /
        self.v = self.hSpeed    #/ 

        '''Variavel que define se a cobra pode atravessar paredes'''
        self.walls = True

        '''Direcao de movimento'''
        self.direct = 0 #0 - nula, 1 - direita, 2 - esquerda, 3 - para baixo, 4 - para cima
        
        '''Contador'''
        self.moveCount = 0

        '''Variaveis de fim de jogo'''
        self.snakeHit = 0
        
        '''Associa os movimentos da cobra as teclas'''
        self.canvas.bind("<Right>", self.changeDirect)
        self.canvas.bind("<Left>", self.changeDirect)
        self.canvas.bind("<Down>", self.changeDirect)
        self.canvas.bind("<Up>", self.changeDirect)
        self.canvas.focus_set()
        '''-------------------------------------------------------'''
        #############################################################
        
        #############################################################
        '''--------------------- M E N U S -----------------------'''        
        '''Define o menu principal'''
        self.mainmenu = Menu(master)

        '''Define os menus secundarios'''
        self.submenu1 = Menu(self.mainmenu, tearoff = 0)
        self.submenu2 = Menu(self.mainmenu, tearoff = 0)
        self.submenu3 = Menu(self.mainmenu, tearoff = 0)
        self.submenu4 = Menu(self.mainmenu, tearoff = 0)
        
        self.mainmenu.add_cascade(label = "Options", menu = self.submenu1)
        self.mainmenu.add_cascade(label = "Difficulty", menu = self.submenu2)
        self.mainmenu.add_cascade(label = "Help", menu = self.submenu3)
        self.mainmenu.add_cascade(label = "About", menu = self.submenu4)

        '''Adiciona comandos aos menus secundarios'''
        self.submenu1.add_command(label = 'Restart', command = self.gameRestart)
        self.submenu1.add_command(label = 'Walls', command = self.gameWalls)
        self.submenu1.add_command(label = 'Stop', command = self.gameStop)
        self.submenu1.add_command(label = 'Exit', command = self.gameExit)
        
        self.submenu2.add_command(label = 'Easy', command = self.gameEasy)
        self.submenu2.add_command(label = 'Medium', command = self.gameMedium)
        self.submenu2.add_command(label = 'Hard', command = self.gameHard)
        self.submenu2.add_command(label = 'Expert', command = self.gameExpert)
        self.submenu2.add_command(label = 'God', command = self.gameGod)
        
        self.submenu3.add_command(label = 'Instructions', command = self.gameInstructions)
        
        self.submenu4.add_command(label = 'Author', command = self.gameAuthor)
        
        master.config(menu = self.mainmenu)
        '''-------------------------------------------------------'''
        #############################################################
                
        #############################################################
        '''------------------ C H A M A D A S --------------------'''
        '''Chama o metodo de criacao da comida'''
        self.reFood()
        
        '''Chama o metodo de movimento da cobra'''
        self.moveSnake()
        '''-------------------------------------------------------'''
        #############################################################
        
    #############################################################
    '''-------------- C O N F I G U R A C O E S --------------'''    
    '''Reinicia o jogo'''
    def gameRestart(self):
        self.frame.destroy() #destroi o frame
        if self.window == True:
            self.top_restart.destroy() #destroi a janela de restart
        Snake(root) #chama a classe Snake

    '''Muda a dinamica das paredes'''
    def gameWalls(self):
        '''Verifica o status da variavel'''
        if self.walls == False:
            self.walls = True
            self.lbl_walls["text"] = "Walls: On"
        else:
            self.walls = False
            self.lbl_walls["text"] = "Walls: Off"

    '''Pausa o jogo'''
    def gameStop(self):
        self.direct = 0 

    '''Fecha a janela'''
    def gameExit(self):
        root.destroy()

    '''Altera a velocidade da cobra para a intermediaria'''
    def mediumSpeed(self):
        self.v = self.mSpeed #altera o delay no metodo de movimento
        self.lbl_speed["text"] = "Speed: Medium"
        
    '''Altera a velocidade da cobra para uma rapida'''
    def highSpeed(self):
        self.v = self.hSpeed #altera o delay no metodo de movimento
        self.lbl_speed["text"] = "Speed: High"

    '''Altera a velocidade da cobra para a mais rapida'''
    def ultraSpeed(self):
        self.v = self.uSpeed #altera o delay no metodo de movimento
        self.lbl_speed["text"] = "Speed: Ultra"
    
    def gameEasy(self):
        self.v = self.sSpeed #altera o delay no metodo de movimento
        self.gameMode = "Easy"
        self.lbl_speed["text"] = "Speed: Slow"
        self.lbl_mode["text"] = "Mode: Easy"
        self.walls = False
        self.lbl_walls["text"] = "Walls: Off"
        
    def gameMedium(self):
        self.v = self.nSpeed #altera o delay no metodo de movimento
        self.gameMode = "Medium"
        self.lbl_speed["text"] = "Speed: Normal"
        self.lbl_mode["text"] = "Mode: Medium"
        self.walls = False
        self.lbl_walls["text"] = "Walls: Off"
        
    def gameHard(self):
        self.v = self.hSpeed #altera o delay no metodo de movimento
        self.gameMode = "Hard"
        self.lbl_speed["text"] = "Speed: High"
        self.lbl_mode["text"] = "Mode: Hard"
        self.walls = True
        self.lbl_walls["text"] = "Walls: On"

    def gameExpert(self):
        self.v = self.uSpeed #altera o delay no metodo de movimento
        self.gameMode = "Expert"
        self.lbl_speed["text"] = "Speed: Ultra"
        self.lbl_mode["text"] = "Mode: Expert"
        self.walls = True
        self.lbl_walls["text"] = "Walls: On"

    def gameGod(self):
        self.v = self.lSpeed #altera o delay no metodo de movimento
        self.gameMode = "God"
        self.lbl_speed["text"] = "Speed: Light"
        self.lbl_mode["text"] = "Mode: God"
        self.walls = True
        self.lbl_walls["text"] = "Walls: On"
        
    '''Mostra as instrucoes do jogo'''
    def gameInstructions(self):
        '''Abre uma nova janela'''
        self.top = Toplevel()
        self.top["bg"] = self.topbg
        self.top.title("Snake Intructions")

        '''Mensagens da janela'''
        self.msg1 = Label(self.top, bg = self.topbg, font = ("Calibri", 10), text = "Use the arrow keys to change directions")
        self.msg2 = Label(self.top, bg = self.topbg, font = ("Calibri", 10), text = "If it shows'Walls: On',\n the snake will die by hitting them,\n in order to change the walls dynamics,\n click on 'Options', then on 'Walls'")
        self.msg3 = Label(self.top, bg = self.topbg, font = ("Calibri", 10), text = "If you want, you can also change the snake's speed\n by clicking on 'Speed' and choosing a different one")

        self.msg1.pack(side = TOP, fill = BOTH)
        self.msg2.pack(side = TOP, fill = BOTH)
        self.msg3.pack(side = TOP, fill = BOTH)

    def gameAuthor(self):
        '''Abre uma nova janela'''
        self.top = Toplevel()
        self.top["bg"] = self.topbg
        self.top.title("Author section")

        '''Mensagens da janela'''
        self.msg4 = Label(self.top, bg = self.topbg, font = ("Calibri", 10), text = " Game developer: Rodrigo Pita (University Student) \n\n  This game was developed as an assignment for \n programming class Comp II (2017.2)")
        self.msg4.pack(side = TOP, fill = BOTH)
    
    '''Acaba o jogo'''
    def endGame(self):
        if self.gameMode == "Hard" or self.gameMode == "Expert":
            with open('highScore.txt', 'r') as self.highScore:
                score = self.highScore.readline()
                if int(self.score) > int(score):
                    with open('highScore.txt', 'w') as self.highScore:
                        self.highScore.write(str(self.score))
        self.game = False
        self.direct = 0
        if self.snakeHit == 1:
            showerror("Game Over", "Snake hit itself")
        else:
            showerror("Game Over", "Snake hit a wall")
        self.frame.focus_set()
        self.restartWindow()     

    '''Abre uma janela de restart'''
    def restartWindow(self):
        '''Cria a janela'''
        self.top_restart = Toplevel()
        self.top_restart["bg"] = self.topbg
        self.top_restart.title("Game Over")

        '''Cria os labels e buttons para a janela'''
        self.lbl_gameover = Label(self.top_restart, bg = self.topbg, font = ("Calibri", 12), text = "Do you want to play again?")
        self.lbl_gameover.pack(side = TOP, fill = BOTH, expand = 1)
        
        self.lbl1_blank = Label(self.top_restart, bg = self.topbg, height = 3)
        self.lbl1_blank.pack(side = LEFT)
        
        self.lbl2_blank = Label(self.top_restart, bg = self.topbg, width = 5)
        self.lbl2_blank.pack(side = LEFT)
        
        self.btn_restart = Button(self.top_restart, width = 5, bg = self.topbg, font = ("Calibri", 10), text = "Yes", command = self.gameRestart)
        self.btn_restart.pack(side = LEFT)
        
        self.btn_exit = Button(self.top_restart, width = 5, bg = self.topbg, font = ("Calibri", 10), text = "No", command = self.gameExit)
        self.btn_exit.pack(side = LEFT)

        '''Muda a variavel da janela de restart para que ela seja destruida'''
        self.window = True
    '''-------------------------------------------------------'''
    #############################################################

    #############################################################
    '''--------------------- C O B R A -----------------------'''
    '''Metodo de mudanca da direcao'''
    def changeDirect(self, event):
        '''Detecta qual tecla foi pressionada'''
        if event.keysym == "Right":
            '''Impede que a cobra mude apenas sentido do movimento e que chame o mesmo metodo mais de uma vez'''
            if self.direct != 2 and self.direct!= 1 and self.move != 0:
                '''Move a cobra para direita'''        
                self.direct = 1 #muda a variavel da direcao para direita
                self.move = 0 #muda a variavel da condicao da troca de direcao
                
        elif event.keysym == "Left":
            '''Impede que a cobra mude apenas sentido do movimento e que chame o mesmo metodo mais de uma vez'''
            if self.direct != 1 and self.direct!= 2 and self.move != 0:
                '''Move a cobra para esquerda'''
                self.direct = 2 #muda a variavel da direcao para esquerda
                self.move = 0 #muda a variavel da condicao da troca de direcao
                
        elif event.keysym == "Down":
            '''Impede que a cobra mude apenas sentido do movimento e que chame o mesmo metodo mais de uma vez'''
            if self.direct != 4 and self.direct!= 3 and self.move != 0:
                '''Move a cobra para baixo'''        
                self.direct = 3 #muda a variavel da direcao para baixo
                self.move = 0 #muda a variavel da condicao da troca de direcao
                
        elif event.keysym == "Up":
            '''Impede que a cobra mude apenas sentido do movimento e que chame o mesmo metodo mais de uma vez'''
            if self.direct != 3 and self.direct!= 4 and self.move != 0:
                '''Move a cobra para cima'''        
                self.direct = 4 #muda a variavel da direcao para cima
                self.move = 0 #muda a variavel da condicao da troca de direcao
                
    '''Metodo de movimento da cobra'''
    def moveSnake(self):
        '''Faz com que o movimento se repita infinitamente'''
        while self.game == True:
            if int(len(self.SnakeBCoords)) > int(self.lenCoords):
                self.SnakeBCoords.remove(self.SnakeBCoords[0])
            if self.direct == 1:
                '''Move para direita'''
                if int(self.canvas.coords(self.Snakebody)[2]) < int(self.xMax):
                    self.canvas.move(self.SnakeB[0], self.dif, 0)
                    for k in range(1, len(self.SnakeB)):
                        self.canvas.coords(self.SnakeB[k], self.SnakeBCoords[-k][0], self.SnakeBCoords[-k][1], self.SnakeBCoords[-k][2], self.SnakeBCoords[-k][3])

                    self.SnakeBCoords.append(self.canvas.coords(self.Snakebody)) #adiciona as coordenadas do quadrado a lista de coordenadas do corpo da cobra

                else:
                    if self.walls == False:
                        '''Caso a cobra chegue a parede, faz com que ela apareca do lado oposto'''
                        self.canvas.move(self.SnakeB[0], -(self.xMax - (self.dif + self.xMin)), 0)
                        for k in range(1, len(self.SnakeB)):
                            self.canvas.coords(self.SnakeB[k], self.SnakeBCoords[-k][0], self.SnakeBCoords[-k][1], self.SnakeBCoords[-k][2], self.SnakeBCoords[-k][3])

                        self.SnakeBCoords.append(self.canvas.coords(self.Snakebody)) #adiciona as coordenadas do quadrado a lista de coordenadas do corpo da cobra

                    else:
                        self.endGame() #chama um metodo que acaba o jogo
                        
            if self.direct == 2:
                '''Move para esquerda'''
                if int(self.canvas.coords(self.Snakebody)[0]) > int(self.xMin):
                    self.canvas.move(self.SnakeB[0], -self.dif, 0)
                    for k in range(1, len(self.SnakeB)):
                        self.canvas.coords(self.SnakeB[k], self.SnakeBCoords[-k][0], self.SnakeBCoords[-k][1], self.SnakeBCoords[-k][2], self.SnakeBCoords[-k][3])

                    self.SnakeBCoords.append(self.canvas.coords(self.Snakebody)) #adiciona as coordenadas do quadrado a lista de coordenadas do corpo da cobra
                    
                else:
                    if self.walls == False:
                        '''Caso a cobra chegue a parede, faz com que ela apareca do lado oposto'''
                        self.canvas.move(self.SnakeB[0], (self.xMax - (self.dif + self.xMin)), 0)
                        for k in range(1, len(self.SnakeB)):
                            self.canvas.coords(self.SnakeB[k], self.SnakeBCoords[-k][0], self.SnakeBCoords[-k][1], self.SnakeBCoords[-k][2], self.SnakeBCoords[-k][3])

                        self.SnakeBCoords.append(self.canvas.coords(self.Snakebody)) #adiciona as coordenadas do quadrado a lista de coordenadas do corpo da cobra

                    else:
                        self.endGame() #chama um metodo que acaba o jogo
                        
            if self.direct == 3:
                '''Move para baixo'''
                if int(self.canvas.coords(self.Snakebody)[3]) < int(self.yMax):
                    self.canvas.move(self.SnakeB[0], 0, self.dif)
                    for k in range(1, len(self.SnakeB)):
                        self.canvas.coords(self.SnakeB[k], self.SnakeBCoords[-k][0], self.SnakeBCoords[-k][1], self.SnakeBCoords[-k][2], self.SnakeBCoords[-k][3])

                    self.SnakeBCoords.append(self.canvas.coords(self.Snakebody)) #adiciona as coordenadas do quadrado a lista de coordenadas do corpo da cobra

                else:
                    if self.walls == False:
                        '''Caso a cobra chegue a parede, faz com que ela apareca do lado oposto'''
                        self.canvas.move(self.SnakeB[0], 0, -(self.yMax - (self.dif + self.yMin)))
                        for k in range(1, len(self.SnakeB)):
                            self.canvas.coords(self.SnakeB[k], self.SnakeBCoords[-k][0], self.SnakeBCoords[-k][1], self.SnakeBCoords[-k][2], self.SnakeBCoords[-k][3])

                        self.SnakeBCoords.append(self.canvas.coords(self.Snakebody)) #adiciona as coordenadas do quadrado a lista de coordenadas do corpo da cobra
                        
                    else:
                        self.endGame() #chama um metodo que acaba o jogo
                        
            if self.direct == 4:
                '''Move para cima'''
                if int(self.canvas.coords(self.Snakebody)[1]) > int(self.yMin):
                    self.canvas.move(self.SnakeB[0], 0, -self.dif)
                    for k in range(1, len(self.SnakeB)):
                        self.canvas.coords(self.SnakeB[k], self.SnakeBCoords[-k][0], self.SnakeBCoords[-k][1], self.SnakeBCoords[-k][2], self.SnakeBCoords[-k][3])
                        
                    self.SnakeBCoords.append(self.canvas.coords(self.Snakebody)) #adiciona as coordenadas do quadrado a lista de coordenadas do corpo da cobra
                
                else:
                    if self.walls == False:
                        '''Caso a cobra chegue a parede, faz com que ela apareca do lado oposto'''
                        self.canvas.move(self.SnakeB[0], 0, (self.yMax - (self.dif + self.yMin)))
                        for k in range(1, len(self.SnakeB)):
                            self.canvas.coords(self.SnakeB[k], self.SnakeBCoords[-k][0], self.SnakeBCoords[-k][1], self.SnakeBCoords[-k][2], self.SnakeBCoords[-k][3])

                        self.SnakeBCoords.append(self.canvas.coords(self.Snakebody)) #adiciona as coordenadas do quadrado a lista de coordenadas do corpo da cobra
                        
                    else:
                        self.endGame() #chama um metodo que acaba o jogo

            if len(self.SnakeB) > 1:
                self.canvas.itemconfig(self.SnakeB[-1], fill = self.Scolor) #muda a cor da ponta da cobra para a padrao
            self.moveCount += 1 #contador de movimentos

            '''Impede que a comida apareca dentro da cobra mais de uma vez'''
            if self.moveCount > len(self.SnakeB):
                self.foodPosition = -1

            else:
                self.foodPosition = -2
            '''Detecta quando a coordenada da cabeca da cobra se iguala a da comida'''
            if self.canvas.coords(self.SnakeB[0]) == self.canvas.coords(self.food):
                self.canvas.delete(self.food) #apaga a comida
                self.snakeGrow() #chama o metodo de crescimento da cobra
                self.reFood() #chama o metodo para criar outra comida
                self.lenCoords += 1 #aumenta a capacidade da lista de coordenadas

            else:
                '''Deixa a cobra da cor original novamente'''
                for k in range(1, len(self.SnakeB)):
                    if self.canvas.coords(self.SnakeB[k]) == self.foodCoords[self.foodPosition]:
                        self.canvas.itemconfig(self.SnakeB[k], fill = self.Fcolors[self.i-1])
                        if (k-1) != 0:
                            self.canvas.itemconfig(self.SnakeB[k-1], fill = self.Scolor)
                    
            if len(self.SnakeB) >= 3:
                self.count = 0
                for i in range(2, len(self.SnakeBCoords)-1):
                    '''Detecta se a coordenada da cabeca da cobra se iguala as do resto do corpo'''
                    if self.canvas.coords(self.SnakeB[0]) == self.SnakeBCoords[i]:
                        self.count += 1
                        if self.count != 0:
                            self.snakeHit = 1
                            self.endGame() #chama um metodo que acaba o jogo
                            
            self.move = 1 #permite que mude a direcao
            self.canvas.update() #atualiza o canvas para o movimento continuar
            time.sleep(self.v) #cria um delay para ajustar a velocidade da cobra

    '''Metodo de criacao da comida'''
    def reFood(self):
        '''Cria a condicao para o while ser se repetir'''
        self.food = 0
        self.moveCount = 0
        
        while self.food == 0:
            '''Embaralha a lista com as possiveis coordenadas da comida'''
            shuffle(self.Lx)
            shuffle(self.Ly)

            '''Atribui as coordenadas a comida'''
            self.x1 = self.Lx[0]
            self.y1 = self.Ly[0]
            
            if [float(self.x1), float(self.y1), float(self.x1+self.dif), float(self.y1+self.dif)] not in self.SnakeBCoords:
                '''Cria a comida'''                
                self.food = self.canvas.create_oval(self.x1, self.y1, self.x1+self.dif, self.y1+self.dif, fill = self.Fcolor, outline = self.borderScolor)
                self.foodCoords.append(self.canvas.coords(self.food))

    '''Aumenta a cobra'''
    def snakeGrow(self):
        '''Cria um quadrado para adicionar no corpo da cobra'''
        time.sleep(self.v)
        self.Snakebodyplus = self.canvas.create_rectangle(self.canvas.coords(self.Snakebody), fill = self.Scolor, outline = self.borderScolor)
        self.SnakeB.append(self.Snakebodyplus) #insere o quadrado a lista do corpo da cobra
        
        '''Aumenta a pontuacao'''
        self.score += 1
        self.lbl_score["text"] += 1

        if self.score >= self.high_score:
            self.high_score = self.score
     
        if self.Fcolor == self.Fcolors[self.i]:
            '''Define a lista de cores como limite de mudanca entre as cores da comida'''
            if self.i < (len(self.Fcolors)-1):
                self.i += 1
            else:
                self.i = 0
                
            '''Muda a cor da comida'''
            self.Fcolor = self.Fcolors[self.i]
    '''-------------------------------------------------------'''
    #############################################################

root = Tk()
Snake(root)
root.mainloop()
