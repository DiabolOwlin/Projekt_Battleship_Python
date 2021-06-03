from tkinter import *
from tkinter import messagebox
import numpy as np
import time
import random

window = Tk()
app_running = True

size_canvas_x = 600
size_canvas_y = 400
x = y = 10
step_x = 200 // x
step_y = 200 // y

menu_x = 150

ships = 10
ship_len1 = 1
ship_len2 = 2
ship_len3 = 3
ship_len4 = 4
list_ids = []  # список объектов canvas


def on_closing():
    global app_running
    if messagebox.askokcancel("Exit the game", "Do you want to exit?"):
        app_running = False
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)
window.title("Игра Морской Бой")
window.resizable(0, 0)
window.wm_attributes("-topmost", 1)
canvas = Canvas(window, width=size_canvas_x + menu_x, height=size_canvas_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.pack()
window.update()


def draw_board():
    for i in range(x + 1):
        canvas.create_line(50 + step_x * i, 50, 50 + step_x * i, size_canvas_y - 150)  # X-LINE
        canvas.create_line(50, 50 + step_y * i, size_canvas_x - 350, 50 + step_y * i)  # Y-LINE

        canvas.create_line(350 + step_x * i, 50, 350 + step_x * i, size_canvas_y - 150)  # X-LINE
        canvas.create_line(350, 50 + step_y * i, size_canvas_x - 50, 50 + step_y * i)  # Y-LINE


draw_board()

#coord_x = Label(text="A  B  C  D  E  F  G  H  I  J", font=("Arial", 13))
#coord_x.place(x=50, y=25)
#coord_x.config(bg="white")


# coord_y = Label(text = "1\n\n2\n\n3\n\n4\n\n5\n\n6\n\n7\n\n8\n\n9\n\n10")
# coord_y.place(x=40, y=60)
# coord_y.config(bg = "white")

def button_show_enemy_ships():
    for i in range(0, x):
        for j in range(0, y):
            if enemy_ships[j][i] > 0:
                _id = canvas.create_rectangle(350 + i * step_x, 50 + j * step_y, 350 + i * step_x + step_x,
                                              50 + j * step_y + step_y,
                                              fill="red")
                list_ids.append(_id)


def button_play_again():
    global list_ids
    for element in list_ids:
        canvas.delete(element)
    list_ids = []
    generate_enemy_ships()

b0 = Button(window, text="Show enemy ships", command=button_show_enemy_ships)
b0.place(x=size_canvas_x + 20, y=30)

b1 = Button(window, text="Play again", command=button_play_again)
b1.place(x=size_canvas_x + 20, y=70)


def add_to_all(event):
    _type = 0  # ЛКМ
    if event.num == 3:
        _type = 1  # ПКМ
    # print(_type)

    mouse_x = -50 + canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = -50 + canvas.winfo_pointery() - canvas.winfo_rooty()

    if mouse_x >= 300:
        game_coord_x = (mouse_x - 300) // step_x
    else:
        game_coord_x = mouse_x // step_x
    game_coord_y = mouse_y // step_y
    print(f"Coordinates: {game_coord_x}:{game_coord_y}, click type: {_type}")


canvas.bind_all("<Button-1>", add_to_all)  # LKM
canvas.bind_all("<Button-3>", add_to_all)  # PKM


def generate_enemy_ships():
    global enemy_ships
    ships_list = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    sum_len_all_ships = sum(ships_list)
    enemy_ships = np.array([[0 for i in range(x)] for j in range(y)])
    sum_len_enemy_ships = 0

    while sum_len_enemy_ships != sum_len_all_ships:

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
                check_near_ships = 0
                check_near_ships = enemy_ships[coord_x - 1][coord_y - 1] + \
                                   enemy_ships[coord_x][coord_y - 1] + \
                                   enemy_ships[coord_x + 1][coord_y - 1] + \
                                   enemy_ships[coord_x - 1][coord_y] + \
                                   enemy_ships[coord_x][coord_y] + \
                                   enemy_ships[coord_x + 1][coord_y]

                for j in range(length):
                    check_near_ships += enemy_ships[coord_x - 1][coord_y + 1 + j] + \
                                        enemy_ships[coord_x][coord_y + 1 + j] + \
                                        enemy_ships[coord_x + 1][coord_y + 1 + j]

                if check_near_ships == 0:
                    for j in range(length):
                        enemy_ships[coord_x][coord_y + j] = 1

                    ships_list.remove(length)
                    print(ships_list)
                    sum_len_enemy_ships += length

            except Exception:
                pass

        if horizont_vertical == 2:
            try:
                check_near_ships = 0
                check_near_ships = enemy_ships[coord_x-1][coord_y-1] + \
                                   enemy_ships[coord_x-1][coord_y] + \
                                   enemy_ships[coord_x-1][coord_y+1] + \
                                   enemy_ships[coord_x][coord_y-1] + \
                                   enemy_ships[coord_x][coord_y] + \
                                   enemy_ships[coord_x][coord_y+1]

                for i in range(length):
                    check_near_ships += enemy_ships[coord_x+1+i][coord_y-1] + \
                    enemy_ships[coord_x+1+i][coord_y] + \
                    enemy_ships[coord_x+1+i][coord_y+1]

                if check_near_ships == 0:
                    for i in range(length):
                        enemy_ships[coord_x+i][coord_y] = 1

                    ships_list.remove(length)
                    print(ships_list)
                    sum_len_enemy_ships += length

            except Exception:
                pass





        # # print(horizont_vertical, primerno_x,primerno_y)
        # if horizont_vertical == 1:
        #     if primerno_x + length <= x:
        #         for j in range(0, length):
        #             try:
        #                 check_near_ships = 0
        #                 check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
        #                                    enemy_ships[primerno_y][primerno_x + j] + \
        #                                    enemy_ships[primerno_y][primerno_x + j + 1] + \
        #                                    enemy_ships[primerno_y][primerno_x + j - 1] + \
        #                                    enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
        #                                    enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
        #                                    enemy_ships[primerno_y + 1][primerno_x + j] + \
        #                                    enemy_ships[primerno_y - 1][primerno_x + j]
        #                 # print(check_near_ships)
        #                 if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
        #                     enemy_ships[primerno_y][primerno_x + j] = 1 # записываем номер корабля
        #                     ships_list.remove(length)
        #                     print(ships_list)
        #                     sum_len_enemy_ships += length
        #             except Exception:
        #                 pass
        #
        # if horizont_vertical == 2:
        #     if primerno_y + length <= y:
        #         for j in range(0, length):
        #             try:
        #                 check_near_ships = 0
        #                 check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
        #                                    enemy_ships[primerno_y + j][primerno_x] + \
        #                                    enemy_ships[primerno_y + j + 1][primerno_x] + \
        #                                    enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
        #                                    enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
        #                                    enemy_ships[primerno_y + j][primerno_x + 1] + \
        #                                    enemy_ships[primerno_y + j][primerno_x - 1]
        #                 # print(check_near_ships)
        #                 if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
        #                     enemy_ships[primerno_y + j][primerno_x] = 1  # записываем номер корабля
        #                     ships_list.remove(length)
        #                     print(ships_list)
        #                     sum_len_enemy_ships += length
        #             except Exception:
        #                 pass

        # делаем подсчет 1ц
        #sum_len_enemy_ships = 0
        #for i in range(0, x):
        #    for j in range(0, y):
        #        if enemy_ships[j][i] > 0:
        #            sum_len_enemy_ships = sum_len_enemy_ships + 1

    print(sum_len_enemy_ships)
    # print(ships_list)
    print(enemy_ships)

generate_enemy_ships()

while app_running:
    if app_running:
        window.update_idletasks()
        window.update()
    time.sleep(0.005)
