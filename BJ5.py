from tkinter import *
from random import *
import time

root = Tk()
root.geometry("1440x900")
canvas = Canvas(root, width=1440, height=900)
canvas.pack(anchor="nw")
card_base = PhotoImage(file="Test_Images/blue_back.png")
card_base = card_base.subsample(3)
def base_card():
    canvas.create_image(4, 4, image=card_base, anchor="nw")
    canvas.create_image(2, 2, image=card_base, anchor="nw")
    canvas.create_image(0, 0, image=card_base, anchor="nw")
base_card()
card_deck = []

hej = [0] * 52
hej[1] = (1,6) #på index x byt ut 0 med tippeln
print(hej)

[(1,)]

suits = ["S","C","D","H"]
ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]


rank_index = suits_index = 0


kortlista = ["Test_Images/10D.png","Test_Images/KS.png"]
for i in kortlista:
    img = PhotoImage(file=i)
    img = img.subsample(3)
    card_deck.append(img)


#Global
card_list_main = []
card_list_s1 = []
card_list_s2 = []
current_list = []
pic = []
split_1 = False
split_2 = False

def move(x):
    for i in range(3):
        canvas.move(x, 20, 0)
        root.update()

def animation(x,pos):
    while canvas.coords(x)[0] != pos[0]:
        canvas.move(x,20,0)
        root.update()
    while canvas.coords(x)[1] != pos[1]:
        canvas.move(x, 0, 20)
        root.update()

def draw(pos):
    button_split.configure(state=DISABLED)
    button_draw.configure(state=DISABLED)
    hide = canvas.create_image(0, 0, image=card_base, anchor="nw")
    animation(hide, pos)
    pic.append(choice(card_deck))
    p = canvas.coords(hide)
    canvas.delete(hide)
    card = canvas.create_image(p[0], p[1], image=pic[-1], anchor="nw")
    button_draw.configure(state=DISABLED)
    if len(card_list_main) == 2: #and card_number_1 == card_number_2
        button_split.configure(state=NORMAL)
    else:
        button_split.configure(state=DISABLED)
    button_draw.configure(state=NORMAL)
    if split_1 == True:
        card_list_s1.append(card)
        current_list = card_list_s1
    elif split_2 == True:
        card_list_s2.append(card)
        current_list = card_list_s2
    else:
        card_list_main.append(card)
        current_list = card_list_main
    #Split func
    if len(current_list) > 1:
        for i in current_list:
            if i != current_list[-1]:
                move(i)

def split():
    global split_1
    button_split.configure(state=DISABLED)
    button_draw.configure(state=DISABLED)
    card_list_s2.append(card_list_main[0])
    card_list_s1.append(card_list_main[1])
    while canvas.coords(card_list_s2[0])[0] < 720:
        canvas.move(card_list_s2[0], 20, 0)
        root.update()
    while canvas.coords(card_list_s1[0])[0] > 20:
        canvas.move(card_list_s1[0], -20, 0)
        root.update()
    card_list_main.clear()
    split_1 = True
    button_draw.configure(state=NORMAL)
    return split_1

def position():
    global split_1
    global split_2
    main = [500, 460]
    split1 = [20, 460]
    split2 = [720, 460]
    if split_1 == True:
        return draw(split1)
    elif split_2 == True:
        return draw(split2)
    else:
        return draw(main)


def reset():
    global split_1
    global split_2
    for i in [card_list_main,card_list_s1,card_list_s2,pic,current_list,dealer_list,dpic,dealer_list]:
        i.clear()
    dealer_total = 0
    split_1 = False
    split_2 = False
    canvas.delete("all")
    base_card()
    try:
        label.destroy()
    except:
        pass
    button_stay.configure(state=NORMAL)
    button_draw.configure(state=NORMAL)
    start()

dpic = []
dealer_list = []
dealer_total = 15

def dealer_play():
    pos = canvas.coords(dealer_list[-1])
    canvas.delete(dealer_list[-1])
    dpic.append(choice(card_deck))
    dcard = canvas.create_image(pos[0], pos[1], image=dpic[-1], anchor="nw")
    dealer_list.pop(-1)
    dealer_list.append(dcard)
    for i in range(2): #ska egentligen vara en while loop där man lägger ihop kortens totala summa
        if dealer_total < 16:
            draw_dealer()


def stay():
    global split_1
    global split_2
    global label
    if split_1 == True:
        split_1 = False
        split_2 = True
        return
    button_stay.configure(state=DISABLED)
    button_draw.configure(state=DISABLED)
    #checka vem som vann
    label = Label(root, text="VEM VANN", bg="red")
    label.place(x=500, y=200)
    dealer_play()
    print(card_list_main,card_list_s1, card_list_s2,dealer_list)

def draw_dealer():
    button_draw.configure(state=DISABLED)
    button_split.configure(state=DISABLED)
    if len(dpic) == 1:
        dpic.append(card_base)
    else:
        dpic.append(choice(card_deck))
    dcard = canvas.create_image(0, 0, image=dpic[-1], anchor="nw")
    dealer_list.append(dcard)
    animation(dcard, [500,40])
    if len(dealer_list) > 1:
        for i in dealer_list:
            if i != dealer_list[-1]:
                move(i)
    button_draw.configure(state=NORMAL)
    button_split.configure(state=NORMAL)

def start():
    button_stay.configure(state=DISABLED)
    button_draw.configure(state=DISABLED)
    draw([500, 460])
    draw([500, 460])
    draw_dealer()
    draw_dealer()
    button_draw.configure(state=NORMAL)
    button_stay.configure(state=NORMAL)

button_draw = Button(root, text = "Draw", width = 10, height = 5, command = lambda: position())
button_draw.place(x=1000,y=10)
button_split = Button(root, text = "Split", width = 10, height = 5, command = lambda: split(), state = DISABLED)
button_split.place(x=1100,y=10)
button_stay = Button(root, text = "Stay", width = 10, height = 5, command = lambda: stay(), state = NORMAL)
button_stay.place(x=1200,y=10)
button_reset = Button(root, text = "Reset", width = 10, height = 5, command = lambda: reset(), state = NORMAL)
button_reset.place(x=1300,y=10)

start()

root.mainloop()