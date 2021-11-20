!pip install pytube mega.py

from pytube import YouTube, Playlist
import os, time, datetime
from mega import Mega

mega = Mega()
username = ""
password = ""
m = mega.login(username, password)

def dl_mega(path):
  file = m.upload(f'{os.listdir(path)[0]}')
  return m.get_upload_link(file)


def create_dir(name=None):
  # Directory
  directory = name or input('Enter name of folder: ') 

  # Parent Directory path
  parent_dir = "/content"
    
  # Path
  path = os.path.join(parent_dir, directory)

  # Path existence verification
  if not os.path.exists(path):  
    # Create the directory
    os.mkdir(path)
  
  return path


def display_qualities():
  print('Enter:\n[0] 720p\n[1] 480p\n[2] 360p\n[3] 240p\n[4] 144p')
  num = input('Qualiy: ')
  return num


def download_fn(num):
  res = ["720p", "480p", "360p", "240p", "144p"]

  if num.isdigit() and int(num) <= 4:
    num = int(num)
    begin = time.time()

    # playlist
    if str(url).find('playlist') > 0:
      yt = Playlist(url)
      filesize = 0
      path = create_dir(yt.title)
      for video in yt.videos:
        try:
          stream = video.streams.filter(res=res[num]).first()
          print(f"Downloading selected quality: {res[num]}")
        except:
          stream = video.streams.get_highest_resolution().first()
          print(f"Downloading highest quality")
        filesize += stream.filesize 
        stream.download(path)

    # Single
    else:
      yt = YouTube(url)
      try:
        stream = yt.streams.filter(res=res[num]).first()
        print(f"Downloading selected quality: {res[num]}")
      except:
        stream = yt.streams.get_highest_resolution()
        print(f"Downloading highest quality")

      filesize = stream.filesize
      stream.download(path)

    os.chdir(path)
    print(dl_mega(path))
    
    end = time.time()
    filesize = round(filesize/(1024*1024))

    print("Total size copied: ", filesize, " MB")
    print("Elapsed Time: ",int((end-begin)//60),"min :", int((end-begin)%60), "sec")
    print(datetime.datetime.now())  
    return None

  print('ENTER 0, 1, 2, 3 or 4')
  num = display_qualities()
  download_fn(num)


path = create_dir()

url = input('Video/Playlist URL: ')

num = display_qualities()
download_fn(num)