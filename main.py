import os
import random
from tkinter import *
from tkinter import messagebox

from pandas import *

BACKGROUND_COLOR = "#B1DDC6"
card = None
language = None
words_to_learn = {}


try:
    data = pandas.read_csv("data/words_to_learn.csv")
    language = data.columns[0]
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
    language = original_data.columns[0]
else:
    words_to_learn = data.to_dict(orient="records")

# print(type(language))

# ----------------- random word ------------------------ #


def next_word():
    global card, flip_timer
    screen.after_cancel(flip_timer)

    canvas.itemconfig(canvas_title, text=f"{language}", fill="black")
    card = random.choice(words_to_learn)
    canvas.itemconfig(canvas_word, text=card[language], fill="black")

    canvas.itemconfig(canvas_image, image=front_card)
    flip_timer = screen.after(4000, english_translate)

# ----------------- English ------------------------ #


def english_translate():
    canvas.itemconfig(canvas_image, image=back_card)
    canvas.itemconfig(canvas_title, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=card["English"], fill="white")

# ----------------- save progress ------------------------ #


def is_known():
    if len(words_to_learn) > 1:
        words_to_learn.remove(card)
        data = pandas.DataFrame(words_to_learn)
        data.to_csv("data/words_to_learn.csv", index= False)
        next_word()
    else:
        messagebox.showinfo(title="You did it!!",
                            message=f"Congratulations! You've learned all the words in {language}\nGreat job!!")
        os.remove("data/words_to_learn.csv")

# ----------------- SAVE option on exit ------------------------ #


def save_files():
    if messagebox.askyesno(title="Goodbye", message="Do you want to save your progress") == True:
        data = pandas.DataFrame(words_to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
        screen.destroy()
    else:
        os.remove("data/words_to_learn.csv")
        screen.destroy()


# ----------------- UI ------------------------ #


screen = Tk()
screen.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
screen.title("Language Card")

flip_timer = screen.after(4000, english_translate)
screen.protocol("WM_DELETE_WINDOW", save_files)

# Canvas
canvas = Canvas(width=800, height=526)
back_card = PhotoImage(file="images/card_back.png")
front_card = PhotoImage(file="images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=front_card)

# Canvas Text
canvas_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))

# Canvas configs
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# right button
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known)
right_button.grid(row=1, column=1)

# wrong button
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_word)
wrong_button.grid(row=1, column=0)

next_word()

screen.mainloop()
