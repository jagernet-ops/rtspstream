'''
Downloads simple rtsp server and runs in a thread, then sends video file using ffmpeg wrapper to the server

Execution:
python3 main.py [Video Path] [Port Forward Bool] 
'''
import ffmpeg
import threading
import pyngrok
import os
import platform
import argparse

parser = argparse.ArgumentParser(description='RTSP Streamer for local and external forwarding.')
parser.add_argument("Video Path", help="Whole path to the video you wish to stream.")
parser.add_argument("-f","--forwarding", help="Enable port forwarding using ngrok.",action="store_true")
args = parser.parse_args()
forward_bool = args.forwarding

def init():
    OSINFO = platform.system()
    if(OSINFO == 'Linux'):
        os.system("wget https://github.com/aler9/rtsp-simple-server/releases/download/v0.21.2/rtsp-simple-server_v0.21.2_linux_amd64.tar.gz")
        os.system("tar -xf rtsp-simple-server_v0.21.2_linux_amd64.tar.gz")
        os.system("touch .rtspInit")
    elif(OSINFO == 'Darwin'):
        os.system("wget https://github.com/aler9/rtsp-simple-server/releases/download/v0.21.2/rtsp-simple-server_v0.21.2_darwin_amd64.tar.gz")
        os.system("tar -xf rtsp-simple-server_v0.21.2_darwin_amd64.tar.gz")
        os.system("touch .rtspInit")
    elif(OSINFO == 'Windows'):
        os.system("wget https://github.com/aler9/rtsp-simple-server/releases/download/v0.21.2/rtsp-simple-server_v0.21.2_windows_amd64.zip")
        os.system("tar xf rtsp-simple-server_v0.21.2_windows_amd64.zip")
        os.system("type . > .rtspInit")

def startserver():
    if(forward_bool == False):
        os.system("./rtsp-simple-server")
    else:
        os.system("./rtsp-simple-server")
        forwarded = pyngrok.ngrok.connect(8554, 'tcp')
        print(forwarded)
        
def start():
    while(True):
        print("HELLO!")

serverthread = threading.Thread(target=startserver(), daemon=True)
videothread = threading.Thread(target=start())
    
if(os.path.isfile('.rtspInit') != True):
    init()

serverthread.start()
videothread.start()



