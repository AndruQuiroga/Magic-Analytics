import datetime
import os
from tkinter import *
from tkinter import ttk, messagebox
from bin import main_menu_gui
from bin.main_menu_gui import MainMenu
from bin.normal.match import Match


class MainGUI:

    def __init__(self):
        self.main = Tk()
        self.main.title("Magic")
        self.title = Label(self.main, text="This is out label!")
        self.main.geometry("{}x{}".format(560, 360))
        self.main.configure(background='white')

        self.n = ttk.Notebook(self.main)
        self.f1 = ttk.Frame(self.n)
        self.f2 = ttk.Frame(self.n)
        self.n.add(self.f1, text=f"{'CLI':^10}")
        self.n.add(self.f2, text='Roster')
        self.n.pack(fill=BOTH, expand=True)

        self.log = Text(self.f1, state='disabled', width=68, height=17, wrap='none')
        self.log.grid(row=0, column=0, sticky='N', padx=5, pady=5)

        self.cli_entry = Entry(self.f1, width=68)
        # self.cli_entry.bind("<Return>", self.run_command)
        self.cli_entry.grid(row=2)

        self.button_frame = Frame(self.f2)
        self.button_frame.pack(side="right", anchor="ne")

        self.roster_list = Listbox(self.button_frame, width=30, height=15)
        self.roster_list.pack(side="right", pady=5, padx=5)

        self.button = Button(self.button_frame, text="Add Player", width=12, command=self.add_player)
        self.button.pack(side="top", pady=5, padx=5)

        self.button1 = Button(self.button_frame, text="Remove Player", width=12, command=self.remove_player)
        self.button1.pack(side="top")

        self.button2 = Button(self.button_frame, text="Match Make", width=12, command=self.match_make_command)
        self.button2.pack(side="top")

        self.info_txt = StringVar()  # todo move

        self.main_menu = MainMenu()
        self.update_roster()

    def run(self):
        self.main.mainloop()

    def add_player(self):
        popup = Toplevel()
        popup.title("Adding Players")
        popup.geometry("280x80")

        self.info_txt.set("")

        info = Label(popup, textvariable=self.info_txt)
        info.pack(pady=5, padx=5)

        frame = Frame(popup)
        frame.pack(pady=5, padx=5)

        directions = Label(frame, text="Scan ID: ")
        directions.pack(side="left")

        global put
        put = Entry(frame, width=30)
        put.bind("<Return>", self.add_player_command)
        put.pack(side="left", fill="x")

    def add_player_command(self, *args):
        self.main_menu.add_player(self.info_txt, put.get())
        put.delete(0, 'end')

    def remove_player(self):
        # popup = Toplevel()
        # popup.title("Removing Player")
        # popup.geometry("280x80")
        #
        # self.info_txt.set("")
        #
        # info = Label(popup, textvariable=self.info_txt)
        # info.pack(pady=5, padx=5)
        #
        # frame = Frame(popup)
        # frame.pack(pady=5, padx=5)
        #
        # directions = Label(frame, text="Player Name: ")
        # directions.pack(side="left")
        #
        # global put
        # put = Entry(frame, width=30)
        # put.bind("<Return>", self.remove_player_command)
        # put.pack(side="left", fill="x")

        player = self.main_menu.current_players[self.roster_list.curselection()[0]]
        answer = messagebox.askyesno("Removing Player:",
                                     f"Are you sure you want to remove {player.name} from the roster?")
        if answer:
            self.roster_list.delete(self.roster_list.curselection())
            self.main_menu.current_players.remove(player)




    # def remove_player_command(self, *args):
    #     self.main_menu.remove_player(self.info_txt, put.get())
    #     put.delete(0, 'end')
    #     self.update_roster()

    def match_make(self):
        popup = Toplevel()
        popup.title("Match Make")
        popup.geometry("280x80")

        self.info_txt.set("")

        info = Label(popup, textvariable=self.info_txt)
        info.pack(pady=5, padx=5)

        frame = Frame(popup)
        frame.pack(pady=5, padx=5)

        directions = Label(frame, text="Player Name: ")
        directions.pack(side="left")

        global put
        put = Listbox(frame, width=30)
        put.pack(side="left", fill="x")

        # for item in ["one", "two", "three", "four"]:
        #     put.insert(END, item)
        #
        # items = map(int, put.curselection())
        # for item in items:
        #     print(item)
        #
        # b = Button(frame, text="Delete",
        #            command=lambda put=put: put.delete(ANCHOR))
        # b.pack()

    def match_make_command(self, *args):
        self.main_menu.current_match = Match(self.main_menu.current_players,
                                       self.main_menu.current_match.round_number + 1)
        frame = self.add_notebook(f"Round #{self.main_menu.current_match.round_number}")

        txt = Listbox(frame, width=16)
        txt.bind("<Double-Button-1>", lambda e: self.main_menu.declare((txt.curselection()[0], -1)))
        txt.pack(side="left", fill="both")
        txt1 = Listbox(frame, width=4, relief=FLAT)
        txt1.pack(side="left", fill="both")
        txt2 = Listbox(frame, width=16)
        txt2.bind("<Double-Button-1>", lambda e: self.main_menu.declare((-1, txt2.curselection()[0])))
        txt2.pack(side="left", fill="both")

        for match in self.main_menu.current_match.matches:
            txt.insert('end', match.player1.name)
            txt1.insert('end', " VS ")
            txt2.insert('end', match.player2.name)


    def add_notebook(self, name):
        frame = Frame(self.n)
        self.n.add(frame, text=name)
        self.n.pack(fill=BOTH, expand=True)
        return frame

    def remove_notebook(self, tabid):
        self.n.forget(tabid)

    def update_roster(self):
        self.roster_list.delete(0, 'end')
        for player in self.main_menu.current_players:
            self.roster_list.insert('end', player.name)

    def write_to_log(self, msg):  # tk_docs
        numlines = self.log.index('end - 1 line').split('.')[0]
        self.log['state'] = 'normal'
        if numlines == 24:
            self.log.delete(1.0, 2.0)
        if self.log.index('end-1c') != '1.0':
            self.log.insert('end', '\n')
        self.log.insert('end', msg)
        self.log['state'] = 'disabled'


if __name__ == '__main__':
    gui = MainGUI()
    gui.run()
