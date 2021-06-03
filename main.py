from tkinter import *
from tkinter import messagebox
import numpy as np
import time
import random

window = Tk()
app_running = True

size_canvas_x = 500
size_canvas_y = 500
x = y = 10
step_x = size_canvas_x // x
step_y = size_canvas_y // y

menu_x = step_x * 4  # 200
menu_y = 40

ships = 10
ship_len1 = 1
ship_len2 = 2
ship_len3 = 3
ship_len4 = 4
sum_shot_down_player1_ships = 0
sum_shot_down_player2_ships = 0
list_ids = [] # список объектов canvas

#sum_len_player1_ships = 0
#sum_len_player2_ships = 0

player1_ships = np.array([[0 for i in range(x)] for j in range(y)])
player2_ships = np.array([[0 for i in range(x)] for j in range(y)])


already_clicked_player1 = np.array([[-1 for i in range(x)] for j in range(y)])
already_clicked_player2 = np.array([[-1 for i in range(x)] for j in range(y)])


def on_closing():
    global app_running
    if messagebox.askokcancel("Exit the game", "Do you want to exit?"):
        app_running = False
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)
window.title("Battleships")
window.resizable(0, 0)
window.wm_attributes("-topmost", 1)
canvas = Canvas(window, width=size_canvas_x + menu_x + size_canvas_x, height=size_canvas_y + menu_y, bd=0,
                highlightthickness=0)

canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x + menu_x + size_canvas_x, size_canvas_y,
                        fill="white")
canvas.pack()
window.update()


def draw_board(offset_x=0):
    for i in range(x + 1):
        for i in range(0, x + 1):
            canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, size_canvas_y)
        for i in range(0, y + 1):
            canvas.create_line(offset_x, step_y * i, offset_x + size_canvas_x, step_y * i)


draw_board()
draw_board(size_canvas_x + menu_x)

t0 = Label(window, text="Player 1", font=("Comic Sans", 16))
t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3)
t1 = Label(window, text="Player 2", font=("Comic Sans", 16))
t1.place(x=size_canvas_x + menu_x + size_canvas_x // 2 - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3)

t0.configure(bg="red")
t0.configure(bg="#f0f0f0")


# coord_x = Label(text="A  B  C  D  E  F  G  H  I  J", font=("Arial", 13))
# coord_x.place(x=50, y=25)
# coord_x.config(bg="white")


# coord_y = Label(text = "1\n\n2\n\n3\n\n4\n\n5\n\n6\n\n7\n\n8\n\n9\n\n10")
# coord_y.place(x=40, y=60)
# coord_y.config(bg = "white")

def button_show_player_ships(player_ships, offset_x=0):
    for i in range(0, x):
        for j in range(0, y):
            if player_ships[j][i] > 0:
                _id = canvas.create_rectangle(offset_x + i * step_x, j * step_y, offset_x + i * step_x + step_x, j * step_y + step_y,
                                              fill="blue")
                list_ids.append(_id)


def button_play_again():
    global list_ids
    global already_clicked_player1, already_clicked_player2
    global player1_ships, player2_ships
    global sum_len_player1_ships, sum_len_player2_ships

    for element in list_ids:
        canvas.delete(element)
    list_ids = []
    already_clicked_player1 = np.array([[-1 for i in range(x)] for j in range(y)])
    already_clicked_player2 = np.array([[-1 for i in range(x)] for j in range(y)])
    player1_ships, sum_len_player1_ships = generate_player_ships()
    player2_ships, sum_len_player2_ships = generate_player_ships()


b0 = Button(window, text="Show Player 1 ships", command=lambda: button_show_player_ships(player1_ships))
b0.place(x=size_canvas_x + 20, y=30)

b1 = Button(window, text="Show Player 2 ships", command=lambda: button_show_player_ships(player2_ships, size_canvas_x + menu_x))
b1.place(x=size_canvas_x + 20, y=70)

b2 = Button(window, text="Play again", command=button_play_again)
b2.place(x=size_canvas_x + 20, y=110)


def draw_point(x, y):
    print(player1_ships[y][x])
    if player1_ships[y][x] == 0:
        id1 = canvas.create_oval(x * step_x, y * step_y,
                                 x * step_x + step_x,
                                 y * step_y + step_y,
                                 fill="white")
        id2 = canvas.create_oval(x * step_x + step_x // 3, y * step_y + step_y // 3,
                                 x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3,
                                 fill="white")
        id3 = canvas.create_oval(x * step_x + step_x // 3, y * step_y + step_y // 3,
                                 x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3,
                                 fill="white")
        list_ids.append(id1)
        list_ids.append(id2)
        list_ids.append(id3)
    else:
        id4 = canvas.create_rectangle(x * step_x, y * step_y,
                                      x * step_x + step_x, y * step_y + step_y,
                                      fill="red")
        list_ids.append(id4)


def check_winner():
    win = False
    if sum_shot_down_player1_ships == sum_len_player1_ships:
        win = True
    return win


def add_to_all(event):
    global sum_shot_down_player1_ships
    _type = 0  # ЛКМ
    if event.num == 3:
        _type = 1  # ПКМ
    # print(_type)

    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()

    # if mouse_x >= 300:
    #     game_coord_x = (mouse_x - 300) // step_x
    # else:
    #     game_coord_x = mouse_x // step_x
    #
    # game_coord_y = mouse_y // step_y
    game_coord_x = mouse_x // step_x
    game_coord_y = mouse_y // step_y

    print(f"Coordinates: {game_coord_x}:{game_coord_y}, click type: {_type}")

    if 0 <= game_coord_x < x and 0 <= game_coord_y < y:
        if already_clicked_player1[game_coord_y][game_coord_x] == -1:
            if player1_ships[game_coord_y][game_coord_x] > 0:
                sum_shot_down_player1_ships += 1
            already_clicked_player1[game_coord_y][game_coord_x] = _type
            draw_point(game_coord_x, game_coord_y)

            if check_winner():
                print("Win!")
        print(len(list_ids))


canvas.bind_all("<Button-1>", add_to_all)  # LKM
canvas.bind_all("<Button-3>", add_to_all)  # PKM


def generate_player_ships():

    ships_list = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    sum_len_all_ships = sum(ships_list)
    player_ships = np.array([[0 for i in range(x)] for j in range(y)])
    sum_len_player_ships = 0

    while sum_len_player_ships != sum_len_all_ships:

        length = ships_list[0]
        horizont_vertical = random.randrange(1, 3)  # 1- горизонтальное 2 - вертикальное

        coord_x = random.randrange(0, x)
        coord_y = random.randrange(0, y)

        if horizont_vertical == 1:
            if coord_y + (length - 1) > y:
                coord_y = coord_y - (length - 1)

        else:
            if coord_x + (length - 1) > x:
                coord_x = coord_x - (length - 1)

        if horizont_vertical == 1:
            try:
                check_near_ships = player_ships[coord_x - 1][coord_y - 1] + \
                                   player_ships[coord_x][coord_y - 1] + \
                                   player_ships[coord_x + 1][coord_y - 1] + \
                                   player_ships[coord_x - 1][coord_y] + \
                                   player_ships[coord_x][coord_y] + \
                                   player_ships[coord_x + 1][coord_y]

                for j in range(length):
                    check_near_ships += player_ships[coord_x - 1][coord_y + 1 + j] + \
                                        player_ships[coord_x][coord_y + 1 + j] + \
                                        player_ships[coord_x + 1][coord_y + 1 + j]

                if check_near_ships == 0:
                    for j in range(length):
                        player_ships[coord_x][coord_y + j] = 1

                    ships_list.remove(length)
                    # print(ships_list)
                    sum_len_player_ships += length

            except Exception:
                pass

        if horizont_vertical == 2:
            try:
                check_near_ships = 0
                check_near_ships = player_ships[coord_x - 1][coord_y - 1] + \
                                   player_ships[coord_x - 1][coord_y] + \
                                   player_ships[coord_x - 1][coord_y + 1] + \
                                   player_ships[coord_x][coord_y - 1] + \
                                   player_ships[coord_x][coord_y] + \
                                   player_ships[coord_x][coord_y + 1]

                for i in range(length):
                    check_near_ships += player_ships[coord_x + 1 + i][coord_y - 1] + \
                                        player_ships[coord_x + 1 + i][coord_y] + \
                                        player_ships[coord_x + 1 + i][coord_y + 1]

                if check_near_ships == 0:
                    for i in range(length):
                        player_ships[coord_x + i][coord_y] = 1

                    ships_list.remove(length)
                    # print(ships_list)
                    sum_len_player_ships += length

            except Exception:
                pass

    print(sum_len_player_ships)
    print(player_ships)
    return player_ships, sum_len_player_ships


player1_ships, sum_len_player1_ships = generate_player_ships()
player2_ships, sum_len_player2_ships = generate_player_ships()

while app_running:
    if app_running:
        window.update_idletasks()
        window.update()
    time.sleep(0.005)
