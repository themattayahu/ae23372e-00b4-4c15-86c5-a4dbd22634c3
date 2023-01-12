import requests
import uuid
import subprocess
import os
import sys
import logging
from time import sleep
from datetime import datetime
def is_live(channel):
    headers = {
        "Host": "gql.twitch.tv",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Content-Type": "text/plain;charset=UTF-8",
        "Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko",
    }
    data = '[{"operationName":"UseLive","variables":{"channelLogin":"'+channel+'"},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"639d5f11bfb8bf3053b424d9ef650d04c4ebb7d94711d644afb08fe9a0fad5d9"}}}]'
    response = requests.post("https://gql.twitch.tv/gql", headers=headers, data=data, verify=True).json()
    if response[0]["data"]["user"]["stream"]:
        return True
    else:
        return False
def convert(filename, id):
    command = "ffmpeg -i {} -c copy {} >/dev/null 2>&1".format(filename, id)
    output = subprocess.call(command, stdout=subprocess.PIPE, shell=True)
    if output == 0:
        return True
    else:
        return False
def delete(filename):
    try:
        os.remove(filename)
        return True
    except:
        return False
def recording(channel, filename):
    command = "streamlink twitch.tv/{} 720p60,720p,best -o {}".format(channel, filename)
    output = subprocess.call(command, stdout=subprocess.PIPE, shell=True)
    if output == 0:
        return True
    else:
        return False
def create_folder():
    if os.path.exists(os.getcwd()+"/vods"):
        return True
    try:
        os.mkdir(os.getcwd()+"/vods")
        return True
    except:
        return False
def vod_id():
    return str(uuid.uuid4())
if __name__ == '__main__':
    logging.basicConfig(filename="logs.txt", filemode="w", format="[%(asctime)s] %(message)s", datefmt="%d-%m-%y %H:%M:%S", level=logging.INFO)
    logging.info("[info]: Started archiving VODs!")
    if create_folder():
        logging.info("[info]: VODs folder created.\n")
    else:
        logging.info("[error]: Couldn't create VODs folder.")
        sys.exit()
    while True:
        channel = "surskity"
        vultr_file = vod_id()
        streamlink_file = vod_id()
        if is_live(channel):
            from_current = datetime.now()
            from_formatted = "{}-{:02}-{:02}T{:02}:{:02}:{:02}+00:00".format(from_current.year, from_current.month, from_current.day, from_current.hour, from_current.minute, from_current.second)
            logging.info("[info]: #{} is currently live, starting to record stream.".format(channel))
            if recording(channel, os.getcwd()+"/vods/"+streamlink_file+".ts"):
                logging.info("[info]: Ended recording VOD.")
                to_current = datetime.now()
                to_formatted = "{}-{:02}-{:02}T{:02}:{:02}:{:02}+00:00".format(to_current.year, to_current.month, to_current.day, to_current.hour, to_current.minute, to_current.second)
            else:
                logging.info("[error]: Something went wrong while executing streamlink.")
                sys.exit()
            if convert(os.getcwd()+"/vods/"+streamlink_file+".ts", os.getcwd()+"/vods/"+vultr_file+".mp4"):
                logging.info("[info]: Converting .ts streamlink file to .mp4, cutie.")
            else:
                logging.info("[error]: Couldn't convert .ts streamlink file to .mp4, i'm sorry.")
                sys.exit()
            if delete(os.getcwd() + "/vods/" + streamlink_file + ".ts"):
                logging.info("[info]: Deleting .ts streamlink file.")
            else:
                logging.info("[error]: Couldn't delete .ts streamlink file.")
                sys.exit()
            logging.info("[info]: You do the rest, here are the timestamps -> vod={}&from={}&to={}\n".format(vultr_file, from_formatted, to_formatted))
            sleep(5)
        else:
            sleep(5)
print("qc4pTjA3PZvTie3nvhhHcjmLXyRESLf")
print("RdcAS5wFSY4duLRsfzXPkHALvDH3fJT")
