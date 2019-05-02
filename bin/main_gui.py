from tkinter import *
from tkinter import ttk, messagebox

from bin.formats.normal.match_up import MatchUp
from bin.main_menu_gui import MainMenu
from bin.formats.ranked.ranked_match import RankedMatch, Match
from bin.formats.ranked.ranked_member import RankedMember, Member


class MainGUI:

    def __init__(self):
        self.main = Tk()
        self.main.title("Magic")
        self.title = Label(self.main, text="This is out label!")
        self.main.geometry("{}x{}".format(320, 320))
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
        self.button.pack(side="top", pady=5, padx=8)

        self.button1 = Button(self.button_frame, text="Remove Player", width=12, command=self.remove_player)
        self.button1.pack(side="top", pady=5, padx=8)

        self.button2 = Button(self.button_frame, text="Match Make", width=12, command=self.match_make_command)
        self.button2.pack(side="top", pady=5, padx=8)

        self.radio_frame = Frame(self.button_frame)
        self.radio_frame.pack(side="top")

        modes = [
            ("R", "Ranked"),
            ("N", "Normal"),
            ("C", "Commander"),
        ]

        self.format = StringVar()
        self.format.set("L")  # initialize

        for text, mode in modes:
            self.b = Radiobutton(self.radio_frame, text=text,
                                 variable=self.format, value=mode, indicatoron=0, width=3)
            self.b.pack(anchor=W, side="right")

        self.info_txt = StringVar()

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
        player = self.main_menu.current_players[self.roster_list.curselection()[0]]
        answer = messagebox.askyesno("Removing Player:",
                                     f"Are you sure you want to remove {player.name} from the roster?")
        if answer:
            self.roster_list.delete(self.roster_list.curselection())
            self.main_menu.current_players.remove(player)

    def match_make_command(self, *args):
        format = self.format.get()
        if format == "Normal":
            match_type = Match
            member_type = Member
        elif format == "Ranked":
            match_type = RankedMatch
            member_type = RankedMember
        else:
            match_type = Match
            member_type = Member

        if self.main_menu.current_match.round_number == 0:
            self.main_menu.convert_current_players(member_type)

        self.main_menu.current_match.re_rank(self.main_menu.current_players)
        self.main_menu.current_match = match_type(self.main_menu.current_players,
                                                  self.main_menu.current_match.round_number + 1)
        frame = self.add_notebook(f"Round #{self.main_menu.current_match.round_number}")

        def remake():
            txt.delete(0, 'end')
            txt1.delete(0, 'end')
            txt2.delete(0, 'end')
            for match in self.main_menu.current_match.matches:
                txt.insert('end', match.player1.name)
                txt1.insert('end', " VS ")
                txt2.insert('end', match.player2.name)

        def remove():
            if txt.curselection():
                player = self.main_menu.current_match.matches[txt.curselection()[0]][0]
                match = self.main_menu.current_match.matches[txt.curselection()[0]]
            else:
                player = self.main_menu.current_match.matches[txt2.curselection()[0]][1]
                match = self.main_menu.current_match.matches[txt2.curselection()[0]]

            answer = messagebox.askyesno("Removing Player:",
                                         f"Are you sure you want to remove {player.name} from the roster?")
            if answer:
                self.main_menu.current_players.remove(player)
                self.main_menu.current_match.matches.remove(match)
                self.update_roster()
                remake()

        def conclude():
            if txt.curselection():
                self.main_menu.declare((txt.curselection()[0], -1))
            else:
                self.main_menu.declare((-1, txt2.curselection()[0]))

        def manual():

            def manual_command():
                player1 = next(player for player in self.main_menu.current_players
                               if player.name == v.get())
                player2 = next(player for player in self.main_menu.current_players
                               if player.name == v1.get())

                self.main_menu.current_match.matches.append(MatchUp(player1, player2))
                popup.destroy()
                remake()

            if len([player.name for player in self.main_menu.current_players
                                       if player not in self.main_menu.current_match]) < 2:
                messagebox.showerror("Error", "Not Enough non-Matched players to Manually Match")
                return

            popup = Toplevel()
            popup.title("Adding Players")
            popup.geometry("280x140")

            v = StringVar()
            v.set("Player 1")
            v1 = StringVar()
            v1.set("Player 2")

            w = OptionMenu(popup, v, *[player.name for player in self.main_menu.current_players
                                       if player not in self.main_menu.current_match])
            w1 = OptionMenu(popup, v1, *[player.name for player in self.main_menu.current_players
                                         if player not in self.main_menu.current_match])
            w.pack()
            w1.pack()

            createbut = Button(popup, text="Create Match",
                          command=manual_command)
            createbut.pack()

        buttonframe = Frame(frame)
        buttonframe.pack(side="left", padx=5, pady=5, anchor=N)

        but1 = Button(buttonframe, text="Conclude",
                      command=conclude)
        but1.pack(pady=5)

        but2 = Button(buttonframe, text="Remove", command=remove)
        but2.pack(pady=5)

        but3 = Button(buttonframe, text="Manual", command=manual)
        but3.pack(pady=5)

        txt = Listbox(frame, width=16, height=15)
        txt.bind("<Double-Button-1>", lambda e: conclude())
        txt.pack(side="left")
        txt1 = Listbox(frame, width=4, height=15, relief=FLAT)
        txt1.pack(side="left")
        txt2 = Listbox(frame, width=16, height=15)
        txt2.bind("<Double-Button-1>", lambda e: conclude())
        txt2.pack(side="left")

        remake()

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
