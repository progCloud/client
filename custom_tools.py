import socket
import sys
import settings
import json
import datetime
import time
import os

def isValid(filename):
        a=filename.split('/');
        if (a[-1][0]=='.' or a[-1][-1]=='~'):
            return 0
        else:
            return 1

def parse_dir(path):
    response = []
    for i, val in enumerate(os.listdir(path)):
        if (isValid(val)):
            statinfo = os.stat(path+val)
            st = datetime.datetime.fromtimestamp(statinfo.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            response.append({'filename': val, 'timestamp' : st})
    #print json.dumps(response)
    return response

if __name__ == '__main__':
    files_get('/home/siddhantmanocha/hadoop_dropbox/')
