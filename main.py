from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = []
known_words = []

try:
    data = pandas.read_csv("data/unknown_words.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/english_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="Hungarian", fill="white")
    canvas.itemconfig(card_word, text=current_card["Hungarian"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


try:
    data_checked_words = pandas.read_csv("data/known_words.csv")
except FileNotFoundError:
    pass
else:
    known_words = data_checked_words.to_dict(orient="records")


def is_known():
    data_index = pandas.read_csv("data/english_words.csv")
    to_learn_index = data_index.English.to_list()
    chosen_card_index = to_learn_index.index(current_card["English"])
    print(chosen_card_index)

    known_words.append(current_card)
    data_known_words = pandas.DataFrame(known_words)
    data_known_words.to_csv("data/known_words.csv", index=False)

    to_learn.remove(current_card)
    data_unknown_words = pandas.DataFrame(to_learn)
    data_unknown_words.to_csv("data/unknown_words.csv", index=False)

    next_card()


window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(column=1, row=1)

next_card()

window.mainloop()
