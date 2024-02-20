import os
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import messagebox, ttk, colorchooser
from PIL import Image, ImageTk


class Add_Menu(tk.Toplevel):
    def __init__(self, desk, apps, userdict, username):
        tk.Toplevel.__init__(self, master=desk.master)
        self.desk = desk
        self.title('Add File')
        self.resizable(0, 0)
        #self.master = master
        tk.Label(self, text='File Name (or Alias) ').grid(row=0, column=0)
        tk.Label(self, text='File Location ').grid(row=1, column=0)
        tk.Label(self, text='Select Deskfolder').grid(row=3, column=0)
        self.names = tk.Entry(self, width=30)
        self.names.grid(row=0, column=1)

        self.locs = tk.Entry(self, width=30)
        self.locs.grid(row=1, column=1)

        tk.Button(self, text='Browse File', command=lambda win=self, entry=self.locs, entry2=self.names: 
            self.desk.master.browse_file(win=win, entry=entry, entry2=entry2)).grid(row=2, column=2)
        self.addvar = tk.IntVar(self, value=1)
        self.deskcheck = tk.Checkbutton(self, text='Add File to Desktop', variable=self.addvar,
                                        onvalue=1, offvalue=0)
        self.deskcheck.grid(row=2, column=0)
        self.myfiles = userdict[username]['myfiles']

        self.select_folder = ttk.Combobox(self, value=self.desk.get_deskfolders(), width=30)
        self.select_folder.current(0)
        self.select_folder.grid(row=3, column=1)

        tk.Button(self, text="Save", command=self.savefile).grid(
            row=4, column=1)

    def savefile(self):
        self.filename = self.names.get()
        self.add = self.locs.get()

        if self.filename and os.path.isfile(self.add):
            for i in self.myfiles:
                if i[0] == self.filename:
                    self.desk.set_dialogbox(text='Filename already exists..')
                    messagebox.showerror('Error!!', 'Filename already exists..')
                    break
            else:
                if self.addvar.get():
                    location = self.desk.get_empty()
                else:
                    location = None
                deskfolder = self.select_folder.get()
                deskfolder = deskfolder.replace('\\', '/')
                deskfolder = deskfolder.replace('//', '/')
                deskfolder = deskfolder.rstrip('/')
                if deskfolder and deskfolder[0] != '/':
                    deskfolder = '/' + deskfolder
                self.myfiles.append(
                    [self.filename, self.add, deskfolder, location])
                self.destroy()
                self.desk.create_maindesk()
                self.desk.save_to_DeskData()
        else:
            self.desk.set_dialogbox(
                text='Entered Filename or Address is Invalid!!')
            messagebox.showerror('Error!!', 'Entered Filename or Address is Invalid!!')


class My_File_Win(tk.Toplevel):
    def __init__(self, desk, userdict, username, apps):
        tk.Toplevel.__init__(self, master=desk.master)
        self.title('My Files')
        self.resizable(0,0)
        
        self.apps = apps
        self.desk = desk
        self.myfiles = userdict[username]['myfiles']

        self.verscrlbar = None
        self.tree = None
        self.frame1 = None
        self.search_entry = None
        self.rename_entry = None

        self.search = ''

        self.sort_myfiles(by='Name')

    def create_tree(self):
        self.desk.save_to_DeskData()
        columns = ('#1', '#2', '#3')
        heading = ('Name', 'Location', 'File Size', 'Desk Coordinates')
        for child in self.winfo_children():
            child.destroy()

        self.verscrlbar = ttk.Scrollbar(self, orient ="vertical") 
        self.verscrlbar.grid(row=0,column=1, sticky='ns')
        
        self.tree = ttk.Treeview(self, height=20, columns=columns, yscrollcommand = self.verscrlbar.set)
        self.tree.grid(row=0, column=0, sticky='news')

        self.verscrlbar.configure(command=self.tree.yview)

        self.tree.tag_bind('file', '<Double-Button-1>', self.on_double_click)
        self.tree.tag_bind('file', '<Button-3>', self.on_right_click)
        self.tree.tag_bind('folder', '<Button-3>', self.on_right_click)

        self.tree.images = []

        for i in range(len(heading)):
            self.tree.column(f'#{i}', minwidth=150)
            self.tree.heading(f'#{i}', text=heading[i], anchor='w', command=lambda by=heading[i]: self.sort_myfiles(by))
        
        self.frame1 = tk.Frame(self)
        self.frame1.grid(row=1, column=0, columnspan=2, sticky='ew')

        self.search_entry = tk.Entry(self.frame1, width=30)
        self.search_entry.grid(row=0, column=0)
        self.search_entry.insert(0, self.search)
        tk.Button(self.frame1, text='Search', command=self.search_items).grid(row=0, column=1)

        if self.search:
            self.search = self.search.lower()
        else:
            for i in self.desk.get_deskfolders()[1:]:
                loc = i.split('/')
                par = '/'.join(loc[:-1])
                self.tree.insert(parent=par, index='end', iid=i, text=loc[-1], tags='folder')
        for myfile in self.myfiles:
            if self.search and self.search not in myfile[0].lower() and self.search not in myfile[1].lower() and self.search not in myfile[2].lower() and self.search not in str(myfile[3]).lower():
                continue
            name = myfile[0]
            try:
                address = os.path.relpath(myfile[1])
            except:
                address = os.path.realpath(myfile[1])
            coord = str(myfile[3])
            deskfolder = myfile[2]

            ext = os.path.splitext(address)[1]
            try:
                size = f'{os.path.getsize(address)/1000} KB'
            except:
                size = '0 KB'

            for app in self.apps:
                if ext in self.apps[app]['ext']:
                    image = self.apps[app]['image']
                    break
            else:
                if ext == '.exe':
                    image = 'images/exe.png'
                elif ext:
                    image = 'images/question.png'
            pilimage = Image.open(image).resize((20,20))
            tkimage = ImageTk.PhotoImage(image=pilimage)
            self.tree.images.append(tkimage)

            if self.search:
                parent=''
            else:
                parent=deskfolder
            self.tree.insert(parent=parent, index='end', iid=name, image=tkimage, text=name, values=(address, size, coord), tags='file')

    def search_items(self):
        self.search = self.search_entry.get()
        self.create_tree()


    def on_double_click(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        add = values[0]
        ext = os.path.splitext(add)[1]
        for app in self.apps:
            if ext in self.apps[app]['ext']:
                def_cmd = self.apps[app]['default']
                if def_cmd:
                    cmd = self.apps[app]['filemenu'][def_cmd]
                else:
                    continue
                self.desk.run_command(cmd, app, add)
                break
        else:
            if ext == '.exe':
                self.desk.run_command(['<file>'], None, add)
            else:
                messagebox.showerror('Error!!', f'No apps for opening {ext}')
    def on_right_click(self, event):
        try:
            item = self.tree.selection()[0]
        except:
            return

        self.options = tk.Menu(self.tree, tearoff=0)
        cord_x, cord_y = event.x_root, event.y_root

        if self.tree.item(item, 'tags')[0] == 'folder':
            name = self.tree.item(item, 'text')
            parent = self.tree.parent(item)
            self.options.add_command(label=name)
            self.options.add_separator()
            self.options.add_separator()
            self.options.add_command(label='Rename', command=lambda name=name, parent=parent: self.rename_item(name, parent))
            self.options.add_command(label='Move To', command=lambda name=name, parent=parent: self.move_item(name, parent))
            self.options.add_command(label='Delete', command=lambda name=name, parent=parent: self.delete_folder(name, parent))
        else:
            values = self.tree.item(item, 'values')
            add = values[0]
            ext = os.path.splitext(add)[1]
            name = self.tree.item(item, 'text')
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
                    command=lambda app=app, add=add, win=self: self.desk.open_with(app, add, win))
                if ext in self.apps[app]['ext']:
                    for option in optiondict:
                        self.options.add_command(label=option, image=img, compound='left',
                            command=lambda cmd=optiondict[option], app=app, add=add: self.desk.run_command(cmd, app, add))
                    self.options.add_separator()
            if ext == '.exe':
                image = Image.open('images/exe.png').resize((20,20))
                image = ImageTk.PhotoImage(image=image)
                self.options.images.append(image)
                self.options.add_command(label='Start', image=image, compound='left', command=
                    lambda add=add: self.desk.run_command(['<file>'], None, add))
                self.options.add_separator()
            self.options.add_command(label='Rename', command=lambda name = name: self.rename_item(name))
            self.options.add_command(label='Move To', command=lambda name = name: self.move_item(name))
            self.options.add_command(label='Open File Location', command=
                lambda add=os.path.dirname(add): self.desk.run_command(['explorer', '<file>'], None, add))
            var = [1 if values[2]=='None' else 0][0]
            if var:    
                self.options.add_command(label='Add to Desktop', command=lambda name=name, var=var: self.add_to_desktop(name, var))
            else:
                self.options.add_command(label='Remove from Desktop', command=lambda name=name, var=var: self.add_to_desktop(name, var))
            self.options.add_command(label='Delete', command=lambda name=name, win=self: self.desk.delete_item(name, win))
        self.options.tk_popup(cord_x, cord_y)


    def delete_folder(self, name, parent):
        yesno = messagebox.askquestion('Confirm Delete', 'Deleting this will delete all files and folders under it. Are you sure?')
        if yesno == 'yes':
            folder = f'{parent}/{name}'
            for myfile in self.myfiles:
                if folder in myfile[2]:
                    self.myfiles.remove(myfile)
            self.desk.create_maindesk()
            self.create_tree()
            self.lift()

    def move_item(self, name, parent=None):
        self.rename_entry = ttk.Combobox(self, value=self.desk.get_deskfolders(), width=30)
        self.rename_entry.grid(row=1, column=0)
        self.rename_entry.current(0)
        tk.Button(self.frame1, text='Select Folder', command = lambda name=name, parent=parent:self.move_to(name, parent)).grid(row=1,column=1)

    def rename_item(self, name, parent=None):
        self.rename_entry = tk.Entry(self.frame1, width=30)
        self.rename_entry.grid(row=1, column=0)
        self.rename_entry.insert(0, name)
        tk.Button(self.frame1, text='Rename', command = lambda name=name, parent=parent:self.rename(name, parent)).grid(row=1,column=1)

    def move_to(self, name, parent):
        move = self.rename_entry.get()
        move = move.replace('\\', '/')
        move = move.replace('//', '/')
        move = move.rstrip('/')
        for myfile in self.myfiles:
            if not parent and parent != '':
                if myfile[0] == name:
                    myfile[2] = move
                    self.desk.create_maindesk()
                    self.create_tree()
                    break
            else:
                if myfile[2].find(move) == 0 or parent == '':
                    myfile[2] = myfile[2].replace(f'{parent}/{name}', f'{move}/{name}')
                    self.desk.create_maindesk()
                    self.create_tree()

    def rename(self, name, parent):
        rename = self.rename_entry.get()
        if not parent and parent != '':
            if rename and rename not in [myfile[0] for myfile in self.myfiles]:
                for myfile in self.myfiles:
                    if myfile[0] == name:
                        myfile[0] = rename
                        self.desk.create_maindesk()
                        self.create_tree()
                        break
                        
        else:
            path = f'{parent}/{name}'
            if rename:
                for myfile in self.myfiles:
                    if path in myfile[2]:
                        myfile[2] = myfile[2].replace(path, f'{parent}/{rename}')
                self.desk.create_maindesk()
                self.create_tree()

    def add_to_desktop(self, name, var):
        for x in self.myfiles:
            if x[0] == name:
                if var:
                    x[3] = self.desk.get_empty()
                else:
                    self.desk.deskno = x[3][0]
                    x[3] = None
                    if self.desk.get_deskitems() == {(i, j): ['disabled', '', '', ''] for i in range(8) for j in range(10)} :
                        for myfile in self.myfiles:
                            if myfile[3] and myfile[3][0] > self.desk.deskno:
                                myfile[3] = (myfile[3][0]-1, myfile[3][1], myfile[3][2])
                self.desk.create_maindesk()
                self.create_tree()
                
    def sort_myfiles(self, by):
        n = len(self.myfiles)
        for i in range(n):
            for j in range(n - i - 1):
                if by == 'Name':
                    r1 = self.myfiles[j][0].lower()
                    r2 = self.myfiles[j+1][0].lower()
                elif by == 'Location':
                    try:
                        r1 = os.path.splitext(self.myfiles[j][1])[1]
                    except:
                        r1 = 0
                    try:
                        r2 = os.path.splitext(self.myfiles[j+1][1])[1]
                    except:
                        r2 = 0
                elif by == 'File Size':
                    r1 = os.path.getsize(self.myfiles[j][1])
                    r2 = os.path.getsize(self.myfiles[j+1][1])
                else: # by == 'coordinates'
                    r1 = self.myfiles[j][3]
                    r2 = self.myfiles[j+1][3]
                    if r1 == None:
                        r1 = tuple()
                    if r2 == None:
                        r2 = tuple()
                
                if r1 > r2:
                    self.myfiles[j], self.myfiles[j+1] = self.myfiles[j+1], self.myfiles[j]
        self.create_tree()
        

class Settings_Win(tk.Toplevel):
    def __init__(self, desk, apps, userdict, username, users):
        tk.Toplevel.__init__(self, master=desk.master)
        self.title(f'Settings - {username}')
        self.geometry('400x400')

        self.desk = desk
        self.users = users
        self.userdict = userdict
        self.username = username

        self.frame1 = tk.PanedWindow(self)
        self.frame1.grid(row=0, sticky='news')
        self.create_frame_1()

        self.frame2 = tk.PanedWindow(self)
        self.frame2.grid(row=1, sticky='news')

        self.desk.master.equal(self)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def create_frame_1(self):
        self.desk.save_to_DeskData()

        tk.Label(self.frame1, text="Username:", width=20).grid(row=1, column=0, sticky='news')
        self.namelbl = tk.Button(self.frame1, text= self.username, width=20, relief='flat')
        self.namelbl.grid(row=1, column=1, sticky='news')
        tk.Label(self.frame1, text='Password:', width=20).grid(row=2, column=0, sticky='news')
        self.pwdlbl = tk.Button(self.frame1, text='*'*len(self.userdict[self.username]['password']), width=20, relief='flat')
        self.pwdlbl.grid(row=2, column=1, sticky='news')
        tk.Label(self.frame1, text='Theme:').grid(row=3, column=0, sticky='news')
        self.bglbl = tk.Button(self.frame1, bg=self.userdict[self.username]['bg'], width=5)
        self.bglbl.grid(row=3, column=1)


        image = Image.open(self.userdict[self.username]['image']).resize((100,100))
        image = ImageTk.PhotoImage(image=image)
        self.pic = tk.Label(self.frame1, image=image)
        self.pic.img = image
        self.pic.grid(row=0, column=0, columnspan=2, sticky='news')

        if self.username != 'Guest':
            self.pic.config(text='Click to change.', compound='top')
            self.pic.bind('<Button-1>', self.change_pic)
            self.namelbl.configure(command=self.change_username)
            self.pwdlbl.configure(command=self.change_pwd)
            tk.Button(self.frame1, text='RESET MY DESK', command=self.desk_reset).grid(row=4, column=0, sticky='news')
            tk.Button(self.frame1, text='TERMINATE USER', command=self.terminate_user).grid(row=4, column=1, sticky='news')
        self.bglbl.configure(command=self.change_bg)
        self.desk.master.equal(self.frame1)

    def change_username(self):
        for child in self.frame2.winfo_children():
            child.destroy()
        tk.Label(self.frame2, text='New Username:').grid(row=0, column=0)
        uname = tk.Entry(self.frame2, width=40)
        uname.insert(0, self.username)
        uname.grid(row=0, column=2)
        tk.Button(self.frame2, text='SAVE', command=lambda e1=uname: self.save_username(e1)).grid(row=1, column=1)
        self.desk.master.equal(self.frame2)

    def change_pwd(self):
        for child in self.frame2.winfo_children():
            child.destroy()
        tk.Label(self.frame2, text='Current Password:').grid(row=0, column=0)
        tk.Label(self.frame2, text='New Password:').grid(row=1, column=0)
        tk.Label(self.frame2, text='Confirm Password:').grid(row=2, column=0)
        cpwd = tk.Entry(self.frame2, width=40, show='*')
        cpwd.grid(row=0, column=1)
        npwd = tk.Entry(self.frame2, width=40, show='*')
        npwd.grid(row=1, column=1)
        vpwd = tk.Entry(self.frame2, width=40, show='*')
        vpwd.grid(row=2, column=1)
        tk.Button(self.frame2, text='SAVE', command=lambda e1=cpwd, e2=npwd, e3=vpwd: self.save_password(e1, e2, e3)).grid(row=3, column=0)
        self.desk.master.equal(self.frame2)

    def change_bg(self):
        color = colorchooser.askcolor(color= self.userdict[self.username]['bg'])[1]
        if color:
            self.userdict[self.username]['bg'] = color
            self.create_frame_1()
            self.desk.create_maindesk()
            self.desk.set_dialogbox(text='Theme changed')

        self.lift()

    def change_pic(self, event):
        pic = fd.askopenfilename()
        self.lift()
        if pic:
            self.userdict[self.username]['image'] = pic
            self.create_frame_1()

    def save_username(self, e1):
        if e1.get() and e1.get() not in self.userdict:
            self.userdict[e1.get()] = self.userdict[self.username]
            del self.userdict[self.username]
            for i in range(len(self.users)):
                if self.users[i] == self.username:
                    self.users[i] = e1.get()

            self.username = e1.get()
            self.desk.username = self.username
            self.title(f'Settings - {self.username}')

            for child in self.frame2.winfo_children():
                child.destroy()
            self.create_frame_1()

    def save_password(self, e1, e2, e3):
        if e1.get() == self.userdict[self.username]['password'] and e2.get() == e3.get():
            self.userdict[self.username]['password'] = e2.get()
            for child in self.frame2.winfo_children():
                child.destroy()
            self.create_frame_1()
    
    def desk_reset(self):
        yesno = messagebox.askoyesno('Confirm Reset', 'This will reset all of your Desk Data. Are you sure to proceed?')
        if yesno =='yes':
            self.userdict[self.username]['myfiles'] = self.userdict['Guest']['myfiles']
            self.userdict[self.username]['bg'] = self.userdict['Guest']['bg']

            self.create_frame_1()
            self.desk.create_maindesk()
            self.desk.set_dialogbox(text='Reset Successful')
    def terminate_user(self):
        yesno = messagebox.askquestion('Confirm Delete', 'This will delete your user and data permanentaly. Proceed?')
        if yesno == 'yes':
            del self.userdict[self.username]
            self.users.remove(self.username)
            self.desk.save_to_DeskData()
            self.desk.master.destroy()
