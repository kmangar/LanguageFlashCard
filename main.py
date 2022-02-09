import random
from tkinter import *
from pandas import *

BACKGROUND_COLOR = "#B1DDC6"
card = None

# ----------------- random word ------------------------ #
data = pandas.read_csv("data/french_words.csv")
french_english_dict = data.to_dict(orient="records")


def french_word_gen():
    global card, flip_timer
    screen.after_cancel(flip_timer)

    canvas.itemconfig(canvas_title, text="French", fill="black")
    card = random.choice(french_english_dict)
    canvas.itemconfig(canvas_word, text=card["French"], fill="black")

    canvas.itemconfig(canvas_image, image=front_card)
    flip_timer = screen.after(4000, english_translate)

# ----------------- English ------------------------ #

def english_translate():
    canvas.itemconfig(canvas_image, image=back_card)
    canvas.itemconfig(canvas_title, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=card["English"], fill="white")

# ----------------- save progress ------------------------ #


# ----------------- UI ------------------------ #

screen = Tk()
screen.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
screen.title("Language Card")

flip_timer = screen.after(4000, english_translate)

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
right_button = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=french_word_gen)
right_button.grid(row=1, column=0)

# wrong button
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=french_word_gen)
wrong_button.grid(row=1, column=1)

french_word_gen()

screen.mainloop()
