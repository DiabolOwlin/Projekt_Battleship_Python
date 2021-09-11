from tkinter import *
from tkinter import messagebox
import numpy as np
import time
import random
import game_functions as game_func

window = Tk()
app_running = True

size_canvas_x = 500                                                             # size of the one canvas
size_canvas_y = 500                                                             #
x = y = 10                                                                      # size of gaming field
step_x = size_canvas_x // x
step_y = size_canvas_y // y

delta_menu_x = 4                                                                # size of the menu
menu_x = step_x * delta_menu_x  # 200
menu_y = 40

sum_shot_down_player1_ships = 0                                                 # sum of shot down ships of each players
sum_shot_down_player2_ships = 0                                                 #
list_ids = []                                                                   # list of canvas objects
list_deploying = []                                                             # list of figures created by manually deploying ships
list_used = np.array([0 for _ in range(10)])                                    # additional list for checking purpose in game preparations

sum_len_player1_ships = 20
sum_len_player2_ships = 20

player1_ships = np.array([[0 for _ in range(x + 1)] for _ in range(y + 1)])             # array of player 1`s ships
player2_ships = np.array([[0 for _ in range(x + 1)] for _ in range(y + 1)])             # array of player 2`s ships

already_clicked_player1 = np.array([[5 for _ in range(x + 1)] for _ in range(y + 1)])       # array of player 1`s shots
already_clicked_player2 = np.array([[5 for _ in range(x + 1)] for _ in range(y + 1)])       # array of player 2`s shots

player1_turn = random.choice([True, False])                          # a variable to determine which player has a turn
add_to_label = ""

computer = False                                                     # a variable to determine who we`re playing against


def on_closing():
    ''' a function which destroy our "window" if we want to close it with additional warning window '''
    global app_running
    if messagebox.askokcancel("Exit the game", "Do you want to exit?"):
        app_running = False
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)
window.title("Battleships")
window.resizable(0, 0)                                      # restrictable size of the our app
canvas = Canvas(window, width=size_canvas_x + menu_x + size_canvas_x, height=size_canvas_y + menu_y, bd=0,
                highlightthickness=0)

canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x + menu_x + size_canvas_x, size_canvas_y,
                        fill="white")
canvas.pack()
window.update()


def draw_board(offset_x=0):
    ''' a function that draws field 10x10 on our canvas '''
    for i in range(0, x + 1):
        canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, size_canvas_y)
    for i in range(0, y + 1):
        canvas.create_line(offset_x, step_y * i, offset_x + size_canvas_x, step_y * i)


draw_board()                                                                                      # field for player 1
draw_board(size_canvas_x + menu_x)                                                                # field for player 2

t0 = Label(window, text="Player 1", font=("Comic Sans", 16), fg="blue")
t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3)
t1 = Label(window, text="Player 2", font=("Comic Sans", 16), fg='red')
t1.place(x=size_canvas_x + menu_x + size_canvas_x // 2 - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3)

t3 = Label(window, text="", font=("Comic Sans", 16))
t3.place(x=size_canvas_x + (step_x // 2) - t3.winfo_reqwidth() // 2, y=size_canvas_y // 2)             # label to show in real time whome turn is

t2_result = Label(window, text="", font=("Comic Sans", 16))
t2_result.place(x=size_canvas_x + 20 - t2_result.winfo_reqwidth() // 2, y=size_canvas_y - step_y * 3)   # label to show the result of player`s turn


def button_show_player_ships(player_ships, already_clicked_player, offset_x=0, color="blue"):
    ''' a function that shows player`s fleet deployment '''
    for i in range(0, x):
        for j in range(0, y):
            if player_ships[j][i] > 0:
                if already_clicked_player[j][i] == 0:
                    pass
                else:
                    _id = canvas.create_rectangle(offset_x + i * step_x, j * step_y, offset_x + i * step_x + step_x,        # drawing a rectangle in cell where a part of ship is
                                                  j * step_y + step_y,
                                                  fill=color)
                    list_ids.append(_id)                                                    # adding a shape to the list that will be used to clean up the canvas


def button_reset(comp):
    ''' a function for button "Reset" that cleans up the canvas or restarting the game '''
    global player1_ships, player2_ships
    global list_ids, computer, add_to_label, list_deploying
    global already_clicked_player1, already_clicked_player2
    global sum_shot_down_player1_ships, sum_shot_down_player2_ships

    global start_button, reset_button, generate_fleet_button
    global t2_result, t3

    for element in list_ids:                                                            # cleaning up the canvas
        canvas.delete(element)
    list_ids = []

    for element in list_deploying:                                                      # cleaning up the list of figures created by manually deploying ships
        canvas.delete(element)
    list_deploying = []

    t2_result.destroy()
    t3.destroy()

    already_clicked_player1 = np.array([[5 for i in range(x + 1)] for j in range(y + 1)])       # resetting arrays of players` shots
    already_clicked_player2 = np.array([[5 for i in range(x + 1)] for j in range(y + 1)])       #

    player1_ships = np.array([[0 for i in range(x + 1)] for j in range(y + 1)])                 # resetting arrays of players` ships
    player2_ships = np.array([[0 for i in range(x + 1)] for j in range(y + 1)])                 #

    sum_shot_down_player1_ships = 0                                                             # reseting sum of shot down ships of each players
    sum_shot_down_player2_ships = 0
    t0.configure(bg="#f0f0f0", fg="blue")
    t1.configure(bg="#f0f0f0", fg="red")

    t3 = Label(window, text="", font=("Comic Sans", 16))
    t3.place(x=size_canvas_x + (step_x // 2) - t3.winfo_reqwidth() // 2, y=size_canvas_y // 2)

    t2_result = Label(window, text="", font=("Comic Sans", 16))
    t2_result.place(x=size_canvas_x + 20 - t2_result.winfo_reqwidth() // 2, y=size_canvas_y - step_y * 3)

    if comp:
        computer = True
        canvas.bind_all("<Button-3>", place_ships)  # RMB                       # activation right-click binding for manually deploying ships
        t1.configure(text="Player 2 (Computer)")

        generate_fleet_button["state"] = ACTIVE
        start_button["state"] = ACTIVE
        reset_button["state"] = ACTIVE
    else:
        computer = False
        t1.configure(text="Player 2")
        start_button["state"] = ACTIVE
        reset_button["state"] = DISABLED


def button_start():
    ''' a function for button "Start" which starts a game when all is settled up '''
    global player1_ships, player2_ships
    global already_clicked_player1, already_clicked_player2
    global sum_len_player1_ships, sum_len_player2_ships
    global list_gen_coordinates_player1, list_gen_coordinates_player2, generate_fleet_button, reset_button, start_button
    global player1_turn
    global list_used

    already_clicked_player1 = np.array([[-1 for i in range(x + 1)] for j in range(y + 1)])
    already_clicked_player2 = np.array([[-1 for i in range(x + 1)] for j in range(y + 1)])

    if computer:
        player2_ships, sum_len_player2_ships, list_gen_coordinates_player2 = game_func.generate_player_ships(x, y)            # if playing against computer, then generate all needed for player 2
        checksum = 0
        for i in range(x):                                              # checking if array with player 1`s ships
            for j in range(y):                                          # has all ships needed for game
                if player1_ships[j][i] != 0:                            #
                    checksum += 1

        if checksum != 20:
            messagebox.showerror(title="Error", message="You deployed your fleet incorrectly!")
            return -1
        else:
            check = 0
            for i in range(10):                                          # checking if array with player 1`s ships
                for j in range(10):                                      # is not empty
                    if player1_ships[j][i] > 0:                          #
                        check += 1
                        break
            if check > 0:
                pass
            else:
                list_gen_coordinates_player1 = [(0, 0, 0) for _ in range(10)]                       # begin of manually ship deployment,
                list_used = np.array([0 for _ in range(10)])                                        # checks if check that all ships meet the requirements,
                list_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]                                         #  no corners or sides are in contact
                num = 0
                for i in range(10):
                    for j in range(10):
                        if player1_ships[j][i] == -1:
                            if player1_ships[j + 1][i] == -1:
                                horizont_vertical = 2
                                column = 0
                                for step in range(0, 4):
                                    if player1_ships[j + step][i] == -1:
                                        column += 1
                                    else:
                                        break

                                for a in range(0, 10):
                                    if list_ships[a] == column and list_used[a] == 0:
                                        list_used[a] = 1
                                        num = a + 1

                                        for step in range(column):
                                            player1_ships[j + step][i] = num
                                        break
                                    else:
                                        print("Error: More ships then needed/incorrect required number of ships for each type")
                            else:
                                horizont_vertical = 1
                                row = 0
                                for step in range(0, 4):
                                    if player1_ships[j][i + step] == -1:
                                        row += 1
                                    else:
                                        break

                                for a in range(0, 10):
                                    if list_ships[a] == row and list_used[a] == 0:
                                        list_used[a] = 1
                                        num = a + 1

                                        for step in range(row):
                                            player1_ships[j][i + step] = num
                                        break
                                    else:
                                        print("Error: More ships then needed/incorrect required number of ships for each type")
                            list_gen_coordinates_player1[num - 1] = (horizont_vertical, j, i)
                print("list_gen:", list_gen_coordinates_player1)
                print("list_used:", list_used)
                print(player1_ships)
                if not list_used.all():
                    messagebox.showerror(title="Error",
                                         message="More ships then needed/incorrect required number of ships for each type!")
                    return -1
                else:
                    for index in range(10):
                        data = list_gen_coordinates_player1[index]
                        length = list_ships[index] - 1
                        vector, begin_y, begin_x = data

                        check_near_ships = 0
                        if vector == 1:
                            check_near_ships = player1_ships[begin_y - 1][begin_x - 1] + \
                                               player1_ships[begin_y + 1][begin_x - 1] + \
                                               player1_ships[begin_y - 1][begin_x] + \
                                               player1_ships[begin_y + 1][begin_x]

                            for j in range(1, length):
                                check_near_ships += player1_ships[begin_y - 1][begin_x + 1 + j] + \
                                                    player1_ships[begin_y + 1][begin_x + 1 + j]
                        if vector == 2:
                            check_near_ships = player1_ships[begin_y - 1][begin_x - 1] + \
                                               player1_ships[begin_y - 1][begin_x + 1] + \
                                               player1_ships[begin_y][begin_x - 1] + \
                                               player1_ships[begin_y][begin_x + 1]

                            for i in range(1, length):
                                check_near_ships += player1_ships[begin_y + 1 + i][begin_x - 1] + \
                                                    player1_ships[begin_y + 1 + i][begin_x + 1]

                        if check_near_ships != 0:
                            messagebox.showerror(title="Error", message="Can`t deploy ships near other ships")
                            return -1

        canvas.unbind_all("<Button-3>")                            # unbind RMB for manual ship deployment

        player1_turn = random.choice([True, False])                # randoming first turn
        game_func.mark_turn(player1_turn, t0, t1, t3)

        generate_fleet_button["state"] = DISABLED
        reset_button["state"] = ACTIVE
        start_button["state"] = DISABLED

        if not player1_turn and computer:
            computer_turn()

    else:
        player1_ships, sum_len_player1_ships, list_gen_coordinates_player1 = game_func.generate_player_ships(x, y)        # if we`re playing against other player,
        player2_ships, sum_len_player2_ships, list_gen_coordinates_player2 = game_func.generate_player_ships(x, y)        # all will generate automatically
        player1_turn = random.choice([True, False])
        game_func.mark_turn(player1_turn, t0, t1, t3)
        generate_fleet_button["state"] = DISABLED
        reset_button["state"] = ACTIVE
        start_button["state"] = DISABLED


def generate_random_fleet():
    ''' a function to button "Generate random fleet" which calls function generate_player_ships for player 1 in "player vs computer" mode'''
    global player1_ships, list_used
    global sum_len_player1_ships, list_gen_coordinates_player1
    button_reset(computer)

    player1_ships, sum_len_player1_ships, list_gen_coordinates_player1 = game_func.generate_player_ships(x, y)
    list_used = np.array([1 for _ in range(10)])
    button_show_player_ships(player1_ships, already_clicked_player1)


main_menu = Menu(window)
window.config(menu=main_menu)

game_menu = Menu(main_menu, tearoff=0)                                                          # adding menu bar

game_menu.add_command(label='New game vs Computer', command=lambda: button_reset(True))
game_menu.add_command(label='New game vs Player', command=lambda: button_reset(False))
game_menu.add_separator()
game_menu.add_command(label='Exit', command=on_closing)

debug_menu = Menu(main_menu, tearoff=0)                                                         # adding menu for debugging

debug_menu.add_command(label='Show Player 1`s fleet', command=lambda: button_show_player_ships(player1_ships, already_clicked_player1, color='light sky blue'))
debug_menu.add_command(label='Show Player 2`s fleet',
                       command=lambda: button_show_player_ships(player2_ships, already_clicked_player2, size_canvas_x + menu_x, color='light coral'))

main_menu.add_cascade(label="Game", menu=game_menu)
main_menu.add_cascade(label="Debug Menu", menu=debug_menu)

start_button = Button(window, text="Start game", command=button_start)
start_button.place(x=size_canvas_x + (step_x * 2) - start_button.winfo_reqwidth() // 2, y=20)

reset_button = Button(window, text="Reset", command=lambda: button_reset(computer))
reset_button.place(x=size_canvas_x + (step_x * 2) - reset_button.winfo_reqwidth() // 2, y=70)

if not computer:
    reset_button["state"] = DISABLED

generate_fleet_button = Button(window, text="Generate random fleet", command=generate_random_fleet)
generate_fleet_button.place(x=size_canvas_x + (step_x * 2) - generate_fleet_button.winfo_reqwidth() // 2, y=110)
generate_fleet_button["state"] = DISABLED

messagebox.showinfo(title="Welcome to Battleship!", message='Welcome to Battleship!\n\nThis game has two modes: "against the player" and "against the computer". \
Right now you are in two-player mode, to switch between modes, use the Game menu. \n\nIn two-player mode the fleet is randomly generated \
for both players, and in up against the computer you will also be able to manually place ships. To place a ship, \
right-click on the desired cell. \n\nEnjoy! :)')


def draw_point(player_ships, draw_x, draw_y, offset_x=0):
    ''' a function to draw a shape on canvas depending what is happened in game'''

    if computer:
        if np.array_equal(player_ships, player1_ships):
            color_miss = "red"
            color_hit = "light sky blue"
        else:
            color_miss = "blue"
            color_hit = "red"
        if 0 <= draw_x <= 9 and 0 <= draw_y <= 9:
            if player_ships[draw_y][draw_x] == 0:

                id1 = canvas.create_oval(offset_x + draw_x * step_x + step_x // 3, draw_y * step_y + step_y // 3,
                                         offset_x + draw_x * step_x + step_x - step_x // 3,
                                         draw_y * step_y + step_y - step_y // 3,
                                         fill=color_miss)

                list_ids.append(id1)

            else:
                id2 = canvas.create_rectangle(offset_x + draw_x * step_x, draw_y * step_y,
                                              offset_x + draw_x * step_x + step_x, draw_y * step_y + step_y,
                                              fill=color_hit)
                list_ids.append(id2)
        else:
            pass
    else:
        if np.array_equal(player_ships, player1_ships):
            color_miss = "red"
            color_hit = "blue"
        else:
            color_miss = "blue"
            color_hit = "red"
        if 0 <= draw_x <= 9 and 0 <= draw_y <= 9:
            if player_ships[draw_y][draw_x] == 0:

                id1 = canvas.create_oval(offset_x + draw_x * step_x + step_x // 3, draw_y * step_y + step_y // 3,
                                         offset_x + draw_x * step_x + step_x - step_x // 3,
                                         draw_y * step_y + step_y - step_y // 3,
                                         fill=color_miss)
                list_ids.append(id1)
            else:
                id2 = canvas.create_rectangle(offset_x + draw_x * step_x, draw_y * step_y,
                                              offset_x + draw_x * step_x + step_x, draw_y * step_y + step_y,
                                              fill=color_hit)
                list_ids.append(id2)
        else:
            pass


def check_ship(player_ships, already_clicked_player, val):                          # a function to check if ship has been destroyed
    quantity = 0
    for i in range(0, x):
        for j in range(0, y):
            if player_ships[j][i] == val and already_clicked_player[j][i] == -1:
                quantity += 1
    if quantity > 1:
        return False
    else:
        return True


def mark_destroyed(val, already_clicked_player, player_ships, list_gen_coordinates_player, _type, offset_x=0):   # a function to mark all surrounding cells
    ships_length = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]                                                                # of destroyed ship as "misses"
    length = ships_length[val - 1]
    horizontal_or_vertical, begin_x, begin_y = list_gen_coordinates_player[val - 1]
    print(horizontal_or_vertical, begin_x, begin_y)
    if horizontal_or_vertical == 2:

        already_clicked_player[begin_x - 1][begin_y - 1] = _type
        draw_point(player_ships, begin_y - 1, begin_x - 1, offset_x)

        already_clicked_player[begin_x - 1][begin_y] = _type
        draw_point(player_ships, begin_y, begin_x - 1, offset_x)

        already_clicked_player[begin_x - 1][begin_y + 1] = _type
        draw_point(player_ships, begin_y + 1, begin_x - 1, offset_x)

        already_clicked_player[begin_x][begin_y - 1] = _type
        draw_point(player_ships, begin_y - 1, begin_x, offset_x)

        already_clicked_player[begin_x][begin_y] = _type
        draw_point(player_ships, begin_y, begin_x, offset_x)

        already_clicked_player[begin_x][begin_y + 1] = _type
        draw_point(player_ships, begin_y + 1, begin_x, offset_x)

        for j in range(length):
            already_clicked_player[begin_x + 1 + j][begin_y - 1] = _type
            draw_point(player_ships, begin_y - 1, begin_x + 1 + j, offset_x)

            already_clicked_player[begin_x + 1 + j][begin_y] = _type
            draw_point(player_ships, begin_y, begin_x + 1 + j, offset_x)

            already_clicked_player[begin_x + 1 + j][begin_y + 1] = _type
            draw_point(player_ships, begin_y + 1, begin_x + 1 + j, offset_x)

    if horizontal_or_vertical == 1:

        already_clicked_player[begin_x - 1][begin_y - 1] = _type
        draw_point(player_ships, begin_y - 1, begin_x - 1, offset_x)

        already_clicked_player[begin_x][begin_y - 1] = _type
        draw_point(player_ships, begin_y - 1, begin_x, offset_x)

        already_clicked_player[begin_x + 1][begin_y - 1] = _type
        draw_point(player_ships, begin_y - 1, begin_x + 1, offset_x)

        already_clicked_player[begin_x - 1][begin_y] = _type
        draw_point(player_ships, begin_y, begin_x - 1, offset_x)

        already_clicked_player[begin_x][begin_y] = _type
        draw_point(player_ships, begin_y, begin_x, offset_x)

        already_clicked_player[begin_x + 1][begin_y] = _type
        draw_point(player_ships, begin_y, begin_x + 1, offset_x)

        for i in range(length):
            already_clicked_player[begin_x - 1][begin_y + 1 + i] = _type
            draw_point(player_ships, begin_y + 1 + i, begin_x - 1, offset_x)

            already_clicked_player[begin_x][begin_y + 1 + i] = _type
            draw_point(player_ships, begin_y + 1 + i, begin_x, offset_x)

            already_clicked_player[begin_x + 1][begin_y + 1 + i] = _type
            draw_point(player_ships, begin_y + 1 + i, begin_x + 1, offset_x)


def computer_turn():
    global already_clicked_player1, already_clicked_player2, computer
    global sum_shot_down_player1_ships, sum_len_player1_ships
    global player1_turn
    window.update()
    wait = random.randrange(1, 2)

    time.sleep(wait)
    game_coord_x = random.randint(0, x - 1)
    game_coord_y = random.randint(0, y - 1)

    while not already_clicked_player1[game_coord_y][game_coord_x] == -1:
        game_coord_x = random.randint(0, x - 1)
        game_coord_y = random.randint(0, y - 1)

    player1_turn = not player1_turn

    if player1_ships[game_coord_y][game_coord_x] > 0:
        val = player1_ships[game_coord_y][game_coord_x]

        if check_ship(player1_ships, already_clicked_player1, val):
            mark_destroyed(val, already_clicked_player1, player1_ships, list_gen_coordinates_player1, _type=1)
            destroyed = "Our ship has been \n    destroyed..."
            t2_result.configure(text=destroyed, fg='red')
        else:
            hit = "We've been hit.\n Buckle up!"
            t2_result.configure(text=hit, fg='red')

        sum_shot_down_player1_ships += 1
        player1_turn = not player1_turn
    else:
        missed = "Computer missed!"
        t2_result.configure(text=missed, fg='red')
        game_func.mark_turn(player1_turn, t0, t1, t3)

    already_clicked_player1[game_coord_y][game_coord_x] = 5
    draw_point(player1_ships, game_coord_x, game_coord_y)

    if game_func.check_winner(sum_shot_down_player1_ships, sum_len_player1_ships):
        winner = "Computer wins!"
        winner_add = "The entire Player 1 fleet was sunk..."
        print(winner, winner_add)

        already_clicked_player1 = np.array([[10 for i in range(x + 1)] for j in range(y + 1)])
        already_clicked_player2 = np.array([[10 for i in range(x + 1)] for j in range(y + 1)])



        t2_result.destroy()
        t3.destroy()

        id5 = canvas.create_rectangle(step_x * 3, step_y * 3,
                                      size_canvas_x + menu_x + size_canvas_x - step_x * 3,
                                      size_canvas_y - step_y, fill="yellow")
        list_ids.append(id5)
        id6 = canvas.create_rectangle(step_x * 3 + step_x // 2, step_y * 3 + step_y // 2,
                                      size_canvas_x + menu_x + size_canvas_x - step_x * 3 - step_x // 2,
                                      size_canvas_y - step_y - step_y // 2, fill="white")
        list_ids.append(id6)
        id7 = canvas.create_text(step_x * 12, step_y * 5, text=winner, font=("Arial", 50), justify=CENTER)
        id8 = canvas.create_text(step_x * 12, step_y * 7, text=winner_add, font=("Arial", 25), justify=CENTER)
        list_ids.append(id7)
        list_ids.append(id8)

    if not player1_turn:
        computer_turn()


def draw_point_deploying(draw_x, draw_y, color="blue"):                         # a function to draw on canvas while manually deploying ships
    global list_deploying

    id1 = canvas.create_rectangle(draw_x * step_x, draw_y * step_y,
                                  draw_x * step_x + step_x,
                                  draw_y * step_y + step_y,
                                  fill=color)

    list_deploying.append(id1)


def place_ships(event):                                                         # a binding function for RMB to draw ships on canvas
    _type = 3  # RMB

    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()

    game_coord_x = mouse_x // step_x
    game_coord_y = mouse_y // step_y

    print(f"Coordinates: {game_coord_y}:{game_coord_x}, click type: {_type}")

    if 0 <= game_coord_x < x and 0 <= game_coord_y < y:
        if player1_ships[game_coord_y][game_coord_x] == -1:
            player1_ships[game_coord_y][game_coord_x] = 0
            draw_point_deploying(game_coord_x, game_coord_y, color="white")
        else:
            player1_ships[game_coord_y][game_coord_x] = -1
            draw_point_deploying(game_coord_x, game_coord_y)


def add_to_all(event):                                                          # a binding function for LMB to shot in game
    global sum_shot_down_player1_ships, sum_shot_down_player2_ships
    global already_clicked_player1, already_clicked_player2
    global player1_turn
    global t2_result

    _type = 0  # LMB

    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()

    game_coord_x = mouse_x // step_x
    game_coord_y = mouse_y // step_y

    print(f"Coordinates: {game_coord_y}:{game_coord_x}, click type: {_type}")

    if 0 <= game_coord_x < x and 0 <= game_coord_y < y and not player1_turn and not computer:
        if already_clicked_player1[game_coord_y][game_coord_x] == -1:
            player1_turn = not player1_turn

            if player1_ships[game_coord_y][game_coord_x] > 0:
                val = player1_ships[game_coord_y][game_coord_x]

                if check_ship(player1_ships, already_clicked_player1, val):
                    mark_destroyed(val, already_clicked_player1, player1_ships, list_gen_coordinates_player1, _type)
                    destroyed = "Ship destroyed!\nGood work!"
                    t2_result.configure(text=destroyed, fg='red')
                else:
                    hit = "  That`s a hit!\n Don`t stop!"
                    t2_result.configure(text=hit, fg='red')

                sum_shot_down_player1_ships += 1
                player1_turn = not player1_turn

            else:
                missed = "     Missed..."
                t2_result.configure(text=missed, fg='red')
                game_func.mark_turn(player1_turn, t0, t1, t3)

            already_clicked_player1[game_coord_y][game_coord_x] = _type
            draw_point(player1_ships, game_coord_x, game_coord_y)

            if game_func.check_winner(sum_shot_down_player1_ships, sum_len_player1_ships):
                winner = "Player 2 wins!"
                winner_add = "The entire Player 1 fleet was sunk..."
                print(winner, winner_add)

                already_clicked_player1 = np.array([[10 for i in range(x + 1)] for j in range(y + 1)])
                already_clicked_player2 = np.array([[10 for i in range(x + 1)] for j in range(y + 1)])

                t2_result.destroy()
                t3.destroy()

                id5 = canvas.create_rectangle(step_x * 3, step_y * 3,
                                              size_canvas_x + menu_x + size_canvas_x - step_x * 3,
                                              size_canvas_y - step_y, fill="yellow")
                list_ids.append(id5)
                id6 = canvas.create_rectangle(step_x * 3 + step_x // 2, step_y * 3 + step_y // 2,
                                              size_canvas_x + menu_x + size_canvas_x - step_x * 3 - step_x // 2,
                                              size_canvas_y - step_y - step_y // 2, fill="white")
                list_ids.append(id6)
                id7 = canvas.create_text(step_x * 12, step_y * 5, text=winner, font=("Arial", 50), justify=CENTER)
                id8 = canvas.create_text(step_x * 12, step_y * 7, text=winner_add, font=("Arial", 25), justify=CENTER)
                list_ids.append(id7)
                list_ids.append(id8)

    if x + delta_menu_x <= game_coord_x < x + x + delta_menu_x and 0 <= game_coord_y < y and player1_turn:
        if already_clicked_player2[game_coord_y][game_coord_x - x - delta_menu_x] == -1:
            player1_turn = not player1_turn

            if player2_ships[game_coord_y][game_coord_x - x - delta_menu_x] > 0:
                val = player2_ships[game_coord_y][game_coord_x - x - delta_menu_x]
                print(val)

                if check_ship(player2_ships, already_clicked_player2, val):
                    mark_destroyed(val, already_clicked_player2, player2_ships, list_gen_coordinates_player2, _type,
                                   offset_x=size_canvas_x + menu_x)
                    destroyed = "Ship destroyed!\nGood work!"
                    t2_result.configure(text=destroyed, fg='blue')
                else:
                    hit = "  That`s a hit!\n Don`t stop!"
                    t2_result.configure(text=hit, fg='blue')

                player1_turn = not player1_turn
                sum_shot_down_player2_ships += 1

            else:
                missed = "     Missed..."
                t2_result.configure(text=missed, fg='blue')

                game_func.mark_turn(player1_turn, t0, t1, t3)

            already_clicked_player2[game_coord_y][game_coord_x - x - delta_menu_x] = _type
            draw_point(player2_ships, game_coord_x - x - delta_menu_x, game_coord_y, size_canvas_x + menu_x)

            if not player1_turn and computer:
                computer_turn()

            if game_func.check_winner(sum_shot_down_player2_ships, sum_len_player2_ships):
                winner = "Player 1 wins!"
                winner_add = "The entire Player 2 fleet was sunk..."
                print(winner, winner_add)

                already_clicked_player1 = np.array([[10 for i in range(x + 1)] for j in range(y + 1)])
                already_clicked_player2 = np.array([[10 for i in range(x + 1)] for j in range(y + 1)])

                t2_result.destroy()
                t3.destroy()

                id5 = canvas.create_rectangle(step_x * 3, step_y * 3,
                                              size_canvas_x + menu_x + size_canvas_x - step_x * 3,
                                              size_canvas_y - step_y, fill="yellow")
                list_ids.append(id5)
                id6 = canvas.create_rectangle(step_x * 3 + step_x // 2, step_y * 3 + step_y // 2,
                                              size_canvas_x + menu_x + size_canvas_x - step_x * 3 - step_x // 2,
                                              size_canvas_y - step_y - step_y // 2, fill="white")
                list_ids.append(id6)
                id7 = canvas.create_text(step_x * 12, step_y * 5, text=winner, font=("Arial", 50), justify=CENTER)
                id8 = canvas.create_text(step_x * 12, step_y * 7, text=winner_add, font=("Arial", 25), justify=CENTER)
                list_ids.append(id7)
                list_ids.append(id8)


canvas.bind_all("<Button-1>", add_to_all)  # LMB

while app_running:                                                                              # analog for mainloop()
    if app_running:
        window.update_idletasks()
        window.update()

    time.sleep(0.005)