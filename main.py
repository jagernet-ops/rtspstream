'''
Downloads simple rtsp server and runs in a thread, then sends video file using ffmpeg wrapper to the server

usage: main.py [-h] [-f] [-t TOKEN] video_path

RTSP Streamer for local and external forwarding.

positional arguments:
  video_path            Whole path to the video you wish to stream.

options:
  -h, --help            show this help message and exit
  -f, --forwarding      Enable port forwarding using ngrok.
  -t TOKEN, --token TOKEN
                        Ngrok authentication token.
'''
import ffmpeg
import threading
from pyngrok import ngrok
import os
import platform
import argparse

bitrate = '1M'
parser = argparse.ArgumentParser(description='RTSP Streamer for local and external forwarding.')
parser.add_argument("video_path", help="Whole path to the video you wish to stream.")
parser.add_argument("-f","--forwarding", help="Enable port forwarding using ngrok.",action="store_true")
parser.add_argument("-t","--token", help="Ngrok authentication token.")
args = parser.parse_args()
forward_bool = args.forwarding


def init():
    OSINFO = platform.system()
    if(OSINFO == 'Linux'):
        os.system("wget https://github.com/aler9/rtsp-simple-server/releases/download/v0.21.2/rtsp-simple-server_v0.21.2_linux_amd64.tar.gz")
        os.system("tar -xf rtsp-simple-server_v0.21.2_linux_amd64.tar.gz")
        os.system("rm rtsp-simple-server_v0.21.2_linux_amd64.tar.gz")
        os.system("touch .rtspInit")
    elif(OSINFO == 'Darwin'):
        os.system("wget https://github.com/aler9/rtsp-simple-server/releases/download/v0.21.2/rtsp-simple-server_v0.21.2_darwin_amd64.tar.gz")
        os.system("tar -xf rtsp-simple-server_v0.21.2_darwin_amd64.tar.gz")
        os.system("rm rtsp-simple-server_v0.21.2_linux_amd64.tar.gz")
        os.system("touch .rtspInit")
    elif(OSINFO == 'Windows'):
        os.system("wget https://github.com/aler9/rtsp-simple-server/releases/download/v0.21.2/rtsp-simple-server_v0.21.2_windows_amd64.zip")
        os.system("tar xf rtsp-simple-server_v0.21.2_windows_amd64.zip")
        os.system("del /f rtsp-simple-server_v0.21.2_linux_amd64.tar.gz")
        os.system("type . > .rtspInit")
    print("Run this script once more to execute.")

def localserver():
    os.system("./rtsp-simple-server")

def forwardedserver():
    ngrok.set_auth_token(args.token)
    public_url = ngrok.connect(8554, 'tcp')
    print(public_url)
    os.system("./rtsp-simple-server")
    
def main():
    server_url = "rtsp://127.0.0.1:8554/librestream"
    print("Send this link: "+server_url)
    input_stream = ffmpeg.input(args.video_path)
    encoded_stream = input_stream.output(server_url, format='rtsp', vcodec='libx264', b=bitrate)  
    encoded_stream.run()

serverthread = threading.Thread(target=localserver)
forwardserverthread = threading.Thread(target=forwardedserver)
videothread = threading.Thread(target=main)
    
if(os.path.isfile('.rtspInit') != True):
    init()
else:
    if(forward_bool == True):
        forwardserverthread.start()
    else:
        serverthread.start()
    main()
