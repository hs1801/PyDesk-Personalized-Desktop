import tkinter as tk
import tkinter.filedialog as fd
from tkinter import messagebox, simpledialog
import os, pickle
from subprocess import run
from threading import Thread
import webbrowser

import otherwin

from PIL import Image, ImageTk


class Desk():
    def __init__(self, master, apps, users, userdict, username):
        for child in master.winfo_children():
            child.destroy()
        self.master = master
        self.apps = apps
        self.users = users
        self.userdict = userdict
        self.username = username

        self.master.attributes('-fullscreen', True)
        self.master.title(f'PyDesk - {username}')
        self.master.h, self.master.w = self.master.winfo_height(), self.master.winfo_width()
        self.master['bg'] = self.userdict[self.username]['bg']
        self.deskno = 0

        self.maindesk = tk.Frame(self.master, bg=self.userdict[self.username]['bg'])
        self.maindesk.grid(row=0, column=0, sticky='news')
        self.deskitems = self.get_deskitems()

        self.move_mode = tk.IntVar(self.master, value=0)
        self.move_from = None
        self.move_to = None

        self.create_maindesk()
        self.create_dock()
        self.set_dialogbox(f'Welcome {username}')
        self.master.equal(self.master)

    def create_maindesk(self):
        self.save_to_DeskData()
        for child in self.maindesk.winfo_children():
            child.destroy()
        self.maindesk['bg'] = self.userdict[self.username]['bg']
        self.master['bg'] = self.userdict[self.username]['bg']
        self.deskitems = self.get_deskitems()
        for row in range(8):
            for col in range(10):
                fname = self.deskitems[(row, col)][1]
                add = self.deskitems[(row, col)][2]
                image = 'images/default.png'
                ext = os.path.splitext(add)[1]
                for app in self.apps:
                    if ext in self.apps[app]['ext']:
                        image = self.apps[app]['image']
                        break
                else:
                    if ext == '.exe':
                        image = 'images/exe.png'
                    elif ext:
                        image = 'images/question.png'
                try:
                    image = Image.open(image).resize((50, 50))
                except:
                    messagebox.showerror('Error', f'File {image} not found.')
                    image = Image.open('images/defapp.png').resize((50,50))
                    self.apps[app]['image'] = os.path.realpath('images/defapp.png')
                image = ImageTk.PhotoImage(image=image)
                but = tk.Button(self.maindesk, relief='flat', text=fname, state=self.deskitems[(row, col)][0], wraplength=int(self.master.w/11),
                                image=image, compound='top', activebackground=self.userdict[self.username]['bg'],
                                bg=self.userdict[self.username]['bg'], height=int(self.master.h/9), width=int(self.master.w/11))

                but.img = image
                but.bind('<Button-1>', lambda event, text=fname, z=self.deskno, x=row, y=col: self.on_single_click(event, text, z, x, y))
                but.bind('<Double-Button-1>', self.on_double_click)
                but.bind('<Button-3>', self.on_right_click)
                but.grid(row=row, column=col)
        self.master.equal(self.maindesk)

    def create_dock(self):
        self.dock = tk.Frame(self.master)
        self.dock.grid(row=0, column=1, rowspan=2, sticky='news')
        self.dockitems = [['images/exit.png', self.on_closing], ['images/add.png', self.addfiles],
            ['images/apps.png', self.app_window], ['images/files.png', self.myfile_window],
            ['images/setting.png', self.setting_win]]
        
        row=0
        for item in self.dockitems:
            img1 = Image.open(item[0]).resize((50, 50))
            img1 = ImageTk.PhotoImage(image=img1)
            butt = tk.Button(self.dock, relief='flat', image=img1, height=self.master.h//6,
                            width=self.master.w//12, command=item[1])
            butt.img = img1
            butt.grid(row=row, column=0)
            row += 1

    def set_dialogbox(self, text):
        self.dialogbox = tk.Frame(self.master, bg=self.userdict[self.username]['bg'])
        self.dialogbox.grid(row=1, column=0, sticky='news')
        self.master.equal(self.master)

        self.dialogtxt = tk.Label(self.dialogbox, text=text, bg=self.userdict[self.username]['bg'])
        self.dialogtxt.grid(row=0, column=1, sticky='we')
        self.dialogbox.columnconfigure(1, weight=1)

        self.next = Image.open('images/arrow.png').resize((20,20))
        self.back = self.next.rotate(180)

        self.next = ImageTk.PhotoImage(image=self.next)
        self.back = ImageTk.PhotoImage(image=self.back)

        tk.Button(self.dialogbox, image=self.back, activebackground=self.userdict[self.username]['bg'],
                                bg=self.userdict[self.username]['bg'], command=lambda: self.change_desk('back')).grid(row=0, column=0)
        tk.Button(self.dialogbox, image=self.next, activebackground=self.userdict[self.username]['bg'],
                                bg=self.userdict[self.username]['bg'], command=lambda: self.change_desk('next')).grid(row=0, column=2)

    def get_deskitems(self):
        deskitems = {}
        for x in self.userdict[self.username]['myfiles']:
            if x[3] != None and x[3][0] == self.deskno:
                # State, Name, Address, DeskFolder
                deskitems[x[3][1:]] = ['active', x[0], x[1], x[2]]
        for i in range(8):
            for j in range(10):
                if (i, j) not in deskitems:
                    # State, Name, Address, DeskFolder
                    deskitems[(i, j)] = ['disabled', '', '', '']
        return deskitems
    def change_desk(self, move):
        if move=='back' and self.deskno!=0:
            self.deskno -= 1
            self.create_maindesk()
            self.set_dialogbox(f'Desk No. {self.deskno}')
        elif move=='next' and self.deskitems != {(i,j):['disabled', '', '', ''] for i in range(8) for j in range(10)}:
            self.deskno += 1
            self.create_maindesk()
            self.set_dialogbox(f'Desk No. {self.deskno}')
        else:
            pass

    def get_empty(self):
        self.filelist = []
        for files in self.userdict[self.username]['myfiles']:
            self.filelist.append(files[3])
        k = self.deskno
        while k >= 0:
            for j in range(10):
                for i in range(8):
                    if (k, i, j) not in self.filelist:
                        return (k, i, j)

    def on_closing(self):
        if not self.move_mode.get():
            yesno = messagebox.askquestion('Exit PyDesk', 'Are you sure to exit PyDesk?')
            if yesno == 'yes':
                self.master.destroy()

    def on_single_click(self, event, text, z, x, y):
        if not self.move_mode.get():
            self.set_dialogbox(text)
        else:
            self.move_to = (z, x, y)
            i, j = -1, -1
            myfiles = self.userdict[self.username]['myfiles']
            for t in range(len(myfiles)):
                coord = myfiles[t][3]
                if coord == self.move_from:
                    i = t
                if coord == self.move_to:
                    j = t
                if i != -1 and j != -1:
                    break
            myfiles[i][3] = self.move_to
            if j != -1:
                myfiles[j][3] = self.move_from

            self.deskno = self.move_from[0]
            if self.get_deskitems() == {(i, j): ['disabled', '', '', ''] for i in range(8) for j in range(10)} :
                for myfile in self.userdict[self.username]['myfiles']:
                    if myfile[3] and myfile[3][0] > self.deskno:
                        myfile[3] = (myfile[3][0]-1, myfile[3][1], myfile[3][2])
            self.deskno = self.move_to[0]
            self.create_maindesk()
            self.set_dialogbox('Move File Successful')
            self.move_mode.set(0)

    def open_with(self, app, add, win=None):
        ext = os.path.splitext(add)[1]
        def_cmd = self.apps[app]['default']
        if def_cmd:
            yesno = messagebox.askquestion('Confirm', f'Do you want to add {ext} to APP Extensions?')
            if yesno == 'yes':
                self.apps[app]['ext'].append(ext)
                self.create_maindesk()
                if win:
                    win.create_tree()
                    
                    win.lift()
            self.run_command(self.apps[app]['filemenu'][def_cmd], app, add)
        else:
            messagebox.showerror('Error', f'No default command for {app}')
    def on_double_click(self, event):
        if self.move_mode.get():
            return
        cord_x, cord_y = event.x_root, event.y_root
        y, x = self.maindesk.location(cord_x, cord_y)

        if self.deskitems[(x,y)][0] == 'active':
            add = self.deskitems[(x,y)][2]
            ext = os.path.splitext(add)[1]
            for app in self.apps:
                if ext in self.apps[app]['ext']:
                    def_cmd = self.apps[app]['default']
                    if def_cmd:
                        cmd = self.apps[app]['filemenu'][def_cmd]
                    else:
                        continue
                    self.run_command(cmd, app, add)
                    break
            else:
                if ext == '.exe':
                    self.run_command(['<file>'], None, add)
                else:
                    messagebox.showerror('Error!!', f'No apps for opening {ext}')

    def get_deskfolders(self):
        folders = []
        for myfile in self.userdict[self.username]['myfiles']:
            deskfolders = myfile[2].split('/')
            for i in range(1, len(deskfolders)+1):
                loc = '/'.join(deskfolders[:i])
                if loc not in folders:
                    folders.append(loc)
        folders.sort()
        return folders

    def on_right_click(self, event):
        if self.move_mode.get():
            return
        cord_x, cord_y = event.x_root, event.y_root
        y, x = self.maindesk.location(cord_x, cord_y)

        if self.deskitems[(x,y)][0] == 'active':
            add = self.deskitems[(x,y)][2]
            ext = os.path.splitext(add)[1]
            self.options = tk.Menu(self.maindesk, tearoff=0)
            name = self.deskitems[(x,y)][1]
            self.options.add_command(label=name)
            self.options.add_separator()
            self.options.add_separator()
            submenu = tk.Menu(self.options, tearoff=0)
            self.options.add_cascade(label='Open With', menu=submenu)
            self.options.add_separator()

            self.options.images = []
            for app in self.apps:
                img = Image.open(self.apps[app]['image']).resize((20,20))
                img = ImageTk.PhotoImage(image=img)
                self.options.images.append(img)

                optiondict = self.apps[app]['filemenu']
                def_cmd = self.apps[app]['default']
                submenu.add_command(label=app, image=img, compound='left', 
                    command=lambda app=app, add=add: self.open_with(app, add))
                if ext in self.apps[app]['ext']:
                    for option in optiondict:
                        self.options.add_command(label=option, image=img, compound='left',
                         command=lambda cmd=optiondict[option], app=app, add=add: self.run_command(cmd, app, add))
                    self.options.add_separator()
            if ext == '.exe':
                image = Image.open('images/exe.png').resize((20,20))
                image = ImageTk.PhotoImage(image=image)
                self.options.images.append(image)
                self.options.add_command(label='Start', image=image, compound='left', command=
                    lambda add=add: self.desk.run_command(['<file>'], None, add))
                self.options.add_separator()

            self.options.add_command(label='Move', command=lambda z=self.deskno, x=x, y=y: self.act_move_file(z, x, y))
            self.options.add_command(label='Delete', command=lambda name=name: self.delete_item(name))
            self.options.tk_popup(cord_x, cord_y)

    def act_move_file(self, z, x, y):
        self.move_mode.set(1)
        self.move_from = (z, x, y)
        self.set_dialogbox('Move Mode ON')

    def delete_item(self, name, win=None):
        yesno = messagebox.askquestion("Confirm Delete", f"Are sure sure you want to delete '{name}'?")
        if yesno == 'yes':
            for item in self.userdict[self.username]['myfiles']:
                if item[0] == name:
                    self.userdict[self.username]['myfiles'].remove(item)
                    if item[3] != None:
                        self.deskno = item[3][0]
                        if self.get_deskitems() == {(i, j): ['disabled', '', '', ''] for i in range(8) for j in range(10)} :
                            for myfile in self.userdict[self.username]['myfiles']:
                                if myfile[3] and myfile[3][0] > item[3][0]:
                                    myfile[3] = (myfile[3][0]-1, myfile[3][1], myfile[3][2])
                    self.create_maindesk()
                    if win:
                        win.create_tree()
                        
                        win.lift()
                    self.save_to_DeskData()

    def run_command(self, cmd, app, add):
        cmd = ' '.join(cmd)
        i = cmd.find('<input>')
        while i != -1:
            enter = simpledialog.askstring(title='Enter Required Input', prompt=cmd)
            if enter != None:
                cmd = cmd.replace('<input>', f'{enter}', 1)
            else:
                return
            i = cmd.find('<input>', i)
        try:
            loc = self.apps[app]['loc']
            cmd = cmd.replace('<app>', f'"{loc}"')
        except:
            pass
        cmd = cmd.replace('<file>', f'"{add}"')
            
        print(cmd)
        Thread(target=lambda:run(cmd)).start()

    def save_to_DeskData(self):
        f = open('data/DeskData.bin', 'wb')
        d = dict(self.userdict)
        cur_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(cur_path)
        d['Guest'] = {'password': '', 'myfiles': [['Single Line Calculator', f'{cur_path}\\Calculator- single-line.py', '', (0, 0, 0)],
                                                  ['Tic-Tac-Toe',
                                                   f'{cur_path}\\Tic-Tac-Toe.py', '', (1, 7, 9)],
                                                  ['Trial',
                                                      f'{cur_path}\\trial.txt', '', (0, 7, 0)]], 'bg': 'orange',
                      'image': f'{cur_path}\\images\\guest.png'}
        savestr = [self.apps, self.users, d]
            
        pickle.dump(savestr, f)
        f.flush()
        f.close()

    def myfile_window(self):
        if not self.move_mode.get():
            self.set_dialogbox('My Files')
            myfile_tk = otherwin.My_File_Win(self, self.userdict, self.username, self.apps)
    def addfiles(self):
        if not self.move_mode.get():
            self.set_dialogbox('Add File')
            add_mod = otherwin.Add_Menu(self, self.apps, self.userdict, self.username)
    def app_window(self):
        if self.move_mode.get():
            return
        if self.username == 'Guest':
            messagebox.showerror('User Error', "'Guest' user cannot modify apps.")
        else:
            self.set_dialogbox('Apps - PyDesk')    
            pyaps = App_Window(self, self.apps)
    def setting_win(self):
        if not self.move_mode.get():
            self.set_dialogbox('Settings')
            settings = otherwin.Settings_Win(self, self.apps, self.userdict, self.username, self.users)

class App_Window(tk.Toplevel):
    def __init__(self, desk, apps):
        tk.Toplevel.__init__(self, master=desk.master)
        self.desk = desk
        self.apps = apps
        self.title('PyDesk - Apps')
        self.geometry("400x400")
        self.attributes('-topmost', 1)
        self.frame = tk.Frame(self)
        self.frame.pack(side='top', expand=True, fill='both')
        
        self.create_objects()

    def create_objects(self):
        self.desk.save_to_DeskData()
        for child in self.frame.winfo_children():
            child.destroy()
        row, col = 0, 0
        self.frame.rowconfigure(row, weight=1)
        self.frame.columnconfigure(col, weight=1)
        for app in self.apps:
            img = Image.open(self.apps[app]['image']).resize((50,50))
            img = ImageTk.PhotoImage(image=img)
            but = tk.Button(self.frame, image=img, text=app, compound='top', relief='flat', command=lambda app=app: self.create_app(app))
            but.img = img
            but.grid(row=row, column=col, sticky='ew')
            col += 1
            if not col % 5:
                col = 0
                row += 1
                self.frame.rowconfigure(row, weight=1)
            self.frame.columnconfigure(col, weight=1)
        img = Image.open('images/add_app.png').resize((50,50))
        img = ImageTk.PhotoImage(image=img)
        but = tk.Button(self.frame, text='Add App', image=img, compound='top', relief='flat', command=self.add_app)
        but.img = img
        but.grid(row=row, column=col, sticky='ew')

    def create_app(self, app):
        self.desk.save_to_DeskData()
        for child in self.frame.winfo_children():
            child.destroy()

        img = Image.open(self.apps[app]['image']).resize((50,50))
        img = ImageTk.PhotoImage(image=img)
        label = tk.Label(self.frame, image=img, text=app, compound='top', relief='flat')
        label.img = img
        label.grid(row=0, column=0, sticky='news')

        self.frame2 = tk.PanedWindow(self.frame)
        self.frame2.grid(row=0, column=1, sticky='news')

        tk.Button(self.frame2, text='Add App Command', command=lambda app=app, ctype='appmenu':
                     self.add_command(app, ctype)).grid(row=0, column=0, sticky='news')
        tk.Button(self.frame2, text='Add File Command', command=lambda app=app, ctype='filemenu':
                     self.add_command(app, ctype)).grid(row=1, column=0, sticky='news')
        tk.Button(self.frame2, text='BACK', command=self.create_objects).grid(row=2, column=0, sticky='news')
        tk.Button(self.frame2, text='DELETE', command=lambda app=app: self.delete_ok(app)).grid(row=2, column=1, sticky='news')
        tk.Button(self.frame2, text='Manage Ext.', command=lambda app=app:self.manage_ext(app)).grid(row=0, column=1, sticky='news')
        tk.Button(self.frame2, text='Modify', command=lambda app=app:self.add_app(app)).grid(row=1, column=1, sticky='news')

        self.app_frame = tk.PanedWindow(self.frame)
        self.app_frame.grid(row=1, column=0, sticky='news', columnspan=2)

        self.file_frame = tk.PanedWindow(self.frame)
        self.file_frame.grid(row=2, column=0, sticky='news', columnspan=2)

        row, col = 0, 0
        for option in self.apps[app]['appmenu']:
            but = tk.Button(self.app_frame, text=option, command= lambda cmd=self.apps[app]['appmenu'][option], app=app:
             self.desk.run_command(cmd, app, None))
            but.bind("<Button-3>", lambda event, app=app, ctype='appmenu', option=option: self.delete_pop(event, app, ctype, option))
            but.grid(row=row, column=col, sticky='ew')
            #but.grid(row=row, column=col)
            col += 1
            if not col % 4:
                col = 0
                row += 1

        row, col = 0, 0
        for option in self.apps[app]['filemenu']:
            but = tk.Button(self.file_frame, text=option)
            but.bind("<Button-3>", lambda event, app=app, ctype='filemenu', option=option: self.delete_pop(event, app, ctype, option))
            but.grid(row=row, column=col, sticky='ew')
            #but.grid(row=row, column=col)
            col += 1
            if not col % 4:
                col = 0
                row += 1

        self.desk.master.equal(self.frame)
        self.desk.master.equal(self.frame2)
        self.desk.master.equal(self.file_frame)
        self.desk.master.equal(self.app_frame)

    def delete_pop(self, event, app, ctype=None, option=None):
        cord_x, cord_y = event.x_root, event.y_root
        self.menu = tk.Menu(self)
        if ctype == 'filemenu':
            self.menu.add_command(label='Set as Default', 
                command= lambda option=option, app=app: self.file_default(option,app))
        self.menu.add_command(label='Delete', command= 
            lambda option=option, app=app, ctype=ctype: self.delete_ok(option=option, app=app, ctype=ctype))
        self.menu.tk_popup(cord_x, cord_y)

    def file_default(self, option, app):
        self.apps[app]['default'] = option
        self.create_app(app)

    def delete_ok(self, app, option=None, ctype=None):
        yesno = messagebox.askquestion('Confirm Delete', 'Are you sure you want to delete?')
        if yesno == 'yes':
            if option:
                del self.apps[app][ctype][option]
                if ctype == 'filemenu' and option == self.apps[app]['default']:
                    for i in self.apps[app][ctype]:
                        self.apps[app]['default'] = i
                        break
                    else:
                        self.apps[app]['default'] = None
                self.create_app(app)
            else:
                del self.apps[app]
                self.create_objects()
                self.desk.create_maindesk()
        

    def add_app(self, app=None):
        self.defapp = os.path.abspath('images/defapp.png')
        self.add_app_win = tk.Toplevel(self)
        self.add_app_win.attributes('-topmost', True)
        tk.Label(self.add_app_win, text='App Name\n(or Alias name)').grid(row=0,column=0)
        tk.Label(self.add_app_win, text='App Location\n(write only app name if added to PATH)').grid(row=1,column=0)
        tk.Label(self.add_app_win, text='App Icon').grid(row=2,column=0)

        e1 = tk.Entry(self.add_app_win, width=30)
        e2 = tk.Entry(self.add_app_win, width=30)
        e3 = tk.Entry(self.add_app_win, width=30)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        e3.grid(row=2, column=1)
        if app:
            e1.insert(0, app)
            e2.insert(0, self.apps[app]['loc'])
            e3.insert(0, self.apps[app]['image'])
        else:
            e3.insert(0, self.defapp)

        tk.Button(self.add_app_win, text='Browse', command= lambda win=self, entry=e2, entry2=e1: self.desk.master.browse_file(win=win, entry=entry, entry2=entry2)).grid(row=1, column=2)
        tk.Button(self.add_app_win, text='Browse', command= lambda win=self, entry=e3: self.desk.master.browse_file(win=win, entry=entry)).grid(row=2, column=2)
        tk.Button(self.add_app_win, text='Look for app icon online..', relief='flat', foreground='blue', command=lambda name=e1:
            webbrowser.open('google.com/images?q='+name.get().replace(' ', '+')+'+icon')).grid(row=3, column=0)
        tk.Button(self.add_app_win, text=['Add App' if not app else 'Modify'][0], command= lambda win=self.add_app_win, e1=e1, e2=e2, e3=e3, app=app: self.check_new(win, e1, e2, e3, app)).grid(row=4,column=1)
    
    def browse_exe(self, e1, e2):
        exe = fd.askopenfilename()
        name = os.path.splitext(os.path.basename(exe))[0]
        e1.delete(0, len(e1.get()))
        e2.delete(0, len(e2.get()))
        e1.insert(0, name)
        e2.insert(0, exe)

    def browse_img(self, e3):
        png = fd.askopenfilename()
        e3.delete(0, len(e3.get()))
        e3.insert(0, png)

    def check_new(self, win,  e1, e2, e3, app):
        if e1.get() and os.path.isfile(e3.get()):
            if not app:
                self.apps[e1.get()] = {'ext': [], 'loc': e2.get(), 'appmenu': {'Open':['<app>']}, 'filemenu': {'Open':['<app>', '<file>']}, 'image': e3.get(), 'default':'Open'}
                self.create_objects()
            else:
                self.apps[e1.get()] = dict(self.apps[app])
                if e1.get() != app:
                    del self.apps[app]
                self.apps[e1.get()]['loc'] = e2.get()
                self.apps[e1.get()]['pic'] = e3.get()
                self.create_app(e1.get())
            win.destroy()
    
    def add_command(self, app, ctype):
        self.cmd_win = tk.Toplevel(self)
        self.cmd_win.attributes('-topmost', True)
        tk.Label(self.cmd_win, text='Command Name').grid(row=0,column=0)
        tk.Label(self.cmd_win, text='CMD Command').grid(row=1,column=0)
        tk.Label(self.cmd_win, text='app_name - <app>,   filename - <file>,    user_input - <input>').grid(row=2, column=0, columnspan=2)
        tk.Button(self.cmd_win, text='Look online for command line options..', relief='flat', foreground='blue', command=lambda name=app:
            webbrowser.open('google.com/search?q='+name.replace(' ', '+')+'+command+line+options')).grid(row=3, column=0)

        e1 = tk.Entry(self.cmd_win, width=30)
        e2 = tk.Entry(self.cmd_win, width=30)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        tk.Button(self.cmd_win, text='Add Command', command= lambda win=self.cmd_win, e1=e1, e2=e2, app=app, ctype=ctype: 
                    self.save_cmd(win, e1, e2, app, ctype)).grid(row=3,column=1)

    def save_cmd(self, win, e1, e2, app, ctype):
        if e1.get() and e1.get() not in self.apps[app][ctype]:
            self.apps[app][ctype][e1.get()] = e2.get().split()
            if ctype == 'filemenu' and len(self.apps[app]['filemenu']) == 1:
                self.apps[app]['default'] = e1.get()
            win.destroy()
            self.create_app(app)
            
    def manage_ext(self, app):
        self.manage_win = tk.Toplevel(self)
        e1 = tk.Entry(self.manage_win, width=40)
        e1.grid(row=0)

        self.manage_win.title(f'Manage Extensions - {app}')
        enter = str(self.apps[app]['ext'])
        e1.insert(0, enter)
  
        tk.Button(self.manage_win, text='SAVE', command=
            lambda win=self.manage_win, app=app, entry=e1: self.save_ext(win, app, entry)).grid(row=1)
    def save_ext(self, win, app, entry):
        text = entry.get()
        text = eval(text)
        if type(text) == list:
            self.apps[app]['ext'] = text
            self.create_app(app)
            win.destroy()
            self.desk.create_maindesk()
    

            
