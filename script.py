import os
import re
import shutil
import sys
import tkinter as tk
from pathlib import Path
from tkinter import *
from tkinter import colorchooser
from tkinter import tix
from tkinter.tix import *

import cv2
import gspread
import numpy as np

from config import *
from consts import *

directory = DIR
directory_all = DIR2

files = Path(directory).glob('*')
files2 = Path(directory_all).glob('*')

gr = []
gr_two = []
gr_third = []
gr_fourth = []

window_gr_1 = np.zeros((190, 390, 3), dtype='uint8')
window_gr_2 = np.zeros((190, 390, 3), dtype='uint8')
window_1 = np.zeros((90, 400, 3), dtype='uint8')
window_2 = np.zeros((90, 400, 3), dtype='uint8')
window_3 = np.zeros((90, 400, 3), dtype='uint8')

credentials = gspread.service_account(filename=FILE_NAME)
sheet = credentials.open_by_url(PATH_TABLE)
connectors_sheet = sheet.worksheet(WORKSHEET)


class Gui(object):

    def __init__(self):
        self.build_gui()

    def build_gui(self):

        for file in files:

            img = cv2.imread(str(file))
            img2 = cv2.imread(str(file))
            img = cv2.resize(img, (256, 256))
            img2 = cv2.resize(img2, (img2.shape[1] // 12, img2.shape[0] // 12))

            winname = str(file)[16:][:-3]
            cv2.namedWindow(winname)
            cv2.moveWindow(winname, 1617, 17)
            cv2.imshow(winname, img)

            height = np.size(img2, 0)
            width = np.size(img2, 1)

            colors = []
            for i in range(1, width):
                for l in range(1, height):
                    (b, g, r) = img2[l, i]
                    color = str((r, g, b))
                    colors.append(color)

            colors2 = []

            for l in colors:
                if l not in colors2:
                    colors2.append(l)

            colors = colors2

            root = tix.Tk()
            root.title(TITLE)
            root.iconbitmap(ICON)
            root.config(bg=BG_WINDOW)
            root.geometry(ROOT_CONSTANT)

            def buttons(frame):

                for color_gr in colors:
                    index = colors.index(color_gr)
                    re_digits = re.compile(r"\b\d+\b")
                    ls = re_digits.findall(colors[index])

                    hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))
                    tk.Button(frame,
                              text=f'{hex_color}',
                              fg=FONT_COLOR,
                              bg=hex_color,
                              width=8,
                              height=1,
                              command=lambda color_gr=color_gr: self.table_gradient(color_gr)).grid(row=index,
                                                                                                    pady=2,
                                                                                                    padx=2,
                                                                                                    column=1)
                for color_3 in colors:
                    index = colors.index(color_3)
                    re_digits = re.compile(r"\b\d+\b")
                    ls = re_digits.findall(colors[index])

                    hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))
                    tk.Button(frame,
                              text=f'{hex_color}',
                              fg=FONT_COLOR,
                              bg=hex_color,
                              width=8,
                              height=1,
                              command=lambda color_3=color_3: self.table_two(color_3)).grid(row=index,
                                                                                            pady=2,
                                                                                            padx=2,
                                                                                            column=2)
                for color_4 in colors:
                    index = colors.index(color_4)
                    re_digits = re.compile(r"\b\d+\b")
                    ls = re_digits.findall(colors[index])

                    hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))
                    tk.Button(frame,
                              text=f'{hex_color}',
                              fg=FONT_COLOR,
                              bg=hex_color,
                              width=8,
                              height=1,
                              command=lambda color_4=color_4: self.table_third(color_4)).grid(row=index,
                                                                                              pady=2,
                                                                                              padx=2,
                                                                                              column=3)
                for color_5 in colors:
                    index = colors.index(color_5)
                    re_digits = re.compile(r"\b\d+\b")
                    ls = re_digits.findall(colors[index])

                    hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))
                    tk.Button(frame,
                              text=f'{hex_color}',
                              fg=FONT_COLOR,
                              bg=hex_color,
                              width=8,
                              height=1,
                              command=lambda color_5=color_5: self.table_fourth(color_5)).grid(row=index,
                                                                                               pady=2,
                                                                                               padx=2,
                                                                                               column=4)

            def onFrameConfigure(canvas):

                canvas.configure(scrollregion=canvas.bbox("all"))

            canvas = tk.Canvas(root, borderwidth=0, background=BG_CANVAS, width=290, height=300)
            frame = tk.Frame(canvas, background=BG_CANVAS)
            vsb = tk.Scrollbar(root, orient=ORIENT, command=canvas.yview)
            canvas.configure(yscrollcommand=vsb.set)

            vsb.grid(row=3, column=0, sticky=NS)
            canvas.grid(row=3, column=1)
            canvas.create_window((3, 3), window=frame, anchor="nw")

            frame.bind(CONFIG, lambda event, canvas=canvas: onFrameConfigure(canvas))

            buttons(frame)

            def sort(*args):

                for file_name in files:
                    os.remove(file_name)

                variable_option = variable.get()

                if variable_option == 'RU':

                    logos = connectors_sheet.col_values(8)
                    logos.pop(0)

                    logos_ru = connectors_sheet.col_values(14)
                    logos_ru.pop(0)

                    local_name = []

                    for name, number in zip(logos, logos_ru):

                        try:
                            if int(number) in range(1, 6000):
                                local_name.append(name)
                        except:
                            print()

                    for file_name in files2:
                        for i in local_name:
                            if i == str(file_name)[14:]:
                                print(i)
                                shutil.copyfile(file_name, f'{DIR}{i}')

                    tk.Label(root,
                             text=ClOSE_WINDOW_TEXT,
                             fg=LABEL_COLOR,
                             font=9).grid(row=1,
                                          column=1,
                                          padx=2,
                                          pady=2)

                elif variable_option == 'EN':

                    logos = connectors_sheet.col_values(8)
                    logos.pop(0)

                    logos_ru = connectors_sheet.col_values(16)
                    logos_ru.pop(0)

                    local_name = []

                    for name, number in zip(logos, logos_ru):

                        try:
                            if int(number) in range(1, 6000):
                                local_name.append(name)
                        except:
                            print()

                    for file_name in files2:
                        for i in local_name:
                            if i == str(file_name)[14:]:
                                print(i)
                                shutil.copyfile(file_name, f'{DIR}{i}')

                    tk.Label(root,
                             text=ClOSE_WINDOW_TEXT,
                             fg=LABEL_COLOR,
                             font=9).grid(row=1,
                                          column=1,
                                          padx=2,
                                          pady=2)

            def reset_gradient():
                gr.clear()

            def next_logo():

                gr.clear()
                gr_two.clear()
                gr_third.clear()
                gr_fourth.clear()

                try:
                    root.destroy()
                except:
                    print()

                try:
                    root1.destroy()
                except:
                    print()

                try:
                    root2.destroy()
                except:
                    print()

                try:
                    root3.destroy()
                except:
                    print()

                try:
                    root4.destroy()
                except:
                    print()

                cv2.destroyAllWindows()

            def exit_window():
                sys.exit()

            def google_table():

                re_digits_table_format = re.compile(r"\b\d+\b")

                ls_gr = re_digits_table_format.findall(gr[0])
                hex_color_gr_1 = HEX_CONSTANT % (int(ls_gr[0]), int(ls_gr[1]), int(ls_gr[2]))

                ls1 = re_digits_table_format.findall(gr[1])
                hex_color_gr_2 = HEX_CONSTANT % (int(ls1[0]), int(ls1[1]), int(ls1[2]))

                ls2 = re_digits_table_format.findall(gr_two[0])
                hex_color_t_1 = HEX_CONSTANT % (int(ls2[0]), int(ls2[1]), int(ls2[2]))

                ls3 = re_digits_table_format.findall(gr_third[0])
                hex_color_t_2 = HEX_CONSTANT % (int(ls3[0]), int(ls3[1]), int(ls3[2]))

                ls4 = re_digits_table_format.findall(gr_fourth[0])
                hex_color_t_3 = HEX_CONSTANT % (int(ls4[0]), int(ls4[1]), int(ls4[2]))

                logos_col = connectors_sheet.col_values(8)
                name_logo_file = str(file)
                name_logo_file_table = name_logo_file[16:]

                if name_logo_file_table in logos_col:

                    index_logo = logos_col.index(name_logo_file_table)
                    row = index_logo + 1

                    connectors_sheet.update(f'I{row}', hex_color_gr_1)
                    connectors_sheet.update(f'J{row}', hex_color_gr_2)
                    connectors_sheet.update(f'K{row}', hex_color_t_1)
                    connectors_sheet.update(f'L{row}', hex_color_t_2)
                    connectors_sheet.update(f'M{row}', hex_color_t_3)

                gr.clear()
                gr_two.clear()
                gr_third.clear()
                gr_fourth.clear()

                root.destroy()
                root1.destroy()
                root2.destroy()
                root3.destroy()
                root4.destroy()

                cv2.destroyAllWindows()
                os.remove(file)
                os.remove(f"{DIR2}{str(file)[16:]}")

            tk.Button(root,
                      text=BUTTON_SEND,
                      command=google_table,
                      width=18,
                      fg=FONT_COLOR2,
                      font=BUTTON_FONT,
                      bg=BG_COLOR_BUTTON,
                      height=2).grid(row=1,
                                     column=2,
                                     padx=2,
                                     pady=2)
            tk.Button(root,
                      text=BUTTON_CLOSE,
                      command=exit_window,
                      width=18,
                      fg=FONT_COLOR2,
                      font=BUTTON_FONT,
                      bg=BG_COLOR_BUTTON,
                      height=2).grid(row=2,
                                     column=3,
                                     padx=2,
                                     pady=2)

            tk.Button(root,
                      text=BUTTON_MISS,
                      command=next_logo,
                      width=18,
                      fg=FONT_COLOR2,
                      font=BUTTON_FONT,
                      bg=BG_COLOR_BUTTON,
                      height=2).grid(row=1,
                                     column=3,
                                     padx=2,
                                     pady=2)

            tk.Button(root,
                      text=BUTTON_RESET,
                      command=reset_gradient,
                      width=18,
                      fg=FONT_COLOR2,
                      font=BUTTON_FONT,
                      bg=BG_COLOR_BUTTON,
                      height=2).grid(row=2,
                                     column=1,
                                     padx=2,
                                     pady=2)

            tk.Label(root,
                     text=f"{LABEL_LOGO}\n{str(file)[16:]}",
                     fg=LABEL_COLOR,
                     font=LABEL_FONT).grid(row=1,
                                           column=1,
                                           padx=2,
                                           pady=2)

            variable = tk.StringVar(root)
            variable.set(LABEL_MENU)

            opt = tk.OptionMenu(root, variable, *SORT)
            opt.config(width=16,
                       height=2,
                       font=MENU_FONT,
                       bg=BG_COLOR_BUTTON,
                       fg=FONT_COLOR2)
            opt.grid(row=2, column=2)
            variable.trace("w", sort)

            root.mainloop()

    def table_gradient(self, color_gr):

        global root1

        try:
            root1.destroy()
        except:
            print()

        gr.append(color_gr)

        if len(gr) == 2:

            re_digits = re.compile(r"\b\d+\b")
            ls = re_digits.findall(gr[0])
            ls2 = re_digits.findall(gr[1])

            figure_1 = cv2.rectangle(window_gr_1, (0, 0), (400, 200), (int(ls[2]), int(ls[1]), int(ls[0])),
                                     thickness=cv2.FILLED)
            figure_2 = cv2.rectangle(window_gr_2, (0, 0), (400, 200), (int(ls2[2]), int(ls2[1]), int(ls2[0])),
                                     thickness=cv2.FILLED)

            cv2.imwrite(FILE_NAME_GR_1, figure_1)
            cv2.imwrite(FILE_NAME_GR_2, figure_2)

            img1 = cv2.resize(cv2.imread(FILE_NAME_GR_1), (400, 200))
            img2 = cv2.resize(cv2.imread(FILE_NAME_GR_2), (400, 200))

            mask1 = np.repeat(np.tile(np.linspace(1, 0, img1.shape[1]), (img1.shape[0], 1))[:, :, np.newaxis], 3,
                              axis=2)
            mask2 = np.repeat(np.tile(np.linspace(0, 1, img2.shape[1]), (img2.shape[0], 1))[:, :, np.newaxis], 3,
                              axis=2)

            final = np.uint8(img1 * mask1 + img2 * mask2)

            winname = NAME_TABLE_GR
            cv2.namedWindow(winname)
            cv2.moveWindow(winname, 613, 17)
            cv2.imshow(winname, final)

        def pick_color():
            hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))

            color = colorchooser.askcolor(hex_color,
                                          title=BUTTON_COLOR)

            gr.append(str(color[0]))

            if len(gr) == 2:

                re_digits_1 = re.compile(r"\b\d+\b")
                ls_1 = re_digits_1.findall(gr[0])
                ls_2 = re_digits_1.findall(gr[1])

                figure_1_change = cv2.rectangle(window_gr_1, (0, 0), (400, 200),
                                                (int(ls_1[2]), int(ls_1[1]), int(ls_1[0])),
                                                thickness=cv2.FILLED)
                figure_2_change = cv2.rectangle(window_gr_2, (0, 0), (400, 200),
                                                (int(ls_2[2]), int(ls_2[1]), int(ls_2[0])),
                                                thickness=cv2.FILLED)

                cv2.imwrite(FILE_NAME_GR_1, figure_1_change)
                cv2.imwrite(FILE_NAME_GR_2, figure_2_change)

                img_1 = cv2.resize(cv2.imread(FILE_NAME_GR_1), (400, 200))
                img_2 = cv2.resize(cv2.imread(FILE_NAME_GR_2), (400, 200))

                mask_1 = np.repeat(np.tile(np.linspace(1, 0, img1.shape[1]), (img1.shape[0], 1))[:, :, np.newaxis], 3,
                                  axis=2)
                mask_2 = np.repeat(np.tile(np.linspace(0, 1, img2.shape[1]), (img2.shape[0], 1))[:, :, np.newaxis], 3,
                                  axis=2)

                final = np.uint8(img_1 * mask_1 + img_2 * mask_2)

                winname = NAME_TABLE_GR
                cv2.namedWindow(winname)
                cv2.moveWindow(winname, 613, 17)
                cv2.imshow(winname, final)

        root1 = Tk()
        root1.title(TITLE)
        root1.iconbitmap(ICON)
        root1.config(bg=BG_WINDOW)
        root1.geometry(ROOT_CONSTANT1)

        tk.Button(root1,
                  text=BUTTON_COLOR,
                  command=pick_color,
                  width=18,
                  fg=FONT_COLOR2,
                  font=BUTTON_FONT,
                  bg=BG_COLOR_BUTTON,
                  height=2).grid(row=2, column=2)

    def table_two(self, color_3):

        global root2

        try:
            root2.destroy()
            gr_two.clear()
            gr_two.append(color_3)

        except:
            gr_two.append(color_3)

        re_digits = re.compile(r"\b\d+\b")
        ls = re_digits.findall(gr_two[0])

        cv2.rectangle(window_1, (0, 0), (400, 100), (int(ls[2]), int(ls[1]), int(ls[0])), thickness=cv2.FILLED)

        winname = NAME_TABLE_AINSYS_1
        cv2.namedWindow(winname)
        cv2.moveWindow(winname, 613, 250)
        cv2.imshow(winname, window_1)

        def pick_color():

            hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))

            color = colorchooser.askcolor(hex_color,
                                          title=BUTTON_COLOR)

            try:
                gr_two.clear()
                gr_two.append(str(color[0]))

            except:
                gr_two.append(str(color[0]))

            re_digits2 = re.compile(r"\b\d+\b")
            ls2 = re_digits2.findall(str(color[0]))

            cv2.rectangle(window_1, (0, 0), (400, 100), (int(ls2[2]), int(ls2[1]), int(ls2[0])), thickness=cv2.FILLED)

            winname = NAME_TABLE_AINSYS_1
            cv2.namedWindow(winname)
            cv2.moveWindow(winname, 613, 250)
            cv2.imshow(winname, window_1)

        root2 = Tk()
        root2.title(TITLE)
        root2.iconbitmap(ICON)
        root2.config(bg=BG_WINDOW)
        root2.geometry(ROOT_CONSTANT2)

        tk.Button(root2,
                  text=BUTTON_COLOR,
                  command=pick_color,
                  width=18,
                  fg=FONT_COLOR2,
                  font=BUTTON_FONT,
                  bg=BG_COLOR_BUTTON,
                  height=2).grid(row=2,
                                 column=2)

    def table_third(self, color_4):

        global root3

        try:
            root3.destroy()
            gr_third.clear()
            gr_third.append(color_4)
        except:
            gr_third.append(color_4)

        re_digits = re.compile(r"\b\d+\b")
        ls = re_digits.findall(gr_third[0])

        cv2.rectangle(window_2, (0, 0), (400, 100), (int(ls[2]), int(ls[1]), int(ls[0])), thickness=cv2.FILLED)

        winname = NAME_TABLE_AINSYS_2
        cv2.namedWindow(winname)
        cv2.moveWindow(winname, 613, 372)
        cv2.imshow(winname, window_2)

        def pick_color():

            hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))

            color = colorchooser.askcolor(hex_color,
                                          title=BUTTON_COLOR)

            try:
                gr_third.clear()
                gr_third.append(str(color[0]))

            except:
                gr_third.append(str(color[0]))

            re_digits2 = re.compile(r"\b\d+\b")
            ls2 = re_digits2.findall(str(color[0]))

            cv2.rectangle(window_2, (0, 0), (400, 100), (int(ls2[2]), int(ls2[1]), int(ls2[0])), thickness=cv2.FILLED)

            winname = NAME_TABLE_AINSYS_2
            cv2.namedWindow(winname)
            cv2.moveWindow(winname, 613, 372)
            cv2.imshow(winname, window_2)

        root3 = Tk()
        root3.title(TITLE)
        root3.iconbitmap(ICON)
        root3.config(bg=BG_WINDOW)
        root3.geometry(ROOT_CONSTANT3)

        tk.Button(root3,
                  text=BUTTON_COLOR,
                  command=pick_color,
                  width=18,
                  fg=FONT_COLOR2,
                  font=BUTTON_FONT,
                  bg=BG_COLOR_BUTTON,
                  height=2).grid(row=2, column=2)

    def table_fourth(self, color_5):

        global root4

        try:
            root4.destroy()
            gr_fourth.clear()
            gr_fourth.append(color_5)
        except:
            gr_fourth.append(color_5)

        re_digits = re.compile(r"\b\d+\b")
        ls = re_digits.findall(gr_fourth[0])

        cv2.rectangle(window_3, (0, 0), (400, 100), (int(ls[2]), int(ls[1]), int(ls[0])), thickness=cv2.FILLED)

        winname = NAME_TABLE_AINSYS_3
        cv2.namedWindow(winname)
        cv2.moveWindow(winname, 613, 495)
        cv2.imshow(winname, window_3)

        def pick_color():

            hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))

            color = colorchooser.askcolor(hex_color,
                                          title=BUTTON_COLOR)

            try:
                gr_fourth.clear()
                gr_fourth.append(str(color[0]))

            except:
                gr_fourth.append(str(color[0]))

            re_digits2 = re.compile(r"\b\d+\b")
            ls2 = re_digits2.findall(str(color[0]))

            cv2.rectangle(window_3, (0, 0), (400, 100), (int(ls2[2]), int(ls2[1]), int(ls2[0])), thickness=cv2.FILLED)

            winname = NAME_TABLE_AINSYS_3
            cv2.namedWindow(winname)
            cv2.moveWindow(winname, 613, 495)
            cv2.imshow(winname, window_3)

        root4 = Tk()
        root4.title(TITLE)
        root4.iconbitmap(ICON)
        root4.config(bg=BG_WINDOW)
        root4.geometry(ROOT_CONSTANT4)

        tk.Button(root4,
                  text=BUTTON_COLOR,
                  command=pick_color,
                  width=18,
                  fg=FONT_COLOR2,
                  font=BUTTON_FONT,
                  bg=BG_COLOR_BUTTON,
                  height=2).grid(row=2, column=2)


app = Gui()
