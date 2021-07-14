#-----------------Boilerplate Code Start-----------
import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk, Image


screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

leftBoxes = []
rightBoxes = []
finishingBox = None

playerType = None
dice = None

rollButton = None


#-----------------Boilerplate Code End-----------




def rollDice():
    global SERVER
    #create a number variable in which the list of all the ASCII characters of the string will be stored
    #Use backslash because unicode must have a backslash
    diceChoices=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']

    #configure the label
    value = random.choice(diceChoices)

    global playerType
    global rollButton
    global playerTurn

    rollButton.destroy()
    playerTurn = False

    if(playerType == 'player1'):
        SERVER.send(f'{value}player2Turn'.encode())

    if(playerType == 'player2'):
        SERVER.send(f'{value}player1Turn'.encode())

# Teacher Activity
def leftBoard():
    global gameWindow
    global leftBoxes
    global screen_height

    xPos = 30
    for box in range(0,11):
        if(box == 0):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="red")
            boxLabel.place(x=xPos, y=screen_height/2 - 88)
            leftBoxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",55), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2- 100)
            leftBoxes.append(boxLabel)
            xPos +=75

#  Teacher Activity
def rightBoard():
    global gameWindow
    global rightBoxes
    global screen_height

    xPos = 988
    for box in range(0,11):
        if(box == 10):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="yellow")
            boxLabel.place(x=xPos, y=screen_height/2-88)
            rightBoxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",55), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2 - 100)
            rightBoxes.append(boxLabel)
            xPos +=75

# Boilerplate Code
def finishingBox():
    global gameWindow
    global finishingBox
    global screen_width
    global screen_height

    finishingBox = Label(gameWindow, text="Home", font=("Chalkboard SE", 32), width=8, height=4, borderwidth=0, bg="green", fg="white")
    finishingBox.place(x=screen_width/2 - 68, y=screen_height/2 -160)



def gameWindow():
    # ----------- Boilerplate Code start----------
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice



    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    # Add Text
    canvas2.create_text( screen_width/2, screen_height/5, text = "Ludo Ladder", font=("Chalkboard SE",100), fill="white")

    # ----------- Boilerplate Code End----------


    # Teacher Activity
    leftBoard()
    rightBoard()

    # ----------- Boilerplate Code start----------
    finishingBox()
    # ----------- Boilerplate Code End----------


    # student activity
    global rollButton

    rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)

    global playerTurn
    global playerType
    global playerName


    if(playerType == 'player1' and playerTurn):
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
    else:
        rollButton.pack_forget()


    # ---------------Boilerplate Code Start

    # Creating Dice with value 1
    dice = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 100, text = "\u2680", font=("Chalkboard SE",250), fill="white")

    gameWindow.resizable(True, True)
    gameWindow.mainloop()

    # -----------------Boilerplate Code End



def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    # Boilerplate Code
    gameWindow()



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes('-fullscreen',True)


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    # Display image
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2, screen_height/5, text = "Enter Name", font=("Chalkboard SE",100), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 50), bd=5, bg='white')
    nameEntry.place(x = screen_width/2 - 220, y=screen_height/4 + 100)


    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=15, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x = screen_width/2 - 130, y=screen_height/2 - 30)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()



# Boilerplate Code
def recivedMsg():
   pass


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 6000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    # Boilerplate Code
    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()




setup()
