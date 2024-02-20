import tkinter as tk
import tkinter.filedialog as fd
import os
import pickle
import login


class App(tk.Tk):
    def __init__(self, users, userdict, apps):
        self.users = users
        self.userdict = userdict
        self.apps = apps
        self.cur_path = os.path.dirname(os.path.abspath(__file__))

        tk.Tk.__init__(self)
        self.resizable(0, 0)
        self.login = login.Login(
            self, self.users, self.userdict, self.apps)
        self.mainloop()

    def equal(self, widget):
        y, x = widget.grid_size()
        for i in range(x):
            widget.rowconfigure(i, weight=1)
        for j in range(y):
            widget.columnconfigure(j, weight=1)

    def browse_file(self, win, entry, entry2=None, filetypes=None):
        address = fd.askopenfilename()
        if address:
            entry.delete(0, len(entry.get()))
            entry.insert(0, address)
            if entry2:
                name = os.path.splitext(os.path.basename(address))[0]
                entry2.delete(0, len(entry2.get()))
                entry2.insert(0, name)
        win.lift()


if __name__ == '__main__':
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path)  # Opening path in cmd line

        f = open('data/DeskData.bin', 'rb')
        loadstr = pickle.load(f)
        apps, users, userdict = loadstr[0], loadstr[1], loadstr[2]
    except:
        apps, users, userdict = None, None, None
    pydesk = App(users, userdict, apps)
