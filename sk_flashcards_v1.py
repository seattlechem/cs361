# Author: Seokwon Kim
# Project: FlashCards for SAT Vocabulary
# Version: 1
# Course: CS 361
# File Description: This is the main file of this project

from os.path import isfile, join
from os import listdir
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo
import random
import os


def read_file(file_name):
    base_dir = './files/'
    with open(base_dir + file_name, mode='r') as f:
        contents = f.readlines()
        for idx, line in enumerate(contents):
            if ',' in line:
                contents[idx] = line.split(',')
    return contents


def popup_showinfo():
    msg_txt = "You can review the words in the default word list " + \
        "by clicking the start button"
    showinfo("Message", msg_txt)


class FlashCard(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.btn_width = 20
        self.start = ''
        self.start_lb_var = tk.StringVar()
        self.word_list = None
        self.flip = False
        self.card_index = 0
        self.font = 'consolas'
        self.base_dir = './files/'
        self.font_size = 18
        self.height = 3
        self.flashcard_list = list()
        self.random_order = False
        self.option_menu_clicked = tk.StringVar()
        self.default_word_list_file_name = 'sat_words.txt'
        self.pack()
        popup_showinfo()
        self.empty_grid_row(1)
        self.empty_grid_row(2)
        self.main_button('New List', None, 3, 1)
        self.main_button('User Guide', None, 3, 3)
        self.main_button('Random', self.random_generator, 4, 2)
        self.main_button('Start', self.start_window, 5, 1)
        self.main_button('Quit', self.close_window, 5, 3)
        self.find_flashcards()
        self.lb_flashcard_list()
        self.create_option_menu()

    def random_generator(self):
        if not self.random_order:
            self.random_order = True
        self.start_window()

    def find_flashcards(self):
        # show file list in files
        list_files = [f for f in listdir(
            self.base_dir) if isfile(join(self.base_dir, f))]
        self.flashcard_list = list_files

    def create_option_menu(self):
        self.option_menu_clicked.set("sat_words.txt")
        option_menu = tk.OptionMenu(
            self, self.option_menu_clicked, *self.flashcard_list)
        option_menu.grid(row=6, column=2, pady=20)

    def lb_flashcard_list(self):
        self.lb_flashcard_list = tk.Label(self, text='Choose a Flashcard',
                                          font=(self.font, self.font_size - 6))
        self.lb_flashcard_list.grid(row=6, column=1, pady=20)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?", parent=self.start):
            self.start.destroy()

    def previous_word(self):
        if self.word_list is not None:
            if self.card_index == 0:
                messagebox.showerror(
                    "Index Error", "You're already at the first word", parent=self.start)
            else:
                self.card_index -= 1
                self.flip = False
                self.start_lb_var.set(
                    self.word_list[self.card_index][1 if self.flip else 0])

    def next_word(self):
        if self.word_list is not None:
            if self.card_index == len(self.word_list) - 1:
                messagebox.showerror(
                    "Index Error", "You're already at the last word", parent=self.start)
            else:
                self.card_index += 1
                self.flip = False
                self.start_lb_var.set(
                    self.word_list[self.card_index][1 if self.flip else 0])

    def card_flip(self):
        if not self.flip:
            self.flip = True
        else:
            self.flip = False
        self.start_lb_var.set(
            self.word_list[self.card_index][1 if self.flip else 0])

    def start_window(self):
        txt_file = self.option_menu_clicked.get()
        self.start = tk.Toplevel(root)
        self.start.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.start.wm_title("Start")
        self.word_list = read_file(txt_file)
        if self.random_order:
            random.shuffle(self.word_list)
        self.card_index = 0
        self.start_lb_var.set(
            self.word_list[self.card_index][1 if self.flip else 0])

        self.start_lb = tk.Label(self.start, textvariable=self.start_lb_var,
                                 font=(self.font, self.font_size),
                                 width=20, height=10, wraplength=400, justify="center")
        self.start_lb.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E)
        self.start_lb.bind("<Button-1>", lambda e: self.card_flip())

        btn_previous = tk.Button(self.start, text="Previous", command=self.previous_word,
                                 width=self.btn_width, height=self.height, font=(self.font, self.font_size))
        btn_previous.grid(row=1, column=0)

        btn_next = tk.Button(self.start, text="Next", command=self.next_word,
                             width=self.btn_width, height=self.height, font=(self.font, self.font_size))
        btn_next.grid(row=1, column=2)

    def close_window(self):
        root.destroy()

    def empty_grid_row(self, row_num):
        lb = tk.Label(self, text="", font=(self.font, self.font_size))
        lb.grid(row=row_num, column=0)

    def main_button(self, title, command, row_num, col_num):
        button_new_list = tk.Button(self, text=title, command=command,
                                    width=self.btn_width, height=self.height, font=(self.font, self.font_size))
        button_new_list.grid(row=row_num, column=col_num)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Flashcards for SAT Vocabulary")
    root.geometry("960x500")
    flashcard = FlashCard(root)
    root.mainloop()
    os._exit(0)
