# Author: Seokwon Kim
# Project: FlashCards for SAT Vocabulary
# Version: 2
# Course: CS 361
# File Description: This is the main file of this project

from os.path import isfile, join
from os import listdir
from subprocess import PIPE
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter.messagebox import showinfo
from microservice.client import main
import subprocess
import tkinter as tk
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
        self.photoimage = None
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
        self.random_order = tk.IntVar()
        self.option_menu_clicked = tk.StringVar()
        self.add_new_option_clicked = tk.StringVar()
        self.default_word_list_file_name = 'sat_words.txt'
        self.pack()
        popup_showinfo()
        self.empty_grid_row(1)
        self.empty_grid_row(2)
        self.main_button('New List', self.new_list_window, 3, 1)
        self.main_button('User Guide', self.user_guide_window, 3, 3)
        self.create_photo_image_obj()
        self.main_button('Start', self.start_window, 5, 1)
        self.main_button('Quit', self.close_window, 5, 3)
        self.find_flashcards()
        self.lb_flashcard_list()
        self.create_main_option_menu()
        self.random_checkbox()
        self.new_file_add_lb_text = """Please enter a new flashcard
        file name to create and press 'Create' button"""
        self.new_file_name_input_box = ''
        self.add_new_word_text =  """Please choose a flashcard
        and enter a new and its definition"""
        self.add_new_option_menu = ''
        self.new_word_input_box = ''
        self.definition_input_box = ''
        self.how_to_begin_text = "How to start?"

    def random_checkbox(self):
        """Provide a random checkbox"""
        cb_random = tk.Checkbutton(self, text='Random Order', variable=self.random_order,
                                   onvalue=1, offvalue=0, command=None)
        cb_random.grid(row=6)
        cb_random.grid(column=1)

    def create_photo_image_obj(self):
        """Create a photo image and place in a desired grid"""
        photo = PhotoImage(file="images/flashcard.png")
        label = tk.Label(self, image=photo)
        label.image = photo
        label.grid(row=4)
        label.grid(column=2)

    def random_generator(self):
        """Update random_order value and open a start window"""
        if not self.random_order:
            self.random_order = True
        self.start_window()

    def find_flashcards(self):
        """Create a flashcard_list"""
        list_files = [f for f in listdir(
            self.base_dir) if isfile(join(self.base_dir, f))]
        self.flashcard_list = list_files

    def create_main_option_menu(self):
        """Create a main option menu"""
        self.option_menu_clicked.set(self.default_word_list_file_name)
        option_menu = tk.OptionMenu(
            self, self.option_menu_clicked, *self.flashcard_list)
        option_menu.grid(row=7, column=2, pady=20)

    def lb_flashcard_list(self):
        """Create a flashcard list label"""
        self.lb_flashcard_list = tk.Label(self, text='Choose a Flashcard',
                                          font=(self.font, self.font_size - 6))
        self.lb_flashcard_list.grid(row=7, column=1, pady=20)

    def quit_text(self):
        """Returns a quit confirmation text"""
        return 'Do you want to quit?'

    def on_closing(self):
        """Messagebox for main window"""
        if messagebox.askokcancel("Quit", self.quit_text(), parent=self.start):
            self.start.destroy()

    def on_closing_new_list(self):
        """Messagebox for new list window"""
        if messagebox.askokcancel("Quit", self.quit_text(), parent=self.new_list):
            self.new_list.destroy()

    def on_closing_user_guide(self):
        """Messagebox for quit window"""
        if messagebox.askokcancel("Quit", self.quit_text(), parent=self.user_guide):
            self.user_guide.destroy()

    def previous_word(self):
        """Navigate to the previous word"""
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
        """Navigate to the next word"""
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
        """Flip the flashcard"""
        if not self.flip:
            self.flip = True
        else:
            self.flip = False
        self.start_lb_var.set(
            self.word_list[self.card_index][1 if self.flip else 0])

    def create_lb(self, root, lb_text, row_num, col_num, font_adjust, stick_val="w"):
        """Create a label"""
        lb = tk.Label(root, text=lb_text,
                                 font=(self.font, self.font_size + font_adjust))
        lb.grid(row=row_num, column=col_num, pady=10, sticky=stick_val)

    def place_separator(self, root, row_num):
        """Place a separator line"""
        separator = tk.ttk.Separator(root, orient='horizontal')
        separator.grid(row=row_num, pady=20, sticky="ew")

    def begin_text(self):
        """Return a begin text"""
        how_to_begin = """Choose a flashcard from the option list (1)
        Select if you want a random order by selecting the Random Order box (2)
        Finally click 'Start' button (3)"""
        return how_to_begin

    def place_image(self, image_location, row_num):
        """Import an image and place in a grid"""
        image = PhotoImage(file=image_location)
        image_lb = tk.Label(self.user_guide, image=image)
        image_lb.image = image
        image_lb.grid(row=row_num, column=0)

    def add_text(self):
        """Returns an add text"""
        how_to_add = """To create a new flashcard, please enter a flashcard
        name (1) and click 'Create' button (2)
        To add an additional word to the existing flashcard, choose a
        flashcard (A), enter word (B) and definition (C), and click
        'Add' button (D)."""
        return how_to_add

    def user_guide_window(self):
        """Create a user guide window"""
        self.user_guide = tk.Toplevel(root)
        self.user_guide.protocol("WM_DELETE_WINDOW", self.on_closing_user_guide)
        self.user_guide.wm_title('User Guide')
        self.place_separator(self.user_guide, 0)
        self.create_lb(self.user_guide, self.how_to_begin_text, 1, 0, -6)
        self.create_lb(self.user_guide, self.begin_text(), 2, 0, -6)
        self.place_image("images/user_guide/how_to_start.png", 3)
        self.place_separator(self.user_guide, 3)
        self.create_lb(self.user_guide, 'How to add?', 4, 0, -5)
        self.create_lb(self.user_guide, self.add_text(), 5, 0, -6)
        self.place_image("images/user_guide/how_to_add.png", 6)

    def create_entry_box(self, root, row_num, col_num):
        """Create an entry box"""
        self.new_file_name_input_box = tk.Entry(root, width=40)
        self.new_file_name_input_box.grid(row=row_num, column=col_num, pady=10)

    def create_button(self, root, text, command, adjust, row_num, col_num, width=6):
        """Create a button and place in a desired grid"""
        self.btn_create_new_file = tk.Button(root, text=text,
        command=command, width=width, height=1, font=(self.font, self.font_size + adjust))
        self.btn_create_new_file.grid(row=row_num, column=col_num, padx=20, pady=5, sticky="w")

    def create_new_flashcard(self):
        """Create a top layout of new list window"""
        self.place_separator(self.new_list, 0)
        self.create_lb(self.new_list, self.new_file_add_lb_text, 1, 0, -6)
        self.create_lb(self.new_list, '           ', 1, 2, -6)
        self.create_entry_box(self.new_list, 2, 0)
        self.create_button(self.new_list, 'Create', self.create_new_file, -6, 2, 1)
        self.place_separator(self.new_list, 3)
        self.create_lb(self.new_list, self.add_new_word_text, 4, 0, -6)

    def create_option_menu(self, option_click, default, root, row_num, col_num):
        """Create an option menu"""
        option_click.set(default)
        self.add_new_option_menu = tk.OptionMenu(root, option_click,
        *self.flashcard_list)
        self.add_new_option_menu.grid(row=row_num, column=col_num, padx=20, pady=10, sticky="w")

    def new_list_window(self):
        """Create a new list window"""
        self.new_list = tk.Toplevel(root)
        self.new_list.protocol("WM_DELETE_WINDOW", self.on_closing_new_list)
        self.new_list.wm_title('New List Window')
        self.create_new_flashcard()
        self.create_option_menu(self.add_new_option_clicked, "sat_words.txt", self.new_list, 4, 1)
        self.create_lb(self.new_list, 'Word', 6, 0, -6, "we")
        self.new_word_input_box = tk.Entry(self.new_list, width=40)
        self.new_word_input_box.grid(row=6, column=1, padx=20, pady=10, sticky="w")
        self.create_lb(self.new_list, 'Definition', 7, 0, -6, "we")
        self.definition_input_box = tk.Text(self.new_list, width=40, height=5)
        self.definition_input_box.grid(row=7, column=1, padx=20, pady=10, sticky="w")
        self.create_button(self.new_list, 'Add', self.add_new_word, -6, 8, 1)

    def add_new_word(self):
        """Add a new word into the selected flashcard"""
        file_name = self.add_new_option_clicked.get()
        new_word = self.new_word_input_box.get()
        definition = self.definition_input_box.get("1.0", "end")
        with open(self.base_dir + file_name, 'a') as f:
            f.write(new_word + ',' + definition)
        messagebox.showinfo(parent=self.new_list, message='New word and definition added')
        self.add_new_option_clicked.set("sat_words.txt")
        self.new_word_input_box.delete(0, 'end')
        self.definition_input_box.delete("1.0", "end")

    def create_new_file(self):
        """Create a new flashcard"""
        file_name = self.new_file_name_input_box.get()
        open(self.base_dir + file_name, 'x')
        self.new_file_name_input_box.delete(0, 'end')
        messagebox.showinfo(parent=self.new_list, message='New flashcard successfully created!')

    def start_window_first_part(self):
        """Returns a first layout of start window"""
        txt_file = self.option_menu_clicked.get()
        self.start = tk.Toplevel(root)
        self.start.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.start.wm_title(txt_file)
        self.word_list = read_file(txt_file)

    def start_window_second_part(self):
        """Returns a second layout of start window"""
        self.card_index = 0
        self.start_lb_var.set(
            self.word_list[self.card_index][1 if self.flip else 0])
        self.start_lb = tk.Label(self.start, textvariable=self.start_lb_var,
                                 font=(self.font, self.font_size),
                                 width=20, height=10, wraplength=400, justify="center")
        self.start_lb.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E)
        self.start_lb.bind("<Button-1>", lambda e: self.card_flip())
        self.create_button(self.start, "Previous", self.previous_word, 0, 1, 0, self.btn_width)
        self.create_button(self.start, "Next", self.next_word, 0, 1, 1, self.btn_width)

    def start_window(self):
        """Create a start window"""
        self.start_window_first_part()
        if self.random_order.get() == 1:
            length = str(len(self.word_list))
            try:
                response = subprocess.run(
                    ['python', 'microservice\\client.py', length],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
                random_list = response.stdout.decode('utf-8').split(',')
                random_list = [int(x) - 1 for x in random_list]
                self.word_list = self.reorder_list(self.word_list, random_list)
            except Exception as e:
                print(e)
                random.shuffle(self.word_list)
        self.start_window_second_part()

    def reorder_list(self, word_list, index_list):
        """Reorder the flashcard based on the array of indexes"""
        new_word_list = list()
        for val in index_list:
            new_word_list.append(word_list[val])

        return new_word_list

    def close_window(self):
        """Close window"""
        root.destroy()

    def empty_grid_row(self, row_num):
        """Placeholder label"""
        lb = tk.Label(self, text="", font=(self.font, self.font_size))
        lb.grid(row=row_num, column=0)

    def main_button(self, title, command, row_num, col_num):
        """Create a main window"""
        button_new_list = tk.Button(self, text=title, command=command,
                                    width=self.btn_width, height=self.height,
                                    font=(self.font, self.font_size))
        button_new_list.grid(row=row_num, column=col_num)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Flashcards for SAT Vocabulary")
    root.geometry("960x600")
    flashcard = FlashCard(root)
    root.mainloop()
    os._exit(0)
