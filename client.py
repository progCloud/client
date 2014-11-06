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

# Sends file from client to server
def add_file(filename):
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
    a=filename.split('/');
    fo = open(settings.secrets_file, "r")
    email = fo.readline().rstrip()
    password = fo.readline().rstrip()
    watch_dir = fo.readline().rstrip()
    fo.close()
    url = urllib.pathname2url(filename)
    mimetype=mimetypes.guess_type(url)
    mimetype=str(mimetype[0])
    statinfo = os.stat(filename)
    timestamp = datetime.datetime.fromtimestamp(statinfo.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    print "Transferring file ", filename
    # print "Files in directory are:"
    # for i in custom_tools.parse_dir(settings.main_dir+'/'):
    #     print i['filename'],i['timestamp']
    protocol.send_one_message(s, json.dumps({'filename' : a[-1],'email':email,'password':password, 'req_type':'add_file','file_size':statinfo.st_size,'file_timestamp':timestamp,'content_type':mimetype,'dir_parse_json':custom_tools.parse_dir(settings.main_dir+'/')}))
    
    if (protocol.recv_one_message(s)=='1'):
        protocol.send_one_file(s,filename)
        # Pull Request Code
        # loop=int(protocol.recv_one_message(s))
        # print 'value of loop is', loop
        # protocol.send_one_message(s,'1')
        # reply = protocol.recv_one_message(s)
        # data = json.loads(reply)
        # print "Data Received is ", data
        # filename_list = data["filename_list"]
        # print filename_list
        # for x in range(0,len(filename_list)):
        #     filename=settings.main_dir+'/'+filename_list[x]
        #     if(protocol.recv_one_message(s)=='1'):
        #         print('about to recieve file'+filename)
        #         protocol.recv_one_file(s,filename)
        #     else:
        #         print('will not recieve file'+filename)
        #     protocol.send_one_message(s,'1')
        # print 'File Send (Send loop terminated)'
        s.close()
    else:
        print "You are not Authenticated"

def remove_file(filename):
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
    a=filename.split('/');
    fo = open(settings.secrets_file, "r")
    email = fo.readline().rstrip()
    password = fo.readline().rstrip()
    watch_dir = fo.readline().rstrip()
    fo.close()
    url = urllib.pathname2url(filename)
    mimetype=mimetypes.guess_type(url)
    mimetype=str(mimetype[0])
    statinfo = os.stat(filename)
    timestamp = datetime.datetime.fromtimestamp(statinfo.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    print "Transferring file ", filename
    protocol.send_one_message(s, json.dumps({'filename' : a[-1],'email':email,'password':password, 'req_type':'remove_file','file_size':statinfo.st_size,'file_timestamp':timestamp,'content_type':mimetype,'dir_parse_json':custom_tools.parse_dir(settings.main_dir+'/')}))

    if (protocol.recv_one_message(s)=='1'):
        # protocol.send_one_file(s,filename)
        s.close()
    else:
        print "You are not Authenticated"


if __name__ == '__main__':
    filename=sys.argv[1]
    client_call(filename)
