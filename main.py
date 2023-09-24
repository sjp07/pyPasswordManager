import random
import webbrowser
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import back
import csv
from ttkbootstrap import *


class window:
    # these are lists of initialized characters
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    lc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
          'm', 'n', 'o', 'p', 'q',
          'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
          'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
          'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    sym = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|',
           '~', '>', '*', '<']

    def __init__(self, root, geo, title) -> None:
        self.root = root
        self.root.title(title)
        self.root.geometry(geo)
        self.root.resizable(width=False, height=False)

        Label(self.root, text='Your Password').grid(
            row=0, column=0, padx=10, pady=10)
        Label(self.root, text='Corresponding User_id').grid(
            row=1, column=0, padx=10, pady=10)
        Label(self.root, text='Of').grid(row=2, column=0, padx=10, pady=10)
        self.pa = StringVar()
        self.user_id = StringVar()
        self.site = StringVar()
        ttk.Entry(self.root, width=30, textvariable=self.pa
                  ).grid(row=0, column=1, padx=10, pady=10)
        ttk.Entry(self.root, width=30, textvariable=self.user_id
                  ).grid(row=1, column=1, padx=10, pady=10)
        ttk.Entry(self.root, width=30, textvariable=self.site
                  ).grid(row=2, column=1, padx=10, pady=10)
        self.length = StringVar()

        e = ttk.Combobox(self.root, values=['4', '8', '12', '16', '20', '24'],
                         textvariable=self.length)
        e.grid(row=0, column=2)
        e['state'] = 'readonly'
        self.length.set('Set password length')

        ttk.Button(self.root, text='Generate', padding=5,
                   style='success.Outline.TButton', width=20,
                   command=self.generate).grid(row=1, column=2)

        ttk.Button(self.root, text='Save to Database', style='success.TButton',
                   width=20, padding=5, command=self.save).grid(row=3, column=2)

        ttk.Button(self.root, text='Delete', width=20, style='danger.TButton',
                   padding=5, command=self.erase).grid(row=2, column=2)

        ttk.Button(self.root, text='Show All', width=20, padding=5,
                   command=self.view).grid(row=3, column=0)

        ttk.Button(self.root, text='Update', width=20, padding=5,
                   command=self.update).grid(row=3, column=1)

        # ========self.tree view=============
        self.tree = ttk.Treeview(self.root, height=20)
        self.tree['columns'] = ('site', 'user', 'pas')
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('site', width=160, anchor=W)
        self.tree.column('user', width=200, anchor=W)
        self.tree.column('pas', width=200, anchor=W)
        self.tree.heading('#0', text='')
        self.tree.heading('site', text='Site name', anchor=W)
        self.tree.heading('user', text='User Id', anchor=W)
        self.tree.heading('pas', text='Password', anchor=W)
        self.tree.grid(row=4, column=0, columnspan=3, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.catch)
        # this command will call the catch function

        # this is right click pop-up menu
        self.menu = Menu(self.root, tearoff=False)
        self.menu.add_command(label='Refresh', command=self.refresh)
        self.menu.add_command(label='Insert', command=self.save)
        self.menu.add_command(label='Update', command=self.update)
        self.menu.add_separator()
        self.menu.add_command(label='Show All', command=self.view)
        self.menu.add_command(label='Clear Fields', command=self.clear)
        self.menu.add_command(label='Clear Table', command=self.table)
        self.menu.add_command(label='Export', command=self.export)
        self.menu.add_separator()
        self.menu.add_command(label='Delete', command=self.erase)
        self.menu.add_command(label='Help', command=self.help)
        self.menu.add_separator()
        self.menu.add_command(label='Exit', command=self.root.quit)
        # this binds the button 3 of the mouse with
        self.root.bind("<Button-3>", self.poppin)

    # poppin function

    def help(self):
        # this function will open the help.txt in
        # notepad when called
        webbrowser.open('help.txt')

    def refresh(self):
        # this function basically refreshes the table
        # or tree view
        self.table()
        self.view()

    def table(self):
        # this function will clear all the values
        # displayed in the table
        for r in self.tree.get_children():
            self.tree.delete(r)

    def clear(self):
        # this function will clear all the entry
        # fields
        self.pa.set('')
        self.user_id.set('')
        self.site.set('')

    def poppin(self, e):
        # it triggers the right click pop-up menu
        self.menu.tk_popup(e.x_root, e.y_root)

    def catch(self, event):
        # this function will take all the selected data
        # from the table/ tree view and will fill up the
        # respective entry fields
        self.pa.set('')
        self.user_id.set('')
        self.site.set('')
        selected = self.tree.focus()
        value = self.tree.item(selected, 'value')
        self.site.set(value[0])
        self.user_id.set(value[1])
        self.pa.set(value[2])

    def update(self):
        # this function will update database with new
        # values given by the user
        selected = self.tree.focus()
        value = self.tree.item(selected, 'value')
        back.edit(self.site.get(), self.user_id.get(), self.pa.get())
        self.refresh()

    def view(self):
        # this will show all the data from the database
        # this is similar to "SELECT * FROM TABLE" sql
        # command
        if back.check() is False:
            messagebox.showerror('Attention Amigo!', 'Database is EMPTY!')
        else:
            for row in back.show():
                self.tree.insert(parent='', text='', index='end',
                                 values=(row[0], row[1], row[2]))

    def erase(self):
        # this will delete or remove the selected tuple or
        # row from the database
        selected = self.tree.focus()
        value = self.tree.item(selected, 'value')
        back.Del(value[2])
        self.refresh()

    def save(self):
        # this function will insert all the data into the
        # database
        back.enter(self.site.get(), self.user_id.get(), self.pa.get())
        self.tree.insert(parent='', index='end', text='',
                         values=(self.site.get(), self.user_id.get(), self.pa.get()))

    def generate(self):
        # this function will produce a random string which
        # will be used as password
        if self.length.get() == 'Set password length':
            messagebox.showerror('Attention!', "You forgot to SELECT")
        else:
            a = ''
            for x in range(int(int(self.length.get()) / 4)):
                a0 = random.choice(self.uc)
                a1 = random.choice(self.lc)
                a2 = random.choice(self.sym)
                a3 = random.choice(self.digits)
                a = a0 + a1 + a2 + a3 + a
                self.pa.set(a)

    def export(self):
        # this function will save all the data from the
        # database in a csv format which can be opened
        # in excel
        pop = Toplevel(self.root)
        pop.geometry('300x100')
        self.v = StringVar()
        Label(pop, text='Save File Name as').pack()
        ttk.Entry(pop, textvariable=self.v).pack()
        ttk.Button(pop, text='Save', width=18,
                   command=lambda: exp(self.v.get())).pack(pady=5)

        def exp(x):
            with open(x + '.csv', 'w', newline='') as f:
                chompa = csv.writer(f, dialect='excel')
                for r in back.show():
                    chompa.writerow(r)
            messagebox.showinfo("File Saved", "Saved as " + x + ".csv")


if __name__ == '__main__':
    win = Style(theme='darkly').master
    name = 'Password Generator'
    dimension = '800x600'

    app = window(win, dimension, name)
    win.mainloop()


