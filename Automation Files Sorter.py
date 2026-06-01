# -*- coding: utf-8 -*-
"""
Created on Sun May 31 23:46:16 2026

@author: Hp
"""

from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
from logging import basicConfig, info, INFO
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


source_dir = r"C:\Users\Hp\Downloads\Source"
dest_dir = r"C:\Users\Hp\Downloads\Dest"


extensions = { 
            # ? supported image types
            'Sorted_Images' : [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                                ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"],
            # ? supported Video types
            'Sorted_Videos' : [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                                ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"],
            # ? supported Audio types
            'Sorted_Audios' : [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"],
            # ? supported Document types
            'Sorted_Documents' : [".doc", ".docx", ".odt",
                                   ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"]
            }



def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if not Path(f"{dest}").is_dir():
        Path(f"{dest}").mkdir(exist_ok=True)
        
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
        
    for x in range(10):
        try:
            move(entry, dest)
            break
        except:
            sleep(1)


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_files(entry, name)
                
    
    def check_files(self, entry, name):  # * Checks all Files
       
        ext = splitext(name)[-1]
               
        for file_type, lst in extensions.items():
            if ext.lower() in lst:
                dest = f"{dest_dir}\{file_type}"   
                break
        else:
            dest = f"{dest_dir}\Mixed_Files"   
            
        move_file(dest, entry, name)
        info(f"Moved {dest} file: {name}")  
                    


if __name__ == "__main__":
    basicConfig(level=INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
    