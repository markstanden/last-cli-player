""" An application to play a song and retreive information
    about the song from last.fm.
    For simplicity the songs provided are used
"""

# required command line ninjitsu
# pip3 install pylast

# the last.fm api
import pylast

# for file file handling
import io

# for the filename to call
#from sys import argv

import playsound as ps

def play_file (path_and_file):
    """ Plays the file sent the function"""

    ps.playsound(path_and_file)


def get_tags(path_and_file):
    """ Gets tags from the file, this is to identify
        the song to last.fm for scrobbling"""

    tags = {'Artist':'Unknown',
            'Album':'Unknown',
            'Track':'Unknown'
            }
    # tag lookup goes here     
    return tags


def get_lfm(artist, album, track)
    """ Looks up relevant information about track to be played
        returns a list of stuff """

    last_data = [artist, album, track]
    return last_data


    tags = get_tags(path_and_file)
    print(tags)


music_path = 'Music/' 
file1 = 'Gillicuddy_-_01_-_Adventure_Darling.mp3'
file2 = 'Kevin_MacLeod_-_08_-_Slow_Burn.mp3'

#ps.playsound('Music/Gillicuddy_-_01_-_Adventure_Darling.mp3')
#ps.playsound('Music/Kevin_MacLeod_-_08_-_Slow_Burn.mp3')

play_file(music_path + file1)