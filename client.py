import socket
import sys
import settings
import json
import datetime
import time
import custom_tools
import os
import urllib, mimetypes
import protocol

#Establish Connection
def getSocket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()
    print 'Socket Created'
    port = settings.main_server_port
    host= settings.main_server
    s.connect(( host, port))
    print 'Socket connected to main server'
    return s

def getCredentials():
    fo = open(settings.secrets_file, "r")
    email = fo.readline().rstrip()
    password = fo.readline().rstrip()
    fo.close()
    return email,password

# Sends file from client to server
def add_file(filename):
    if (not os.path.isfile(filename)):
        return
    s = getSocket() 
  
    a=filename.split('/');
    root=settings.main_dir.split('/');
    folder = '.'
    if ( len(a) > len(root) + 1 ):
        folder = a[len(a)-2]
    print "Folder: ", folder
    
    email,password = getCredentials()

    url = urllib.pathname2url(filename)
    mimetype=mimetypes.guess_type(url)
    mimetype=str(mimetype[0])
    statinfo = os.stat(filename)
    timestamp = datetime.datetime.fromtimestamp(statinfo.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    print "Transferring file ", filename

    protocol.send_one_message(s, json.dumps({'filename' : a[-1],'foldername' : folder,'email':email,'password':password, 'req_type':'add_file','file_size':statinfo.st_size,'file_timestamp':timestamp,'content_type':mimetype,'dir_parse_json':custom_tools.parse_dir(settings.main_dir+'/')}))

    if (protocol.recv_one_message(s)=='1'):
        protocol.send_one_file(s,filename)
        reply = protocol.recv_one_message(s)
        print "Server Replied", reply
        s.close()
    else:
        print "You are not Authenticated"


#Adds folder
def add_folder(folder):
    s=getSocket()

    a=folder.split('/');
    email,password = getCredentials()

    print "Adding folder", a[-1]
   
    protocol.send_one_message(s, json.dumps({'foldername' : a[-1],'email':email,'password':password, 'req_type':'add_folder'}))

    if (protocol.recv_one_message(s)=='1'):
        reply = protocol.recv_one_message(s)
        print "Server Replied", reply
        s.close()
    else:
        print "You are not Authenticated"


#Removes folder
def remove_folder(folder):
    s=getSocket()

    a=folder.split('/');
    email,password = getCredentials()

    print "Removing folder", a[-1]
   
    protocol.send_one_message(s, json.dumps({'foldername' : a[-1],'email':email,'password':password, 'req_type':'delete_folder'}))

    if (protocol.recv_one_message(s)=='1'):
        reply = protocol.recv_one_message(s)
        print "Server Replied", reply
        s.close()
    else:
        print "You are not Authenticated"


#Removes file from server
def remove_file(filename):
    s = getSocket()

    a=filename.split('/');
    
    email,password = getCredentials()

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print "Deleting File ", filename
    
    root=settings.main_dir.split('/');
    folder = '.'
    if ( len(a) > len(root) + 1 ):
        folder = a[len(a)-2]
    print "Folder: ", folder
 

    protocol.send_one_message(s, json.dumps({'filename' : a[-1], 'foldername' : folder, 'email':email,'password':password, 'req_type':'delete_file','file_timestamp':timestamp}))
   
    if (protocol.recv_one_message(s)=='1'):
        reply = protocol.recv_one_message(s)
        print "Server Replied: ", reply
        s.close()
    else:
        print "You are not Authenticated"


#Pulls changes from the server
def pull():
    s = getSocket();
    email,password = getCredentials()
    protocol.send_one_message(s, json.dumps({'email':email,'password':password, 'req_type':'pull', 'dir_parse_json': custom_tools.parse_dir(settings.main_dir)}))
    if (protocol.recv_one_message(s)=='1'):
        print "Pulling Files..."
        print "Files in directory are:"
        for i in custom_tools.parse_dir(settings.main_dir+'/'):
            print i['filename'],i['foldername'],i['timestamp']
        
        num_files = int(protocol.recv_one_message(s))
        print 'Number of files to receive is ', num_files
       
        details = json.loads(protocol.recv_one_message(s))
        filename_list = details["filename_list"]
        foldername_list = details["foldername_list"]
        print filename_list
        print foldername_list
        for x in range(0,len(filename_list)):
            if(foldername_list[x] == ''):
                filename=settings.main_dir+'/'+filename_list[x]
            else:
                directory = settings.main_dir+'/'+foldername_list[x]+'/'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                filename=settings.main_dir+'/'+foldername_list[x]+'/'+filename_list[x]
            if(protocol.recv_one_message(s)=='1'):
                print('Receiving file with filename '+filename)
                protocol.recv_one_file(s,filename)
                print "received"
            else:
                print('Will not receive file with filename '+filename)
        s.close()
    else:
        print "You are not Authenticated"


#Pushes changes to the server
def push():
    print "Pushing"
    s = getSocket();
    email,password = getCredentials()
    protocol.send_one_message(s, json.dumps({'email':email,'password':password, 'req_type':'push', 'dir_parse_json': custom_tools.parse_dir(settings.main_dir)}))
    if (protocol.recv_one_message(s)=='1'):
        print "Pushing Files..."
        print "Files in directory are:"
        for i in custom_tools.parse_dir(settings.main_dir+'/'):
            print i['filename'],i['foldername'],i['timestamp']
        
        num_files = int(protocol.recv_one_message(s))
        print 'Number of files to send is ', num_files
       
        details = json.loads(protocol.recv_one_message(s))
        filename_list = details["filename_list"]
        foldername_list = details["foldername_list"]
        print filename_list
        s.close()
        for x in range(0,len(filename_list)):
            if(foldername_list[x] == ''):
                filename=settings.main_dir+'/'+filename_list[x]
            else:
                filename=settings.main_dir+'/'+foldername_list[x]+'/'+filename_list[x]
            print('Sending file with filename '+filename)
            if ( os.path.isdir(filename) ):
                add_folder(filename)
            else:
                add_file(filename)
    else:
        print "You are not Authenticated"


if __name__ == '__main__':
    filename=sys.argv[1]
    client_call(filename)
