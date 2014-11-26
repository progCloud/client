import asyncore
import pyinotify
import client
from Tkinter import *

# Watches Directory specified by watch_dir
def watch_directory(watch_dir):
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_DELETE | pyinotify.IN_DELETE_SELF | pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVE_SELF | pyinotify.IN_OPEN | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM
    def isValid(filename):
        a=filename.split('/');
        if (a[-1][0]=='.' or a[-1][-1]=='~'):
            return 0
        else:
            return 1

    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CREATE(self, event):
            pass
            # print "Creating:", event.pathname

        def process_IN_DELETE(self, event):
            filename=event.pathname
            if (isValid(filename)):
                print "Removing:", event.pathname
                client.remove_file(filename)

        def process_IN_CLOSE_WRITE(self, event):
            filename=event.pathname
            if (isValid(filename)):
                print "Close Write:",event.pathname
                client.add_file(filename)            # Send file to server

        def process_IN_MOVE_SELF(self, event):
            pass
            # print "Move Self:", event.pathname

        def process_IN_MOVED_TO(self, event):
            filename=event.pathname
            if (isValid(filename)):
                print "Move To:", event.pathname
                client.add_file(filename)            # Send file to server

        def process_IN_MOVED_FROM(self, event):
            filename=event.pathname
            if (isValid(filename)):
                print "Move From:", event.pathname
                client.remove_file(filename)

        def process_IN_OPEN(self, event):
            pass
            # print "Open:", event.pathname

    #notifier = pyinotify.AsyncNotifier(wm, EventHandler())
    notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
    notifier.start()
    wdd = wm.add_watch(watch_dir, mask, rec=True)
    #asyncore.loop()
    print 'GUI Starting'
    # Opens a popup where users can see status, pull etc
    # Saves the details in secrets file
    root = Tk()
    root.title('DROPBOX!!')
    root.minsize(width=200, height=100)
    def onok():
        #Does a pull request
        client.pull()
    def onclose():
        notifier.stop()
        root.destroy()
    Button(root, text='PULL', command=onok).pack(side=LEFT)
    Button(root, text='CLOSE', command=onclose).pack(side= RIGHT)
    root.mainloop()
