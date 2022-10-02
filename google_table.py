import os
import re
import tkinter as tk
import sqlite3

from config import sheet_with_connectors
from constants import ButtonsWindow, ElementsColorWindow, TitlesWindow, SettingsFontWindow, CommandsDb

colors_db = sqlite3.connect('сolors.db')
cursor = colors_db.cursor()


class GoogleTable:
    def __init__(self, file_image, main_screen):
        self.file_image = file_image
        self.main_screen = main_screen

    def send_colors_google_spreedsheet(self):
        """We convert the colors selected by the user to HEX format
        and send them to the Google table.
        """

        regular_expression_format = re.compile(r"\b\d+\b")

        cursor.execute(CommandsDb.COMMAND_SELECT_GRADIENT)
        gradient_colors = cursor.fetchall()
        print(gradient_colors)

        gradient_colors_rgb_codes = regular_expression_format.findall(str(gradient_colors[-1]))
        first_gradient_color = ElementsColorWindow.HEX_ENCODING % (
            int(gradient_colors_rgb_codes[0]), int(gradient_colors_rgb_codes[1]), int(gradient_colors_rgb_codes[2]))

        gradient_colors_rgb_codes = regular_expression_format.findall(str(gradient_colors[-2]))
        second_gradient_color = ElementsColorWindow.HEX_ENCODING % (
            int(gradient_colors_rgb_codes[0]), int(gradient_colors_rgb_codes[1]), int(gradient_colors_rgb_codes[2]))

        cursor.execute(CommandsDb.COMMAND_SELECT_FIRST_COLOR)
        first_colors = cursor.fetchall()

        first_color_rgb_codes = regular_expression_format.findall(str(first_colors[-1]))
        first_color = ElementsColorWindow.HEX_ENCODING % (
            int(first_color_rgb_codes[0]), int(first_color_rgb_codes[1]), int(first_color_rgb_codes[2]))

        cursor.execute(CommandsDb.COMMAND_SELECT_SECOND_COLOR)
        second_colors = cursor.fetchall()

        second_color_rgb_codes = regular_expression_format.findall(str(second_colors[-1]))
        second_color = ElementsColorWindow.HEX_ENCODING % (
            int(second_color_rgb_codes[0]), int(second_color_rgb_codes[1]), int(second_color_rgb_codes[2]))

        cursor.execute(CommandsDb.COMMAND_SELECT_THIRD_COLOR)
        third_colors = cursor.fetchall()

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

        for command_select, command_deleted in zip(CommandsDb.COMMANDS_SELECT, CommandsDb.COMMANDS_DELETED):
            cursor.execute(command_select)
            if cursor.fetchone() is not None:
                cursor.execute(command_deleted, )
                colors_db.commit()

        self.main_screen.destroy()
        os.remove(self.file_image)
        delete_file = str(self.file_image)[7:]
        cursor.execute(CommandsDb.COMMAND_DELETED_IMAGE, (delete_file,))
        colors_db.commit()


class RegionsGoogleTable:
    def __init__(self, listbox, main_screen):
        self.listbox = listbox
        self.main_screen = main_screen

    def sorting_image_by_regions(self):
        """We sort the photos by the regions presented in the table.
        1. we get an array of numbering and arrays of color values from certain columns of the table
        2. remove the headers from them
        3. check arrays with colors for empty values
        4 we write all the necessary images to the database for subsequent work
        """

        cursor.execute(CommandsDb.COMMAND_SELECT_SORTING_IMAGE)
        if cursor.fetchone() is not None:
            cursor.execute(CommandsDb.COMMAND_DELETED_SORTING_IMAGE, )
            colors_db.commit()

        for result_sorting in self.listbox.curselection():
            region = self.listbox.get(result_sorting)

            for number_column, sort_region in enumerate(ButtonsWindow.SORTING_REGION, start=16):
                if region == sort_region:

                    order_numbers = sheet_with_connectors.col_values(number_column)
                    name_file_image = sheet_with_connectors.col_values(9)
                    first_column_colors = sheet_with_connectors.col_values(10)
                    second_column_colors = sheet_with_connectors.col_values(11)
                    third_column_colors = sheet_with_connectors.col_values(12)
                    fourth_column_colors = sheet_with_connectors.col_values(13)
                    fifth_column_colors = sheet_with_connectors.col_values(14)

                    order_numbers.pop(0)
                    name_file_image.pop(0)
                    first_column_colors.pop(0)
                    second_column_colors.pop(0)
                    third_column_colors.pop(0)
                    fourth_column_colors.pop(0)
                    fifth_column_colors.pop(0)

                    new_type_order_numbers = list(map(int, order_numbers))

                    sorted_images = {}

                    for number, name_file, color1, color2, color3, color4, color5 in zip(new_type_order_numbers,
                                                                                         name_file_image,
                                                                                         first_column_colors,
                                                                                         second_column_colors,
                                                                                         third_column_colors,
                                                                                         fourth_column_colors,
                                                                                         fifth_column_colors):
                        if color1 == '' or color2 == '' or color3 == '' or color4 == '' or color5 == '':
                            sorted_images.update({number: name_file})

                    cursor.executemany(CommandsDb.COMMAND_INSERT_SORTING_IMAGE, list(sorted_images.items()), )
                    colors_db.commit()

                    tk.Label(self.main_screen,
                             text=TitlesWindow.TEXT_AFTER_SORTING,
                             font=SettingsFontWindow.TITLE_FONT).grid(row=4, column=1, padx=2, pady=2)
