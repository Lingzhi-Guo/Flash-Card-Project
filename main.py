from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    to_learn = data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

chosen_dic = {}
# --------------------CREATING NEW FLASH CARDS------------------#

def next_card():
    global chosen_dic
    chosen_dic = random.choice(data)
    title = "French"
    word = chosen_dic["French"]
    canvas.itemconfig(canvas_image, image=front_img)
    canvas.itemconfig(title_text, text=title)
    canvas.itemconfig(word_text, text=word)
    button_wrong.config(state="disabled")
    button_right.config(state="disabled")
    countdown(3)

# -----------------------FLIPPING THE CARDS--------------------------#

def flip_cards():
    canvas.itemconfig(canvas_image, image=back_img)
    title = "English"
    word = chosen_dic["English"]
    canvas.itemconfig(title_text, text=title)
    canvas.itemconfig(word_text, text=word)
    canvas.itemconfig(countdown_text, text="")
    button_wrong.config(state="normal")
    button_right.config(state="normal")

def countdown(count):
    if count > 0:
        window.after(1000, countdown, count-1)
        canvas.itemconfig(countdown_text, text=count)
    else:
        flip_cards()


# -----------------------SAVING WORDS--------------------------#
def cross_the_word():
    data.remove(chosen_dic)
    next_card()
    to_learn = pandas.DataFrame(data)
    to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# -----------------------UI SETTING--------------------------#
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
wrong_img = PhotoImage(file="images/wrong.png")
right_img = PhotoImage(file="images/right.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=front_img)
title_text = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
countdown_text = canvas.create_text(400, 400, text="3", fill=BACKGROUND_COLOR, font=("Arial", 45, "normal"))
canvas.grid(row=0, column=0, columnspan=2)

button_right = Button(image=right_img, command=next_card, highlightthickness=0)
button_right.grid(row=1, column=0)
button_wrong = Button(image=wrong_img, command=cross_the_word, highlightthickness=0)
button_wrong.grid(row=1, column=1)

next_card()

window.mainloop()
