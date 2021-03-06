#! /usr/bin/python

from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.mp3 import MP3
import sys, os, fnmatch, time

def get_info(inf,funstuff,pattern,qbitrate):
    num_files = 0
    durate=0 ;
    for root, dirs, files in os.walk(inf):
        for nm in files:
            if fnmatch.fnmatch(nm.casefold(),pattern):
                try:
                    #if verbose: print("current file is: ",os.path.join(root,nm),end="\r")
                    if verbose: print(num_files," current file is:",os.path.join(root,nm),end="")
                    audio=funstuff(os.path.join(root,nm))
                    samplerate=audio.info.sample_rate
                    if qbitrate: biterate=audio.info.bitrate
                    durate += audio.info.length
                    num_files += 1
                    if verbose: print(' {0:8.2f}s'.format(audio.info.length))
                except:
                    if verbose: print("problem file is: ",os.path.join(root,nm))
                    continue
    if verbose: print("                                                             ",end="\r")
    return durate, num_files

def out_time(num,nam,out):
    if num: out.append(("%d"+nam) % num)

def print_info(duration,numb,tag):
    ''' prints the info about the found files in days, hours, ...
        No leap years yet - find something standard: import time ?? '''
    years=duration//3600//24//365 ; rest = duration-years*3600*24*365
    days=rest//3600//24 ; rest -= days*3600*24 ; hours=rest//3600
    rest -= hours*3600 ;  minutes=rest//60 ; rest -= minutes*60
    out=[tag,'='] ; out_time(years,"y",out) ; out_time(days,"d",out)
    out_time(hours,"h",out) ; out_time(minutes,"m",out) ; out_time(rest,"s",out)
    print('Number of ',tag,' files = ',numb, ', seconds = ',int(duration))
    if len(out) > 2: print('Total duration for',' '.join(out))


start_name='.'
verbose = False
# first parse the verbose - position dependent: must be first, otherwise ignored
num_args=len(sys.argv) ; arg_shift=0
if num_args > 1 :
    if sys.argv[1].find('-v') > -1:
        verbose = True
        arg_shift=1
if num_args < 2+arg_shift : print("Starting from current folder!")
else: start_name=sys.argv[1+arg_shift]

durate_flac,num_files_flac = get_info(start_name,FLAC,'*.flac',False)
print_info(durate_flac,num_files_flac,'flac')

durate_ogg,num_files_ogg = get_info(start_name,OggVorbis,'*.ogg',True)
print_info(durate_ogg,num_files_ogg,'ogg')

durate_mp3,num_files_mp3 = get_info(start_name,MP3,'*.mp3',True)
print_info(durate_mp3,num_files_mp3,'mp3')

durate=durate_flac+durate_ogg+durate_mp3
num_files=num_files_flac+num_files_ogg+num_files_mp3
print_info(durate,num_files,'all')

