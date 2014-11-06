from Tkinter import *
import main
import os
import settings

# Opens a popup where users can enter username, password etc.
# Saves the details in secrest file
def enter():
    print 'Your credentials does not exist'
    root = Tk()
    root.title('Authentication System')
    Label(text='Username').pack(side=TOP,padx=30,pady=10)
    username_input = Entry(root, width=30)
    username_input.pack(side=TOP,padx=10,pady=10)
    Label(text='Password').pack(side=TOP,padx=30,pady=10)
    password_input = Entry(root,show="*",width=30)
    password_input.pack(side=TOP,padx=10,pady=10)
    def onok():
        # Takes directory details from settings and creates them if they do not exist
        directory_1=settings.main_dir
        directory_2=settings.main_dir_hidden
        if not os.path.exists(directory_1):
            os.makedirs(directory_1)
        if not os.path.exists(directory_2):
            os.makedirs(directory_2)
        # 
        username = username_input.get()
        password = password_input.get()
        secrets_file = settings.secrets_file
        f = open(secrets_file, "w")
        f.write(username+'\n') # python will convert \n to os.linesep
        f.write(password+'\n') # python will convert \n to os.linesep
        f.write(directory_1+'\n')
        f.close() # you can omit in most cases as the destructor will call if
        root.destroy()
        main.main_func()
    def onclose():
        exit()
    Button(root, text='OK', command=onok).pack(side=LEFT)
    Button(root, text='CLOSE', command=onclose).pack(side= RIGHT)
    root.mainloop()
