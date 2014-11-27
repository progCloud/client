import socket
import sys
import settings
import json
import datetime
import time
import os

def isValid(filename):
    if (filename[0]=='.' or filename[-1]=='~'):
        return 0
    else:
        return 1


def parse_dir(path):
    response = []
    if path[-1] != '/':
        path += '/'
    for myFile in os.listdir(path):
        if (isValid(myFile)):
            if (os.path.isdir(path + myFile)):
                for myFile2 in os.listdir(path+myFile):
                    if (not os.path.isdir(path + myFile + '/' + myFile2)):
                        statinfo = os.stat(path+myFile + '/' + myFile2)
                        st = datetime.datetime.fromtimestamp(statinfo.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        response.append({'filename': myFile2, 'foldername': myFile,  'timestamp' : st})
            else:
                statinfo = os.stat(path+myFile)
                st = datetime.datetime.fromtimestamp(statinfo.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                response.append({'filename': myFile, 'foldername': '.',  'timestamp' : st})
    return response

if __name__ == '__main__':
    print parse_dir('/home/akshayaggarwal/hadoop_dropbox/')
