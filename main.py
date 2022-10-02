import re
import sys
import sqlite3
import tkinter as tk

from tkinter import *
from tkinter import colorchooser

from PIL import Image as PilImage, ImageTk

from colors import get_image_colors
from config import directory_for_photos
from google_table import GoogleTable, RegionsGoogleTable
from constants import ButtonsWindow, SettingsCanvas, ElementsColorWindow, TitlesWindow, SizesWindow, \
    SettingsFontWindow, CommandsDb

colors_db = sqlite3.connect('сolors.db')
cursor = colors_db.cursor()


class GradientCanvas(tk.Frame):
    """ Init the gradient frame in the canvas """

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
        """Draw a gradient frame based on the color received from the user"""

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
    """ In the class, we initialize the buttons and work with them """

    def __init__(self, colors, main_screen, file_image):
        self.colors = colors
        self.main_screen = main_screen
        self.file_image = file_image

    def get_colored_buttons(self, frame):
        """ We get 4 buttons that contain colors from the photo """

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
        """ We get 4 main buttons that are always on the screen """

        google_table = GoogleTable(self.file_image, self.main_screen)

        button_send = tk.Button(self.main_screen,
                                text=ButtonsWindow.BUTTON_SEND,
                                command=google_table.send_colors_google_spreedsheet,
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
        """In this method, we initialize the gradient frame in the plane of the main application
         by getting the colors that the user chooses
         """

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

            GradientCanvas(self.main_screen, first_hex_color, second_hex_color).grid(row=0, column=4)

            tk.Button(self.main_screen,
                      text=ButtonsWindow.CHANGE_BUTTON_COLOR_GRADIENT,
                      command=self.change_color_gradient_table,
                      width=33,
                      fg=SettingsFontWindow.SECOND_FONT_COLOR,
                      font=SettingsFontWindow.BUTTONS_FONT,
                      bg=ElementsColorWindow.BACKGROUND_COLOR_BUTTON,
                      height=1).grid(row=1, column=4, padx=2, pady=2)

    def build_first_color_frame(self, color):
        """In this method, we initialize the color frame № 1 in the plane of the main application
         by obtaining the colors that the user chooses
         """

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
        """In this method, we initialize the color frame № 2 in the plane of the main application
         by obtaining the colors that the user chooses
         """

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
        """In this method, we initialize the color frame № 1 in the plane of the main application
         by obtaining the colors that the user chooses
         """

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
        """In this method, we change the gradient frame in the plane of the main application
         by getting the colors that the user chooses
         """

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

            GradientCanvas(self.main_screen, first_hex_color, second_hex_color).grid(row=0, column=4)

    def change_first_color_table(self):
        """In this method, we change the color frame № 1 in the plane of the main application
        by getting the colors that the user chooses
        """

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
        """In this method, we change the color frame № 2 in the plane of the main application
        by getting the colors that the user chooses
        """

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
        """In this method, we change the color frame № 3 in the plane of the main application
        by getting the colors that the user chooses
        """

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

    def switch_image(self):
        """ switching the current image to the next one """

        for command_select, command_deleted in zip(CommandsDb.COMMANDS_SELECT, CommandsDb.COMMANDS_DELETED):
            cursor.execute(command_select)
            if cursor.fetchone() is not None:
                cursor.execute(command_deleted, )
                colors_db.commit()

        self.main_screen.destroy()

    @staticmethod
    def close_main_window():
        """ closing the application """

        for command_select, command_deleted in zip(CommandsDb.COMMANDS_SELECT, CommandsDb.COMMANDS_DELETED):
            cursor.execute(command_select)
            if cursor.fetchone() is not None:
                cursor.execute(command_deleted, )
                colors_db.commit()

        colors_db.close()
        sys.exit()


class MainScreen:

    def __init__(self, image, colors):
        self.image = image
        self.colors = colors
        self.main_screen = Tk()

    def get_main_screen(self, inner_frame):
        """ Open the main application and initialize all the necessary elements """

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

        value_listbox = RegionsGoogleTable(self.get_listbox(), self.main_screen)
        sorting_image = value_listbox.sorting_image_by_regions

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
        """ We get a frame with a scroll, in which there are buttons with the colors of the image """

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

    def get_listbox(self):
        """ we get a list with regions to sort """

        listbox = Listbox(self.main_screen, width=18, height=4, selectmode=MULTIPLE)

        for number_button in range(4):
            listbox.insert(number_button, ButtonsWindow.SORTING_REGION[number_button])

        listbox.grid(row=3, column=1, padx=1, pady=1)

        return listbox


def main():
    cursor.execute(CommandsDb.COMMAND_SELECT_SORTING_IMAGE)
    images = cursor.fetchall()
    for image in images:
        file = f'{directory_for_photos}{image[1]}'

        main_screen = MainScreen(file, get_image_colors(file))
        main_screen.get_main_screen(main_screen.get_inner_frame())


if __name__ == '__main__':
    main()
