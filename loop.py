import asyncore
import pyinotify
import client
import settings
from Tkinter import *

# Watches Directory specified by watch_dir
def watch_directory(watch_dir):
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_DELETE | pyinotify.IN_DELETE_SELF | pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVE_SELF | pyinotify.IN_OPEN | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM | pyinotify.IN_ISDIR
    
    def isValid(filename):
        a=filename.split('/');
        if (a[-1][0]=='.' or a[-1][-1]=='~' or a[-1]== "4913" ): #4913???
            return 0
        else:   
            #Now check if the level is not too deep
            root=settings.main_dir.split('/');
            return len(a)>=len(root) and len(a) <= len(root) + 2
   
    def isValidFolderDepth(filename):
       a=filename.split('/');
       root=settings.main_dir.split('/');
       return len(a) <= len(root) + 1

    class EventHandler(pyinotify.ProcessEvent):
     
        def process_IN_CREATE(self, event):
            filename=event.pathname
            if (isValid(filename)):
                #print "Adding:", filename, ", Folder: ", os.path.isdir(filename)
                if (event.dir):
                    if (isValidFolderDepth(filename)):
                        client.add_folder(filename)
                else:
                    pass
                    #client.add_file(filename)      #Uncomment to create empty files
  
        def process_IN_DELETE(self, event):
            filename=event.pathname
            if (isValid(filename)):
                print "Removing:", filename
                if (event.dir):
                    print "FOLDER"
                    if (isValidFolderDepth(filename)):
                       client.remove_folder(filename)
                else:
                    print "FILE"
                    client.remove_file(filename)

        def process_IN_CLOSE_WRITE(self, event):
            filename=event.pathname
            if (isValid(filename)):
                #print "Close Write:",filename
                client.add_file(filename)

        def process_IN_MOVE_SELF(self, event):
            pass
            # print "Move Self:", event.pathname

        def process_IN_MOVED_TO(self, event):
            filename=event.pathname
            if (isValid(filename)):
                #print "Move From:", filename
                if (event.dir):
                    if (isValidFolderDepth(filename)): 
                         client.add_folder(filename)
                else:
                    client.add_file(filename)

        def process_IN_MOVED_FROM(self, event):
            filename=event.pathname
            if (isValid(filename)):
                #print "Move From:", filename
                if (event.dir):
                    if (isValidFolderDepth(filename)): 
                         client.remove_folder(filename)
                else:
                    client.remove_file(filename)

        def process_IN_OPEN(self, event):
            pass
            # print "Open:", event.pathname

    #notifier = pyinotify.AsyncNotifier(wm, EventHandler())
    notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
    notifier.start()
    wdd = wm.add_watch(watch_dir, mask, rec=True, auto_add = True)
    #asyncore.loop()
    print 'GUI Starting'
    # Opens a popup where users can see status, pull etc
    # Saves the details in secrets file
    root = Tk()
    root.title('DROPBOX!!')
    root.minsize(width=200, height=100)
    def onpull():
        #Does a pull request
        #notifier.stop()
        client.pull()
        #notifier.start()
    def onclose():
        notifier.stop()
        root.destroy()
    def onpush():
        client.push()
    Button(root, text='PULL', command=onpull).pack(side=LEFT)
    Button(root, text='PUSH', command=onpush).pack(side=LEFT)
    Button(root, text='CLOSE', command=onclose).pack(side= BOTTOM)
    root.mainloop()
