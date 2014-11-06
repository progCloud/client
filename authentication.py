import getpass
import json
import socket
import os.path
from os.path import expanduser
import settings
import protocol
# Gets user authentication details if present
# Otherwise asks from user
def authenticate_user(username,password):
    #fname = '~/.my_dropbox/secrets'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()        # Create a socket object
    host = settings.main_server
    port = settings.main_server_port
    s.connect((host, port))
    print username
    print password
    protocol.send_one_message(s, json.dumps({'email' : username, 'password' : password, 'req_type' : 'authentication'}) )
    status = protocol.recv_one_message(s)
    #print status
    s.close  
    print 'status is'  
    print status                # Close the socket when done
    return status

if __name__ == '__main__':
    print "Enter Username:",
    username = raw_input()
    password = getpass.getpass()
    print authenticate_user(username,password)
