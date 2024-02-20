import os
import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog as fd
try:
    from PIL import Image, ImageTk
except:
    os.system('pip install --user pillow')
    from PIL import Image, ImageTk
import userdesk


class Login():
    def __init__(self, master, users, userdict, apps):
        self.apps = apps
        self.users = users
        self.userdict = userdict
        self.master = master
        self.userpage = 0

        self.path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.path)  # Opening path in cmd line

        if not self.users or (self.users and len(self.users)==1):
            self.create_user('Welcome to PyDesk')
        else:
            self.create_frames()

    def create_frames(self):
        for child in self.master.winfo_children():
            child.destroy()

        self.master['bg'] = 'orange'
        self.master.attributes("-fullscreen", False)
        self.master.title('PyDesk - User Login')
        self.master.unbind('<Return>')

        self.logo = tk.PhotoImage(file='images/intro.png')
        self.label = tk.Label(self.master, image=self.logo)
        self.label.grid(row=0, column=0, rowspan=3, sticky='news')

        self.admin_frame = tk.Frame(self.master, bg='orange')
        self.admin_frame.grid(row=0, column=1, sticky='news')

        try:
            self.admin_pic = Image.open(self.userdict[self.users[1]]['image']).resize(
            (100, 100), Image.ANTIALIAS)
        except:
            messagebox.showerror('Error', f"File {self.userdict[self.users[1]]['image']} not found !!")
            self.admin_pic = Image.open('images/guest.png').resize(
            (100, 100), Image.ANTIALIAS)
        self.admin_pic = ImageTk.PhotoImage(image=self.admin_pic)

        self.admin = tk.Button(self.admin_frame, relief='flat', image=self.admin_pic, anchor='w',
                               text=self.users[1], bg='orange', compound='top', command=lambda: self.login(self.users[1]))
        self.admin.grid(row=0, column=0, rowspan=3, sticky='news')

        self.add_img = Image.open('images/add.png').resize(
            (50, 50))
        self.add_img = ImageTk.PhotoImage(image=self.add_img)

        self.guest_img = Image.open(self.userdict['Guest']['image']).resize(
            (50, 50))
        self.guest_img = ImageTk.PhotoImage(image=self.guest_img)

        self.exit_img = Image.open('images/exit.png').resize(
            (50, 50))
        self.exit_img = ImageTk.PhotoImage(image=self.exit_img)

        self.add_user = tk.Button(self.admin_frame, relief='flat', image=self.add_img, bg='orange', anchor='w',
                                  text='Add User', compound='left', command=lambda: self.create_user('Create New User..'))
        self.add_user.grid(row=0, column=1, sticky='news')

        self.guest_log = tk.Button(self.admin_frame, relief='flat', image=self.guest_img, bg='orange', anchor='w',
                                   text='Guest', compound='left', command=lambda: self.login('Guest'))
        self.guest_log.grid(row=1, column=1, sticky='news')

        self.quit_but = tk.Button(self.admin_frame, relief='flat', image=self.exit_img, bg='orange', anchor='w',
                                  text='Exit', compound='left', command=self.master.destroy)
        self.quit_but.grid(row=2, column=1, sticky='news')

        self.create_user_frame()
        self.master.equal(self.admin_frame)
        self.master.equal(self.master)


    def create_user_frame(self):
        self.user_frame = tk.Frame(self.master, bg='orange')
        self.user_frame.grid(row=1, column=1, sticky='news')

        self.usersnow = self.users[2:][5*(self.userpage) : 5*(self.userpage + 2)]

        if len(self.users) > 12:
            self.above = Image.open('images/arrow.png').resize((20,20))
            self.above = self.above.rotate(90)

            self.below = self.above.rotate(180)

            self.above = ImageTk.PhotoImage(image=self.above)
            self.below = ImageTk.PhotoImage(image=self.below)

            tk.Button(self.user_frame, bg='orange', image=self.above, command=lambda move='up':self.move_frame(move)).grid(row=0, column=2)
            tk.Button(self.user_frame, bg='orange', image=self.below, command=lambda move='down':self.move_frame(move)).grid(row=3, column=2)

        blank = Image.open('images/default.png').resize((50,50))
        blank = ImageTk.PhotoImage(image=blank)

        for i in range(10):
            try:
                img = Image.open(self.userdict[self.usersnow[i]]['image']).resize((50,50))
                img = ImageTk.PhotoImage(image=img)
                but = tk.Button(self.user_frame, text= self.usersnow[i], image=img, bg='orange', relief='flat', compound='top',
                command=lambda user=self.usersnow[i]: self.login(user), padx=10)
                but.img = img
                but.grid(row=(i//5)+1, column=i%5)
            except:
                but = tk.Label(self.user_frame, padx=10, image=blank, bg='orange', text=' ', compound='top')
                but.img = blank
                but.grid(row=(i//5)+1, column=i%5)

    def move_frame(self, move):
        if move == 'up' and self.userpage:
            self.userpage -= 1
            self.create_user_frame()
        elif move == 'down' and self.users[2:][5*(self.userpage + 1) : 5*(self.userpage + 3)] != []:
            self.userpage += 1
            self.create_user_frame()

    def login(self, username):
        self.cur_pass = self.userdict[username]['password']
        if self.cur_pass == '':
            userdesk.Desk(self.master, self.apps, self.users,
                          self.userdict, username)
        else:
            self.pass_frame = tk.Frame(self.master, bg='orange')
            self.pass_frame.grid(row=2, column=1, sticky='news')
            self.next_img = Image.open('images/arrow.png').resize(
                (50, 50))
            self.next_img = ImageTk.PhotoImage(image=self.next_img)

            tk.Label(self.pass_frame, bg='orange', text=username).grid(
                row=0, column=0, columnspan=3, sticky='news')
            tk.Label(self.pass_frame, bg='orange', text='Enter Password: ').grid(
                row=1, column=0, sticky='news')

            self.pwd_entry = tk.Entry(self.pass_frame, width=30, show='*')
            self.pwd_submit = tk.Button(self.pass_frame, relief='flat', image=self.next_img,
                                        bg='orange', command=lambda: self.check_login(None, username, self.cur_pass, self.pwd_entry.get()))
            self.master.bind('<Return>', lambda event: self.check_login(event, username, self.cur_pass, self.pwd_entry.get()))
            self.pwd_entry.grid(row=1, column=1, sticky='news')
            self.pwd_submit.grid(row=1, column=2, sticky='news')

            self.master.equal(self.master)
            for i in range(3):
                self.pass_frame.columnconfigure(i, weight=1)
            #self.master.equal(self.pass_frame)

    def check_login(self, event, username, correct_pass, entered_pass):
        if entered_pass == correct_pass:
            self.master.unbind('<Return>')
            userdesk.Desk(self.master, self.apps, self.users,
                          self.userdict, username)
        else:
            messagebox.showerror(
                'Login Error', f"Invalid Password for user '{username}'")

    def save_new_user(self, event, name, pwd, cpwd, img):
        name = name.get()
        pwd = pwd.get()
        cpwd = cpwd.get()
        img = img.get()
        if name and name != 'Guest' and pwd == cpwd and os.path.isfile(img) and os.path.splitext(img)[1] == '.png':
            if not self.users:
                self.apps = {'Python': {'ext': ['.py', '.pyw'], 'loc': 'pythonw', 'appmenu': {'New Shell': ['<app>', '-m', 'idlelib'], 'New Script': ['<app>', '-m', 'idlelib', 'untitled']}, 'default':'Open',
                                        'filemenu': {'Open': ['<app>', '-m', 'idlelib', '-r', '<file>'], 'Edit': ['<app>', '-m', 'idlelib', '<file>']},
                                        'image': f'{self.path}\\idle.png'},
                            'WordPad': {'ext': ['.txt', '.doc', '.py', '.docx'], 'loc': 'write', 'appmenu': {'create new': ['<app>']},
                                        'filemenu': {'Open': ['<app>', '<file>'], 'Print': ['<app>', '/p', '<file>']},
                                        'image': f'{self.path}\\wordpad.png', 'default':'Open'}}
                self.users = ['Guest', name]
                self.userdict = {'Guest': {'password': '', 'myfiles': [['Single Line Calculator', f'{self.path}\\Calculator- single-line.py', '/FOLDER1', (0, 0, 0)],
                                                                    ['Tic-Tac-Toe',
                                                                        f'{self.path}\\Tic-Tac-Toe.py', '/FOLDER1/FOLDER2', (1, 7, 9)],
                                                                    ['readme',
                                                                        f'{self.path}\\readme.txt', '', (0, 7, 0)]], 'bg': 'orange',
                                        'image': f'{self.path}\\images\\guest.png'}}
                self.userdict[name] = {'password': pwd, 'image': img, 'myfiles': self.userdict['Guest']['myfiles'], 'bg':'orange'}
                self.create_frames()
            else:
                if self.users and name not in self.users:
                    self.users.append(name)
                    self.userdict[name] = {'password': pwd, 'myfiles': self.userdict['Guest']['myfiles'], 'bg': 'orange',
                                            'image': img}
                    self.create_frames()
                else:
                    messagebox.showerror('PyDesk- Create User', 'User already exists')
        else:
            messagebox.showerror('PyDesk- Create User', 'Invalid set of entries')

    def create_user(self, title):
        for child in self.master.winfo_children():
            child.destroy()
        self.master.title(title)
        self.master['bg'] = 'SystemButtonFace'
        self.master.resizable(0, 0)
        tk.Label(self.master, text='Enter Username: ').grid(row=0, column=0)
        tk.Label(self.master, text='Enter a Password:\n(optional)').grid(
            row=1, column=0)
        tk.Label(self.master, text='Confirm Password: ').grid(row=2, column=0)
        tk.Label(self.master, text='Select a User image:\n(optional) ').grid(
            row=3, column=0)

        e1 = tk.Entry(self.master, width=30)
        e1.grid(row=0, column=1)
        e2 = tk.Entry(self.master, width=30, show='*')
        e2.grid(row=1, column=1)
        e3 = tk.Entry(self.master, width=30, show='*')
        e3.grid(row=2, column=1)
        e4 = tk.Entry(self.master, width=30)
        e4.grid(row=3, column=1)
        e4.insert(0, f'{self.path}\\images\\guest.png')

        tk.Button(self.master, text='Browse pic', command=lambda win=self.master, entry=e4: self.master.browse_file(win=win,
            entry=entry)).grid(row=3, column=2)
        
        tk.Button(self.master, text='Submit', command=lambda name=e1, pwd=e2,
                  cpwd=e3, img=e4: self.save_new_user(None, name, pwd, cpwd, img)).grid(row=4, column=1)
        self.master.bind('<Return>', lambda event, name=e1, pwd=e2,
                  cpwd=e3, img=e4: self.save_new_user(event, name, pwd, cpwd, img))
        try:
            length = len(self.users)
            tk.Button(self.master, text='Cancel', command=self.create_frames).grid(row=4, column=0)
        except:
            pass