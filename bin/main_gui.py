from tkinter import *
from tkinter import ttk
from bin import main_menu_gui


class MainGUI:

    def __init__(self):
        self.main = Tk()
        self.main.title("Magic")
        self.title = Label(self.main, text="This is out label!")
        self.main.geometry("{}x{}".format(560, 360))
        self.main.configure(background='white')

        rows = 0
        while rows < 20:
            self.main.rowconfigure(rows, weight=1)
            self.main.columnconfigure(rows, weight=1)
            rows += 1

        n = ttk.Notebook(self.main)
        self.f1 = ttk.Frame(n)
        self.f2 = ttk.Frame(n)
        n.add(self.f1, text=f"{'CLI':^10}")
        n.add(self.f2, text='Roster')
        n.pack(fill=BOTH, expand=True)

        self.log = Text(self.f1, state='disabled', width=68, height=17, wrap='none')
        self.log.grid(row=0, column=0, sticky='N', padx=5, pady=5)

        self.cli_entry = Entry(self.f1, width=68)
        self.cli_entry.bind("<Return>", self.run_command)
        self.cli_entry.grid(row=2)

        self.roster = StringVar()
        self.roster.set("Testing")

        self.roster_list = Label(self.f2, textvariable=self.roster, wraplength=300, bd=100)
        self.roster_list.grid(row=1, columnspan=3)

    def run(self):
        self.main.mainloop()

    def run_command(self, *args):
        main_menu_gui.main_menu(str(self.cli_entry.get()))
        self.cli_entry.delete(0, END)

    def write_to_log(self, msg):   # tkdocs
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
    main_menu_gui.pre_main(gui)
    gui.run()

