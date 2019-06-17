from tkinter import *
from tkinter import ttk, messagebox
from bin.main_menu import MainMenu


def main():
    global mm
    global n

    gui = Tk()
    gui.title("Magic")
    gui.geometry("{}x{}".format(320, 320))

    n = ttk.Notebook(gui)
    mm = ttk.Frame(n)
    n.add(mm, text='Roster')
    n.pack(fill=BOTH, expand=True)


    settings_menu()
    gui.mainloop()


def settings_menu():
    global format

    popup = Toplevel()
    popup.title("Adding Players")

    f1 = Frame(popup)
    f1.pack(side="top")

    info = Label(f1, text="Select Format")
    info.pack(side="left", pady=5, padx=5)

    radio_frame = Frame(f1)
    radio_frame.pack(side="left")

    modes = [
        ("Ranked", "Ranked"),
        ("Normal", "Normal"),
        ("Commander", "Commander"),
    ]

    format = StringVar()
    format.set("L")  # initialize

    for text, mode in modes:
        b = Radiobutton(radio_frame, text=text,
                        variable=format, value=mode, indicatoron=0, width=12)
        b.pack(anchor=W, side="right")

    done_button = Button(popup, text="Finish", width=12, command=lambda: make_mm(popup))
    done_button.pack(side="top", pady=5, padx=8)


def make_mm(settings=None):
    global main_menu
    global roster_list
    global format

    if settings:
        settings.destroy()

    main_menu = MainMenu(format.get())

    button_frame = Frame(mm)
    button_frame.pack(side="right", anchor="ne")

    roster_list = Listbox(button_frame, width=30, height=15)
    roster_list.pack(side="right", pady=5, padx=5)

    button = Button(button_frame, text="Add Player", width=12, command=add_player)
    button.pack(side="top", pady=5, padx=8)

    button1 = Button(button_frame, text="Remove Player", width=12, command=remove_player)
    button1.pack(side="top", pady=5, padx=8)

    button2 = Button(button_frame, text="Match Make", width=12, command=match_make)
    button2.pack(side="top", pady=5, padx=8)

    update_roster()


def add_notebook(name):
    frame = Frame(n)
    n.add(frame, text=name)
    n.pack(fill=BOTH, expand=True)
    return frame


def update_roster():
    roster_list.delete(0, 'end')
    for player in main_menu.current_players:
        roster_list.insert('end', player.name)


def add_player():
    popup = Toplevel()
    popup.title("Adding Players")
    popup.geometry("280x80")

    info_txt = StringVar()
    info_txt.set("")

    info = Label(popup, textvariable=info_txt)
    info.pack(pady=5, padx=5)

    frame = Frame(popup)
    frame.pack(pady=5, padx=5)

    directions = Label(frame, text="Scan ID: ")
    directions.pack(side="left")

    def command(e):
        main_menu.add_player(info_txt, put)
        update_roster()

    put = Entry(frame, width=30)
    put.bind("<Return>", command)
    put.pack(side="left", fill="x")


def remove_player():
    player = main_menu.current_players[roster_list.curselection()[0]]
    answer = messagebox.askyesno("Removing Player:",
                                 f"Are you sure you want to remove {player.name} from the roster?")
    if answer:
        main_menu.current_players.remove(player)
        update_roster()


def match_make():
    main_menu.make_match()
    frame = add_notebook(f"Round #{main_menu.current_match.round_number}")

    def remake():
        txt.delete(0, 'end')
        txt1.delete(0, 'end')
        txt2.delete(0, 'end')
        for match in main_menu.current_match.match_ups:
            txt.insert('end', match.player1.name)
            txt1.insert('end', " VS ")
            txt2.insert('end', match.player2.name)

    def conclude():

        if txt.curselection():
            match_up = main_menu.current_match.match_ups[txt.curselection()[0]]
            winner = match_up[1]
            loser = match_up[0]
        else:
            match_up = main_menu.current_match.match_ups[txt2.curselection()[0]]
            winner = match_up[1]
            loser = match_up[0]

        if match_up.match_concluded:
            messagebox.showerror("Error", str(match_up))
            return

        answer = messagebox.askyesno("Declaring Winner:", f"Are you sure {winner.name} beat {loser.name}?")
        if answer:
            match_up.conclude_match(winner)

    def remove():
        if txt.curselection():
            match_up = main_menu.current_match.match_ups[txt.curselection()[0]]
            player = match_up[0]
        else:
            match_up = main_menu.current_match.match_ups[txt2.curselection()[0]]
            player = match_up[1]

        answer = messagebox.askyesno("Dropping Player:",
                                     f"Are you sure you want to drop {player.name} from the roster?")
        if answer:
            main_menu.current_players.remove(player)
            main_menu.current_match.match_ups.remove(match_up)
            update_roster()
            remake()

    buttonframe = Frame(frame)
    buttonframe.pack(side="left", padx=5, pady=5, anchor=N)

    but1 = Button(buttonframe, text="Conclude",
                  command=conclude)
    but1.pack(pady=5)

    but2 = Button(buttonframe, text="Drop", command=remove)
    but2.pack(pady=5)

    # but3 = Button(buttonframe, text="Manual", command=manual)
    # but3.pack(pady=5)

    txt = Listbox(frame, width=16, height=15)
    txt.bind("<Double-Button-1>", lambda e: conclude())
    txt.pack(side="left")
    txt1 = Listbox(frame, width=4, height=15, relief=FLAT)
    txt1.pack(side="left")
    txt2 = Listbox(frame, width=16, height=15)
    txt2.bind("<Double-Button-1>", lambda e: conclude())
    txt2.pack(side="left")

    remake()


if __name__ == '__main__':
    main()
