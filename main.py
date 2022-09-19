import os
import re
import sys
import tkinter as tk
from tkinter import *
from tkinter import colorchooser
import sqlite3
import pprint

import cv2
import numpy as np
from PIL import Image as PilImage, ImageTk

from constants import ButtonsWindow, SettingsCanvas, ElementsColorWindow, TitlesWindow, SizesWindow, \
    SettingsFontWindow, CommandsDb
from config import sheet_with_connectors, directory_for_photos

colors_db = sqlite3.connect('сolors.db')
cursor = colors_db.cursor()


class GoogleTable:

    def __init__(self, file_image, main_screen):
        self.file_image = file_image
        self.main_screen = main_screen

    def send_colors(self):

        cursor.execute(CommandsDb.COMMAND_SELECT_GRADIENT)
        gradient_colors = cursor.fetchall()

        cursor.execute(CommandsDb.COMMAND_SELECT_FIRST_COLOR)
        first_colors = cursor.fetchall()

        cursor.execute(CommandsDb.COMMAND_SELECT_SECOND_COLOR)
        second_colors = cursor.fetchall()

        cursor.execute(CommandsDb.COMMAND_SELECT_THIRD_COLOR)
        third_colors = cursor.fetchall()

        regular_expression_format = re.compile(r"\b\d+\b")

        gradient_colors_rgb_codes = regular_expression_format.findall(str(gradient_colors[-1]))
        first_gradient_color = ElementsColorWindow.HEX_ENCODING % (
            int(gradient_colors_rgb_codes[0]), int(gradient_colors_rgb_codes[1]), int(gradient_colors_rgb_codes[2]))

        gradient_colors_rgb_codes = regular_expression_format.findall(str(gradient_colors[-2]))
        second_gradient_color = ElementsColorWindow.HEX_ENCODING % (
            int(gradient_colors_rgb_codes[0]), int(gradient_colors_rgb_codes[1]), int(gradient_colors_rgb_codes[2]))

        first_color_rgb_codes = regular_expression_format.findall(str(first_colors[-1]))
        first_color = ElementsColorWindow.HEX_ENCODING % (
            int(first_color_rgb_codes[0]), int(first_color_rgb_codes[1]), int(first_color_rgb_codes[2]))

        second_color_rgb_codes = regular_expression_format.findall(str(second_colors[-1]))
        second_color = ElementsColorWindow.HEX_ENCODING % (
            int(second_color_rgb_codes[0]), int(second_color_rgb_codes[1]), int(second_color_rgb_codes[2]))

        third_color_rbg_codes = regular_expression_format.findall(str(third_colors[-1]))
        third_color = ElementsColorWindow.HEX_ENCODING % (
            int(third_color_rbg_codes[0]), int(third_color_rbg_codes[1]), int(third_color_rbg_codes[2]))

        column_with_images = sheet_with_connectors.col_values(9)
        name_image_file = str(self.file_image)
        name_image = name_image_file[7:]

        if name_image in column_with_images:
            index_photo = column_with_images.index(name_image)
            row = index_photo + 1

            sheet_with_connectors.update(f'J{row}', first_gradient_color)
            sheet_with_connectors.update(f'K{row}', second_gradient_color)
            sheet_with_connectors.update(f'L{row}', first_color)
            sheet_with_connectors.update(f'M{row}', second_color)
            sheet_with_connectors.update(f'N{row}', third_color)

        cursor.execute(CommandsDb.COMMAND_SELECT_GRADIENT)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_GRADIENT_COLOR, )
            colors_db.commit()

        cursor.execute(CommandsDb.COMMAND_SELECT_FIRST_COLOR)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_FIRST_COLOR, )
            colors_db.commit()

        cursor.execute(CommandsDb.COMMAND_SELECT_SECOND_COLOR)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_SECOND_COLOR, )
            colors_db.commit()

        cursor.execute(CommandsDb.COMMAND_SELECT_THIRD_COLOR)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_THIRD_COLOR, )
            colors_db.commit()

        self.main_screen.destroy()
        os.remove(self.file_image)
        delete_file = str(self.file_image)[7:]
        cursor.execute(CommandsDb.COMMAND_DELETED_IMAGE, (delete_file,))
        colors_db.commit()


class SortingImage:
    def __init__(self, listbox, main_screen):
        self.listbox = listbox
        self.main_screen = main_screen

    def sorting_photos(self):

        cursor.execute(CommandsDb.COMMAND_SELECT_SORTING_IMAGE)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_SORTING_IMAGE, )
            colors_db.commit()

        listbox_frame = self.listbox

        for result_sorting in listbox_frame.curselection():
            region = listbox_frame.get(result_sorting)

            if region == ButtonsWindow.SORTING_REGION[0]:
                order_numbers_ua = sheet_with_connectors.col_values(16)
                name_file_image = sheet_with_connectors.col_values(9)
                first_colors_for_check = sheet_with_connectors.col_values(10)
                second_colors_for_check = sheet_with_connectors.col_values(11)
                third_colors_for_check = sheet_with_connectors.col_values(12)
                fourth_colors_for_check = sheet_with_connectors.col_values(13)
                fivth_colors_for_check = sheet_with_connectors.col_values(14)

                order_numbers_ua.pop(0)
                name_file_image.pop(0)
                first_colors_for_check.pop(0)
                second_colors_for_check.pop(0)
                third_colors_for_check.pop(0)
                fourth_colors_for_check.pop(0)
                fivth_colors_for_check.pop(0)

                new_type_order_numbers_ua = list(map(int, order_numbers_ua))

                sorted_images = {}

                for number, name_file, color1, color2, color3, color4, color5 in zip(new_type_order_numbers_ua,
                                                                                     name_file_image,
                                                                                     first_colors_for_check,
                                                                                     second_colors_for_check,
                                                                                     third_colors_for_check,
                                                                                     fourth_colors_for_check,
                                                                                     fivth_colors_for_check):
                    if color1 == '' or color2 == '' or color3 == '' or color4 == '' or color5 == '':
                        sorted_images.update({number: name_file})

                cursor.executemany(CommandsDb.COMMAND_INSERT_SORTING_IMAGE, list(sorted_images.items()), )
                colors_db.commit()

                tk.Label(self.main_screen,
                         text=TitlesWindow.TEXT_AFTER_SORTING,
                         font=SettingsFontWindow.TITLE_FONT).grid(row=4, column=1, padx=2, pady=2)

            if region == ButtonsWindow.SORTING_REGION[1]:
                order_numbers_ua = sheet_with_connectors.col_values(17)
                name_file_image = sheet_with_connectors.col_values(9)
                first_colors_for_check = sheet_with_connectors.col_values(10)
                second_colors_for_check = sheet_with_connectors.col_values(11)
                third_colors_for_check = sheet_with_connectors.col_values(12)
                fourth_colors_for_check = sheet_with_connectors.col_values(13)
                fivth_colors_for_check = sheet_with_connectors.col_values(14)

                order_numbers_ua.pop(0)
                name_file_image.pop(0)
                first_colors_for_check.pop(0)
                second_colors_for_check.pop(0)
                third_colors_for_check.pop(0)
                fourth_colors_for_check.pop(0)
                fivth_colors_for_check.pop(0)

                new_type_order_numbers_ua = list(map(int, order_numbers_ua))

                sorted_images = {}

                for number, name_file, color1, color2, color3, color4, color5 in zip(new_type_order_numbers_ua,
                                                                                     name_file_image,
                                                                                     first_colors_for_check,
                                                                                     second_colors_for_check,
                                                                                     third_colors_for_check,
                                                                                     fourth_colors_for_check,
                                                                                     fivth_colors_for_check):
                    if color1 == '' or color2 == '' or color3 == '' or color4 == '' or color5 == '':
                        sorted_images.update({number: name_file})

                cursor.executemany(CommandsDb.COMMAND_INSERT_SORTING_IMAGE, list(sorted_images.items()), )
                colors_db.commit()

                tk.Label(self.main_screen,
                         text=TitlesWindow.TEXT_AFTER_SORTING,
                         font=SettingsFontWindow.TITLE_FONT).grid(row=4, column=1, padx=2, pady=2)

            if region == ButtonsWindow.SORTING_REGION[2]:
                order_numbers_ua = sheet_with_connectors.col_values(18)
                name_file_image = sheet_with_connectors.col_values(9)
                first_colors_for_check = sheet_with_connectors.col_values(10)
                second_colors_for_check = sheet_with_connectors.col_values(11)
                third_colors_for_check = sheet_with_connectors.col_values(12)
                fourth_colors_for_check = sheet_with_connectors.col_values(13)
                fivth_colors_for_check = sheet_with_connectors.col_values(14)

                order_numbers_ua.pop(0)
                name_file_image.pop(0)
                first_colors_for_check.pop(0)
                second_colors_for_check.pop(0)
                third_colors_for_check.pop(0)
                fourth_colors_for_check.pop(0)
                fivth_colors_for_check.pop(0)

                new_type_order_numbers_ua = list(map(int, order_numbers_ua))

                sorted_images = {}

                for number, name_file, color1, color2, color3, color4, color5 in zip(new_type_order_numbers_ua,
                                                                                     name_file_image,
                                                                                     first_colors_for_check,
                                                                                     second_colors_for_check,
                                                                                     third_colors_for_check,
                                                                                     fourth_colors_for_check,
                                                                                     fivth_colors_for_check):
                    if color1 == '' or color2 == '' or color3 == '' or color4 == '' or color5 == '':
                        sorted_images.update({number: name_file})

                cursor.executemany(CommandsDb.COMMAND_INSERT_SORTING_IMAGE, list(sorted_images.items()), )
                colors_db.commit()

                tk.Label(self.main_screen,
                         text=TitlesWindow.TEXT_AFTER_SORTING,
                         font=SettingsFontWindow.TITLE_FONT).grid(row=4, column=1, padx=2, pady=2)

            if region == ButtonsWindow.SORTING_REGION[3]:
                order_numbers_ua = sheet_with_connectors.col_values(19)
                name_file_image = sheet_with_connectors.col_values(9)
                first_colors_for_check = sheet_with_connectors.col_values(10)
                second_colors_for_check = sheet_with_connectors.col_values(11)
                third_colors_for_check = sheet_with_connectors.col_values(12)
                fourth_colors_for_check = sheet_with_connectors.col_values(13)
                fivth_colors_for_check = sheet_with_connectors.col_values(14)

                order_numbers_ua.pop(0)
                name_file_image.pop(0)
                first_colors_for_check.pop(0)
                second_colors_for_check.pop(0)
                third_colors_for_check.pop(0)
                fourth_colors_for_check.pop(0)
                fivth_colors_for_check.pop(0)

                new_type_order_numbers_ua = list(map(int, order_numbers_ua))

                sorted_images = {}

                for number, name_file, color1, color2, color3, color4, color5 in zip(new_type_order_numbers_ua,
                                                                                     name_file_image,
                                                                                     first_colors_for_check,
                                                                                     second_colors_for_check,
                                                                                     third_colors_for_check,
                                                                                     fourth_colors_for_check,
                                                                                     fivth_colors_for_check):
                    if color1 == '' or color2 == '' or color3 == '' or color4 == '' or color5 == '':
                        sorted_images.update({number: name_file})

                cursor.executemany(CommandsDb.COMMAND_INSERT_SORTING_IMAGE, list(sorted_images.items()), )
                colors_db.commit()

                tk.Label(self.main_screen,
                         text=TitlesWindow.TEXT_AFTER_SORTING,
                         font=SettingsFontWindow.TITLE_FONT).grid(row=4, column=1, padx=2, pady=2)


class ListBox:
    def __init__(self, main_screen):
        self.main_screen = main_screen

    def get_listbox(self):
        listbox = Listbox(self.main_screen, width=18, height=4, selectmode=MULTIPLE)

        listbox.insert(1, ButtonsWindow.SORTING_REGION[0])
        listbox.insert(2, ButtonsWindow.SORTING_REGION[1])
        listbox.insert(3, ButtonsWindow.SORTING_REGION[2])
        listbox.insert(4, ButtonsWindow.SORTING_REGION[3])

        listbox.grid(row=3, column=1, padx=1, pady=1)

        return listbox


class ColorsImage:

    def __init__(self, image):
        self.image = image

    def get_image_colors(self):

        title_image = cv2.imread(str(self.image))

        matrix_image = cv2.resize(title_image, (title_image.shape[1] // 12, title_image.shape[0] // 12))

        height_image = np.size(matrix_image, 0)
        width_image = np.size(matrix_image, 1)

        colors_input = []
        colors_output = []

        for first_cordinate in range(1, width_image):
            for second_cordinate in range(1, height_image):
                (b, g, r) = matrix_image[second_cordinate, first_cordinate]
                color_format = str((r, g, b))
                colors_input.append(color_format)

        for color in colors_input:
            if color not in colors_output:
                colors_output.append(color)

        return colors_output


class CreateGradientFrame(tk.Frame):
    def __init__(self, parent, color_first, color_second):
        tk.Frame.__init__(self, parent)
        frame = GradientFrame(self, color_first, color_second, borderwidth=1, relief="sunken")
        frame.grid(row=0, column=0)


class GradientFrame(tk.Canvas):

    def __init__(self, parent, color1, color2, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind(SettingsCanvas.CONFIG, self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete(SettingsCanvas.TAG_FRAME)
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2 - r1) / limit
        g_ratio = float(g2 - g1) / limit
        b_ratio = float(b2 - b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = SettingsCanvas.CANVAS_CONSTANT % (nr, ng, nb)
            self.create_line(i, 0, i, height, tags=(SettingsCanvas.TAG_FRAME,), fill=color)
        self.lower(SettingsCanvas.TAG_FRAME)


class ButtonsMainScreen:

    def __init__(self, colors, main_screen, file_image):
        self.colors = colors
        self.main_screen = main_screen
        self.file_image = file_image

    def get_colored_buttons(self, frame):

        for color in self.colors:
            index = self.colors.index(color)
            regular_expression_format = re.compile(r"\b\d+\b")
            list_rgb_codes = regular_expression_format.findall(self.colors[index])
            hex_color = ElementsColorWindow.HEX_ENCODING % (
                int(list_rgb_codes[0]), int(list_rgb_codes[1]), int(list_rgb_codes[2]))

            tk.Button(frame,
                      text=f'{hex_color}',
                      fg=SettingsFontWindow.FIRST_FONT_COLOR,
                      bg=hex_color,
                      width=8,
                      height=1,
                      command=lambda color_image=color: self.build_gradient_color_frame(color_image)).grid(row=index,
                                                                                                           pady=2,
                                                                                                           padx=2,
                                                                                                           column=1)
        for color in self.colors:
            index = self.colors.index(color)
            regular_expression_format = re.compile(r"\b\d+\b")
            list_rgb_codes = regular_expression_format.findall(self.colors[index])

            hex_color = ElementsColorWindow.HEX_ENCODING % (
                int(list_rgb_codes[0]), int(list_rgb_codes[1]), int(list_rgb_codes[2]))
            tk.Button(frame,
                      text=f'{hex_color}',
                      fg=SettingsFontWindow.FIRST_FONT_COLOR,
                      bg=hex_color,
                      width=8,
                      height=1,
                      command=lambda color_image=color: self.build_first_color_frame(color_image)).grid(row=index,
                                                                                                        pady=2,
                                                                                                        padx=2,
                                                                                                        column=2)
        for color in self.colors:
            index = self.colors.index(color)
            regular_expression_format = re.compile(r"\b\d+\b")
            list_rgb_codes = regular_expression_format.findall(self.colors[index])

            hex_color = ElementsColorWindow.HEX_ENCODING % (
                int(list_rgb_codes[0]), int(list_rgb_codes[1]), int(list_rgb_codes[2]))
            tk.Button(frame,
                      text=f'{hex_color}',
                      fg=SettingsFontWindow.FIRST_FONT_COLOR,
                      bg=hex_color,
                      width=8,
                      height=1,
                      command=lambda color_image=color: self.build_second_color_frame(color_image)).grid(row=index,
                                                                                                         pady=2,
                                                                                                         padx=2,
                                                                                                         column=3)
        for color in self.colors:
            index = self.colors.index(color)
            regular_expression_format = re.compile(r"\b\d+\b")
            list_rgb_codes = regular_expression_format.findall(self.colors[index])

            hex_color = ElementsColorWindow.HEX_ENCODING % (
                int(list_rgb_codes[0]), int(list_rgb_codes[1]), int(list_rgb_codes[2]))
            tk.Button(frame,
                      text=f'{hex_color}',
                      fg=SettingsFontWindow.FIRST_FONT_COLOR,
                      bg=hex_color,
                      width=8,
                      height=1,
                      command=lambda color_image=color: self.build_third_color_frame(color_image)).grid(row=index,
                                                                                                        pady=2,
                                                                                                        padx=2,
                                                                                                        column=4)

    def get_control_buttons(self):

        google_table = GoogleTable(self.file_image, self.main_screen)

        button_send = tk.Button(self.main_screen,
                                text=ButtonsWindow.BUTTON_SEND,
                                command=google_table.send_colors,
                                width=33,
                                fg=SettingsFontWindow.SECOND_FONT_COLOR,
                                font=SettingsFontWindow.BUTTONS_FONT,
                                bg=ElementsColorWindow.BACKGROUND_COLOR_BUTTON,
                                height=1)

        button_close = tk.Button(self.main_screen,
                                 text=ButtonsWindow.BUTTON_CLOSE,
                                 command=self.close_main_window,
                                 width=18,
                                 fg=SettingsFontWindow.SECOND_FONT_COLOR,
                                 font=SettingsFontWindow.BUTTONS_FONT,
                                 bg=ElementsColorWindow.BACKGROUND_COLOR_BUTTON,
                                 height=1)

        button_miss = tk.Button(self.main_screen,
                                text=ButtonsWindow.BUTTON_MISS,
                                command=self.switch_image,
                                width=18,
                                fg=SettingsFontWindow.SECOND_FONT_COLOR,
                                font=SettingsFontWindow.BUTTONS_FONT,
                                bg=ElementsColorWindow.BACKGROUND_COLOR_BUTTON,
                                height=1)

        buttons = {
            'simple_buttons': [button_send, button_close, button_miss],
        }

        return buttons

    def build_gradient_color_frame(self, color):

        cursor.execute(CommandsDb.COMMAND_INSERT_GRADIENT, (str(color),))
        colors_db.commit()
        cursor.execute(CommandsDb.COMMAND_SELECT_GRADIENT)
        colors = cursor.fetchall()

        if len(colors) >= 2:
            regular_expression_format = re.compile(r"\b\d+\b")
            first_list_rgb_codes = regular_expression_format.findall(str(colors[-1]))
            second_list_rgb_codes = regular_expression_format.findall(str(colors[-2]))

            first_hex_color = ElementsColorWindow.HEX_ENCODING % (
                int(first_list_rgb_codes[0]), int(first_list_rgb_codes[1]), int(first_list_rgb_codes[2]))

            second_hex_color = ElementsColorWindow.HEX_ENCODING % (
                int(second_list_rgb_codes[0]), int(second_list_rgb_codes[1]), int(second_list_rgb_codes[2]))

            CreateGradientFrame(self.main_screen, first_hex_color, second_hex_color).grid(row=0, column=4)

            tk.Button(self.main_screen,
                      text=ButtonsWindow.CHANGE_BUTTON_COLOR_GRADIENT,
                      command=self.change_color_gradient_table,
                      width=33,
                      fg=SettingsFontWindow.SECOND_FONT_COLOR,
                      font=SettingsFontWindow.BUTTONS_FONT,
                      bg=ElementsColorWindow.BACKGROUND_COLOR_BUTTON,
                      height=1).grid(row=1, column=4, padx=2, pady=2)

    def build_first_color_frame(self, color):

        cursor.execute(CommandsDb.COMMAND_INSERT_FIRST_COLOR, (str(color),))
        colors_db.commit()
        cursor.execute(CommandsDb.COMMAND_SELECT_FIRST_COLOR)
        colors = cursor.fetchall()

        regular_expression_format = re.compile(r"\b\d+\b")
        list_rgb_codes = regular_expression_format.findall(str(colors[-1]))

        hex_color = ElementsColorWindow.HEX_ENCODING % (
            int(list_rgb_codes[0]), int(list_rgb_codes[1]), int(list_rgb_codes[2]))

        rectangle = tk.Canvas(self.main_screen, width=300, height=80, bg=hex_color)
        rectangle.grid(row=3, column=3, padx=2, pady=2)

        tk.Button(self.main_screen,
                  text=ButtonsWindow.CHANGE_BUTTON_FIRST_COLOR,
                  command=self.change_first_color_table,
                  width=33,
                  fg=SettingsFontWindow.SECOND_FONT_COLOR,
                  font=SettingsFontWindow.BUTTONS_FONT,
                  bg=ElementsColorWindow.BACKGROUND_COLOR_BUTTON,
                  height=1).grid(row=2, column=3, padx=2, pady=2)

    def build_second_color_frame(self, color):

        cursor.execute(CommandsDb.COMMAND_INSERT_SECOND_COLOR, (str(color),))
        colors_db.commit()
        cursor.execute(CommandsDb.COMMAND_SELECT_SECOND_COLOR)
        colors = cursor.fetchall()

        regular_expression_format = re.compile(r"\b\d+\b")
        list_rgb_codes = regular_expression_format.findall(str(colors[-1]))

        hex_color = ElementsColorWindow.HEX_ENCODING % (
            int(list_rgb_codes[0]), int(list_rgb_codes[1]), int(list_rgb_codes[2]))

        rectangle = tk.Canvas(self.main_screen, width=300, height=80, bg=hex_color)
        rectangle.grid(row=3, column=4, padx=2, pady=2)

        tk.Button(self.main_screen,
                  text=ButtonsWindow.CHANGE_BUTTON_SECOND_COLOR,
                  command=self.change_second_color_table,
                  width=33,
                  fg=SettingsFontWindow.SECOND_FONT_COLOR,
                  font=SettingsFontWindow.BUTTONS_FONT,
                  bg=ElementsColorWindow.BACKGROUND_COLOR_BUTTON,
                  height=1).grid(row=2, column=4, padx=2, pady=2)

    def build_third_color_frame(self, color):

        cursor.execute(CommandsDb.COMMAND_INSERT_THIRD_COLOR, (str(color),))
        colors_db.commit()
        cursor.execute(CommandsDb.COMMAND_SELECT_THIRD_COLOR)
        colors = cursor.fetchall()

        regular_expression_format = re.compile(r"\b\d+\b")
        list_rgb_codes = regular_expression_format.findall(str(colors[-1]))

        hex_color = ElementsColorWindow.HEX_ENCODING % (
            int(list_rgb_codes[0]), int(list_rgb_codes[1]), int(list_rgb_codes[2]))

        rectangle = tk.Canvas(self.main_screen, width=300, height=80, bg=hex_color)
        rectangle.grid(row=3, column=5, padx=2, pady=2)

        tk.Button(self.main_screen,
                  text=ButtonsWindow.CHANGE_BUTTON_THIRD_COLOR,
                  command=self.change_third_color_table,
                  width=33,
                  fg=SettingsFontWindow.SECOND_FONT_COLOR,
                  font=SettingsFontWindow.BUTTONS_FONT,
                  bg=ElementsColorWindow.BACKGROUND_COLOR_BUTTON,
                  height=1).grid(row=2, column=5, padx=2, pady=2)

    def change_color_gradient_table(self):

        cursor.execute(CommandsDb.COMMAND_SELECT_GRADIENT)
        colors = cursor.fetchall()

        regular_expression_format = re.compile(r"\b\d+\b")
        first_list_rgb_codes = regular_expression_format.findall(str(colors[-1]))

        hex_color = ElementsColorWindow.HEX_ENCODING % (int(first_list_rgb_codes[0]), int(first_list_rgb_codes[1]),
                                                        int(first_list_rgb_codes[2]))

        color = colorchooser.askcolor(hex_color)

        cursor.execute(CommandsDb.COMMAND_INSERT_GRADIENT, (str(color),))
        colors_db.commit()
        cursor.execute(CommandsDb.COMMAND_SELECT_GRADIENT)
        colors = cursor.fetchall()

        if len(colors) >= 2:
            regular_expression_format = re.compile(r"\b\d+\b")
            first_list_rgb_codes = regular_expression_format.findall(str(colors[-1]))
            second_list_rgb_codes = regular_expression_format.findall(str(colors[-2]))

            first_hex_color = ElementsColorWindow.HEX_ENCODING % (
                int(first_list_rgb_codes[0]), int(first_list_rgb_codes[1]), int(first_list_rgb_codes[2]))

            second_hex_color = ElementsColorWindow.HEX_ENCODING % (
                int(second_list_rgb_codes[0]), int(second_list_rgb_codes[1]), int(second_list_rgb_codes[2]))

            CreateGradientFrame(self.main_screen, first_hex_color, second_hex_color).grid(row=0, column=4)

    def change_first_color_table(self):

        cursor.execute(CommandsDb.COMMAND_SELECT_FIRST_COLOR)
        colors = cursor.fetchall()

        regular_expression_format = re.compile(r"\b\d+\b")

        first_list_rgb_codes = regular_expression_format.findall(str(colors[-1]))

        hex_color = ElementsColorWindow.HEX_ENCODING % (
            int(first_list_rgb_codes[0]), int(first_list_rgb_codes[1]), int(first_list_rgb_codes[2]))

        color = colorchooser.askcolor(hex_color)

        cursor.execute(CommandsDb.COMMAND_INSERT_FIRST_COLOR, (str(color),))
        colors_db.commit()
        cursor.execute(CommandsDb.COMMAND_SELECT_FIRST_COLOR)
        colors = cursor.fetchall()

        second_list_rgb_codes = regular_expression_format.findall(str(colors[-1]))

        hex_color = ElementsColorWindow.HEX_ENCODING % (
            int(second_list_rgb_codes[0]), int(second_list_rgb_codes[1]), int(second_list_rgb_codes[2]))

        rectangle = tk.Canvas(self.main_screen, width=300, height=80, bg=hex_color)
        rectangle.grid(row=3, column=3, padx=2, pady=2)

    def change_second_color_table(self):

        cursor.execute(CommandsDb.COMMAND_SELECT_SECOND_COLOR)
        colors = cursor.fetchall()

        regular_expression_format = re.compile(r"\b\d+\b")
        first_list_rgb_codes = regular_expression_format.findall(str(colors[-1]))

        hex_color = ElementsColorWindow.HEX_ENCODING % (
            int(first_list_rgb_codes[0]), int(first_list_rgb_codes[1]), int(first_list_rgb_codes[2]))

        color = colorchooser.askcolor(hex_color)

        cursor.execute(CommandsDb.COMMAND_INSERT_SECOND_COLOR, (str(color),))
        colors_db.commit()
        cursor.execute(CommandsDb.COMMAND_SELECT_SECOND_COLOR)
        colors = cursor.fetchall()

        second_list_rgb_codes = regular_expression_format.findall(str(colors[-1]))

        hex_color = ElementsColorWindow.HEX_ENCODING % (
            int(second_list_rgb_codes[0]), int(second_list_rgb_codes[1]), int(second_list_rgb_codes[2]))

        rectangle = tk.Canvas(self.main_screen, width=300, height=80, bg=hex_color)
        rectangle.grid(row=3, column=4, padx=2, pady=2)

    def change_third_color_table(self):

        cursor.execute(CommandsDb.COMMAND_SELECT_THIRD_COLOR)
        colors = cursor.fetchall()

        regular_expression_format = re.compile(r"\b\d+\b")
        first_list_rgb_codes = regular_expression_format.findall(str(colors[-1]))

        hex_color = ElementsColorWindow.HEX_ENCODING % (
            int(first_list_rgb_codes[0]), int(first_list_rgb_codes[1]), int(first_list_rgb_codes[2]))
        color = colorchooser.askcolor(hex_color)

        cursor.execute(CommandsDb.COMMAND_INSERT_THIRD_COLOR, (str(color),))
        colors_db.commit()
        cursor.execute(CommandsDb.COMMAND_SELECT_THIRD_COLOR)
        colors = cursor.fetchall()

        second_list_rgb_codes = regular_expression_format.findall(str(colors[-1]))

        hex_color = ElementsColorWindow.HEX_ENCODING % (
            int(second_list_rgb_codes[0]), int(second_list_rgb_codes[1]), int(second_list_rgb_codes[2]))

        rectangle = tk.Canvas(self.main_screen, width=300, height=80, bg=hex_color)
        rectangle.grid(row=3, column=5, padx=2, pady=2)

    @staticmethod
    def close_main_window():

        cursor.execute(CommandsDb.COMMAND_SELECT_GRADIENT)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_GRADIENT_COLOR, )
            colors_db.commit()

        cursor.execute(CommandsDb.COMMAND_SELECT_FIRST_COLOR)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_FIRST_COLOR, )
            colors_db.commit()

        cursor.execute(CommandsDb.COMMAND_SELECT_SECOND_COLOR)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_SECOND_COLOR, )
            colors_db.commit()

        cursor.execute(CommandsDb.COMMAND_SELECT_THIRD_COLOR)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_THIRD_COLOR, )
            colors_db.commit()

        colors_db.close()
        sys.exit()

    def switch_image(self):

        cursor.execute(CommandsDb.COMMAND_SELECT_GRADIENT)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_GRADIENT_COLOR, )
            colors_db.commit()

        cursor.execute(CommandsDb.COMMAND_SELECT_FIRST_COLOR)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_FIRST_COLOR, )
            colors_db.commit()

        cursor.execute(CommandsDb.COMMAND_SELECT_SECOND_COLOR)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_SECOND_COLOR, )
            colors_db.commit()

        cursor.execute(CommandsDb.COMMAND_SELECT_THIRD_COLOR)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_THIRD_COLOR, )
            colors_db.commit()

        self.main_screen.destroy()


class MainScreen:

    def __init__(self, image, colors):
        self.image = image
        self.colors = colors
        self.main_screen = Tk()

    def get_main_screen(self, inner_frame):
        main_screen = self.main_screen

        tk.Label(main_screen,
                 text=f"{TitlesWindow.TITLE_IMAGE}\n{str(self.image)[7:]}",
                 font=SettingsFontWindow.TITLE_FONT).grid(row=1, column=1, padx=2, pady=2)

        canvas = tk.Canvas(main_screen, height=120, width=120)
        image = PilImage.open(self.image)
        resize_image = image.resize((100, 100))
        photo = ImageTk.PhotoImage(resize_image)
        canvas.create_image(0, 0, anchor='nw', image=photo)
        canvas.grid(row=0, column=2)

        buttons = ButtonsMainScreen(self.colors, self.main_screen, self.image)

        buttons.get_colored_buttons(inner_frame)
        control_buttons = buttons.get_control_buttons()

        button_send = control_buttons['simple_buttons'][0]
        button_send.grid(row=1, column=3, padx=1, pady=1)

        button_close = control_buttons['simple_buttons'][1]
        button_close.grid(row=2, column=2, padx=1, pady=1)

        button_miss = control_buttons['simple_buttons'][2]
        button_miss.grid(row=1, column=2, padx=1, pady=1)

        listbox = ListBox(self.main_screen)
        input_listbox = SortingImage(listbox.get_listbox(), self.main_screen)
        sorting_image = input_listbox.sorting_photos

        button_sorting = Button(self.main_screen,
                                text=ButtonsWindow.BUTTON_SORT,
                                command=sorting_image,
                                width=18,
                                fg=SettingsFontWindow.SECOND_FONT_COLOR,
                                font=SettingsFontWindow.BUTTONS_FONT,
                                bg=ElementsColorWindow.BACKGROUND_COLOR_BUTTON,
                                height=1)
        button_sorting.grid(row=2, column=1, padx=1, pady=1)

        main_screen.state(SizesWindow.SIZE_MAIN_SCREEN)
        main_screen.mainloop()

    def get_inner_frame(self):
        canvas = tk.Canvas(self.main_screen, borderwidth=0,
                           background=ElementsColorWindow.BACKGROUND_COLOR_INNER_WINDOW,
                           width=290,
                           height=350)

        inner_frame = tk.Frame(canvas, background=ElementsColorWindow.BACKGROUND_COLOR_INNER_WINDOW)
        scroll_in_inner_frame = tk.Scrollbar(self.main_screen, orient=SettingsCanvas.ORIENT, command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_in_inner_frame.set)

        scroll_in_inner_frame.grid(row=0, column=0, sticky=NS)
        canvas.grid(row=0, column=1)
        canvas.create_window((3, 3), window=inner_frame, anchor="nw")

        inner_frame.bind(SettingsCanvas.CONFIG,
                         lambda event, canvas_frame=canvas: canvas_frame.configure(
                             scrollregion=canvas_frame.bbox("all")))

        return inner_frame


def main():
    cursor.execute(CommandsDb.COMMAND_SELECT_SORTING_IMAGE)
    images = cursor.fetchall()
    for element in images:
        file = f'{directory_for_photos}{element[1]}'

        settings_image = ColorsImage(file)
        mainscreen = MainScreen(file, settings_image.get_image_colors())
        mainscreen.get_main_screen(mainscreen.get_inner_frame())


if __name__ == '__main__':
    main()
