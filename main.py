import threading
import time
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog as fd
import PIL
import customtkinter
import playsound
import pygame
from PIL import Image, ImageTk

pygame.mixer.init()
s = pygame.mixer.Sound('song.wav')
def create_files(s):
    '''
    Creates images based on the window size, and the file uploaded.
    :param s: the window size
    '''
    global f1, f2, fullf1, fullf2, fullf3, fullf4
    f1, f2 = resizer(file_list[0], (s//2, s)), resizer(file_list[1], (s//2, s))
    fullf1, fullf2, fullf3, fullf4 = resizer(file_list[2], (s, s)), resizer(file_list[3], (s, s)), resizer(
        file_list[4], (s, s)), resizer(file_list[5], (s, s))
def resizer(link: str, size: tuple):
    '''
    :param link: link to the photo/image
    :param size: size of the photo required
    :return: Resized PhotoImage object to dimensions (size[0], size[1])
    '''
    return PIL.ImageTk.PhotoImage(PIL.Image.open(link).resize(size), PIL.Image.Resampling.LANCZOS)
def play(audio):
    '''
    Plays an audio in a different thread from the main thread so that program can run with sound in the background.
    :param audio: audio file
    '''
    threading.Thread(target=lambda: playsound.playsound(audio)).start()
counter, c1, c2 = 0, 0, 0
C = 40.1
def move(canvas, child, x_pos, y_pos, speed, timer=float('inf')):
    '''

    :param canvas: the canvas used
    :param child: the image about to be modified
    :param x_pos: the desired x-position of the image
    :param y_pos: the desired y-position of the image
    :param speed: the speed at which the child will travel to the desired co-ordinates
    :param timer: (optional) stops the image moving, once it has moved for a certain amount of time.
    '''
    global begin, c1, c2, option_config, vals, si, C
    tim = 0
    while not ((round(canvas.coords(child)[0]) == x_pos and round(canvas.coords(child)[1]) == y_pos) or tim >= timer):
        tim += 0.02
        canvas.move(child, (x_pos - (canvas.coords(child)[0])) / speed, (y_pos - (canvas.coords(child)[1])) / speed)
        time.sleep(0.01)
    values = [12 if int(option_config[i][2].get()) and int(option_config[i][3].get()) else 1 if int(
        option_config[i][2].get()) else 2 for i in range(7)]
    # 12 represents both characters, 1 represents the first character and 2 represents the second character.
    if speed == C * (700/si):
        time.sleep(0.5)
        for vv in range(7):
            phase(values[vv], vals[vv])
        if c1 == c2:
            phase(12, 'Winner')
        elif c1 > c2:
            phase(1, 'Winner')
        else:
            phase(2, 'Winner')
        time.sleep(1)
        window.destroy()
def phase(n, text):
    global txt, f1, f2, fullf1, fullf2, fullf3, fullf4, counter, c1, c2, color_me, si
    global fighter_canvas
    fighter_canvas.itemconfigure(2, state='hidden')
    fighter_canvas.itemconfigure(1, state='hidden')
    tn = n in range(1, 3)
    counter += 1
    if n == 12:
        c1 += 1
        c2 += 1
    elif n == 1:
        c1 += 1
    else:
        c2 += 1
    fighter_canvas.delete('txt')
    txt = fighter_canvas.create_text(si//2, si//2, text=text, font=('Consolas', 65), fill=color_me, tags='txt')
    if counter % 4 != 0:
        fighter_canvas.moveto(1, si//4, 5000 if counter % 2 == 1 else -5000)
        fighter_canvas.moveto(2, si * 0.75, -5000 if counter % 2 == 1 else 5000)
    else:
        fighter_canvas.moveto(1, si * -2, si//2)
        fighter_canvas.moveto(2, si * 2, si//2)
    fighter_canvas.itemconfigure(1, state='normal')
    fighter_canvas.itemconfigure(2, state='normal')
    threading.Thread(target=lambda: move(fighter_canvas, 1, si // 4, si//2, 6)).start()
    threading.Thread(target=lambda: move(fighter_canvas, 2, si * 0.75, si//2, 6)).start()
    time.sleep(1)
    if n == 12 and not text == 'Winner':
        txt_2 = fighter_canvas.create_text(si//2, 250, text='Tie', font=('Consolas', 65), fill=color_me, tags='txt')
    if text == 'Winner':
        fighter_canvas.delete(txt)
        if not tn:
            txt_2 = fighter_canvas.create_text(si//2, si//2, text=' YOU\nDECIDE', font=('Consolas', 75), fill=color_me,
                                               tags='txt')
        else:
            txt_2 = fighter_canvas.create_text(si//2, si//2, text=chars[n - 1], font=('Consolas', 75), fill=color_me,
                                               tags='txt')
    if not text == 'Winner':
        fighter_canvas.itemconfig(txt, text=f'{c1}-{c2}')
    if tn or counter == 4:
        fighter_canvas.itemconfigure(2 // n, state='hidden')

    if counter == 4:
        if tn:
            fighter_canvas.itemconfig(n, image=fullf1 if n == 1 else fullf2)
            fighter_canvas.moveto(n, 0, 400)
            threading.Thread(target=lambda: move(fighter_canvas, n, si//2, si//2, 6, 1.6)).start()
            time.sleep(0.5)
            fighter_canvas.itemconfig(n, image=fullf3 if n == 1 else fullf4)
            fighter_canvas.moveto(n, 0, -400)
            threading.Thread(target=lambda: move(fighter_canvas, n, si//2, si//2, 6, 1.6)).start()
            time.sleep(0.1)
        else:
            fighter_canvas.itemconfigure(2, state='hidden')
            fighter_canvas.itemconfig(1, image=fullf1)
            fighter_canvas.moveto(1, 0, 400)
            threading.Thread(target=lambda: move(fighter_canvas, 1, si//2, si//2, 13, 1.6)).start()
            time.sleep(0.5)
            fighter_canvas.itemconfig(1, image=fullf4)
            fighter_canvas.moveto(1, 0, -400)
            time.sleep(0.1)
    else:
        if tn:
            fighter_canvas.itemconfig(n, image=fullf1 if n == 1 else fullf2)
            fighter_canvas.moveto(n, 0, si/1.5)
            threading.Thread(target=lambda: move(fighter_canvas, n if tn else 2, si//2, si//2, 15, 1.3)).start()

    if counter == 4:
        time.sleep(0.5)
    else:
        time.sleep(0.9)
    if (tn and not text == 'Winner') or (not tn and text == 'Winner'):
        fighter_canvas.itemconfig(n, image=f1 if n == 1 else f2)
        fighter_canvas.moveto(n, 0 if n == 1 else si//2, 0)
        fighter_canvas.itemconfigure(2 // n, state='normal')
    if not tn and counter == 4:
        fighter_canvas.itemconfig(1, image=f1)
        fighter_canvas.moveto(1, 0, 0)
        fighter_canvas.itemconfig(2, image=f2)
        fighter_canvas.moveto(2, si//2, 0)
        fighter_canvas.itemconfigure(2, state='normal')


chars = []

si = 900
def start():
    global file_list, fighter_canvas, f1, f2, fullf1, fullf2, fullf3, fullf4, chars, color_me, window, vals, si
    a, b = ask_info.get(), ask_info_2.get()

    if a == '':
        a = 'Goku'
    if b == '':
        b = 'Saitama'
    chars = [a, b]
    vals = [option_config[i][1].get() for i in range(7)]
    for q in window.winfo_children():
        if str(q).count('.') > 1:
            for z in q.winfo_children():
                z.destroy()
        q.destroy()

    window.geometry(f'{si}x{si}') # Matches window size according to the si variable

    create_files(si)
    fighter_canvas = Canvas(window, background='black', borderwidth=0, highlightthickness=0)
    fighter_canvas.pack(fill=BOTH, expand=TRUE)
    img1 = fighter_canvas.create_image((si//4), 0, image=f1)
    img2 = fighter_canvas.create_image((si * 0.75), 1000, image=f2)
    txt = fighter_canvas.create_text(0, si//2, text=f'{a} vs {b}', font=('Consolas', 55), fill=color_me, tags='txt')
    threading.Thread(target=lambda: move(fighter_canvas, img1, si//4, si//2, 50)).start()
    threading.Thread(target=lambda: move(fighter_canvas, img2, si * 0.75, si//2, 50)).start()
    threading.Thread(target=lambda: move(fighter_canvas, txt, si // 2, si//2, C * (700/si))).start()
    s.play()

file_list = [None for i in range(6)]
f1, f2, fullf1, fullf2, fullf3, fullf4 = None, None, None, None, None, None # referencing images
t_T_t = []


def select_file(c):
    global file_list, f1, f2, fullf1, fullf2, fullf3, fullf4, color_me, t_T_t
    filetypes = [
        ('Image', '*.png *.jpg')

    ]

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='Downloads',
        filetypes=filetypes)

    if filename != '':
        file_list[c] = filename

        uploaded_msg = customtkinter.CTkLabel(file_upload_grid, text='', width=5, image=imag)
        uploaded_msg.grid(row=c, column=3, padx=20)
        if not None in file_list and color_me != '' and t_T_t:

            info_button.configure(state='normal')


customtkinter.set_appearance_mode('dark')
window = Tk()
window.title('1v1TiktokFightMaker')


def check():
    global file_list, f1, f2, fullf1, fullf2, fullf3, fullf4, color_me, t_T_t
    t_T_t = all([int(option_config[n][2].get()) == 1 or int(option_config[n][3].get()) == 1 for n in range(7)])
    if not None in file_list and color_me != '' and t_T_t:

        info_button.configure(state='normal')

def help_me():
    wow = customtkinter.CTkToplevel(window)
    wow.grab_set()
    wow.geometry('500x500')
    wow.title('Help')
    usage = customtkinter.CTkLabel(wow, text='How to Use', text_font=('Consolas', 30))
    usage.pack()
    help_1 = customtkinter.CTkTextbox(wow, text_font=('Consolas', 12), wrap='word', border_width=2, height=350)
    help_1.pack(pady=15)
    help_1.insert(1.0,' Click on "Upload Image" buttons to upload an image from your computer to use for the app.\n\n '
                      'Click on the "Choose Colour" button to manipulate the colour of the text in the app.\n\n Tick '
                      'the tickboxes to show whether the first or second character is better in a specified ability. '
                      'You can tick for both characters.\n\n Type the names of the characters you want to label on '
                      'the top two input boxes of the project.\n\n Once all of the steps above have been completed, '
                      'the begin button will light up. Click on it to see the results!')
    help_1.configure(state=DISABLED, width=500)
    close = customtkinter.CTkButton(wow, text='Exit', command=lambda: wow.destroy(), text_font=('Consolas', 20))
    close.pack(pady=10, ipady=15)
    wow.mainloop()

window.geometry('1000x600')
window.resizable(False, False)
window.configure(background='gray12')
imag = resizer('img.png', (20, 20))
info_help_frame = customtkinter.CTkFrame(window)
TITLE = customtkinter.CTkLabel(window, text='1v1 Tiktok Fight Maker', text_font=('Consolas', 23))
TITLE.pack(side=TOP)
info_button = customtkinter.CTkButton(info_help_frame, text='Begin', command=start, state='disabled', text_font=('Consolas', 13))
how_to_button = customtkinter.CTkButton(info_help_frame, text='Help', command=help_me, text_font=('Consolas', 13))
step_1 = customtkinter.CTkFrame(window)
step_1.pack(side=LEFT, padx=10, anchor=N, pady=20)

title = customtkinter.CTkLabel(step_1, text='Step 1', text_font=('Consolas', 23, 'bold'))
title.pack()

step_2 = customtkinter.CTkFrame(window)
step_2.pack(side=RIGHT, anchor=NW, pady=20, padx=10)
title_2 = customtkinter.CTkLabel(step_2, text='Step 2', text_font=('Consolas', 23, 'bold'))
title_2.pack()
info_help_frame.pack(ipady=10, pady=250)
how_to_button.pack(side=BOTTOM)
info_button.pack(side=TOP)
option_frame = customtkinter.CTkFrame(step_2)
option_frame.pack()
options = ['Durability', 'Power', 'Hax', 'IQ', 'Battle IQ', 'Agility', 'Experience', 'Persistence', 'Strength',
           'Menacing', 'Vibrant', 'Handsome', 'Beautiful', 'Cute', 'Frightening', 'Cool', 'Overpowered']
option_config = [(customtkinter.CTkLabel(option_frame),
                  customtkinter.CTkComboBox(option_frame, values=options, height=20),
                  customtkinter.CTkCheckBox(option_frame, height=10, width=10, command=check),
                  customtkinter.CTkCheckBox(option_frame, height=10, width=10, command=check)) for wo in range(7)]

for i in range(len(option_config)):
    option_config[i][0].configure(text=f'Ability {i + 1}:')
    option_config[i][0].grid(row=i * 3, column=0, pady=5)
    option_config[i][1].grid(row=i * 3, column=1, padx=25)
    option_config[i][2].grid(row=i * 3 + 1, column=0, pady=5, padx=25)
    option_config[i][3].grid(row=i * 3 + 1, column=1, pady=5, padx=25)
    option_config[i][1].set(options[i])
    option_config[i][2].configure(text='Character 1')
    option_config[i][3].configure(text='Character 2')
vals = [option_config[i][1].get() for i in range(7)]


def pick_color():
    global color_me, file_list, f1, f2, fullf1, fullf2, fullf3, fullf4

    color = colorchooser.askcolor(title="Choose color")
    if not color[0] == None:
        color_me = color[1]
        color_label_2.grid(row=0, column=2, padx=40)
        color_label_2.configure(text=color[1])
        if not None in file_list and color_me != '' and t_T_t:

            info_button.configure(state='normal')


color_me = ''
ask_label, ask_label_2 = customtkinter.CTkLabel(step_1, text='Character 1:'), customtkinter.CTkLabel(step_1,
                                                                                                     text='Character 2:')
ask_label.pack(pady=5)
ask_info, ask_info_2 = customtkinter.CTkEntry(step_1, placeholder_text='Goku'), customtkinter.CTkEntry(step_1,
                                                                                                       placeholder_text='Saitama')
ask_info.pack()
ask_label_2.pack(pady=5)
ask_info_2.pack()
color_frame = customtkinter.CTkFrame(step_1)
color_label_2 = customtkinter.CTkLabel(color_frame, text='', width=5, image=imag)
color_label = customtkinter.CTkLabel(color_frame, text='Text Colour:')

button = customtkinter.CTkButton(color_frame, text='Choose Color', command=pick_color, width=150)
file_upload_grid = customtkinter.CTkFrame(step_1, width=200, height=200)
file_upload_grid.pack(pady=20, )
uploads = [customtkinter.CTkLabel(file_upload_grid, text='Character 1 Image:', name='o') for i in range(6)]
uploads[1].configure(text='Character 2 Image:')
uploads[2].configure(text='Character 1 Alternative #1:')
uploads[3].configure(text='Character 2 Alternative #1:')
uploads[4].configure(text='Character 1 Alternative #2:')
uploads[5].configure(text='Character 2 Alternative #2:')
upload_files = [
    customtkinter.CTkButton(file_upload_grid, text='Upload Image!', command=lambda c=i: select_file(c), width=50,
                            name=str(i)) for i in range(6)]
for q in range(len(uploads)):
    uploads[q].grid(row=q, column=0, padx=20, pady=5)
for t in range(len(upload_files)):
    upload_files[t].grid(row=t, column=1, padx=20, pady=5)
color_frame.pack(pady=10, fill=Y)
color_label.grid(row=0, column=0, padx=10)
button.grid(row=0, column=1, padx=10)
window.mainloop()
