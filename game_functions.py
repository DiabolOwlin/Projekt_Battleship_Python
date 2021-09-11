from tkinter import *
from tkinter import messagebox
import numpy as np
import time
import random


def mark_turn(player1_turn, t0, t1, t3):  # marking the player which making a turn
    if player1_turn:
        t0.configure(bg="blue", fg="#f0f0f0")
        t1.configure(bg="#f0f0f0", fg="red")
        t3.configure(text="Player 1`s turn", fg="blue")
    else:
        t1.configure(bg="red", fg="#f0f0f0")
        t0.configure(bg="#f0f0f0", fg="blue")
        t3.configure(text="Player 2`s turn", fg="red")


def check_winner(sum_shot_down_player_ships, sum_len_player_ships):                     # a function to check if player are the winner or not
    win = False
    if sum_shot_down_player_ships == sum_len_player_ships:
        win = True
    return win


def generate_player_ships(x, y):                                                        # a generator of player`s ships
    ships_list = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    sum_len_all_ships = sum(ships_list)
    player_ships = np.array([[0 for i in range(x + 1)] for j in range(y + 1)])
    list_gen_coordinates = []
    sum_len_player_ships = 0
    num = 1

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
            if coord_x + length <= x:
                try:
                    check_near_ships = 0
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
                        list_gen_coordinates.append((horizont_vertical, coord_x, coord_y))
                        for j in range(length):
                            player_ships[coord_x][coord_y + j] = num

                        ships_list.remove(length)

                        sum_len_player_ships += length
                        num += 1

                except Exception:
                    pass

        if horizont_vertical == 2:
            if coord_y + length <= y:
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
                        list_gen_coordinates.append((horizont_vertical, coord_x, coord_y))
                        for i in range(length):
                            player_ships[coord_x + i][coord_y] = num

                        ships_list.remove(length)

                        sum_len_player_ships += length
                        num += 1

                except Exception:
                    pass

    return player_ships[0:-1, 0:-1], sum_len_player_ships, list_gen_coordinates